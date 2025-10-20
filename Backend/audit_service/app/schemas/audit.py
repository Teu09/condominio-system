from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ActionType(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    APPROVE = "approve"
    REJECT = "reject"
    PUBLISH = "publish"
    ARCHIVE = "archive"
    PIN = "pin"
    UNPIN = "unpin"
    VIEW = "view"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    SEND_EMAIL = "send_email"
    OTHER = "other"


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLogIn(BaseModel):
    user_id: str
    user_email: str
    action: ActionType
    resource_type: str
    resource_id: Optional[str] = None
    resource_name: Optional[str] = None
    description: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    log_level: LogLevel = LogLevel.INFO


class AuditLogOut(BaseModel):
    id: int
    user_id: str
    user_email: str
    action: ActionType
    resource_type: str
    resource_id: Optional[str]
    resource_name: Optional[str]
    description: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    session_id: Optional[str]
    tenant_id: Optional[int]
    unit_id: Optional[int]
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]
    log_level: LogLevel
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogSearchIn(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    action: Optional[ActionType] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    log_level: Optional[LogLevel] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    ip_address: Optional[str] = None
    session_id: Optional[str] = None


class AuditStatsIn(BaseModel):
    start_date: datetime
    end_date: datetime
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    group_by: Optional[str] = None  # user, action, resource_type, date


class AuditStatsOut(BaseModel):
    total_logs: int
    unique_users: int
    action_breakdown: Dict[str, int]
    resource_breakdown: Dict[str, int]
    user_breakdown: Dict[str, int]
    daily_breakdown: Dict[str, int]
    error_count: int
    warning_count: int
    most_active_user: Optional[str] = None
    most_common_action: Optional[str] = None
    most_common_resource: Optional[str] = None


class AuditReportIn(BaseModel):
    start_date: datetime
    end_date: datetime
    tenant_id: Optional[int] = None
    unit_id: Optional[int] = None
    user_id: Optional[str] = None
    action: Optional[ActionType] = None
    resource_type: Optional[str] = None
    format: str = "json"  # json, csv, pdf


class AuditReportOut(BaseModel):
    report_id: str
    format: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    created_at: datetime
    expires_at: datetime

