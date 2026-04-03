# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_group_service,
    destroy_group_service,
    get_all_groups as get_all_service,
    search_group_by_id as search_by_id_service,
    search_groups_by_name as search_by_name_service,
    update_group_service
)
from schemas import GroupCreate, GroupResponse, GroupUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de grupos
group_controller = APIRouter()


# RUTAS DE GRUPOS - SOLO ADMIN
@group_controller.get("/groups", tags=["groups"],
                     description="Endpoint para obtener todos los grupos del sistema. Admin y Profesor.",
                     response_model=list[GroupResponse],
                     status_code=status.HTTP_200_OK)
async def get_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[GroupResponse]:
    groups_list = get_all_service(db)
    return groups_list

@group_controller.get("/groups/{id}", tags=["groups"],
                     description="Endpoint para obtener un grupo específico por su ID. Admin y Profesor.",
                     response_model=GroupResponse,
                     status_code=status.HTTP_200_OK)
async def get_group(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> GroupResponse:
    group = search_by_id_service(db, id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return group

@group_controller.get("/groups/search/{name}", tags=["groups"],
                     description="Endpoint para obtener un grupo específico por su nombre. Admin y Profesor.",
                     response_model=GroupResponse,
                     status_code=status.HTTP_200_OK)
async def get_group_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> GroupResponse:
    group = search_by_name_service(db, name)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return group

@group_controller.post("/groups", tags=["groups"],
                      description="Endpoint para crear un nuevo grupo en el sistema. Solo Admin.",
                      response_model=GroupResponse,
                      status_code=status.HTTP_201_CREATED)
async def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> GroupResponse:
    try:
        created_group = create_group_service(group, db)
        if not created_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el grupo")
        
        group_response = GroupResponse.model_validate(created_group)
        return group_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@group_controller.put("/groups/{id}", tags=["groups"],
                     description="Endpoint para actualizar un grupo específico por su ID. Solo Admin.",
                     response_model=GroupResponse,
                     status_code=status.HTTP_200_OK)
async def update_group(
    id: str,
    group: GroupUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> GroupResponse:
    try:
        updated_group = update_group_service(id, group, db)
        if not updated_group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
        
        group_response = GroupResponse.model_validate(updated_group)
        return group_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@group_controller.delete("/groups/{id}", tags=["groups"],
                        description="Endpoint para eliminar un grupo específico por su ID. Solo Admin.",
                        status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_group_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
