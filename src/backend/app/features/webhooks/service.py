import secrets
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.ids import new_id
from app.models import WebhookRow
class WebhookService:
    def __init__(self, db: Session):
        self.db = db
    def add(self, owner_id: str, url: str) -> dict:
        row = WebhookRow(id=new_id(), owner_id=owner_id, url=url[:300], secret=secrets.token_hex(16))
        self.db.add(row); self.db.commit()
        return {"id": row.id, "url": row.url, "secret": row.secret}
    def list(self, owner_id: str) -> list[dict]:
        return [{"id": r.id, "url": r.url} for r in self.db.scalars(select(WebhookRow).where(WebhookRow.owner_id == owner_id))]
