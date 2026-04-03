from pydantic import BaseModel, ConfigDict

# 1. Base: solo campos comunes (publicos)
class CareerSignatureBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    signature_id: str
    career_id: str

# 2. CREATE: lo que envia el cliente
class CareerSignatureCreate(BaseModel):
    id: str
    signature_id: str
    career_id: str

# 3. UPDATE: todos opcionales
class CareerSignatureUpdate(BaseModel):
    signature_id: str | None = None
    career_id: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class CareerSignatureResponse(CareerSignatureBase):
    id: str
