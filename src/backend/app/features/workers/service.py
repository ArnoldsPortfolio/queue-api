import hashlib, hmac, json
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import JobRow, WebhookRow
from app.settings import Settings
HANDLERS = {
    "echo": lambda p: p,
    "upper": lambda p: {"text": str(p.get("text", "")).upper()},
    "fail": lambda p: (_ for _ in ()).throw(RuntimeError(p.get("message", "forced fail"))),
}
class WorkerService:
    def __init__(self, db: Session):
        self.db = db
    def tick(self, n: int = 5) -> list[dict]:
        now = datetime.utcnow()
        jobs = list(self.db.scalars(select(JobRow).where(JobRow.status == "queued", JobRow.run_after <= now).limit(n)))
        return [self._run(job) for job in jobs]
    def _run(self, job: JobRow) -> dict:
        job.attempts += 1
        job.status = "running"
        try:
            job.result = json.dumps(HANDLERS.get(job.kind, HANDLERS["echo"])(json.loads(job.payload or "{}")))
            job.status = "done"
            job.error = ""
            self._hook(job)
        except Exception as exc:
            job.error = str(exc)
            job.status = "dead" if job.attempts >= Settings().max_attempts else "queued"
        self.db.commit()
        return {"id": job.id, "status": job.status, "attempts": job.attempts}
    def _hook(self, job: JobRow) -> None:
        hooks = list(self.db.scalars(select(WebhookRow).where(WebhookRow.owner_id == job.owner_id)))
        body = json.dumps({"job_id": job.id, "status": job.status, "result": job.result})
        for hook in hooks:
            hmac.new(hook.secret.encode(), body.encode(), hashlib.sha256).hexdigest()
