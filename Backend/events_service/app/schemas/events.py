from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    MEETING = "meeting"
    MAINTENANCE = "maintenance"
    SOCIAL = "social"
    ADMINISTRATIVE = "administrative"
    EMERGENCY = "emergency"
    OTHER = "other"


class EventPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EventIn(BaseModel):
    title: str
    description: str
    event_type: EventType
    priority: EventPriority
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    organizer: str
    attendees: Optional[List[str]] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    reminder_days: Optional[int] = None
    unit_id: Optional[int] = None


class EventOut(BaseModel):
    id: int
    title: str
    description: str
    event_type: EventType
    priority: EventPriority
    start_date: datetime
    end_date: datetime
    location: Optional[str]
    organizer: str
    attendees: Optional[List[str]]
    is_recurring: bool
    recurrence_pattern: Optional[str]
    reminder_days: Optional[int]
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    priority: Optional[EventPriority] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    attendees: Optional[List[str]] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    reminder_days: Optional[int] = None
    unit_id: Optional[int] = None


class EventHistoryIn(BaseModel):
    event_id: int
    action: str
    description: str
    changed_by: str


class EventHistoryOut(BaseModel):
    id: int
    event_id: int
    action: str
    description: str
    changed_by: str
    created_at: datetime

    class Config:
        from_attributes = True


