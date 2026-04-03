# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    academic_cycle_create as create, \
    academic_cycle_get_all as get_all, \
    academic_cycle_search_by_id as search_by_id, \
    academic_cycle_search_by_name as search_by_name, \
    academic_cycle_update as update, \
    academic_cycle_destroy as destroy)
from database import get_db
from models import AcademicCycle
from schemas import AcademicCycleCreate, AcademicCycleUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[AcademicCycle]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: int | None = None) -> AcademicCycle | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> AcademicCycle | None:
    if not name:
        return None
    return search_by_name(db, name)

def create_academic_cycle_service(cycle: AcademicCycleCreate, db: Session = Depends(get_db)) -> AcademicCycle | None:
    try:
        new_cycle = create(db, cycle.cycle_name, cycle.cycle_year)
        return new_cycle
    except Exception as e:
        # Log error
        logger.error("Error creando ciclo académico: %s", e, exc_info=True)
        return None

def update_academic_cycle_service(cycle_id: int, cycle_update: AcademicCycleUpdate,
                                   db: Session = Depends(get_db)) -> AcademicCycle | None:
    try:
        updated_cycle = update(db, id=cycle_id, cycle_name=cycle_update.cycle_name, cycle_year=cycle_update.cycle_year)
        return updated_cycle
    except Exception as e:
        # Log error
        logger.error("Error actualizando ciclo académico: %s", e, exc_info=True)
        return None

def destroy_academic_cycle_service(cycle_id: int, db: Session = Depends(get_db)) -> bool:
    try:
        cycle = destroy(db, cycle_id)
        return True if cycle else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando ciclo académico: %s", e, exc_info=True)
        return False
