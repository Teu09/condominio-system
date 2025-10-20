from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from datetime import datetime
from io import StringIO
import csv
from shared import auth_client
from ..services import report_service as svc


router = APIRouter(prefix='/reports', tags=['reports'])


@router.post('/generate', dependencies=[Depends(auth_client.get_current_user)])
def generate_report_ep(payload: dict):
    report_type = payload['report_type']
    start_date = datetime.fromisoformat(payload['start_date'])
    end_date = datetime.fromisoformat(payload['end_date'])
    return svc.generate_report(report_type, start_date, end_date)


@router.get('/reservations/export', response_class=PlainTextResponse, dependencies=[Depends(auth_client.get_current_user)])
def export_reservations_csv(start_date: str, end_date: str):
    sd = datetime.fromisoformat(start_date)
    ed = datetime.fromisoformat(end_date)
    report = svc.generate_report('reservations', sd, ed)
    rows = report['data'].get('rows', []) if isinstance(report.get('data'), dict) else []

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'unit_id', 'area', 'start_time', 'end_time', 'status'])
    for r in rows:
        writer.writerow([r.get('id'), r.get('unit_id'), r.get('area'), r.get('start_time'), r.get('end_time'), r.get('status')])
    return output.getvalue()


