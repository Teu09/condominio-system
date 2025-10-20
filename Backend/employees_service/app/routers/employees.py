from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.employees import EmployeeIn, EmployeeOut, EmployeeUpdate, EmployeeHistoryIn, EmployeeTerminationIn, EmployeePromotionIn
from ..services.employee_service import EmployeeService
from datetime import datetime, date

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeOut)
def create_employee(employee_data: EmployeeIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = EmployeeService(db)
    try:
        return service.create_employee(employee_data, created_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    status: Optional[str] = None,
    position: Optional[str] = None,
    department: Optional[str] = None,
    unit_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.list_employees(status, position, department, unit_id)


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.get("/document/{document}", response_model=EmployeeOut)
def get_employee_by_document(document: str, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.get_employee_by_document(document)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    update_data: EmployeeUpdate,
    changed_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    employee = service.update_employee(employee_id, update_data, changed_by)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.post("/{employee_id}/terminate", response_model=EmployeeOut)
def terminate_employee(
    employee_id: int,
    termination_data: EmployeeTerminationIn,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    employee = service.terminate_employee(employee_id, termination_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.post("/{employee_id}/promote", response_model=EmployeeOut)
def promote_employee(
    employee_id: int,
    promotion_data: EmployeePromotionIn,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    employee = service.promote_employee(employee_id, promotion_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.post("/{employee_id}/suspend")
def suspend_employee(
    employee_id: int,
    suspended_by: str,
    reason: str,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    employee = service.suspend_employee(employee_id, suspended_by, reason)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"message": "Funcionário suspenso com sucesso"}


@router.post("/{employee_id}/reactivate", response_model=EmployeeOut)
def reactivate_employee(
    employee_id: int,
    reactivated_by: str,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    employee = service.reactivate_employee(employee_id, reactivated_by)
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    success = service.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"message": "Funcionário excluído com sucesso"}


@router.get("/{employee_id}/history")
def get_employee_history(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employee_history(employee_id)


@router.get("/{employee_id}/work-history")
def get_employee_work_history(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employee_work_history(employee_id)


@router.get("/{employee_id}/salary-history")
def get_employee_salary_history(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employee_salary_history(employee_id)


@router.post("/{employee_id}/history", response_model=dict)
def add_employee_history(
    employee_id: int,
    history_data: EmployeeHistoryIn,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    history_data.employee_id = employee_id
    return service.add_employee_history(history_data)


@router.get("/position/{position}")
def get_employees_by_position(position: str, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employees_by_position(position)


@router.get("/department/{department}")
def get_employees_by_department(department: str, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employees_by_department(department)


@router.get("/status/{status}")
def get_employees_by_status(status: str, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employees_by_status(status)


@router.get("/unit/{unit_id}")
def get_employees_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employees_by_unit(unit_id)


@router.get("/active/list")
def get_active_employees(db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_active_employees()


@router.get("/search/{search_term}")
def search_employees(search_term: str, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.search_employees(search_term)


@router.get("/stats/summary")
def get_employees_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = EmployeeService(db)
    return service.get_employees_stats(start, end)


