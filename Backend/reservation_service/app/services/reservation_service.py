from fastapi import HTTPException
from ..repositories import reservation_repository as repo


def list_reservations(caller: dict):
    if caller['role'] in ('admin','sindico'):
        rows = repo.list_all()
    else:
        rows = repo.list_by_owner(caller['id'])
    return [{'id':r[0],'unit_id':r[1],'area':r[2],'start_time':r[3],'end_time':r[4],'status':r[5]} for r in rows]


def create_reservation(unit_id: int, area: str, start_time, end_time, caller: dict):
    if caller['role'] == 'morador':
        owner_id = repo.get_unit_owner_id(unit_id)
        if owner_id != caller['id']:
            raise HTTPException(status_code=403, detail='Forbidden: cannot reserve for this unit')
    if repo.has_conflict(area, start_time, end_time):
        raise HTTPException(status_code=409, detail='Conflict: area already reserved for this time range')
    if repo.count_upcoming_for_unit(unit_id) >= 2:
        raise HTTPException(status_code=400, detail='Reservation limit reached for this unit (2 in 30 days)')
    rid = repo.insert(unit_id, area, start_time, end_time, 'confirmed')
    return {'id': rid, 'unit_id': unit_id, 'area': area, 'start_time': start_time, 'end_time': end_time, 'status': 'confirmed'}


def cancel_reservation(res_id: int, caller: dict):
    info = repo.get_unit_id_and_status(res_id)
    if not info:
        raise HTTPException(status_code=404, detail='Reservation not found')
    unit_id, _ = info
    if caller['role'] not in ('admin','sindico'):
        owner_id = repo.get_unit_owner_id(unit_id)
        if owner_id != caller['id']:
            raise HTTPException(status_code=403, detail='Forbidden')
    repo.set_status(res_id, 'cancelled')
    return {'status':'cancelled'}


def is_time_range_available(area: str, start_time, end_time) -> bool:
    return not repo.has_conflict(area, start_time, end_time)









