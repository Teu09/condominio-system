
# simple auth client to decode JWT and provide dependency helpers
import jwt
from fastapi import HTTPException, Header, Depends
from typing import Optional
SECRET='SECRET_KEY'

def decode_token(authorization: Optional[str]):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing authorization header')
    if authorization.startswith('Bearer '):
        token = authorization.split(' ',1)[1]
    else:
        token = authorization
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')
    return payload

def get_current_user(authorization: Optional[str] = Header(None)):
    payload = decode_token(authorization)
    # payload must contain 'sub' and 'role'
    return {'id': payload.get('sub'), 'role': payload.get('role')}

def require_role(allowed_roles):
    def dep(authorization: Optional[str] = Header(None)):
        user = get_current_user(authorization)
        if user['role'] not in allowed_roles:
            raise HTTPException(status_code=403, detail='Forbidden: role not allowed')
        return user
    return dep
