from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MeetingType(str, Enum):
    ASSEMBLY = "assembly"
    BOARD = "board"
    COMMITTEE = "committee"
    EMERGENCY = "emergency"
    REGULAR = "regular"
    OTHER = "other"


class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class MeetingIn(BaseModel):
    title: str
    description: str
    meeting_type: MeetingType
    scheduled_date: datetime
    location: str
    organizer: str
    attendees: List[str]
    agenda_items: List[str]
    is_public: bool = True
    requires_quorum: bool = False
    quorum_percentage: Optional[float] = None
    unit_id: Optional[int] = None


class MeetingOut(BaseModel):
    id: int
    title: str
    description: str
    meeting_type: MeetingType
    status: MeetingStatus
    scheduled_date: datetime
    location: str
    organizer: str
    attendees: List[str]
    agenda_items: List[str]
    is_public: bool
    requires_quorum: bool
    quorum_percentage: Optional[float]
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: str
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    actual_attendees: Optional[List[str]]

    class Config:
        from_attributes = True


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    meeting_type: Optional[MeetingType] = None
    status: Optional[MeetingStatus] = None
    scheduled_date: Optional[datetime] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    attendees: Optional[List[str]] = None
    agenda_items: Optional[List[str]] = None
    is_public: Optional[bool] = None
    requires_quorum: Optional[bool] = None
    quorum_percentage: Optional[float] = None
    unit_id: Optional[int] = None
    actual_attendees: Optional[List[str]] = None


class MeetingHistoryIn(BaseModel):
    meeting_id: int
    action: str
    description: str
    changed_by: str


class MeetingHistoryOut(BaseModel):
    id: int
    meeting_id: int
    action: str
    description: str
    changed_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class MeetingInvitationIn(BaseModel):
    meeting_id: int
    email: str
    name: str
    role: Optional[str] = None


class MeetingInvitationOut(BaseModel):
    id: int
    meeting_id: int
    email: str
    name: str
    role: Optional[str]
    sent_at: datetime
    status: str  # sent, delivered, opened, responded

    class Config:
        from_attributes = True


class MeetingMinutesIn(BaseModel):
    meeting_id: int
    content: str
    decisions: List[str]
    action_items: List[str]
    next_meeting_date: Optional[datetime] = None
    created_by: str


class MeetingMinutesOut(BaseModel):
    id: int
    meeting_id: int
    content: str
    decisions: List[str]
    action_items: List[str]
    next_meeting_date: Optional[datetime]
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True


