# Librerias
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importar directorios del proyecto
from database import Base

# Modelo de usuario para la base de datos
class User(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(15), primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Relacion con el modelo de rol para SQLAlchemy
    role = relationship("Role", back_populates="users")
    
    # Relacion con grupos (el profesor a cargo)
    groups = relationship("Group", back_populates="user")