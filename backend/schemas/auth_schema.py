# Librerias
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenResponse(BaseModel):
    # Respuesta con tokens despues del login
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str = Field(..., description="Token de acceso para autenticación")
    refresh_token: str = Field(..., description="Token para renovar el access token")
    token_type: str = Field(default="bearer", description="Tipo de token")
    user_id: str = Field(..., description="ID del usuario autenticado")
    user_name: str = Field(..., description="Nombre del usuario")


class LoginRequest(BaseModel):
    # Datos necesarios para login
    username: str = Field(..., description="ID de usuario o email", min_length=1)
    password: str = Field(..., description="Contraseña del usuario", min_length=6)


class RegisterRequest(BaseModel):
    # Datos necesarios para registro
    id: str = Field(..., description="ID único del usuario", min_length=1, max_length=15)
    first_name: str = Field(..., description="Nombre del usuario", min_length=1)
    last_name: str = Field(..., description="Apellido del usuario", min_length=1)
    email: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(..., description="Contraseña del usuario", min_length=8)
    password_confirm: str = Field(..., description="Confirmación de contraseña")
    role_id: int = Field(default=3, description="ID del rol (1=Admin, 2=Profesor, 3=Estudiante)")


class RefreshTokenRequest(BaseModel):
    # Solicitud para renovar token
    refresh_token: str = Field(..., description="Refresh token")


class ChangePasswordRequest(BaseModel):
    # Solicitud para cambiar contraseña
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., description="Nueva contraseña", min_length=8)
    password_confirm: str = Field(..., description="Confirmación de nueva contraseña")
