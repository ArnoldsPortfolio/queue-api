from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.workers.service import WorkerService
router = APIRouter(prefix="/worker", tags=["worker"])
@router.post("/tick")
def tick(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return WorkerService(db).tick()
