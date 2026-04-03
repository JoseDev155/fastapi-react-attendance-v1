# main.py - Archivo principal de la aplicacion backend con FastAPI

# Librerias
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os
import time
# Importar directorios del proyecto
from utils import limiter, logger
from routes import (
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
    user_controller, \
    exports_controller, \
    metrics_controller, \
    reports_controller, \
    uploads_controller)


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


# CONFIGURAR LOGGING MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        logger.error("Excepción no manejada en solicitud %s %s: %s", request.method, request.url.path, e, exc_info=True)
        raise e
    finally:
        process_time = (time.time() - start_time) * 1000
        logger.info(
            "%s %s | Status: %s | Processed in %.2fms",
            request.method,
            request.url.path,
            status_code,
            process_time
        )
        
    return response


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
app.include_router(exports_controller)
app.include_router(metrics_controller)
app.include_router(reports_controller)
app.include_router(uploads_controller)


# Ruta base de la API
@app.get("/")
async def root():
    raise HTTPException(
        status_code=404,
        detail="Ruta no encontrada. Revisa /docs para la documentación de la API"
    )