from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class EmployeeBase(BaseModel):
    employee_number: str
    name: str
    email: str
    department_id: Optional[int] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    status: Optional[str] = "active"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    employee_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    employee_id: Optional[int] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class DepartmentBase(BaseModel):
    name: str
    manager: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class AssetBase(BaseModel):
    asset_number: str
    asset_type: str
    name: str
    assigned_employee_id: Optional[int] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = "active"

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    employee_id: int
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TicketOut(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MachineBase(BaseModel):
    machine_number: str
    department: str
    status: Optional[str] = "running"
    hours_run: Optional[int] = 0

class MachineCreate(MachineBase):
    pass

class MachineUpdate(BaseModel):
    status: Optional[str] = None
    hours_run: Optional[int] = None

class MachineOut(MachineBase):
    id: int

    class Config:
        from_attributes = True