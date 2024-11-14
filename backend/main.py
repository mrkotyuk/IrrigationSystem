from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine

from api.auth import router as AuthAPI
from api.agent import router as AgentAPI
from api.watering import router as WateringAPI
from api.hardware import router as HardwareAPI

app = FastAPI(title="Irrigation API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthAPI)
app.include_router(AgentAPI)
app.include_router(WateringAPI)
app.include_router(HardwareAPI)
