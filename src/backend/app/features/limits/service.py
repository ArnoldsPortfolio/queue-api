from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.errors import RateLimited
from app.kernel.ids import new_id
from app.models import RateRow
from app.settings import Settings
class LimitService:
    def __init__(self, db: Session):
        self.db = db
    def hit(self, key_id: str) -> None:
        since = datetime.utcnow() - timedelta(minutes=1)
        n = len(list(self.db.scalars(select(RateRow).where(RateRow.key_id == key_id, RateRow.at >= since))))
        if n >= Settings().rate_per_minute:
            raise RateLimited()
        self.db.add(RateRow(id=new_id(), key_id=key_id)); self.db.commit()
