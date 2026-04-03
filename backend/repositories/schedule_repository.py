# Librerias
from sqlalchemy.orm import Session
from datetime import time
# Importar directorios del proyecto
from models import Schedule

# Metodos
def get_all(db: Session):
    return db.query(Schedule).all()

def search_by_id(db: Session, id: str):
    return db.query(Schedule).filter(Schedule.id == id).first()

def search_by_day(db: Session, day_of_week: int):
    return db.query(Schedule).filter(Schedule.day_of_week == day_of_week).first()

def create(db: Session, id: str, day_of_week: int, start_time: time, end_time: time, max_entry_minutes: int,
                minutes_to_be_present: int, group_id: str):
    # Crear una nueva instancia del modelo Schedule con los datos proporcionados
    schedule = Schedule(
        id=id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        max_entry_minutes=max_entry_minutes,
        minutes_to_be_present=minutes_to_be_present,
        group_id=group_id
    )
    
    # Agregar el nuevo horario
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return schedule

def update(db: Session, id: str, day_of_week: int | None = None, start_time: time | None = None, end_time: time | None = None, max_entry_minutes: int | None = None, minutes_to_be_present: int | None = None, group_id: str | None = None):
    # Buscar el horario por id
    schedule = search_by_id(db, id)
    
    if not schedule:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if day_of_week is not None:
        schedule.day_of_week = day_of_week
    if start_time is not None:
        schedule.start_time = start_time
    if end_time is not None:
        schedule.end_time = end_time
    if max_entry_minutes is not None:
        schedule.max_entry_minutes = max_entry_minutes
    if minutes_to_be_present is not None:
        schedule.minutes_to_be_present = minutes_to_be_present
    if group_id is not None:
        schedule.group_id = group_id
    
    # Guardar los cambios
    db.commit()
    db.refresh(schedule)
    
    return schedule

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el horario por id
    schedule = search_by_id(db, id)
    
    if not schedule:
        return None
    
    # Eliminar el horario
    db.delete(schedule)
    db.commit()
    
    return schedule


# Metodos adicionales
#def validate_if_exists(schedule: Schedule | None):
#    if not schedule:
#        return None
#    return schedule