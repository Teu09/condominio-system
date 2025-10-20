from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.employees import Employee, EmployeeHistory
from ..schemas.employees import EmployeeIn, EmployeeUpdate, EmployeeHistoryIn, EmployeeTerminationIn, EmployeePromotionIn
from datetime import datetime, date


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, employee_data: EmployeeIn) -> Employee:
        db_employee = Employee(
            name=employee_data.name,
            document=employee_data.document,
            position=employee_data.position,
            department=employee_data.department,
            hire_date=employee_data.hire_date,
            salary=employee_data.salary,
            phone=employee_data.phone,
            email=employee_data.email,
            address=employee_data.address,
            emergency_contact=employee_data.emergency_contact,
            emergency_phone=employee_data.emergency_phone,
            work_schedule=employee_data.work_schedule,
            unit_id=employee_data.unit_id,
            created_by="Sistema"  # This should be passed from the service
        )
        
        self.db.add(db_employee)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = EmployeeHistory(
            employee_id=db_employee.id,
            action="created",
            description="Funcionário cadastrado",
            changed_by="Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def get_employee_by_document(self, document: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.document == document).first()

    def list_employees(self, 
                      status: Optional[str] = None,
                      position: Optional[str] = None,
                      department: Optional[str] = None,
                      unit_id: Optional[int] = None) -> List[Employee]:
        query = self.db.query(Employee)
        
        if status:
            query = query.filter(Employee.status == status)
        if position:
            query = query.filter(Employee.position == position)
        if department:
            query = query.filter(Employee.department == department)
        if unit_id:
            query = query.filter(Employee.unit_id == unit_id)
            
        return query.order_by(Employee.name.asc()).all()

    def update_employee(self, employee_id: int, update_data: EmployeeUpdate) -> Optional[Employee]:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return None
        
        # Store old values for history
        old_values = {
            "name": db_employee.name,
            "position": db_employee.position,
            "department": db_employee.department,
            "salary": db_employee.salary,
            "status": db_employee.status
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_employee, field, value)
        
        db_employee.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "name": db_employee.name,
            "position": db_employee.position,
            "department": db_employee.department,
            "salary": db_employee.salary,
            "status": db_employee.status
        }
        
        # Add history entry
        history_entry = EmployeeHistory(
            employee_id=employee_id,
            action="updated",
            description=f"Funcionário atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def terminate_employee(self, employee_id: int, termination_data: EmployeeTerminationIn) -> Optional[Employee]:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return None
        
        # Store old values for history
        old_values = {
            "status": db_employee.status,
            "termination_date": db_employee.termination_date,
            "termination_reason": db_employee.termination_reason
        }
        
        db_employee.status = "terminated"
        db_employee.termination_date = termination_data.termination_date
        db_employee.termination_reason = termination_data.termination_reason
        db_employee.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "status": db_employee.status,
            "termination_date": db_employee.termination_date,
            "termination_reason": db_employee.termination_reason
        }
        
        # Add history entry
        history_entry = EmployeeHistory(
            employee_id=employee_id,
            action="terminated",
            description=f"Funcionário demitido: {termination_data.termination_reason}",
            changed_by=termination_data.terminated_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def promote_employee(self, employee_id: int, promotion_data: EmployeePromotionIn) -> Optional[Employee]:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return None
        
        # Store old values for history
        old_values = {
            "position": db_employee.position,
            "department": db_employee.department,
            "salary": db_employee.salary
        }
        
        db_employee.position = promotion_data.new_position
        db_employee.department = promotion_data.new_department
        db_employee.salary = promotion_data.new_salary
        db_employee.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "position": db_employee.position,
            "department": db_employee.department,
            "salary": db_employee.salary
        }
        
        # Add history entry
        history_entry = EmployeeHistory(
            employee_id=employee_id,
            action="promoted",
            description=f"Funcionário promovido para {promotion_data.new_position} em {promotion_data.new_department}",
            changed_by=promotion_data.promoted_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def suspend_employee(self, employee_id: int, suspended_by: str, reason: str) -> Optional[Employee]:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return None
        
        # Store old values for history
        old_values = {"status": db_employee.status}
        
        db_employee.status = "suspended"
        db_employee.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_employee.status}
        
        # Add history entry
        history_entry = EmployeeHistory(
            employee_id=employee_id,
            action="suspended",
            description=f"Funcionário suspenso: {reason}",
            changed_by=suspended_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def reactivate_employee(self, employee_id: int, reactivated_by: str) -> Optional[Employee]:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return None
        
        # Store old values for history
        old_values = {"status": db_employee.status}
        
        db_employee.status = "active"
        db_employee.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_employee.status}
        
        # Add history entry
        history_entry = EmployeeHistory(
            employee_id=employee_id,
            action="reactivated",
            description="Funcionário reativado",
            changed_by=reactivated_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete_employee(self, employee_id: int) -> bool:
        db_employee = self.get_employee(employee_id)
        if not db_employee:
            return False
        
        self.db.delete(db_employee)
        self.db.commit()
        return True

    def get_employee_history(self, employee_id: int) -> List[EmployeeHistory]:
        return self.db.query(EmployeeHistory).filter(
            EmployeeHistory.employee_id == employee_id
        ).order_by(EmployeeHistory.created_at.desc()).all()

    def add_employee_history(self, history_data: EmployeeHistoryIn) -> EmployeeHistory:
        db_history = EmployeeHistory(
            employee_id=history_data.employee_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by,
            old_values=history_data.old_values,
            new_values=history_data.new_values
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_employees_by_position(self, position: str) -> List[Employee]:
        return self.db.query(Employee).filter(
            Employee.position == position
        ).order_by(Employee.name.asc()).all()

    def get_employees_by_department(self, department: str) -> List[Employee]:
        return self.db.query(Employee).filter(
            Employee.department == department
        ).order_by(Employee.name.asc()).all()

    def get_active_employees(self) -> List[Employee]:
        return self.db.query(Employee).filter(
            Employee.status == "active"
        ).order_by(Employee.name.asc()).all()

    def get_employees_stats(self, start_date: date, end_date: date) -> dict:
        query = self.db.query(Employee).filter(
            Employee.hire_date >= start_date,
            Employee.hire_date <= end_date
        )
        
        total_employees = query.count()
        
        position_breakdown = {}
        department_breakdown = {}
        status_breakdown = {}
        
        for employee in query.all():
            position_breakdown[employee.position] = position_breakdown.get(employee.position, 0) + 1
            department_breakdown[employee.department] = department_breakdown.get(employee.department, 0) + 1
            status_breakdown[employee.status] = status_breakdown.get(employee.status, 0) + 1
        
        return {
            "total_employees": total_employees,
            "position_breakdown": position_breakdown,
            "department_breakdown": department_breakdown,
            "status_breakdown": status_breakdown
        }


