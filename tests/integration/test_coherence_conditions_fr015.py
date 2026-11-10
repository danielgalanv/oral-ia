"""Integration test: demuestra detección real (no solo configurabilidad) y
recovery_action correcto para las 5 condiciones de FR-015 aún sin prueba conductual:
perdida_objetivo, exceso_turnos_mismo_concepto, fallo_agente, latencia_excesiva,
ausencia_progreso — usa los umbrales ya definidos en research.md §5/config.py, sin fijar
cifras nuevas — [Remediación E5/MEDIUM — FR-015]."""

from __future__ import annotations

import pytest

from oralia.domain.agents.response_generator_agent import ResponseGeneratorAgent
from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


def _incident_types(app_client, session_id) -> list[tuple[str, str]]:
    Session = app_client.__db_sessionmaker__
    db = Session()
    incidents = (
        db.query(models.CoherenceIncident).filter(models.CoherenceIncident.session_id == session_id).all()
    )
    db.close()
    return [(i.incident_type, i.recovery_action) for i in incidents]


@pytest.mark.integration
def test_fallo_agente_detected_with_recovery_action(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    async def _raise(self, request, cancellation):
        raise RuntimeError("simulated agent failure")

    monkeypatch.setattr(ResponseGeneratorAgent, "execute", _raise)
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-fr015-fallo"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-fr015-fallo", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué contiene el documento?"}
    )
    incidents = _incident_types(app_client, session_id)
    assert ("fallo_agente", "finalizar_de_forma_segura") in incidents


@pytest.mark.integration
def test_latencia_excesiva_detected_with_recovery_action(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    async def _timeout(self, request, cancellation):
        raise TimeoutError("simulated timeout")

    monkeypatch.setattr(ResponseGeneratorAgent, "execute", _timeout)
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-fr015-latencia"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-fr015-latencia", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué contiene el documento?"}
    )
    incidents = _incident_types(app_client, session_id)
    assert ("latencia_excesiva", "reducir_respuesta") in incidents


@pytest.mark.integration
def test_exceso_turnos_mismo_concepto_detected(app_client, self_study_activity):
    # sample.docx yields 3 fragments — guided_explanation's per-turn rotation
    # (T039/T068) exhausts the queue after 3 turns; a 4th turn on the same concept
    # (concepts_addressed stuck at 1 item) MUST trigger exceso_turnos_mismo_concepto
    # (ORALIA_COHERENCE_NO_PROGRESS_WINDOW, default 3 — no new threshold introduced here).
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["guided_explanation"], participant_code="est-fr015-exceso"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-fr015-exceso", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Explícame paso a paso el documento de prueba"},
    )
    for _ in range(3):
        app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "continúa"})

    incidents = _incident_types(app_client, session_id)
    assert any(t == "exceso_turnos_mismo_concepto" and r == "pedir_aclaracion" for t, r in incidents)


@pytest.mark.integration
def test_ausencia_progreso_detected(app_client, self_study_activity):
    # presentation_preparation's ask/re_ask pattern (T058) never marks a concept as
    # addressed (dialogue_action is always ask/re_ask, never respond), so
    # concepts_addressed stays empty across turns — ausencia_progreso MUST fire once
    # turn_number reaches ORALIA_COHERENCE_NO_PROGRESS_WINDOW (default 3).
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["presentation_preparation"], participant_code="est-fr015-ausencia"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-fr015-ausencia", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    for _ in range(4):
        app_client.post(
            f"/api/v1/sessions/{session_id}/study-turns",
            json={"text": "Quiero preparar una exposición sobre el documento de prueba"},
        )

    incidents = _incident_types(app_client, session_id)
    assert any(t == "ausencia_progreso" and r == "reformular" for t, r in incidents)


@pytest.mark.integration
def test_perdida_objetivo_detected_near_session_limit(app_client, self_study_activity):
    # A small max_turns activity so the "near the session limit" signal (research.md
    # §5) triggers quickly, distinct from FR-020's own session-close limit.
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, self_study_activity["activity_id"])
    activity.max_turns = 2
    db.add(activity)
    db.commit()
    db.close()

    # presentation_preparation rotates evidence per turn (T039/T068 shared mechanism)
    # so back-to-back turns MUST NOT trigger a spurious repetition incident here.
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["presentation_preparation"], participant_code="est-fr015-perdida"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-fr015-perdida", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Quiero preparar una exposición sobre el documento de prueba"},
    )
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Sigue estructurando la exposición"},
    )

    incidents = _incident_types(app_client, session_id)
    assert any(t == "perdida_objetivo" and r == "reducir_respuesta" for t, r in incidents)
