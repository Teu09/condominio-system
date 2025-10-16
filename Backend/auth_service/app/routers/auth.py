from fastapi import APIRouter
from ..schemas.auth import LoginIn, TokenOut
from ..services.auth_service import authenticate


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=TokenOut)
def login(data: LoginIn):
    return authenticate(data.email, data.password, data.tenant_id)






