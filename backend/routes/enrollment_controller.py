# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
# Importar directorios del proyecto
from services import (
    create_enrollment_service,
    destroy_enrollment_service,
    get_all_enrollments as get_all_service,
    search_enrollments_by_date as search_by_date_service,
    search_enrollment_by_id as search_by_id_service,
    update_enrollment_service
)
from schemas import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de inscripciones
enrollment_controller = APIRouter()


# RUTAS DE INSCRIPCIONES - ADMIN Y PROFESOR
@enrollment_controller.get("/enrollments", tags=["enrollments"],
                           description="Endpoint para obtener todas las inscripciones del sistema. Admin y Profesor.",
                           response_model=list[EnrollmentResponse],
                           status_code=status.HTTP_200_OK)
async def get_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[EnrollmentResponse]:
    enrollments_list = get_all_service(db)
    return [EnrollmentResponse.model_validate(e) for e in enrollments_list]


@enrollment_controller.get("/enrollments/{id}", tags=["enrollments"],
                           description="Endpoint para obtener una inscripción específica por su ID. Admin y Profesor.",
                           response_model=EnrollmentResponse,
                           status_code=status.HTTP_200_OK)
async def get_enrollment(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> EnrollmentResponse:
    enrollment = search_by_id_service(db, id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscripción no encontrada")
    return enrollment


@enrollment_controller.get("/enrollments/search/{enrollment_date}", tags=["enrollments"],
                           description="Endpoint para obtener una inscripción específica por fecha. Admin y Profesor.",
                           response_model=EnrollmentResponse,
                           status_code=status.HTTP_200_OK)
async def get_enrollment_by_date(
    enrollment_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> EnrollmentResponse:
    enrollment = search_by_date_service(db, enrollment_date)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscripción no encontrada")
    return enrollment


# RUTAS DE INSCRIPCIONES - SOLO ADMIN
@enrollment_controller.post("/enrollments", tags=["enrollments"],
                            description="Endpoint para crear una nueva inscripción en el sistema. Solo Admin.",
                            response_model=EnrollmentResponse,
                            status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> EnrollmentResponse:
    try:
        created_enrollment = create_enrollment_service(enrollment, db)
        if not created_enrollment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la inscripción")
        
        enrollment_response = EnrollmentResponse.model_validate(created_enrollment)
        return enrollment_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@enrollment_controller.put("/enrollments/{id}", tags=["enrollments"],
                           description="Endpoint para actualizar una inscripción específica por su ID. Solo Admin.",
                           response_model=EnrollmentResponse,
                           status_code=status.HTTP_200_OK)
async def update_enrollment(
    id: int,
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> EnrollmentResponse:
    try:
        updated_enrollment = update_enrollment_service(id, enrollment, db)
        if not updated_enrollment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscripción no encontrada")
        
        enrollment_response = EnrollmentResponse.model_validate(updated_enrollment)
        return enrollment_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@enrollment_controller.delete("/enrollments/{id}", tags=["enrollments"],
                              description="Endpoint para eliminar una inscripción específica por su ID. Solo Admin.",
                              status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_enrollment_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscripción no encontrada")
