from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..schemas.maintenance import MaintenanceIn, MaintenanceOut, MaintenanceUpdate
from ..services.maintenance_service import list_maintenance_orders, get_maintenance_order, create_maintenance_order, assign_maintenance_order, complete_maintenance_order, delete_maintenance_order


router = APIRouter(prefix='', tags=['maintenance'])


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/info')
def info():
    return {'service': 'Maintenance Service'}


@router.get('/maintenance', response_model=List[MaintenanceOut], dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def list_maintenance_orders_ep():
    return list_maintenance_orders()


@router.get('/maintenance/{order_id}', response_model=MaintenanceOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def get_maintenance_order_ep(order_id: int):
    return get_maintenance_order(order_id)


@router.post('/maintenance', response_model=MaintenanceOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def create_maintenance_order_ep(order: MaintenanceIn):
    return create_maintenance_order(order.unit_id, order.title, order.description, 
                                  order.priority, order.category, order.requested_by, 
                                  order.expected_date)


@router.post('/maintenance/{order_id}/assign', response_model=MaintenanceOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def assign_maintenance_order_ep(order_id: int, assigned_to: str):
    return assign_maintenance_order(order_id, assigned_to)


@router.post('/maintenance/{order_id}/complete', response_model=MaintenanceOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def complete_maintenance_order_ep(order_id: int):
    return complete_maintenance_order(order_id)


@router.delete('/maintenance/{order_id}', dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def delete_maintenance_order_ep(order_id: int):
    return delete_maintenance_order(order_id)





