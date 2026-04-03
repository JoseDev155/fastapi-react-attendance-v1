from pydantic import BaseModel, ConfigDict
from datetime import date

# 1. Base: solo campos comunes (publicos)
class AcademicCycleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cycle_name: str
    cycle_year: date

# 2. CREATE: lo que envia el cliente
class AcademicCycleCreate(BaseModel):
    cycle_name: str
    cycle_year: date

# 3. UPDATE: todos opcionales
class AcademicCycleUpdate(BaseModel):
    cycle_name: str | None = None
    cycle_year: date | None = None

# 4. RESPONSE: lo que retorna el servidor
class AcademicCycleResponse(AcademicCycleBase):
    id: int
