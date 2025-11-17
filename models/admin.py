from sqlalchemy import Column, Integer, String
from ..db import Base

class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True)
    name = Column(String)