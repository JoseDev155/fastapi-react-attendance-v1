# Librerias
from sqlalchemy import Integer, Date, Time, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, time
# Importar directorios del proyecto
from database import Base

# Modelo de asistencia para la base de datos
class Attendance(Base):
    __tablename__ = "attendances"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    arrival_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    enrollment_id: Mapped[int] = mapped_column(Integer, ForeignKey("enrollments.id"), nullable=False)
    
    enrollment = relationship("Enrollment", back_populates="attendances")

    __table_args__ = (
        UniqueConstraint("enrollment_id", "attendance_date", name="uq_attendance_day"),
    )