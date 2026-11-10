"""Failure test: ambos adaptadores de GenerationPort fallan de forma inesperada → la red
de seguridad genérica ya existente de execute_agency/SafeFallbackAgent (Feature 001, sin
cambios) produce una respuesta segura, turno marcado degraded/failed (research.md §2)."""

from __future__ import annotations

import pytest

from oralia.domain.agents.response_generator_agent import ResponseGeneratorAgent
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


async def _always_raise(self, request, cancellation):
    raise RuntimeError("both adapters unavailable")


@pytest.mark.failure
def test_safe_fallback_when_generation_totally_fails(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(ResponseGeneratorAgent, "execute", _always_raise)

    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution"],
        participant_code="est-total-fail-001",
        operational_fallback_allowed=True,
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-total-fail-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["output_text"]
    assert body["dialogue_action"] == "clarify"
