"""US4 integration test: an out-of-scope retrieval attempt is blocked and produces a
traceable TraceEvent (FR-026)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.integration
def test_blocked_attempt_produces_trace_event(app_client, seeded_course, seeded_activity):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-authorized"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    configure_test_recipients(app_client, seeded_activity, recipients=("part-blocked01",))
    session_resp = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-blocked01", "activity_configuration_id": seeded_activity},
    )
    session_id = session_resp.json()["session_id"]

    r2 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-NOT-authorized",
            "session_id": session_id,
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )
    assert r2.status_code == 200
    assert r2.json()["fragments"] == []

    Session = app_client.__db_sessionmaker__
    db = Session()
    events = (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session_id,
            models.TraceEvent.event_type == "material_retrieval_blocked_out_of_scope",
        )
        .all()
    )
    db.close()
    assert len(events) == 1
    assert events[0].memory_category == "metacognitive"
