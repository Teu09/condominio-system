from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.events import EventIn, EventOut, EventUpdate, EventHistoryIn
from ..services.event_service import EventService
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventOut)
def create_event(event_data: EventIn, db: Session = Depends(get_db)):
    service = EventService(db)
    return service.create_event(event_data)


@router.get("/", response_model=List[EventOut])
def list_events(
    event_type: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    
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
    
    return service.list_events(event_type, priority, start_dt, end_dt)


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    service = EventService(db)
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return event


@router.put("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    update_data: EventUpdate,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    event = service.update_event(event_id, update_data)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return event


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    service = EventService(db)
    success = service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"message": "Evento excluído com sucesso"}


@router.get("/{event_id}/history")
def get_event_history(event_id: int, db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_event_history(event_id)


@router.post("/{event_id}/history", response_model=dict)
def add_event_history(
    event_id: int,
    history_data: EventHistoryIn,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    history_data.event_id = event_id
    return service.add_event_history(history_data)


@router.get("/upcoming/list")
def get_upcoming_events(days_ahead: int = 30, db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_upcoming_events(days_ahead)


@router.get("/today/list")
def get_today_events(db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_today_events()


@router.get("/week/list")
def get_this_week_events(db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_this_week_events()


@router.get("/month/list")
def get_this_month_events(db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_this_month_events()


@router.get("/organizer/{organizer}")
def get_events_by_organizer(organizer: str, db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_events_by_organizer(organizer)


@router.get("/location/{location}")
def get_events_by_location(location: str, db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_events_by_location(location)


@router.get("/stats/summary")
def get_events_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = EventService(db)
    return service.get_events_stats(start, end)


@router.get("/reminders/list")
def get_events_requiring_reminder(db: Session = Depends(get_db)):
    service = EventService(db)
    return service.get_events_requiring_reminder()


