# Librerias
from sqlalchemy import SmallInteger, String, Time, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import time
# Importar directorios del proyecto
from database import Base

# Modelo de horario para la base de datos
class Schedule(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "schedules"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    max_entry_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    minutes_to_be_present: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("groups.id"), nullable=False)
    
    # Relacion con el modelo de grupo para SQLAlchemy
    group = relationship("Group", back_populates="schedules")