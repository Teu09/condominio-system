from pydantic import BaseModel
from typing import Optional


class LoginIn(BaseModel):
    company: Optional[str] = None
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: dict






