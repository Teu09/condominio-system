from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.budget_repository import BudgetRepository
from ..schemas.budgets import BudgetIn, BudgetOut, BudgetUpdate, BudgetHistoryIn
from datetime import datetime


class BudgetService:
    def __init__(self, db: Session):
        self.repository = BudgetRepository(db)

    def create_budget(self, budget_data: BudgetIn) -> BudgetOut:
        budget = self.repository.create_budget(budget_data)
        return BudgetOut.from_orm(budget)

    def get_budget(self, budget_id: int) -> Optional[BudgetOut]:
        budget = self.repository.get_budget(budget_id)
        if budget:
            return BudgetOut.from_orm(budget)
        return None

    def list_budgets(self, budget_type: Optional[str] = None, status: Optional[str] = None) -> List[BudgetOut]:
        budgets = self.repository.list_budgets(budget_type, status)
        return [BudgetOut.from_orm(budget) for budget in budgets]

    def update_budget(self, budget_id: int, update_data: BudgetUpdate) -> Optional[BudgetOut]:
        budget = self.repository.update_budget(budget_id, update_data)
        if budget:
            return BudgetOut.from_orm(budget)
        return None

    def approve_budget(self, budget_id: int, approved_by: str) -> Optional[BudgetOut]:
        budget = self.repository.approve_budget(budget_id, approved_by)
        if budget:
            return BudgetOut.from_orm(budget)
        return None

    def reject_budget(self, budget_id: int, rejected_by: str, reason: str) -> Optional[BudgetOut]:
        budget = self.repository.reject_budget(budget_id, rejected_by, reason)
        if budget:
            return BudgetOut.from_orm(budget)
        return None

    def delete_budget(self, budget_id: int) -> bool:
        return self.repository.delete_budget(budget_id)

    def get_budget_history(self, budget_id: int) -> List[dict]:
        history = self.repository.get_budget_history(budget_id)
        return [
            {
                "id": entry.id,
                "action": entry.action,
                "description": entry.description,
                "changed_by": entry.changed_by,
                "created_at": entry.created_at
            }
            for entry in history
        ]

    def add_budget_history(self, history_data: BudgetHistoryIn) -> dict:
        history = self.repository.add_budget_history(history_data)
        return {
            "id": history.id,
            "budget_id": history.budget_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "created_at": history.created_at
        }

    def get_budget_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_budget_stats(start_date, end_date)

    def get_pending_budgets(self) -> List[BudgetOut]:
        return self.list_budgets(status="pending")

    def get_approved_budgets(self) -> List[BudgetOut]:
        return self.list_budgets(status="approved")

    def get_budgets_by_type(self, budget_type: str) -> List[BudgetOut]:
        return self.list_budgets(budget_type=budget_type)

    def get_budgets_by_supplier(self, supplier_name: str) -> List[BudgetOut]:
        budgets = self.repository.db.query(self.repository.Budget).filter(
            self.repository.Budget.supplier_name.ilike(f"%{supplier_name}%")
        ).all()
        return [BudgetOut.from_orm(budget) for budget in budgets]


