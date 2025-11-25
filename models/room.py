from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from .base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    roomNumber = Column(Integer, nullable=False)
