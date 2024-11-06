from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Boolean
from sqlalchemy.orm import relationship
from database.database import Base


class Agent(Base):
    __tablename__ = "agent"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    location = Column(String)
    description = Column(String)
    unigue_identificator = Column(String, unique=True)
    created_at = Column(DATETIME, default=datetime.now(timezone.utc))
    is_online = Column(Boolean)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User")
