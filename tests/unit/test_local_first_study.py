"""CPU order/receipt tests; all model and web decisions are explicit fixtures."""

from types import SimpleNamespace

import pytest

from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.documentary.reviewed_study import ReviewedStudySession
from oralia.documentary.study_errors import StudyFailure
from oralia.infrastructure.generation.generation_port import EvidenceItem
from tests.course_dialogue.test_web_review_rounds import Provider
from tests.unit.test_reviewed_study_chat import PASS, Owner


def setup_session(critic):
    owner = Owner(Provider("FIXTURE LOCAL ANSWER", "FIXTURE EXTERNAL ANSWER"), critic)
    owner.local_first = True
    session = ReviewedStudySession(owner, lambda: None)
    item = EvidenceItem(fragment_id="local", document_id="fixture", document_version=1, text="Fixture only")
    session.bind_sources(
        {"local": SourceLocation(document_id="fixture", document_version=1, document_title="Fixture", page=1)}
    )
    request = RepairGenerationRequest(
        purpose="explicacion", instruction="Fixture", student_input="Pregunta fixture", evidence=[item]
    )
    return owner, session, request


class WebFixture:
    web = SimpleNamespace(check_policy=lambda: None)
    sources = []
    trace = {}

    def __init__(self):
        self.calls = 0

    async def admit_local(self, request):
        self.trace = {"status": "activity_scope_admitted_not_answer_verified", "fixture": True}

    async def extend(self, request, locations):
        self.calls += 1
        self.sources = [{"url": "https://example.org/fixture"}]
        self.trace = {"status": "external_ready_unverified", "fixture": True}
        external = EvidenceItem(
            fragment_id="external",
            document_id="fixture-external",
            document_version=1,
            text="Fixture external evidence only",
        )
        updated = dict(locations)
        updated["external"] = SourceLocation(
            document_id="fixture-external",
            document_version=1,
            document_title="External fixture",
            url="https://example.org/fixture",
        )
        return request.model_copy(update={"evidence": [*request.evidence, external]}), updated

    def guard(self):
        pass

    def scope_guard(self):
        pass


@pytest.mark.asyncio
async def test_local_source_is_reviewed_before_deciding_it_cannot_answer():
    owner, session, request = setup_session(Provider(PASS))
    web = WebFixture()
    session.web_flow = web
    result = await session.generate(request)
    assert result.text == "FIXTURE LOCAL ANSWER"
    assert len(owner.critic_adapter.requests) == 1
    assert web.calls == 0


@pytest.mark.asyncio
async def test_actual_insufficiency_can_extend_once_without_losing_first_attempt():
    owner, session, request = setup_session(Provider('{"status":"insufficient_evidence","issues":[]}', PASS))
    web = WebFixture()
    session.web_flow = web
    result = await session.generate(request)
    assert result.text == "FIXTURE EXTERNAL ANSWER"
    assert web.calls == 1 and len(owner.adapter.requests) == 2
    assert session.last_review_trace["prior_local_attempt"]["status"] == "unresolved_evidence_limit"


@pytest.mark.asyncio
async def test_empty_sources_still_require_web_before_academic_generation():
    owner, session, request = setup_session(Provider(PASS))

    class Refused(WebFixture):
        async def extend(self, request, locations):
            self.calls += 1
            raise StudyFailure("web_scope_uncertain")

    web = Refused()
    session.web_flow = web
    with pytest.raises(StudyFailure):
        await session.generate(request.model_copy(update={"evidence": []}))
    assert not owner.adapter.requests and web.calls == 1


@pytest.mark.asyncio
async def test_disagreeing_sufficiency_does_not_retry_the_same_local_context():
    owner, session, request = setup_session(Provider('{"status":"insufficient_evidence","issues":[]}'))

    class Unchanged(WebFixture):
        async def extend(self, request, locations):
            self.calls += 1
            self.sources = []
            self.trace = {"status": "local_sufficient"}
            return request, locations

    web = Unchanged()
    session.web_flow = web
    with pytest.raises(StudyFailure):
        await session.generate(request)
    assert len(owner.adapter.requests) == 1 and web.calls == 1
    assert session.last_review_trace["status"] == "unresolved_evidence_limit"


