from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.assets import AssetType, AssetStatus, AssetCondition


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    asset_type = Column(SQLEnum(AssetType), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    purchase_date = Column(Date, nullable=False)
    purchase_price = Column(Float, nullable=False)
    supplier = Column(String(255))
    warranty_expires = Column(Date)
    location = Column(String(255), nullable=False)
    condition = Column(SQLEnum(AssetCondition), nullable=False)
    status = Column(SQLEnum(AssetStatus), default=AssetStatus.ACTIVE)
    responsible_person = Column(String(255))
    maintenance_schedule = Column(String(100))
    notes = Column(Text)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    disposal_date = Column(Date)
    disposal_reason = Column(Text)

    # Relationships
    history = relationship("AssetHistory", back_populates="asset", cascade="all, delete-orphan")
    maintenance = relationship("AssetMaintenance", back_populates="asset", cascade="all, delete-orphan")


class AssetHistory(Base):
    __tablename__ = "asset_history"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    asset = relationship("Asset", back_populates="history")


class AssetMaintenance(Base):
    __tablename__ = "asset_maintenance"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    maintenance_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    cost = Column(Float, nullable=False)
    performed_by = Column(String(255), nullable=False)
    maintenance_date = Column(Date, nullable=False)
    next_maintenance_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    asset = relationship("Asset", back_populates="maintenance")


