from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import declarative_base
from .base import Base


class Availability(Base):
    __tablename__ = "availability"

    trainer_id = Column(Integer, ForeignKey("trainers.id"), primary_key=True)
    start_time = Column(DateTime(), default=datetime.now)
    end_time = Column(DateTime(), default=datetime.now)
    availability_type = Column(String(100), nullable=False)
