from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.database import Base


class Agent(Base):
    __tablename__ = "agent"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    location = Column(String)
    description = Column(String)
    unigue_identificator = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_online = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("operator.id"))
    author = relationship("User")
    scheduled_irrigations = relationship("Watering", back_populates="host_agent")
