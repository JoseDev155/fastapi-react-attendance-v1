# Librerias
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
# Importar directorios del proyecto
from repositories import (
    schedule_create as create, \
    schedule_get_all as get_all, \
    schedule_search_by_id as search_by_id, \
    schedule_search_by_day as search_by_day, \
    schedule_update as update, \
    schedule_destroy as destroy)
from database import get_db
from models import Schedule
from schemas import ScheduleCreate, ScheduleUpdate


def get_all_service(db: Session = Depends(get_db)) -> List[Schedule]:
    return get_all(db)

def search_by_id_service(db: Session = Depends(get_db), id: str | None = None) -> Schedule | None:
    if not id:
        return None
    return search_by_id(db, id)

def search_by_day_service(db: Session = Depends(get_db), day: int | None = None) -> Schedule | None:
    if not day:
        return None
    return search_by_day(db, day)

def create_schedule_service(schedule: ScheduleCreate, db: Session = Depends(get_db)) -> Schedule | None:
    try:
        new_schedule = create(db, schedule.id, schedule.day_of_week, schedule.start_time,
                             schedule.end_time, schedule.max_entry_minutes,
                             schedule.minutes_to_be_present, schedule.group_id)
        return new_schedule
    except Exception as e:
        # Log error
        print(f"Error creando horario: {e}")
        return None

def update_schedule_service(schedule_id: str, schedule_update: ScheduleUpdate,
                            db: Session = Depends(get_db)) -> Schedule | None:
    try:
        updated_schedule = update(db, id=schedule_id, day_of_week=schedule_update.day_of_week,
                                 start_time=schedule_update.start_time, end_time=schedule_update.end_time,
                                 max_entry_minutes=schedule_update.max_entry_minutes,
                                 minutes_to_be_present=schedule_update.minutes_to_be_present,
                                 group_id=schedule_update.group_id)
        return updated_schedule
    except Exception as e:
        # Log error
        print(f"Error actualizando horario: {e}")
        return None

def destroy_schedule_service(schedule_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        schedule = destroy(db, schedule_id)
        return True if schedule else False
    except Exception as e:
        # Log error
        print(f"Error eliminando horario: {e}")
        return False
