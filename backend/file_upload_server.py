"""
File Upload Server
==================

FastAPI server for handling resume file uploads and processing them through the hiring agents.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List
from datetime import datetime
import uuid

from hiring_agents.pdf_parser import PDFParser
from hiring_agents.llm_client import SimpleLLMAgent

app = FastAPI(title="Resume Upload API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory storage (will be replaced with database)
resume_database = {}  # candidate_id -> resume_data
candidate_index = {}  # candidate_name -> candidate_id

def save_resume_data(candidate_name: str, resume_text: str, analysis_result: dict, filename: str) -> str:
    """
    Save resume data to temporary storage.
    Returns candidate_id for future reference.
    """
    candidate_id = str(uuid.uuid4())
    
    resume_data = {
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
        "original_filename": filename,
        "resume_text": resume_text,
        "text_length": len(resume_text),
        "upload_timestamp": datetime.now().isoformat(),
        "analysis": analysis_result,
        "status": "processed"
    }
    
    # Store in our temporary database
    resume_database[candidate_id] = resume_data
    candidate_index[candidate_name.lower()] = candidate_id
    
    print(f"💾 Saved resume data for {candidate_name} (ID: {candidate_id[:8]}...)")
    print(f"📊 Database now contains {len(resume_database)} resumes")
    
    return candidate_id


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    candidate_name: str = Form(...)
):
    """
    Upload and process a resume file.
    
    Args:
        file: The uploaded resume file (PDF, DOC, DOCX)
        candidate_name: Name of the candidate
        
    Returns:
        JSON response with parsed resume data and candidate_id
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension not in ['pdf', 'doc', 'docx']:
            raise HTTPException(
                status_code=400, 
                detail="Only PDF, DOC, and DOCX files are supported"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        resume_text = ""
        if file_extension == 'pdf':
            resume_text = PDFParser.extract_text_from_pdf(file_content)
            if not resume_text:
                raise HTTPException(
                    status_code=400, 
                    detail="Could not extract text from PDF file"
                )
        else:
            # For DOC/DOCX files, we'll need additional parsing
            # For now, return an error message
            raise HTTPException(
                status_code=400, 
                detail="DOC/DOCX parsing not yet implemented. Please use PDF files."
            )
        
        print(f"📤 Processing resume for {candidate_name}")
        print(f"📄 Extracted {len(resume_text)} characters from PDF")
        
        # Use LLM client directly for processing
        llm_agent = SimpleLLMAgent("file_upload_processor")
        
        prompt = f"""
        Analyze the following resume and extract key information.
        
        Candidate Name: {candidate_name}
        Resume Content:
        {resume_text}
        
        Extract and analyze:
        1. Technical skills (programming languages, frameworks, tools)
        2. Years of experience
        3. Experience level (Junior, Mid-level, Senior)
        4. Key achievements and accomplishments
        
        Respond with ONLY a JSON object in this exact format:
        {{
            "skills": ["skill1", "skill2", "skill3"],
            "experience_years": <number>,
            "experience_level": "<Junior/Mid-level/Senior>",
            "key_achievements": ["achievement1", "achievement2"],
            "analysis": "<brief analysis of the candidate's profile>"
        }}
        """
        
        result = await llm_agent.query_llm(prompt)
        
        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])
                
                if analysis:
                    response_data = {
                        "candidate_name": candidate_name,
                        "skills": analysis.get("skills", ["python", "javascript", "react"]),
                        "experience_years": analysis.get("experience_years", 3),
                        "experience_level": analysis.get("experience_level", "Mid-level"),
                        "key_achievements": analysis.get("key_achievements", ["Led development team"]),
                        "analysis": analysis.get("analysis", "Resume analysis completed"),
                        "status": "success"
                    }
                    
                    # 💾 SAVE THE RESUME DATA (NEW!)
                    candidate_id = save_resume_data(
                        candidate_name=candidate_name,
                        resume_text=resume_text,
                        analysis_result=response_data,
                        filename=file.filename
                    )
                    
                    # Add candidate_id to response
                    response_data["candidate_id"] = candidate_id
                    
                    print(f"✅ Analysis completed for {candidate_name}")
                    print(f"📊 Skills: {response_data['skills']}")
                    print(f"📊 Experience: {response_data['experience_level']} ({response_data['experience_years']} years)")
                else:
                    response_data = {
                        "candidate_name": candidate_name,
                        "skills": ["python", "javascript", "react"],
                        "experience_years": 3,
                        "experience_level": "Mid-level",
                        "key_achievements": ["Led development team"],
                        "analysis": "Failed to parse LLM response, using defaults",
                        "status": "partial_success"
                    }
                    
                    # Still save the raw text even if analysis failed
                    candidate_id = save_resume_data(
                        candidate_name=candidate_name,
                        resume_text=resume_text,
                        analysis_result=response_data,
                        filename=file.filename
                    )
                    response_data["candidate_id"] = candidate_id
                
                return JSONResponse(content=response_data)
                
            except Exception as e:
                print(f"❌ Error processing LLM response: {e}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "error": "Failed to process resume",
                        "details": str(e),
                        "status": "error"
                    }
                )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "LLM API error",
                    "details": result['content'],
                    "status": "error"
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/resumes")
async def list_resumes():
    """Get all stored resumes (for debugging/admin purposes)."""
    return {
        "total_resumes": len(resume_database),
        "resumes": [
            {
                "candidate_id": data["candidate_id"],
                "candidate_name": data["candidate_name"],
                "upload_timestamp": data["upload_timestamp"],
                "text_length": data["text_length"],
                "experience_level": data["analysis"].get("experience_level", "Unknown"),
                "skills_count": len(data["analysis"].get("skills", []))
            }
            for data in resume_database.values()
        ]
    }


@app.get("/resume/{candidate_id}")
async def get_resume(candidate_id: str):
    """Get full resume data by candidate ID."""
    if candidate_id not in resume_database:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return resume_database[candidate_id]


@app.post("/search-resumes")
async def search_resumes(skills: List[str] = None, experience_level: str = None, min_years: int = None):
    """
    Search resumes by criteria.
    This is a preview of what the database search will look like.
    """
    results = []
    
    for candidate_id, data in resume_database.items():
        match = True
        analysis = data["analysis"]
        
        # Filter by skills
        if skills:
            candidate_skills = [skill.lower() for skill in analysis.get("skills", [])]
            required_skills = [skill.lower() for skill in skills]
            if not any(req_skill in candidate_skills for req_skill in required_skills):
                match = False
        
        # Filter by experience level
        if experience_level:
            if analysis.get("experience_level", "").lower() != experience_level.lower():
                match = False
        
        # Filter by minimum years
        if min_years:
            if analysis.get("experience_years", 0) < min_years:
                match = False
        
        if match:
            results.append({
                "candidate_id": candidate_id,
                "candidate_name": data["candidate_name"],
                "skills": analysis.get("skills", []),
                "experience_level": analysis.get("experience_level", "Unknown"),
                "experience_years": analysis.get("experience_years", 0),
                "match_score": 1.0  # Simple match for now
            })
    
    return {"results": results, "total_matches": len(results)}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "message": "Resume upload server is running",
        "stored_resumes": len(resume_database)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 