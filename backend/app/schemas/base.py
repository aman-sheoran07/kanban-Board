from pydantic import BaseModel, EmailStr
from datetime import datetime

class TimestampModel(BaseModel):
    created_at: datetime | None = None

    class Config:
        from_attributes = True