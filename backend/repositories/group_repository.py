# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Group

# Metodos
def get_all(db: Session):
    return db.query(Group).all()

def search_by_id(db: Session, id: str):
    return db.query(Group).filter(Group.id == id).first()

def search_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()

def create(db: Session, id: str, name: str, user_id: str, career_signature_id: str, academic_cycle_id: int):
    # Crear una nueva instancia del modelo Group con los datos proporcionados
    group = Group(
        id=id,
        name=name,
        user_id=user_id,
        career_signature_id=career_signature_id,
        academic_cycle_id=academic_cycle_id
    )
    
    # Agregar el nuevo grupo
    db.add(group)
    db.commit()
    db.refresh(group)
    
    return group

def update(db: Session, id: str, name: str | None = None, user_id: str | None = None, 
                career_signature_id: str | None = None, academic_cycle_id: int | None = None):
    # Buscar el grupo por id
    group = search_by_id(db, id)
    
    if not group:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if name is not None:
        group.name = name
    if user_id is not None:
        group.user_id = user_id
    if career_signature_id is not None:
        group.career_signature_id = career_signature_id
    if academic_cycle_id is not None:
        group.academic_cycle_id = academic_cycle_id
    
    # Guardar los cambios
    db.commit()
    db.refresh(group)
    
    return group

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el grupo por id
    group = search_by_id(db, id)
    
    if not group:
        return None
    
    # Eliminar el grupo
    db.delete(group)
    db.commit()
    
    return group

# Metodos adicionales
#def validate_if_exists(group: Group | None):
#    if not group:
#        return None
#    return group