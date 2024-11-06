from pydantic import BaseModel
from datetime import datetime
from watering import WateringResponse


class AgentCreateForm(BaseModel):
    title: str
    location: str
    description: str
    unigue_identificator: str
    author_id: int


class AgentShortResponse(BaseModel):
    id: int
    location: str
    description: str
    created_at: datetime
    is_online: bool


class AgentResponse(BaseModel):
    id: int
    location: str
    description: str
    created_at: datetime
    author_id: int
    scheduled_irrigations: list[WateringResponse]
