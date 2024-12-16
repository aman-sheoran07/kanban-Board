from pydantic import BaseModel
from typing import List

class CardPosition(BaseModel):
    id: int
    position: int
    list_id: int

class ListPosition(BaseModel):
    id: int
    position: int

class CardPositionUpdate(BaseModel):
    cards: List[CardPosition]

class ListPositionUpdate(BaseModel):
    lists: List[ListPosition]