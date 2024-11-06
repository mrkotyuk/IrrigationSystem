from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from utils.security import checkToken
from database.database import get_db
from models.agent import Agent
from schemas.agent import AgentCreateForm, AgentShortResponse, AgentResponse

router = APIRouter(prefix="/api/v1/agent", tags=["Agents"])


@router.post("", response_model=AgentResponse)
async def create_agent(
    agent_req: AgentCreateForm,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> AgentResponse:

    if (
        db.query(Agent)
        .filter(Agent.unigue_identificator == agent_req.unigue_identificator)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Agent already exist")
    new_agent = Agent(
        title=agent_req.title,
        location=agent_req.location,
        description=agent_req.description,
        unigue_identificator=agent_req.unigue_identificator,
        author_id=agent_req.author_id,
    )
    db.add(new_agent)
    db.commit()
    return new_agent


@router.get("", response_model=list[AgentShortResponse])
async def get_agents(
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> list[AgentShortResponse]:

    agents = db.query(Agent).all()

    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def one_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> AgentResponse:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"data": "Agent deleted successfully"}


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_req: AgentCreateForm,
    db: Session = Depends(get_db),
    is_authorised: bool = Depends(checkToken),
) -> AgentResponse:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.query(Agent).filter(Agent.id == agent_id).update(agent_req.model_dump())
    db.commit()
    db.refresh(agent)
    return agent
