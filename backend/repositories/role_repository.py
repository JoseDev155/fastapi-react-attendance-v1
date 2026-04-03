# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Role

# Metodos
def get_all(db: Session):
    # Solo activos
    #return db.query(Role).filter(Role.is_active == True).all()
    return db.query(Role).all()

def search_by_id(db: Session, id: int):
    return db.query(Role).filter(Role.id == id).first()

def search_by_name(db: Session, name: str):
    return db.query(Role).filter(
        (Role.name == name) & (Role.is_active == True)).first()

def create(db: Session, name: str, description: str | None = None):
    # Crear una nueva instancia del modelo Role con los datos proporcionados
    role = Role(
        name=name,
        description=description,
        is_active=True
    )
    
    # Agregar el nuevo rol
    db.add(role)
    db.commit()
    db.refresh(role)
    
    return role

def update(db: Session, id: int, name: str | None = None, description: str | None = None):
    # Buscar el rol por id
    role = search_by_id(db, id)
    
    if not role:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if name is not None:
        role.name = name
    if description is not None:
        role.description = description
    
    # Guardar los cambios
    db.commit()
    db.refresh(role)
    
    return role

def reactivate(db: Session, role_id: int):
    role = search_by_id(db, role_id)
    
    if not role:
        return None
    elif role.is_active:
        return role
    else:
        role.is_active = True
    
    db.commit()
    db.refresh(role)
    
    return role

# Borrado definitivo
def destroy(db: Session, id: int):
    # Buscar el rol por id
    role = search_by_id(db, id)
    
    if not role:
        return None
    
    # Eliminar el rol
    db.delete(role)
    db.commit()
    
    return role

# Borrado logico
def deactivate(db: Session, id: int):
    role = search_by_id(db, id)
    
    if not role:
        return None
    elif not role.is_active:
        return role  # Ya esta inactivo
    
    role.is_active = False
    db.commit()
    db.refresh(role)
    
    return role


# Metodos adicionales
#def validate_if_exists(role: Role | None):
#    if not role:
#        return None
#    elif not role.is_active:
#        return role