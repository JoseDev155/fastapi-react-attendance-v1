# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_career_signature_service,
    destroy_career_signature_service,
    get_all_career_signatures as get_all_service,
    search_career_signature_by_id as search_by_id_service,
    update_career_signature_service
)
from schemas import CareerSignatureCreate, CareerSignatureResponse, CareerSignatureUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de carrera-asignatura
career_signature_controller = APIRouter()


# RUTAS DE CARRERA-ASIGNATURA - ADMIN Y PROFESOR
@career_signature_controller.get("/career-signatures", tags=["career-signatures"],
                                 description="Endpoint para obtener todas las carrera-asignatura del sistema. Admin y Profesor.",
                                 response_model=list[CareerSignatureResponse],
                                 status_code=status.HTTP_200_OK)
async def get_career_signatures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[CareerSignatureResponse]:
    career_sigs_list = get_all_service(db)
    return [CareerSignatureResponse.model_validate(cs) for cs in career_sigs_list]

@career_signature_controller.get("/career-signatures/{id}", tags=["career-signatures"],
                                 description="Endpoint para obtener una carrera-asignatura específica por su ID. Admin y Profesor.",
                                 response_model=CareerSignatureResponse,
                                 status_code=status.HTTP_200_OK)
async def get_career_signature(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> CareerSignatureResponse:
    career_sig = search_by_id_service(db, id)
    if not career_sig:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera-asignatura no encontrada")
    return career_sig

# RUTAS DE CARRERA-ASIGNATURA - SOLO ADMIN
@career_signature_controller.post("/career-signatures", tags=["career-signatures"],
                                  description="Endpoint para crear una nueva carrera-asignatura en el sistema. Solo Admin.",
                                  response_model=CareerSignatureResponse,
                                  status_code=status.HTTP_201_CREATED)
async def create_career_signature(
    career_sig: CareerSignatureCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> CareerSignatureResponse:
    try:
        created_career_sig = create_career_signature_service(career_sig, db)
        if not created_career_sig:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la carrera-asignatura")
        
        career_sig_response = CareerSignatureResponse.model_validate(created_career_sig)
        return career_sig_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@career_signature_controller.put("/career-signatures/{id}", tags=["career-signatures"],
                                 description="Endpoint para actualizar una carrera-asignatura específica por su ID. Solo Admin.",
                                 response_model=CareerSignatureResponse,
                                 status_code=status.HTTP_200_OK)
async def update_career_signature(
    id: str,
    career_sig: CareerSignatureUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> CareerSignatureResponse:
    try:
        updated_career_sig = update_career_signature_service(id, career_sig, db)
        if not updated_career_sig:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera-asignatura no encontrada")
        
        career_sig_response = CareerSignatureResponse.model_validate(updated_career_sig)
        return career_sig_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@career_signature_controller.delete("/career-signatures/{id}", tags=["career-signatures"],
                                   description="Endpoint para eliminar una carrera-asignatura específica por su ID. Solo Admin.",
                                   status_code=status.HTTP_204_NO_CONTENT)
async def delete_career_signature(
    id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_career_signature_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrera-asignatura no encontrada")
