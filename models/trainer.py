from sqlalchemy import Column, Integer, String
from ..db import Base

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True)
    name = Column(String)