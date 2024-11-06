from pydantic import BaseModel


class WateringCreateForm(BaseModel):
    appointment_time: str
    intensity: int


class WateringResponse(BaseModel):
    id: int
    appointment_time: str
    intensity: int
    host_agent: int
