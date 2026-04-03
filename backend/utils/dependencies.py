# Librerias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
# Importar directorios del proyecto
from .security import decode_token
from database import get_db
from models import User
from repositories import user_repository


# Esquema de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Dependencia para obtener el usuario actual desde el token JWT
    # Valida el token y retorna el usuario de la base de datos
    
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_repository.search_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    # Dependencia para verificar que el usuario actual es administrador
    # Se usa cuando se necesitan permisos elevados
    
    if current_user.role_id != 1:  # role_id = 1 es Admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador"
        )
    
    return current_user


def get_current_professor_user(current_user: User = Depends(get_current_user)) -> User:
    # Dependencia para verificar que el usuario actual es profesor
    # Se usa para las operaciones permitidas para profesores
    
    if current_user.role_id != 2:  # role_id = 2 es Profesor
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de profesor"
        )
    
    return current_user


def get_current_professor_or_admin_user(current_user: User = Depends(get_current_user)) -> User:
    # Dependencia para verificar que el usuario es profesor O administrador
    # Se usa cuando tanto admin como profesores pueden acceder
    
    if current_user.role_id not in [1, 2]:  # role_id = 1 es Admin, 2 es Profesor
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador o profesor"
        )
    
    return current_user
