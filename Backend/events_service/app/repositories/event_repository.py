from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.events import Event, EventHistory
from ..schemas.events import EventIn, EventUpdate, EventHistoryIn
from datetime import datetime, timedelta


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event_data: EventIn) -> Event:
        db_event = Event(
            title=event_data.title,
            description=event_data.description,
            event_type=event_data.event_type,
            priority=event_data.priority,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            location=event_data.location,
            organizer=event_data.organizer,
            attendees=event_data.attendees,
            is_recurring=event_data.is_recurring,
            recurrence_pattern=event_data.recurrence_pattern,
            reminder_days=event_data.reminder_days,
            unit_id=event_data.unit_id,
            created_by=event_data.organizer
        )
        
        self.db.add(db_event)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = EventHistory(
            event_id=db_event.id,
            action="created",
            description="Evento criado",
            changed_by=event_data.organizer
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_event(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def list_events(self, 
                   event_type: Optional[str] = None, 
                   priority: Optional[str] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Event]:
        query = self.db.query(Event)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
        if priority:
            query = query.filter(Event.priority == priority)
        if start_date:
            query = query.filter(Event.start_date >= start_date)
        if end_date:
            query = query.filter(Event.end_date <= end_date)
            
        return query.order_by(Event.start_date.asc()).all()

    def get_upcoming_events(self, days_ahead: int = 30) -> List[Event]:
        today = datetime.utcnow()
        future_date = today + timedelta(days=days_ahead)
        
        return self.db.query(Event).filter(
            Event.start_date >= today,
            Event.start_date <= future_date
        ).order_by(Event.start_date.asc()).all()

    def get_events_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Event]:
        return self.db.query(Event).filter(
            Event.start_date >= start_date,
            Event.end_date <= end_date
        ).order_by(Event.start_date.asc()).all()

    def update_event(self, event_id: int, update_data: EventUpdate) -> Optional[Event]:
        db_event = self.get_event(event_id)
        if not db_event:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_event, field, value)
        
        db_event.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = EventHistory(
            event_id=event_id,
            action="updated",
            description=f"Evento atualizado: {', '.join(update_dict.keys())}",
            changed_by=update_data.organizer or "Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def delete_event(self, event_id: int) -> bool:
        db_event = self.get_event(event_id)
        if not db_event:
            return False
        
        self.db.delete(db_event)
        self.db.commit()
        return True

    def get_event_history(self, event_id: int) -> List[EventHistory]:
        return self.db.query(EventHistory).filter(
            EventHistory.event_id == event_id
        ).order_by(EventHistory.created_at.desc()).all()

    def add_event_history(self, history_data: EventHistoryIn) -> EventHistory:
        db_history = EventHistory(
            event_id=history_data.event_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_events_by_organizer(self, organizer: str) -> List[Event]:
        return self.db.query(Event).filter(
            Event.organizer == organizer
        ).order_by(Event.start_date.desc()).all()

    def get_events_by_location(self, location: str) -> List[Event]:
        return self.db.query(Event).filter(
            Event.location.ilike(f"%{location}%")
        ).order_by(Event.start_date.desc()).all()

    def get_events_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Event).filter(
            Event.start_date >= start_date,
            Event.end_date <= end_date
        )
        
        total_events = query.count()
        
        type_breakdown = {}
        priority_breakdown = {}
        
        for event in query.all():
            type_breakdown[event.event_type] = type_breakdown.get(event.event_type, 0) + 1
            priority_breakdown[event.priority] = priority_breakdown.get(event.priority, 0) + 1
        
        return {
            "total_events": total_events,
            "type_breakdown": type_breakdown,
            "priority_breakdown": priority_breakdown
        }

    def get_events_requiring_reminder(self) -> List[Event]:
        today = datetime.utcnow()
        return self.db.query(Event).filter(
            Event.reminder_days.isnot(None),
            Event.start_date >= today,
            Event.start_date <= today + timedelta(days=Event.reminder_days)
        ).all()


