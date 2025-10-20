from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Optional, Dict, Any
from ..models.audit import AuditLog, AuditReport
from ..schemas.audit import AuditLogIn, AuditLogSearchIn, AuditStatsIn, AuditReportIn
from datetime import datetime, timedelta
import uuid


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_audit_log(self, log_data: AuditLogIn) -> AuditLog:
        db_log = AuditLog(
            user_id=log_data.user_id,
            user_email=log_data.user_email,
            action=log_data.action,
            resource_type=log_data.resource_type,
            resource_id=log_data.resource_id,
            resource_name=log_data.resource_name,
            description=log_data.description,
            ip_address=log_data.ip_address,
            user_agent=log_data.user_agent,
            session_id=log_data.session_id,
            tenant_id=log_data.tenant_id,
            unit_id=log_data.unit_id,
            old_values=log_data.old_values,
            new_values=log_data.new_values,
            metadata=log_data.metadata,
            log_level=log_data.log_level
        )
        
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def get_audit_log(self, log_id: int) -> Optional[AuditLog]:
        return self.db.query(AuditLog).filter(AuditLog.id == log_id).first()

    def search_audit_logs(self, search_data: AuditLogSearchIn, limit: int = 100, offset: int = 0) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        
        if search_data.user_id:
            query = query.filter(AuditLog.user_id == search_data.user_id)
        if search_data.user_email:
            query = query.filter(AuditLog.user_email.ilike(f"%{search_data.user_email}%"))
        if search_data.action:
            query = query.filter(AuditLog.action == search_data.action)
        if search_data.resource_type:
            query = query.filter(AuditLog.resource_type == search_data.resource_type)
        if search_data.resource_id:
            query = query.filter(AuditLog.resource_id == search_data.resource_id)
        if search_data.tenant_id:
            query = query.filter(AuditLog.tenant_id == search_data.tenant_id)
        if search_data.unit_id:
            query = query.filter(AuditLog.unit_id == search_data.unit_id)
        if search_data.log_level:
            query = query.filter(AuditLog.log_level == search_data.log_level)
        if search_data.start_date:
            query = query.filter(AuditLog.created_at >= search_data.start_date)
        if search_data.end_date:
            query = query.filter(AuditLog.created_at <= search_data.end_date)
        if search_data.ip_address:
            query = query.filter(AuditLog.ip_address == search_data.ip_address)
        if search_data.session_id:
            query = query.filter(AuditLog.session_id == search_data.session_id)
        
        return query.order_by(desc(AuditLog.created_at)).offset(offset).limit(limit).all()

    def get_audit_logs_by_user(self, user_id: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_resource(self, resource_type: str, resource_id: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            and_(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id
            )
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_tenant(self, tenant_id: int, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.tenant_id == tenant_id
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_unit(self, unit_id: int, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.unit_id == unit_id
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_action(self, action: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.action == action
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_date_range(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            and_(
                AuditLog.created_at >= start_date,
                AuditLog.created_at <= end_date
            )
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_ip(self, ip_address: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.ip_address == ip_address
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_session(self, session_id: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.session_id == session_id
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_logs_by_log_level(self, log_level: str, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).filter(
            AuditLog.log_level == log_level
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()

    def get_audit_stats(self, stats_data: AuditStatsIn) -> Dict[str, Any]:
        query = self.db.query(AuditLog).filter(
            and_(
                AuditLog.created_at >= stats_data.start_date,
                AuditLog.created_at <= stats_data.end_date
            )
        )
        
        if stats_data.tenant_id:
            query = query.filter(AuditLog.tenant_id == stats_data.tenant_id)
        if stats_data.unit_id:
            query = query.filter(AuditLog.unit_id == stats_data.unit_id)
        
        # Total logs
        total_logs = query.count()
        
        # Unique users
        unique_users = query.with_entities(AuditLog.user_id).distinct().count()
        
        # Action breakdown
        action_breakdown = {}
        action_counts = query.with_entities(
            AuditLog.action, 
            func.count(AuditLog.id)
        ).group_by(AuditLog.action).all()
        
        for action, count in action_counts:
            action_breakdown[action] = count
        
        # Resource breakdown
        resource_breakdown = {}
        resource_counts = query.with_entities(
            AuditLog.resource_type, 
            func.count(AuditLog.id)
        ).group_by(AuditLog.resource_type).all()
        
        for resource_type, count in resource_counts:
            resource_breakdown[resource_type] = count
        
        # User breakdown
        user_breakdown = {}
        user_counts = query.with_entities(
            AuditLog.user_email, 
            func.count(AuditLog.id)
        ).group_by(AuditLog.user_email).all()
        
        for user_email, count in user_counts:
            user_breakdown[user_email] = count
        
        # Daily breakdown
        daily_breakdown = {}
        daily_counts = query.with_entities(
            func.date(AuditLog.created_at), 
            func.count(AuditLog.id)
        ).group_by(func.date(AuditLog.created_at)).all()
        
        for date, count in daily_counts:
            daily_breakdown[str(date)] = count
        
        # Error and warning counts
        error_count = query.filter(AuditLog.log_level == "error").count()
        warning_count = query.filter(AuditLog.log_level == "warning").count()
        
        # Most active user
        most_active_user = None
        if user_counts:
            most_active_user = max(user_counts, key=lambda x: x[1])[0]
        
        # Most common action
        most_common_action = None
        if action_counts:
            most_common_action = max(action_counts, key=lambda x: x[1])[0]
        
        # Most common resource
        most_common_resource = None
        if resource_counts:
            most_common_resource = max(resource_counts, key=lambda x: x[1])[0]
        
        return {
            "total_logs": total_logs,
            "unique_users": unique_users,
            "action_breakdown": action_breakdown,
            "resource_breakdown": resource_breakdown,
            "user_breakdown": user_breakdown,
            "daily_breakdown": daily_breakdown,
            "error_count": error_count,
            "warning_count": warning_count,
            "most_active_user": most_active_user,
            "most_common_action": most_common_action,
            "most_common_resource": most_common_resource
        }

    def create_audit_report(self, report_data: AuditReportIn, user_id: str) -> AuditReport:
        report_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=7)  # Reports expire in 7 days
        
        db_report = AuditReport(
            report_id=report_id,
            user_id=user_id,
            format=report_data.format,
            filters=report_data.dict(),
            expires_at=expires_at
        )
        
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def get_audit_report(self, report_id: str) -> Optional[AuditReport]:
        return self.db.query(AuditReport).filter(AuditReport.report_id == report_id).first()

    def update_audit_report(self, report_id: str, file_path: str = None, download_url: str = None, status: str = "completed") -> Optional[AuditReport]:
        db_report = self.get_audit_report(report_id)
        if not db_report:
            return None
        
        if file_path:
            db_report.file_path = file_path
        if download_url:
            db_report.download_url = download_url
        db_report.status = status
        
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def get_user_audit_reports(self, user_id: str) -> List[AuditReport]:
        return self.db.query(AuditReport).filter(
            AuditReport.user_id == user_id
        ).order_by(desc(AuditReport.created_at)).all()

    def delete_expired_reports(self) -> int:
        expired_reports = self.db.query(AuditReport).filter(
            AuditReport.expires_at < datetime.utcnow()
        ).all()
        
        count = len(expired_reports)
        for report in expired_reports:
            self.db.delete(report)
        
        self.db.commit()
        return count

    def get_recent_audit_logs(self, limit: int = 50) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(
            desc(AuditLog.created_at)
        ).limit(limit).all()

    def get_audit_logs_by_filters(self, filters: Dict[str, Any], limit: int = 100) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        
        for key, value in filters.items():
            if hasattr(AuditLog, key) and value is not None:
                if isinstance(value, str):
                    query = query.filter(getattr(AuditLog, key).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(AuditLog, key) == value)
        
        return query.order_by(desc(AuditLog.created_at)).limit(limit).all()

