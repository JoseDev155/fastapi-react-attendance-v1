# Librerias
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importar directorios del proyecto
from database import Base

# Modelo de carrera-asignatura para la base de datos
class CareerSignature(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "career_signatures"
    
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    signature_id: Mapped[str] = mapped_column(String(15), ForeignKey("signatures.id"), nullable=False)
    career_id: Mapped[str] = mapped_column(String(15), ForeignKey("careers.id"), nullable=False)
    
    # Relacion inversa para SQLAlchemy
    signature = relationship("Signature", back_populates="career_signatures")
    career = relationship("Career", back_populates="career_signatures")
    groups = relationship("Group", back_populates="career_signature")