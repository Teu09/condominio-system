from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.db import get_db
from ..schemas.audit import AuditLogIn, AuditLogOut, AuditLogSearchIn, AuditStatsIn, AuditStatsOut, AuditReportIn, AuditReportOut
from ..services.audit_service import AuditService
from datetime import datetime, timedelta

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("/logs", response_model=AuditLogOut)
def create_audit_log(log_data: AuditLogIn, db: Session = Depends(get_db)):
    service = AuditService(db)
    return service.log_action(log_data)


@router.get("/logs/{log_id}", response_model=AuditLogOut)
def get_audit_log(log_id: int, db: Session = Depends(get_db)):
    service = AuditService(db)
    audit_log = service.get_audit_log(log_id)
    if not audit_log:
        raise HTTPException(status_code=404, detail="Log de auditoria não encontrado")
    return audit_log


@router.post("/logs/search", response_model=List[AuditLogOut])
def search_audit_logs(
    search_data: AuditLogSearchIn,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.search_audit_logs(search_data, limit, offset)


@router.get("/logs/user/{user_id}")
def get_audit_logs_by_user(
    user_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_user(user_id, limit)


@router.get("/logs/resource/{resource_type}/{resource_id}")
def get_audit_logs_by_resource(
    resource_type: str,
    resource_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_resource(resource_type, resource_id, limit)


@router.get("/logs/tenant/{tenant_id}")
def get_audit_logs_by_tenant(
    tenant_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_tenant(tenant_id, limit)


@router.get("/logs/unit/{unit_id}")
def get_audit_logs_by_unit(
    unit_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_unit(unit_id, limit)


@router.get("/logs/action/{action}")
def get_audit_logs_by_action(
    action: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_action(action, limit)


@router.get("/logs/date-range")
def get_audit_logs_by_date_range(
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_date_range(start, end, limit)


@router.get("/logs/ip/{ip_address}")
def get_audit_logs_by_ip(
    ip_address: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_ip(ip_address, limit)


@router.get("/logs/session/{session_id}")
def get_audit_logs_by_session(
    session_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_session(session_id, limit)


@router.get("/logs/level/{log_level}")
def get_audit_logs_by_log_level(
    log_level: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_log_level(log_level, limit)


@router.get("/logs/recent")
def get_recent_audit_logs(
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_recent_audit_logs(limit)


@router.get("/logs/resource-type/{resource_type}")
def get_audit_logs_by_resource_type(
    resource_type: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_resource_type(resource_type, limit)


@router.get("/logs/tenant/{tenant_id}/user/{user_id}")
def get_audit_logs_by_tenant_and_user(
    tenant_id: int,
    user_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_tenant_and_user(tenant_id, user_id, limit)


@router.get("/logs/unit/{unit_id}/user/{user_id}")
def get_audit_logs_by_unit_and_user(
    unit_id: int,
    user_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_unit_and_user(unit_id, user_id, limit)


@router.get("/logs/user/{user_id}/action/{action}")
def get_audit_logs_by_user_and_action(
    user_id: str,
    action: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.get_audit_logs_by_user_and_action(user_id, action, limit)


@router.get("/logs/action/{action}/date-range")
def get_audit_logs_by_action_and_date(
    action: str,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_action_and_date(action, start, end, limit)


@router.get("/logs/resource/{resource_type}/{resource_id}/date-range")
def get_audit_logs_by_resource_and_date(
    resource_type: str,
    resource_id: str,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_resource_and_date(resource_type, resource_id, start, end, limit)


@router.get("/logs/ip/{ip_address}/date-range")
def get_audit_logs_by_ip_and_date(
    ip_address: str,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_ip_and_date(ip_address, start, end, limit)


@router.get("/logs/session/{session_id}/date-range")
def get_audit_logs_by_session_and_date(
    session_id: str,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_session_and_date(session_id, start, end, limit)


@router.get("/logs/level/{log_level}/date-range")
def get_audit_logs_by_log_level_and_date(
    log_level: str,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_log_level_and_date(log_level, start, end, limit)


@router.get("/logs/tenant/{tenant_id}/date-range")
def get_audit_logs_by_tenant_and_date(
    tenant_id: int,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_tenant_and_date(tenant_id, start, end, limit)


@router.get("/logs/unit/{unit_id}/date-range")
def get_audit_logs_by_unit_and_date(
    unit_id: int,
    start_date: str,
    end_date: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    service = AuditService(db)
    return service.get_audit_logs_by_unit_and_date(unit_id, start, end, limit)


@router.post("/stats", response_model=AuditStatsOut)
def get_audit_stats(stats_data: AuditStatsIn, db: Session = Depends(get_db)):
    service = AuditService(db)
    return service.get_audit_stats(stats_data)


@router.get("/stats/summary")
def get_audit_stats_summary(
    start_date: str,
    end_date: str,
    tenant_id: Optional[int] = None,
    unit_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601")
    
    stats_data = AuditStatsIn(
        start_date=start,
        end_date=end,
        tenant_id=tenant_id,
        unit_id=unit_id
    )
    
    service = AuditService(db)
    return service.get_audit_stats(stats_data)


# Report endpoints
@router.post("/reports", response_model=AuditReportOut)
def create_audit_report(
    report_data: AuditReportIn,
    user_id: str = "Sistema",
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    return service.create_audit_report(report_data, user_id)


@router.get("/reports/{report_id}", response_model=AuditReportOut)
def get_audit_report(report_id: str, db: Session = Depends(get_db)):
    service = AuditService(db)
    report = service.get_audit_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório de auditoria não encontrado")
    return report


@router.get("/reports/user/{user_id}")
def get_user_audit_reports(user_id: str, db: Session = Depends(get_db)):
    service = AuditService(db)
    return service.get_user_audit_reports(user_id)


@router.put("/reports/{report_id}")
def update_audit_report(
    report_id: str,
    file_path: Optional[str] = None,
    download_url: Optional[str] = None,
    status: str = "completed",
    db: Session = Depends(get_db)
):
    service = AuditService(db)
    report = service.update_audit_report(report_id, file_path, download_url, status)
    if not report:
        raise HTTPException(status_code=404, detail="Relatório de auditoria não encontrado")
    return report


@router.delete("/reports/expired")
def delete_expired_reports(db: Session = Depends(get_db)):
    service = AuditService(db)
    count = service.delete_expired_reports()
    return {"message": f"{count} relatórios expirados foram excluídos"}


# Utility endpoints
@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Audit Service"}


@router.get("/")
def root():
    return {"message": "Audit Service API"}

