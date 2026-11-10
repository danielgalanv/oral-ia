"""StatePatch: append-only log + atomic compare-and-swap apply engine.

research.md §1: a patch applies only if ``base_version`` matches the CognitiveState's
current version at write time (an atomic ``UPDATE ... WHERE version = :base_version``).
Every attempt is persisted, applied or not — this is simultaneously the mechanism for
conflict detection (US5, FR-019) and for full reconstruction (US6, FR-016, FR-020).
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session as SASession

from oralia.domain.cognitive_state.cognitive_state import ELEMENT_TYPES, MINIMUM_FIELDS
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class InvalidElementType(ValueError):
    pass


def apply_patch(
    db: SASession,
    *,
    session_id: str,
    base_version: int,
    proposed_by_agent_id: str,
    element_type: str,
    payload: dict[str, Any],
    justification: str = "",
) -> models.StatePatch:
    """Attempt to apply ``payload`` on top of ``base_version``.

    Always persists a ``StatePatch`` row (applied or rejected) and returns it. Callers
    inspect ``patch.applied`` to know whether to retry against the new current version.
    """

    if element_type not in ELEMENT_TYPES:
        raise InvalidElementType(f"{element_type!r} is not one of {ELEMENT_TYPES}")

    unknown_fields = set(payload) - (set(MINIMUM_FIELDS) | {"dialogue_context"})
    if unknown_fields:
        raise ValueError(f"payload references unknown CognitiveState fields: {unknown_fields}")

    if "dialogue_context" in payload and payload["dialogue_context"] is not None:
        from oralia.domain.dialogue.contracts import DialogueContext

        payload = dict(payload)
        payload["dialogue_context"] = DialogueContext.model_validate(payload["dialogue_context"]).model_dump(
            mode="json"
        )

    now = utcnow()
    patch = models.StatePatch(
        session_id=session_id,
        base_version=base_version,
        resulting_version=None,
        proposed_by_agent_id=proposed_by_agent_id,
        payload=payload,
        element_type=element_type,
        justification=justification,
        applied=False,
        rejected_reason=None,
        created_at=now,
    )

    resulting_version = base_version + 1
    values = dict(payload)
    values["version"] = resulting_version
    values["updated_at"] = now

    result = db.execute(
        update(models.CognitiveState)
        .where(
            models.CognitiveState.session_id == session_id,
            models.CognitiveState.version == base_version,
        )
        .values(**values)
    )

    if result.rowcount == 1:
        patch.applied = True
        patch.resulting_version = resulting_version
    else:
        current = db.get(models.CognitiveState, session_id)
        current_version = current.version if current is not None else None
        patch.applied = False
        patch.rejected_reason = (
            f"conflict: base_version={base_version} does not match current version={current_version}"
        )

    db.add(patch)
    db.flush()
    return patch


def history_for_session(db: SASession, session_id: str) -> list[models.StatePatch]:
    """Full patch history — applied and rejected — ordered for reconstruction (US6)."""
    return (
        db.query(models.StatePatch)
        .filter(models.StatePatch.session_id == session_id)
        .order_by(models.StatePatch.created_at.asc())
        .all()
    )
