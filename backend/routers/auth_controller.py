# Librerias
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from database import get_db
from models import User
from utils import get_current_user, limiter, RATE_LIMIT_LOGIN, RATE_LIMIT_REGISTER, RATE_LIMIT_REFRESH
from services import (
    login_auth_service,
    register_auth_service,
    refresh_token_auth_service,
    change_password_auth_service,
    get_current_user_info_service
)
from schemas import (
    LoginRequest, RegisterRequest, ChangePasswordRequest, RefreshTokenRequest,
    TokenResponse, UserResponse
)

# Instancia del router de autenticacion
auth_controller = APIRouter(prefix="/auth", tags=["Autenticación"])


# RUTAS DE AUTENTICACION
@auth_controller.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit(RATE_LIMIT_LOGIN)  # type: ignore  # Límite desde .env
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    **Login de usuario**
    
    Autentica un usuario usando ID o email y contraseña.
    Retorna access_token y refresh_token.
    
    - **username**: ID del usuario o email
    - **password**: Contraseña del usuario
    """
    return login_auth_service(db, login_data)


@auth_controller.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(RATE_LIMIT_REGISTER)  # type: ignore  # Limite desde .env
async def register(    request: Request,    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    **Registro de nuevo usuario**
    
    Crea un nuevo usuario en el sistema.
    Las contraseñas deben ser iguales y minimo 8 caracteres.
    
    - **id**: ID unico del usuario (maximo 15 caracteres)
    - **first_name**: Nombre del usuario
    - **last_name**: Apellido del usuario
    - **email**: Email unico
    - **password**: Contraseña (minimo 8 caracteres)
    - **password_confirm**: Confirmacion de contraseña
    - **role_id**: ID del rol (1=Admin, 2=Profesor, 3=Estudiante)
    """
    return register_auth_service(db, register_data)


@auth_controller.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit(RATE_LIMIT_REFRESH)  # type: ignore  # Limite desde .env
async def refresh_access_token(
    request: Request,
    refresh_data: RefreshTokenRequest
):
    """
    **Renovar access token**
    
    Genera un nuevo access_token usando un refresh_token valido.
    El refresh_token debe estar vigente.
    """
    return refresh_token_auth_service(refresh_data.refresh_token)


@auth_controller.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    **Obtener información del usuario actual**
    
    Retorna los datos del usuario autenticado.
    Requiere token válido.
    """
    return get_current_user_info_service(current_user)


@auth_controller.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    change_pwd_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    **Cambiar contraseña**
    
    Permite al usuario cambiar su contraseña.
    Requiere la contraseña actual para validacion.
    
    - **current_password**: Contraseña actual
    - **new_password**: Nueva contraseña (minimo 8 caracteres)
    - **password_confirm**: Confirmacion de nueva contraseña
    """
    return change_password_auth_service(db, current_user, change_pwd_data)