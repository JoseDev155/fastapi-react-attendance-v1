# Librerias
from sqlalchemy.orm import Session
from datetime import date
# Importar directorios del proyecto
from models import Student

# Metodos
def get_all(db: Session):
    # Solo activos
    #return db.query(Student).filter(Student.is_active == True).all()
    return db.query(Student).all()

def search_by_id(db: Session, id: str):
    return db.query(Student).filter(Student.id == id).first()

def search_by_name(db: Session, first_name: str):
    return db.query(Student).filter(
        (Student.first_name == first_name) & (Student.is_active == True)).first()

def search_by_email(db: Session, email: str):
    return db.query(Student).filter(
        (Student.email == email) & (Student.is_active == True)).first()

def create(db: Session, id: str, nickname: str, first_name: str, last_name: str, email: str,
           enrollment_date: date, is_active: bool = True):
    # Crear una nueva instancia del modelo Student con los datos proporcionados
    student = Student(
        id=id,
        nickname=nickname,
        first_name=first_name,
        last_name=last_name,
        email=email,
        enrollment_date=enrollment_date,
        is_active=is_active
    )
    
    # Agregar el nuevo usuario
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student

def update(db: Session, id: str, nickname: str | None = None, first_name: str | None = None, last_name: str | None = None, 
                email: str | None = None, enrollment_date: date | None = None):
    # Buscar el usuario por id
    student = search_by_id(db, id)
    
    if not student:
        return None
    
    # Actualizar solo los campos que fueron proporcionados
    if nickname is not None:
        student.nickname = nickname
    if first_name is not None:
        student.first_name = first_name
    if last_name is not None:
        student.last_name = last_name
    if email is not None:
        student.email = email
    if enrollment_date is not None:
        student.enrollment_date = enrollment_date
    
    # Guardar los cambios
    db.commit()
    db.refresh(student)
    
    return student

def reactivate(db: Session, user_id: str):
    student = search_by_id(db, user_id)
    
    if not student:
        return None
    elif student.is_active:
        return student
    else:
        student.is_active = True
    
    db.commit()
    db.refresh(student)
    
    return student

# Borrado definitivo
def destroy(db: Session, id: str):
    # Buscar el usuario por id
    student = search_by_id(db, id)
    
    if not student:
        return None
    
    # Eliminar el usuario
    db.delete(student)
    db.commit()
    
    return student

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
#def validate_if_exists(student: Student | None):
#    if not student:
#        return None
#    elif not student.is_active:
#        return student