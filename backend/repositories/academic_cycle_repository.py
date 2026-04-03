# Librerias
from sqlalchemy.orm import Session
from datetime import date
# Importar directorios del proyecto
from models import AcademicCycle

# Metodos
def get_all(db: Session):
    return db.query(AcademicCycle).all()

def search_by_id(db: Session, id: int):
    return db.query(AcademicCycle).filter(AcademicCycle.id == id).first()

def search_by_name(db: Session, cycle_name: str):
    return db.query(AcademicCycle).filter(
        (AcademicCycle.cycle_name == cycle_name) & (AcademicCycle.is_active == True)).first()

def create(db: Session, cycle_name: str, cycle_year: date):
    # Crear una nueva instancia del modelo AcademicCycle con los datos proporcionados
    cycle = AcademicCycle(
        cycle_name=cycle_name,
        cycle_year=cycle_year
    )
    
    # Agregar el nuevo ciclo
    db.add(cycle)
    db.commit()
    db.refresh(cycle)
    
    return cycle

def update(db: Session, id: int, cycle_name: str | None = None, cycle_year: date | None = None):
    # Buscar el ciclo por id
    cycle = search_by_id(db, id)

    if not cycle:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if cycle_name is not None:
        cycle.cycle_name = cycle_name
    if cycle_year is not None:
        cycle.cycle_year = cycle_year
    
    # Guardar los cambios
    db.commit()
    db.refresh(cycle)
    
    return cycle

# Borrado definitivo
def destroy(db: Session, id: int):
    # Buscar el ciclo por id
    cycle = search_by_id(db, id)
    
    if not cycle:
        return None
    
    # Eliminar el ciclo
    db.delete(cycle)
    db.commit()
    
    return cycle