# Librerias
from sqlalchemy.orm import Session
from datetime import date, time
# Importar directorios del proyecto
from models import Attendance

# Metodos
def get_all(db: Session):
    return db.query(Attendance).all()

def search_by_id(db: Session, id: int):
    return db.query(Attendance).filter(Attendance.id == id).first()

def search_by_arrival(db: Session, arrival_time: time):
    return db.query(Attendance).filter(Attendance.arrival_time == arrival_time).first()

def search_by_enrollment_and_date(db: Session, enrollment_id: int, attendance_date: date):
    return db.query(Attendance).filter(
        Attendance.enrollment_id == enrollment_id,
        Attendance.attendance_date == attendance_date
    ).first()

def create(db: Session, attendance_date: date, arrival_time: time | None, notes: str | None, enrollment_id: int):
    # Crear una nueva instancia del modelo Attendance con los datos proporcionados
    attendance = Attendance(
        attendance_date=attendance_date,
        arrival_time=arrival_time,
        notes=notes,
        enrollment_id=enrollment_id
    )
    
    # Agregar la nueva asistencia
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return attendance

def update(db: Session, id: int, attendance_date: date | None = None, arrival_time: time | None = None, status: str | None = None, 
                notes: str | None = None, enrollment_id: int | None = None):
    # Buscar la asistencia por id
    attendance = search_by_id(db, id)
    
    if not attendance:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if attendance_date is not None:
        attendance.attendance_date = attendance_date
    if arrival_time is not None:
        attendance.arrival_time = arrival_time
    if notes is not None:
        attendance.notes = notes
    if enrollment_id is not None:
        attendance.enrollment_id = enrollment_id

    # Guardar los cambios
    db.commit()
    db.refresh(attendance)

    return attendance

# Borrado definitivo
def destroy(db: Session, id: int):
    # Buscar la asistencia por id
    attendance = search_by_id(db, id)
    
    if not attendance:
        return None
    
    # Eliminar la asistencia
    db.delete(attendance)
    db.commit()
    
    return attendance


# Metodos adicionales
#def validate_if_exists(attendance: Attendance | None):
#    if not attendance:
#        return None
#    return attendance