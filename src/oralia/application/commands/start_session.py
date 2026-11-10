"""FR-010, FR-011, FR-012a: start an interactive session."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.create_activity import mark_immutable_if_needed
from oralia.application.services import session_lock_service
from oralia.application.services.trace_service import record_event
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.infrastructure.db import models
from oralia.infrastructure.telemetry import resources

AI_DISCLOSURE = (
    "Estás interactuando con ORAL-IA, un sistema automático de apoyo docente. "
    "Puede cometer errores y no sustituye el criterio del profesorado."
)


class ActivityNotFound(ValueError):
    pass


class InvalidParticipantCode(ValueError):
    """Edge Case: código de participante ausente o con apariencia de dato personal real."""


class SessionPreflightFailure(ValueError):
    def __init__(self, code: Literal["recipient_not_allowed", "activity_unavailable"], message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def _looks_like_real_identity(code: str) -> bool:
    # Heuristic per spec Edge Cases: reject values that look like "Nombre Apellido" or
    # an email address rather than an opaque pseudonym token.
    if "@" in code:
        return True
    parts = code.split(" ")
    if len(parts) >= 2 and all(p[:1].isupper() for p in parts if p):
        return True
    return False


class StartSessionInput(BaseModel):
    participant_code: str
    activity_configuration_id: str


def start_session(db: SASession, data: StartSessionInput) -> models.Session:
    if not data.participant_code or _looks_like_real_identity(data.participant_code):
        raise InvalidParticipantCode(
            "participant_code must be an opaque pseudonym, not a real-looking identity"
        )

    activity = db.get(models.ActivityConfiguration, data.activity_configuration_id)
    if activity is None:
        raise ActivityNotFound(f"activity {data.activity_configuration_id} not found")
    governance = db.get(models.ActivityGovernance, activity.id)
    if governance is not None and governance.status != "active":
        raise ValueError("activity version is not published")
    # Validate recipient and the frozen publication contract before any participant,
    # session, governance or lock mutation. A pseudonym is a recipient label, not auth.
    try:
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        )
    except (TypeError, ValueError):
        raise SessionPreflightFailure(
            "activity_unavailable", "La actividad no tiene una política válida; solicita revisión docente."
        ) from None
    if data.participant_code not in policy.allowed_recipients:
        raise SessionPreflightFailure(
            "recipient_not_allowed",
            "El código no es destinatario de esta actividad; "
            "comprueba la actividad o solicita acceso docente.",
        )
    if policy.general_knowledge_allowed != activity.general_knowledge_allowed:
        raise SessionPreflightFailure(
            "activity_unavailable", "La política no coincide con la configuración de la actividad."
        )
    if governance is not None and governance.model_id == "guided_controlled":
        from oralia.application.services.guided_dialogue_service import validate_guided_configuration

        try:
            validate_guided_configuration(db, activity)
        except ValueError:
            raise SessionPreflightFailure(
                "activity_unavailable",
                "El contenido revisado no está disponible para este perfil; solicita revisión docente.",
            ) from None
    if governance is None:
        # Existing configurations were published by the historical teacher path.
        # Freeze their first-use material/model selection; do not reactivate a
        # different legacy member after this family has been explicitly governed.
        import os

        from oralia.application.services.activity_governance_service import register_governance

        if db.query(models.ActivityGovernance).filter_by(family_id=activity.family_id).first():
            raise ValueError("activity version is not published")
        references = [
            {"document_id": document.id, "version": document.version}
            for document in db.query(models.MaterialDocument).filter_by(status="active")
            if activity.id in (document.activity_configuration_ids or [])
        ]
        model = os.environ.get("ORALIA_OLLAMA_MODEL")
        governance = register_governance(
            db,
            activity,
            status="active",
            model_id=f"ollama:{model}" if model else "deterministic",
            material_versions=references,
        )
    if governance is not None and governance.status != "active":
        raise ValueError("activity version is not published")

    participant = db.get(models.ParticipantCode, data.participant_code)
    if participant is None:
        participant = models.ParticipantCode(code=data.participant_code)
        db.add(participant)
        db.flush()

    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="active",
        turn_count=0,
    )
    db.add(session)
    db.flush()

    # FR-012a: acquire the single-active-session lock; raises SessionAlreadyActive on
    # conflict, which the caller (API layer) maps to HTTP 409.
    session_lock_service.acquire(db, session)

    mark_immutable_if_needed(db, activity)

    record_event(
        db,
        session_id=session.id,
        event_type="session_started",
        payload={"activity_configuration_id": activity.id},
        # Session lifecycle events are session-level occurrences — episodic memory
        # (Constitution III), made explicit rather than relying on the default.
        memory_category="episodic",
        # FR-017: monitor CPU/memory per session, not just per agent.
        resource_usage=resources.as_dict(),
    )

    return session
