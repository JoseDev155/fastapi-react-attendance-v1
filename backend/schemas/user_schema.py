from pydantic import BaseModel, ConfigDict, EmailStr

# 1. Base: solo campos comunes (publicos)
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    email: EmailStr

# 2. CREATE: lo que envia el cliente (id, password, role_id)
class UserCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: int

# 3. UPDATE: todos opcionales
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None

# 4. RESPONSE: lo que retorna el servidor (sin password)
class UserResponse(UserBase):
    id: str
    role_id: int
    is_active: bool