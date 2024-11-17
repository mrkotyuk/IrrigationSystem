from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as AuthAPI
from api.agent import router as AgentAPI
from api.watering import router as WateringAPI
from api.hardware import router as HardwareAPI

app = FastAPI(title="Irrigation API")


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://irrigationsystem.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


app.include_router(AuthAPI)
app.include_router(AgentAPI)
app.include_router(WateringAPI)
app.include_router(HardwareAPI)
