from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.notification_repository import NotificationRepository
from ..services.email_service import EmailService
from ..schemas.notifications import (
    NotificationIn, NotificationOut, NotificationUpdate, NotificationSearchIn, 
    EmailTemplateIn, EmailTemplateOut, EmailTemplateUpdate, 
    NotificationStatsOut, BulkNotificationIn, NotificationQueueOut
)
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, db: Session):
        self.repository = NotificationRepository(db)
        self.email_service = EmailService()

    def create_notification(self, notification_data: NotificationIn, created_by: str = "Sistema") -> NotificationOut:
        notification = self.repository.create_notification(notification_data)
        return NotificationOut.from_orm(notification)

    def get_notification(self, notification_id: int) -> Optional[NotificationOut]:
        notification = self.repository.get_notification(notification_id)
        if notification:
            return NotificationOut.from_orm(notification)
        return None

    def list_notifications(self, 
                          status: Optional[str] = None,
                          notification_type: Optional[str] = None,
                          priority: Optional[str] = None,
                          template_type: Optional[str] = None,
                          tenant_id: Optional[int] = None,
                          unit_id: Optional[int] = None,
                          user_id: Optional[str] = None) -> List[NotificationOut]:
        notifications = self.repository.list_notifications(
            status, notification_type, priority, template_type, tenant_id, unit_id, user_id
        )
        return [NotificationOut.from_orm(notification) for notification in notifications]

    def search_notifications(self, search_data: NotificationSearchIn) -> List[NotificationOut]:
        notifications = self.repository.search_notifications(search_data)
        return [NotificationOut.from_orm(notification) for notification in notifications]

    def update_notification(self, notification_id: int, update_data: NotificationUpdate) -> Optional[NotificationOut]:
        notification = self.repository.update_notification(notification_id, update_data)
        if notification:
            return NotificationOut.from_orm(notification)
        return None

    def delete_notification(self, notification_id: int) -> bool:
        return self.repository.delete_notification(notification_id)

    def send_notification(self, notification_id: int) -> bool:
        """
        Send a single notification
        """
        notification = self.repository.get_notification(notification_id)
        if not notification:
            return False
        
        try:
            # Update status to sending
            self.repository.update_notification(notification_id, NotificationUpdate(status="sending"))
            
            # Send email
            success = self.email_service.send_email(
                to_email=notification.recipient_email,
                subject=notification.subject,
                html_content=notification.message,
                from_name=notification.recipient_name or "Sistema"
            )
            
            if success:
                # Update status to sent
                self.repository.update_notification(
                    notification_id, 
                    NotificationUpdate(
                        status="sent",
                        sent_at=datetime.utcnow()
                    )
                )
                self.repository.add_notification_log(
                    notification_id, 
                    "sent", 
                    "Notificação enviada com sucesso"
                )
                return True
            else:
                # Update status to failed
                self.repository.update_notification(
                    notification_id, 
                    NotificationUpdate(
                        status="failed",
                        failed_at=datetime.utcnow(),
                        failure_reason="Falha ao enviar email"
                    )
                )
                self.repository.add_notification_log(
                    notification_id, 
                    "failed", 
                    "Falha ao enviar notificação"
                )
                return False
                
        except Exception as e:
            logger.error(f"Error sending notification {notification_id}: {str(e)}")
            self.repository.update_notification(
                notification_id, 
                NotificationUpdate(
                    status="failed",
                    failed_at=datetime.utcnow(),
                    failure_reason=str(e)
                )
            )
            self.repository.add_notification_log(
                notification_id, 
                "failed", 
                f"Erro ao enviar notificação: {str(e)}"
            )
            return False

    def send_template_notification(self, 
                                  recipient_email: str, 
                                  template_type: str, 
                                  template_data: Dict[str, Any],
                                  priority: str = "medium",
                                  created_by: str = "Sistema") -> bool:
        """
        Send a notification using a template
        """
        try:
            # Get template
            template = self.repository.get_email_template_by_type(template_type)
            if not template:
                logger.error(f"Template {template_type} not found")
                return False
            
            # Replace variables in template
            subject = template.subject.format(**template_data)
            html_content = template.html_content.format(**template_data)
            text_content = template.text_content.format(**template_data) if template.text_content else None
            
            # Send email
            success = self.email_service.send_email(
                to_email=recipient_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
            if success:
                # Create notification record
                notification_data = NotificationIn(
                    recipient_email=recipient_email,
                    subject=subject,
                    message=html_content,
                    template_type=template_type,
                    template_data=template_data,
                    priority=priority,
                    created_by=created_by
                )
                self.repository.create_notification(notification_data)
                
            return success
            
        except Exception as e:
            logger.error(f"Error sending template notification: {str(e)}")
            return False

    def send_bulk_notifications(self, bulk_data: BulkNotificationIn) -> Dict[str, bool]:
        """
        Send bulk notifications
        """
        results = {}
        
        for i, email in enumerate(bulk_data.recipient_emails):
            try:
                # Create individual notification
                notification_data = NotificationIn(
                    recipient_email=email,
                    recipient_name=bulk_data.recipient_names[i] if bulk_data.recipient_names and i < len(bulk_data.recipient_names) else None,
                    subject=bulk_data.subject,
                    message=bulk_data.message,
                    notification_type=bulk_data.notification_type,
                    priority=bulk_data.priority,
                    template_type=bulk_data.template_type,
                    template_data=bulk_data.template_data,
                    scheduled_at=bulk_data.scheduled_at,
                    expires_at=bulk_data.expires_at,
                    tenant_id=bulk_data.tenant_id,
                    unit_id=bulk_data.unit_id,
                    user_id=bulk_data.user_id,
                    related_entity_type=bulk_data.related_entity_type,
                    related_entity_id=bulk_data.related_entity_id,
                    attachments=bulk_data.attachments,
                    created_by=bulk_data.created_by
                )
                
                notification = self.repository.create_notification(notification_data)
                success = self.send_notification(notification.id)
                results[email] = success
                
            except Exception as e:
                logger.error(f"Error creating bulk notification for {email}: {str(e)}")
                results[email] = False
        
        return results

    def process_pending_notifications(self, limit: int = 100) -> Dict[str, int]:
        """
        Process pending notifications
        """
        pending_notifications = self.repository.get_pending_notifications(limit)
        
        results = {
            "processed": 0,
            "sent": 0,
            "failed": 0
        }
        
        for notification in pending_notifications:
            results["processed"] += 1
            
            if self.send_notification(notification.id):
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results

    def retry_failed_notifications(self, limit: int = 100) -> Dict[str, int]:
        """
        Retry failed notifications
        """
        failed_notifications = self.repository.get_failed_notifications(limit)
        
        results = {
            "processed": 0,
            "sent": 0,
            "failed": 0
        }
        
        for notification in failed_notifications:
            results["processed"] += 1
            
            if self.send_notification(notification.id):
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results

    def get_notification_logs(self, notification_id: int) -> List[Dict[str, Any]]:
        logs = self.repository.get_notification_logs(notification_id)
        return [
            {
                "id": log.id,
                "action": log.action,
                "description": log.description,
                "details": log.details,
                "created_at": log.created_at
            }
            for log in logs
        ]

    def get_notification_stats(self, start_date: datetime, end_date: datetime) -> NotificationStatsOut:
        stats = self.repository.get_notification_stats(start_date, end_date)
        return NotificationStatsOut(**stats)

    def get_pending_notifications(self, limit: int = 100) -> List[NotificationOut]:
        notifications = self.repository.get_pending_notifications(limit)
        return [NotificationOut.from_orm(notification) for notification in notifications]

    def get_failed_notifications(self, limit: int = 100) -> List[NotificationOut]:
        notifications = self.repository.get_failed_notifications(limit)
        return [NotificationOut.from_orm(notification) for notification in notifications]

    def get_expired_notifications(self) -> List[NotificationOut]:
        notifications = self.repository.get_expired_notifications()
        return [NotificationOut.from_orm(notification) for notification in notifications]

    def cancel_notification(self, notification_id: int) -> bool:
        """
        Cancel a notification
        """
        notification = self.repository.get_notification(notification_id)
        if not notification or notification.status != "pending":
            return False
        
        success = self.repository.update_notification(
            notification_id, 
            NotificationUpdate(status="cancelled")
        )
        
        if success:
            self.repository.add_notification_log(
                notification_id, 
                "cancelled", 
                "Notificação cancelada"
            )
        
        return success is not None

    def schedule_notification(self, notification_id: int, scheduled_at: datetime) -> bool:
        """
        Schedule a notification for later sending
        """
        notification = self.repository.get_notification(notification_id)
        if not notification:
            return False
        
        success = self.repository.update_notification(
            notification_id, 
            NotificationUpdate(status="pending")
        )
        
        if success:
            self.repository.add_notification_log(
                notification_id, 
                "scheduled", 
                f"Notificação agendada para {scheduled_at}"
            )
        
        return success is not None

    # Email Template methods
    def create_email_template(self, template_data: EmailTemplateIn, created_by: str = "Sistema") -> EmailTemplateOut:
        template = self.repository.create_email_template(template_data)
        return EmailTemplateOut.from_orm(template)

    def get_email_template(self, template_id: int) -> Optional[EmailTemplateOut]:
        template = self.repository.get_email_template(template_id)
        if template:
            return EmailTemplateOut.from_orm(template)
        return None

    def get_email_template_by_type(self, template_type: str) -> Optional[EmailTemplateOut]:
        template = self.repository.get_email_template_by_type(template_type)
        if template:
            return EmailTemplateOut.from_orm(template)
        return None

    def list_email_templates(self, is_active: Optional[bool] = None) -> List[EmailTemplateOut]:
        templates = self.repository.list_email_templates(is_active)
        return [EmailTemplateOut.from_orm(template) for template in templates]

    def update_email_template(self, template_id: int, update_data: EmailTemplateUpdate) -> Optional[EmailTemplateOut]:
        template = self.repository.update_email_template(template_id, update_data)
        if template:
            return EmailTemplateOut.from_orm(template)
        return None

    def delete_email_template(self, template_id: int) -> bool:
        return self.repository.delete_email_template(template_id)

    def test_email_connection(self) -> bool:
        """
        Test email service connection
        """
        return self.email_service.test_connection()

    def get_queue_entries(self, status: Optional[str] = None, limit: int = 100) -> List[NotificationQueueOut]:
        queue_entries = self.repository.get_queue_entries(status, limit)
        return [NotificationQueueOut.from_orm(entry) for entry in queue_entries]

    def process_queue(self, limit: int = 100) -> Dict[str, int]:
        """
        Process notification queue
        """
        queue_entries = self.repository.get_queue_entries("pending", limit)
        
        results = {
            "processed": 0,
            "sent": 0,
            "failed": 0
        }
        
        for entry in queue_entries:
            results["processed"] += 1
            
            if self.send_notification(entry.notification_id):
                results["sent"] += 1
                # Update queue entry status
                self.repository.update_queue_entry(entry.id, {"status": "sent"})
            else:
                results["failed"] += 1
                # Increment retry count
                self.repository.increment_retry_count(entry.id)
        
        return results

    def cleanup_expired_notifications(self) -> int:
        """
        Clean up expired notifications
        """
        expired_notifications = self.repository.get_expired_notifications()
        count = 0
        
        for notification in expired_notifications:
            if self.repository.update_notification(
                notification.id, 
                NotificationUpdate(status="cancelled")
            ):
                count += 1
                self.repository.add_notification_log(
                    notification.id, 
                    "expired", 
                    "Notificação expirada e cancelada"
                )
        
        return count

