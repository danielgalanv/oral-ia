"""A real turn/teacher-close race leaves one closure and no late resurrection."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from uuid import uuid4

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_close_waits_for_transaction_then_erases_late_content(app_client, monkeypatch, mode):
    from oralia.interfaces.api.routers import oral_defense, self_study

    prepared = prepare_guided(app_client, mode=mode)
    sid = prepared["session"]["session_id"]
    module = self_study if mode == "self_study" else oral_defense
    symbol = "submit_study_turn" if mode == "self_study" else "submit_defense_turn"
    actual = getattr(module, symbol)
    prepared_turn = Event()
    release = Event()

    async def delayed(*args, **kwargs):
        result = await actual(*args, **kwargs)
        prepared_turn.set()
        assert await asyncio.to_thread(release.wait, 5)
        return result

    monkeypatch.setattr(module, symbol, delayed)
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    payload = {
        "text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else "",
        "client_request_id": str(uuid4()),
    }
    with ThreadPoolExecutor(max_workers=2) as pool:
        turn = pool.submit(app_client.post, endpoint, json=payload)
        assert prepared_turn.wait(5)
        close = pool.submit(
            app_client.post,
            f"/api/v1/governance/sessions/{sid}/close",
            json={"confirm": True, "reason": "abandoned"},
        )
        try:
            assert not close.done()
        finally:
            release.set()
        assert turn.result(timeout=10).status_code == 200
        closed = checked(close.result(timeout=10))
    assert closed["transition_won"]
    assert app_client.post(endpoint, json=payload).status_code == 409
    assert (
        checked(
            app_client.post(
                f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
            )
        )["transition_won"]
        is False
    )
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "closed_teacher_confirmed"
        assert db.get(models.Session, sid).active_lock_token is None
        state = db.get(models.CognitiveState, sid)
        assert state is None or state.dialogue_context is None
        assert db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count() == 0
        assert (
            db.query(models.TraceEvent)
            .filter_by(session_id=sid, event_type="teacher_confirmed_close")
            .count()
            == 1
        )
        assert all(turn.output_text is None for turn in db.query(models.Turn).filter_by(session_id=sid))
