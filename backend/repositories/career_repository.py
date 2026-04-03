# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Career

# Metodos
def get_all(db: Session):
    # Solo activos
    #return db.query(Career).filter(Career.is_active == True).all()
    return db.query(Career).all()

def search_by_id(db: Session, id: int):
    return db.query(Career).filter(Career.id == id).first()

def search_by_name(db: Session, name: str):
    return db.query(Career).filter(
        (Career.name == name) & (Career.is_active == True)).first()

def create(db: Session, name: str, description: str | None = None):
    # Crear una nueva instancia del modelo Career con los datos proporcionados
    career = Career(
        name=name,
        description=description,
        is_active=True
    )
    
    # Agregar el nuevo rol
    db.add(career)
    db.commit()
    db.refresh(career)
    
    return career

def update(db: Session, id: int, name: str | None = None, description: str | None = None):
    # Buscar el rol por id
    career = search_by_id(db, id)
    
    if not career:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if name is not None:
        career.name = name
    if description is not None:
        career.description = description
    
    # Guardar los cambios
    db.commit()
    db.refresh(career)
    
    return career

def reactivate(db: Session, career_id: int):
    career = search_by_id(db, career_id)
    
    if not career:
        return None
    elif career.is_active:
        return career
    else:
        career.is_active = True
    
    db.commit()
    db.refresh(career)
    
    return career

# Borrado definitivo
def destroy(db: Session, id: int):
    # Buscar el rol por id
    career = search_by_id(db, id)
    
    if not career:
        return None
    
    # Eliminar el rol
    db.delete(career)
    db.commit()
    
    return career

# Borrado logico
def deactivate(db: Session, id: int):
    career = search_by_id(db, id)
    
    if not career:
        return None
    elif not career.is_active:
        return career  # Ya esta inactivo
    
    career.is_active = False
    db.commit()
    db.refresh(career)
    
    return career


# Metodos adicionales
#def validate_if_exists(career: Career | None):
#    if not career:
#        return None
#    elif not career.is_active:
#        return career