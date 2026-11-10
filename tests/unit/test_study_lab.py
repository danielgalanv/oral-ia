"""Synthetic generation, real reviewed source bytes. Never validates LLM quality."""

import asyncio
import uuid

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from oralia.course_dialogue.lab_request import LabGenerationConstraints
from oralia.documentary.__main__ import PACKAGES, create_app, load_package
from oralia.documentary.study_lab import DiagnosticStudy, FixtureGenerationPort, TrialBudget
from oralia.infrastructure.generation.generation_port import GenerationOutcome


class RetrievalFixture:
    """Deterministic retrieval fixture over genuine bytes, not real dense ranking."""

    def __init__(self):
        self.package = PACKAGES["v2"][0]
        self.manifest, pages = load_package(self.package, "manifest-v2.json")
        self.pages = {
            p["id"]: {**p, "document_id": doc_id}
            for doc_id, rows in pages.items()
            for p in rows
            if p["status"] == "disponible"
        }
        self.documents = {d["id"]: d for d in self.manifest["documents"]}
        self.fingerprint = {"revision": "fixture-ranking-real-source-bytes"}
        self.active = True
        self.hook = lambda: None
        self.calls = []

    def revalidate(self):
        if not self.active:
            raise ValueError("fixture source withdrawn")

    def query(self, question, strategy, **kwargs):
        self.calls.append((question, strategy, kwargs))
        self.hook()
        p = self.pages["docente-requisitos:4"]
        doc = self.documents[p["document_id"]]
        return {
            "identity": self.fingerprint["revision"],
            "strategy": strategy,
            "sufficiency": "not_assessed",
            "candidates": [p["id"]],
            "omitted_context": [],
            "passages": [
                {
                    **p,
                    "filename": doc["filename"],
                    "source_sha256": doc["sha256"],
                    "original_url": f"/api/v1/documentary/{doc['id']}/original#page={p['page']}",
                }
            ],
        }


class ProviderFixture:
    diagnostic_label = "TEST_DOUBLE_NO_LLM"

    def __init__(self, *, reason="stop", text="Fixture <script>no ejecutar</script>", hook=None):
        self.requests = []
        self.reason, self.text, self.hook = reason, text, hook

    async def generate(self, request):
        self.requests.append(request)
        if self.hook:
            await self.hook()
        return GenerationOutcome(
            ok=self.reason == "stop", text=self.text, adapter="deterministic", finish_reason=self.reason
        )


def setup(provider=None):
    r = RetrievalFixture()
    provider = provider or ProviderFixture()
    lab = DiagnosticStudy(
        r,
        provider,
        authority=lambda: True,
        budget=TrialBudget(),
        course="test-course",
        activity="test-activity",
    )
    return lab, r, provider


def identifier():
    return str(uuid.uuid4())


