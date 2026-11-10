"""FR-008/FR-009: a full turn round-trip advances CognitiveState.version (via a chained
sequence of individually FR-009-typed patches, not a single blended one), outside the LLM."""

import pytest

from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_minimal_output_policy


@pytest.mark.integration
def test_turn_increments_cognitive_state_version(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-state001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-state001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    state_before = db.get(models.CognitiveState, sid)
    version_before = state_before.version if state_before else 0
    db.close()

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "Primer turno"})
    assert r.status_code == 200

    db = Session()
    state_after = db.get(models.CognitiveState, sid)
    assert state_after.version > version_before
    assert state_after.current_input == "Primer turno"
    assert state_after.turn_number == 1
    db.close()


@pytest.mark.integration
def test_two_turns_increment_version_twice(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-state002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-state002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r1 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "uno"})
    r2 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "dos"})

    assert r2.json()["state_version"] > r1.json()["state_version"]
