from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.minutes_repository import MinutesRepository
from ..schemas.minutes import MinutesIn, MinutesOut, MinutesUpdate, MinutesHistoryIn, MinutesApprovalIn, MinutesRejectionIn
from ..services.email_service import EmailService
from datetime import datetime


class MinutesService:
    def __init__(self, db: Session):
        self.repository = MinutesRepository(db)
        self.email_service = EmailService()

    def create_minutes(self, minutes_data: MinutesIn) -> MinutesOut:
        minutes = self.repository.create_minutes(minutes_data)
        return MinutesOut.from_orm(minutes)

    def get_minutes(self, minutes_id: int) -> Optional[MinutesOut]:
        minutes = self.repository.get_minutes(minutes_id)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def get_minutes_by_meeting(self, meeting_id: int) -> Optional[MinutesOut]:
        minutes = self.repository.get_minutes_by_meeting(meeting_id)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def list_minutes(self, 
                    status: Optional[str] = None,
                    unit_id: Optional[int] = None,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(status, unit_id, start_date, end_date)
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def update_minutes(self, minutes_id: int, update_data: MinutesUpdate) -> Optional[MinutesOut]:
        minutes = self.repository.update_minutes(minutes_id, update_data)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def approve_minutes(self, minutes_id: int, approval_data: MinutesApprovalIn) -> Optional[MinutesOut]:
        minutes = self.repository.approve_minutes(minutes_id, approval_data)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def reject_minutes(self, minutes_id: int, rejection_data: MinutesRejectionIn) -> Optional[MinutesOut]:
        minutes = self.repository.reject_minutes(minutes_id, rejection_data)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def publish_minutes(self, minutes_id: int, published_by: str) -> Optional[MinutesOut]:
        minutes = self.repository.publish_minutes(minutes_id, published_by)
        if minutes:
            return MinutesOut.from_orm(minutes)
        return None

    def delete_minutes(self, minutes_id: int) -> bool:
        return self.repository.delete_minutes(minutes_id)

    def get_minutes_history(self, minutes_id: int) -> List[dict]:
        history = self.repository.get_minutes_history(minutes_id)
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

    def add_minutes_history(self, history_data: MinutesHistoryIn) -> dict:
        history = self.repository.add_minutes_history(history_data)
        return {
            "id": history.id,
            "minutes_id": history.minutes_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "created_at": history.created_at
        }

    def get_minutes_by_creator(self, created_by: str) -> List[MinutesOut]:
        minutes = self.repository.get_minutes_by_creator(created_by)
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_pending_approval_minutes(self) -> List[MinutesOut]:
        minutes = self.repository.get_pending_approval_minutes()
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_published_minutes(self) -> List[MinutesOut]:
        minutes = self.repository.get_published_minutes()
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_minutes_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_minutes_stats(start_date, end_date)

    def send_approval_request(self, minutes_id: int, approver_emails: List[str]) -> bool:
        minutes = self.repository.get_minutes(minutes_id)
        if not minutes:
            return False
        
        # Update status to pending approval
        minutes.status = "pending_approval"
        minutes.updated_at = datetime.utcnow()
        self.repository.db.commit()
        
        # Prepare data for email
        minutes_data = {
            "title": minutes.title,
            "meeting_date": minutes.created_at,  # Using created_at as meeting date
            "created_by": minutes.created_by,
            "content": minutes.content
        }
        
        return self.email_service.send_minutes_approval_request(minutes_data, approver_emails)

    def send_minutes_notification(self, minutes_id: int, recipient_emails: List[str]) -> bool:
        minutes = self.repository.get_minutes(minutes_id)
        if not minutes:
            return False
        
        # Prepare data for email
        minutes_data = {
            "title": minutes.title,
            "meeting_date": minutes.created_at,  # Using created_at as meeting date
            "status": minutes.status,
            "content": minutes.content,
            "decisions": minutes.decisions,
            "action_items": minutes.action_items
        }
        
        return self.email_service.send_minutes_notification(minutes_data, recipient_emails)

    def send_rejection_notification(self, minutes_id: int, reason: str) -> bool:
        minutes = self.repository.get_minutes(minutes_id)
        if not minutes:
            return False
        
        # Prepare data for email
        minutes_data = {
            "title": minutes.title,
            "meeting_date": minutes.created_at,
            "created_by": minutes.created_by
        }
        
        return self.email_service.send_minutes_rejection_notification(minutes_data, minutes.created_by, reason)

    def get_draft_minutes(self) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(status="draft")
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_approved_minutes(self) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(status="approved")
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_rejected_minutes(self) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(status="rejected")
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_minutes_by_status(self, status: str) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(status=status)
        return [MinutesOut.from_orm(minutes) for minutes in minutes]

    def get_minutes_by_unit(self, unit_id: int) -> List[MinutesOut]:
        minutes = self.repository.list_minutes(unit_id=unit_id)
        return [MinutesOut.from_orm(minutes) for minutes in minutes]


