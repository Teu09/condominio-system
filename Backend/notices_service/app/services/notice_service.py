from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.notice_repository import NoticeRepository
from ..schemas.notices import NoticeIn, NoticeOut, NoticeUpdate, NoticeHistoryIn, NoticeBoardIn, NoticeBoardOut, NoticeBoardUpdate, NoticeViewIn
from datetime import datetime, timedelta


class NoticeService:
    def __init__(self, db: Session):
        self.repository = NoticeRepository(db)

    def create_notice(self, notice_data: NoticeIn, created_by: str = "Sistema") -> NoticeOut:
        notice = self.repository.create_notice(notice_data)
        return NoticeOut.from_orm(notice)

    def get_notice(self, notice_id: int) -> Optional[NoticeOut]:
        notice = self.repository.get_notice(notice_id)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def list_notices(self, 
                    notice_type: Optional[str] = None,
                    priority: Optional[str] = None,
                    status: Optional[str] = None,
                    is_public: Optional[bool] = None,
                    unit_id: Optional[int] = None,
                    is_pinned: Optional[bool] = None) -> List[NoticeOut]:
        notices = self.repository.list_notices(notice_type, priority, status, is_public, unit_id, is_pinned)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_public_notices(self) -> List[NoticeOut]:
        notices = self.repository.get_public_notices()
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_pinned_notices(self) -> List[NoticeOut]:
        notices = self.repository.get_pinned_notices()
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_expired_notices(self) -> List[NoticeOut]:
        notices = self.repository.get_expired_notices()
        return [NoticeOut.from_orm(notice) for notice in notices]

    def search_notices(self, search_term: str) -> List[NoticeOut]:
        notices = self.repository.search_notices(search_term)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def update_notice(self, notice_id: int, update_data: NoticeUpdate, changed_by: str = "Sistema") -> Optional[NoticeOut]:
        notice = self.repository.update_notice(notice_id, update_data)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def publish_notice(self, notice_id: int, published_by: str) -> Optional[NoticeOut]:
        notice = self.repository.publish_notice(notice_id, published_by)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def archive_notice(self, notice_id: int, archived_by: str) -> Optional[NoticeOut]:
        notice = self.repository.archive_notice(notice_id, archived_by)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def pin_notice(self, notice_id: int, pinned_by: str) -> Optional[NoticeOut]:
        notice = self.repository.pin_notice(notice_id, pinned_by)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def unpin_notice(self, notice_id: int, unpinned_by: str) -> Optional[NoticeOut]:
        notice = self.repository.unpin_notice(notice_id, unpinned_by)
        if notice:
            return NoticeOut.from_orm(notice)
        return None

    def view_notice(self, notice_id: int, viewer_id: Optional[str] = None, viewer_ip: Optional[str] = None) -> Optional[NoticeOut]:
        # Increment view count
        notice = self.repository.increment_view_count(notice_id)
        if not notice:
            return None
        
        # Record view
        view_data = NoticeViewIn(
            notice_id=notice_id,
            viewer_id=viewer_id,
            viewer_ip=viewer_ip
        )
        self.repository.record_view(view_data)
        
        return NoticeOut.from_orm(notice)

    def delete_notice(self, notice_id: int) -> bool:
        return self.repository.delete_notice(notice_id)

    def get_notice_history(self, notice_id: int) -> List[dict]:
        history = self.repository.get_notice_history(notice_id)
        return [
            {
                "id": entry.id,
                "action": entry.action,
                "description": entry.description,
                "changed_by": entry.changed_by,
                "old_values": entry.old_values,
                "new_values": entry.new_values,
                "created_at": entry.created_at
            }
            for entry in history
        ]

    def add_notice_history(self, history_data: NoticeHistoryIn) -> dict:
        history = self.repository.add_notice_history(history_data)
        return {
            "id": history.id,
            "notice_id": history.notice_id,
            "action": history.action,
            "description": history.description,
            "changed_by": history.changed_by,
            "old_values": history.old_values,
            "new_values": history.new_values,
            "created_at": history.created_at
        }

    def get_notices_by_type(self, notice_type: str) -> List[NoticeOut]:
        notices = self.repository.get_notices_by_type(notice_type)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_notices_by_priority(self, priority: str) -> List[NoticeOut]:
        notices = self.repository.get_notices_by_priority(priority)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_notices_by_creator(self, created_by: str) -> List[NoticeOut]:
        notices = self.repository.get_notices_by_creator(created_by)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_notices_by_tags(self, tags: List[str]) -> List[NoticeOut]:
        notices = self.repository.get_notices_by_tags(tags)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_notices_stats(self, start_date: datetime, end_date: datetime) -> dict:
        return self.repository.get_notices_stats(start_date, end_date)

    def get_notices_by_unit(self, unit_id: int) -> List[NoticeOut]:
        notices = self.repository.list_notices(unit_id=unit_id)
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_recent_notices(self, limit: int = 10) -> List[NoticeOut]:
        notices = self.repository.db.query(self.repository.Notice).order_by(
            self.repository.Notice.created_at.desc()
        ).limit(limit).all()
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_most_viewed_notices(self, limit: int = 10) -> List[NoticeOut]:
        notices = self.repository.db.query(self.repository.Notice).order_by(
            self.repository.Notice.view_count.desc()
        ).limit(limit).all()
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_notices_by_date_range(self, start_date: datetime, end_date: datetime) -> List[NoticeOut]:
        notices = self.repository.list_notices()
        filtered_notices = []
        
        for notice in notices:
            if start_date <= notice.created_at <= end_date:
                filtered_notices.append(notice)
        
        return [NoticeOut.from_orm(notice) for notice in filtered_notices]

    def get_urgent_notices(self) -> List[NoticeOut]:
        notices = self.repository.list_notices(priority="urgent", status="published")
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_emergency_notices(self) -> List[NoticeOut]:
        notices = self.repository.list_notices(notice_type="emergency", status="published")
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_maintenance_notices(self) -> List[NoticeOut]:
        notices = self.repository.list_notices(notice_type="maintenance", status="published")
        return [NoticeOut.from_orm(notice) for notice in notices]

    def get_social_notices(self) -> List[NoticeOut]:
        notices = self.repository.list_notices(notice_type="social", status="published")
        return [NoticeOut.from_orm(notice) for notice in notices]

    # Notice Board methods
    def create_notice_board(self, board_data: NoticeBoardIn, created_by: str = "Sistema") -> NoticeBoardOut:
        board = self.repository.create_notice_board(board_data)
        return NoticeBoardOut.from_orm(board)

    def get_notice_board(self, board_id: int) -> Optional[NoticeBoardOut]:
        board = self.repository.get_notice_board(board_id)
        if board:
            return NoticeBoardOut.from_orm(board)
        return None

    def list_notice_boards(self, is_active: Optional[bool] = None, unit_id: Optional[int] = None) -> List[NoticeBoardOut]:
        boards = self.repository.list_notice_boards(is_active, unit_id)
        return [NoticeBoardOut.from_orm(board) for board in boards]

    def update_notice_board(self, board_id: int, update_data: NoticeBoardUpdate) -> Optional[NoticeBoardOut]:
        board = self.repository.update_notice_board(board_id, update_data)
        if board:
            return NoticeBoardOut.from_orm(board)
        return None

    def delete_notice_board(self, board_id: int) -> bool:
        return self.repository.delete_notice_board(board_id)

    def get_active_notice_boards(self) -> List[NoticeBoardOut]:
        boards = self.repository.list_notice_boards(is_active=True)
        return [NoticeBoardOut.from_orm(board) for board in boards]

    def get_notice_boards_by_unit(self, unit_id: int) -> List[NoticeBoardOut]:
        boards = self.repository.list_notice_boards(unit_id=unit_id)
        return [NoticeBoardOut.from_orm(board) for board in boards]

