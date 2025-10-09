from pydantic import BaseModel
from typing import Optional


class UserIn(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = 'morador'
    document: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: str









