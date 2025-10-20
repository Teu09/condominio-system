from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.minutes import Minutes, MinutesHistory
from ..schemas.minutes import MinutesIn, MinutesUpdate, MinutesHistoryIn, MinutesApprovalIn, MinutesRejectionIn
from datetime import datetime


class MinutesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_minutes(self, minutes_data: MinutesIn) -> Minutes:
        db_minutes = Minutes(
            meeting_id=minutes_data.meeting_id,
            title=minutes_data.title,
            content=minutes_data.content,
            decisions=minutes_data.decisions,
            action_items=minutes_data.action_items,
            attendees=minutes_data.attendees,
            absentees=minutes_data.absentees,
            next_meeting_date=minutes_data.next_meeting_date,
            created_by=minutes_data.created_by,
            unit_id=minutes_data.unit_id
        )
        
        self.db.add(db_minutes)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = MinutesHistory(
            minutes_id=db_minutes.id,
            action="created",
            description="Ata criada",
            changed_by=minutes_data.created_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def get_minutes(self, minutes_id: int) -> Optional[Minutes]:
        return self.db.query(Minutes).filter(Minutes.id == minutes_id).first()

    def get_minutes_by_meeting(self, meeting_id: int) -> Optional[Minutes]:
        return self.db.query(Minutes).filter(Minutes.meeting_id == meeting_id).first()

    def list_minutes(self, 
                    status: Optional[str] = None,
                    unit_id: Optional[int] = None,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Minutes]:
        query = self.db.query(Minutes)
        
        if status:
            query = query.filter(Minutes.status == status)
        if unit_id:
            query = query.filter(Minutes.unit_id == unit_id)
        if start_date:
            query = query.filter(Minutes.created_at >= start_date)
        if end_date:
            query = query.filter(Minutes.created_at <= end_date)
            
        return query.order_by(Minutes.created_at.desc()).all()

    def update_minutes(self, minutes_id: int, update_data: MinutesUpdate) -> Optional[Minutes]:
        db_minutes = self.get_minutes(minutes_id)
        if not db_minutes:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_minutes, field, value)
        
        db_minutes.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MinutesHistory(
            minutes_id=minutes_id,
            action="updated",
            description=f"Ata atualizada: {', '.join(update_dict.keys())}",
            changed_by="Sistema"
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def approve_minutes(self, minutes_id: int, approval_data: MinutesApprovalIn) -> Optional[Minutes]:
        db_minutes = self.get_minutes(minutes_id)
        if not db_minutes:
            return None
        
        db_minutes.status = "approved"
        db_minutes.approved_by = approval_data.approved_by
        db_minutes.approved_at = datetime.utcnow()
        db_minutes.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MinutesHistory(
            minutes_id=minutes_id,
            action="approved",
            description=f"Ata aprovada{f' - {approval_data.comments}' if approval_data.comments else ''}",
            changed_by=approval_data.approved_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def reject_minutes(self, minutes_id: int, rejection_data: MinutesRejectionIn) -> Optional[Minutes]:
        db_minutes = self.get_minutes(minutes_id)
        if not db_minutes:
            return None
        
        db_minutes.status = "rejected"
        db_minutes.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MinutesHistory(
            minutes_id=minutes_id,
            action="rejected",
            description=f"Ata rejeitada: {rejection_data.reason}{f' - {rejection_data.comments}' if rejection_data.comments else ''}",
            changed_by=rejection_data.rejected_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def publish_minutes(self, minutes_id: int, published_by: str) -> Optional[Minutes]:
        db_minutes = self.get_minutes(minutes_id)
        if not db_minutes:
            return None
        
        db_minutes.status = "published"
        db_minutes.published_at = datetime.utcnow()
        db_minutes.updated_at = datetime.utcnow()
        
        # Add history entry
        history_entry = MinutesHistory(
            minutes_id=minutes_id,
            action="published",
            description="Ata publicada",
            changed_by=published_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_minutes)
        return db_minutes

    def delete_minutes(self, minutes_id: int) -> bool:
        db_minutes = self.get_minutes(minutes_id)
        if not db_minutes:
            return False
        
        self.db.delete(db_minutes)
        self.db.commit()
        return True

    def get_minutes_history(self, minutes_id: int) -> List[MinutesHistory]:
        return self.db.query(MinutesHistory).filter(
            MinutesHistory.minutes_id == minutes_id
        ).order_by(MinutesHistory.created_at.desc()).all()

    def add_minutes_history(self, history_data: MinutesHistoryIn) -> MinutesHistory:
        db_history = MinutesHistory(
            minutes_id=history_data.minutes_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_minutes_by_creator(self, created_by: str) -> List[Minutes]:
        return self.db.query(Minutes).filter(
            Minutes.created_by == created_by
        ).order_by(Minutes.created_at.desc()).all()

    def get_pending_approval_minutes(self) -> List[Minutes]:
        return self.db.query(Minutes).filter(
            Minutes.status == "pending_approval"
        ).order_by(Minutes.created_at.asc()).all()

    def get_published_minutes(self) -> List[Minutes]:
        return self.db.query(Minutes).filter(
            Minutes.status == "published"
        ).order_by(Minutes.created_at.desc()).all()

    def get_minutes_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Minutes).filter(
            Minutes.created_at >= start_date,
            Minutes.created_at <= end_date
        )
        
        total_minutes = query.count()
        
        status_breakdown = {}
        
        for minutes in query.all():
            status_breakdown[minutes.status] = status_breakdown.get(minutes.status, 0) + 1
        
        return {
            "total_minutes": total_minutes,
            "status_breakdown": status_breakdown
        }


