"""Read-only session recovery; no generation or acknowledgement is inferred from a retry."""

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from oralia.documentary.__main__ import create_app
from tests.integration.test_study_presentation_delivery import enter, turn
from tests.unit.test_study_lab import ProviderFixture, RetrievalFixture, identifier


def make_client(provider=None):
    provider = provider or ProviderFixture(text="FIXTURE CPU: original response")
    provider.diagnostic_label = "FIXTURE_CPU_RECOVERY"
    retrieval = RetrievalFixture()
    return (
        TestClient(
            create_app(
                retrieval.package,
                manifest_name="manifest-v2.json",
                retrieval=retrieval,
                study_lab=True,
                study_provider=provider,
                study_chat=True,
            ),
            base_url="http://127.0.0.1",
        ),
        provider,
        retrieval,
    )


def test_resume_restores_confirmed_and_pending_separately_without_new_calls_or_raw_data():
    client, provider, _ = make_client()
    with client:
        assert client.get("/api/v1/study-lab/resume").status_code == 401
        enter(client)
        first = identifier()
        turn(client, first)
        client.post(f"/api/v1/study-lab/{first}/shown", json={})
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 200
        second = identifier()
        turn(client, second)
        for _ in range(3):
            snapshot = client.get("/api/v1/study-lab/resume").json()
            assert [r["id"] for r in snapshot["messages"]] == [first]
            assert snapshot["candidate"]["id"] == second and not snapshot["busy"]
            assert snapshot["quota"]["used"] == 2 and len(provider.requests) == 2
            assert not {"raw_candidate", "transport", "outcome", "request"} & snapshot["candidate"].keys()
        client.post(f"/api/v1/study-lab/{second}/shown", json={})
        snapshot = client.get("/api/v1/study-lab/resume").json()
        assert [r["id"] for r in snapshot["messages"]] == [first, second]
        assert snapshot["candidate"] is None and len(provider.requests) == 2
        client.post("/api/v1/study-lab/close", json={})
        assert client.get("/api/v1/study-lab/resume").status_code == 409


def test_resume_while_generation_runs_reports_busy_and_never_exposes_partial_answer():
    started, release = threading.Event(), threading.Event()

    async def wait():
        started.set()
        while not release.is_set():
            await asyncio.sleep(0.01)

    client, provider, _ = make_client(ProviderFixture(hook=wait))
    with client, ThreadPoolExecutor(max_workers=1) as pool:
        enter(client)
        future = pool.submit(turn, client, identifier())
        try:
            assert started.wait(5)
            snapshot = client.get("/api/v1/study-lab/resume").json()
            assert snapshot["busy"] and snapshot["candidate"] is None and snapshot["messages"] == []
            assert len(provider.requests) == 1
        finally:
            release.set()
        assert future.result(timeout=5).json()["status"] == "prepared_unverified"


def test_resume_after_source_withdrawal_cannot_restore_conversation():
    client, _, retrieval = make_client()
    with client:
        enter(client)
        key = identifier()
        turn(client, key)
        client.post(f"/api/v1/study-lab/{key}/shown", json={})
        retrieval.active = False
        response = client.get("/api/v1/study-lab/resume")
        assert response.status_code == 409 and "messages" not in response.json()


def test_resume_after_runtime_expiry_returns_no_messages():
    expired = [False]
    client, provider, _ = make_client()
    provider.runtime_status = lambda: {"expired": expired[0]}
    with client:
        enter(client)
        key = identifier()
        turn(client, key)
        client.post(f"/api/v1/study-lab/{key}/shown", json={})
        expired[0] = True
        response = client.get("/api/v1/study-lab/resume")
        assert response.status_code == 410 and "messages" not in response.json()


def test_cancel_pending_recovery_preserves_confirmed_history_and_spent_quota():
    client, provider, _ = make_client()
    with client:
        enter(client)
        first, cancelled = identifier(), identifier()
        turn(client, first)
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 200
        turn(client, cancelled)
        assert client.post("/api/v1/study-lab/cancel", json={}).status_code == 200
        snapshot = client.get("/api/v1/study-lab/resume").json()
        assert [row["id"] for row in snapshot["messages"]] == [first]
        assert snapshot["candidate"] is None and not snapshot["busy"]
        assert snapshot["quota"]["used"] == 2
        assert client.post(f"/api/v1/study-lab/{cancelled}/shown", json={}).status_code == 409
        assert turn(client, identifier()).status_code == 200
        assert len(provider.requests) == 3
        assert len(provider.requests[-1].conversation_history) == 2


def test_reentry_cannot_recover_old_receipts_or_reset_spent_quota():
    client, provider, _ = make_client()
    with client:
        enter(client)
        first = identifier()
        turn(client, first)
        client.post(f"/api/v1/study-lab/{first}/shown", json={})
        assert client.post("/api/v1/study-lab/close", json={}).status_code == 200
        enter(client)
        snapshot = client.get("/api/v1/study-lab/resume").json()
        assert snapshot["messages"] == [] and snapshot["candidate"] is None
        assert snapshot["quota"]["used"] == 1
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 409
        assert len(provider.requests) == 1


def test_duplicate_send_during_generation_does_not_start_another_request():
    started, release = threading.Event(), threading.Event()

    async def wait():
        started.set()
        while not release.is_set():
            await asyncio.sleep(0.01)

    client, provider, _ = make_client(ProviderFixture(hook=wait))
    with client, ThreadPoolExecutor(max_workers=1) as pool:
        enter(client)
        first = identifier()
        future = pool.submit(turn, client, first)
        try:
            assert started.wait(5)
            assert turn(client, first).status_code == 409
            assert turn(client, identifier()).status_code == 409
            snapshot = client.get("/api/v1/study-lab/resume").json()
            assert snapshot["busy"] and snapshot["quota"]["used"] == 1
            assert len(provider.requests) == 1
        finally:
            release.set()
        assert future.result(timeout=5).status_code == 200
