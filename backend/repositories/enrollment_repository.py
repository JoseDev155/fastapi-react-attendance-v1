# Librerias
from datetime import date
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Enrollment

# Metodos
def get_all(db: Session):
    return db.query(Enrollment).all()

def search_by_id(db: Session, id: int):
    return db.query(Enrollment).filter(Enrollment.id == id).first()

def search_by_date(db: Session, enrollment_date: date):
    return db.query(Enrollment).filter(Enrollment.enrollment_date == enrollment_date).first()

def create(db: Session, enrollment_date: date, student_id: str, group_id: str):
    # Crear una nueva instancia del modelo Enrollment con los datos proporcionados
    enrollment = Enrollment(
        enrollment_date=enrollment_date,
        student_id=student_id,
        group_id=group_id
    )
    
    # Agregar la nueva inscripcion
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment

def update(db: Session, id: int, enrollment_date: date | None = None, student_id: str | None = None, 
                group_id: str | None = None):
    # Buscar la inscripcion por id
    enrollment = search_by_id(db, id)
    
    if not enrollment:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if enrollment_date is not None:
        enrollment.enrollment_date = enrollment_date
    if student_id is not None:
        enrollment.student_id = student_id
    if group_id is not None:
        enrollment.group_id = group_id
    
    # Guardar los cambios
    db.commit()
    db.refresh(enrollment)
    
    return enrollment

# Borrado definitivo
def destroy(db: Session, id: int):
    # Buscar la inscripcion por id
    enrollment = search_by_id(db, id)
    
    if not enrollment:
        return None
    
    # Eliminar la inscripcion
    db.delete(enrollment)
    db.commit()
    
    return enrollment


# Metodos adicionales
#def validate_if_exists(enrollment: Enrollment | None):
#    if not enrollment:
#        return None
#    return enrollment