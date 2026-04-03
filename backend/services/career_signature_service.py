# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from repositories import (
    career_signature_create as create, \
    career_signature_get_all as get_all, \
    career_signature_search_by_id as search_by_id, \
    career_signature_update as update, \
    career_signature_destroy as destroy)
from database import get_db
from models import CareerSignature
from schemas import CareerSignatureCreate, CareerSignatureUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[CareerSignature]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: str | None = None) -> CareerSignature | None:
    if not id:
        return None
    return search_by_id(db, id)

def create_career_signature_service(career_sig: CareerSignatureCreate, db: Session = Depends(get_db)) -> CareerSignature | None:
    try:
        new_career_sig = create(db, id=career_sig.id, signature_id=career_sig.signature_id, career_id=career_sig.career_id)
        return new_career_sig
    except Exception as e:
        # Log error
        print(f"Error creando carrera-asignatura: {e}")
        return None

def update_career_signature_service(career_sig_id: str, career_sig_update: CareerSignatureUpdate,
                                    db: Session = Depends(get_db)) -> CareerSignature | None:
    try:
        updated_career_sig = update(db, id=career_sig_id, signature_id=career_sig_update.signature_id, 
                                   career_id=career_sig_update.career_id)
        return updated_career_sig
    except Exception as e:
        # Log error
        print(f"Error actualizando carrera-asignatura: {e}")
        return None

def destroy_career_signature_service(career_sig_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        career_sig = destroy(db, career_sig_id)
        return True if career_sig else False
    except Exception as e:
        # Log error
        print(f"Error eliminando carrera-asignatura: {e}")
        return False
