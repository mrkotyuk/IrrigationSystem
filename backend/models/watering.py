from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Watering(Base):
    __tablename__ = "watering"
    id = Column(Integer, primary_key=True, index=True)
    appointment_time = Column(String, unique=True)
    intensity = Column(Integer)
    host_agent_id = Column(Integer, ForeignKey("agent.id"))
    host_agent = relationship("Agent", back_populates="scheduled_irrigations")
