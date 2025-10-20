from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from ..models.notifications import Notification, EmailTemplate, NotificationQueue, NotificationLog
from ..schemas.notifications import (
    NotificationIn, NotificationUpdate, NotificationSearchIn, 
    EmailTemplateIn, EmailTemplateUpdate, NotificationQueueIn
)
from datetime import datetime, timedelta


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, notification_data: NotificationIn) -> Notification:
        db_notification = Notification(
            recipient_email=notification_data.recipient_email,
            recipient_name=notification_data.recipient_name,
            subject=notification_data.subject,
            message=notification_data.message,
            notification_type=notification_data.notification_type,
            priority=notification_data.priority,
            template_type=notification_data.template_type,
            template_data=notification_data.template_data,
            scheduled_at=notification_data.scheduled_at,
            expires_at=notification_data.expires_at,
            tenant_id=notification_data.tenant_id,
            unit_id=notification_data.unit_id,
            user_id=notification_data.user_id,
            related_entity_type=notification_data.related_entity_type,
            related_entity_id=notification_data.related_entity_id,
            attachments=notification_data.attachments,
            created_by=notification_data.created_by
        )
        
        self.db.add(db_notification)
        self.db.flush()  # Get the ID
        
        # Create queue entry
        queue_entry = NotificationQueue(
            notification_id=db_notification.id,
            priority=notification_data.priority
        )
        self.db.add(queue_entry)
        
        # Create log entry
        log_entry = NotificationLog(
            notification_id=db_notification.id,
            action="created",
            description="Notificação criada"
        )
        self.db.add(log_entry)
        
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def get_notification(self, notification_id: int) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def list_notifications(self, 
                          status: Optional[str] = None,
                          notification_type: Optional[str] = None,
                          priority: Optional[str] = None,
                          template_type: Optional[str] = None,
                          tenant_id: Optional[int] = None,
                          unit_id: Optional[int] = None,
                          user_id: Optional[str] = None) -> List[Notification]:
        query = self.db.query(Notification)
        
        if status:
            query = query.filter(Notification.status == status)
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        if priority:
            query = query.filter(Notification.priority == priority)
        if template_type:
            query = query.filter(Notification.template_type == template_type)
        if tenant_id:
            query = query.filter(Notification.tenant_id == tenant_id)
        if unit_id:
            query = query.filter(Notification.unit_id == unit_id)
        if user_id:
            query = query.filter(Notification.user_id == user_id)
            
        return query.order_by(desc(Notification.created_at)).all()

    def search_notifications(self, search_data: NotificationSearchIn) -> List[Notification]:
        query = self.db.query(Notification)
        
        if search_data.recipient_email:
            query = query.filter(Notification.recipient_email.ilike(f"%{search_data.recipient_email}%"))
        if search_data.notification_type:
            query = query.filter(Notification.notification_type == search_data.notification_type)
        if search_data.status:
            query = query.filter(Notification.status == search_data.status)
        if search_data.priority:
            query = query.filter(Notification.priority == search_data.priority)
        if search_data.template_type:
            query = query.filter(Notification.template_type == search_data.template_type)
        if search_data.tenant_id:
            query = query.filter(Notification.tenant_id == search_data.tenant_id)
        if search_data.unit_id:
            query = query.filter(Notification.unit_id == search_data.unit_id)
        if search_data.user_id:
            query = query.filter(Notification.user_id == search_data.user_id)
        if search_data.related_entity_type:
            query = query.filter(Notification.related_entity_type == search_data.related_entity_type)
        if search_data.related_entity_id:
            query = query.filter(Notification.related_entity_id == search_data.related_entity_id)
        if search_data.start_date:
            query = query.filter(Notification.created_at >= search_data.start_date)
        if search_data.end_date:
            query = query.filter(Notification.created_at <= search_data.end_date)
            
        return query.order_by(desc(Notification.created_at)).all()

    def update_notification(self, notification_id: int, update_data: NotificationUpdate) -> Optional[Notification]:
        db_notification = self.get_notification(notification_id)
        if not db_notification:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_notification, field, value)
        
        db_notification.updated_at = datetime.utcnow()
        
        # Create log entry
        log_entry = NotificationLog(
            notification_id=notification_id,
            action="updated",
            description=f"Notificação atualizada: {', '.join(update_dict.keys())}",
            details=update_dict
        )
        self.db.add(log_entry)
        
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def delete_notification(self, notification_id: int) -> bool:
        db_notification = self.get_notification(notification_id)
        if not db_notification:
            return False
        
        self.db.delete(db_notification)
        self.db.commit()
        return True

    def get_pending_notifications(self, limit: int = 100) -> List[Notification]:
        return self.db.query(Notification).filter(
            Notification.status == "pending",
            or_(
                Notification.scheduled_at.is_(None),
                Notification.scheduled_at <= datetime.utcnow()
            )
        ).order_by(Notification.priority.desc(), Notification.created_at.asc()).limit(limit).all()

    def get_failed_notifications(self, limit: int = 100) -> List[Notification]:
        return self.db.query(Notification).filter(
            Notification.status == "failed"
        ).order_by(Notification.created_at.desc()).limit(limit).all()

    def get_expired_notifications(self) -> List[Notification]:
        return self.db.query(Notification).filter(
            Notification.expires_at < datetime.utcnow(),
            Notification.status == "pending"
        ).all()

    def get_notification_logs(self, notification_id: int) -> List[NotificationLog]:
        return self.db.query(NotificationLog).filter(
            NotificationLog.notification_id == notification_id
        ).order_by(desc(NotificationLog.created_at)).all()

    def add_notification_log(self, notification_id: int, action: str, description: str, details: Optional[Dict] = None) -> NotificationLog:
        log_entry = NotificationLog(
            notification_id=notification_id,
            action=action,
            description=description,
            details=details
        )
        
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        return log_entry

    def get_notification_stats(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        query = self.db.query(Notification).filter(
            and_(
                Notification.created_at >= start_date,
                Notification.created_at <= end_date
            )
        )
        
        total_notifications = query.count()
        
        status_counts = {}
        for status in ["pending", "sent", "delivered", "failed", "cancelled"]:
            status_counts[status] = query.filter(Notification.status == status).count()
        
        type_breakdown = {}
        type_counts = query.with_entities(
            Notification.notification_type, 
            func.count(Notification.id)
        ).group_by(Notification.notification_type).all()
        
        for notification_type, count in type_counts:
            type_breakdown[notification_type] = count
        
        priority_breakdown = {}
        priority_counts = query.with_entities(
            Notification.priority, 
            func.count(Notification.id)
        ).group_by(Notification.priority).all()
        
        for priority, count in priority_counts:
            priority_breakdown[priority] = count
        
        template_breakdown = {}
        template_counts = query.with_entities(
            Notification.template_type, 
            func.count(Notification.id)
        ).group_by(Notification.template_type).all()
        
        for template_type, count in template_counts:
            if template_type:
                template_breakdown[template_type] = count
        
        daily_breakdown = {}
        daily_counts = query.with_entities(
            func.date(Notification.created_at), 
            func.count(Notification.id)
        ).group_by(func.date(Notification.created_at)).all()
        
        for date, count in daily_counts:
            daily_breakdown[str(date)] = count
        
        success_rate = 0.0
        if total_notifications > 0:
            successful = status_counts["sent"] + status_counts["delivered"]
            success_rate = (successful / total_notifications) * 100
        
        return {
            "total_notifications": total_notifications,
            "sent_notifications": status_counts["sent"],
            "pending_notifications": status_counts["pending"],
            "failed_notifications": status_counts["failed"],
            "delivered_notifications": status_counts["delivered"],
            "cancelled_notifications": status_counts["cancelled"],
            "type_breakdown": type_breakdown,
            "priority_breakdown": priority_breakdown,
            "template_breakdown": template_breakdown,
            "daily_breakdown": daily_breakdown,
            "success_rate": success_rate
        }

    # Email Template methods
    def create_email_template(self, template_data: EmailTemplateIn) -> EmailTemplate:
        db_template = EmailTemplate(
            template_type=template_data.template_type,
            name=template_data.name,
            subject=template_data.subject,
            html_content=template_data.html_content,
            text_content=template_data.text_content,
            variables=template_data.variables,
            is_active=template_data.is_active,
            created_by=template_data.created_by
        )
        
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

    def get_email_template(self, template_id: int) -> Optional[EmailTemplate]:
        return self.db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()

    def get_email_template_by_type(self, template_type: str) -> Optional[EmailTemplate]:
        return self.db.query(EmailTemplate).filter(
            EmailTemplate.template_type == template_type,
            EmailTemplate.is_active == True
        ).first()

    def list_email_templates(self, is_active: Optional[bool] = None) -> List[EmailTemplate]:
        query = self.db.query(EmailTemplate)
        
        if is_active is not None:
            query = query.filter(EmailTemplate.is_active == is_active)
            
        return query.order_by(desc(EmailTemplate.created_at)).all()

    def update_email_template(self, template_id: int, update_data: EmailTemplateUpdate) -> Optional[EmailTemplate]:
        db_template = self.get_email_template(template_id)
        if not db_template:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_template, field, value)
        
        db_template.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

    def delete_email_template(self, template_id: int) -> bool:
        db_template = self.get_email_template(template_id)
        if not db_template:
            return False
        
        self.db.delete(db_template)
        self.db.commit()
        return True

    # Notification Queue methods
    def get_queue_entries(self, status: Optional[str] = None, limit: int = 100) -> List[NotificationQueue]:
        query = self.db.query(NotificationQueue)
        
        if status:
            query = query.filter(NotificationQueue.status == status)
            
        return query.order_by(
            NotificationQueue.priority.desc(),
            NotificationQueue.next_retry_at.asc()
        ).limit(limit).all()

    def update_queue_entry(self, queue_id: int, update_data: dict) -> Optional[NotificationQueue]:
        db_queue = self.db.query(NotificationQueue).filter(NotificationQueue.id == queue_id).first()
        if not db_queue:
            return None
        
        for field, value in update_data.items():
            setattr(db_queue, field, value)
        
        db_queue.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_queue)
        return db_queue

    def delete_queue_entry(self, queue_id: int) -> bool:
        db_queue = self.db.query(NotificationQueue).filter(NotificationQueue.id == queue_id).first()
        if not db_queue:
            return False
        
        self.db.delete(db_queue)
        self.db.commit()
        return True

    def get_retry_queue_entries(self, limit: int = 100) -> List[NotificationQueue]:
        return self.db.query(NotificationQueue).filter(
            and_(
                NotificationQueue.status == "failed",
                NotificationQueue.retry_count < NotificationQueue.max_retries,
                or_(
                    NotificationQueue.next_retry_at.is_(None),
                    NotificationQueue.next_retry_at <= datetime.utcnow()
                )
            )
        ).order_by(NotificationQueue.priority.desc()).limit(limit).all()

    def increment_retry_count(self, queue_id: int) -> Optional[NotificationQueue]:
        db_queue = self.db.query(NotificationQueue).filter(NotificationQueue.id == queue_id).first()
        if not db_queue:
            return None
        
        db_queue.retry_count += 1
        db_queue.next_retry_at = datetime.utcnow() + timedelta(minutes=5 * db_queue.retry_count)
        db_queue.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_queue)
        return db_queue

