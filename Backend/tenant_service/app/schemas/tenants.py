from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TenantThemeConfig(BaseModel):
    primary_color: str = "#1976d2"
    secondary_color: str = "#dc004e"
    background_color: str = "#f5f5f5"
    text_color: str = "#333333"
    logo_url: Optional[str] = None
    custom_css: Optional[str] = None


class TenantIn(BaseModel):
    name: str
    cnpj: str
    address: str
    phone: str
    email: str
    theme_config: Optional[TenantThemeConfig] = None
    admin_email: str
    admin_password: str
    admin_name: str


class TenantOut(BaseModel):
    id: int
    name: str
    cnpj: str
    address: str
    phone: str
    email: str
    theme_config: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    theme_config: Optional[TenantThemeConfig] = None
    is_active: Optional[bool] = None


class RolePermission(BaseModel):
    role: str
    permissions: list[str]


class TenantRoleConfig(BaseModel):
    tenant_id: int
    roles: list[RolePermission]
