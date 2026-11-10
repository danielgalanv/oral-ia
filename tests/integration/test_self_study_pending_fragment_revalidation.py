"""T099 (Feature 002, follow-up to T085) — the queue-continuity fix in
`self_study_agency_composer.py` (`_PROGRESSIVE_MODES` block) reused a
`cognitive_state.concepts_pending` fragment by fetching its row directly
(`db.get(models.MaterialFragment, current_fragment_id)`), presuming only that it
"was already vetted when it was enqueued" — never revalidating authorization or
lifecycle at the moment of reuse. Between the turn that enqueues a fragment and the
turn that reuses it, any of seven independent changes can silently invalidate it
without the composer detecting it; if the row is gone entirely, the old code fell
back to `fragments[:1]` — an arbitrary, unrelated substitution.

Every assertion below states the CORRECT required behavior — invalid content MUST
NOT reach `output_text`, `sources`, the `generation_call` trace event's
`fragment_ids`, or survive in `concepts_pending`. Run against the pre-T099 code, all
seven MUST fail; the exact same assertions MUST hold, unchanged, once T099 is
implemented.
"""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_mode_doubt_resolution import (
    _authorize_catalogued_self_study_outputs,
    _setup_activity_with_material,
)


def _read_concepts_pending(app_client, session_id: str) -> list[str]:
    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.get(models.CognitiveState, session_id)
    pending = list(state.concepts_pending) if state else []
    db.close()
    return pending


def _read_fragment_and_document(app_client, fragment_id: str):
    Session = app_client.__db_sessionmaker__
    db = Session()
    fragment = db.get(models.MaterialFragment, fragment_id)
    document = db.get(models.MaterialDocument, fragment.document_id) if fragment else None
    text = fragment.text if fragment else None
    db.close()
    return text, document


def _last_generation_fragment_ids(app_client, session_id: str) -> list[str]:
    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert events, "expected at least one generation_call trace event"
    return events[-1]["payload"].get("fragment_ids", [])


def _mutate_document_inactive(db, fragment):
    document = db.get(models.MaterialDocument, fragment.document_id)
    document.status = "inactive"
    db.add(document)


def _mutate_document_retired(db, fragment):
    document = db.get(models.MaterialDocument, fragment.document_id)
    document.retired_at = utcnow()
    db.add(document)


def _mutate_fragment_expired(db, fragment):
    fragment.valid_until = utcnow().replace(year=2000)
    db.add(fragment)


def _mutate_fragment_not_indexed(db, fragment):
    fragment.indexing_status = "pending"
    db.add(fragment)


def _mutate_fragment_unassigned(db, fragment):
    fragment.activity_configuration_ids = []
    db.add(fragment)


def _mutate_different_course(db, fragment):
    other_course = models.Course(name="Otro curso", subject_code="OTR999")
    db.add(other_course)
    db.flush()
    document = db.get(models.MaterialDocument, fragment.document_id)
    fragment.course_id = other_course.id
    document.course_id = other_course.id
    db.add_all([fragment, document])


def _mutate_fragment_deleted(db, fragment):
    db.delete(fragment)


_INVALIDATIONS = [
    ("document_inactive", _mutate_document_inactive),
    ("document_retired", _mutate_document_retired),
    ("fragment_expired", _mutate_fragment_expired),
    ("fragment_not_indexed", _mutate_fragment_not_indexed),
    ("fragment_unassigned_from_activity", _mutate_fragment_unassigned),
    ("fragment_different_course", _mutate_different_course),
    ("fragment_row_deleted", _mutate_fragment_deleted),
]


@pytest.mark.integration
@pytest.mark.parametrize("case_id,mutate", _INVALIDATIONS, ids=[c[0] for c in _INVALIDATIONS])
def test_invalidated_pending_fragment_never_reused(app_client, self_study_activity, case_id, mutate):
    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["guided_explanation"])
    _authorize_catalogued_self_study_outputs(
        app_client,
        activity_id,
        f"est-t099-{case_id}",
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": f"est-t099-{case_id}", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    turn1 = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Explícame paso a paso el documento de prueba"},
    )
    assert turn1.status_code == 200

    pending_before = _read_concepts_pending(app_client, session_id)
    assert pending_before, "guided_explanation must have queued at least one pending fragment after turn 1"
    invalid_id = pending_before[0]
    invalid_text, _invalid_document = _read_fragment_and_document(app_client, invalid_id)
    assert invalid_text is not None

    Session = app_client.__db_sessionmaker__
    db = Session()
    fragment = db.get(models.MaterialFragment, invalid_id)
    mutate(db, fragment)
    db.commit()
    db.close()

    turn2 = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "continúa"},
    )
    assert turn2.status_code == 200
    body = turn2.json()

    assert invalid_text not in (body["output_text"] or ""), (
        f"{case_id}: invalidated fragment's text leaked into output_text"
    )
    # NOTE: all three sample.docx fragments share the same document_id — comparing
    # document_id would spuriously fail whenever a DIFFERENT, still-valid fragment of
    # the same document is legitimately reused. Compare the specific fragment's own
    # text instead, which uniquely identifies it in this fixture.
    assert all(source.get("fragment_text") != invalid_text for source in body["sources"]), (
        f"{case_id}: invalidated fragment's text leaked into sources"
    )
    assert invalid_id not in _last_generation_fragment_ids(app_client, session_id), (
        f"{case_id}: invalidated fragment_id leaked into the generation_call trace"
    )
    pending_after = _read_concepts_pending(app_client, session_id)
    assert invalid_id not in pending_after, (
        f"{case_id}: invalidated fragment_id survived in concepts_pending as if still usable"
    )
