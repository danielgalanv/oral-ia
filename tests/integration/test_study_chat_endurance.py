"""Bounded CPU endurance: real HTTP/session logic, explicit deterministic model ports."""

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from tests.integration.test_study_chat_resume import make_client
from tests.integration.test_study_presentation_delivery import enter, turn
from tests.unit.test_study_lab import ProviderFixture, identifier


def test_twelve_question_session_preserves_exact_recent_history_and_quota_on_reentry():
    from oralia.documentary.study_lab import TrialBudget

    provider = ProviderFixture()
    provider.study_budget_profile = "study-reviewed/v1"
    provider.diagnostic_deadline_seconds = 600
    provider.trial_budget = TrialBudget(maximum=12)
    client, _, _ = make_client(provider)
    keys = []
    with client:
        enter(client)
        for index in range(12):
            key = identifier()
            keys.append(key)
            provider.text = f"FIXTURE_CPU_{index}: " + "texto " * 900
            assert turn(client, key).json()["status"] == "prepared_unverified"
            history = provider.requests[-1].conversation_history
            assert len(history) == min(index, 3) * 2
            for offset, message in enumerate(history[1::2]):
                previous = max(0, index - 3) + offset
                assert message.content == f"FIXTURE_CPU_{previous}: " + "texto " * 900
            for _ in range(2):
                assert client.post(f"/api/v1/study-lab/{key}/shown", json={}).status_code == 200
            snapshot = client.get("/api/v1/study-lab/resume").json()
            assert [row["id"] for row in snapshot["messages"]] == keys
            assert snapshot["quota"]["used"] == index + 1
        exhausted = turn(client, identifier()).json()
        assert exhausted["failure_code"] == "budget_exhausted"
        assert len(provider.requests) == 12
        client.post("/api/v1/study-lab/close", json={})
        enter(client)
        snapshot = client.get("/api/v1/study-lab/resume").json()
        assert snapshot["messages"] == [] and snapshot["quota"]["exhausted"]
        assert turn(client, identifier()).json()["failure_code"] == "budget_exhausted"
        assert len(provider.requests) == 12


def test_repeated_inflight_cancellation_never_promotes_cancelled_text_to_history():
    started, release = threading.Event(), threading.Event()

    async def wait():
        started.set()
        while not release.is_set():
            await asyncio.sleep(0.01)

    client, provider, _ = make_client(ProviderFixture(hook=wait))
    with client, ThreadPoolExecutor(max_workers=1) as pool:
        enter(client)
        for index in range(4):
            started.clear()
            key = identifier()
            future = pool.submit(turn, client, key)
            try:
                assert started.wait(5)
                assert client.post("/api/v1/study-lab/cancel", json={}).status_code == 200
            finally:
                release.set()
            assert future.result(timeout=5).json()["status"] == "cancelled"
            release.clear()
            snapshot = client.get("/api/v1/study-lab/resume").json()
            assert snapshot["messages"] == [] and snapshot["candidate"] is None
            assert snapshot["quota"]["used"] == index + 1
            assert client.post(f"/api/v1/study-lab/{key}/shown", json={}).status_code == 409
        provider.hook = None
        final = identifier()
        assert turn(client, final).json()["status"] == "prepared_unverified"
        assert provider.requests[-1].conversation_history == []
        client.post(f"/api/v1/study-lab/{final}/shown", json={})
        assert len(client.get("/api/v1/study-lab/resume").json()["messages"]) == 1
