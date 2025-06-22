from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from main import run_hiring_system
from hiring_agents.pdf_parser import PDFParser

app = FastAPI(
    title="Hiring Agent System API",
    description="API to interact with the uAgents-based hiring system.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate-candidate")
async def evaluate_candidate(
    candidate_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    """
    Endpoint to trigger the full hiring evaluation pipeline.
    """
    try:
        # Read resume file content
        file_content = await resume_file.read()

        # Check file type and extract text accordingly
        if resume_file.content_type == "application/pdf":
            print("📄 Parsing PDF file...")
            resume_content = PDFParser.extract_text_from_pdf(file_content)
            if not resume_content:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
        elif resume_file.content_type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        ]:
            # Placeholder for future Word document parsing
            raise HTTPException(
                status_code=501,
                detail="DOC/DOCX file parsing is not yet implemented.",
            )
        else:
            # Assume plain text for other file types
            print("📄 Reading text file...")
            resume_content = file_content.decode("utf-8", errors="ignore")

        print("🚀 Kicking off the hiring agent pipeline and awaiting results...")
        
        final_result = await run_hiring_system(
            resume_content=resume_content,
            job_description=job_description,
            candidate_name=candidate_name,
            job_title=job_title,
        )
        
        if not final_result:
            raise HTTPException(status_code=500, detail="Pipeline did not return a result.")

        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 