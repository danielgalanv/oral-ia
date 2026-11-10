"""Injected failures are labelled; successful follow-up uses the actual provider."""

import pytest

from oralia.application.services.reviewed_unit_renderer import ReviewedUnitGenerationAdapter
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_controlled_provider_timeout_is_explicit_and_recoverable(app_client, monkeypatch, mode):
    fixture = prepare_guided(app_client, mode=mode)
    sid = fixture["session"]["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    actual = ReviewedUnitGenerationAdapter.render

    def timeout(*args, **kwargs):
        raise TimeoutError("synthetic controlled provider timeout")

    monkeypatch.setattr(ReviewedUnitGenerationAdapter, "render", timeout)
    response = checked(
        app_client.post(
            endpoint, json={"text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else ""}
        )
    )
    assert response["dialogue_status"]["effective_profile"] == "degraded"
    assert response["dialogue_status"]["notice"] == "unavailable"
    assert response["output_text"] and response["sources"] == []
    monkeypatch.setattr(ReviewedUnitGenerationAdapter, "render", actual)
    next_response = checked(
        app_client.post(
            endpoint, json={"text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else ""}
        )
    )
    assert next_response["dialogue_status"]["effective_profile"] == "guided_controlled"
    assert next_response["dialogue_status"]["rendered_unit_ids"]
