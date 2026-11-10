"""CPU composition and HTTP tests; ports are explicit fixtures, never semantic evidence."""

import asyncio
import json
import time
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from oralia.course_dialogue.review_repair import CallBudget
from oralia.documentary.__main__ import create_app
from oralia.documentary.chat_context import retrieval_context
from oralia.documentary.reviewed_study import ReviewedStudySession
from oralia.documentary.study_lab import DiagnosticStudy, TrialBudget
from tests.course_dialogue.test_web_review_rounds import Provider
from tests.unit.test_study_lab import RetrievalFixture, identifier, setup

PASS = '{"status":"no_issues_found","issues":[]}'
ISSUE = json.dumps(
    {
        "status": "issues_found",
        "issues": [
            {
                "kind": "unsupported",
                "claim": "FIXTURE INITIAL",
                "explanation": "Fixture correction, no academic verdict",
                "evidence": [],
            }
        ],
    }
)


class Owner:
    """No lifespan and no loader. Used to exercise the production session composition."""

    diagnostic_label = "FIXTURE_CPU_REVIEWED_CHAIN"
    reviewed = ready = True
    study_budget_profile = "study-reviewed/v1"
    diagnostic_deadline_seconds = 600

    def __init__(self, generator, critic):
        self.adapter, self.critic_adapter = generator, critic
        self.review_budget = CallBudget(maximum=84)
        self.review_lock = asyncio.Lock()
        self.deadline = time.monotonic() + 900
        self.trial_budget = TrialBudget(maximum=12)

    def runtime_status(self):
        remaining = max(0, self.deadline - time.monotonic())
        return {
            "expires_at_unix_ms": (time.time() + remaining) * 1000,
            "remaining_seconds": remaining,
            "expired": remaining <= 0,
            "renewable": False,
        }

    def for_session(self, revalidate):
        return ReviewedStudySession(self, revalidate)


@pytest.mark.parametrize(
    "question,mode",
    [
        ("¿Por qué?", "followup"),
        ("Pon otro ejemplo", "followup"),
        ("¿Cómo comprobaríamos ese requisito?", "followup"),
        ("Acláralo", "followup"),
        ("¿Qué es la trazabilidad?", "current_question"),
        ("¿Por qué son importantes las pruebas de aceptación?", "current_question"),
    ],
)
def test_current_question_first_and_referential_followups(question, mode):
    history = [{"question": "¿Qué es un requisito funcional?", "text": "shown"}]
    result = retrieval_context(question, history)
    assert result["mode"] == mode
    assert result["references"] == ([history[0]["question"]] if mode == "followup" else [])


@pytest.mark.asyncio
async def test_missing_referent_asks_without_retrieval_or_model_and_topic_keeps_history():
    lab, retrieval, provider = setup()
    first = await lab.turn("¿Por qué?", identifier())
    assert lab.display(first["id"])["response_kind"] == "clarification"
    assert lab.budget.used == 0 and not provider.requests and not retrieval.calls
    lab.acknowledge(first["id"])
    second = await lab.turn("¿Qué es la trazabilidad?", identifier())
    assert retrieval.calls[-1][2]["history"] == []
    assert len(provider.requests[-1].conversation_history) == 2
    lab.acknowledge(second["id"])
    assert len(lab.history) == 2


@pytest.mark.asyncio
async def test_review_repair_then_delivery_is_one_question_and_four_model_calls():
    owner = Owner(Provider("FIXTURE INITIAL", "FIXTURE FINAL"), Provider(ISSUE, PASS))
    retrieval = RetrievalFixture()
    lab = DiagnosticStudy(
        retrieval, owner, authority=lambda: True, budget=owner.trial_budget, course="test", activity="test"
    )
    row = await lab.turn("Explica el requisito", identifier())
    assert row["status"] == "prepared_unverified"
    receipt = lab.display(row["id"])
    assert receipt["diagnostic_preview"] == "FIXTURE FINAL"
    assert [v["text"] for v in receipt["review_repair"]["versions"]] == ["FIXTURE INITIAL", "FIXTURE FINAL"]
    assert owner.review_budget.used == 4 and owner.trial_budget.used == 1
    assert retrieval.calls[0][1] == "rrf"
    assert not lab.history
    lab.acknowledge(row["id"])
    assert lab.history[-1]["text"] == "FIXTURE FINAL"
    assert owner.critic_adapter.requests[0].model_profile == "qwen3-8b-thinking"
    assert owner.adapter.requests[0].didactic_profile == "study-dialogue/v2"


