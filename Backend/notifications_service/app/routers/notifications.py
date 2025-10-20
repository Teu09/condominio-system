from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.notifications import (
    NotificationIn, NotificationOut, NotificationUpdate, NotificationSearchIn, 
    EmailTemplateIn, EmailTemplateOut, EmailTemplateUpdate, 
    NotificationStatsOut, BulkNotificationIn, NotificationQueueOut
)
from ..services.notification_service import NotificationService
from datetime import datetime, timedelta

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationOut)
def create_notification(notification_data: NotificationIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.create_notification(notification_data, created_by)


@router.post("/bulk", response_model=dict)
def send_bulk_notifications(bulk_data: BulkNotificationIn, db: Session = Depends(get_db)):
    service = NotificationService(db)
    results = service.send_bulk_notifications(bulk_data)
    return {"results": results, "total": len(results), "successful": sum(1 for success in results.values() if success)}


@router.get("/", response_model=List[NotificationOut])
def list_notifications(
    status: Optional[str] = None,
    notification_type: Optional[str] = None,
    priority: Optional[str] = None,
    template_type: Optional[str] = None,
    tenant_id: Optional[int] = None,
    unit_id: Optional[int] = None,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    return service.list_notifications(
        status, notification_type, priority, template_type, tenant_id, unit_id, user_id
    )


@router.post("/search", response_model=List[NotificationOut])
def search_notifications(search_data: NotificationSearchIn, db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.search_notifications(search_data)


@router.get("/{notification_id}", response_model=NotificationOut)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    notification = service.get_notification(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notification


@router.put("/{notification_id}", response_model=NotificationOut)
def update_notification(
    notification_id: int,
    update_data: NotificationUpdate,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    notification = service.update_notification(notification_id, update_data)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notification


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    success = service.delete_notification(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return {"message": "Notificação excluída com sucesso"}


@router.post("/{notification_id}/send")
def send_notification(notification_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    success = service.send_notification(notification_id)
    if not success:
        raise HTTPException(status_code=400, detail="Falha ao enviar notificação")
    return {"message": "Notificação enviada com sucesso"}


@router.post("/{notification_id}/cancel")
def cancel_notification(notification_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    success = service.cancel_notification(notification_id)
    if not success:
        raise HTTPException(status_code=400, detail="Falha ao cancelar notificação")
    return {"message": "Notificação cancelada com sucesso"}


@router.post("/{notification_id}/schedule")
def schedule_notification(
    notification_id: int,
    scheduled_at: datetime,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    success = service.schedule_notification(notification_id, scheduled_at)
    if not success:
        raise HTTPException(status_code=400, detail="Falha ao agendar notificação")
    return {"message": "Notificação agendada com sucesso"}


@router.get("/{notification_id}/logs")
def get_notification_logs(notification_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.get_notification_logs(notification_id)


@router.get("/pending/list")
def get_pending_notifications(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.get_pending_notifications(limit)


@router.get("/failed/list")
def get_failed_notifications(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.get_failed_notifications(limit)


@router.get("/expired/list")
def get_expired_notifications(db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.get_expired_notifications()


@router.post("/process/pending")
def process_pending_notifications(
    limit: int = Query(100, ge=1, le=1000),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    if background_tasks:
        background_tasks.add_task(service.process_pending_notifications, limit)
        return {"message": "Processamento de notificações pendentes iniciado em background"}
    else:
        results = service.process_pending_notifications(limit)
        return results


@router.post("/process/failed")
def retry_failed_notifications(
    limit: int = Query(100, ge=1, le=1000),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    if background_tasks:
        background_tasks.add_task(service.retry_failed_notifications, limit)
        return {"message": "Tentativa de reenvio de notificações falhadas iniciada em background"}
    else:
        results = service.retry_failed_notifications(limit)
        return results


@router.post("/process/queue")
def process_notification_queue(
    limit: int = Query(100, ge=1, le=1000),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    if background_tasks:
        background_tasks.add_task(service.process_queue, limit)
        return {"message": "Processamento da fila de notificações iniciado em background"}
    else:
        results = service.process_queue(limit)
        return results


@router.post("/cleanup/expired")
def cleanup_expired_notifications(
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    if background_tasks:
        background_tasks.add_task(service.cleanup_expired_notifications)
        return {"message": "Limpeza de notificações expiradas iniciada em background"}
    else:
        count = service.cleanup_expired_notifications()
        return {"message": f"{count} notificações expiradas foram canceladas"}


@router.get("/stats/summary")
def get_notification_stats(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = NotificationService(db)
    return service.get_notification_stats(start, end)


@router.post("/template/send")
def send_template_notification(
    recipient_email: str,
    template_type: str,
    template_data: dict,
    priority: str = "medium",
    created_by: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    success = service.send_template_notification(
        recipient_email, template_type, template_data, priority, created_by
    )
    if not success:
        raise HTTPException(status_code=400, detail="Falha ao enviar notificação template")
    return {"message": "Notificação template enviada com sucesso"}


@router.get("/test/connection")
def test_email_connection(db: Session = Depends(get_db)):
    service = NotificationService(db)
    success = service.test_email_connection()
    if not success:
        raise HTTPException(status_code=400, detail="Falha na conexão de email")
    return {"message": "Conexão de email testada com sucesso"}


# Email Template endpoints
@router.post("/templates/", response_model=EmailTemplateOut)
def create_email_template(template_data: EmailTemplateIn, created_by: str = "Sistema", db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.create_email_template(template_data, created_by)


@router.get("/templates/", response_model=List[EmailTemplateOut])
def list_email_templates(is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    service = NotificationService(db)
    return service.list_email_templates(is_active)


@router.get("/templates/{template_id}", response_model=EmailTemplateOut)
def get_email_template(template_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    template = service.get_email_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template de email não encontrado")
    return template


@router.get("/templates/type/{template_type}", response_model=EmailTemplateOut)
def get_email_template_by_type(template_type: str, db: Session = Depends(get_db)):
    service = NotificationService(db)
    template = service.get_email_template_by_type(template_type)
    if not template:
        raise HTTPException(status_code=404, detail="Template de email não encontrado")
    return template


@router.put("/templates/{template_id}", response_model=EmailTemplateOut)
def update_email_template(
    template_id: int,
    update_data: EmailTemplateUpdate,
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    template = service.update_email_template(template_id, update_data)
    if not template:
        raise HTTPException(status_code=404, detail="Template de email não encontrado")
    return template


@router.delete("/templates/{template_id}")
def delete_email_template(template_id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    success = service.delete_email_template(template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template de email não encontrado")
    return {"message": "Template de email excluído com sucesso"}


# Queue endpoints
@router.get("/queue/", response_model=List[NotificationQueueOut])
def get_queue_entries(
    status: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    return service.get_queue_entries(status, limit)

