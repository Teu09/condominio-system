from fastapi import HTTPException
from datetime import datetime
from ..repositories import visitor_repository as repo


def list_visitors():
    rows = repo.list_visitors()
    return [{
        'id': r[0], 'name': r[1], 'document': r[2], 'unit_id': r[3],
        'visit_date': r[4], 'expected_duration': r[5], 'purpose': r[6],
        'contact_phone': r[7], 'status': r[8], 'check_in': r[9], 'check_out': r[10]
    } for r in rows]


def get_visitor(visitor_id: int):
    row = repo.get_visitor(visitor_id)
    if not row:
        raise HTTPException(status_code=404, detail='Visitor not found')
    return {
        'id': row[0], 'name': row[1], 'document': row[2], 'unit_id': row[3],
        'visit_date': row[4], 'expected_duration': row[5], 'purpose': row[6],
        'contact_phone': row[7], 'status': row[8], 'check_in': row[9], 'check_out': row[10]
    }


def create_visitor(name: str, document: str, unit_id: int, visit_date, 
                  expected_duration: int, purpose: str, contact_phone: str = None):
    try:
        visitor_id = repo.create_visitor(name, document, unit_id, visit_date, 
                                       expected_duration, purpose, contact_phone)
        return get_visitor(visitor_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def check_in_visitor(visitor_id: int):
    visitor = get_visitor(visitor_id)
    if visitor['status'] != 'scheduled':
        raise HTTPException(status_code=400, detail='Visitor is not scheduled')
    
    repo.update_visitor_status(visitor_id, 'checked_in', check_in=datetime.now())
    return get_visitor(visitor_id)


def check_out_visitor(visitor_id: int):
    visitor = get_visitor(visitor_id)
    if visitor['status'] != 'checked_in':
        raise HTTPException(status_code=400, detail='Visitor is not checked in')
    
    repo.update_visitor_status(visitor_id, 'checked_out', check_out=datetime.now())
    return get_visitor(visitor_id)


def delete_visitor(visitor_id: int):
    visitor = get_visitor(visitor_id)
    if visitor['status'] in ['checked_in']:
        raise HTTPException(status_code=400, detail='Cannot delete checked-in visitor')
    
    repo.delete_visitor(visitor_id)
    return {'message': 'Visitor deleted successfully'}








