from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils import get_current_admin_user
from uploads import process_attendance_excel

uploads_controller = APIRouter()

@uploads_controller.post("/uploads/attendance-excel", tags=["uploads"])
async def upload_attendance_excel(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    if not (file.filename.endswith('.xlsx') or file.filename.endswith('.xlsm')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un .xlsx o .xlsm")
        
    try:
        content = await file.read()
        result = process_attendance_excel(content, db)
        return dict(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
