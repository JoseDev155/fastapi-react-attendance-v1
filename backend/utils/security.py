# Librerias
from datetime import datetime, timedelta, timezone
from typing import Any, cast
import jwt
from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()


# Configuracion de variables de entorno para JWT
_SECRET_KEY = os.getenv("SECRET_KEY")
if not _SECRET_KEY:
    raise ValueError("ERROR: SECRET_KEY no está configurada en .env")

SECRET_KEY: str = _SECRET_KEY
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


# FUNCIONES DE JWT
def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    # jwt.encode() puede retornar str o bytes según la versión — cast garantiza str
    return cast(str, jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))


def create_refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    return cast(str, jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))


def decode_token(token: str) -> dict[str, Any]:
    try:
        # jwt.decode() retorna dict[str, Any] pero los stubs lo marcan como Any
        payload = cast(dict[str, Any], jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token expirado")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Token inválido")