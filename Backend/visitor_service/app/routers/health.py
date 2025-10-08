from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..schemas.visitors import VisitorIn, VisitorOut, VisitorUpdate
from ..services.visitor_service import list_visitors, get_visitor, create_visitor, check_in_visitor, check_out_visitor, delete_visitor


router = APIRouter(prefix='', tags=['visitors'])


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/info')
def info():
    return {'service': 'Visitor Service'}


@router.get('/visitors', response_model=List[VisitorOut], dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def list_visitors_ep():
    return list_visitors()


@router.get('/visitors/{visitor_id}', response_model=VisitorOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def get_visitor_ep(visitor_id: int):
    return get_visitor(visitor_id)


@router.post('/visitors', response_model=VisitorOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def create_visitor_ep(visitor: VisitorIn):
    return create_visitor(visitor.name, visitor.document, visitor.unit_id, 
                        visitor.visit_date, visitor.expected_duration, 
                        visitor.purpose, visitor.contact_phone)


@router.post('/visitors/{visitor_id}/check-in', response_model=VisitorOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def check_in_visitor_ep(visitor_id: int):
    return check_in_visitor(visitor_id)


@router.post('/visitors/{visitor_id}/check-out', response_model=VisitorOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def check_out_visitor_ep(visitor_id: int):
    return check_out_visitor(visitor_id)


@router.delete('/visitors/{visitor_id}', dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def delete_visitor_ep(visitor_id: int):
    return delete_visitor(visitor_id)





