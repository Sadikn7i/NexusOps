from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Company Management System API is running"}


@app.get("/api/employees", response_model=list[schemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.Employee).all()


@app.get("/api/employees/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/api/employees", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.put("/api/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted"}


@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = auth.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed,
        role=user.role,
        employee_id=user.employee_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/departments", response_model=list[schemas.DepartmentOut])
def get_departments(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.Department).all()


@app.post("/api/departments", response_model=schemas.DepartmentOut)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin"]))):
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@app.put("/api/departments/{department_id}", response_model=schemas.DepartmentOut)
def update_department(department_id: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin"]))):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    for key, value in department.model_dump().items():
        setattr(db_department, key, value)
    db.commit()
    db.refresh(db_department)
    return db_department


@app.delete("/api/departments/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin"]))):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_department)
    db.commit()
    return {"message": "Department deleted"}


@app.get("/api/assets", response_model=list[schemas.AssetOut])
def get_assets(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.Asset).all()


@app.post("/api/assets", response_model=schemas.AssetOut)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.put("/api/assets/{asset_id}", response_model=schemas.AssetOut)
def update_asset(asset_id: int, asset: schemas.AssetUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in asset.model_dump().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.delete("/api/assets/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"message": "Asset deleted"}


@app.get("/api/tickets", response_model=list[schemas.TicketOut])
def get_tickets(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    if current_user["role"] in ["admin", "it_staff"]:
        return db.query(models.SupportTicket).all()
    user = db.query(models.User).filter(models.User.username == current_user["username"]).first()
    return db.query(models.SupportTicket).filter(models.SupportTicket.employee_id == user.employee_id).all()


@app.post("/api/tickets", response_model=schemas.TicketOut)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_ticket = models.SupportTicket(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.put("/api/tickets/{ticket_id}", response_model=schemas.TicketOut)
def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_ticket = db.query(models.SupportTicket).filter(models.SupportTicket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in ticket.model_dump(exclude_unset=True).items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.get("/api/machines", response_model=list[schemas.MachineOut])
def get_machines(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return db.query(models.Machine).all()


@app.post("/api/machines", response_model=schemas.MachineOut)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_machine = models.Machine(**machine.model_dump())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine


@app.put("/api/machines/{machine_id}", response_model=schemas.MachineOut)
def update_machine(machine_id: int, machine: schemas.MachineUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.require_role(["admin", "it_staff"]))):
    db_machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    for key, value in machine.model_dump(exclude_unset=True).items():
        setattr(db_machine, key, value)
    db.commit()
    db.refresh(db_machine)
    return db_machine