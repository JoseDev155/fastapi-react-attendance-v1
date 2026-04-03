# Funciones de utilidad
from .dependencies import (
    get_db,
    get_current_user,
    get_current_admin_user,
    get_current_professor_user,
    get_current_professor_or_admin_user
)
from .functions import get_password_hash, verify_password
from .logger import logger
from .security import create_access_token, create_refresh_token, decode_token
from .rate_limiter import limiter, RATE_LIMIT_LOGIN, RATE_LIMIT_REGISTER, RATE_LIMIT_REFRESH

__all__ = [
    # Dependencias
    "get_db",
    "get_current_user",
    "get_current_admin_user",
    "get_current_professor_user",
    "get_current_professor_or_admin_user",
    # Funciones de password (desde pwdlib)
    "get_password_hash",
    "verify_password",
    # Logger
    "logger",
    # Funciones de seguridad JWT
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    # Rate Limiter
    "limiter",
    "RATE_LIMIT_LOGIN",
    "RATE_LIMIT_REGISTER",
    "RATE_LIMIT_REFRESH",
]
