from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.budgets import BudgetIn, BudgetOut, BudgetUpdate, BudgetHistoryIn
from ..services.budget_service import BudgetService
from datetime import datetime

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=BudgetOut)
def create_budget(budget_data: BudgetIn, db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.create_budget(budget_data)


@router.get("/", response_model=List[BudgetOut])
def list_budgets(
    budget_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = BudgetService(db)
    return service.list_budgets(budget_type, status)


@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    service = BudgetService(db)
    budget = service.get_budget(budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return budget


@router.put("/{budget_id}", response_model=BudgetOut)
def update_budget(
    budget_id: int,
    update_data: BudgetUpdate,
    db: Session = Depends(get_db)
):
    service = BudgetService(db)
    budget = service.update_budget(budget_id, update_data)
    if not budget:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return budget


@router.post("/{budget_id}/approve", response_model=BudgetOut)
def approve_budget(
    budget_id: int,
    approved_by: str,
    db: Session = Depends(get_db)
):
    service = BudgetService(db)
    budget = service.approve_budget(budget_id, approved_by)
    if not budget:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return budget


@router.post("/{budget_id}/reject", response_model=BudgetOut)
def reject_budget(
    budget_id: int,
    rejected_by: str,
    reason: str,
    db: Session = Depends(get_db)
):
    service = BudgetService(db)
    budget = service.reject_budget(budget_id, rejected_by, reason)
    if not budget:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return budget


@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    service = BudgetService(db)
    success = service.delete_budget(budget_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    return {"message": "Orçamento excluído com sucesso"}


@router.get("/{budget_id}/history")
def get_budget_history(budget_id: int, db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.get_budget_history(budget_id)


@router.post("/{budget_id}/history", response_model=dict)
def add_budget_history(
    budget_id: int,
    history_data: BudgetHistoryIn,
    db: Session = Depends(get_db)
):
    service = BudgetService(db)
    history_data.budget_id = budget_id
    return service.add_budget_history(history_data)


@router.get("/stats/summary")
def get_budget_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = BudgetService(db)
    return service.get_budget_stats(start, end)


@router.get("/pending/list")
def get_pending_budgets(db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.get_pending_budgets()


@router.get("/approved/list")
def get_approved_budgets(db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.get_approved_budgets()


@router.get("/type/{budget_type}")
def get_budgets_by_type(budget_type: str, db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.get_budgets_by_type(budget_type)


@router.get("/supplier/{supplier_name}")
def get_budgets_by_supplier(supplier_name: str, db: Session = Depends(get_db)):
    service = BudgetService(db)
    return service.get_budgets_by_supplier(supplier_name)


