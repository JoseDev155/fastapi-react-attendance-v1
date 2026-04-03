# Librerias
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Importar directorios del proyecto
from database import Base

# Modelo de grupo para la base de datos
class Group(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "groups"
    
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False) # Ej: "A", "B" o "101"
    user_id: Mapped[str] = mapped_column(String(15), ForeignKey("users.id")) # El profesor a cargo del grupo
    career_signature_id: Mapped[str] = mapped_column(String(15), ForeignKey("career_signatures.id")) # La materia
    academic_cycle_id: Mapped[int] = mapped_column(Integer, ForeignKey("academic_cycles.id")) # El ciclo academico
    
    # Relaciones
    schedules = relationship("Schedule", back_populates="group")
    enrollments = relationship("Enrollment", back_populates="group")
    career_signature = relationship("CareerSignature", back_populates="groups")
    user = relationship("User", back_populates="groups")
    academic_cycle = relationship("AcademicCycle", back_populates="groups")