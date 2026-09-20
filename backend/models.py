from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    manager = Column(String)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position = Column(String)
    hire_date = Column(Date)
    status = Column(String, default="active")

    department = relationship("Department", back_populates="employees")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_number = Column(String, unique=True, nullable=False)
    asset_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    assigned_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    purchase_date = Column(Date, nullable=True)
    status = Column(String, default="active")


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_number = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    status = Column(String, default="running")
    hours_run = Column(Integer, default=0)