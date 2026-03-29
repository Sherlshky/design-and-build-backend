from sqlalchemy import Column, Integer, String, BLOB, DateTime
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    face_image = Column(BLOB, nullable=False)
    nickname = Column(String)
    exp = Column(Integer)
    email = Column(String)


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    timestamp = Column(DateTime, default=func.now())
