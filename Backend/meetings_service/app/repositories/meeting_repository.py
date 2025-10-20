from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.meetings import Meeting, MeetingHistory, MeetingInvitation, MeetingMinutes
from ..schemas.meetings import MeetingIn, MeetingUpdate, MeetingHistoryIn, MeetingInvitationIn, MeetingMinutesIn
from datetime import datetime, timedelta


class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_meeting(self, meeting_data: MeetingIn) -> Meeting:
        db_meeting = Meeting(
            title=meeting_data.title,
            description=meeting_data.description,
            meeting_type=meeting_data.meeting_type,
            scheduled_date=meeting_data.scheduled_date,
            location=meeting_data.location,
            organizer=meeting_data.organizer,
            attendees=meeting_data.attendees,
            agenda_items=meeting_data.agenda_items,
            is_public=meeting_data.is_public,
            requires_quorum=meeting_data.requires_quorum,
            quorum_percentage=meeting_data.quorum_percentage,
            unit_id=meeting_data.unit_id,
            created_by=meeting_data.organizer
        )
        
        self.db.add(db_meeting)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = MeetingHistory(
            meeting_id=db_meeting.id,
            action="created",
            description="Reunião criada",
            changed_by=meeting_data.organizer
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def get_meeting(self, meeting_id: int) -> Optional[Meeting]:
        return self.db.query(Meeting).filter(Meeting.id == meeting_id).first()

    def list_meetings(self, 
                     meeting_type: Optional[str] = None, 
                     status: Optional[str] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[Meeting]:
        query = self.db.query(Meeting)
        
        if meeting_type:
            query = query.filter(Meeting.meeting_type == meeting_type)
        if status:
            query = query.filter(Meeting.status == status)
        if start_date:
            query = query.filter(Meeting.scheduled_date >= start_date)
        if end_date:
            query = query.filter(Meeting.scheduled_date <= end_date)
            
        return query.order_by(Meeting.scheduled_date.asc()).all()

    def get_upcoming_meetings(self, days_ahead: int = 30) -> List[Meeting]:
        today = datetime.utcnow()
        future_date = today + timedelta(days=days_ahead)
        
        return self.db.query(Meeting).filter(
            Meeting.scheduled_date >= today,
            Meeting.scheduled_date <= future_date,
            Meeting.status.in_(["scheduled", "in_progress"])
        ).order_by(Meeting.scheduled_date.asc()).all()

    def get_meetings_by_organizer(self, organizer: str) -> List[Meeting]:
        return self.db.query(Meeting).filter(
            Meeting.organizer == organizer
        ).order_by(Meeting.scheduled_date.desc()).all()

    def update_meeting(self, meeting_id: int, update_data: MeetingUpdate) -> Optional[Meeting]:
        db_meeting = self.get_meeting(meeting_id)
        if not db_meeting:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_meeting, field, value)
        
        db_meeting.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MeetingHistory(
            meeting_id=meeting_id,
            action="updated",
            description=f"Reunião atualizada: {', '.join(update_dict.keys())}",
            changed_by=update_data.organizer or "Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def start_meeting(self, meeting_id: int, started_by: str) -> Optional[Meeting]:
        db_meeting = self.get_meeting(meeting_id)
        if not db_meeting:
            return None
        
        db_meeting.status = "in_progress"
        db_meeting.started_at = datetime.utcnow()
        db_meeting.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MeetingHistory(
            meeting_id=meeting_id,
            action="started",
            description="Reunião iniciada",
            changed_by=started_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def end_meeting(self, meeting_id: int, ended_by: str, actual_attendees: List[str] = None) -> Optional[Meeting]:
        db_meeting = self.get_meeting(meeting_id)
        if not db_meeting:
            return None
        
        db_meeting.status = "completed"
        db_meeting.ended_at = datetime.utcnow()
        db_meeting.updated_at = datetime.utcnow()
        
        if actual_attendees:
            db_meeting.actual_attendees = actual_attendees
        
        # Add history entry
        history_entry = MeetingHistory(
            meeting_id=meeting_id,
            action="ended",
            description="Reunião finalizada",
            changed_by=ended_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def cancel_meeting(self, meeting_id: int, cancelled_by: str, reason: str = None) -> Optional[Meeting]:
        db_meeting = self.get_meeting(meeting_id)
        if not db_meeting:
            return None
        
        db_meeting.status = "cancelled"
        db_meeting.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MeetingHistory(
            meeting_id=meeting_id,
            action="cancelled",
            description=f"Reunião cancelada{f': {reason}' if reason else ''}",
            changed_by=cancelled_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def delete_meeting(self, meeting_id: int) -> bool:
        db_meeting = self.get_meeting(meeting_id)
        if not db_meeting:
            return False
        
        self.db.delete(db_meeting)
        self.db.commit()
        return True

    def get_meeting_history(self, meeting_id: int) -> List[MeetingHistory]:
        return self.db.query(MeetingHistory).filter(
            MeetingHistory.meeting_id == meeting_id
        ).order_by(MeetingHistory.created_at.desc()).all()

    def add_meeting_history(self, history_data: MeetingHistoryIn) -> MeetingHistory:
        db_history = MeetingHistory(
            meeting_id=history_data.meeting_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def create_invitation(self, invitation_data: MeetingInvitationIn) -> MeetingInvitation:
        db_invitation = MeetingInvitation(
            meeting_id=invitation_data.meeting_id,
            email=invitation_data.email,
            name=invitation_data.name,
            role=invitation_data.role
        )
        
        self.db.add(db_invitation)
        self.db.commit()
        self.db.refresh(db_invitation)
        return db_invitation

    def get_meeting_invitations(self, meeting_id: int) -> List[MeetingInvitation]:
        return self.db.query(MeetingInvitation).filter(
            MeetingInvitation.meeting_id == meeting_id
        ).all()

    def create_minutes(self, minutes_data: MeetingMinutesIn) -> MeetingMinutes:
        db_minutes = MeetingMinutes(
            meeting_id=minutes_data.meeting_id,
            content=minutes_data.content,
            decisions=minutes_data.decisions,
            action_items=minutes_data.action_items,
            next_meeting_date=minutes_data.next_meeting_date,
            created_by=minutes_data.created_by
        )
        
        self.db.add(db_minutes)
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def get_meeting_minutes(self, meeting_id: int) -> Optional[MeetingMinutes]:
        return self.db.query(MeetingMinutes).filter(
            MeetingMinutes.meeting_id == meeting_id
        ).first()

    def get_meetings_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Meeting).filter(
            Meeting.scheduled_date >= start_date,
            Meeting.scheduled_date <= end_date
        )
        
        total_meetings = query.count()
        
        type_breakdown = {}
        status_breakdown = {}
        
        for meeting in query.all():
            type_breakdown[meeting.meeting_type] = type_breakdown.get(meeting.meeting_type, 0) + 1
            status_breakdown[meeting.status] = status_breakdown.get(meeting.status, 0) + 1
        
        return {
            "total_meetings": total_meetings,
            "type_breakdown": type_breakdown,
            "status_breakdown": status_breakdown
        }


