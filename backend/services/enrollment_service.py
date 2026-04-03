# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    enrollment_create as create, \
    enrollment_get_all as get_all, \
    enrollment_search_by_id as search_by_id, \
    enrollment_search_by_date as search_by_date, \
    enrollment_update as update, \
    enrollment_destroy as destroy)
from database import get_db
from models import Enrollment
from schemas import EnrollmentCreate, EnrollmentUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Enrollment]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: int | None = None) -> Enrollment | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_date_service(db: Session = Depends(get_db), enrollment_date: date | None = None) -> Enrollment | None:
    if not enrollment_date:
        return None
    return search_by_date(db, enrollment_date)

def create_enrollment_service(enrollment: EnrollmentCreate, db: Session = Depends(get_db)) -> Enrollment | None:
    try:
        new_enrollment = create(db, enrollment.enrollment_date, enrollment.student_id, enrollment.group_id)
        return new_enrollment
    except Exception as e:
        # Log error
        logger.error("Error creando inscripción: %s", e, exc_info=True)
        return None

def update_enrollment_service(enrollment_id: int, enrollment_update: EnrollmentUpdate,
                              db: Session = Depends(get_db)) -> Enrollment | None:
    try:
        updated_enrollment = update(db, id=enrollment_id, enrollment_date=enrollment_update.enrollment_date,
                                   student_id=enrollment_update.student_id, group_id=enrollment_update.group_id)
        return updated_enrollment
    except Exception as e:
        # Log error
        logger.error("Error actualizando inscripción: %s", e, exc_info=True)
        return None

def destroy_enrollment_service(enrollment_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        enrollment = destroy(db, enrollment_id)
        return True if enrollment else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando inscripción: %s", e, exc_info=True)
        return False
