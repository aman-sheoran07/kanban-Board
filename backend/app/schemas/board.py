from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True