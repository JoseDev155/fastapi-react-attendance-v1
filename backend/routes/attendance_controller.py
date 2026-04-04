# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_attendance_service,
    destroy_attendance_service,
    get_all_attendances as get_all_service,
    get_calculated_attendances_by_group as get_calculated_by_group_service,
    search_attendance_by_id as search_by_id_service,
    update_attendance_service
)
from schemas import AttendanceCreate, AttendanceResponse, AttendanceUpdate, CalculatedAttendanceResponse
from database import get_db
from models import User
from utils import get_current_professor_or_admin_user, get_current_admin_user


# Instancia del router de asistencias
attendance_controller = APIRouter()


# RUTAS DE ASISTENCIAS - Admin y Profesor  
@attendance_controller.get("/attendances", tags=["attendances"],
                          description="Endpoint para obtener todas las asistencias del sistema. Admin y Profesor.",
                          response_model=list[AttendanceResponse],
                          status_code=status.HTTP_200_OK)
async def get_attendances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[AttendanceResponse]:
    attendances_list = get_all_service(db)
    return attendances_list


@attendance_controller.get("/attendances/group/{group_id}/calculated", tags=["attendances"],
                          description="Endpoint para obtener asistencias de un grupo con el estado calculado dinámicamente. Admin y Profesor.",
                          response_model=list[CalculatedAttendanceResponse],
                          status_code=status.HTTP_200_OK)
async def get_calculated_attendances(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[CalculatedAttendanceResponse]:
    attendances_list = get_calculated_by_group_service(group_id, db)
    return attendances_list


@attendance_controller.get("/attendances/{id}", tags=["attendances"],
                          description="Endpoint para obtener una asistencia específica por su ID. Admin y Profesor.",
                          response_model=AttendanceResponse,
                          status_code=status.HTTP_200_OK)
async def get_attendance(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> AttendanceResponse:
    attendance = search_by_id_service(db, id)
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
    return attendance


@attendance_controller.post("/attendances", tags=["attendances"],
                           description="Endpoint para crear una nueva asistencia en el sistema. Admin y Profesor.",
                           response_model=AttendanceResponse,
                           status_code=status.HTTP_201_CREATED)
async def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> AttendanceResponse:
    try:
        created_attendance = create_attendance_service(attendance, db)
        if not created_attendance:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la asistencia")
        
        attendance_response = AttendanceResponse.model_validate(created_attendance)
        return attendance_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@attendance_controller.put("/attendances/{id}", tags=["attendances"],
                          description="Endpoint para actualizar una asistencia específica por su ID. Solo Admin.",
                          response_model=AttendanceResponse,
                          status_code=status.HTTP_200_OK)
async def update_attendance(
    id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> AttendanceResponse:
    try:
        updated_attendance = update_attendance_service(id, attendance, db)
        if not updated_attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
        
        attendance_response = AttendanceResponse.model_validate(updated_attendance)
        return attendance_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@attendance_controller.delete("/attendances/{id}", tags=["attendances"],
                             description="Endpoint para eliminar una asistencia específica por su ID. Solo Admin.",
                             status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_attendance_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
