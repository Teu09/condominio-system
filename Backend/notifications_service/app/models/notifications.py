from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.notifications import NotificationType, NotificationStatus, NotificationPriority, EmailTemplateType


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(255), nullable=False, index=True)
    recipient_name = Column(String(255))
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    priority = Column(SQLEnum(NotificationPriority), default=NotificationPriority.MEDIUM, index=True)
    template_type = Column(SQLEnum(EmailTemplateType), index=True)
    template_data = Column(JSON)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING, index=True)
    scheduled_at = Column(DateTime, index=True)
    expires_at = Column(DateTime, index=True)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    failed_at = Column(DateTime)
    failure_reason = Column(Text)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), index=True)
    user_id = Column(String(255), index=True)
    related_entity_type = Column(String(100), index=True)
    related_entity_id = Column(String(100), index=True)
    attachments = Column(JSON)  # List of file paths
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    queue_entries = relationship("NotificationQueue", back_populates="notification", cascade="all, delete-orphan")


class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_type = Column(SQLEnum(EmailTemplateType), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=False)
    text_content = Column(Text)
    variables = Column(JSON)  # List of variable names
    is_active = Column(Boolean, default=True, index=True)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NotificationQueue(Base):
    __tablename__ = "notification_queue"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=False)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    next_retry_at = Column(DateTime, index=True)
    priority = Column(SQLEnum(NotificationPriority), default=NotificationPriority.MEDIUM, index=True)
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    notification = relationship("Notification", back_populates="queue_entries")


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    notification = relationship("Notification", backref="logs")

