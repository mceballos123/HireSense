from fastapi import FastAPI
from api.job_postings import router as job_postings_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(job_postings_router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
