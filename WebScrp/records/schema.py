from typing import Optional
from pydantic import BaseModel, constr
import datetime


class District(BaseModel):
    name: constr(min_length=2, max_length=60)


class ListDistrict(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    id: Optional[int]
    id_olx: int
    id_otodom: int
    rooms: int
    date: datetime.date
    price: float

    class Config:
        orm_mode = True


class Record(RecordBase):
    district_id: int


class RecordListing(RecordBase):
    district: ListDistrict

    class Config:
        orm_mode = True
