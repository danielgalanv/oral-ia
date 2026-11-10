"""CPU reproductions; never inspect the user's running session or infer its cause."""

import uuid

import pytest

from oralia.documentary.study_lab import HISTORY_TURNS, TrialBudget
from oralia.infrastructure.generation.generation_port import GenerationError
from tests.unit.test_study_lab import ProviderFixture, runtime_client, setup

QUESTIONS = [
    "¿Qué diferencia hay entre verificar y validar los requisitos? Explícamelo de forma sencilla.",
    "Ponme un ejemplo con una aplicación para pedir cita médica.",
    "No entiendo la diferencia en ese ejemplo. Explícamela con otras palabras.",
    "¿Cómo podría comprobar que una cita se reserva correctamente?",
    "¿Qué significa que un requisito sea realizable y comprobable? ¿Es lo mismo?",
]


async def test_exhausted_budget_has_observable_cause_without_new_generation():
    lab, _, provider = setup()
    lab.budget.maximum = 6
    lab.budget.used = 6
    result = await lab.turn(
        "¿Qué significa que un requisito sea realizable y comprobable? ¿Es lo mismo?",
        str(uuid.uuid4()),
        focus_change=True,
    )
    assert result["failure_code"] == "budget_exhausted"
    assert provider.requests == [] and lab.budget.used == 6


def test_exact_five_step_script_does_not_exhaust_six_call_quota_without_retries_and_reentry_keeps_count():
    provider = ProviderFixture()
    provider.trial_budget = TrialBudget(maximum=6)
    with runtime_client(provider) as client:
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        for index, question in enumerate(QUESTIONS):
            key = str(uuid.uuid4())
            result = client.post(
                "/api/v1/study-lab/turn", json={"id": key, "question": question, "focus_change": index == 4}
            ).json()
            assert result["status"] == "prepared_unverified"
            assert result["quota"]["remaining"] == 5 - index
            client.get(f"/api/v1/study-lab/{key}/display")
            client.post(f"/api/v1/study-lab/{key}/shown", json={})
        assert len(provider.requests[-1].conversation_history) == 2 * HISTORY_TURNS
        client.post("/api/v1/study-lab/close", json={})
        reopened = client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()
        assert reopened["quota"]["used"] == 5 and reopened["quota"]["remaining"] == 1
        key = str(uuid.uuid4())
        result = client.post(
            "/api/v1/study-lab/turn",
            json={"id": key, "question": "Synthetic sixth call; not an observed human question"},
        ).json()
        assert result["status"] == "prepared_unverified" and result["quota"]["exhausted"]
        client.post(f"/api/v1/study-lab/{key}/shown", json={})
        blocked = client.post(
            "/api/v1/study-lab/turn",
            json={"id": str(uuid.uuid4()), "question": QUESTIONS[4], "focus_change": True},
        ).json()
        assert blocked["failure_code"] == "budget_exhausted" and len(provider.requests) == 6


async def test_timeout_stops_fixture_worker_and_retries_do_not_consume_quota_or_hidden_history():
    class Worker(ProviderFixture):
        ready = True

        async def generate(self, request):
            if len(self.requests) == 1:
                self.requests.append(request)
                self.ready = False
                raise TimeoutError("synthetic deadline, no 50-second wait")
            return await super().generate(request)

    worker = Worker()
    lab, _, _ = setup(worker)
    lab.budget.maximum = 6
    first = await lab.turn(QUESTIONS[0], str(uuid.uuid4()))
    lab.acknowledge(first["id"])
    second = await lab.turn(QUESTIONS[1], str(uuid.uuid4()))
    assert second["failure_code"] == "generation_timeout" and lab.budget.used == 2
    for index in [1, 2, 3, 4]:
        result = await lab.turn(QUESTIONS[index], str(uuid.uuid4()), focus_change=index == 4)
        assert result["failure_code"] == "model_unavailable"
    assert lab.budget.used == 2 and len(worker.requests) == 2
    assert len(lab.history) == 1 and lab.history[0]["question"] == QUESTIONS[0]


