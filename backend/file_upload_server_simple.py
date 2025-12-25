
import asyncio
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import our custom modules
from helper_func.pdf_parser import PDFParser
from helper_func.llm_client import SimpleLLMAgent
from db.supabase_client import HiringEvaluationsClient


app = FastAPI(title="Resume Upload Server (Simple)", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_client = HiringEvaluationsClient()

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    candidate_name: str = Form(...),
    job_title: str = Form(default="To Be Determined")  # Default job title
):
    
    try:
        # Validate file type
        print(f"📤 Processing resume for {candidate_name}")
        print(f"📄 File: {file.filename}")
        print(f"📄 Job Title: {job_title}")
        print(f"📄 Candidate Name: {candidate_name}")
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension != 'pdf':
            raise HTTPException(
                status_code=400, 
                detail="Only PDF files are supported in this simple version"
            )
        
        # Read file content and extract text
        file_content = await file.read()
        resume_text = PDFParser.extract_text_from_pdf(file_content)
        
        if not resume_text:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract text from PDF file"
            )
        
        print(f"📤 Processing resume for {candidate_name}")
        print(f"📄 Extracted {len(resume_text)} characters from PDF")
        
        # Use LLM to analyze resume
        llm_agent = SimpleLLMAgent("resume_analyzer")
        
        prompt = f"""
        Analyze this resume and create a summary for hiring evaluation.
        
        Candidate: {candidate_name}
        Job Title: {job_title}
        Resume Content:
        {resume_text}
        
        Provide a JSON response with:
        {{
            "resume_summary": "<2-3 sentence summary of candidate's background>",
            "key_skills": ["skill1", "skill2", "skill3"],
            "experience_level": "<Junior/Mid-level/Senior>",
            "years_experience": <number>
        }}
        """
        
        result = await llm_agent.query_llm(prompt)
        
        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])
                
                if analysis:
                    resume_summary = analysis.get("resume_summary", f"Resume analysis for {candidate_name}")
                    
                    print(f"✅ Analysis completed for {candidate_name}")
                    print(f"📊 Summary: {resume_summary[:100]}...")
                    
                    # 💾 SAVE TO HIRING_EVALUATIONS TABLE (partial record with full resume text)
                    # This creates a partial evaluation record that can be completed later
                    evaluation_record = await supabase_client.create_evaluation(
                        resume_id=None,  # We don't have separate resumes table
                        candidate_name=candidate_name,
                        job_title=job_title,
                        resume_summary=resume_summary,
                        resume_text=resume_text,  # 🆕 FULL RESUME TEXT STORED HERE!
                        job_summary=None,  # Will be filled when job is analyzed
                        intersection_score=None,  # Will be calculated during hiring process
                        intersection_notes=None,  # Will be filled during hiring process
                        pro_arguments=None,  # Will be filled during debate
                        anti_arguments=None,  # Will be filled during debate
                        final_decision=None,  # Will be decided during hiring process
                        decision_confidence=None,  # Will be calculated during hiring process
                        decision_reasoning=None  # Will be filled during hiring process
                    )
                    
                    response_data = {
                        "evaluation_id": evaluation_record["id"],
                        "candidate_name": candidate_name,
                        "job_title": job_title,
                        "resume_summary": resume_summary,
                        "skills": analysis.get("key_skills", []),
                        "experience_level": analysis.get("experience_level", "Unknown"),
                        "years_experience": analysis.get("years_experience", 0),
                        "status": "resume_parsed",
                        "next_step": "ready_for_hiring_evaluation"
                    }
                    
                    print(f"💾 Saved to hiring_evaluations with ID: {evaluation_record['id']}")
                    
                else:
                    # Fallback if LLM parsing fails
                    resume_summary = f"Resume uploaded for {candidate_name}. Manual review required."
                    
                    evaluation_record = await supabase_client.create_evaluation(
                        resume_id=None,
                        candidate_name=candidate_name,
                        job_title=job_title,
                        resume_summary=resume_summary,
                        resume_text=resume_text
                    )
                    
                    response_data = {
                        "evaluation_id": evaluation_record["id"],
                        "candidate_name": candidate_name,
                        "job_title": job_title,
                        "resume_summary": resume_summary,
                        "status": "resume_uploaded",
                        "note": "LLM analysis failed, manual review needed"
                    }
                
                return JSONResponse(content=response_data)
                
            except Exception as e:
                print(f"❌ Error processing analysis: {e}")
                # Still try to save basic info
                basic_summary = f"Resume uploaded for {candidate_name} on {datetime.now().strftime('%Y-%m-%d')}"
                
                evaluation_record = await supabase_client.create_evaluation(
                    resume_id=None,
                    candidate_name=candidate_name,
                    job_title=job_title,
                    resume_summary=basic_summary,
                    resume_text=resume_text
                )
                
                return JSONResponse(content={
                    "evaluation_id": evaluation_record["id"],
                    "candidate_name": candidate_name,
                    "job_title": job_title,
                    "resume_summary": basic_summary,
                    "status": "basic_upload",
                    "error": "Analysis failed but resume was saved"
                })
        else:
            raise HTTPException(
                status_code=500,
                content={
                    "error": "LLM API error",
                    "details": result['content']
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/evaluations")
async def list_evaluations():
    """Get all hiring evaluations (including partial ones from resume uploads)."""
    try:
        evaluations = await supabase_client.get_recent_evaluations(limit=100)
        
        return {
            "total_evaluations": len(evaluations),
            "evaluations": [
                {
                    "evaluation_id": eval["id"],
                    "candidate_name": eval["candidate_name"],
                    "job_title": eval["job_title"],
                    "resume_summary": eval.get("resume_summary", "")[:100] + "..." if eval.get("resume_summary") and len(eval.get("resume_summary", "")) > 100 else eval.get("resume_summary", ""),
                    "final_decision": eval.get("final_decision"),
                    "created_at": eval["created_at"],
                    "status": "complete" if eval.get("final_decision") else "partial"
                }
                for eval in evaluations
            ]
        }
    except Exception as e:
        print(f"❌ Error fetching evaluations: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/evaluation/{evaluation_id}")
async def get_evaluation(evaluation_id: str):
    """Get full evaluation data by ID."""
    try:
        evaluation = await supabase_client.get_evaluation(evaluation_id)
        
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        return evaluation
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching evaluation: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "simple_resume_upload_server"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 