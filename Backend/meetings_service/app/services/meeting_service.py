from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.meeting_repository import MeetingRepository
from ..schemas.meetings import MeetingIn, MeetingOut, MeetingUpdate, MeetingHistoryIn, MeetingInvitationIn, MeetingMinutesIn
from ..services.email_service import EmailService
from datetime import datetime, timedelta


class MeetingService:
    def __init__(self, db: Session):
        self.repository = MeetingRepository(db)
        self.email_service = EmailService()

    def create_meeting(self, meeting_data: MeetingIn) -> MeetingOut:
        meeting = self.repository.create_meeting(meeting_data)
        return MeetingOut.from_orm(meeting)

    def get_meeting(self, meeting_id: int) -> Optional[MeetingOut]:
        meeting = self.repository.get_meeting(meeting_id)
        if meeting:
            return MeetingOut.from_orm(meeting)
        return None

    def list_meetings(self, 
                     meeting_type: Optional[str] = None, 
                     status: Optional[str] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> List[MeetingOut]:
        meetings = self.repository.list_meetings(meeting_type, status, start_date, end_date)
        return [MeetingOut.from_orm(meeting) for meeting in meetings]

    def get_upcoming_meetings(self, days_ahead: int = 30) -> List[MeetingOut]:
        meetings = self.repository.get_upcoming_meetings(days_ahead)
        return [MeetingOut.from_orm(meeting) for meeting in meetings]

    def get_meetings_by_organizer(self, organizer: str) -> List[MeetingOut]:
        meetings = self.repository.get_meetings_by_organizer(organizer)
        return [MeetingOut.from_orm(meeting) for meeting in meetings]

    def update_meeting(self, meeting_id: int, update_data: MeetingUpdate) -> Optional[MeetingOut]:
        meeting = self.repository.update_meeting(meeting_id, update_data)
        if meeting:
            return MeetingOut.from_orm(meeting)
        return None

    def start_meeting(self, meeting_id: int, started_by: str) -> Optional[MeetingOut]:
        meeting = self.repository.start_meeting(meeting_id, started_by)
        if meeting:
            return MeetingOut.from_orm(meeting)
        return None

    def end_meeting(self, meeting_id: int, ended_by: str, actual_attendees: List[str] = None) -> Optional[MeetingOut]:
        meeting = self.repository.end_meeting(meeting_id, ended_by, actual_attendees)
        if meeting:
            return MeetingOut.from_orm(meeting)
        return None

    def cancel_meeting(self, meeting_id: int, cancelled_by: str, reason: str = None) -> Optional[MeetingOut]:
        meeting = self.repository.cancel_meeting(meeting_id, cancelled_by, reason)
        if meeting:
            return MeetingOut.from_orm(meeting)
        return None

    def delete_meeting(self, meeting_id: int) -> bool:
        return self.repository.delete_meeting(meeting_id)

    def get_meeting_history(self, meeting_id: int) -> List[dict]:
        history = self.repository.get_meeting_history(meeting_id)
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

    def add_meeting_history(self, history_data: MeetingHistoryIn) -> dict:
        history = self.repository.add_meeting_history(history_data)
        return {
            "id": history.id,
            "meeting_id": history.meeting_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "created_at": history.created_at
        }

    def send_invitations(self, meeting_id: int, attendee_emails: List[str]) -> bool:
        meeting = self.repository.get_meeting(meeting_id)
        if not meeting:
            return False
        
        # Create invitation records
        for email in attendee_emails:
            invitation_data = MeetingInvitationIn(
                meeting_id=meeting_id,
                email=email,
                name=email.split('@')[0],  # Use email prefix as name
                role="attendee"
            )
            self.repository.create_invitation(invitation_data)
        
        # Send email invitations
        meeting_data = {
            "title": meeting.title,
            "description": meeting.description,
            "scheduled_date": meeting.scheduled_date,
            "location": meeting.location,
            "organizer": meeting.organizer,
            "agenda_items": meeting.agenda_items
        }
        
        return self.email_service.send_meeting_invitation(meeting_data, attendee_emails)

    def send_reminders(self, meeting_id: int) -> bool:
        meeting = self.repository.get_meeting(meeting_id)
        if not meeting:
            return False
        
        # Get attendee emails from invitations
        invitations = self.repository.get_meeting_invitations(meeting_id)
        attendee_emails = [inv.email for inv in invitations]
        
        if not attendee_emails:
            return False
        
        meeting_data = {
            "title": meeting.title,
            "scheduled_date": meeting.scheduled_date,
            "location": meeting.location
        }
        
        return self.email_service.send_meeting_reminder(meeting_data, attendee_emails)

    def create_minutes(self, minutes_data: MeetingMinutesIn) -> dict:
        minutes = self.repository.create_minutes(minutes_data)
        return {
            "id": minutes.id,
            "meeting_id": minutes.meeting_id,
            "content": minutes.content,
            "decisions": minutes.decisions,
            "action_items": minutes.action_items,
            "next_meeting_date": minutes.next_meeting_date,
            "created_by": minutes.created_by,
            "created_at": minutes.created_at
        }

    def get_meeting_minutes(self, meeting_id: int) -> Optional[dict]:
        minutes = self.repository.get_meeting_minutes(meeting_id)
        if minutes:
            return {
                "id": minutes.id,
                "meeting_id": minutes.meeting_id,
                "content": minutes.content,
                "decisions": minutes.decisions,
                "action_items": minutes.action_items,
                "next_meeting_date": minutes.next_meeting_date,
                "created_by": minutes.created_by,
                "created_at": minutes.created_at
            }
        return None

    def send_minutes(self, meeting_id: int) -> bool:
        meeting = self.repository.get_meeting(meeting_id)
        minutes = self.repository.get_meeting_minutes(meeting_id)
        
        if not meeting or not minutes:
            return False
        
        # Get attendee emails from invitations
        invitations = self.repository.get_meeting_invitations(meeting_id)
        attendee_emails = [inv.email for inv in invitations]
        
        if not attendee_emails:
            return False
        
        meeting_data = {
            "title": meeting.title,
            "scheduled_date": meeting.scheduled_date,
            "location": meeting.location
        }
        
        minutes_data = {
            "content": minutes.content,
            "decisions": minutes.decisions,
            "action_items": minutes.action_items
        }
        
        return self.email_service.send_meeting_minutes(meeting_data, minutes_data, attendee_emails)

    def get_meetings_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_meetings_stats(start_date, end_date)

    def get_meetings_requiring_reminder(self) -> List[MeetingOut]:
        # Get meetings scheduled for tomorrow
        tomorrow = datetime.utcnow() + timedelta(days=1)
        start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        meetings = self.repository.list_meetings(
            start_date=start_of_day,
            end_date=end_of_day
        )
        
        return [MeetingOut.from_orm(meeting) for meeting in meetings]

    def get_today_meetings(self) -> List[MeetingOut]:
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        meetings = self.repository.list_meetings(
            start_date=start_of_day,
            end_date=end_of_day
        )
        
        return [MeetingOut.from_orm(meeting) for meeting in meetings]


