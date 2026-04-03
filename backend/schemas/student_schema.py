from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date

# 1. Base: solo campos comunes (publicos)
class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    email: EmailStr
    nickname: str

# 2. CREATE: lo que envia el cliente
class StudentCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    nickname: str
    enrollment_date: date
    is_active: bool = True

# 3. UPDATE: todos opcionales
class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    nickname: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class StudentResponse(StudentBase):
    id: str
    enrollment_date: date
    is_active: bool
