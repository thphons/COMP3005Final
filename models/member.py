from sqlalchemy import Column, Integer, String
from ..db import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String)