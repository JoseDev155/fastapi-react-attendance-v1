# Librerias
from sqlalchemy import String, Date, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
# Importar directorios del proyecto
from database import Base

# Modelo de estudiante para la base de datos
class Student(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "students"
    
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=True) # Apodos
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relacion inversa para SQLAlchemy
    enrollments = relationship("Enrollment", back_populates="student")