from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.meetings import MeetingIn, MeetingOut, MeetingUpdate, MeetingHistoryIn, MeetingInvitationIn, MeetingMinutesIn
from ..services.meeting_service import MeetingService
from datetime import datetime

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("/", response_model=MeetingOut)
def create_meeting(meeting_data: MeetingIn, db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.create_meeting(meeting_data)


@router.get("/", response_model=List[MeetingOut])
def list_meetings(
    meeting_type: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    
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
    
    return service.list_meetings(meeting_type, status, start_dt, end_dt)


@router.get("/{meeting_id}", response_model=MeetingOut)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    meeting = service.get_meeting(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return meeting


@router.put("/{meeting_id}", response_model=MeetingOut)
def update_meeting(
    meeting_id: int,
    update_data: MeetingUpdate,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    meeting = service.update_meeting(meeting_id, update_data)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return meeting


@router.post("/{meeting_id}/start", response_model=MeetingOut)
def start_meeting(meeting_id: int, started_by: str, db: Session = Depends(get_db)):
    service = MeetingService(db)
    meeting = service.start_meeting(meeting_id, started_by)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return meeting


@router.post("/{meeting_id}/end", response_model=MeetingOut)
def end_meeting(
    meeting_id: int, 
    ended_by: str, 
    actual_attendees: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    meeting = service.end_meeting(meeting_id, ended_by, actual_attendees)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return meeting


@router.post("/{meeting_id}/cancel")
def cancel_meeting(
    meeting_id: int, 
    cancelled_by: str, 
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    meeting = service.cancel_meeting(meeting_id, cancelled_by, reason)
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return {"message": "Reunião cancelada com sucesso"}


@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    success = service.delete_meeting(meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return {"message": "Reunião excluída com sucesso"}


@router.get("/{meeting_id}/history")
def get_meeting_history(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.get_meeting_history(meeting_id)


@router.post("/{meeting_id}/history", response_model=dict)
def add_meeting_history(
    meeting_id: int,
    history_data: MeetingHistoryIn,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    history_data.meeting_id = meeting_id
    return service.add_meeting_history(history_data)


@router.post("/{meeting_id}/invitations/send")
def send_invitations(
    meeting_id: int,
    attendee_emails: List[str],
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    success = service.send_invitations(meeting_id, attendee_emails)
    if not success:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return {"message": "Convites enviados com sucesso"}


@router.post("/{meeting_id}/reminders/send")
def send_reminders(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    success = service.send_reminders(meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reunião não encontrada")
    return {"message": "Lembretes enviados com sucesso"}


@router.post("/{meeting_id}/minutes", response_model=dict)
def create_minutes(
    meeting_id: int,
    minutes_data: MeetingMinutesIn,
    db: Session = Depends(get_db)
):
    service = MeetingService(db)
    minutes_data.meeting_id = meeting_id
    return service.create_minutes(minutes_data)


@router.get("/{meeting_id}/minutes")
def get_meeting_minutes(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    minutes = service.get_meeting_minutes(meeting_id)
    if not minutes:
        raise HTTPException(status_code=404, detail="Ata não encontrada")
    return minutes


@router.post("/{meeting_id}/minutes/send")
def send_minutes(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    success = service.send_minutes(meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reunião ou ata não encontrada")
    return {"message": "Ata enviada com sucesso"}


@router.get("/upcoming/list")
def get_upcoming_meetings(days_ahead: int = 30, db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.get_upcoming_meetings(days_ahead)


@router.get("/today/list")
def get_today_meetings(db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.get_today_meetings()


@router.get("/organizer/{organizer}")
def get_meetings_by_organizer(organizer: str, db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.get_meetings_by_organizer(organizer)


@router.get("/stats/summary")
def get_meetings_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = MeetingService(db)
    return service.get_meetings_stats(start, end)


@router.get("/reminders/list")
def get_meetings_requiring_reminder(db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.get_meetings_requiring_reminder()


