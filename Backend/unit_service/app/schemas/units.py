from pydantic import BaseModel
from typing import Optional


class UnitIn(BaseModel):
    block: str
    number: str
    owner_id: Optional[int] = None


class UnitOut(BaseModel):
    id: int
    block: str
    number: str
    owner_id: Optional[int] = None



















