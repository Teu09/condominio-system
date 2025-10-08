from pydantic import BaseModel, field_validator
from datetime import datetime


class ReservationIn(BaseModel):
    unit_id: int
    area: str
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    def end_after_start(cls, v, info):
        values = info.data
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class ReservationOut(BaseModel):
    id: int
    unit_id: int
    area: str
    start_time: datetime
    end_time: datetime
    status: str



