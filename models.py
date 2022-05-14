from .database import Base
from sqlalchemy import Column, Float,Integer,String
from operator import index


class AddressBook(Base):
    __tablename__ = "addressbook"
    id = Column(Integer,primary_key =True,index = True)
    name = Column(String)
    address = Column(String)
    pin = Column(Integer)
    phone = Column(Integer)
    long = Column(Float)
    lat = Column(Float)