@pytest.mark.parametrize(
    "kind,code",
    [
        ("retrieval", "retrieval_error"),
        ("context", "context_invalid"),
        ("transport", "transport_error"),
        ("unknown", "invalidated_unknown"),
    ],
)
async def test_failures_are_typed_without_exposing_exception_text(kind, code):
    worker = ProviderFixture()
    lab, retrieval, _ = setup(worker)
    if kind == "retrieval":

        def query(*args, **kwargs):
            raise OSError("SECRET_LOCAL_PATH")

        retrieval.query = query
    elif kind == "context":
        lab.history = [{"question": "shown", "text": "x" * 4001}]
    else:

        async def fail(request):
            raise (
                GenerationError("SECRET_LOCAL_PATH")
                if kind == "transport"
                else ValueError("SECRET_LOCAL_PATH")
            )

        worker.generate = fail
    key = str(uuid.uuid4())
    result = await lab.turn(QUESTIONS[1], key)
    assert result["failure_code"] == code
    assert "SECRET_LOCAL_PATH" not in str(result) and "SECRET_LOCAL_PATH" not in str(lab.receipt(key))


def test_source_withdrawal_has_specific_safe_api_reason():
    from fastapi.testclient import TestClient

    from oralia.documentary.__main__ import create_app
    from tests.unit.test_study_lab import RetrievalFixture

    provider = ProviderFixture()
    retrieval = RetrievalFixture()
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=provider,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        retrieval.active = False
        response = client.get("/api/v1/study-lab/state")
        assert response.status_code == 409 and response.json()["detail"]["code"] == "source_changed"
        assert provider.requests == []


def test_explicit_prepare_restores_fixture_model_without_renewing_used_quota():
    class Stopped(ProviderFixture):
        ready = False
        preparing = False

        def request_prepare(self, revalidate):
            revalidate()
            self.ready = True

    provider = Stopped()
    provider.trial_budget = TrialBudget(used=2, maximum=6)
    with runtime_client(provider) as client:
        client.post("/documentary/enter")
        opened = client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()
        assert opened["provider_ready"] is False
        prepared = client.post("/api/v1/study-lab/prepare", json={}).json()
        assert prepared["provider_ready"] and prepared["quota"]["used"] == 2
        result = client.post(
            "/api/v1/study-lab/turn", json={"id": str(uuid.uuid4()), "question": QUESTIONS[0]}
        ).json()
        assert result["status"] == "prepared_unverified" and result["quota"]["used"] == 3


async def test_source_withdrawal_remains_typed_while_purging_history():
    from oralia.documentary.study_errors import StudyFailure

    lab, retrieval, _ = setup()
    retrieval.active = False
    with pytest.raises(StudyFailure) as error:
        await lab.turn(QUESTIONS[4], str(uuid.uuid4()), focus_change=True)
    assert error.value.code == "source_changed" and lab.closed and lab.history == []


async def test_source_change_during_generation_retains_reason_without_resurrecting_receipt():
    from oralia.documentary.study_errors import StudyFailure

    lab, retrieval, provider = setup()

    async def withdraw():
        retrieval.active = False

    provider.hook = withdraw
    with pytest.raises(StudyFailure) as error:
        await lab.turn(QUESTIONS[1], str(uuid.uuid4()))
    assert error.value.code == "source_changed"
    assert lab.receipts == {} and lab.history == []


async def test_incomplete_length_has_specific_reason_and_is_not_shown():
    lab, _, _ = setup(ProviderFixture(reason="length"))
    result = await lab.turn(QUESTIONS[1], str(uuid.uuid4()))
    assert result["failure_code"] == "generation_length_limit"
    assert lab.history == [] and lab.receipt(result["id"])["diagnostic_preview"] is None
