from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VisitorIn(BaseModel):
    name: str
    document: str
    unit_id: int
    visit_date: datetime
    expected_duration: int = 120  # minutes
    purpose: str
    contact_phone: Optional[str] = None


class VisitorOut(BaseModel):
    id: int
    name: str
    document: str
    unit_id: int
    visit_date: datetime
    expected_duration: int
    purpose: str
    contact_phone: Optional[str] = None
    status: str
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None


class VisitorUpdate(BaseModel):
    status: Optional[str] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None