@pytest.mark.asyncio
async def test_cancel_while_reviewing_never_delivers_initial_answer_and_keeps_budget():
    started = asyncio.Event()

    class Waiting:
        async def generate(self, request):
            started.set()
            await asyncio.Event().wait()

    owner = Owner(Provider("FIXTURE INITIAL"), Waiting())
    retrieval = RetrievalFixture()
    lab = DiagnosticStudy(
        retrieval, owner, authority=lambda: True, budget=owner.trial_budget, course="test", activity="test"
    )
    task = asyncio.create_task(lab.turn("Explica", identifier()))
    await started.wait()
    lab.cancel()
    await task
    assert not lab.history and owner.review_budget.used == 2
    assert all(r["diagnostic_preview"] is None for r in lab.receipts.values())
    assert owner.for_session(lambda: None).owner.review_budget.used == 2


def test_student_http_delivers_final_only_and_removes_diagnostics_from_display_and_receipt():
    owner = Owner(Provider("FIXTURE INITIAL", "FIXTURE FINAL"), Provider(ISSUE, PASS))
    retrieval = RetrievalFixture()
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=owner,
        study_chat=True,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        assert client.get("/api/v1/documentary").json()["study_chat"]
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        key = identifier()
        assert (
            client.post("/api/v1/study-lab/turn", json={"id": key, "question": "Explica"}).json()["status"]
            == "prepared_unverified"
        )
        for suffix in ("display", "receipt"):
            row = client.get(f"/api/v1/study-lab/{key}/{suffix}").json()
            assert row["diagnostic_preview"] == "FIXTURE FINAL"
            assert not {"raw_candidate", "outcome", "request", "transport", "review_repair"} & row.keys()
            assert set(row["retrieval"]["passages"][0]) == {"filename", "page", "original_url"}


@pytest.mark.asyncio
@pytest.mark.parametrize("fail_critic", [False, True])
async def test_two_owned_worker_lifecycle_and_partial_startup_cleanup(tmp_path, monkeypatch, fail_critic):
    import oralia.documentary.real_study_provider as module

    events = []

    @asynccontextmanager
    async def fake_cached(folder, **kwargs):
        profile = kwargs["model_prompt_profile"]
        events.append(("enter", profile))
        if profile == "qwen3-8b-thinking" and fail_critic:
            raise RuntimeError("fixture critic startup failure")
        try:
            yield SimpleNamespace(usable=True)
        finally:
            events.append(("exit", profile))

    monkeypatch.setattr(module, "cached_provider", fake_cached)
    monkeypatch.setattr(module, "gpu", lambda: {"total_mib": 32000, "used_mib": 0, "utilization_percent": 0})
    owner = module.RealStudyProvider(tmp_path / "runtime", reviewed=True, experimental_limits=True)
    original_deadline = owner.deadline
    app = SimpleNamespace(state=SimpleNamespace(request_shutdown=lambda: None))
    if fail_critic:
        with pytest.raises(RuntimeError):
            async with owner.lifespan(app):
                pytest.fail("startup should fail")
        assert ("exit", "qwen25-14b") in events
    else:
        async with owner.lifespan(app):
            assert owner.ready and owner.trial_budget.maximum == 12
        assert events[-2:] == [("exit", "qwen3-8b-thinking"), ("exit", "qwen25-14b")]
    assert not owner.ready and owner.deadline == original_deadline


