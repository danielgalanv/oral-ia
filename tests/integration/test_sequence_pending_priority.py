"""Real pending-operation effects; a lexical confirmation grants no new scope."""

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided


def begin(client):
    prepared = prepare_guided(client, screenless=True, pedagogy=True, advanced=True, continuity=True)
    sid = prepared["session"]["session_id"]
    return sid, f"/api/v1/sessions/{sid}/conversation-controls"


def observe(client, sid):
    with client.__db_sessionmaker__() as db:
        row = db.get(models.Session, sid)
        state = db.get(models.CognitiveState, sid)
        preference = db.get(models.SessionPrivacyPreference, sid)
        return row.status, bool(preference and preference.retain), state.dialogue_context if state else {}


@pytest.mark.parametrize("confirmation", ["Confirmo.", "Confirmo el cierre.", "Lo confirmo."])
def test_single_actual_close_has_priority_over_academic_recovery(app_client, confirmation):
    sid, endpoint = begin(app_client)
    app_client.post(endpoint, json={"text": "¿Qué significa evaporación?"})
    response = app_client.post(endpoint, json={"text": "Sí. Termina sin conservar nada."})
    assert response.status_code == 200 and observe(app_client, sid)[2]["close_confirmation_pending"]
    response = app_client.post(endpoint, json={"text": confirmation})
    assert response.status_code == 200
    assert observe(app_client, sid)[:2] == ("closed_voluntary", False)


@pytest.mark.parametrize("confirmation", ["Confirmo.", "Confirmo el cierre."])
def test_confirmation_without_proposal_never_creates_close_or_retention(app_client, confirmation):
    sid, endpoint = begin(app_client)
    assert app_client.post(endpoint, json={"text": confirmation}).status_code == 200
    assert observe(app_client, sid)[:2] == ("active", False)
    app_client.post(endpoint, json={"text": "conservar resumen y transcripción"})
    app_client.post(endpoint, json={"text": confirmation})
    assert observe(app_client, sid)[:2] == ("active", False)


def test_close_specific_confirmation_cannot_confirm_a_pending_revocation(app_client):
    sid, endpoint = begin(app_client)
    for text in ["conservar resumen y transcripción", "confirmo conservar resumen y transcripción"]:
        assert app_client.post(endpoint, json={"text": text}).status_code == 200
    app_client.post(endpoint, json={"text": "Quiero terminar sin conservar nada."})
    assert observe(app_client, sid)[2]["pending_conservation"] == "none"
    app_client.post(endpoint, json={"text": "Confirmo el cierre."})
    assert observe(app_client, sid)[:2] == ("active", True)
    assert not observe(app_client, sid)[2]["close_confirmation_pending"]
    app_client.post(endpoint, json={"text": "Confirmo."})
    assert observe(app_client, sid)[:2] == ("active", False)
    assert not observe(app_client, sid)[2]["close_confirmation_pending"]
    app_client.post(endpoint, json={"text": "Quiero terminar sin conservar nada."})
    app_client.post(endpoint, json={"text": "Confirmo."})
    assert observe(app_client, sid)[:2] == ("closed_voluntary", False)


@pytest.mark.parametrize("text", ["No confirmo.", "Di «Confirmo».", "Confirmo resumen y cierre."])
def test_negation_quote_or_mixed_scope_never_confirms_pending_close(app_client, text):
    sid, endpoint = begin(app_client)
    app_client.post(endpoint, json={"text": "Quiero terminar."})
    app_client.post(endpoint, json={"text": text})
    assert observe(app_client, sid)[:2] == ("active", False)


def test_topic_confirmation_remains_a_topic_operation(app_client):
    sid, endpoint = begin(app_client)
    app_client.post(endpoint, json={"text": "elijo condensacion"})
    assert observe(app_client, sid)[2]["pending_topic_ref"] == "condensacion"
    app_client.post(endpoint, json={"text": "Confirmo."})
    status, retain, context = observe(app_client, sid)
    assert status == "active" and not retain
    assert context["current_topic_ref"] == "condensacion" and not context["pending_topic_ref"]


def test_intervening_request_invalidates_generic_close_confirmation(app_client):
    sid, endpoint = begin(app_client)
    app_client.post(endpoint, json={"text": "Quiero terminar."})
    app_client.post(endpoint, json={"text": "¿Qué significa evaporación?"})
    app_client.post(endpoint, json={"text": "Confirmo."})
    assert observe(app_client, sid)[:2] == ("active", False)


def test_pending_close_cancellation_does_not_swallow_a_source_request(app_client):
    sid, endpoint = begin(app_client)
    app_client.post(endpoint, json={"text": "¿Qué significa evaporación?"})
    app_client.post(endpoint, json={"text": "Quiero terminar."})
    response = app_client.post(endpoint, json={"text": "De dónde sale eso"})
    assert response.status_code == 200 and "sección" in response.json()["output_text"]
    assert not observe(app_client, sid)[2]["close_confirmation_pending"]
    app_client.post(endpoint, json={"text": "Confirmo."})
    assert observe(app_client, sid)[:2] == ("active", False)
