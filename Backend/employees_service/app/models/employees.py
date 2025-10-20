from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.db import Base
from ..schemas.employees import EmployeeStatus, EmployeePosition


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    document = Column(String(20), nullable=False, unique=True)
    position = Column(SQLEnum(EmployeePosition), nullable=False)
    department = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    emergency_contact = Column(String(255))
    emergency_phone = Column(String(20))
    work_schedule = Column(String(100))
    status = Column(SQLEnum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    unit_id = Column(Integer, ForeignKey("units.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    termination_date = Column(Date)
    termination_reason = Column(Text)

    # Relationships
    history = relationship("EmployeeHistory", back_populates="employee", cascade="all, delete-orphan")


class EmployeeHistory(Base):
    __tablename__ = "employee_history"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    changed_by = Column(String(255), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="history")


