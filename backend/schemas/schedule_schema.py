from pydantic import BaseModel, ConfigDict
from datetime import time

# 1. Base: solo campos comunes (publicos)
class ScheduleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    day_of_week: int
    start_time: time
    end_time: time
    max_entry_minutes: int
    minutes_to_be_late: int
    group_id: str

# 2. CREATE: lo que envia el cliente
class ScheduleCreate(BaseModel):
    id: str
    day_of_week: int
    start_time: time
    end_time: time
    max_entry_minutes: int
    minutes_to_be_late: int
    group_id: str

# 3. UPDATE: todos opcionales
class ScheduleUpdate(BaseModel):
    day_of_week: int | None = None
    start_time: time | None = None
    end_time: time | None = None
    max_entry_minutes: int | None = None
    minutes_to_be_late: int | None = None
    group_id: str | None = None

# 4. RESPONSE: lo que retorna el servidor
class ScheduleResponse(ScheduleBase):
    id: str
