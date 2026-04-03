import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()

# Codifica caracteres especiales en la contraseña
password = urllib.parse.quote_plus(str(os.getenv("DB_PASSWORD")))

username = str(os.getenv("DB_USER"))
host = str(os.getenv("DB_HOST"))
port = str(os.getenv("DB_PORT"))
database = str(os.getenv("DB_NAME"))
driver = str(os.getenv("DB_PYTHON_DRIVER"))


# URL de conexion a la base de datos de PostgreSQL
database_url = f"postgresql+{driver}://{username}:{password}@{host}:{port}/{database}"

# Configuracion de la conexion a PostgreSQL
engine = create_engine(database_url)
#meta = MetaData()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()