from pydantic import BaseModel, ConfigDict
from datetime import date

# 1. Base: solo campos comunes (publicos)
class EnrollmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    enrollment_date: date
    student_id: str
    group_id: str

# 2. CREATE: lo que envia el cliente
class EnrollmentCreate(BaseModel):
    enrollment_date: date
    student_id: str
    group_id: str

# 3. UPDATE: todos opcionales
class EnrollmentUpdate(BaseModel):
    enrollment_date: date | None = None
    student_id: str | None = None
    group_id: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class EnrollmentResponse(EnrollmentBase):
    id: int
