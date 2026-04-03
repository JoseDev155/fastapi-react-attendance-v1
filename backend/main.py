# main.py - Archivo principal de la aplicacion backend con FastAPI

# Librerias
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os
# Importar directorios del proyecto
from utils import limiter
from routers import (
    academic_cycle_controller, \
    attendance_controller, \
    auth_controller, \
    career_controller, \
    career_signature_controller, \
    enrollment_controller, \
    group_controller, \
    health_controller, \
    role_controller, \
    schedule_controller, \
    signature_controller, \
    student_controller, \
    user_controller)


# Crear una instancia de FastAPI
app = FastAPI()


# Cargar variables de entorno
load_dotenv()

# CONFIGURAR CORS
# Leer URLs de CORS desde .env (ej: "http://localhost:3000,http://localhost:8080")
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
cors_origins = [url.strip() for url in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# CONFIGURAR RATE LIMITING
app.state.limiter = limiter
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"detail": "Demasiadas solicitudes. Intenta más tarde."}
    )
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)  # type: ignore


# Agregar los controladores a la API
app.include_router(academic_cycle_controller)
app.include_router(attendance_controller)
app.include_router(auth_controller)
app.include_router(career_controller)
app.include_router(career_signature_controller)
app.include_router(enrollment_controller)
app.include_router(group_controller)
app.include_router(health_controller)
app.include_router(role_controller)
app.include_router(schedule_controller)
app.include_router(signature_controller)
app.include_router(student_controller)
app.include_router(user_controller)


# Ruta base de la API
@app.get("/")
async def root():
    raise HTTPException(
        status_code=404,
        detail="Ruta no encontrada. Revisa /docs para la documentación de la API"
    )