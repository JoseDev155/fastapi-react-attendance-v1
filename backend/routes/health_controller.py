# Librerias
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
# Importar directorios del proyecto
from database import get_db


# Instancia del router de health
health_controller = APIRouter()


# RUTAS DE SALUD - PUBLICO
@health_controller.get("/health", tags=["system"],
                       description="Endpoint para verificar el estado de la API. Público, sin autenticación requerida.")
async def health_check(db: Session = Depends(get_db)) -> dict[str, object]:
    """
    Verifica el estado de salud de la API y la conexión a la base de datos.
    """
    try:
        # Verificar conexión a la base de datos
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "Sistema de Asistencias UBBJ",
            "version": "1.0",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Sistema de Asistencias UBBJ",
            "version": "1.0",
            "database": "disconnected",
            "error": str(e)
        }
