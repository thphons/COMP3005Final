from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import declarative_base
from .base import Base


class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    start_time = Column(DateTime(), default=datetime.now, primary_key=True)
    end_time = Column(DateTime(), default=datetime.now)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    
