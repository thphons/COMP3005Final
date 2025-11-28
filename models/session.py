from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base
from .base import Base


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_time = Column(DateTime(), default=datetime.now)
    end_time = Column(DateTime(), default=datetime.now)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    member_id = Column(Integer, ForeignKey("members.id"))

    # Constraint to enforce unique sessions
    __table_args__ = (
        UniqueConstraint("room_id", "start_time", name="session_time"),
    )
    
