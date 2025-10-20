from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.notices import Notice, NoticeHistory, NoticeBoard, NoticeView
from ..schemas.notices import NoticeIn, NoticeUpdate, NoticeHistoryIn, NoticeBoardIn, NoticeBoardUpdate, NoticeViewIn
from datetime import datetime, timedelta


class NoticeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_notice(self, notice_data: NoticeIn) -> Notice:
        db_notice = Notice(
            title=notice_data.title,
            content=notice_data.content,
            notice_type=notice_data.notice_type,
            priority=notice_data.priority,
            is_public=notice_data.is_public,
            publish_date=notice_data.publish_date,
            expiry_date=notice_data.expiry_date,
            target_audience=notice_data.target_audience,
            tags=notice_data.tags,
            unit_id=notice_data.unit_id,
            created_by=notice_data.created_by
        )
        
        self.db.add(db_notice)
        self.db.flush()  # Get the ID
        
        # Create initial history entry
        history_entry = NoticeHistory(
            notice_id=db_notice.id,
            action="created",
            description="Aviso criado",
            changed_by=notice_data.created_by
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def get_notice(self, notice_id: int) -> Optional[Notice]:
        return self.db.query(Notice).filter(Notice.id == notice_id).first()

    def list_notices(self, 
                    notice_type: Optional[str] = None,
                    priority: Optional[str] = None,
                    status: Optional[str] = None,
                    is_public: Optional[bool] = None,
                    unit_id: Optional[int] = None,
                    is_pinned: Optional[bool] = None) -> List[Notice]:
        query = self.db.query(Notice)
        
        if notice_type:
            query = query.filter(Notice.notice_type == notice_type)
        if priority:
            query = query.filter(Notice.priority == priority)
        if status:
            query = query.filter(Notice.status == status)
        if is_public is not None:
            query = query.filter(Notice.is_public == is_public)
        if unit_id:
            query = query.filter(Notice.unit_id == unit_id)
        if is_pinned is not None:
            query = query.filter(Notice.is_pinned == is_pinned)
            
        return query.order_by(Notice.is_pinned.desc(), Notice.priority.desc(), Notice.created_at.desc()).all()

    def get_public_notices(self) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.is_public == True,
            Notice.status == "published",
            (Notice.expiry_date.is_(None)) | (Notice.expiry_date > datetime.utcnow())
        ).order_by(Notice.is_pinned.desc(), Notice.priority.desc(), Notice.created_at.desc()).all()

    def get_pinned_notices(self) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.is_pinned == True,
            Notice.status == "published",
            (Notice.expiry_date.is_(None)) | (Notice.expiry_date > datetime.utcnow())
        ).order_by(Notice.priority.desc(), Notice.created_at.desc()).all()

    def get_expired_notices(self) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.expiry_date < datetime.utcnow(),
            Notice.status == "published"
        ).order_by(Notice.expiry_date.desc()).all()

    def search_notices(self, search_term: str) -> List[Notice]:
        return self.db.query(Notice).filter(
            (Notice.title.ilike(f"%{search_term}%")) |
            (Notice.content.ilike(f"%{search_term}%")) |
            (Notice.tags.contains([search_term]))
        ).order_by(Notice.created_at.desc()).all()

    def update_notice(self, notice_id: int, update_data: NoticeUpdate) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        # Store old values for history
        old_values = {
            "title": db_notice.title,
            "content": db_notice.content,
            "notice_type": db_notice.notice_type,
            "priority": db_notice.priority,
            "status": db_notice.status,
            "is_public": db_notice.is_public
        }
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_notice, field, value)
        
        db_notice.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {
            "title": db_notice.title,
            "content": db_notice.content,
            "notice_type": db_notice.notice_type,
            "priority": db_notice.priority,
            "status": db_notice.status,
            "is_public": db_notice.is_public
        }
        
        # Add history entry
        history_entry = NoticeHistory(
            notice_id=notice_id,
            action="updated",
            description=f"Aviso atualizado: {', '.join(update_dict.keys())}",
            changed_by="Sistema",
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def publish_notice(self, notice_id: int, published_by: str) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        # Store old values for history
        old_values = {"status": db_notice.status, "publish_date": db_notice.publish_date}
        
        db_notice.status = "published"
        db_notice.publish_date = datetime.utcnow()
        db_notice.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_notice.status, "publish_date": db_notice.publish_date}
        
        # Add history entry
        history_entry = NoticeHistory(
            notice_id=notice_id,
            action="published",
            description="Aviso publicado",
            changed_by=published_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def archive_notice(self, notice_id: int, archived_by: str) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        # Store old values for history
        old_values = {"status": db_notice.status}
        
        db_notice.status = "archived"
        db_notice.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"status": db_notice.status}
        
        # Add history entry
        history_entry = NoticeHistory(
            notice_id=notice_id,
            action="archived",
            description="Aviso arquivado",
            changed_by=archived_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def pin_notice(self, notice_id: int, pinned_by: str) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        # Store old values for history
        old_values = {"is_pinned": db_notice.is_pinned}
        
        db_notice.is_pinned = True
        db_notice.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"is_pinned": db_notice.is_pinned}
        
        # Add history entry
        history_entry = NoticeHistory(
            notice_id=notice_id,
            action="pinned",
            description="Aviso fixado",
            changed_by=pinned_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def unpin_notice(self, notice_id: int, unpinned_by: str) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        # Store old values for history
        old_values = {"is_pinned": db_notice.is_pinned}
        
        db_notice.is_pinned = False
        db_notice.updated_at = datetime.utcnow()
        
        # Store new values for history
        new_values = {"is_pinned": db_notice.is_pinned}
        
        # Add history entry
        history_entry = NoticeHistory(
            notice_id=notice_id,
            action="unpinned",
            description="Aviso desfixado",
            changed_by=unpinned_by,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(history_entry)
        
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def increment_view_count(self, notice_id: int) -> Optional[Notice]:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return None
        
        db_notice.view_count += 1
        self.db.commit()
        self.db.refresh(db_notice)
        return db_notice

    def record_view(self, view_data: NoticeViewIn) -> NoticeView:
        db_view = NoticeView(
            notice_id=view_data.notice_id,
            viewer_id=view_data.viewer_id,
            viewer_ip=view_data.viewer_ip
        )
        
        self.db.add(db_view)
        self.db.commit()
        self.db.refresh(db_view)
        return db_view

    def delete_notice(self, notice_id: int) -> bool:
        db_notice = self.get_notice(notice_id)
        if not db_notice:
            return False
        
        self.db.delete(db_notice)
        self.db.commit()
        return True

    def get_notice_history(self, notice_id: int) -> List[NoticeHistory]:
        return self.db.query(NoticeHistory).filter(
            NoticeHistory.notice_id == notice_id
        ).order_by(NoticeHistory.created_at.desc()).all()

    def add_notice_history(self, history_data: NoticeHistoryIn) -> NoticeHistory:
        db_history = NoticeHistory(
            notice_id=history_data.notice_id,
            action=history_data.action,
            description=history_data.description,
            changed_by=history_data.changed_by,
            old_values=history_data.old_values,
            new_values=history_data.new_values
        )
        
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_notices_by_type(self, notice_type: str) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.notice_type == notice_type
        ).order_by(Notice.created_at.desc()).all()

    def get_notices_by_priority(self, priority: str) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.priority == priority
        ).order_by(Notice.created_at.desc()).all()

    def get_notices_by_creator(self, created_by: str) -> List[Notice]:
        return self.db.query(Notice).filter(
            Notice.created_by == created_by
        ).order_by(Notice.created_at.desc()).all()

    def get_notices_by_tags(self, tags: List[str]) -> List[Notice]:
        query = self.db.query(Notice)
        for tag in tags:
            query = query.filter(Notice.tags.contains([tag]))
        return query.order_by(Notice.created_at.desc()).all()

    def get_notices_stats(self, start_date: datetime, end_date: datetime) -> dict:
        query = self.db.query(Notice).filter(
            Notice.created_at >= start_date,
            Notice.created_at <= end_date
        )
        
        total_notices = query.count()
        
        type_breakdown = {}
        priority_breakdown = {}
        status_breakdown = {}
        
        for notice in query.all():
            type_breakdown[notice.notice_type] = type_breakdown.get(notice.notice_type, 0) + 1
            priority_breakdown[notice.priority] = priority_breakdown.get(notice.priority, 0) + 1
            status_breakdown[notice.status] = status_breakdown.get(notice.status, 0) + 1
        
        return {
            "total_notices": total_notices,
            "type_breakdown": type_breakdown,
            "priority_breakdown": priority_breakdown,
            "status_breakdown": status_breakdown
        }

    # Notice Board methods
    def create_notice_board(self, board_data: NoticeBoardIn) -> NoticeBoard:
        db_board = NoticeBoard(
            title=board_data.title,
            description=board_data.description,
            location=board_data.location,
            is_active=board_data.is_active,
            unit_id=board_data.unit_id,
            created_by="Sistema"  # This should be passed from the service
        )
        
        self.db.add(db_board)
        self.db.commit()
        self.db.refresh(db_board)
        return db_board

    def get_notice_board(self, board_id: int) -> Optional[NoticeBoard]:
        return self.db.query(NoticeBoard).filter(NoticeBoard.id == board_id).first()

    def list_notice_boards(self, is_active: Optional[bool] = None, unit_id: Optional[int] = None) -> List[NoticeBoard]:
        query = self.db.query(NoticeBoard)
        
        if is_active is not None:
            query = query.filter(NoticeBoard.is_active == is_active)
        if unit_id:
            query = query.filter(NoticeBoard.unit_id == unit_id)
            
        return query.order_by(NoticeBoard.created_at.desc()).all()

    def update_notice_board(self, board_id: int, update_data: NoticeBoardUpdate) -> Optional[NoticeBoard]:
        db_board = self.get_notice_board(board_id)
        if not db_board:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_board, field, value)
        
        db_board.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_board)
        return db_board

    def delete_notice_board(self, board_id: int) -> bool:
        db_board = self.get_notice_board(board_id)
        if not db_board:
            return False
        
        self.db.delete(db_board)
        self.db.commit()
        return True