def test_web_inspection_is_opt_in_gap_traced_and_never_changes_history_or_generation_quota():
    from oralia.documentary.web_evidence import (
        CuratedPublicSearch,
        PublicSource,
        WebEvidence,
        WebPolicy,
    )

    class PublicFixture:
        calls = 0

        async def fetch(self, url, **kwargs):
            self.calls += 1
            kwargs["consume"](250)
            return 200, {"content-type": "text/plain"}, b"Public unreviewed source. " * 10

    retrieval = RetrievalFixture()
    transport = PublicFixture()
    policy = WebPolicy(
        "requirements-teacher-diagnostic-v2",
        enabled=True,
        concepts=("software requirements",),
        destinations=("original.example",),
    )
    live = [policy]
    web = WebEvidence(
        policy,
        current_policy=lambda: live[0],
        acquisition=transport,
        search=CuratedPublicSearch(
            {
                "software requirements": (
                    PublicSource("https://original.example/", "Original", "Original entity"),
                )
            }
        ),
    )
    provider = ProviderFixture()
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=provider,
        web_evidence=web,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        opened = client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()
        assert opened["web"]["enabled"]
        key = identifier()
        client.post("/api/v1/study-lab/turn", json={"id": key, "question": "Local question"})
        client.get(f"/api/v1/study-lab/{key}/display")
        client.post(f"/api/v1/study-lab/{key}/shown")
        body = {
            "id": identifier(),
            "local_receipt": key,
            "concept": "software requirements",
            "confirmed_in_scope_gap": True,
            "notice_shown": True,
        }
        assert (
            client.post("/api/v1/study-lab/web-inspect", json={**body, "notice_shown": False}).status_code
            == 409
        )
        result = client.post("/api/v1/study-lab/web-inspect", json=body).json()
        assert result["status"] == "acquired_unreviewed"
        assert result["decision"]["local_receipt"] == key
        assert result["decision"]["assessor"] == "teacher_diagnostic_attestation"
        assert len(result["review"]["teacher_pages_reviewed"]) > 1
        assert result["review"]["approved_content"] == [] and not result["publication_allowed"]
        assert len(provider.requests) == transport.calls == 1
        assert client.post("/api/v1/study-lab/web-inspect", json=body).status_code == 409
        assert transport.calls == 1
        live[0] = None
        assert not client.get("/api/v1/study-lab/state").json()["web"]["enabled"]
        assert not web.cache and not web.receipts[body["id"]]["documents"]
        follow = client.post(
            "/api/v1/study-lab/turn", json={"id": identifier(), "question": "Continue locally"}
        )
        assert follow.json()["quota"]["used"] == 2
        assert len(provider.requests[-1].conversation_history) == 2
        assert "Public unreviewed" not in str(provider.requests[-1])


@pytest.mark.asyncio
async def test_real_source_bytes_reach_port_and_only_acknowledged_text_reaches_history():
    lab, retrieval, provider = setup()
    first = await lab.turn("¿Qué es un requisito?", identifier())
    request = provider.requests[0]
    assert request.constraints.deadline_ms == 50000
    assert request.constraints.max_tokens == 768
    assert request.general_knowledge_allowed is False
    assert retrieval.pages["docente-requisitos:4"]["text"] in request.evidence[0].text
    assert "SHA256 original:" in request.evidence[0].text
    assert request.evidence[0].document_id.startswith(retrieval.manifest["package_id"] + "/")
    assert lab.history == []
    row = lab.display(first["id"])
    assert row["semantic_support"] == "unverified" and row["sufficiency"] == "not_assessed"
    assert row["participant_display"] is None and row["publication_allowed"] is False
    with pytest.raises(ValueError, match="pendiente"):
        await lab.turn("seguimiento no mostrado", identifier())
    lab.acknowledge(first["id"])
    await lab.turn("Acláralo", identifier())
    assert provider.requests[1].conversation_history[-1].content == row["diagnostic_preview"]
    assert retrieval.calls[-1][2]["history"] == ["¿Qué es un requisito?"]


@pytest.mark.asyncio
@pytest.mark.parametrize("when", ["before", "retrieval", "provider", "display", "ack"])
async def test_source_withdrawal_blocks_at_every_boundary(when):
    lab, r, p = setup()
    if when == "before":
        r.active = False
        with pytest.raises(ValueError):
            await lab.turn("test", identifier())
    elif when == "retrieval":
        r.hook = lambda: setattr(r, "active", False)
        with pytest.raises(ValueError):
            await lab.turn("test", identifier())
    else:
        if when == "provider":

            async def withdraw():
                r.active = False

            p.hook = withdraw
            with pytest.raises(ValueError):
                await lab.turn("test", identifier())
        else:
            row = await lab.turn("test", identifier())
            if when == "ack":
                lab.display(row["id"])
            r.active = False
            with pytest.raises(ValueError):
                (lab.display if when == "display" else lab.acknowledge)(row["id"])
    assert lab.history == [] and lab.receipts == {}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reason,text", [("length", "truncado"), ("deadline", "tarde"), ("stop", ""), ("stop", "x" * 4001)]
)
async def test_incomplete_or_invalid_candidate_is_raw_only(reason, text):
    lab, _, _ = setup(ProviderFixture(reason=reason, text=text))
    row = await lab.turn("test", identifier())
    assert row["status"] in {"incomplete_candidate", "oversized_candidate"}
    receipt = lab.receipt(row["id"])
    assert receipt["raw_candidate"] == text and receipt["diagnostic_preview"] is None
    assert lab.history == []
    with pytest.raises(ValueError):
        lab.acknowledge(row["id"])


