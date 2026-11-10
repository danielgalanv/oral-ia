"""study_turn_orchestrator: public entry point `run_study_turn`, reutilizando
`execute_agency` (Feature 001, sin cambios) a través de `self_study_agency_composer`
(que construye y ejecuta la `AgencyDefinition` dinámica de cada turno, research.md §6)."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.orchestration.self_study_agency_composer import (
    StudyTurnResult,
)
from oralia.application.orchestration.self_study_agency_composer import (
    run_study_turn as _run_study_turn,
)
from oralia.infrastructure.db import models


async def run_study_turn(
    db: SASession, session: models.Session, input_text: str, *, dialogue_control=None, semantic_runtime=None
) -> StudyTurnResult:
    return await _run_study_turn(
        db,
        session,
        input_text,
        **({"dialogue_control": dialogue_control} if dialogue_control is not None else {}),
        **({"semantic_runtime": semantic_runtime} if semantic_runtime is not None else {}),
    )
