from datetime import datetime

from app.database import Base
from pkg_resources import require
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_employee = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    addresses = relationship("Address")