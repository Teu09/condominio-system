from fastapi import HTTPException
from datetime import datetime
from ..repositories import maintenance_repository as repo


def list_maintenance_orders():
    rows = repo.list_maintenance_orders()
    return [{
        'id': r[0], 'unit_id': r[1], 'title': r[2], 'description': r[3],
        'priority': r[4], 'category': r[5], 'requested_by': r[6], 'status': r[7],
        'expected_date': r[8], 'assigned_to': r[9], 'completed_date': r[10], 'created_at': r[11]
    } for r in rows]


def get_maintenance_order(order_id: int):
    row = repo.get_maintenance_order(order_id)
    if not row:
        raise HTTPException(status_code=404, detail='Maintenance order not found')
    return {
        'id': row[0], 'unit_id': row[1], 'title': row[2], 'description': row[3],
        'priority': row[4], 'category': row[5], 'requested_by': row[6], 'status': row[7],
        'expected_date': row[8], 'assigned_to': row[9], 'completed_date': row[10], 'created_at': row[11]
    }


def create_maintenance_order(unit_id: int, title: str, description: str, 
                           priority: str, category: str, requested_by: int, 
                           expected_date=None):
    try:
        order_id = repo.create_maintenance_order(unit_id, title, description, 
                                                priority, category, requested_by, expected_date)
        return get_maintenance_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def assign_maintenance_order(order_id: int, assigned_to: str):
    order = get_maintenance_order(order_id)
    if order['status'] != 'open':
        raise HTTPException(status_code=400, detail='Order is not open for assignment')
    
    repo.update_maintenance_order(order_id, status='assigned', assigned_to=assigned_to)
    return get_maintenance_order(order_id)


def complete_maintenance_order(order_id: int):
    order = get_maintenance_order(order_id)
    if order['status'] not in ['assigned', 'in_progress']:
        raise HTTPException(status_code=400, detail='Order is not assigned or in progress')
    
    repo.update_maintenance_order(order_id, status='completed', completed_date=datetime.now())
    return get_maintenance_order(order_id)


def delete_maintenance_order(order_id: int):
    order = get_maintenance_order(order_id)
    if order['status'] in ['completed']:
        raise HTTPException(status_code=400, detail='Cannot delete completed order')
    
    repo.delete_maintenance_order(order_id)
    return {'message': 'Maintenance order deleted successfully'}




