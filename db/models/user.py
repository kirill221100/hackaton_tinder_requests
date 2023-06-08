from sqlalchemy import Integer, Column, Boolean, DateTime
from db.db_setup import Base
from datetime import datetime


class UserNotifications(Base):
    __tablename__ = 'user_notifications'
    id = Column(Integer, primary_key=True)
    is_request = Column(Boolean)
    profile_id = Column(Integer)
    user_id = Column(Integer)
    date = Column(DateTime, default=datetime.now)
