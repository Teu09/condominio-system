from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class EmployeePosition(str, Enum):
    PORTER = "porter"
    CLEANER = "cleaner"
    MAINTENANCE = "maintenance"
    SECURITY = "security"
    ADMINISTRATIVE = "administrative"
    MANAGER = "manager"
    OTHER = "other"


class EmployeeIn(BaseModel):
    name: str
    document: str
    position: EmployeePosition
    department: str
    hire_date: date
    salary: float
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    work_schedule: Optional[str] = None
    unit_id: Optional[int] = None


class EmployeeOut(BaseModel):
    id: int
    name: str
    document: str
    position: EmployeePosition
    department: str
    hire_date: date
    salary: float
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    emergency_contact: Optional[str]
    emergency_phone: Optional[str]
    work_schedule: Optional[str]
    status: EmployeeStatus
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: str
    termination_date: Optional[date]
    termination_reason: Optional[str]

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    position: Optional[EmployeePosition] = None
    department: Optional[str] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    work_schedule: Optional[str] = None
    status: Optional[EmployeeStatus] = None
    unit_id: Optional[int] = None
    termination_date: Optional[date] = None
    termination_reason: Optional[str] = None


class EmployeeHistoryIn(BaseModel):
    employee_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class EmployeeHistoryOut(BaseModel):
    id: int
    employee_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeTerminationIn(BaseModel):
    termination_date: date
    termination_reason: str
    terminated_by: str
    comments: Optional[str] = None


class EmployeePromotionIn(BaseModel):
    new_position: EmployeePosition
    new_department: str
    new_salary: float
    effective_date: date
    promoted_by: str
    comments: Optional[str] = None


