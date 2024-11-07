import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from utils.security import checkToken
from database.database import get_db
from models.agent import Agent
from models.watering import Watering
from schemas.watering import WateringCreateForm, WateringResponse

from .hardware import send_scheduled_message

router = APIRouter(prefix="/api/v1/watering", tags=["Waterings"])


@router.post("/{agent_id}", response_model=WateringResponse)
async def create_watering(
    agent_id: int,
    watering_req: WateringCreateForm,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> WateringResponse:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        send_time_dt = datetime.strptime(
            watering_req.appointment_time, "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'"
        )

    delay = (send_time_dt - datetime.now()).total_seconds()
    if delay < 0:
        raise HTTPException(status_code=400, detail="Send time must be in the future")

    new_watering = Watering(
        appointment_time=watering_req.appointment_time,
        intensity=watering_req.intensity,
        host_agent_id=agent_id,
    )
    db.add(new_watering)
    db.commit()

    asyncio.create_task(
        send_scheduled_message(
            agent.unigue_identificator,
            str(watering_req.intensity),
            delay,
            new_watering.id,
        )
    )

    return new_watering


@router.get("/{agent_id}", response_model=list[WateringResponse])
async def all_waterings(
    agent_id: int,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> list[WateringResponse]:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    waterings = db.query(Watering).filter(Watering.host_agent_id == agent_id)
    return waterings


@router.put("/{watering_id}")
async def update_watering(
    watering_id: int,
    watering_req: WateringCreateForm,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
):
    watering = db.query(Watering).filter(Watering.id == watering_id).first()
    if not watering:
        raise HTTPException(status_code=404, detail="Watering not found")
    db.query(Watering).filter(Watering.id == watering_id).update(
        watering_req.model_dump()
    )
    db.commit()
    db.refresh(watering)
    return watering


@router.delete("/{watering_id}")
async def delete_watering(
    watering_id: int,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
):
    watering = db.query(Watering).filter(Watering.id == watering_id).first()
    if not watering:
        raise HTTPException(status_code=404, detail="Watering not found")
    db.delete(watering)
    db.commit()
    return {"data": "Watering deleted successfully"}
