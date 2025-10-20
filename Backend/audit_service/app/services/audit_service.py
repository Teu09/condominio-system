from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..repositories.audit_repository import AuditRepository
from ..schemas.audit import AuditLogIn, AuditLogOut, AuditLogSearchIn, AuditStatsIn, AuditStatsOut, AuditReportIn, AuditReportOut
from datetime import datetime, timedelta
import uuid


class AuditService:
    def __init__(self, db: Session):
        self.repository = AuditRepository(db)

    def log_action(self, log_data: AuditLogIn) -> AuditLogOut:
        audit_log = self.repository.create_audit_log(log_data)
        return AuditLogOut.from_orm(audit_log)

    def get_audit_log(self, log_id: int) -> Optional[AuditLogOut]:
        audit_log = self.repository.get_audit_log(log_id)
        if audit_log:
            return AuditLogOut.from_orm(audit_log)
        return None

    def search_audit_logs(self, search_data: AuditLogSearchIn, limit: int = 100, offset: int = 0) -> List[AuditLogOut]:
        audit_logs = self.repository.search_audit_logs(search_data, limit, offset)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_user(self, user_id: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_user(user_id, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_resource(self, resource_type: str, resource_id: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_resource(resource_type, resource_id, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_tenant(self, tenant_id: int, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_tenant(tenant_id, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_unit(self, unit_id: int, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_unit(unit_id, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_action(self, action: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_action(action, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_date_range(self, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_date_range(start_date, end_date, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_ip(self, ip_address: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_ip(ip_address, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_session(self, session_id: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_session(session_id, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_log_level(self, log_level: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_log_level(log_level, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_stats(self, stats_data: AuditStatsIn) -> AuditStatsOut:
        stats = self.repository.get_audit_stats(stats_data)
        return AuditStatsOut(**stats)

    def get_recent_audit_logs(self, limit: int = 50) -> List[AuditLogOut]:
        audit_logs = self.repository.get_recent_audit_logs(limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_filters(self, filters: Dict[str, Any], limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters(filters, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def create_audit_report(self, report_data: AuditReportIn, user_id: str) -> AuditReportOut:
        report = self.repository.create_audit_report(report_data, user_id)
        return AuditReportOut(
            report_id=report.report_id,
            format=report.format,
            file_path=report.file_path,
            download_url=report.download_url,
            created_at=report.created_at,
            expires_at=report.expires_at
        )

    def get_audit_report(self, report_id: str) -> Optional[AuditReportOut]:
        report = self.repository.get_audit_report(report_id)
        if report:
            return AuditReportOut(
                report_id=report.report_id,
                format=report.format,
                file_path=report.file_path,
                download_url=report.download_url,
                created_at=report.created_at,
                expires_at=report.expires_at
            )
        return None

    def update_audit_report(self, report_id: str, file_path: str = None, download_url: str = None, status: str = "completed") -> Optional[AuditReportOut]:
        report = self.repository.update_audit_report(report_id, file_path, download_url, status)
        if report:
            return AuditReportOut(
                report_id=report.report_id,
                format=report.format,
                file_path=report.file_path,
                download_url=report.download_url,
                created_at=report.created_at,
                expires_at=report.expires_at
            )
        return None

    def get_user_audit_reports(self, user_id: str) -> List[AuditReportOut]:
        reports = self.repository.get_user_audit_reports(user_id)
        return [
            AuditReportOut(
                report_id=report.report_id,
                format=report.format,
                file_path=report.file_path,
                download_url=report.download_url,
                created_at=report.created_at,
                expires_at=report.expires_at
            )
            for report in reports
        ]

    def delete_expired_reports(self) -> int:
        return self.repository.delete_expired_reports()

    def get_audit_logs_by_resource_type(self, resource_type: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({"resource_type": resource_type}, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_tenant_and_date(self, tenant_id: int, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "tenant_id": tenant_id,
            "created_at": start_date  # This would need to be handled differently in the repository
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_user_and_action(self, user_id: str, action: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "user_id": user_id,
            "action": action
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_ip_and_date(self, ip_address: str, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "ip_address": ip_address
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_session_and_date(self, session_id: str, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "session_id": session_id
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_log_level_and_date(self, log_level: str, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "log_level": log_level
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_tenant_and_user(self, tenant_id: int, user_id: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "tenant_id": tenant_id,
            "user_id": user_id
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_unit_and_user(self, unit_id: int, user_id: str, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "unit_id": unit_id,
            "user_id": user_id
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_action_and_date(self, action: str, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "action": action
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

    def get_audit_logs_by_resource_and_date(self, resource_type: str, resource_id: str, start_date: datetime, end_date: datetime, limit: int = 100) -> List[AuditLogOut]:
        audit_logs = self.repository.get_audit_logs_by_filters({
            "resource_type": resource_type,
            "resource_id": resource_id
        }, limit)
        return [AuditLogOut.from_orm(log) for log in audit_logs]

