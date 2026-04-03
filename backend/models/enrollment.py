# Librerias
from sqlalchemy import Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
# Importar directorios del proyecto
from database import Base

# Modelo de incsripciones para la base de datos
class Enrollment(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "enrollments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    student_id: Mapped[str] = mapped_column(String(15), ForeignKey("students.id"), nullable=False)
    group_id: Mapped[str] = mapped_column(String(15), ForeignKey("groups.id"), nullable=False)
    
    # Relacion inversa para SQLAlchemy
    student = relationship("Student", back_populates="enrollments")
    group = relationship("Group", back_populates="enrollments")
    attendances = relationship("Attendance", back_populates="enrollment")