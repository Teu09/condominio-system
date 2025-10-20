from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.budgets import Budget, BudgetItem, BudgetHistory
from ..schemas.budgets import BudgetIn, BudgetUpdate, BudgetHistoryIn
from datetime import datetime


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_budget(self, budget_data: BudgetIn) -> Budget:
        db_budget = Budget(
            title=budget_data.title,
            description=budget_data.description,
            budget_type=budget_data.budget_type,
            supplier_name=budget_data.supplier_name,
            supplier_contact=budget_data.supplier_contact,
            total_amount=budget_data.total_amount,
            valid_until=budget_data.valid_until,
            requested_by=budget_data.requested_by,
            unit_id=budget_data.unit_id
        )
        
        self.db.add(db_budget)
        self.db.flush()  # Get the ID
        
        # Create budget items
        for item_data in budget_data.items:
            db_item = BudgetItem(
                budget_id=db_budget.id,
                description=item_data.description,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price
            )
            self.db.add(db_item)
        
        # Create initial history entry
        history_entry = BudgetHistory(
            budget_id=db_budget.id,
            action="created",
            description="Orçamento criado",
            changed_by=budget_data.requested_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    def get_budget(self, budget_id: int) -> Optional[Budget]:
        return self.db.query(Budget).filter(Budget.id == budget_id).first()

    def list_budgets(self, budget_type: Optional[str] = None, status: Optional[str] = None) -> List[Budget]:
        query = self.db.query(Budget)
        
        if budget_type:
            query = query.filter(Budget.budget_type == budget_type)
        if status:
            query = query.filter(Budget.status == status)
            
        return query.order_by(Budget.created_at.desc()).all()

    def update_budget(self, budget_id: int, update_data: BudgetUpdate) -> Optional[Budget]:
        db_budget = self.get_budget(budget_id)
        if not db_budget:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_budget, field, value)
        
        db_budget.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = BudgetHistory(
            budget_id=budget_id,
            action="updated",
            description=f"Orçamento atualizado: {', '.join(update_dict.keys())}",
            changed_by=update_data.approved_by or "Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    def approve_budget(self, budget_id: int, approved_by: str) -> Optional[Budget]:
        db_budget = self.get_budget(budget_id)
        if not db_budget:
            return None
        
        db_budget.status = "approved"
        db_budget.approved_by = approved_by
        db_budget.approved_at = datetime.utcnow()
        db_budget.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = BudgetHistory(
            budget_id=budget_id,
            action="approved",
            description="Orçamento aprovado",
            changed_by=approved_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    def reject_budget(self, budget_id: int, rejected_by: str, reason: str) -> Optional[Budget]:
        db_budget = self.get_budget(budget_id)
        if not db_budget:
            return None
        
        db_budget.status = "rejected"
        db_budget.rejection_reason = reason
        db_budget.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = BudgetHistory(
            budget_id=budget_id,
            action="rejected",
            description=f"Orçamento rejeitado: {reason}",
            changed_by=rejected_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    def delete_budget(self, budget_id: int) -> bool:
        db_budget = self.get_budget(budget_id)
        if not db_budget:
            return False
        
        self.db.delete(db_budget)
        self.db.commit()
        return True

    def get_budget_history(self, budget_id: int) -> List[BudgetHistory]:
        return self.db.query(BudgetHistory).filter(
            BudgetHistory.budget_id == budget_id
        ).order_by(BudgetHistory.created_at.desc()).all()

    def add_budget_history(self, history_data: BudgetHistoryIn) -> BudgetHistory:
        db_history = BudgetHistory(
            budget_id=history_data.budget_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_budget_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Budget).filter(
            Budget.created_at >= start_date,
            Budget.created_at <= end_date
        )
        
        total_budgets = query.count()
        total_amount = query.with_entities(Budget.total_amount).all()
        total_amount = sum([amount[0] for amount in total_amount])
        
        status_breakdown = {}
        type_breakdown = {}
        
        for budget in query.all():
            status_breakdown[budget.status] = status_breakdown.get(budget.status, 0) + 1
            type_breakdown[budget.budget_type] = type_breakdown.get(budget.budget_type, 0) + 1
        
        return {
            "total_budgets": total_budgets,
            "total_amount": total_amount,
            "status_breakdown": status_breakdown,
            "type_breakdown": type_breakdown
        }


