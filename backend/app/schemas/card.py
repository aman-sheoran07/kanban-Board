from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    position: int
    due_date: Optional[datetime] = None

class CardCreate(CardBase):
    list_id: int

class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

class CardResponse(CardBase):
    id: int
    list_id: int
    assigned_to_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True