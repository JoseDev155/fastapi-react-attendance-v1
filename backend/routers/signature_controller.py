# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_signature_service,
    destroy_signature_service,
    get_all_signatures as get_all_service,
    search_signature_by_id as search_by_id_service,
    search_signatures_by_name as search_by_name_service,
    update_signature_service
)
from schemas import SignatureCreate, SignatureResponse, SignatureUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de asignaturas
signature_controller = APIRouter()


# RUTAS DE ASIGNATURAS - SOLO ADMIN
@signature_controller.get("/signatures", tags=["signatures"],
                         description="Endpoint para obtener todas las asignaturas del sistema. Admin y Profesor.",
                         response_model=list[SignatureResponse],
                         status_code=status.HTTP_200_OK)
async def get_signatures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[SignatureResponse]:
    signatures_list = get_all_service(db)
    return [SignatureResponse.model_validate(sig) for sig in signatures_list]

@signature_controller.get("/signatures/{id}", tags=["signatures"],
                         description="Endpoint para obtener una asignatura específica por su ID. Admin y Profesor.",
                         response_model=SignatureResponse,
                         status_code=status.HTTP_200_OK)
async def get_signature(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> SignatureResponse:
    signature = search_by_id_service(db, id)
    if not signature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
    return signature

@signature_controller.get("/signatures/search/{name}", tags=["signatures"],
                         description="Endpoint para obtener una asignatura específica por su nombre. Admin y Profesor.",
                         response_model=SignatureResponse,
                         status_code=status.HTTP_200_OK)
async def get_signature_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> SignatureResponse:
    signature = search_by_name_service(db, name)
    if not signature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
    return signature

@signature_controller.post("/signatures", tags=["signatures"],
                          description="Endpoint para crear una nueva asignatura en el sistema. Solo Admin.",
                          response_model=SignatureResponse,
                          status_code=status.HTTP_201_CREATED)
async def create_signature(
    signature: SignatureCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> SignatureResponse:
    try:
        created_signature = create_signature_service(signature, db)
        if not created_signature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la asignatura")
        
        signature_response = SignatureResponse.model_validate(created_signature)
        return signature_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@signature_controller.put("/signatures/{id}", tags=["signatures"],
                         description="Endpoint para actualizar una asignatura específica por su ID. Solo Admin.",
                         response_model=SignatureResponse,
                         status_code=status.HTTP_200_OK)
async def update_signature(
    id: str,
    signature: SignatureUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> SignatureResponse:
    try:
        updated_signature = update_signature_service(id, signature, db)
        if not updated_signature:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
        
        signature_response = SignatureResponse.model_validate(updated_signature)
        return signature_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@signature_controller.delete("/signatures/{id}", tags=["signatures"],
                            description="Endpoint para eliminar una asignatura específica por su ID. Solo Admin.",
                            status_code=status.HTTP_204_NO_CONTENT)
async def delete_signature(
    id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_signature_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
