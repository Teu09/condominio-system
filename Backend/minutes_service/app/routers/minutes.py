from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.minutes import MinutesIn, MinutesOut, MinutesUpdate, MinutesHistoryIn, MinutesApprovalIn, MinutesRejectionIn
from ..services.minutes_service import MinutesService
from datetime import datetime

router = APIRouter(prefix="/minutes", tags=["minutes"])


@router.post("/", response_model=MinutesOut)
def create_minutes(minutes_data: MinutesIn, db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.create_minutes(minutes_data)


@router.get("/", response_model=List[MinutesOut])
def list_minutes(
    status: Optional[str] = None,
    unit_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    
    start_dt = None
    end_dt = None
    
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data de início inválido")
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data de fim inválido")
    
    return service.list_minutes(status, unit_id, start_dt, end_dt)


@router.get("/{minutes_id}", response_model=MinutesOut)
def get_minutes(minutes_id: int, db: Session = Depends(get_db)):
    service = MinutesService(db)
    minutes = service.get_minutes(minutes_id)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.get("/meeting/{meeting_id}", response_model=MinutesOut)
def get_minutes_by_meeting(meeting_id: int, db: Session = Depends(get_db)):
    service = MinutesService(db)
    minutes = service.get_minutes_by_meeting(meeting_id)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.put("/{minutes_id}", response_model=MinutesOut)
def update_minutes(
    minutes_id: int,
    update_data: MinutesUpdate,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    minutes = service.update_minutes(minutes_id, update_data)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.post("/{minutes_id}/approve", response_model=MinutesOut)
def approve_minutes(
    minutes_id: int,
    approval_data: MinutesApprovalIn,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    minutes = service.approve_minutes(minutes_id, approval_data)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.post("/{minutes_id}/reject", response_model=MinutesOut)
def reject_minutes(
    minutes_id: int,
    rejection_data: MinutesRejectionIn,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    minutes = service.reject_minutes(minutes_id, rejection_data)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.post("/{minutes_id}/publish", response_model=MinutesOut)
def publish_minutes(
    minutes_id: int,
    published_by: str,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    minutes = service.publish_minutes(minutes_id, published_by)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.delete("/{minutes_id}")
def delete_minutes(minutes_id: int, db: Session = Depends(get_db)):
    service = MinutesService(db)
    success = service.delete_minutes(minutes_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return {"message": "Ata excluída com sucesso"}


@router.get("/{minutes_id}/history")
def get_minutes_history(minutes_id: int, db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_minutes_history(minutes_id)


@router.post("/{minutes_id}/history", response_model=dict)
def add_minutes_history(
    minutes_id: int,
    history_data: MinutesHistoryIn,
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    history_data.minutes_id = minutes_id
    return service.add_minutes_history(history_data)


@router.post("/{minutes_id}/approval-request")
def send_approval_request(
    minutes_id: int,
    approver_emails: List[str],
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    success = service.send_approval_request(minutes_id, approver_emails)
    if not success:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return {"message": "Solicitação de aprovação enviada com sucesso"}


@router.post("/{minutes_id}/notify")
def send_minutes_notification(
    minutes_id: int,
    recipient_emails: List[str],
    db: Session = Depends(get_db)
):
    service = MinutesService(db)
    success = service.send_minutes_notification(minutes_id, recipient_emails)
    if not success:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return {"message": "Notificação enviada com sucesso"}


@router.get("/draft/list")
def get_draft_minutes(db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_draft_minutes()


@router.get("/pending/list")
def get_pending_approval_minutes(db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_pending_approval_minutes()


@router.get("/approved/list")
def get_approved_minutes(db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_approved_minutes()


@router.get("/published/list")
def get_published_minutes(db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_published_minutes()


@router.get("/rejected/list")
def get_rejected_minutes(db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_rejected_minutes()


@router.get("/creator/{created_by}")
def get_minutes_by_creator(created_by: str, db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_minutes_by_creator(created_by)


@router.get("/unit/{unit_id}")
def get_minutes_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = MinutesService(db)
    return service.get_minutes_by_unit(unit_id)


@router.get("/stats/summary")
def get_minutes_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = MinutesService(db)
    return service.get_minutes_stats(start, end)


