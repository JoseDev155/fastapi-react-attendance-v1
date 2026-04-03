from pydantic import BaseModel, ConfigDict

# 1. Base: solo campos comunes (publicos)
class GroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    user_id: str
    career_signature_id: str
    academic_cycle_id: int

# 2. CREATE: lo que envia el cliente
class GroupCreate(BaseModel):
    id: str
    name: str
    user_id: str
    career_signature_id: str
    academic_cycle_id: int

# 3. UPDATE: todos opcionales
class GroupUpdate(BaseModel):
    name: str | None = None
    user_id: str | None = None
    career_signature_id: str | None = None
    academic_cycle_id: int | None = None

# 4. RESPONSE: lo que retorna el servidor
class GroupResponse(GroupBase):
    id: str
