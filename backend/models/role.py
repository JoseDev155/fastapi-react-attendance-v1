# Librerias
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importar directorios del proyecto
from database import Base

# Modelo de rol de usuarios para la base de datos
class Role(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relacion inversa para SQLAlchemy
    users = relationship("User", back_populates="role")