from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EmailTemplateType(str, Enum):
    WELCOME = "welcome"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_ACTIVATION = "account_activation"
    MEETING_INVITATION = "meeting_invitation"
    MEETING_REMINDER = "meeting_reminder"
    MEETING_CANCELLED = "meeting_cancelled"
    MINUTES_READY = "minutes_ready"
    BUDGET_APPROVAL = "budget_approval"
    BUDGET_REJECTION = "budget_rejection"
    MAINTENANCE_REQUEST = "maintenance_request"
    MAINTENANCE_COMPLETED = "maintenance_completed"
    VISITOR_ARRIVAL = "visitor_arrival"
    VISITOR_DEPARTURE = "visitor_departure"
    RESERVATION_CONFIRMED = "reservation_confirmed"
    RESERVATION_CANCELLED = "reservation_cancelled"
    NOTICE_PUBLISHED = "notice_published"
    NOTICE_URGENT = "notice_urgent"
    EVENT_REMINDER = "event_reminder"
    DOCUMENT_EXPIRY = "document_expiry"
    CONTRACT_EXPIRY = "contract_expiry"
    PAYMENT_REMINDER = "payment_reminder"
    SYSTEM_ALERT = "system_alert"
    CUSTOM = "custom"


class NotificationIn(BaseModel):
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    subject: str
    message: str
    notification_type: NotificationType = NotificationType.EMAIL
    priority: NotificationPriority = NotificationPriority.MEDIUM
    template_type: Optional[EmailTemplateType] = None
    template_data: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    user_id: Optional[str] = None
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    attachments: Optional[List[str]] = None
    created_by: str


class NotificationOut(BaseModel):
    id: int
    recipient_email: str
    recipient_name: Optional[str]
    subject: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority
    template_type: Optional[EmailTemplateType]
    template_data: Optional[Dict[str, Any]]
    status: NotificationStatus
    scheduled_at: Optional[datetime]
    expires_at: Optional[datetime]
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    failed_at: Optional[datetime]
    failure_reason: Optional[str]
    tenant_id: Optional[int]
    unit_id: Optional[int]
    user_id: Optional[str]
    related_entity_type: Optional[str]
    related_entity_id: Optional[str]
    attachments: Optional[List[str]]
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None


class NotificationSearchIn(BaseModel):
    recipient_email: Optional[str] = None
    notification_type: Optional[NotificationType] = None
    status: Optional[NotificationStatus] = None
    priority: Optional[NotificationPriority] = None
    template_type: Optional[EmailTemplateType] = None
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    user_id: Optional[str] = None
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class EmailTemplateIn(BaseModel):
    template_type: EmailTemplateType
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: bool = True
    created_by: str


class EmailTemplateOut(BaseModel):
    id: int
    template_type: EmailTemplateType
    name: str
    subject: str
    html_content: str
    text_content: Optional[str]
    variables: Optional[List[str]]
    is_active: bool
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None


class NotificationStatsOut(BaseModel):
    total_notifications: int
    sent_notifications: int
    pending_notifications: int
    failed_notifications: int
    delivered_notifications: int
    cancelled_notifications: int
    type_breakdown: Dict[str, int]
    priority_breakdown: Dict[str, int]
    template_breakdown: Dict[str, int]
    daily_breakdown: Dict[str, int]
    success_rate: float
    average_delivery_time: Optional[float] = None


class BulkNotificationIn(BaseModel):
    recipient_emails: List[EmailStr]
    recipient_names: Optional[List[str]] = None
    subject: str
    message: str
    notification_type: NotificationType = NotificationType.EMAIL
    priority: NotificationPriority = NotificationPriority.MEDIUM
    template_type: Optional[EmailTemplateType] = None
    template_data: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    user_id: Optional[str] = None
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    attachments: Optional[List[str]] = None
    created_by: str


class NotificationQueueIn(BaseModel):
    notification_id: int
    retry_count: int = 0
    max_retries: int = 3
    next_retry_at: Optional[datetime] = None
    priority: NotificationPriority = NotificationPriority.MEDIUM


class NotificationQueueOut(BaseModel):
    id: int
    notification_id: int
    retry_count: int
    max_retries: int
    next_retry_at: Optional[datetime]
    priority: NotificationPriority
    status: NotificationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

