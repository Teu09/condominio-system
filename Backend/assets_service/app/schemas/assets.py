from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class AssetType(str, Enum):
    FURNITURE = "furniture"
    APPLIANCE = "appliance"
    EQUIPMENT = "equipment"
    VEHICLE = "vehicle"
    ELECTRONIC = "electronic"
    TOOL = "tool"
    DECORATION = "decoration"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    OTHER = "other"


class AssetStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DISPOSED = "disposed"
    LOST = "lost"
    STOLEN = "stolen"


class AssetCondition(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class AssetIn(BaseModel):
    name: str
    description: str
    asset_type: AssetType
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: date
    purchase_price: float
    supplier: Optional[str] = None
    warranty_expires: Optional[date] = None
    location: str
    condition: AssetCondition
    status: AssetStatus = AssetStatus.ACTIVE
    responsible_person: Optional[str] = None
    maintenance_schedule: Optional[str] = None
    notes: Optional[str] = None
    unit_id: Optional[int] = None


class AssetOut(BaseModel):
    id: int
    name: str
    description: str
    asset_type: AssetType
    brand: Optional[str]
    model: Optional[str]
    serial_number: Optional[str]
    purchase_date: date
    purchase_price: float
    supplier: Optional[str]
    warranty_expires: Optional[date]
    location: str
    condition: AssetCondition
    status: AssetStatus
    responsible_person: Optional[str]
    maintenance_schedule: Optional[str]
    notes: Optional[str]
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: str
    disposal_date: Optional[date]
    disposal_reason: Optional[str]

    class Config:
        from_attributes = True


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    asset_type: Optional[AssetType] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    supplier: Optional[str] = None
    warranty_expires: Optional[date] = None
    location: Optional[str] = None
    condition: Optional[AssetCondition] = None
    status: Optional[AssetStatus] = None
    responsible_person: Optional[str] = None
    maintenance_schedule: Optional[str] = None
    notes: Optional[str] = None
    unit_id: Optional[int] = None
    disposal_date: Optional[date] = None
    disposal_reason: Optional[str] = None


class AssetHistoryIn(BaseModel):
    asset_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class AssetHistoryOut(BaseModel):
    id: int
    asset_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class AssetMaintenanceIn(BaseModel):
    asset_id: int
    maintenance_type: str
    description: str
    cost: float
    performed_by: str
    maintenance_date: date
    next_maintenance_date: Optional[date] = None
    notes: Optional[str] = None


class AssetMaintenanceOut(BaseModel):
    id: int
    asset_id: int
    maintenance_type: str
    description: str
    cost: float
    performed_by: str
    maintenance_date: date
    next_maintenance_date: Optional[date]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AssetDisposalIn(BaseModel):
    disposal_date: date
    disposal_reason: str
    disposal_method: str
    disposal_value: Optional[float] = None
    disposed_by: str
    notes: Optional[str] = None


