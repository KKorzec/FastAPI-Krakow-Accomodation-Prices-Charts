from fastapi import HTTPException, status
from typing import List
from . import models


async def create_new_district(request, database) -> models.District:
    new_district = models.District(name=request.name)
    database.add(new_district)
    database.commit()
    database.refresh(new_district)
    return new_district


async def get_all_districts(database) -> List[models.District]:
    districts = database.query(models.District).all()
    return districts


async def get_district_by_id(district_id, database) -> models.District:
    district_info = database.query(models.District).get(district_id)
    if not district_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District with that ID doesn't exist!")
    return district_info


async def delete_district_by_id(district_id, database):
    database.query(models.District).filter(models.District.id == district_id).delete()
    database.commit()


async def create_new_record(request, database) -> models.Record:
    new_record = models.Record(id_olx=request.id_olx,
                               id_otodom=request.id_otodom,
                               rooms=request.rooms,
                               date=request.date,
                               district_id=request.district_id,
                               price=request.price
                               )
    database.add(new_record)
    database.commit()
    database.refresh(new_record)
    return new_record


async def get_all_records(database) -> List[models.Record]:
    records = database.query(models.Record).all()
    return records


async def get_record_by_id(record_id, database) -> models.Record:
    record_info = database.query(models.Record).get(record_id)
    if not record_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record with that ID doesn't exist!")
    return record_info


def delete_record_by_id(record_id, database):
    database.query(models.Record).filter(models.Record.id == record_id).delete()
    database.commit()
