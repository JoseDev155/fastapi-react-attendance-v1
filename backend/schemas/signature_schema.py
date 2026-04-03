from pydantic import BaseModel, ConfigDict

# 1. Base: solo campos comunes (publicos)
class SignatureBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None

# 2. CREATE: lo que envia el cliente
class SignatureCreate(BaseModel):
    id: str
    name: str
    description: str | None = None

# 3. UPDATE: todos opcionales
class SignatureUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class SignatureResponse(SignatureBase):
    id: str
    is_active: bool
