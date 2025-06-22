from fastapi import APIRouter, HTTPException
from db.supabase_client import HiringEvaluationsClient

router = APIRouter()
client = HiringEvaluationsClient()


@router.post("/job-postings")
async def create_job_posting(payload: dict):
    try:
        job = await client.create_job_posting(**payload)
        return job
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/job-postings")
async def list_job_postings(status: str = "ACTIVE", limit: int = 20):
    jobs = await client.list_job_postings(status=status, limit=limit)
    return jobs


@router.get("/job-postings/{job_id}")
async def get_job_posting(job_id: str):
    job = await client.get_job_posting(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.patch("/job-postings/{job_id}")
async def update_job_posting(job_id: str, payload: dict):
    job = await client.update_job_posting(job_id, **payload)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not updated")
    return job


@router.delete("/job-postings/{job_id}")
async def delete_job_posting(job_id: str):
    deleted = await client.delete_job_posting(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found or not deleted")
    return {"success": True}
