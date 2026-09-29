from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.webhooks.service import WebhookService
router = APIRouter(prefix="/webhooks", tags=["webhooks"])
class UrlBody(BaseModel):
    url: str
@router.get("")
def list_hooks(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return WebhookService(db).list(user_id)
@router.post("")
def add_hook(body: UrlBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return WebhookService(db).add(user_id, body.url)
