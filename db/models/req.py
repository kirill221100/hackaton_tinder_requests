from sqlalchemy import Integer, Column, Boolean
from db.db_setup import Base


class ToProfile(Base):
    __tablename__ = 'toprofile'
    id = Column(Integer, primary_key=True)
    is_request = Column(Boolean)
    profile_id = Column(Integer)
    user_id = Column(Integer)


class ToUser(Base):
    __tablename__ = 'touser'
    id = Column(Integer, primary_key=True)
    is_request = Column(Boolean)
    profile_id = Column(Integer)
    user_id = Column(Integer)
