from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class ServiceType(str, Enum):
    MAINTENANCE = "maintenance"
    CLEANING = "cleaning"
    SECURITY = "security"
    GARDENING = "gardening"
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    PAINTING = "painting"
    CONSTRUCTION = "construction"
    DELIVERY = "delivery"
    OTHER = "other"


class ProviderStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    REJECTED = "rejected"


class ServiceProviderIn(BaseModel):
    name: str
    company_name: str
    cnpj: str
    cpf: Optional[str] = None
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    service_types: List[ServiceType]
    description: str
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
    is_contractor: bool = False
    contract_start_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    insurance_number: Optional[str] = None
    insurance_expiry: Optional[date] = None
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    rating: Optional[float] = None
    notes: Optional[str] = None
    created_by: str


class ServiceProviderOut(BaseModel):
    id: int
    name: str
    company_name: str
    cnpj: str
    cpf: Optional[str]
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    service_types: List[ServiceType]
    description: str
    hourly_rate: Optional[float]
    daily_rate: Optional[float]
    monthly_rate: Optional[float]
    is_contractor: bool
    contract_start_date: Optional[date]
    contract_end_date: Optional[date]
    insurance_number: Optional[str]
    insurance_expiry: Optional[date]
    license_number: Optional[str]
    license_expiry: Optional[date]
    rating: Optional[float]
    notes: Optional[str]
    status: ProviderStatus
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServiceProviderUpdate(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    cnpj: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    service_types: Optional[List[ServiceType]] = None
    description: Optional[str] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
    is_contractor: Optional[bool] = None
    contract_start_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    insurance_number: Optional[str] = None
    insurance_expiry: Optional[date] = None
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    rating: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[ProviderStatus] = None


class ServiceProviderHistoryIn(BaseModel):
    provider_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class ServiceProviderHistoryOut(BaseModel):
    id: int
    provider_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceProviderRatingIn(BaseModel):
    provider_id: int
    rating: float
    comment: Optional[str] = None
    rated_by: str
    service_date: Optional[date] = None


class ServiceProviderRatingOut(BaseModel):
    id: int
    provider_id: int
    rating: float
    comment: Optional[str]
    rated_by: str
    service_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceProviderSearchIn(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    service_types: Optional[List[ServiceType]] = None
    status: Optional[ProviderStatus] = None
    is_contractor: Optional[bool] = None
    city: Optional[str] = None
    state: Optional[str] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


class ServiceProviderStatsOut(BaseModel):
    total_providers: int
    active_providers: int
    inactive_providers: int
    suspended_providers: int
    pending_providers: int
    rejected_providers: int
    contractors: int
    non_contractors: int
    service_type_breakdown: dict
    city_breakdown: dict
    state_breakdown: dict
    average_rating: Optional[float]
    top_rated_providers: List[dict]
    recent_providers: List[dict]

