from pydantic import BaseModel
from typing import Optional, Dict, Any


class LoginIn(BaseModel):
    tenant_id: Optional[int] = None
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: dict
    tenant: Optional[Dict[str, Any]] = None


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: str
    full_name: Optional[str] = None
    role: str
    permissions: list[str] = []
    is_active: bool


class TenantOut(BaseModel):
    id: int
    name: str
    cnpj: str
    theme_config: Optional[Dict[str, Any]] = None






