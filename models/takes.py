from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from .base import Base


class Takes(Base):
    __tablename__ = "takes"

    member_id = Column(Integer, ForeignKey("members.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"), primary_key=True)