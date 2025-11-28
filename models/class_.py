from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base
from .base import Base


class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_time = Column(DateTime(), default=datetime.now)
    end_time = Column(DateTime(), default=datetime.now)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))

    # Constraint to enforce unique classes
    __table_args__ = (
        UniqueConstraint("room_id", "start_time", name="class_time"),
    )
    