@pytest.mark.asyncio
@pytest.mark.parametrize("close", [False, True])
async def test_late_provider_suppressing_cancel_cannot_deliver(close):
    started = asyncio.Event()

    async def slow():
        started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass  # deliberately misbehaving fixture

    lab, _, _ = setup(ProviderFixture(hook=slow))
    task = asyncio.create_task(lab.turn("test", identifier()))
    await asyncio.wait_for(started.wait(), timeout=2)
    with pytest.raises(ValueError, match="Ocupado"):
        await lab.turn("concurrente", identifier())
    if close:
        lab.close()
        with pytest.raises(ValueError, match="cerrada"):
            await task
        assert lab.receipts == {}
    else:
        lab.cancel()
        result = await task
        assert result["status"] == "cancelled"
        assert lab.receipt(result["id"])["diagnostic_preview"] is None
    assert lab.history == []


@pytest.mark.asyncio
async def test_timeout_even_when_provider_suppresses_cancellation():
    async def slow():
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    lab, _, _ = setup(ProviderFixture(hook=slow))
    lab.budget.remaining = lambda: 0.05
    row = await lab.turn("test", identifier())
    assert row["status"] == "timeout"
    assert lab.receipt(row["id"])["diagnostic_preview"] is None
    assert lab.history == []


@pytest.mark.asyncio
async def test_duplicate_error_recovery_focus_change_and_global_budget():
    calls = 0

    async def fail_once():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("fixture error")

    lab, _, p = setup(ProviderFixture(hook=fail_once))
    first = await lab.turn("test", identifier())
    assert first["status"] == "provider_error"
    with pytest.raises(ValueError, match="duplicada"):
        await lab.turn("test", first["id"])
    second = await lab.turn("segunda", identifier())
    lab.acknowledge(second["id"])
    third = await lab.turn("nuevo tema", identifier(), focus_change=True)
    assert len(p.requests[-1].conversation_history) == 2
    lab.acknowledge(third["id"])
    assert lab.history[-1] == {"question": "nuevo tema", "text": p.text} and len(lab.history) == 2
    lab.budget.used = 8
    row = await lab.turn("novena", identifier())
    assert row["status"] == "invalidated"
    assert len(p.requests) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["text", "source_sha256", "document_id", "original_url"])
async def test_foreign_passages_never_reach_provider(field):
    lab, r, p = setup()
    query = r.query

    def foreign(*args, **kwargs):
        result = query(*args, **kwargs)
        result["passages"][0][field] = "foreign"
        return result

    r.query = foreign
    row = await lab.turn("test", identifier())
    assert row["status"] == "invalidated" and p.requests == []


def test_fifty_exact_and_sixty_rejected():
    assert LabGenerationConstraints(deadline_ms=50000, max_tokens=768).deadline_ms == 50000
    with pytest.raises(ValidationError):
        LabGenerationConstraints(deadline_ms=60000, max_tokens=768)


@pytest.mark.asyncio
async def test_existing_cached_adapter_serializes_v2_request_with_exact_budget():
    from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
    from oralia.course_dialogue.lab_request import LabGenerationRequest
    from tests.course_dialogue.test_cached_adapter import Process

    lab, _, _ = setup()
    result = await lab.turn("test", identifier())
    request = LabGenerationRequest.model_validate(lab.receipt(result["id"])["request"])
    pipe = Process()  # fake pipe, no worker executable or weights
    adapter = CachedTransformersGenerationAdapter(pipe)
    await adapter.generate(request)
    assert pipe.payload["deadline_ms"] == 50000
    assert pipe.payload["max_tokens"] == 768
    assert request.evidence[0].text in pipe.payload["messages"][-1]["content"]
    assert adapter.last_exchange["token_budget"]["status"] == "accepted"


