"""Submit a definitive text answer to the shared oral-defense pipeline."""

from sqlalchemy.orm import Session as SASession

from oralia.application.orchestration.defense_agency_composer import (
    DefenseTurnResult,
    run_defense_turn,
)
from oralia.infrastructure.db import models


class SessionNotActive(ValueError):
    pass


async def submit_defense_turn(
    db: SASession,
    session: models.Session,
    text: str,
    *,
    followup_agent=None,
    requested_topic: str | None = None,
    closure_retain: bool = False,
    closure_scope: list[str] | None = None,
    dialogue_control=None,
) -> DefenseTurnResult:
    if session.status != "active":
        raise SessionNotActive(f"session {session.id} is not active")
    return await run_defense_turn(
        db,
        session,
        text,
        followup_agent=followup_agent,
        requested_topic=requested_topic,
        closure_retain=closure_retain,
        closure_scope=closure_scope,
        **({"dialogue_control": dialogue_control} if dialogue_control is not None else {}),
    )


__all__ = ["SessionNotActive", "submit_defense_turn"]
