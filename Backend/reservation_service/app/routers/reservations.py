from fastapi import APIRouter, Depends
from typing import List
from shared import auth_client
from ..schemas.reservations import ReservationIn, ReservationOut
from ..services.reservation_service import list_reservations, create_reservation, cancel_reservation


router = APIRouter(prefix='/reservations', tags=['reservations'])


@router.get('', response_model=List[ReservationOut])
def list_reservations_ep(auth=Depends(auth_client.get_current_user)):
    return list_reservations(auth)


@router.post('', response_model=ReservationOut)
def create_reservation_ep(r: ReservationIn, auth=Depends(auth_client.get_current_user)):
    return create_reservation(r.unit_id, r.area, r.start_time, r.end_time, auth)


@router.post('/{res_id}/cancel')
def cancel_reservation_ep(res_id: int, auth=Depends(auth_client.get_current_user)):
    return cancel_reservation(res_id, auth)






