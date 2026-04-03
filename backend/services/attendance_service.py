# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    attendance_create as create, \
    attendance_get_all as get_all, \
    attendance_search_by_id as search_by_id, \
    attendance_update as update, \
    attendance_destroy as destroy)
from database import get_db
from models import Attendance
from schemas import AttendanceCreate, AttendanceUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Attendance]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: int | None = None) -> Attendance | None:
    if not id:
        return None
    return search_by_id(db, id)

def create_attendance_service(attendance: AttendanceCreate, db: Session = Depends(get_db)) -> Attendance | None:
    try:
        new_attendance = create(db, attendance.attendance_date, attendance.arrival_time, attendance.status, 
                               attendance.notes, attendance.enrollment_id)
        return new_attendance
    except Exception as e:
        # Log error
        logger.error("Error creando asistencia: %s", e, exc_info=True)
        return None

def update_attendance_service(attendance_id: int, attendance_update: AttendanceUpdate,
                              db: Session = Depends(get_db)) -> Attendance | None:
    try:
        updated_attendance = update(db, id=attendance_id, 
                                   attendance_date=attendance_update.attendance_date, 
                                   arrival_time=attendance_update.arrival_time, 
                                   status=attendance_update.status, notes=attendance_update.notes)
        return updated_attendance
    except Exception as e:
        # Log error
        logger.error("Error actualizando asistencia: %s", e, exc_info=True)
        return None

def destroy_attendance_service(attendance_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        attendance = destroy(db, attendance_id)
        return True if attendance else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando asistencia: %s", e, exc_info=True)
        return False
