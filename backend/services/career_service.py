# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    career_create as create, \
    career_get_all as get_all, \
    career_search_by_id as search_by_id, \
    career_search_by_name as search_by_name, \
    career_update as update, \
    career_reactivate as reactivate, \
    career_destroy as destroy, \
    career_deactivate as deactivate)
from database import get_db
from models import Career
from schemas import CareerCreate, CareerUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Career]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: int | None = None) -> Career | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> Career | None:
    if not name:
        return None
    return search_by_name(db, name)

def create_career_service(career: CareerCreate, db: Session = Depends(get_db)) -> Career | None:
    if not career.description:
        career.description = None
    
    try:
        new_career = create(db, name=career.name, description=career.description)
        return new_career
    except Exception as e:
        # Log error
        logger.error("Error creando carrera: %s", e, exc_info=True)
        return None

def update_career_service(career_id: int, career_update: CareerUpdate,
                          db: Session = Depends(get_db)) -> Career | None:
    try:
        updated_career = update(db, id=career_id, name=career_update.name, description=career_update.description)
        return updated_career
    except Exception as e:
        # Log error
        logger.error("Error actualizando carrera: %s", e, exc_info=True)
        return None

def delete_career_service(career_id: int, db: Session = Depends(get_db)) -> Career | None:
    try:
        career = deactivate(db, career_id)
        return career
    except Exception as e:
        # Log error
        logger.error("Error desactivando carrera: %s", e, exc_info=True)
        return None

def reactivate_career_service(career_id: int, db: Session = Depends(get_db)) -> Career | None:
    try:
        career = reactivate(db, career_id)
        return career
    except Exception as e:
        # Log error
        logger.error("Error reactivando carrera: %s", e, exc_info=True)
        return None

def destroy_career_service(career_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        career = destroy(db, career_id)
        return True if career else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando carrera: %s", e, exc_info=True)
        return False