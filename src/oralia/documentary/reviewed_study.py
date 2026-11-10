"""Session port composing the measured local generation/review loop; no model loading."""

import asyncio
import copy
import time

from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer
from oralia.course_dialogue.review_notice import build_notice, drop_corrections
from oralia.course_dialogue.review_repair import complete
from oralia.course_dialogue.structured_request import structured_request
from oralia.documentary import coverage_check
from oralia.documentary.notice_log import record_notice
from oralia.course_dialogue.web_review_references import SourceLocation, validate_locations
from oralia.course_dialogue.web_review_rounds import WebReviewRounds
from oralia.documentary.study_errors import StudyFailure
from oralia.infrastructure.generation.generation_port import GenerationOutcome


# Best-page reranker probability below which the material is declared not to cover the question. Calibrated on the
# teacher's 60 real questions (all in scope): at 0.3 three of the four refusals were wrong (scores 0.13, 0.22 and
# 0.29: the teacher wanted an answer from the related pages); only the MoSCoW question (0.04) was a right refusal.
# Off-topic and ambiguous questions score below 0.07.
MIN_RELEVANCE = 0.1
NARROWED_NOTE = "Solo he respondido a la parte de tu mensaje que trata de la asignatura."


class ReviewedStudySession:
    study_budget_profile = "study-reviewed/v1"
    diagnostic_deadline_seconds = 600

    def __init__(self, owner, revalidate):
        self.owner, self.revalidate = owner, revalidate
        self.diagnostic_label = owner.diagnostic_label
        self.last_exchange = self.last_review_trace = None
        self.partial, self.phase = "", "idle"  # text streamed so far and where the turn is (idle|generating|reviewing)
        self.locations = {}
        self.web_flow = None
        self.last_web_trace = None
        self.last_web_sources = []

    @property
    def web_enabled(self):
        if self.web_flow is None:
            return False
        try:
            self.web_flow.web.check_policy()
            return True
        except ValueError:
            return False

    def configure_web(self, web, retrieval, activity, notify):
        from oralia.documentary.study_web_flow import StudyWebFlow

        self.web_flow = StudyWebFlow(self.owner, web, retrieval, activity, self.revalidate, notify)

    @property
    def ready(self):
        return self.owner.ready

    def runtime_status(self):
        return self.owner.runtime_status()

    def bind_sources(self, locations):
        self.locations = {k: SourceLocation.model_validate(v) for k, v in copy.deepcopy(locations).items()}

    def clear_diagnostic(self):
        self.last_exchange = self.last_review_trace = None
        self.partial, self.phase = "", "idle"
        self.locations = {}
        self.last_web_trace = None
        self.last_web_sources = []
        if self.web_flow:
            self.web_flow.trace = {}
            self.web_flow.sources = []

    def guard(self):
        self.revalidate()
        if getattr(self.owner, "local_first", False) and self.web_flow is not None:
            self.web_flow.scope_guard()
        if self.web_flow and self.last_web_sources:
            self.web_flow.guard()

    async def generate(self, request):
        narrowed = False
        async with self.owner.review_lock:
            self.revalidate()
            if not self.ready:
                raise StudyFailure("model_unavailable")
            if getattr(self.owner, "local_first", False):
                if self.web_flow is None:
                    raise StudyFailure("scope_policy_required")
                try:
                    await self.web_flow.admit_local(request)
                finally:
                    self.last_web_trace = copy.deepcopy(self.web_flow.trace)
                if getattr(self.web_flow, "narrowed", None):
                    request = request.model_copy(update={"student_input": self.web_flow.narrowed})
                    narrowed = True
            relevance = getattr(request, "retrieval_relevance", None)
            if relevance is not None and relevance < MIN_RELEVANCE:
                # In scope but the retrieved pages do not answer it: say so instead of answering from weak passages.
                raise StudyFailure("material_not_covered")
            local_first = getattr(self.owner, "local_first", False) and bool(request.evidence)
            if self.web_enabled and not local_first:
                request = await self._extend(request)
            if getattr(self.owner, "local_first", False) and not request.evidence:
                raise StudyFailure("no_passages")
            if getattr(self.owner, "notice_review", False):
                outcome = await self._generate_with_notice(request)
                if narrowed and complete(outcome):
                    outcome = outcome.model_copy(
                        update={"text": NARROWED_NOTE + "\n\n" + outcome.text}
                    )
                return outcome
            trace = await self._review_once(request)
            if local_first and trace.get("status") == "unresolved_evidence_limit" and self.web_enabled:
                prior = copy.deepcopy(trace)
                request = await self._extend(request)
                if not self.last_web_sources:
                    # Do not silently override a disagreeing model or repeat the same context.
                    raise StudyFailure("review_unresolved")
                trace = await self._review_once(request, prior=prior)
            if not trace.get("diagnostic_preview"):
                raise StudyFailure("review_unresolved")
            return GenerationOutcome.model_validate(trace["versions"][-1]).model_copy(
                update={"text": trace["diagnostic_preview"]}
            )

    def _on_partial(self, text):
        self.partial = text

    async def _generate_with_notice(self, request):
        """Generate once, review once and never reject or repair: the answer is shown with a fixed notice."""
        self.guard()
        validate_locations(request.evidence, self.locations)
        actual = structured_request(
            request,
            model_profile="qwen25-14b",
            task="generate",
            didactic_profile=getattr(self.owner, "study_dialogue_profile", "study-dialogue/v4"),
        )
        self.partial, self.phase = "", "generating"
        stream = getattr(self.owner.adapter, "generate_stream", None)
        async with asyncio.timeout_at(self.owner.deadline):
            if stream is not None:
                outcome = await stream(actual, self._on_partial)  # the student reads it while it is written
            else:
                outcome = await self.owner.adapter.generate(actual)
        self.phase = "reviewing"
        self.last_exchange = copy.deepcopy(getattr(self.owner.adapter, "last_exchange", None))
        self.guard()
        if not complete(outcome):
            return outcome  # the study lab turns an incomplete generation into its own failure status
        reviewer = ConceptLedgerReviewer(
            None,
            self.owner.critic_adapter,
            budget=self.owner.review_budget,
            revalidate=self.guard,
            prompt_version="concept-ledger/v5",
        )
        try:
            async with asyncio.timeout_at(self.owner.deadline):
                trace = await reviewer.review(
                    request,
                    outcome.text,
                    web_source_ids=[key for key, location in self.locations.items() if location.url],
                )
        finally:
            self.guard()
        extra = ()
        coverage = getattr(self.owner, "coverage", None)
        if (
            coverage is not None
            and getattr(request, "retrieval_relevance", None) is not None  # self-contained question (see study_lab)
            and coverage_check.worth_checking(request.student_input)
        ):
            try:
                async with asyncio.timeout_at(self.owner.deadline):
                    if await coverage(request.student_input, [e.text for e in request.evidence]) == "NO":
                        extra = ("coverage",)
            except (TimeoutError, asyncio.TimeoutError):
                pass  # an undecided check never changes the answer
        notice = build_notice(drop_corrections(trace, request.student_input), extra)
        self.last_review_trace = dict(
            profile="notice-review/v1", status=trace["status"], review_notice=notice, reviewer=trace
        )
        record_notice(
            getattr(self.owner, "notice_log", None),
            request,
            outcome.text,
            trace,
            notice,
            model=getattr(self.owner.critic_adapter, "model_label", ""),
        )
        return outcome

    async def _extend(self, request):
        scope = copy.deepcopy(self.last_web_trace)
        try:
            request, self.locations = await self.web_flow.extend(request, self.locations)
        finally:
            self.last_web_trace = copy.deepcopy(self.web_flow.trace)
            self.last_web_sources = copy.deepcopy(self.web_flow.sources)
            if scope and scope.get("status") == "activity_scope_admitted_not_answer_verified":
                self.last_web_trace["prior_scope_check"] = scope
        return request

    async def _review_once(self, request, prior=None):
        self.guard()
        if not self.ready:
            raise StudyFailure("model_unavailable")
        # Metadata comes from checked_passages, never from text or model output.
        validate_locations(request.evidence, self.locations)
        loop = WebReviewRounds(
            self.owner.adapter,
            self.owner.critic_adapter,
            budget=self.owner.review_budget,
            revalidate=self.guard,
            generator_profile="qwen25-14b",
            critic_profile="qwen3-8b-thinking",
            generation_didactic_profile=getattr(self.owner, "study_dialogue_profile", "study-dialogue/v2"),
            repair_with_generator=True,
            stage_tokens={"generate": 1536, "review": 8192, "repair": 2048},
            stage_deadline_ms=180000,
            prompt_version=getattr(self.owner, "review_prompt_version", "web-review/v7"),
            source_locations=self.locations,
            example_probe_enabled=getattr(self.owner, "example_probe_enabled", False),
            source_terminology_guard=getattr(self.owner, "local_first", False),
        )
        try:
            async with asyncio.timeout_at(self.owner.deadline):
                trace = await loop.process(request)
            self.guard()
            if time.monotonic() >= self.owner.deadline:
                raise TimeoutError("Study runtime expired before delivery")
            return trace
        finally:
            self.last_review_trace = copy.deepcopy(loop.last_trace)
            if prior is not None and self.last_review_trace is not None:
                self.last_review_trace["prior_local_attempt"] = prior
