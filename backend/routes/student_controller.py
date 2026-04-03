# Librerias
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from services import (
    create_student_service,
    destroy_student_service,
    get_all_students as get_all_service,
    search_students_by_email as search_by_email_service,
    search_student_by_id as search_by_id_service,
    search_students_by_name as search_by_name_service,
    update_student_service
)
from schemas import StudentCreate, StudentResponse, StudentUpdate
from database import get_db
from models import User
from utils import get_current_professor_or_admin_user, get_current_admin_user


# Instancia del router de estudiantes
student_controller = APIRouter()


# RUTAS DE ESTUDIANTES - Admin y Profesor
@student_controller.get("/students", tags=["students"],
                       description="Endpoint para obtener todos los estudiantes del sistema. Admin y Profesor.",
                       response_model=list[StudentResponse],
                       status_code=status.HTTP_200_OK)
async def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> list[StudentResponse]:
    students_list = get_all_service(db)
    return students_list


@student_controller.get("/students/{id}", tags=["students"],
                       description="Endpoint para obtener un estudiante específico por su ID. Admin y Profesor.",
                       response_model=StudentResponse,
                       status_code=status.HTTP_200_OK)
async def get_student(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> StudentResponse:
    student = search_by_id_service(db, id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return student


@student_controller.get("/students/search/name/{name}", tags=["students"],
                       description="Endpoint para obtener un estudiante específico por su nombre. Admin y Profesor.",
                       response_model=StudentResponse,
                       status_code=status.HTTP_200_OK)
async def get_student_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> StudentResponse:
    student = search_by_name_service(db, name)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return student


@student_controller.get("/students/search/email/{email}", tags=["students"],
                       description="Endpoint para obtener un estudiante específico por su email. Admin y Profesor.",
                       response_model=StudentResponse,
                       status_code=status.HTTP_200_OK)
async def get_student_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> StudentResponse:
    student = search_by_email_service(db, email)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
    return student


@student_controller.post("/students", tags=["students"],
                        description="Endpoint para crear un nuevo estudiante en el sistema. Admin y Profesor.",
                        response_model=StudentResponse,
                        status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_professor_or_admin_user)
) -> StudentResponse:
    try:
        created_student = create_student_service(student, db)
        if not created_student:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el estudiante")
        
        student_response = StudentResponse.model_validate(created_student)
        return student_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@student_controller.put("/students/{id}", tags=["students"],
                       description="Endpoint para actualizar un estudiante específico por su ID. Solo Admin.",
                       response_model=StudentResponse,
                       status_code=status.HTTP_200_OK)
async def update_student(
    id: str,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> StudentResponse:
    try:
        updated_student = update_student_service(id, student, db)
        if not updated_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
        student_response = StudentResponse.model_validate(updated_student)
        return student_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@student_controller.delete("/students/{id}", tags=["students"],
                          description="Endpoint para eliminar un estudiante específico por su ID. Solo Admin.",
                          status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
) -> None:
    success = destroy_student_service(id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
