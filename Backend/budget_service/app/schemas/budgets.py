from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BudgetType(str, Enum):
    PURCHASE = "purchase"
    SERVICE = "service"


class BudgetStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class BudgetItemIn(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total_price: float


class BudgetIn(BaseModel):
    title: str
    description: str
    budget_type: BudgetType
    supplier_name: str
    supplier_contact: Optional[str] = None
    items: List[BudgetItemIn]
    total_amount: float
    valid_until: datetime
    requested_by: str
    unit_id: Optional[int] = None


class BudgetOut(BaseModel):
    id: int
    title: str
    description: str
    budget_type: BudgetType
    supplier_name: str
    supplier_contact: Optional[str]
    total_amount: float
    status: BudgetStatus
    valid_until: datetime
    requested_by: str
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]

    class Config:
        from_attributes = True


class BudgetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    total_amount: Optional[float] = None
    valid_until: Optional[datetime] = None
    status: Optional[BudgetStatus] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None


class BudgetHistoryIn(BaseModel):
    budget_id: int
    action: str
    description: str
    changed_by: str


class BudgetHistoryOut(BaseModel):
    id: int
    budget_id: int
    action: str
    description: str
    changed_by: str
    created_at: datetime

    class Config:
        from_attributes = True