@pytest.mark.asyncio
async def test_cancel_prepared_candidate_prevents_display_and_history():
    lab, _, _ = setup()
    row = await lab.turn("test", identifier())
    lab.cancel()
    with pytest.raises(ValueError):
        lab.display(row["id"])
    assert lab.receipt(row["id"])["diagnostic_preview"] is None
    assert lab.history == []


@pytest.mark.asyncio
async def test_disconnected_provider_never_retrieves_or_loads_model():
    lab, r, _ = setup()
    lab.provider = None
    with pytest.raises(ValueError, match="no conectado"):
        await lab.turn("test", identifier())
    assert r.calls == [] and lab.budget.used == 0


@pytest.mark.asyncio
async def test_expired_inspection_lease_purges_content_without_new_model_call():
    lab, _, p = setup()
    result = await lab.turn("test", identifier())
    lab.acknowledge(result["id"])
    lab.lease_seconds = 15
    lab.last_seen -= 16
    with pytest.raises(ValueError, match="heartbeat"):
        lab.validate()
    assert not lab.history and not lab.receipts and len(p.requests) == 1


@pytest.mark.asyncio
async def test_adapter_transport_copy_is_ephemeral_and_purged_on_close():
    lab, _, provider = setup()
    provider.last_exchange = {"raw_worker_response": "sensitive fixture text"}
    row = await lab.turn("test", identifier())
    assert lab.receipt(row["id"])["transport"]["raw_worker_response"] == "sensitive fixture text"
    assert provider.last_exchange is None
    lab.close()
    assert lab.receipts == {} and provider.last_exchange is None


def test_http_consent_isolation_close_reentry_and_historical_profile():
    r = RetrievalFixture()
    app = create_app(
        r.package,
        manifest_name="manifest-v2.json",
        retrieval=r,
        study_lab=True,
        study_provider=FixtureGenerationPort(),
    )
    with TestClient(app, base_url="http://127.0.0.1") as a:
        b = TestClient(app, base_url="http://127.0.0.1")
        assert a.get("/api/v1/study-lab/state").status_code == 401
        a.post("/documentary/enter")
        assert (
            a.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": False}).status_code == 403
        )
        assert (
            a.post(
                "/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True, "course": "foreign"}
            ).status_code
            == 422
        )
        assert (
            a.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).status_code == 200
        )
        key = identifier()
        assert (
            a.post("/api/v1/study-lab/turn", json={"id": key, "question": "test"}).json()["status"]
            == "prepared_unverified"
        )
        b.post("/documentary/enter")
        b.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        assert b.get(f"/api/v1/study-lab/{key}/receipt").status_code == 409
        assert a.get(f"/api/v1/study-lab/{key}/display").json()["semantic_support"] == "unverified"
        assert a.post("/api/v1/sessions").status_code == 405
        assert (
            a.post("/api/v1/study-lab/cancel", headers={"Origin": "https://foreign.test"}).status_code == 403
        )
        a.post("/documentary/leave")
        assert a.get(f"/api/v1/study-lab/{key}/receipt").status_code == 401
        a.post("/documentary/enter")
        a.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        assert a.get(f"/api/v1/study-lab/{key}/receipt").status_code == 409
        r.active = False
        assert (
            a.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).status_code == 409
        )
    with TestClient(
        create_app(r.package, manifest_name="manifest-v2.json"), base_url="http://127.0.0.1"
    ) as c:
        c.post("/documentary/enter")
        assert c.post("/api/v1/study-lab/open", json={}).status_code == 405


