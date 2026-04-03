# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from repositories import (
    student_create as create, \
    student_get_all as get_all, \
    student_search_by_id as search_by_id, \
    student_search_by_name as search_by_name, \
    student_search_by_email as search_by_email, \
    student_update as update, \
    student_destroy as destroy)
from database import get_db
from models import Student
from schemas import StudentCreate, StudentUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Student]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: str | None = None) -> Student | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> Student | None:
    if not name:
        return None
    return search_by_name(db, name)

def search_by_email_service(db: Session = Depends(get_db), email: str | None = None) -> Student | None:
    if not email:
        return None
    return search_by_email(db, email)

def create_student_service(student: StudentCreate, db: Session = Depends(get_db)) -> Student | None:
    try:
        new_student = create(db, student.id, student.nickname, student.first_name, student.last_name,
                            student.email, student.enrollment_date, student.is_active)
        return new_student
    except Exception as e:
        # Log error
        print(f"Error creando estudiante: {e}")
        return None

def update_student_service(student_id: str, student_update: StudentUpdate,
                           db: Session = Depends(get_db)) -> Student | None:
    try:
        updated_student = update(db, id=student_id, first_name=student_update.first_name,
                                last_name=student_update.last_name, email=student_update.email,
                                nickname=student_update.nickname)
        return updated_student
    except Exception as e:
        # Log error
        print(f"Error actualizando estudiante: {e}")
        return None

def destroy_student_service(student_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        student = destroy(db, student_id)
        return True if student else False
    except Exception as e:
        # Log error
        print(f"Error eliminando estudiante: {e}")
        return False
