# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import CareerSignature

# Metodos
def get_all(db: Session):
    return db.query(CareerSignature).all()

def search_by_id(db: Session, id: str):
    return db.query(CareerSignature).filter(CareerSignature.id == id).first()

def create(db: Session, id: str, signature_id: str, career_id: str):
    # Crear una nueva instancia del modelo CareerSignature con los datos proporcionados
    career_sign = CareerSignature(
        id=id,
        signature_id=signature_id,
        career_id=career_id,
    )
    
    # Agregar el nuevo registro
    db.add(career_sign)
    db.commit()
    db.refresh(career_sign)
    
    return career_sign

def update(db: Session, id: str, signature_id: str | None, career_id: str | None):
    # Buscar el registro por id
    career_sign = search_by_id(db, id)
    
    if not career_sign:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if signature_id is not None:
        career_sign.signature_id = signature_id
    if career_id is not None:
        career_sign.career_id = career_id
    
    # Guardar los cambios
    db.commit()
    db.refresh(career_sign)
    
    return career_sign

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el registro por id
    career_sign = search_by_id(db, id)
    
    if not career_sign:
        return None
    
    # Eliminar el registro de la base de datos
    db.delete(career_sign)
    db.commit()
    
    return career_sign