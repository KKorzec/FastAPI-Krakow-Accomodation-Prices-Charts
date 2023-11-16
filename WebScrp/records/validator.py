from typing import Optional
from sqlalchemy.orm import Session
from . models import District


async def verify_district_exist(district_id, db_session: Session) -> Optional[District]:
    return db_session.query(District).filter(District.id == district_id).first()
