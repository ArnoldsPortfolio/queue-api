import json
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.errors import NotFound
from app.kernel.ids import new_id
from app.models import JobRow
class JobService:
    def __init__(self, db: Session):
        self.db = db
    def submit(self, owner_id: str, kind: str, payload: dict, key: str = "", delay_sec: int = 0) -> dict:
        if key:
            found = self.db.scalar(select(JobRow).where(JobRow.owner_id == owner_id, JobRow.idempotency_key == key))
            if found:
                return _out(found)
        job = JobRow(id=new_id(), owner_id=owner_id, kind=kind, payload=json.dumps(payload), idempotency_key=key, run_after=datetime.utcnow() + timedelta(seconds=delay_sec))
        self.db.add(job); self.db.commit()
        return _out(job)
    def get(self, owner_id: str, job_id: str) -> dict:
        job = self.db.get(JobRow, job_id)
        if not job or job.owner_id != owner_id:
            raise NotFound("Job not found")
        return _out(job)
    def list(self, owner_id: str, status: str | None = None) -> list[dict]:
        q = select(JobRow).where(JobRow.owner_id == owner_id)
        if status:
            q = q.where(JobRow.status == status)
        return [_out(j) for j in self.db.scalars(q)]
def _out(job: JobRow) -> dict:
    return {"id": job.id, "kind": job.kind, "status": job.status, "attempts": job.attempts, "result": job.result, "error": job.error, "payload": json.loads(job.payload or "{}")}
