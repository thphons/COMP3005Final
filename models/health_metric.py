from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import declarative_base
from .base import Base

## Type can be either "goal" (one per user), or "record" (many per user)

class Health_Metric(Base):
    __tablename__ = "health_metrics"

    date = Column(DateTime(), default=datetime.now, primary_key=True)
    record_type = Column(String(100), primary_key=True)
    user_id = Column(Integer, ForeignKey("members.id"), primary_key=True)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    vo2Max = Column(Integer, nullable=False)
    body_composition = Column(Integer, nullable=False)
    resting_hr = Column(Integer, nullable=False)
