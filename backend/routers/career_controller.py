# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_career_service,
    delete_career_service,
    destroy_career_service,
    get_all_careers as get_all_service,
    reactivate_career_service,
    search_career_by_id as search_by_id_service,
    search_careers_by_name as search_by_name_service,
    update_career_service
)
from schemas import CareerCreate, CareerResponse, CareerUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de carreras
career_controller = APIRouter()


# RUTAS DE CARRERAS - SOLO ADMIN
@career_controller.get("/careers", tags=["careers"],
                     description="Endpoint para obtener todas las carreras del sistema. Admin y Profesor.",
                     response_model=list[CareerResponse],
                     status_code=status.HTTP_200_OK)
async def get_careers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[CareerResponse]:
    careers_list = get_all_service(db)
    return careers_list

@career_controller.get("/careers/{id}", tags=["careers"],
                     description="Endpoint para obtener una carrera específica por su ID. Admin y Profesor.",
                     response_model=CareerResponse,
                     status_code=status.HTTP_200_OK)
async def get_career(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> CareerResponse:
    career = search_by_id_service(db, id)
    if not career:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada")
    return career

@career_controller.get("/careers/{name}", tags=["careers"],
                     description="Endpoint para obtener una carrera específica por su nombre. Admin y Profesor.",
                     response_model=CareerResponse,
                     status_code=status.HTTP_200_OK)
async def get_career_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> CareerResponse:
    career = search_by_name_service(db, name)
    if not career:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada")
    return career

@career_controller.post("/careers", tags=["careers"],
                      description="Endpoint para crear una nueva carrera en el sistema. Solo Admin.",
                      response_model=CareerResponse,
                      status_code=status.HTTP_201_CREATED)
async def create_career(
    career: CareerCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> CareerResponse:
    try:
        created_career = create_career_service(career, db)
        if not created_career:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la carrera")
        
        career_response = CareerResponse.model_validate(created_career)
        return career_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@career_controller.put("/careers/{id}", tags=["careers"],
                     description="Endpoint para actualizar una carrera específico por su ID. Solo Admin.",
                     response_model=CareerResponse,
                     status_code=status.HTTP_200_OK)
async def update_career(
    id: int,
    career: CareerUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> CareerResponse:
    try:
        updated_career = update_career_service(id, career, db)
        if not updated_career:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada")
        
        career_response = CareerResponse.model_validate(updated_career)
        return career_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@career_controller.delete("/careers/{id}", tags=["careers"],
                        description="Endpoint para eliminar una carrera específica por su ID. Solo Admin.",
                        status_code=status.HTTP_204_NO_CONTENT)
async def delete_career(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = delete_career_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada")

@career_controller.post("/careers/{id}/reactivate", tags=["careers"],
                        description="Endpoint para reactivar una carrera específica por su ID. Solo Admin.",
                        response_model=CareerResponse,
                        status_code=status.HTTP_200_OK)
async def reactivate_career(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> CareerResponse:
    try:
        career = reactivate_career_service(id, db)
        if not career:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada o no pudo ser reactivada")
        
        career_response = CareerResponse.model_validate(career)
        return career_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@career_controller.delete("/careers/{id}/destroy", tags=["careers"],
                        description="Endpoint para eliminar definitivamente una carrera específica por su ID. Solo Admin.",
                        status_code=status.HTTP_204_NO_CONTENT)
async def destroy_career(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    try:
        success = destroy_career_service(id, db)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera no encontrada o no pudo ser eliminada definitivamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))