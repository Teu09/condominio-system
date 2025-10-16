from fastapi import APIRouter
from ..schemas.auth import LoginIn, TokenOut
from ..services.auth_service import authenticate, authenticate_super_admin


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=TokenOut)
def login(data: LoginIn):
    return authenticate(data.email, data.password, data.tenant_id)


@router.post('/super-admin-login', response_model=TokenOut)
def super_admin_login(data: LoginIn):
    """Login específico para super administrador"""
    return authenticate_super_admin(data.email, data.password)






