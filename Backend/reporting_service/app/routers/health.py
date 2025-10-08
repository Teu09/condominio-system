from fastapi import APIRouter, Depends
from shared import auth_client
from ..schemas.reports import ReportRequest, ReportOut
from ..services.report_service import generate_report


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





