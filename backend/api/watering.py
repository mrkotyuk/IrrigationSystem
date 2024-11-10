from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from utils.security import checkToken
from database.database import get_db
from models.agent import Agent
from models.watering import Watering
from schemas.watering import WateringCreateForm, WateringResponse

from .hardware import schedule_watering

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

    new_watering = Watering(
        appointment_time=watering_req.appointment_time,
        intensity=watering_req.intensity,
        host_agent_id=agent_id,
    )
    db.add(new_watering)
    db.commit()

    schedule_watering(
        agent.unigue_identificator,
        watering_req.intensity,
        watering_req.appointment_time,
        new_watering.id,
    )
    return new_watering


@router.get("", response_model=list[WateringResponse])
async def all_waterings(
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> list[WateringResponse]:
    waterings = db.query(Watering).all()
    return waterings


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
