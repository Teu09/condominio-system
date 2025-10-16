from pydantic import BaseModel
from typing import Optional, List


class UserIn(BaseModel):
    tenant_id: int
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = 'morador'
    document: Optional[str] = None
    permissions: Optional[List[str]] = None


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: str
    full_name: Optional[str] = None
    role: str
    permissions: List[str] = []
    is_active: bool


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None













