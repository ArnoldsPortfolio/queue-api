from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.keys.service import KeyService
router = APIRouter(prefix="/keys", tags=["keys"])
class NameBody(BaseModel):
    name: str = "default"
@router.get("")
def list_keys(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return KeyService(db).list(user_id)
@router.post("")
def issue_key(body: NameBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return KeyService(db).issue(user_id, body.name)
@router.post("/{key_id}/revoke")
def revoke_key(key_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return KeyService(db).revoke(user_id, key_id)
