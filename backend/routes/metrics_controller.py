from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from models import User
from utils import get_current_professor_or_admin_user
from metrics import get_student_metrics, get_group_metrics

metrics_controller = APIRouter()

@metrics_controller.get("/metrics/student/{student_id}", tags=["metrics"])
async def student_metrics(student_id: str, start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_professor_or_admin_user)):
    return get_student_metrics(db, student_id, start_date, end_date)

@metrics_controller.get("/metrics/group/{group_id}", tags=["metrics"])
async def group_metrics(group_id: int, start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_professor_or_admin_user)):
    return get_group_metrics(db, group_id, start_date, end_date)
