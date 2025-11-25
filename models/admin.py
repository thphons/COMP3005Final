from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base
from .base import Base


class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    dob = Column(DateTime(), default=datetime.now)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