def test_package_root_and_manifest_cannot_be_substituted(tmp_path):
    r = RetrievalFixture()
    r.package = tmp_path
    with pytest.raises(ValueError, match="root"):
        create_app(PACKAGES["v2"][0], manifest_name="manifest-v2.json", retrieval=r, study_lab=True)


class RuntimeProviderFixture(ProviderFixture):
    """Fake global clock, no service, model or GPU."""

    def __init__(self, clock, **kwargs):
        super().__init__(**kwargs)
        self.clock = clock
        self.deadline = 160

    def runtime_status(self):
        remaining = max(0, self.deadline - self.clock[0])
        return {
            "expires_at_unix_ms": 160000,
            "remaining_seconds": remaining,
            "expired": remaining <= 0,
            "renewable": False,
        }


def runtime_client(provider):
    retrieval = RetrievalFixture()
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=provider,
    )
    return TestClient(app, base_url="http://127.0.0.1")


def test_runtime_deadline_visible_and_never_renewed_by_state_or_reentry():
    clock = [100]
    provider = RuntimeProviderFixture(clock)
    with runtime_client(provider) as client:
        client.post("/documentary/enter")
        assert client.get("/api/v1/documentary").json()["study_runtime"]["remaining_seconds"] == 60
        opened = client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()
        assert opened["runtime"]["renewable"] is False and opened["inspection_lease_seconds"] == 15
        for tick in [110, 125, 140, 159]:
            clock[0] = tick
            state = client.get("/api/v1/study-lab/state").json()
            assert state["runtime"]["remaining_seconds"] == 160 - tick
            assert state["runtime"]["expires_at_unix_ms"] == 160000
        client.post("/api/v1/study-lab/close", json={})
        assert (
            client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()[
                "runtime"
            ]["remaining_seconds"]
            == 1
        )
        clock[0] = 160
        for method, path, body in [
            ("get", "state", None),
            ("post", "open", {"ephemeral_inspection_consent": True}),
            ("post", "turn", {"id": identifier(), "question": "no transportar"}),
            ("post", "prepare", {}),
        ]:
            kwargs = {} if body is None else {"json": body}
            response = getattr(client, method)(f"/api/v1/study-lab/{path}", **kwargs)
            assert response.status_code == 410 and response.json()["detail"]["code"] == "runtime_expired"
        assert provider.requests == []


def test_expiry_during_generation_never_exposes_candidate_or_receipt():
    clock = [100]

    async def expire():
        clock[0] = 160

    provider = RuntimeProviderFixture(clock, hook=expire)
    with runtime_client(provider) as client:
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        key = identifier()
        response = client.post("/api/v1/study-lab/turn", json={"id": key, "question": "pendiente"})
        assert response.status_code == 410 and "diagnostic_preview" not in response.json()
        assert len(provider.requests) == 1
        assert client.get(f"/api/v1/study-lab/{key}/display").status_code == 410
        assert client.get(f"/api/v1/study-lab/{key}/receipt").status_code == 410


def test_inspection_lease_is_distinct_from_global_runtime(monkeypatch):
    from types import SimpleNamespace

    import oralia.documentary.study_lab as lab_module
    import oralia.documentary.study_lab_api as api_module

    clock = [100]
    monkeypatch.setattr(lab_module, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    monkeypatch.setattr(api_module, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    provider = RuntimeProviderFixture(clock)
    with runtime_client(provider) as client:
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        clock[0] = 116
        response = client.get("/api/v1/study-lab/state")
        assert response.status_code == 409 and response.json()["detail"]["code"] == "lease_expired"
        assert provider.runtime_status()["remaining_seconds"] == 44
        assert (
            client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).status_code
            == 200
        )


def test_a_long_question_with_its_own_context_is_not_taken_for_a_follow_up():
    from oralia.documentary.chat_context import referential

    assert referential("Explícame ese ejemplo")  # short: it points to the previous turn
    assert not referential(
        "Si un sistema tiene que funcionar tanto en Windows como en Linux, ¿cómo clasificaríamos ese requisito?"
    )
