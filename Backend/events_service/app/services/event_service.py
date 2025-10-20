from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.event_repository import EventRepository
from ..schemas.events import EventIn, EventOut, EventUpdate, EventHistoryIn
from datetime import datetime, timedelta


class EventService:
    def __init__(self, db: Session):
        self.repository = EventRepository(db)

    def create_event(self, event_data: EventIn) -> EventOut:
        event = self.repository.create_event(event_data)
        return EventOut.from_orm(event)

    def get_event(self, event_id: int) -> Optional[EventOut]:
        event = self.repository.get_event(event_id)
        if event:
            return EventOut.from_orm(event)
        return None

    def list_events(self, 
                   event_type: Optional[str] = None, 
                   priority: Optional[str] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[EventOut]:
        events = self.repository.list_events(event_type, priority, start_date, end_date)
        return [EventOut.from_orm(event) for event in events]

    def get_upcoming_events(self, days_ahead: int = 30) -> List[EventOut]:
        events = self.repository.get_upcoming_events(days_ahead)
        return [EventOut.from_orm(event) for event in events]

    def get_events_by_date_range(self, start_date: datetime, end_date: datetime) -> List[EventOut]:
        events = self.repository.get_events_by_date_range(start_date, end_date)
        return [EventOut.from_orm(event) for event in events]

    def update_event(self, event_id: int, update_data: EventUpdate) -> Optional[EventOut]:
        event = self.repository.update_event(event_id, update_data)
        if event:
            return EventOut.from_orm(event)
        return None

    def delete_event(self, event_id: int) -> bool:
        return self.repository.delete_event(event_id)

    def get_event_history(self, event_id: int) -> List[dict]:
        history = self.repository.get_event_history(event_id)
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

    def add_event_history(self, history_data: EventHistoryIn) -> dict:
        history = self.repository.add_event_history(history_data)
        return {
            "id": history.id,
            "event_id": history.event_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "created_at": history.created_at
        }

    def get_events_by_organizer(self, organizer: str) -> List[EventOut]:
        events = self.repository.get_events_by_organizer(organizer)
        return [EventOut.from_orm(event) for event in events]

    def get_events_by_location(self, location: str) -> List[EventOut]:
        events = self.repository.get_events_by_location(location)
        return [EventOut.from_orm(event) for event in events]

    def get_events_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_events_stats(start_date, end_date)

    def get_events_requiring_reminder(self) -> List[EventOut]:
        events = self.repository.get_events_requiring_reminder()
        return [EventOut.from_orm(event) for event in events]

    def get_today_events(self) -> List[EventOut]:
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        events = self.repository.get_events_by_date_range(start_of_day, end_of_day)
        return [EventOut.from_orm(event) for event in events]

    def get_this_week_events(self) -> List[EventOut]:
        today = datetime.utcnow().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        start_datetime = datetime.combine(start_of_week, datetime.min.time())
        end_datetime = datetime.combine(end_of_week, datetime.max.time())
        
        events = self.repository.get_events_by_date_range(start_datetime, end_datetime)
        return [EventOut.from_orm(event) for event in events]

    def get_this_month_events(self) -> List[EventOut]:
        today = datetime.utcnow().date()
        start_of_month = today.replace(day=1)
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        start_datetime = datetime.combine(start_of_month, datetime.min.time())
        end_datetime = datetime.combine(end_of_month, datetime.max.time())
        
        events = self.repository.get_events_by_date_range(start_datetime, end_datetime)
        return [EventOut.from_orm(event) for event in events]


