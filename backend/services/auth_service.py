# Librerias
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import jwt
# Importar directorios del proyecto
from utils.logger import logger
from models import User
from repositories import user_repository
from utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from schemas import (
    LoginRequest,
    RegisterRequest,
    ChangePasswordRequest,
    TokenResponse,
    UserResponse
)


def login_auth_service(db: Session, login_data: LoginRequest) -> TokenResponse | None:
    # Autentica un usuario y retorna tokens JWT
    # Busca el usuario por ID o email, valida contraseña y retorna tokens
    
    try:
        # Buscar usuario por ID o email
        user = user_repository.search_by_id_or_email(
            db,
            id=login_data.username,
            email=login_data.username
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Crear tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=user.id,
            user_name=f"{user.first_name} {user.last_name}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error en login: %s", e, exc_info=True)
        return None


def register_auth_service(db: Session, register_data: RegisterRequest) -> UserResponse | None:
    # Registra un nuevo usuario en el sistema
    # Valida que no exista, crea contraseña hasheada y guarda en BD
    
    try:
        # Validar que las contraseñas coincidan
        if register_data.password != register_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las contraseñas no coinciden"
            )
        
        # Validar que el usuario no exista
        existing_user = user_repository.search_by_id_or_email(
            db,
            id=register_data.id,
            email=register_data.email
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario o email ya está registrado"
            )
        
        # Hashear contraseña
        hashed_password = get_password_hash(register_data.password)
        
        # Crear usuario
        user = user_repository.create(
            db,
            id=register_data.id,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            email=register_data.email,
            password=hashed_password,
            role_id=register_data.role_id,
            is_active=True
        )
        
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error en registro: %s", e, exc_info=True)
        return None


def refresh_token_auth_service(refresh_token_str: str) -> TokenResponse | None:
    """
    Genera un nuevo access token usando un refresh token válido
    
    El refresh token debe ser válido y tener type="refresh"
    """
    try:
        payload = decode_token(refresh_token_str)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Crear nuevo access token
        access_token = create_access_token(data={"sub": user_id})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="bearer",
            user_id=user_id,
            user_name="Usuario"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error en refresh token: %s", e, exc_info=True)
        return None


def change_password_auth_service(db: Session, user: User, change_pwd_data: ChangePasswordRequest) -> dict[str, str] | None:
    """
    Cambia la contraseña del usuario actual
    
    Valida la contraseña actual antes de permitir cambio
    """
    try:
        # Validar que la contraseña actual sea correcta
        if not verify_password(change_pwd_data.current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
        
        # Validar que las nuevas contraseñas coincidan
        if change_pwd_data.new_password != change_pwd_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las nuevas contraseñas no coinciden"
            )
        
        # Validar que no sea igual a la anterior
        if verify_password(change_pwd_data.new_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña no puede ser igual a la anterior"
            )
        
        # Actualizar contraseña
        hashed_password = get_password_hash(change_pwd_data.new_password)
        user_repository.update(db, user.id, password=hashed_password)
        
        return {"message": "Contraseña actualizada exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al cambiar contraseña: %s", e, exc_info=True)
        return None


def get_current_user_info_service(user: User) -> UserResponse | None:
    """Retorna la informacion del usuario actual"""
    try:
        return UserResponse.model_validate(user)
    except Exception as e:
        logger.error("Error al obtener información del usuario: %s", e, exc_info=True)
        return None