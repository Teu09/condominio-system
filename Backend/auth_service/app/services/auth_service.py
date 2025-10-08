import datetime
import jwt
from fastapi import HTTPException
from ..core.config import settings
from ..repositories.user_repository import get_user_by_email


def authenticate(email: str, password: str, company: str | None) -> dict:
    row = get_user_by_email(email)
    if not row or row[1] != password:
        raise HTTPException(status_code=401, detail='Credenciais inválidas')
    user_id, _, role, full_name = row
    payload = {
        'sub': str(user_id),
        'role': role,
        'company': company or 'default',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=settings.jwt_ttl_hours),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return {
        'access_token': token,
        'token_type': 'bearer',
        'user': {'id': user_id, 'email': email, 'name': full_name, 'role': role},
    }






