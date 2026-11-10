"""New context/receipt retention through actual public turns and closure commands."""

import json
from uuid import uuid4

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
@pytest.mark.parametrize("scope", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
@pytest.mark.parametrize("closure", ["participant", "teacher", "natural_finish"])
def test_new_context_receipts_review_export_and_erasure(app_client, mode, scope, closure):
    prepared = prepare_guided(app_client, mode=mode)
    sid = prepared["session"]["session_id"]
    choice = {"retain": bool(scope), "scope": scope}
    checked(app_client.post(f"/api/v1/sessions/{sid}/privacy", json=choice))
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    rid = str(uuid4())
    first = checked(
        app_client.post(
            endpoint,
            json={
                "text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else "",
                "client_request_id": rid,
                "closure_consent": choice,
            },
        )
    )
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.CognitiveState, sid).dialogue_context
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 1
    if closure == "natural_finish":
        checked(
            app_client.post(
                endpoint,
                json={
                    "text": "terminar la sesión",
                    "client_request_id": str(uuid4()),
                    "closure_consent": choice,
                },
            )
        )
    elif closure == "teacher":
        checked(
            app_client.post(
                f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
            )
        )
    else:
        end = (
            f"/api/v1/sessions/{sid}/study-end"
            if mode == "self_study"
            else f"/api/v1/defense-sessions/{sid}/defense-end"
        )
        checked(app_client.post(end, json=choice))
    receipt_url = f"/api/v1/sessions/{sid}/requests/{rid}"
    with app_client.__db_sessionmaker__() as db:
        session = db.get(models.Session, sid)
        assert session.status != "active" and session.active_lock_token is None
        state = db.get(models.CognitiveState, sid)
        context = state.dialogue_context if state else None
        assert bool(context) == ("transcript" in scope)
        receipts = db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count()
        assert bool(receipts) == ("transcript" in scope)
        if "transcript" not in scope:
            assert db.get(models.Turn, first["turn_id"]).output_text is None
            assert all(
                "dialogue_context" not in patch.payload
                for patch in db.query(models.StatePatch).filter_by(session_id=sid)
            )
    assert app_client.get(receipt_url).status_code == (200 if "transcript" in scope else 404)
    review = app_client.get(f"/api/v1/governance/sessions/{sid}")
    if scope:
        data = checked(review)
        assert bool(data["turns"]) == ("transcript" in scope)
        assert bool(data["summary"]) == ("summary" in scope)
        for format in ["json", "markdown"]:
            export = app_client.post(
                "/api/v1/governance/exports", json={"session_ids": [sid], "format": format}
            )
            assert export.status_code == 200, export.text
            assert "client_request_id" not in export.text and "dialogue_context" not in export.text
    else:
        assert review.status_code == 404
    first_delete = checked(
        app_client.request("DELETE", f"/api/v1/sessions/{sid}/content", json={"confirm": True})
    )
    assert (
        checked(app_client.request("DELETE", f"/api/v1/sessions/{sid}/content", json={"confirm": True}))
        == first_delete
    )
    assert app_client.get(receipt_url).status_code == 404
    assert app_client.get(f"/api/v1/sessions/{sid}/resume").status_code == 404
    late = app_client.post(endpoint, json={"text": "repite", "client_request_id": rid})
    assert late.status_code == 409
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        assert state is None or state.dialogue_context is None
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 0
        assert "dialogue_context" not in json.dumps(first_delete)


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_expired_context_and_receipts_are_hidden_then_purged(app_client, mode):
    from datetime import timedelta

    from oralia.infrastructure.db.timeutil import utcnow

    prepared = prepare_guided(app_client, mode=mode)
    sid = prepared["session"]["session_id"]
    choice = {"retain": True, "scope": ["transcript", "summary"]}
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    rid = str(uuid4())
    checked(
        app_client.post(
            endpoint,
            json={
                "text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else "",
                "client_request_id": rid,
                "closure_consent": choice,
            },
        )
    )
    end = (
        f"/api/v1/sessions/{sid}/study-end"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-end"
    )
    checked(app_client.post(end, json=choice))
    with app_client.__db_sessionmaker__() as db:
        # Labelled elapsed-time fault, confined to the synthetic test database.
        db.get(models.Session, sid).ended_at = utcnow() - timedelta(days=2)
        db.commit()
    assert app_client.get(f"/api/v1/sessions/{sid}/requests/{rid}").status_code == 404
    assert app_client.get(f"/api/v1/governance/sessions/{sid}").status_code == 404
    checked(app_client.post("/api/v1/governance/purge"))
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        assert state is None or state.dialogue_context is None
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 0
