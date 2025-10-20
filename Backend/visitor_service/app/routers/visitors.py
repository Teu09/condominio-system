from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..services import visitor_service as svc


router = APIRouter(prefix='/visitors', tags=['visitors'])


@router.get('', dependencies=[Depends(auth_client.get_current_user)])
def list_visitors_ep():
    return svc.list_visitors()


@router.post('', dependencies=[Depends(auth_client.get_current_user)])
def create_visitor_ep(payload: dict):
    return svc.create_visitor(
        name=payload['name'],
        document=payload['document'],
        unit_id=payload['unit_id'],
        visit_date=payload['visit_date'],
        expected_duration=payload.get('expected_duration', 60),
        purpose=payload['purpose'],
        contact_phone=payload.get('contact_phone')
    )


@router.post('/{visitor_id}/check-in', dependencies=[Depends(auth_client.get_current_user)])
def check_in_visitor_ep(visitor_id: int):
    return svc.check_in_visitor(visitor_id)


@router.post('/{visitor_id}/check-out', dependencies=[Depends(auth_client.get_current_user)])
def check_out_visitor_ep(visitor_id: int):
    return svc.check_out_visitor(visitor_id)


@router.delete('/{visitor_id}', dependencies=[Depends(auth_client.get_current_user)])
def delete_visitor_ep(visitor_id: int):
    return svc.delete_visitor(visitor_id)


