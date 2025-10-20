from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.budgets import BudgetType, BudgetStatus


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    budget_type = Column(SQLEnum(BudgetType), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    supplier_contact = Column(String(255))
    total_amount = Column(Float, nullable=False)
    status = Column(SQLEnum(BudgetStatus), default=BudgetStatus.DRAFT)
    valid_until = Column(DateTime, nullable=False)
    requested_by = Column(String(255), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)

    # Relationships
    items = relationship("BudgetItem", back_populates="budget", cascade="all, delete-orphan")
    history = relationship("BudgetHistory", back_populates="budget", cascade="all, delete-orphan")


class BudgetItem(Base):
    __tablename__ = "budget_items"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationships
    budget = relationship("Budget", back_populates="items")


class BudgetHistory(Base):
    __tablename__ = "budget_history"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    budget = relationship("Budget", back_populates="history")
