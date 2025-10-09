from fastapi import HTTPException
from ..repositories.user_repository import list_users_rows, insert_user, get_user_row


def list_users():
    rows = list_users_rows()
    return [{'id':r[0],'email':r[1],'full_name':r[2],'role':r[3]} for r in rows]


def create_user(email: str, password: str, full_name: str | None, role: str):
    try:
        uid = insert_user(email, password, full_name, role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'id': uid, 'email': email, 'full_name': full_name, 'role': role}


def get_user(user_id: int, caller: dict):
    if caller['id'] != user_id and caller['role'] not in ('admin','sindico'):
        raise HTTPException(status_code=403, detail='Forbidden')
    r = get_user_row(user_id)
    if not r:
        raise HTTPException(status_code=404, detail='User not found')
    return {'id': r[0], 'email': r[1], 'full_name': r[2], 'role': r[3]}









