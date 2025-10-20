from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.documents import DocumentType, DocumentStatus


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    version = Column(String(20), default="1.0")
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.DRAFT)
    is_public = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    expires_at = Column(DateTime)
    tags = Column(JSON)  # List of strings
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    published_at = Column(DateTime)
    download_count = Column(Integer, default=0)

    # Relationships
    history = relationship("DocumentHistory", back_populates="document", cascade="all, delete-orphan")


class DocumentHistory(Base):
    __tablename__ = "document_history"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="history")


