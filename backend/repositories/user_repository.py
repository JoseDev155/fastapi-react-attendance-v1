# Librerias
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import User

# Metodos
def get_all(db: Session):
    # Solo activos
    #return db.query(User).filter(User.is_active == True).all()
    return db.query(User).all()

def search_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def search_by_name(db: Session, first_name: str):
    return db.query(User).filter(
        (User.first_name == first_name) & (User.is_active == True)).first()

def search_by_id_or_email(db: Session, id: str | None = None, email: str | None = None):
    if not id and not email:
        return None
    return db.query(User).filter(
        (User.id == id) | (User.email == email)).first()

def create(db: Session, id: str, first_name: str, last_name: str, email: str, password: str,
                role_id: int, is_active: bool):
    # Crear una nueva instancia del modelo User con los datos proporcionados
    user = User(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role_id=role_id,
        is_active=is_active
    )
    
    # Agregar el nuevo usuario
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def update(db: Session, id: str, first_name: str | None = None, last_name: str | None = None, 
                email: str | None = None, password: str | None = None, role_id: int | None = None):
    # Buscar el usuario por id
    user = search_by_id(db, id)
    
    if not user:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        user.email = email
    if password is not None:
        user.password = password
    if role_id is not None:
        user.role_id = role_id
    
    # Guardar los cambios
    db.commit()
    db.refresh(user)
    
    return user

def reactivate(db: Session, user_id: str):
    user = search_by_id(db, user_id)
    
    if not user:
        return None
    elif user.is_active:
        return user
    else:
        user.is_active = True
    
    db.commit()
    db.refresh(user)
    
    return user

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el usuario por id
    user = search_by_id(db, id)
    
    if not user:
        return None
    
    # Eliminar el usuario
    db.delete(user)
    db.commit()
    
    return user

# Borrado logico
def deactivate(db: Session, id: str):
    user = search_by_id(db, id)
    
    if not user:
        return None
    elif not user.is_active:
        return user  # Ya esta inactivo
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return user


# Metodos adicionales
#def validate_if_exists(user: User | None):
#    if not user:
#        return None
#    elif not user.is_active:
#        return user