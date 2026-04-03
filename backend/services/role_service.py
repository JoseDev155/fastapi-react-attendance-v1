# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from repositories import (
    role_create as create, \
    role_get_all as get_all, \
    role_search_by_id as search_by_id, \
    role_search_by_name as search_by_name, \
    role_update as update, \
    role_reactivate as reactivate, \
    role_destroy as destroy, \
    role_deactivate as deactivate)
from database import get_db
from models import Role
from schemas import RoleCreate, RoleUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Role]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: int | None = None) -> Role | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_name_service(db: Session = Depends(get_db), name: str | None = None) -> Role | None:
    if not name:
        return None
    return search_by_name(db, name)

def create_role_service(role: RoleCreate, db: Session = Depends(get_db)) -> Role | None:
    if not role.description:
        role.description = None
    
    try:
        new_role = create(db, name=role.name, description=role.description)
        return new_role
    except Exception as e:
        # Log error
        print(f"Error creating role: {e}")
        return None

def update_role_service(role_id: int, role_update: RoleUpdate,
                        db: Session = Depends(get_db)) -> Role | None:
    try:
        updated_role = update(db, id=role_id, name=role_update.name, description=role_update.description)
        return updated_role
    except Exception as e:
        # Log error
        print(f"Error updating role: {e}")
        return None

def delete_role_service(role_id: int, db: Session = Depends(get_db)) -> Role | None:
    try:
        role = deactivate(db, role_id)
        return role
    except Exception as e:
        # Log error
        print(f"Error desactivando rol: {e}")
        return None

def reactivate_role_service(role_id: int, db: Session = Depends(get_db)) -> Role | None:
    try:
        role = reactivate(db, role_id)
        return role
    except Exception as e:
        # Log error
        print(f"Error reactivating role: {e}")
        return None

def destroy_role_service(role_id: int, db: Session = Depends(get_db)) -> Role | None:
    try:
        role = destroy(db, role_id)
        return role
    except Exception as e:
        # Log error
        print(f"Error eliminando rol: {e}")
        return None