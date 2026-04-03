# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Signature

# Metodos
def get_all(db: Session):
    # Solo activos
    #return db.query(Signature).filter(Signature.is_active == True).all()
    return db.query(Signature).all()

def search_by_id(db: Session, id: str):
    return db.query(Signature).filter(Signature.id == id).first()

def search_by_name(db: Session, name: str):
    return db.query(Signature).filter(
        (Signature.name == name) & (Signature.is_active == True)).first()

def create(db: Session, id: str, name: str, description: str | None = None):
    # Crear una nueva instancia del modelo Signature con los datos proporcionados
    signature = Signature(
        id=id,
        name=name,
        description=description,
        is_active=True
    )
    
    # Agregar el nuevo rol
    db.add(signature)
    db.commit()
    db.refresh(signature)
    
    return signature

def update(db: Session, id: str, name: str | None = None, description: str | None = None):
    # Buscar el rol por id
    signature = search_by_id(db, id)
    
    if not signature:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if name is not None:
        signature.name = name
    if description is not None:
        signature.description = description
    
    # Guardar los cambios
    db.commit()
    db.refresh(signature)
    
    return signature

def reactivate(db: Session, signature_id: str):
    signature = search_by_id(db, signature_id)
    
    if not signature:
        return None
    elif signature.is_active:
        return signature
    else:
        signature.is_active = True
    
    db.commit()
    db.refresh(signature)
    
    return signature

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el rol por id
    signature = search_by_id(db, id)
    
    if not signature:
        return None
    
    # Eliminar el rol
    db.delete(signature)
    db.commit()
    
    return signature

# Borrado logico
def deactivate(db: Session, id: str):
    signature = search_by_id(db, id)
    
    if not signature:
        return None
    elif not signature.is_active:
        return signature  # Ya esta inactivo
    
    signature.is_active = False
    db.commit()
    db.refresh(signature)
    
    return signature


# Metodos adicionales
#def validate_if_exists(signature: Signature | None):
#    if not signature:
#        return None
#    elif not signature.is_active:
#        return signature