@pytest.mark.asyncio
async def test_outside_scope_never_calls_academic_models_and_returns_host_notice():
    from oralia.documentary.study_lab import DiagnosticStudy
    from tests.unit.test_study_lab import RetrievalFixture, identifier

    owner = Owner(Provider(), Provider())
    owner.local_first = True
    lab = DiagnosticStudy(
        RetrievalFixture(),
        owner,
        authority=lambda: True,
        budget=owner.trial_budget,
        course="fixture",
        activity="fixture",
    )

    class Outside(WebFixture):
        async def admit_local(self, request):
            self.trace = {"status": "scope_outside", "fixture": True}
            raise StudyFailure("scope_outside")

    lab.provider.web_flow = Outside()
    row = await lab.turn("Pregunta fuera del tema", identifier())
    receipt = lab.display(row["id"])
    assert receipt["non_academic_notice"] and receipt["response_kind"] == "clarification"
    assert receipt["raw_candidate"] is None and "No he encontrado esa cuestión" in receipt["diagnostic_preview"]
    assert not owner.adapter.requests and not owner.critic_adapter.requests and not lab.history
    lab.acknowledge(row["id"])
    assert len(lab.history) == 1


@pytest.mark.asyncio
async def test_unresolved_ellipsis_stops_before_the_scope_classifier():
    from oralia.documentary.study_lab import DiagnosticStudy
    from tests.unit.test_study_lab import RetrievalFixture, identifier

    owner = Owner(Provider(), Provider())
    owner.local_first = True
    lab = DiagnosticStudy(
        RetrievalFixture(),
        owner,
        authority=lambda: True,
        budget=owner.trial_budget,
        course="fixture",
        activity="fixture",
    )
    # No scope port: reaching the provider would fail, rather than fabricate a referent.
    row = await lab.turn("¿Y eso?", identifier())
    receipt = lab.display(row["id"])
    assert receipt["diagnostic_preview"] == "¿A qué concepto o ejemplo te refieres?"
    assert receipt["response_kind"] == "clarification"
    assert not owner.adapter.requests and not owner.critic_adapter.requests


@pytest.mark.asyncio
@pytest.mark.parametrize("relevance,answers", [(0.05, False), (0.099, False), (0.11, True), (0.29, True), (None, True)])
async def test_a_question_the_retrieved_pages_do_not_answer_is_declared_not_covered_without_calling_models(
    relevance, answers
):
    owner, session, request = setup_session(Provider(PASS))
    session.web_flow = WebFixture()
    request = request.model_copy(update={"retrieval_relevance": relevance})
    if answers:
        await session.generate(request)
        assert owner.adapter.requests
    else:
        with pytest.raises(StudyFailure) as raised:
            await session.generate(request)
        assert raised.value.code == "material_not_covered" and not owner.adapter.requests
        assert "no trata esto" in raised.value.detail()["message"]


@pytest.mark.asyncio
async def test_the_answer_is_readable_while_it_is_written_and_the_phase_changes_to_reviewing():
    import asyncio

    release = asyncio.Event()

    class Streaming(Provider):
        async def generate_stream(self, request, on_text):
            on_text("Un requisito")
            on_text("Un requisito es una condición.")
            await release.wait()
            return await self.generate(request)

    owner, session, request = setup_session(Provider(PASS))
    owner.adapter = Streaming("FIXTURE LOCAL ANSWER", "x")
    owner.notice_review = True
    session.web_flow = WebFixture()
    task = asyncio.create_task(session.generate(request))
    for _ in range(50):
        await asyncio.sleep(0.01)
        if session.partial:
            break
    assert (session.phase, session.partial) == ("generating", "Un requisito es una condición.")
    release.set()
    outcome = await task
    assert outcome.text == "FIXTURE LOCAL ANSWER" and session.phase == "reviewing"
    session.clear_diagnostic()
    assert (session.phase, session.partial) == ("idle", "")


@pytest.mark.asyncio
async def test_a_scope_refusal_is_logged_for_the_teacher_without_calling_models(tmp_path):
    import json

    from oralia.documentary.study_lab import DiagnosticStudy
    from tests.unit.test_study_lab import RetrievalFixture, identifier

    owner = Owner(Provider(), Provider())
    owner.local_first = True
    owner.notice_log = tmp_path / "avisos.jsonl"
    lab = DiagnosticStudy(
        RetrievalFixture(), owner, authority=lambda: True, budget=owner.trial_budget, course="fixture", activity="fixture"
    )

    class Outside(WebFixture):
        async def admit_local(self, request):
            raise StudyFailure("scope_outside")

    lab.provider.web_flow = Outside()
    await lab.turn("Pregunta fuera del tema", identifier())
    entry = json.loads((tmp_path / "avisos.jsonl").read_text(encoding="utf8"))
    assert entry["kind"] == "rechazo" and entry["notice_kinds"] == ["scope_outside"]
    assert entry["question"] == "Pregunta fuera del tema" and "No he encontrado" in entry["answer"]
