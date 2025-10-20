from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    CONTRACT = "contract"
    REGULATION = "regulation"
    MANUAL = "manual"
    CERTIFICATE = "certificate"
    LICENSE = "license"
    PERMIT = "permit"
    REPORT = "report"
    MINUTES = "minutes"
    BUDGET = "budget"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    OTHER = "other"


class DocumentStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class DocumentIn(BaseModel):
    title: str
    description: str
    document_type: DocumentType
    file_path: str
    file_name: str
    file_size: int
    mime_type: str
    version: str = "1.0"
    is_public: bool = True
    requires_approval: bool = False
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    unit_id: Optional[int] = None
    created_by: str


class DocumentOut(BaseModel):
    id: int
    title: str
    description: str
    document_type: DocumentType
    file_path: str
    file_name: str
    file_size: int
    mime_type: str
    version: str
    status: DocumentStatus
    is_public: bool
    requires_approval: bool
    expires_at: Optional[datetime]
    tags: Optional[List[str]]
    unit_id: Optional[int]
    created_by: str
    created_at: datetime
    updated_at: datetime
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    published_at: Optional[datetime]
    download_count: int

    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None
    version: Optional[str] = None
    status: Optional[DocumentStatus] = None
    is_public: Optional[bool] = None
    requires_approval: Optional[bool] = None
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    unit_id: Optional[int] = None


class DocumentHistoryIn(BaseModel):
    document_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None


class DocumentHistoryOut(BaseModel):
    id: int
    document_id: int
    action: str
    description: str
    changed_by: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentApprovalIn(BaseModel):
    approved_by: str
    comments: Optional[str] = None


class DocumentRejectionIn(BaseModel):
    rejected_by: str
    reason: str
    comments: Optional[str] = None


class DocumentSearchIn(BaseModel):
    query: Optional[str] = None
    document_type: Optional[DocumentType] = None
    status: Optional[DocumentStatus] = None
    tags: Optional[List[str]] = None
    unit_id: Optional[int] = None
    created_by: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


