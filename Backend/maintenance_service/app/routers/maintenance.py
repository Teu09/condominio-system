from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..services import maintenance_service as svc


router = APIRouter(prefix='/maintenance', tags=['maintenance'])


@router.get('', dependencies=[Depends(auth_client.get_current_user)])
def list_orders_ep():
    return svc.list_maintenance_orders()


@router.post('', dependencies=[Depends(auth_client.get_current_user)])
def create_order_ep(payload: dict):
    return svc.create_maintenance_order(
        unit_id=payload['unit_id'],
        title=payload['title'],
        description=payload['description'],
        priority=payload.get('priority', 'medium'),
        category=payload.get('category', 'other'),
        requested_by=payload['requested_by'],
        expected_date=payload.get('expected_date')
    )


@router.post('/{order_id}/assign', dependencies=[Depends(auth_client.get_current_user)])
def assign_order_ep(order_id: int, payload: dict):
    return svc.assign_maintenance_order(order_id, payload['assigned_to'])


@router.post('/{order_id}/complete', dependencies=[Depends(auth_client.get_current_user)])
def complete_order_ep(order_id: int):
    return svc.complete_maintenance_order(order_id)


@router.delete('/{order_id}', dependencies=[Depends(auth_client.get_current_user)])
def delete_order_ep(order_id: int):
    return svc.delete_maintenance_order(order_id)


