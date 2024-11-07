from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .watering import WateringResponse
from .user import UserResponse


class AgentCreateForm(BaseModel):
    title: str
    location: str
    description: str
    unigue_identificator: str
    author_id: int


class AgentShortResponse(BaseModel):
    id: int
    title: str
    location: str
    description: str
    created_at: datetime
    is_online: bool


class AgentResponse(BaseModel):
    id: int
    title: str
    location: str
    description: str
    unigue_identificator: str
    created_at: datetime
    is_online: bool
    author_id: int
    author: UserResponse
    scheduled_irrigations: list[WateringResponse] = None

    class Config:
        from_attributes = True
