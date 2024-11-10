from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base


class User(Base):
    __tablename__ = "operator"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
