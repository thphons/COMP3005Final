from sqlalchemy import Column, Integer, DateTime, String, select
from .base import Base

class Schedule_View(Base):
    __tablename__ = "schedule"
    
    room_id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(), primary_key=True)
    end_time = Column(DateTime())
    trainer_id = Column(Integer)
    schedule_type = Column(String(100))