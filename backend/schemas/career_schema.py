from pydantic import BaseModel, ConfigDict

# 1. Base: solo campos comunes (publicos)
class CareerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None

# 2. CREATE: lo que envia el cliente
class CareerCreate(BaseModel):
    name: str
    description: str | None = None

# 3. UPDATE: todos opcionales
class CareerUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class CareerResponse(CareerBase):
    id: int
    is_active: bool
