# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_schedule_service,
    destroy_schedule_service,
    get_all_schedules as get_all_service,
    search_schedules_by_day as search_by_day_service,
    search_schedule_by_id as search_by_id_service,
    update_schedule_service
)
from schemas import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from database import get_db
from models import User
from utils import get_current_admin_user, get_current_professor_or_admin_user


# Instancia del router de horarios
schedule_controller = APIRouter()


# RUTAS DE HORARIOS - SOLO ADMIN
@schedule_controller.get("/schedules", tags=["schedules"],
                        description="Endpoint para obtener todos los horarios del sistema. Admin y Profesor.",
                        response_model=list[ScheduleResponse],
                        status_code=status.HTTP_200_OK)
async def get_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[ScheduleResponse]:
    schedules_list = get_all_service(db)
    return schedules_list

@schedule_controller.get("/schedules/{id}", tags=["schedules"],
                        description="Endpoint para obtener un horario específico por su ID. Admin y Profesor.",
                        response_model=ScheduleResponse,
                        status_code=status.HTTP_200_OK)
async def get_schedule(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> ScheduleResponse:
    schedule = search_by_id_service(db, id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
    return schedule

@schedule_controller.get("/schedules/search/{day}", tags=["schedules"],
                        description="Endpoint para obtener un horario específico por día de la semana. Admin y Profesor.",
                        response_model=ScheduleResponse,
                        status_code=status.HTTP_200_OK)
async def get_schedule_by_day(
    day: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> ScheduleResponse:
    schedule = search_by_day_service(db, day)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
    return schedule

@schedule_controller.post("/schedules", tags=["schedules"],
                         description="Endpoint para crear un nuevo horario en el sistema. Solo Admin.",
                         response_model=ScheduleResponse,
                         status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> ScheduleResponse:
    try:
        created_schedule = create_schedule_service(schedule, db)
        if not created_schedule:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el horario")
        
        schedule_response = ScheduleResponse.model_validate(created_schedule)
        return schedule_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@schedule_controller.put("/schedules/{id}", tags=["schedules"],
                        description="Endpoint para actualizar un horario específico por su ID. Solo Admin.",
                        response_model=ScheduleResponse,
                        status_code=status.HTTP_200_OK)
async def update_schedule(
    id: str,
    schedule: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> ScheduleResponse:
    try:
        updated_schedule = update_schedule_service(id, schedule, db)
        if not updated_schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
        
        schedule_response = ScheduleResponse.model_validate(updated_schedule)
        return schedule_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@schedule_controller.delete("/schedules/{id}", tags=["schedules"],
                           description="Endpoint para eliminar un horario específico por su ID. Solo Admin.",
                           status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_schedule_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
