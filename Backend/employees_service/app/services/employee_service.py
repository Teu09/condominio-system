from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.employee_repository import EmployeeRepository
from ..schemas.employees import EmployeeIn, EmployeeOut, EmployeeUpdate, EmployeeHistoryIn, EmployeeTerminationIn, EmployeePromotionIn
from datetime import datetime, date


class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def create_employee(self, employee_data: EmployeeIn, created_by: str = "Sistema") -> EmployeeOut:
        # Check if employee with same document already exists
        existing_employee = self.repository.get_employee_by_document(employee_data.document)
        if existing_employee:
            raise ValueError("Já existe um funcionário com este documento")
        
        employee = self.repository.create_employee(employee_data)
        return EmployeeOut.from_orm(employee)

    def get_employee(self, employee_id: int) -> Optional[EmployeeOut]:
        employee = self.repository.get_employee(employee_id)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def get_employee_by_document(self, document: str) -> Optional[EmployeeOut]:
        employee = self.repository.get_employee_by_document(document)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def list_employees(self, 
                      status: Optional[str] = None,
                      position: Optional[str] = None,
                      department: Optional[str] = None,
                      unit_id: Optional[int] = None) -> List[EmployeeOut]:
        employees = self.repository.list_employees(status, position, department, unit_id)
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def update_employee(self, employee_id: int, update_data: EmployeeUpdate, changed_by: str = "Sistema") -> Optional[EmployeeOut]:
        employee = self.repository.update_employee(employee_id, update_data)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def terminate_employee(self, employee_id: int, termination_data: EmployeeTerminationIn) -> Optional[EmployeeOut]:
        employee = self.repository.terminate_employee(employee_id, termination_data)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def promote_employee(self, employee_id: int, promotion_data: EmployeePromotionIn) -> Optional[EmployeeOut]:
        employee = self.repository.promote_employee(employee_id, promotion_data)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def suspend_employee(self, employee_id: int, suspended_by: str, reason: str) -> Optional[EmployeeOut]:
        employee = self.repository.suspend_employee(employee_id, suspended_by, reason)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def reactivate_employee(self, employee_id: int, reactivated_by: str) -> Optional[EmployeeOut]:
        employee = self.repository.reactivate_employee(employee_id, reactivated_by)
        if employee:
            return EmployeeOut.from_orm(employee)
        return None

    def delete_employee(self, employee_id: int) -> bool:
        return self.repository.delete_employee(employee_id)

    def get_employee_history(self, employee_id: int) -> List[dict]:
        history = self.repository.get_employee_history(employee_id)
        return [
            {
                "id": entry.id,
                "action": entry.action,
                "description": entry.description,
                "changed_by": entry.changed_by,
                "old_values": entry.old_values,
                "new_values": entry.new_values,
                "created_at": entry.created_at
            }
            for entry in history
        ]

    def add_employee_history(self, history_data: EmployeeHistoryIn) -> dict:
        history = self.repository.add_employee_history(history_data)
        return {
            "id": history.id,
            "employee_id": history.employee_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "old_values": history.old_values,
            "new_values": history.new_values,
            "created_at": history.created_at
        }

    def get_employees_by_position(self, position: str) -> List[EmployeeOut]:
        employees = self.repository.get_employees_by_position(position)
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def get_employees_by_department(self, department: str) -> List[EmployeeOut]:
        employees = self.repository.get_employees_by_department(department)
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def get_active_employees(self) -> List[EmployeeOut]:
        employees = self.repository.get_active_employees()
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def get_employees_stats(self, start_date: date, end_date: date) -> dict:
        return self.repository.get_employees_stats(start_date, end_date)

    def get_employees_by_status(self, status: str) -> List[EmployeeOut]:
        employees = self.repository.list_employees(status=status)
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def get_employees_by_unit(self, unit_id: int) -> List[EmployeeOut]:
        employees = self.repository.list_employees(unit_id=unit_id)
        return [EmployeeOut.from_orm(employee) for employee in employees]

    def search_employees(self, search_term: str) -> List[EmployeeOut]:
        # This would need to be implemented in the repository
        # For now, we'll use a simple approach
        employees = self.repository.list_employees()
        filtered_employees = []
        
        for employee in employees:
            if (search_term.lower() in employee.name.lower() or 
                search_term.lower() in employee.document.lower() or
                (employee.email and search_term.lower() in employee.email.lower())):
                filtered_employees.append(employee)
        
        return [EmployeeOut.from_orm(employee) for employee in filtered_employees]

    def get_employee_work_history(self, employee_id: int) -> List[dict]:
        """Get work history including promotions, suspensions, etc."""
        history = self.repository.get_employee_history(employee_id)
        work_history = []
        
        for entry in history:
            if entry.action in ["created", "promoted", "suspended", "reactivated", "terminated"]:
                work_history.append({
                    "id": entry.id,
                    "action": entry.action,
                    "description": entry.description,
                    "changed_by": entry.changed_by,
                    "old_values": entry.old_values,
                    "new_values": entry.new_values,
                    "created_at": entry.created_at
                })
        
        return work_history

    def get_employee_salary_history(self, employee_id: int) -> List[dict]:
        """Get salary change history"""
        history = self.repository.get_employee_history(employee_id)
        salary_history = []
        
        for entry in history:
            if entry.action in ["created", "updated", "promoted"] and entry.new_values and "salary" in entry.new_values:
                salary_history.append({
                    "id": entry.id,
                    "action": entry.action,
                    "old_salary": entry.old_values.get("salary") if entry.old_values else None,
                    "new_salary": entry.new_values.get("salary"),
                    "changed_by": entry.changed_by,
                    "created_at": entry.created_at
                })
        
        return salary_history


