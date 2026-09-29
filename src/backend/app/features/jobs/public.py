from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db
from app.features.jobs.service import JobService
from app.features.keys.service import KeyService
from app.features.limits.service import LimitService
from app.models import ApiKeyRow
router = APIRouter(prefix="/v1", tags=["public"])
class SubmitBody(BaseModel):
    kind: str = "echo"
    payload: dict = Field(default_factory=dict)
    delay_sec: int = 0
def api_key(x_api_key: str | None = Header(default=None), db: Session = Depends(get_db)) -> ApiKeyRow:
    return KeyService(db).resolve(x_api_key or "")
@router.post("/jobs")
def public_submit(body: SubmitBody, key: ApiKeyRow = Depends(api_key), db: Session = Depends(get_db), idempotency_key: str | None = Header(default="", alias="Idempotency-Key")):
    LimitService(db).hit(key.id)
    return JobService(db).submit(key.owner_id, body.kind, body.payload, idempotency_key or "", body.delay_sec)
@router.get("/jobs/{job_id}")
def public_get(job_id: str, key: ApiKeyRow = Depends(api_key), db: Session = Depends(get_db)):
    return JobService(db).get(key.owner_id, job_id)
