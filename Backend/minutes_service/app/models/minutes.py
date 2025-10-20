from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.minutes import MinutesStatus


class Minutes(Base):
    __tablename__ = "minutes"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    decisions = Column(JSON)  # List of strings
    action_items = Column(JSON)  # List of strings
    attendees = Column(JSON)  # List of strings
    absentees = Column(JSON)  # List of strings
    status = Column(SQLEnum(MinutesStatus), default=MinutesStatus.DRAFT)
    next_meeting_date = Column(DateTime)
    created_by = Column(String(255), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    published_at = Column(DateTime)

    # Relationships
    history = relationship("MinutesHistory", back_populates="minutes", cascade="all, delete-orphan")


class MinutesHistory(Base):
    __tablename__ = "minutes_history"

    id = Column(Integer, primary_key=True, index=True)
    minutes_id = Column(Integer, ForeignKey("minutes.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    minutes = relationship("Minutes", back_populates="history")


