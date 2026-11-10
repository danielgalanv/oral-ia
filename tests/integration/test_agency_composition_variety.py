"""Integration test: ≥3 composiciones de agencia distintas observadas entre
doubt_resolution/sin-evidencia/practice_questions (SC-003)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import configure_test_recipients, minimal_output_policy_columns


@pytest.mark.integration
def test_at_least_three_distinct_agency_compositions(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution", "practice_questions"],
        participant_code="est-variety-001",
    )
    configure_test_recipients(app_client, activity_id, recipients=("est-variety-001",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-variety-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    # 1. doubt_resolution with evidence: generate+verify-grounding+verify-constitutional.
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )

    # 2. practice_questions: generate-question(+verify-non-disclosure)+verify-constitutional.
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Ponme una pregunta de práctica"},
    )

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    agents_selected_events = [e for e in trace["trace_events"] if e["event_type"] == "agents_selected"]
    assert len(agents_selected_events) == 2
    compositions = {
        frozenset(s["step_id"] for s in e["payload"]["activated_steps"]) for e in agents_selected_events
    }

    # Feature 001 allows only one active interactive session per instance at a time —
    # end this one before starting the next (unrelated to the composition being tested).
    app_client.post(f"/api/v1/sessions/{session_id}/end")

    # 3. A SECOND session on an activity the uploaded document is NOT authorized for →
    # guaranteed zero fragments (hard authorization boundary, Feature 002, more reliable
    # than relying on a semantic-similarity miss) → Nivel 0 skip, a structurally distinct
    # doubt_resolution composition (no `generate`/`verify-grounding` steps).
    Session = app_client.__db_sessionmaker__
    db = Session()
    other_activity = models.ActivityConfiguration(
        course_id=self_study_activity["course_id"],
        name="Otra actividad sin materiales autorizados",
        subject="Demo",
        objective="practicar autoestudio",
        mode="self_study",
        language="es",
        max_turns=10,
        max_duration_seconds=1800,
        general_knowledge_allowed=False,
        retention_policy_id=db.get(models.ActivityConfiguration, activity_id).retention_policy_id,
        **minimal_output_policy_columns(),
    )
    db.add(other_activity)
    db.commit()
    other_activity_id = other_activity.id
    db.close()
    app_client.post(
        f"/api/v1/tecnica/activities/{other_activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    configure_test_recipients(app_client, other_activity_id, recipients=("est-variety-002",))
    other_session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-variety-002", "activity_configuration_id": other_activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{other_session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )

    trace_other = app_client.get(f"/api/v1/sessions/{other_session_id}/trace").json()
    other_agents_selected = next(
        e for e in trace_other["trace_events"] if e["event_type"] == "agents_selected"
    )
    other_composition = frozenset(s["step_id"] for s in other_agents_selected["payload"]["activated_steps"])
    assert "generate" not in other_composition

    compositions.add(other_composition)
    assert len(compositions) >= 3, f"expected >=3 distinct compositions, got {compositions}"
