from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.audit import ActionType, LogLevel


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    user_email = Column(String(255), nullable=False, index=True)
    action = Column(SQLEnum(ActionType), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), index=True)
    resource_name = Column(String(255))
    description = Column(Text, nullable=False)
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    session_id = Column(String(255), index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), index=True)
    old_values = Column(JSON)
    new_values = Column(JSON)
    metadata = Column(JSON)
    log_level = Column(SQLEnum(LogLevel), default=LogLevel.INFO, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Create composite indexes for common queries
    __table_args__ = (
        Index('idx_user_action', 'user_id', 'action'),
        Index('idx_resource_action', 'resource_type', 'action'),
        Index('idx_tenant_date', 'tenant_id', 'created_at'),
        Index('idx_unit_date', 'unit_id', 'created_at'),
        Index('idx_date_level', 'created_at', 'log_level'),
    )


class AuditReport(Base):
    __tablename__ = "audit_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=False)
    format = Column(String(10), nullable=False)
    file_path = Column(String(500))
    download_url = Column(String(500))
    filters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, failed

