from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.notices import NoticeIn, NoticeOut, NoticeUpdate, NoticeHistoryIn, NoticeBoardIn, NoticeBoardOut, NoticeBoardUpdate, NoticeViewIn
from ..services.notice_service import NoticeService
from datetime import datetime

router = APIRouter(prefix="/notices", tags=["notices"])


@router.post("/", response_model=NoticeOut)
def create_notice(notice_data: NoticeIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.create_notice(notice_data, created_by)


@router.get("/", response_model=List[NoticeOut])
def list_notices(
    notice_type: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    is_public: Optional[bool] = None,
    unit_id: Optional[int] = None,
    is_pinned: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    return service.list_notices(notice_type, priority, status, is_public, unit_id, is_pinned)


@router.get("/public")
def get_public_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_public_notices()


@router.get("/pinned")
def get_pinned_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_pinned_notices()


@router.get("/expired")
def get_expired_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_expired_notices()


@router.get("/search/{search_term}")
def search_notices(search_term: str, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.search_notices(search_term)


@router.get("/{notice_id}", response_model=NoticeOut)
def get_notice(notice_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    notice = service.get_notice(notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.get("/{notice_id}/view")
def view_notice(
    notice_id: int,
    viewer_id: Optional[str] = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    
    # Get client IP
    viewer_ip = None
    if request:
        viewer_ip = request.client.host
    
    notice = service.view_notice(notice_id, viewer_id, viewer_ip)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.put("/{notice_id}", response_model=NoticeOut)
def update_notice(
    notice_id: int,
    update_data: NoticeUpdate,
    changed_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    notice = service.update_notice(notice_id, update_data, changed_by)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.post("/{notice_id}/publish", response_model=NoticeOut)
def publish_notice(
    notice_id: int,
    published_by: str,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    notice = service.publish_notice(notice_id, published_by)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.post("/{notice_id}/archive", response_model=NoticeOut)
def archive_notice(
    notice_id: int,
    archived_by: str,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    notice = service.archive_notice(notice_id, archived_by)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.post("/{notice_id}/pin", response_model=NoticeOut)
def pin_notice(
    notice_id: int,
    pinned_by: str,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    notice = service.pin_notice(notice_id, pinned_by)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.post("/{notice_id}/unpin", response_model=NoticeOut)
def unpin_notice(
    notice_id: int,
    unpinned_by: str,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    notice = service.unpin_notice(notice_id, unpinned_by)
    if not notice:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return notice


@router.delete("/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    success = service.delete_notice(notice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    return {"message": "Aviso excluído com sucesso"}


@router.get("/{notice_id}/history")
def get_notice_history(notice_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notice_history(notice_id)


@router.post("/{notice_id}/history", response_model=dict)
def add_notice_history(
    notice_id: int,
    history_data: NoticeHistoryIn,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    history_data.notice_id = notice_id
    return service.add_notice_history(history_data)


@router.get("/type/{notice_type}")
def get_notices_by_type(notice_type: str, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notices_by_type(notice_type)


@router.get("/priority/{priority}")
def get_notices_by_priority(priority: str, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notices_by_priority(priority)


@router.get("/creator/{created_by}")
def get_notices_by_creator(created_by: str, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notices_by_creator(created_by)


@router.get("/tags/{tags}")
def get_notices_by_tags(tags: str, db: Session = Depends(get_db)):
    service = NoticeService(db)
    tags_list = [tag.strip() for tag in tags.split(",")]
    return service.get_notices_by_tags(tags_list)


@router.get("/unit/{unit_id}")
def get_notices_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notices_by_unit(unit_id)


@router.get("/recent/list")
def get_recent_notices(limit: int = 10, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_recent_notices(limit)


@router.get("/most-viewed/list")
def get_most_viewed_notices(limit: int = 10, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_most_viewed_notices(limit)


@router.get("/urgent/list")
def get_urgent_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_urgent_notices()


@router.get("/emergency/list")
def get_emergency_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_emergency_notices()


@router.get("/maintenance/list")
def get_maintenance_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_maintenance_notices()


@router.get("/social/list")
def get_social_notices(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_social_notices()


@router.get("/stats/summary")
def get_notices_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = NoticeService(db)
    return service.get_notices_stats(start, end)


# Notice Board endpoints
@router.post("/boards/", response_model=NoticeBoardOut)
def create_notice_board(board_data: NoticeBoardIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.create_notice_board(board_data, created_by)


@router.get("/boards/", response_model=List[NoticeBoardOut])
def list_notice_boards(
    is_active: Optional[bool] = None,
    unit_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    return service.list_notice_boards(is_active, unit_id)


@router.get("/boards/{board_id}", response_model=NoticeBoardOut)
def get_notice_board(board_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    board = service.get_notice_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Quadro de avisos não encontrado")
    return board


@router.put("/boards/{board_id}", response_model=NoticeBoardOut)
def update_notice_board(
    board_id: int,
    update_data: NoticeBoardUpdate,
    db: Session = Depends(get_db)
):
    service = NoticeService(db)
    board = service.update_notice_board(board_id, update_data)
    if not board:
        raise HTTPException(status_code=404, detail="Quadro de avisos não encontrado")
    return board


@router.delete("/boards/{board_id}")
def delete_notice_board(board_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    success = service.delete_notice_board(board_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quadro de avisos não encontrado")
    return {"message": "Quadro de avisos excluído com sucesso"}


@router.get("/boards/active/list")
def get_active_notice_boards(db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_active_notice_boards()


@router.get("/boards/unit/{unit_id}")
def get_notice_boards_by_unit(unit_id: int, db: Session = Depends(get_db)):
    service = NoticeService(db)
    return service.get_notice_boards_by_unit(unit_id)

