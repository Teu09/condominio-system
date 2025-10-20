from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.events import EventType, EventPriority


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(SQLEnum(EventType), nullable=False)
    priority = Column(SQLEnum(EventPriority), default=EventPriority.MEDIUM)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    organizer = Column(String(255), nullable=False)
    attendees = Column(JSON)  # List of strings
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(100))
    reminder_days = Column(Integer)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)

    # Relationships
    history = relationship("EventHistory", back_populates="event", cascade="all, delete-orphan")


class EventHistory(Base):
    __tablename__ = "event_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="history")
