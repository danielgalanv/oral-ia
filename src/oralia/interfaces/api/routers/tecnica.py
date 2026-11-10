"""Área técnica/docente — contracts/api-tecnica.md."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.create_activity import (
    ActivityAlreadyImmutable,
    ActivityConfigurationInput,
    ActivityNotFound,
    ActivitySuccessionInput,
    ActivitySuccessionNotAllowed,
    GeneralKnowledgePolicyMismatch,
    create_activity,
    succeed_activity_configuration,
)
from oralia.application.commands.register_agency import (
    AgencyCompositionInput,
    UnknownAgentReference,
    list_agencies,
    register_agency,
)
from oralia.application.commands.register_agent import (
    AgentRegistrationInput,
    list_agents,
    register_agent,
)
from oralia.application.queries.get_catalog import list_agency_summaries, list_agent_descriptors
from oralia.application.queries.get_session import get_session_detail, list_sessions
from oralia.application.queries.reconstruct_session_trace import reconstruct_session_trace
from oralia.interfaces.api.deps.auth_stub import tecnica_access_control
from oralia.interfaces.api.deps.db import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["tecnica"],
    dependencies=[Depends(tecnica_access_control)],
)


@router.post("/activities", status_code=201)
def post_activity(
    data: ActivityConfigurationInput,
    family_id: str | None = None,
    db: SASession = Depends(get_db, scope="function"),
):
    try:
        activity = create_activity(db, data, family_id=family_id)
    except ActivityAlreadyImmutable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {
        "id": activity.id,
        "family_id": activity.family_id,
        "version": activity.version,
        "name": activity.name,
        "immutable_since": activity.immutable_since,
    }


@router.post("/activities/{activity_id}/successors", status_code=201)
def post_activity_successor(
    activity_id: str,
    data: ActivitySuccessionInput,
    db: SASession = Depends(get_db, scope="function"),
):
    try:
        activity = succeed_activity_configuration(db, activity_id, data)
    except ActivityNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActivitySuccessionNotAllowed as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except GeneralKnowledgePolicyMismatch as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "id": activity.id,
        "family_id": activity.family_id,
        "version": activity.version,
        "name": activity.name,
        "immutable_since": activity.immutable_since,
    }


@router.post("/agents", status_code=201)
def post_agent(data: AgentRegistrationInput, db: SASession = Depends(get_db, scope="function")):
    agent = register_agent(db, data)
    return {"id": agent.id, "name": agent.name, "version": agent.version}


@router.post("/agencies", status_code=201)
def post_agency(data: AgencyCompositionInput, db: SASession = Depends(get_db, scope="function")):
    try:
        agency = register_agency(db, data)
    except UnknownAgentReference as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"id": agency.id, "name": agency.name, "version": agency.version}


@router.get("/catalog/agents")
def get_catalog_agents(db: SASession = Depends(get_db, scope="function")):
    return [d.model_dump() for d in list_agent_descriptors(db)]


@router.get("/catalog/agencies")
def get_catalog_agencies(db: SASession = Depends(get_db, scope="function")):
    return list_agency_summaries(db)


@router.get("/sessions")
def get_sessions(status: str | None = None, db: SASession = Depends(get_db, scope="function")):
    return list_sessions(db, status=status)


@router.get("/sessions/{session_id}")
def get_session(session_id: str, db: SASession = Depends(get_db, scope="function")):
    detail = get_session_detail(db, session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="session not found")
    return detail


@router.get("/sessions/{session_id}/trace")
def get_session_trace(session_id: str, db: SASession = Depends(get_db, scope="function")):
    return reconstruct_session_trace(db, session_id)


# Exposed for tests that want to enumerate agents directly (not part of the public contract).
__all__ = ["router", "list_agents", "list_agencies"]
