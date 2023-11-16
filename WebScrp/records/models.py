from sqlalchemy import Column, Integer, Date, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from WebScrp.db import Base


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))

    record = relationship("Record", back_populates="district")


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_olx = Column(Float, unique=True)
    id_otodom = Column(Float, unique=True)
    rooms = Column(Integer)
    date = Column(Date)
    district_id = Column(Integer, ForeignKey('districts.id', ondelete="CASCADE"),)
    district = relationship("District", back_populates="record")
    price = Column(Float)

    def __init__(self, id_olx, id_otodom, rooms, date, district_id, price, *args, **kwargs):
        self.id_olx = id_olx
        self.id_otodom = id_otodom
        self.rooms = rooms
        self.date = date
        self.district_id = district_id
        self.price = price
