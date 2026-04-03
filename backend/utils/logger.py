import logging
from logging.handlers import RotatingFileHandler
import os

# Crear directorio si no existe
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Instanciar el logger principal
logger = logging.getLogger("antigravity_api")
logger.setLevel(logging.INFO)

# Formateador general
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 1. Handler para Consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 2. Handler giratorio para Todo (app.log) - Máx 5 MB, 3 Respaldos
app_handler = RotatingFileHandler(
    filename=os.path.join(LOGS_DIR, "app.log"),
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# 3. Handler giratorio para Errores (error.log)
error_handler = RotatingFileHandler(
    filename=os.path.join(LOGS_DIR, "error.log"),
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Limpiar handlers para evitar logs duplicados durante imports recargados
if logger.hasHandlers():
    logger.handlers.clear()

# Agregar manejadores al logger principal
logger.addHandler(console_handler)
logger.addHandler(app_handler)
logger.addHandler(error_handler)
