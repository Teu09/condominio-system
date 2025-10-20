from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Boolean, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.service_providers import ServiceType, ProviderStatus


class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False, index=True)
    cpf = Column(String(14), unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(2), nullable=False, index=True)
    zip_code = Column(String(10), nullable=False)
    service_types = Column(JSON, nullable=False)  # List of ServiceType enums
    description = Column(Text)
    hourly_rate = Column(Float)
    daily_rate = Column(Float)
    monthly_rate = Column(Float)
    is_contractor = Column(Boolean, default=False, index=True)
    contract_start_date = Column(Date)
    contract_end_date = Column(Date)
    insurance_number = Column(String(100))
    insurance_expiry = Column(Date)
    license_number = Column(String(100))
    license_expiry = Column(Date)
    rating = Column(Float, default=0.0, index=True)
    notes = Column(Text)
    status = Column(SQLEnum(ProviderStatus), default=ProviderStatus.PENDING, index=True)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    history = relationship("ServiceProviderHistory", back_populates="provider", cascade="all, delete-orphan")
    ratings = relationship("ServiceProviderRating", back_populates="provider", cascade="all, delete-orphan")


class ServiceProviderHistory(Base):
    __tablename__ = "service_provider_history"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("service_providers.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    provider = relationship("ServiceProvider", back_populates="history")


class ServiceProviderRating(Base):
    __tablename__ = "service_provider_ratings"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("service_providers.id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    rated_by = Column(String(255), nullable=False)
    service_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    provider = relationship("ServiceProvider", back_populates="ratings")

