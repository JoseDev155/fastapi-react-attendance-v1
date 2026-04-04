from pydantic import BaseModel, ConfigDict
from datetime import date, time

# 1. Base: solo campos comunes (publicos)
class AttendanceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    attendance_date: date
    arrival_time: time | None = None
    notes: str | None = None

# 2. CREATE: lo que envia el cliente
class AttendanceCreate(BaseModel):
    attendance_date: date
    arrival_time: time | None = None
    notes: str | None = None
    enrollment_id: int

# 3. UPDATE: todos opcionales
class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    arrival_time: time | None = None
    notes: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class AttendanceResponse(AttendanceBase):
    id: int
    enrollment_id: int

# 5. RESPONSE CALCULADO: Inyecta el status computado
class CalculatedAttendanceResponse(AttendanceResponse):
    status: str
