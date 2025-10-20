from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MinutesStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class MinutesIn(BaseModel):
    meeting_id: int
    title: str
    content: str
    decisions: List[str]
    action_items: List[str]
    attendees: List[str]
    absentees: List[str]
    next_meeting_date: Optional[datetime] = None
    created_by: str
    unit_id: Optional[int] = None


class MinutesOut(BaseModel):
    id: int
    meeting_id: int
    title: str
    content: str
    decisions: List[str]
    action_items: List[str]
    attendees: List[str]
    absentees: List[str]
    status: MinutesStatus
    next_meeting_date: Optional[datetime]
    created_by: str
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class MinutesUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    decisions: Optional[List[str]] = None
    action_items: Optional[List[str]] = None
    attendees: Optional[List[str]] = None
    absentees: Optional[List[str]] = None
    status: Optional[MinutesStatus] = None
    next_meeting_date: Optional[datetime] = None
    unit_id: Optional[int] = None


class MinutesHistoryIn(BaseModel):
    minutes_id: int
    action: str
    description: str
    changed_by: str


class MinutesHistoryOut(BaseModel):
    id: int
    minutes_id: int
    action: str
    description: str
    changed_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class MinutesApprovalIn(BaseModel):
    approved_by: str
    comments: Optional[str] = None


class MinutesRejectionIn(BaseModel):
    rejected_by: str
    reason: str
    comments: Optional[str] = None


