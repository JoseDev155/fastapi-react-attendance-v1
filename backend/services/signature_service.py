# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from utils.logger import logger
from repositories import (
    signature_create as create, \
    signature_get_all as get_all, \
    signature_search_by_id as search_by_id, \
    signature_search_by_name as search_by_name, \
    signature_update as update, \
    signature_destroy as destroy)
from database import get_db
from models import Signature
from schemas import SignatureCreate, SignatureUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Signature]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: str | None = None) -> Signature | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> Signature | None:
    if not name:
        return None
    return search_by_name(db, name)

def create_signature_service(signature: SignatureCreate, db: Session = Depends(get_db)) -> Signature | None:
    try:
        new_signature = create(db, id=signature.id, name=signature.name, description=signature.description)
        return new_signature
    except Exception as e:
        # Log error
        logger.error("Error creando asignatura: %s", e, exc_info=True)
        return None

def update_signature_service(signature_id: str, signature_update: SignatureUpdate,
                             db: Session = Depends(get_db)) -> Signature | None:
    try:
        updated_signature = update(db, id=signature_id, name=signature_update.name, 
                                  description=signature_update.description)
        return updated_signature
    except Exception as e:
        # Log error
        logger.error("Error actualizando asignatura: %s", e, exc_info=True)
        return None

def destroy_signature_service(signature_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        signature = destroy(db, signature_id)
        return True if signature else False
    except Exception as e:
        # Log error
        logger.error("Error eliminando asignatura: %s", e, exc_info=True)
        return False
