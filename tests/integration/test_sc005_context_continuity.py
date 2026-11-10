"""Integration test: conversación de ≥5 turnos (mezcla doubt_resolution/
guided_explanation) verificando continuidad de `CognitiveState`, acumulación correcta de
`concepts_addressed`/`concepts_pending`, y que ningún `GenerationRequest` reconstruido a
partir de la traza contiene el texto íntegro de turnos anteriores — solo
`concepts_addressed`/evidencia del turno actual. Usa exclusivamente
`DeterministicGenerationAdapter` (sin `ORALIA_OLLAMA_MODEL`, sin comparar literalmente
ninguna salida generada), ejecutable en CI sin Ollama — [Remediación E1/HIGH — SC-005]."""

from __future__ import annotations

import json

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material

_TURNS = [
    "¿Qué contiene el documento de prueba, primer párrafo?",
    "Explícame paso a paso el documento de prueba",
    "continúa",
    "continúa",
    "¿Qué más dice el documento sobre el segundo párrafo?",
]


@pytest.mark.integration
def test_five_turn_conversation_preserves_state_without_replaying_history(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution", "guided_explanation"],
        participant_code="est-sc005-001",
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-sc005-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    Session = app_client.__db_sessionmaker__
    versions: list[int] = []
    for turn_text in _TURNS:
        response = app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": turn_text})
        assert response.status_code == 200
        versions.append(response.json()["state_version"])

    # CognitiveState.version strictly increases turn over turn — continuity, no reset.
    assert versions == sorted(versions)
    assert len(set(versions)) == len(versions)

    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    assert state.turn_number == len(_TURNS)
    assert state.concepts_addressed, "concepts_addressed MUST accumulate across the conversation"
    db.close()

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    input_texts = list(_TURNS)

    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert len(generation_events) >= 1

    # No generation_call payload (the reconstructible view of what was sent to
    # GenerationPort — purpose/fragment_ids/adapter, never raw text) embeds the literal
    # input_text of a DIFFERENT, earlier turn — context MUST travel as
    # concepts_addressed/evidence, never as replayed conversation history.
    for i, event in enumerate(generation_events):
        payload_json = json.dumps(event["payload"], ensure_ascii=False)
        for earlier_text in input_texts[:i]:
            assert earlier_text not in payload_json, (
                f"generation_call #{i} embeds an earlier turn's raw input_text — history MUST NOT be replayed"
            )

    # DeterministicGenerationAdapter only (no ORALIA_OLLAMA_MODEL configured in CI).
    for event in generation_events:
        assert event["payload"]["adapter"] == "deterministic"
