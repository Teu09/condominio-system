from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.family_members import RelationshipType, Gender, MaritalStatus


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    rg = Column(String(20), unique=True, index=True)
    birth_date = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    marital_status = Column(SQLEnum(MaritalStatus), nullable=False)
    relationship_type = Column(SQLEnum(RelationshipType), nullable=False)
    phone = Column(String(20))
    email = Column(String(255), index=True)
    address = Column(String(500))
    city = Column(String(100), index=True)
    state = Column(String(2), index=True)
    zip_code = Column(String(10))
    occupation = Column(String(255))
    employer = Column(String(255))
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(100))
    is_emergency_contact = Column(Boolean, default=False)
    is_authorized_visitor = Column(Boolean, default=False)
    is_resident = Column(Boolean, default=False)
    notes = Column(Text)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    main_resident_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    history = relationship("FamilyMemberHistory", back_populates="member", cascade="all, delete-orphan")
    documents = relationship("FamilyMemberDocument", back_populates="member", cascade="all, delete-orphan")


class FamilyMemberHistory(Base):
    __tablename__ = "family_member_history"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(Text)  # JSON stored as text
    new_values = Column(Text)  # JSON stored as text
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    member = relationship("FamilyMember", back_populates="history")


class FamilyMemberDocument(Base):
    __tablename__ = "family_member_documents"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    document_number = Column(String(100), nullable=False)
    issuing_authority = Column(String(255), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    file_path = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    member = relationship("FamilyMember", back_populates="documents")

