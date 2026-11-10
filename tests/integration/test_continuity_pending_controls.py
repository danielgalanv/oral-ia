"""Real API negative controls: context alone is not consent, nor a grade."""

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided


def status(client, sid):
    with client.__db_sessionmaker__() as db:
        return db.get(models.Session, sid).status


def prepare(client):
    data = prepare_guided(client, screenless=True, pedagogy=True, advanced=True, continuity=True)
    sid = data["session"]["session_id"]
    return sid, f"/api/v1/sessions/{sid}/conversation-controls"


@pytest.mark.parametrize(
    "text", ["Lo confirmo.", "Confirmo terminar sin conservarlos.", "Estoy de acuerdo: finaliza."]
)
def test_confirmation_without_pending_operation_never_closes(app_client, text):
    sid, endpoint = prepare(app_client)
    r = app_client.post(endpoint, json={"text": text})
    assert r.status_code == 200 and status(app_client, sid) == "active"
    assert not app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]


@pytest.mark.parametrize("text", ["No lo confirmo.", "Di «lo confirmo».", "No quiero terminar.", "Sí."])
def test_negation_quote_or_bare_yes_never_confirms_a_close(app_client, text):
    sid, endpoint = prepare(app_client)
    assert app_client.post(endpoint, json={"text": "Quiero terminar."}).status_code == 200
    assert status(app_client, sid) == "active"
    r = app_client.post(endpoint, json={"text": text})
    assert r.status_code == 200 and status(app_client, sid) == "active"


def test_intervening_academic_request_invalidates_close_alias(app_client):
    sid, endpoint = prepare(app_client)
    app_client.post(endpoint, json={"text": "Quiero terminar."})
    r = app_client.post(endpoint, json={"text": "¿Qué significa evaporación?"})
    assert r.status_code == 200 and status(app_client, sid) == "active"
    r = app_client.post(endpoint, json={"text": "Lo confirmo."})
    assert status(app_client, sid) == "active"


def test_retained_session_must_confirm_revocation_before_separate_close(app_client):
    sid, endpoint = prepare(app_client)
    for text in ["conservar resumen y transcripción", "confirmo conservar resumen y transcripción"]:
        assert app_client.post(endpoint, json={"text": text}).status_code == 200
    assert app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]
    app_client.post(endpoint, json={"text": "Termina sin conservar resumen ni transcripción."}).json()
    assert status(app_client, sid) == "active"
    assert app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]
    app_client.post(endpoint, json={"text": "Lo confirmo."}).json()
    assert status(app_client, sid) == "active"
    assert not app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]
    app_client.post(endpoint, json={"text": "Quiero finalizar."})
    app_client.post(endpoint, json={"text": "Confirmo terminar sin conservarlos."}).json()
    assert status(app_client, sid) == "closed_voluntary"
    assert not app_client.get(f"/api/v1/sessions/{sid}/transcript").json()["turns"]


def test_mentioning_a_process_end_does_not_propose_session_closure(app_client):
    sid, endpoint = prepare(app_client)
    response = app_client.post(endpoint, json={"text": "El proceso termina cuando queda menos agua líquida."})
    assert response.status_code == 200 and status(app_client, sid) == "active"
    with app_client.__db_sessionmaker__() as db:
        context = db.get(models.CognitiveState, sid).dialogue_context
        assert not context.get("close_confirmation_pending")
    app_client.post(endpoint, json={"text": "Lo confirmo."})
    assert status(app_client, sid) == "active"


@pytest.mark.parametrize("confirmation", ["Lo confirmo.", "Confirmo.", "Confirmo el cierre."])
def test_expired_session_never_turns_natural_confirmation_into_voluntary_close(app_client, confirmation):
    from datetime import timedelta

    from oralia.infrastructure.db.timeutil import utcnow

    sid, endpoint = prepare(app_client)
    app_client.post(endpoint, json={"text": "Quiero finalizar."})
    with app_client.__db_sessionmaker__() as db:
        session = db.get(models.Session, sid)
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        session.started_at = utcnow() - timedelta(seconds=activity.max_duration_seconds + 1)
        db.commit()
    response = app_client.post(endpoint, json={"text": confirmation})
    assert response.status_code == 409
    assert status(app_client, sid) != "closed_voluntary"
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 1
    assert not app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]


def test_close_alias_cannot_grant_a_pending_positive_retention_choice(app_client):
    sid, endpoint = prepare(app_client)
    app_client.post(endpoint, json={"text": "conservar resumen y transcripción"})
    app_client.post(endpoint, json={"text": "Lo confirmo."})
    assert status(app_client, sid) == "active"
    assert not app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]
    app_client.post(endpoint, json={"text": "confirmo conservar resumen y transcripción"})
    assert app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["retain"]
