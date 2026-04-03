from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils import get_current_admin_user
from reports import generate_monthly_group_report

reports_controller = APIRouter()

@reports_controller.get("/reports/group/{group_id}/monthly", tags=["reports"])
async def monthly_group_report(group_id: str, year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    report = generate_monthly_group_report(db, group_id, year, month)
    if "error" in report:
        raise HTTPException(status_code=404, detail=report["error"])
    return report
