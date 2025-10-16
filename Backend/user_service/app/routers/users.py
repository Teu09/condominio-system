from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..schemas.users import UserIn, UserOut
from ..services.user_service import list_users, create_user, get_user


router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=List[UserOut], dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def list_users_ep():
    return list_users()


@router.post('', response_model=UserOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def create_user_ep(u: UserIn):
    return create_user(u.email, u.password, u.full_name, u.role)


@router.get('/{user_id}', response_model=UserOut)
def get_user_ep(user_id: int, auth=Depends(auth_client.get_current_user)):
    return get_user(user_id, auth)













