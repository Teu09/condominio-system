from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class NoticeType(str, Enum):
    GENERAL = "general"
    MAINTENANCE = "maintenance"
    SECURITY = "security"
    SOCIAL = "social"
    ADMINISTRATIVE = "administrative"
    EMERGENCY = "emergency"
    EVENT = "event"
    OTHER = "other"


class NoticePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NoticeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    EXPIRED = "expired"


class NoticeIn(BaseModel):
    title: str
    content: str
    notice_type: NoticeType
    priority: NoticePriority
    is_public: bool = True
    publish_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    target_audience: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    unit_id: Optional[int] = None
    created_by: str


class NoticeOut(BaseModel):
    id: int
    title: str
    content: str
    notice_type: NoticeType
    priority: NoticePriority
    status: NoticeStatus
    is_public: bool
    publish_date: Optional[datetime]
    expiry_date: Optional[datetime]
    target_audience: Optional[List[str]]
    tags: Optional[List[str]]
    unit_id: Optional[int]
    created_by: str
    created_at: datetime
    updated_at: datetime
    view_count: int
    is_pinned: bool

    class Config:
        from_attributes = True


class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    notice_type: Optional[NoticeType] = None
    priority: Optional[NoticePriority] = None
    status: Optional[NoticeStatus] = None
    is_public: Optional[bool] = None
    publish_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    target_audience: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    unit_id: Optional[int] = None
    is_pinned: Optional[bool] = None


class NoticeHistoryIn(BaseModel):
    notice_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class NoticeHistoryOut(BaseModel):
    id: int
    notice_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class NoticeBoardIn(BaseModel):
    title: str
    description: str
    location: str
    is_active: bool = True
    unit_id: Optional[int] = None


class NoticeBoardOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    is_active: bool
    unit_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class NoticeBoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    unit_id: Optional[int] = None


class NoticeViewIn(BaseModel):
    notice_id: int
    viewer_id: Optional[str] = None
    viewer_ip: Optional[str] = None


class NoticeViewOut(BaseModel):
    id: int
    notice_id: int
    viewer_id: Optional[str]
    viewer_ip: Optional[str]
    viewed_at: datetime

    class Config:
        from_attributes = True

