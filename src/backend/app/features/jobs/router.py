from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.jobs.service import JobService
router = APIRouter(prefix="/jobs", tags=["jobs"])
class SubmitBody(BaseModel):
    kind: str = Field(default="echo")
    payload: dict = Field(default_factory=dict)
    idempotency_key: str = ""
    delay_sec: int = 0
@router.get("")
def list_jobs(status: str | None = None, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return JobService(db).list(user_id, status)
@router.post("")
def submit(body: SubmitBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return JobService(db).submit(user_id, body.kind, body.payload, body.idempotency_key, body.delay_sec)
@router.get("/{job_id}")
def get_job(job_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return JobService(db).get(user_id, job_id)
