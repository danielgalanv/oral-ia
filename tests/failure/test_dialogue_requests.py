"""Public request identity: actual controlled turns, no generator replacement."""

from uuid import uuid4

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_request_retries_conflicts_and_owner_only_reconciliation(app_client, mode):
    prepared = prepare_guided(app_client, mode=mode)
    sid = prepared["session"]["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    rid = str(uuid4())
    payload = {
        "text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else "",
        "client_request_id": rid,
    }
    first = checked(app_client.post(endpoint, json=payload))
    repeated = checked(app_client.post(endpoint, json=payload))
    assert repeated["turn_id"] == first["turn_id"]
    assert repeated["output_text"] == first["output_text"]
    assert app_client.post(endpoint, json={**payload, "text": "otro contenido"}).status_code == 409
    assert (
        app_client.post(
            endpoint, json={**payload, "closure_consent": {"retain": True, "scope": ["transcript"]}}
        ).status_code
        == 409
    )
    receipt_url = f"/api/v1/sessions/{sid}/requests/{rid}"
    reconciled = checked(app_client.get(receipt_url))
    assert reconciled["status"] == "completed"
    assert reconciled["turn_id"] == first["turn_id"]
    assert "text" not in reconciled and "payload_sha256" not in reconciled
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 1
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 1
    assert app_client.get(f"/api/v1/sessions/{sid}/requests/{uuid4()}").status_code == 404
    app_client.cookies.clear()
    assert app_client.get(receipt_url).status_code == 401
    checked(app_client.post("/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}))
    assert app_client.get(receipt_url).status_code == 403


def test_retired_unit_does_not_reappear_on_request_retry(app_client):
    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    payload = {"text": "¿A qué temperatura hierve el agua?", "client_request_id": str(uuid4())}
    first = checked(app_client.post(endpoint, json=payload))
    unit_id = first["dialogue_status"]["rendered_unit_ids"][0]
    checked(app_client.post(f"/api/v1/governance/teaching-units/{unit_id}/retire"))
    retried = checked(app_client.post(endpoint, json=payload))
    assert retried["turn_id"] == first["turn_id"]
    assert retried["output_text"] is None and retried["replay_content_withheld"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 1


def test_failed_turn_rolls_back_receipt_and_can_retry_same_identity(app_client, monkeypatch):
    from oralia.interfaces.api.routers import self_study

    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    payload = {"text": "¿A qué temperatura hierve el agua?", "client_request_id": str(uuid4())}
    actual = self_study.submit_study_turn

    async def fail_after_real_result(*args, **kwargs):
        await actual(*args, **kwargs)
        raise ValueError("synthetic transport-boundary failure before commit")

    monkeypatch.setattr(self_study, "submit_study_turn", fail_after_real_result)
    assert app_client.post(endpoint, json=payload).status_code == 409
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 0
        assert db.query(models.Turn).filter_by(session_id=sid).count() == 0
        assert db.get(models.Session, sid).turn_count == 0
    monkeypatch.setattr(self_study, "submit_study_turn", actual)
    checked(app_client.post(endpoint, json=payload))


def test_concurrent_identical_requests_commit_one_turn_without_blocking_loop(app_client, monkeypatch):
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from oralia.interfaces.api.routers import self_study

    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    payload = {"text": "¿A qué temperatura hierve el agua?", "client_request_id": str(uuid4())}
    actual = self_study.submit_study_turn

    async def delayed(*args, **kwargs):
        await asyncio.sleep(0.05)  # Labelled scheduling fault; actual services still execute.
        return await actual(*args, **kwargs)

    monkeypatch.setattr(self_study, "submit_study_turn", delayed)
    barrier = Barrier(2)

    def send():
        barrier.wait(timeout=5)
        return checked(app_client.post(endpoint, json=payload))

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(send) for _ in range(2)]
        results = [future.result(timeout=15) for future in futures]
    assert results[0]["turn_id"] == results[1]["turn_id"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 1
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 1


def test_cancelled_interpreter_rolls_back_turn_and_releases_operation(app_client, monkeypatch):
    import asyncio

    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    payload = {"text": "¿A qué temperatura hierve el agua?", "client_request_id": str(uuid4())}
    actual = StudyIntentInterpreterAgent.execute

    async def cancelled(*args, **kwargs):
        raise asyncio.CancelledError()

    monkeypatch.setattr(StudyIntentInterpreterAgent, "execute", cancelled)
    assert app_client.post(endpoint, json=payload).status_code == 409
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 0
        assert db.get(models.Session, sid).turn_count == 0
    monkeypatch.setattr(StudyIntentInterpreterAgent, "execute", actual)
    checked(app_client.post(endpoint, json=payload))
