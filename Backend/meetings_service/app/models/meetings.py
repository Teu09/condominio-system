from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.meetings import MeetingType, MeetingStatus


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    meeting_type = Column(SQLEnum(MeetingType), nullable=False)
    status = Column(SQLEnum(MeetingStatus), default=MeetingStatus.SCHEDULED)
    scheduled_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    organizer = Column(String(255), nullable=False)
    attendees = Column(JSON)  # List of strings
    agenda_items = Column(JSON)  # List of strings
    is_public = Column(Boolean, default=True)
    requires_quorum = Column(Boolean, default=False)
    quorum_percentage = Column(Float)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    actual_attendees = Column(JSON)  # List of strings

    # Relationships
    history = relationship("MeetingHistory", back_populates="meeting", cascade="all, delete-orphan")
    invitations = relationship("MeetingInvitation", back_populates="meeting", cascade="all, delete-orphan")
    minutes = relationship("MeetingMinutes", back_populates="meeting", cascade="all, delete-orphan")


class MeetingHistory(Base):
    __tablename__ = "meeting_history"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    meeting = relationship("Meeting", back_populates="history")


class MeetingInvitation(Base):
    __tablename__ = "meeting_invitations"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(100))
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="sent")  # sent, delivered, opened, responded

    # Relationships
    meeting = relationship("Meeting", back_populates="invitations")


class MeetingMinutes(Base):
    __tablename__ = "meeting_minutes"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    content = Column(Text, nullable=False)
    decisions = Column(JSON)  # List of strings
    action_items = Column(JSON)  # List of strings
    next_meeting_date = Column(DateTime)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    meeting = relationship("Meeting", back_populates="minutes")


