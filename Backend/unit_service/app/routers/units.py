from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..schemas.units import UnitIn, UnitOut
from ..services.unit_service import list_units, create_unit


router = APIRouter(prefix='/units', tags=['units'])


@router.get('', response_model=List[UnitOut], dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def list_units_ep():
    return list_units()


@router.post('', response_model=UnitOut, dependencies=[Depends(auth_client.require_role(['admin','sindico']))])
def create_unit_ep(u: UnitIn):
    return create_unit(u.block, u.number, u.owner_id)



















