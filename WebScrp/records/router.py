from fastapi import HTTPException, APIRouter, Depends, status, FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text

from WebScrp import db
from . import schema
from . import services
from . import scraper_olx
from . import scraper_tabela

router = APIRouter(
    tags=['Records'],
    prefix='/record'
)


@router.post('/district', status_code=status.HTTP_201_CREATED)
async def create_district(request: schema.District, database: Session = Depends(db.get_db)):
    new_district = await services.create_new_district(request, database)
    return new_district


@router.get('/district', response_model=List[schema.ListDistrict])
async def get_all_districts(database: Session = Depends(db.get_db)):
    return await services.get_all_districts(database)


@router.get('/district/{district_id}', response_model=schema.ListDistrict)
async def get_district_by_id(district_id: int, database: Session = Depends(db.get_db)):
    return await services.get_district_by_id(district_id, database)


@router.delete('/district/{district_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_district_by_id(district_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_district_by_id(district_id, database)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_record(request: schema.Record, database: Session = Depends(db.get_db)):
    from WebScrp.records import validator
    district = await validator.verify_district_exist(request.district_id, database)
    if not district:
        raise HTTPException(
            status_code=400,
            detail="Wrong district id!"
        )
    record = await services.create_new_record(request, database)
    return record


@router.post('/olx', status_code=status.HTTP_201_CREATED)
async def create_record_olx(database: Session = Depends(db.get_db)):
    record = await scraper_olx.create_new_record_olx(database)
    return record


@router.get('/olx/1_0')
async def get_olx_data_1_0(database: Session = Depends(db.get_db)):
    query = text("""
        SELECT d.name AS district_name, d.id AS id, CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
        FROM districts d
        JOIN records r ON r.district_id = d.id
        WHERE r.rooms = 1
        GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/1_30')
async def get_olx_data_1_30(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 1 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/1_60')
async def get_olx_data_1_60(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 1 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY) AND r.date < DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/2_0')
async def get_olx_data_2_0(database: Session = Depends(db.get_db)):
    query = text("""
        SELECT d.name AS district_name, d.id AS id, CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
        FROM districts d
        JOIN records r ON r.district_id = d.id
        WHERE r.rooms = 2
        GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/2_30')
async def get_olx_data_2_30(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 2 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/2_60')
async def get_olx_data_2_60(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 2 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY) AND r.date < DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/3_0')
async def get_olx_data_3_0(database: Session = Depends(db.get_db)):
    query = text("""
        SELECT d.name AS district_name, d.id AS id, CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
        FROM districts d
        JOIN records r ON r.district_id = d.id
        WHERE r.rooms = 3
        GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/3_30')
async def get_olx_data_3_30(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 3 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.get('/olx/3_60')
async def get_olx_data_3_60(database: Session = Depends(db.get_db)):
    query = text("""
    SELECT 
        d.name AS district_name, 
        d.id AS id, 
        CAST(ROUND(AVG(r.price)) AS SIGNED) AS average_price
    FROM districts d
    JOIN records r ON r.district_id = d.id
    WHERE r.rooms = 3 AND r.date >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY) AND r.date < DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY d.id;
    """)
    result = database.execute(query).fetchall()

    # Przetwarzanie tablicy wynikowej na listę słowników
    json_result = [{"id": row.id, "district_name": row.district_name, "average_price": row.average_price} for row in result]

    return json_result


@router.post('/tabela', status_code=status.HTTP_201_CREATED)
async def create_record_tabela(database: Session = Depends(db.get_db)):
    record = await scraper_tabela.create_new_record_tabela(database)
    return record


@router.get('/', response_model=List[schema.RecordListing])
async def get_all_records(database: Session = Depends(db.get_db)):
    return await services.get_all_records(database)


@router.get('/{record_id}', response_model=schema.RecordListing)
async def get_record_by_id(record_id: int, database: Session = Depends(db.get_db)):
    return await services.get_record_by_id(record_id, database)


@router.delete('/{record_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_record_by_id(record_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_record_by_id(record_id, database)
