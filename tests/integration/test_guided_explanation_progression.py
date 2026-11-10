"""Integration test: `guided_explanation` progresa por `concepts_pending` con acciones
`ask`, y pasa a `respond`/`summarize` al agotarse."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_guided_explanation_asks_until_pending_exhausted_then_responds(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["guided_explanation"], participant_code="est-guided-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-guided-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Explícame paso a paso el documento de prueba"},
    ).json()
    assert first["mode"] == "guided_explanation"
    assert first["dialogue_action"] in ("ask", "respond")

    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    pending_after_first = list(state.concepts_pending)
    db.close()
    assert pending_after_first, "sample.docx yields 3 fragments — the queue MUST NOT be empty after step 1"

    actions = [first["dialogue_action"]]
    for _ in range(len(pending_after_first)):
        turn = app_client.post(
            f"/api/v1/sessions/{session_id}/study-turns",
            json={"text": "continúa"},
        ).json()
        assert turn["mode"] == "guided_explanation"
        actions.append(turn["dialogue_action"])

    assert actions[-1] in ("respond", "summarize")
    assert "ask" in actions[:-1]

    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    assert state.concepts_pending == []
    db.close()
