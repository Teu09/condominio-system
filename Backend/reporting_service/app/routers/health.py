from fastapi import APIRouter, Depends, Response
from shared import auth_client
from ..schemas.reports import ReportRequest, ReportOut
from ..services.report_service import generate_report
from datetime import datetime
import csv
import io


router = APIRouter(prefix='', tags=['reports'])


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/info')
def info():
    return {'service': 'Reporting Service'}


@router.post('/reports/generate', response_model=ReportOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def generate_report_ep(request: ReportRequest):
    return generate_report(request.report_type, request.start_date, request.end_date)


@router.get('/reports/types')
def get_report_types():
    return {
        'available_types': ['visitors', 'maintenance', 'reservations', 'financial'],
        'descriptions': {
            'visitors': 'Visitor statistics and trends',
            'maintenance': 'Maintenance orders and completion rates',
            'reservations': 'Area reservations and usage patterns',
            'financial': 'Financial overview and costs'
        }
    }


@router.get('/reports/reservations/export', dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def export_reservations_csv(start_date: str, end_date: str):
    try:
        sd = datetime.fromisoformat(start_date)
        ed = datetime.fromisoformat(end_date)
    except Exception:
        return Response(content='invalid date format', media_type='text/plain', status_code=400)

    # Build dataset using repository stats endpoints for simplicity
    from ..repositories import report_repository as repo
    # We'll dump status and area breakdown as CSV rows
    data = repo.get_reservation_stats(sd, ed)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Report', 'Reservations', f'{sd.date()} to {ed.date()}'])
    writer.writerow([])
    writer.writerow(['Total Reservations', data.get('total_reservations', 0)])
    writer.writerow([])
    writer.writerow(['Status', 'Count'])
    for status, count in (data.get('status_breakdown') or {}).items():
        writer.writerow([status, count])
    writer.writerow([])
    writer.writerow(['Area', 'Count'])
    for area, count in (data.get('area_breakdown') or {}).items():
        writer.writerow([area, count])

    content = output.getvalue()
    return Response(
        content=content,
        media_type='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename="reservations_{sd.date()}_{ed.date()}.csv"'
        }
    )





