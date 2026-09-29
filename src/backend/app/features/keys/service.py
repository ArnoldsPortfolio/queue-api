import hashlib, secrets
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.errors import NotFound, Unauthorized
from app.kernel.ids import new_id
from app.models import ApiKeyRow
class KeyService:
    def __init__(self, db: Session):
        self.db = db
    def issue(self, owner_id: str, name: str) -> dict:
        raw = "qk_" + secrets.token_urlsafe(24)
        row = ApiKeyRow(id=new_id(), owner_id=owner_id, name=name[:80], prefix=raw[:10], secret_hash=_hash(raw))
        self.db.add(row); self.db.commit()
        return {"id": row.id, "name": row.name, "prefix": row.prefix, "token": raw, "revoked": False}
    def list(self, owner_id: str) -> list[dict]:
        rows = self.db.scalars(select(ApiKeyRow).where(ApiKeyRow.owner_id == owner_id))
        return [{"id": r.id, "name": r.name, "prefix": r.prefix, "revoked": bool(r.revoked)} for r in rows]
    def revoke(self, owner_id: str, key_id: str) -> dict:
        row = self.db.get(ApiKeyRow, key_id)
        if not row or row.owner_id != owner_id:
            raise NotFound("Key not found")
        row.revoked = 1; self.db.commit()
        return {"id": row.id, "revoked": True}
    def resolve(self, token: str) -> ApiKeyRow:
        row = self.db.scalar(select(ApiKeyRow).where(ApiKeyRow.prefix == token[:10], ApiKeyRow.revoked == 0))
        if not row or row.secret_hash != _hash(token):
            raise Unauthorized("Bad API key")
        return row
def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()
