from fastapi import HTTPException
from ..repositories.unit_repository import list_units_rows, insert_unit


def list_units():
    rows = list_units_rows()
    return [{'id':r[0],'block':r[1],'number':r[2],'owner_id':r[3]} for r in rows]


def create_unit(block: str, number: str, owner_id: int | None):
    try:
        uid = insert_unit(block, number, owner_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'id': uid, 'block': block, 'number': number, 'owner_id': owner_id}



















