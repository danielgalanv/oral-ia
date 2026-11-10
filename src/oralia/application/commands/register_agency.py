"""FR-006: compose an Agency by reusing already-registered agents. No new code/agents
are created at composition time — only references to catalog Agent rows."""

from __future__ import annotations

from pydantic import BaseModel
from sqlalchemy.orm import Session as SASession

from oralia.domain.agencies.agency import AgencyDefinition, ExecutionStep
from oralia.infrastructure.db import models


class UnknownAgentReference(ValueError):
    """Edge Case: the composer could not find a required agent in the catalog."""


class AgencyCompositionInput(BaseModel):
    name: str
    version: str
    steps: list[ExecutionStep]
    verifiers_required: list[str] = []
    fallback_step: str | None = None
    termination_rule: str = ""


def register_agency(db: SASession, data: AgencyCompositionInput) -> models.Agency:
    # Validates the Principio IV rule (generator != verifier for itself) via the Pydantic
    # model's own validator, and rejects unknown agent references (Edge Case) up front.
    definition = AgencyDefinition(
        id="pending",
        name=data.name,
        version=data.version,
        steps=data.steps,
        verifiers_required=data.verifiers_required,
        fallback_step=data.fallback_step,
        termination_rule=data.termination_rule,
    )

    referenced_agent_ids = {step.agent_id for step in definition.steps}
    known_ids = {
        row.id for row in db.query(models.Agent.id).filter(models.Agent.id.in_(referenced_agent_ids)).all()
    }
    missing = referenced_agent_ids - known_ids
    if missing:
        raise UnknownAgentReference(f"unknown agent id(s) referenced by agency steps: {missing}")

    agency = models.Agency(
        name=data.name,
        version=data.version,
        steps=[step.model_dump() for step in data.steps],
        verifiers_required=data.verifiers_required,
        fallback_step=data.fallback_step,
        termination_rule=data.termination_rule,
    )
    db.add(agency)
    db.flush()
    return agency


def list_agencies(db: SASession) -> list[models.Agency]:
    return db.query(models.Agency).all()


def get_agency(db: SASession, agency_id: str) -> models.Agency | None:
    return db.get(models.Agency, agency_id)
