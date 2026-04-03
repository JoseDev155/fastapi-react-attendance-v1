# Librerias
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importar directorios del proyecto
from database import Base

# Modelo de carrera para la base de datos
class Career(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "careers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relacion inversa para SQLAlchemy
    career_signatures = relationship("CareerSignature", back_populates="career")