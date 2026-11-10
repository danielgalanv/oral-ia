"""Structured participant choices use the same guarded policy as textual controls."""

import pytest

from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_button_repeat_and_invalid_authority_are_atomic(app_client, mode):
    fixture = prepare_guided(app_client, mode=mode)
    sid = fixture["session"]["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    first = checked(
        app_client.post(
            endpoint, json={"text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else ""}
        )
    )
    repeated = checked(
        app_client.post(
            endpoint, json={"text": "", "dialogue_control": {"schema_version": 2, "action": "repeat"}}
        )
    )
    assert repeated["output_text"] == first["output_text"]
    assert repeated["dialogue_status"]["primary_act"] == "repeat"
    assert (
        app_client.post(
            endpoint,
            json={
                "text": "",
                "dialogue_control": {"schema_version": 2, "action": "repeat", "approved": True},
            },
        ).status_code
        == 422
    )
    assert (
        app_client.post(
            endpoint, json={"text": "terminar", "dialogue_control": {"schema_version": 2, "action": "repeat"}}
        ).status_code
        == 409
    )
