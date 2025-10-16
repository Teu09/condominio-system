from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MaintenanceIn(BaseModel):
    unit_id: int
    title: str
    description: str
    priority: str = 'medium'  # low, medium, high, urgent
    category: str  # plumbing, electrical, cleaning, security, etc.
    requested_by: int  # user_id
    expected_date: Optional[datetime] = None


class MaintenanceOut(BaseModel):
    id: int
    unit_id: int
    title: str
    description: str
    priority: str
    category: str
    requested_by: int
    status: str
    expected_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    completed_date: Optional[datetime] = None
    created_at: datetime


class MaintenanceUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    completed_date: Optional[datetime] = None








