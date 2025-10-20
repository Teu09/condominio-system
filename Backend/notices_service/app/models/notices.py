from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.notices import NoticeType, NoticePriority, NoticeStatus


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    notice_type = Column(SQLEnum(NoticeType), nullable=False)
    priority = Column(SQLEnum(NoticePriority), default=NoticePriority.MEDIUM)
    status = Column(SQLEnum(NoticeStatus), default=NoticeStatus.DRAFT)
    is_public = Column(Boolean, default=True)
    publish_date = Column(DateTime)
    expiry_date = Column(DateTime)
    target_audience = Column(JSON)  # List of strings
    tags = Column(JSON)  # List of strings
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    view_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)

    # Relationships
    history = relationship("NoticeHistory", back_populates="notice", cascade="all, delete-orphan")
    views = relationship("NoticeView", back_populates="notice", cascade="all, delete-orphan")


class NoticeHistory(Base):
    __tablename__ = "notice_history"

    id = Column(Integer, primary_key=True, index=True)
    notice_id = Column(Integer, ForeignKey("notices.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    notice = relationship("Notice", back_populates="history")


class NoticeBoard(Base):
    __tablename__ = "notice_boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    notices = relationship("Notice", backref="board")


class NoticeView(Base):
    __tablename__ = "notice_views"

    id = Column(Integer, primary_key=True, index=True)
    notice_id = Column(Integer, ForeignKey("notices.id"), nullable=False)
    viewer_id = Column(String(255))
    viewer_ip = Column(String(45))
    viewed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    notice = relationship("Notice", back_populates="views")

