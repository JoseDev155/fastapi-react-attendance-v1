# Librerias
import enum
from sqlalchemy import CheckConstraint, Integer, Date, Time, Enum, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, time
# Importar directorios del proyecto
from database import Base

# Definir el Enum en Python para tener autocompletado y seguridad
class AttendanceStatus(enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    JUSTIFIED = "JUSTIFIED"
    LEFT_EARLY = "LEFT_EARLY"

# Modelo de asistencia para la base de datos
class Attendance(Base):
    __tablename__ = "attendances"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    arrival_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    # Configurar el Enum para que NO sea nativo de Postgres
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus, native_enum=False), 
        nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    enrollment_id: Mapped[int] = mapped_column(Integer, ForeignKey("enrollments.id"), nullable=False)
    
    enrollment = relationship("Enrollment", back_populates="attendances")

    # Opcional: Agregar el CheckConstraint también en el modelo para que SQLAlchemy lo incluya si alguna vez generas migraciones automáticas.
    __table_args__ = (
        UniqueConstraint("enrollment_id", "attendance_date", name="uq_attendance_day"),
        CheckConstraint(
            status.in_([s.value for s in AttendanceStatus]), 
            name="check_attendance_status"
        ),
    )