def test_student_context_is_automatic_even_if_client_sends_a_manual_override():
    owner = Owner(Provider("FIXTURE FIRST", "FIXTURE SECOND"), Provider(PASS, PASS))
    retrieval = RetrievalFixture()
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=owner,
        study_chat=True,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        key = identifier()
        client.post("/api/v1/study-lab/turn", json={"id": key, "question": "¿Qué es un requisito?"})
        client.post(f"/api/v1/study-lab/{key}/shown", json={})
        result = client.post(
            "/api/v1/study-lab/turn", json={"id": identifier(), "question": "¿Por qué?", "focus_change": True}
        )
        assert result.json()["status"] == "prepared_unverified"
        assert retrieval.calls[-1][2]["history"] == ["¿Qué es un requisito?"]


class NoticeOwner(Owner):
    notice_review = True


def _verdict(kind, verdict="incorrect"):
    issue = dict(
        use_id="U1", kind=kind, card_ids=["C1"], verdict=verdict, reason="razón solo para el docente"
    )
    return json.dumps({"issues": [issue]})


@pytest.mark.asyncio
async def test_notice_mode_shows_the_answer_unchanged_with_a_fixed_notice_and_never_repairs():
    owner = NoticeOwner(Provider("Una respuesta del modelo."), Provider(_verdict("contradiction")))
    lab = DiagnosticStudy(
        RetrievalFixture(), owner, authority=lambda: True, budget=owner.trial_budget, course="t", activity="t"
    )
    row = await lab.turn("Explica el requisito", identifier())
    receipt = lab.display(row["id"])
    assert receipt["diagnostic_preview"] == "Una respuesta del modelo."  # shown, not rejected, not repaired
    assert [i["kind"] for i in receipt["review_notice"]["items"]] == ["contradiction"]
    assert "razón solo para el docente" not in json.dumps(receipt["review_notice"])
    assert len(owner.adapter.requests) == 1 and len(owner.critic_adapter.requests) == 1
    assert owner.review_budget.used == 1 and owner.trial_budget.used == 1
    lab.acknowledge(row["id"])
    assert lab.history[-1]["text"] == "Una respuesta del modelo."  # the notice never enters the history


@pytest.mark.asyncio
async def test_notice_mode_is_silent_when_clean_and_honest_when_the_review_could_not_run():
    clean = NoticeOwner(Provider("Respuesta."), Provider('{"issues":[]}'))
    lab = DiagnosticStudy(
        RetrievalFixture(), clean, authority=lambda: True, budget=clean.trial_budget, course="t", activity="t"
    )
    row = await lab.turn("Explica el requisito", identifier())
    assert lab.display(row["id"])["review_notice"] is None

    broken = NoticeOwner(Provider("Respuesta."), Provider("no es json", "tampoco"))
    lab = DiagnosticStudy(
        RetrievalFixture(),
        broken,
        authority=lambda: True,
        budget=broken.trial_budget,
        course="t",
        activity="t",
    )
    row = await lab.turn("Explica el requisito", identifier())
    receipt = lab.display(row["id"])
    assert receipt["diagnostic_preview"] == "Respuesta."
    assert [i["kind"] for i in receipt["review_notice"]["items"]] == ["not_reviewed"]


def test_student_receipt_carries_the_notice_and_nothing_from_the_reviewer_trace():
    import inspect

    from oralia.documentary.study_lab_api import install_study_lab  # noqa: F401  (whitelist lives inside)

    source = inspect.getsource(install_study_lab)
    assert (
        '"review_notice"' in source
        and '"review_repair"' not in source.split("visible_receipt")[1].split("def close")[0]
    )


def test_the_partial_endpoint_is_idle_without_a_turn_and_only_serves_the_students_own_session():
    owner = Owner(Provider("FIXTURE INITIAL", "FIXTURE FINAL"), Provider(PASS, PASS))
    retrieval = RetrievalFixture()
    app = create_app(
        retrieval.package, manifest_name="manifest-v2.json", retrieval=retrieval,
        study_lab=True, study_provider=owner, study_chat=True,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        assert client.get("/api/v1/study-lab/partial").status_code == 401  # not entered
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        assert client.get("/api/v1/study-lab/partial").json() == {"phase": "idle", "text": ""}
