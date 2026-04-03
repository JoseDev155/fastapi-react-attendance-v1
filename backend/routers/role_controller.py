# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_role_service, \
    delete_role_service, \
    destroy_role_service, \
    get_all_roles as get_all_service, \
    reactivate_role_service, \
    search_role_by_id as search_by_id_service, \
    search_roles_by_name as search_by_name_service, \
    update_role_service)
from schemas import RoleCreate, RoleResponse, RoleUpdate
from database import get_db
from models import User
from utils import get_current_admin_user


# Instancia del router de roles
role_controller = APIRouter()


# RUTAS DE ROLES - SOLO ADMIN
@role_controller.get("/roles", tags=["roles"],
                     description="Endpoint para obtener todos los roles del sistema. Solo Admin.",
                     response_model=list[RoleResponse],
                     status_code=status.HTTP_200_OK)
async def get_roles(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> list[RoleResponse]:
    roles_list = get_all_service(db)
    return roles_list


@role_controller.get("/roles/{id}", tags=["roles"],
                     description="Endpoint para obtener un rol específico por su ID. Solo Admin.",
                     response_model=RoleResponse,
                     status_code=status.HTTP_200_OK)
async def get_role(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> RoleResponse:
    role = search_by_id_service(db, id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return role


@role_controller.get("/roles/search/{name}", tags=["roles"],
                     description="Endpoint para obtener un rol específico por su nombre. Solo Admin.",
                     response_model=RoleResponse,
                     status_code=status.HTTP_200_OK)
async def get_role_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> RoleResponse:
    role = search_by_name_service(db, name)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return role


@role_controller.post("/roles", tags=["roles"],
                      description="Endpoint para crear un nuevo rol en el sistema. Solo Admin.",
                      response_model=RoleResponse,
                      status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> RoleResponse:
    try:
        created_role = create_role_service(role, db)
        if not created_role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el rol")
        
        role_response = RoleResponse.model_validate(created_role)
        return role_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@role_controller.put("/roles/{id}", tags=["roles"],
                     description="Endpoint para actualizar un rol específico por su ID. Solo Admin.",
                     response_model=RoleResponse,
                     status_code=status.HTTP_200_OK)
async def update_role(
    id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> RoleResponse:
    try:
        updated_role = update_role_service(id, role, db)
        if not updated_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        
        role_response = RoleResponse.model_validate(updated_role)
        return role_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@role_controller.delete("/roles/{id}", tags=["roles"],
                        description="Endpoint para eliminar (soft delete) un rol específico por su ID. Solo Admin.",
                        status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = delete_role_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")


@role_controller.post("/roles/{id}/reactivate", tags=["roles"],
                      description="Endpoint para reactivar un rol específico por su ID. Solo Admin.",
                      response_model=RoleResponse,
                      status_code=status.HTTP_200_OK)
async def reactivate_role(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> RoleResponse:
    try:
        role = reactivate_role_service(id, db)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado o no pudo ser reactivado")
        
        role_response = RoleResponse.model_validate(role)
        return role_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@role_controller.delete("/roles/{id}/destroy", tags=["roles"],
                        description="Endpoint para eliminar definitivamente un rol específico por su ID. Solo Admin.",
                        status_code=status.HTTP_204_NO_CONTENT)
async def destroy_role(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    try:
        success = destroy_role_service(id, db)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado o no pudo ser eliminado definitivamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))