"""FR-020/FR-021: end a self-study session (voluntary or limit-reached) and produce the
ephemeral, descriptive-only `study_summary` — composes the shared atomic close
primitive with `generate_study_summary`."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_session import close_session_with_outcome
from oralia.application.services.study_session_summary_service import generate_study_summary
from oralia.infrastructure.db import models


def end_study_session(
    db: SASession,
    session: models.Session,
    self_study_config: models.SelfStudyActivityConfig | None,
    *,
    status: str,
    retained_scope: frozenset[str] | None = None,
) -> dict | None:
    """Closes ``session`` (Feature 001 mechanism, unchanged) and returns the
    self-study summary dict — ``None`` if ``summary_authorized`` is false (FR-021)."""

    close_outcome = close_session_with_outcome(db, session, status=status, defer_privacy=True)

    # Only the caller that wins the active -> closed transition may emit the
    # participant-facing study summary.  Repeated voluntary/limit/safe-close
    # requests remain idempotent just like the shared technical close.
    if not close_outcome.transition_won:
        return None

    summary = (
        generate_study_summary(db, session)
        if self_study_config is not None and self_study_config.summary_authorized
        else None
    )
    from oralia.application.services.session_privacy_service import finalize_session_privacy

    finalize_session_privacy(db, session, retained_scope=retained_scope)
    return summary
