"""Integration test: concept_review recupera desde concepts_addressed, no formula una
pregunta nueva no relacionada (SC-001)."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_concept_review_retrieves_from_concepts_addressed(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution", "concept_review"],
        participant_code="est-review-001",
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-review-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    # First, cover a concept in doubt_resolution so concepts_addressed is non-empty.
    first = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    ).json()
    assert first["dialogue_action"] == "respond"

    review = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Quiero repasar los conceptos vistos"},
    ).json()
    assert review["mode"] == "concept_review"
    # concept_review never introduces a brand-new question — it responds/acknowledges,
    # never `ask` (which would imply proposing a fresh unrelated line of inquiry).
    assert review["dialogue_action"] in ("respond", "acknowledge_missing_info")

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    review_generation = generation_events[-1]
    assert review_generation["payload"]["purpose"] == "resumen"
