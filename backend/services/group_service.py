# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    group_create as create, \
    group_get_all as get_all, \
    group_search_by_id as search_by_id, \
    group_search_by_name as search_by_name, \
    group_update as update, \
    group_destroy as destroy)
from database import get_db
from models import Group
from schemas import GroupCreate, GroupUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Group]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: str | None = None) -> Group | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> Group | None:
    if not name:
        return None
    return search_by_name(db, name)

def create_group_service(group: GroupCreate, db: Session = Depends(get_db)) -> Group | None:
    try:
        new_group = create(db, id=group.id, name=group.name, user_id=group.user_id,
                          career_signature_id=group.career_signature_id, academic_cycle_id=group.academic_cycle_id)
        return new_group
    except Exception as e:
        # Log error
        logger.error("Error creando grupo: %s", e, exc_info=True)
        return None

def update_group_service(group_id: str, group_update: GroupUpdate,
                         db: Session = Depends(get_db)) -> Group | None:
    try:
        updated_group = update(db, id=group_id, name=group_update.name, user_id=group_update.user_id,
                              career_signature_id=group_update.career_signature_id, 
                              academic_cycle_id=group_update.academic_cycle_id)
        return updated_group
    except Exception as e:
        # Log error
        logger.error("Error actualizando grupo: %s", e, exc_info=True)
        return None

def destroy_group_service(group_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        group = destroy(db, group_id)
        return True if group else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando grupo: %s", e, exc_info=True)
        return False
