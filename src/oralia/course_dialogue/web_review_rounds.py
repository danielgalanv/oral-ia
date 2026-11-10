"""Opt-in laboratory revision loop. Model agreement is never publication authority.

Uses the existing structured renderer, witnessed issues, call budget and executor.
No model loader, network activation, source approval or participant route lives here.
"""

import asyncio
import json
from typing import Literal

from pydantic import Field, model_validator

from oralia.course_dialogue.academic_presentation import present_academic_answer
from oralia.course_dialogue.model_prompt_profiles import STUDY_PROFILES, data_json
from oralia.course_dialogue.review_repair import (
    AdvisoryReview,
    ReviewRepairGenerationAdapter,
    complete,
    parse_review,
    quote_in,
)
from oralia.course_dialogue.structured_request import StructuredGenerationRequest, structured_request
from oralia.course_dialogue.web_review_prompts import role_policy
from oralia.course_dialogue.web_review_references import (
    SourceLocation,
    parse_minimal_reference_review,
    parse_reference_review,
    readable_references,
    validate_locations,
)

WEB_RULES = """
Teacher and Internet sources have distinct provenance, indicated by document_id.
First check whether an attributed external statement is actually sustained by its
source in context. Then compare its substantive proposition with a concrete teacher
statement ABOUT THE SAME CONDITIONS AND SCOPE. A correct 'NASA says X' attribution
can be supported even if X conflicts with a teacher proposition. Do not label the
attribution unsupported merely because the teacher disagrees. Absence of evidence
is not contradiction; different terminology is not contradiction by itself.
A response can accurately explain a discrepancy and leave it unresolved: that is
an acceptable limit, not a reason to silently replace the teacher or discard all
valid parts. Do not claim feasibility or achievement from hypothetical numbers.
Do not reject style, length, repetition, nonessential omissions or coherent fiction.
"""

WEB_REVIEW = """
You are the critic, not the answer generator. Check only substantive defects.
Return ONLY this JSON schema, no prose outside it:
{"status":"issues_found|no_issues_found|insufficient_evidence",
 "external_support":"supported|rejected|unknown|not_used",
 "teacher_compatibility":"compatible|conflict|unknown",
 "response_action":"explanation|limit|repair", "issues":[]}
Each issue uses exactly: kind (contradiction/unsupported/coverage/ambiguity/overclaim),
claim (short EXACT quote from the draft), explanation (concrete objection), evidence
(list of up to two objects {source_id,quote}, exact short quotes from sources).
Use actual fragment_id for source_id. Report at most two important issues.
Unsupported can have no witness when the missing premise is precisely identified.
For any contradiction cite the teacher proposition, not just the external text.
An accurately attributed discrepancy already made explicit is not a draft defect.
If the draft states the appropriate uncertainty, do not demand invented evidence.
no_issues_found means no objections found by this critic, never semantic approval.
Use response_action=repair only with issues_found. A well explained discrepancy or
acknowledged lack of evidence can be no_issues_found with response_action=limit.
"""


class WebRoundRequest(StructuredGenerationRequest):
    """Registered experimental messages, preserving all existing source/data escaping."""

    format_reminder: bool = False
    source_locations: dict[str, SourceLocation] = Field(default_factory=dict)
    prompt_version: Literal[
        "web-review/v1",
        "web-review/v2",
        "web-review/v3",
        "web-review/v4",
        "web-review/v5",
        "web-review/v6",
        "web-review/v7",
        "web-review/v8",
        "web-review/v9",
        "web-review/v10",
    ] = "web-review/v1"

    def effective_messages(self):
        messages = super().effective_messages()
        if self.prompt_version in {
            "web-review/v5",
            "web-review/v6",
            "web-review/v7",
            "web-review/v8",
            "web-review/v9",
            "web-review/v10",
        }:
            validate_locations(self.evidence, self.source_locations)
            if self.prompt_task in {"review", "repair"}:
                messages[0]["content"] = role_policy(self.prompt_task, self.prompt_version)
            else:
                messages[0]["content"] += WEB_RULES + "\nEl host presenta las fuentes; no generes citas."
            if self.format_reminder:
                messages[0]["content"] += "\nDevuelve el JSON completo con referencias source_id, sin citas."
            data = json.loads(messages[-1]["content"])
            data["localizaciones_fuentes"] = {
                key: value.model_dump() for key, value in self.source_locations.items()
            }
            messages[-1]["content"] = data_json(data)
            return messages
        if self.prompt_version in {
            "web-review/v2",
            "web-review/v3",
            "web-review/v4",
        } and self.prompt_task in {
            "review",
            "repair",
        }:
            # Replace the inherited tutor policy; do not merely append a competing role.
            messages[0]["content"] = role_policy(self.prompt_task, self.prompt_version)
            if self.prompt_task == "review" and self.format_reminder:
                messages[0]["content"] += (
                    "\nRepite el JSON completo con las claves y citas literales indicadas. "
                    "Los hechos y criterios no han cambiado."
                )
            return messages
        messages[0]["content"] += WEB_RULES
        if self.prompt_task == "review":
            messages[0]["content"] += WEB_REVIEW
            if self.format_reminder:
                messages[0]["content"] += (
                    "\nThe prior review did not satisfy the declared schema or literal-witness "
                    "contract. Return the complete JSON exactly as specified, with literal "
                    "quotations. Facts and semantic criteria have not changed."
                )
        elif self.prompt_task == "generate":
            messages[0]["content"] += "\nResponde brevemente, en unas tres frases."
        else:
            messages[0]["content"] += (
                "\nCorrige preferentemente donde está el defecto, conservando lo válido. "
                "Devuelve la respuesta completa, breve; no añadas una negación al final "
                "dejando el error inicial. Las objeciones son falibles."
            )
        return messages


class WebAdvisoryReview(AdvisoryReview):
    external_support: Literal["supported", "rejected", "unknown", "not_used"]
    teacher_compatibility: Literal["compatible", "conflict", "unknown"]
    response_action: Literal["explanation", "limit", "repair"]

    @model_validator(mode="after")
    def check_action(self):
        if (self.response_action == "repair") != (self.status == "issues_found"):
            raise ValueError("repair action and concrete issues must agree")
        return self


def parse_web_review(text, request, candidate):
    text = text.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    if getattr(request, "prompt_version", None) in {
        "web-review/v7",
        "web-review/v8",
        "web-review/v9",
        "web-review/v10",
    }:
        return parse_minimal_reference_review(text, request)
    if getattr(request, "prompt_version", None) in {
        "web-review/v5",
        "web-review/v6",
        "web-review/v7",
        "web-review/v8",
        "web-review/v9",
        "web-review/v10",
    }:
        return parse_reference_review(
            text,
            request,
            teacher_only_contradiction=request.prompt_version == "web-review/v5",
            idle_action_alias=request.prompt_version == "web-review/v6",
        )
    review = WebAdvisoryReview.model_validate_json(text)
    if getattr(request, "prompt_version", "web-review/v1") in {
        "web-review/v2",
        "web-review/v3",
        "web-review/v4",
    }:
        for issue in review.issues:
            # Presentation only: the interior must still be an exact literal span.
            # The raw model output remains unchanged in the generation receipt.
            claim = issue.claim
            if (
                not quote_in(claim, candidate)
                and len(claim) >= 2
                and claim[0] == claim[-1] == '"'
                and quote_in(claim[1:-1], candidate)
            ):
                issue.claim = claim[1:-1]
    # Reuse existing exact-claim and exact-source checks; these are not entailment.
    parse_review(
        json.dumps(review.model_dump(include={"status", "issues"}), ensure_ascii=False), request, candidate
    )
    source_ids = {item.fragment_id: item.document_id for item in request.evidence}
    for issue in review.issues:
        if issue.kind == "contradiction" and not any(
            source_ids[witness.source_id].startswith("teacher/") for witness in issue.evidence
        ):
            raise ValueError("teacher contradiction needs an exact teacher witness")
    return review


def issue_signature(review):
    return tuple(
        sorted(
            (
                issue.kind,
                " ".join(issue.claim.lower().split()),
                tuple(
                    sorted((w.source_id, " ".join(getattr(w, "quote", "").split())) for w in issue.evidence)
                ),
            )
            for issue in review.issues
        )
    )


class WebReviewRounds:
    """Bounded autonomous proposals; independent measurement happens outside this loop."""

    def __init__(
        self,
        generator,
        critic,
        *,
        budget,
        revalidate,
        record=None,
        max_rounds=2,
        generator_profile="qwen25-1.5b",
        generation_didactic_profile=None,
        critic_profile="qwen25-7b",
        stage_tokens=None,
        repair_with_generator=False,
        stage_deadline_ms=150000,
        prompt_version="web-review/v1",
        source_locations=None,
        example_probe_enabled=False,
        source_terminology_guard=False,
    ):
        if type(source_terminology_guard) is not bool or (
            source_terminology_guard
            and prompt_version not in {"web-review/v7", "web-review/v8", "web-review/v9", "web-review/v10"}
        ):
            raise ValueError("Source terminology guard requires a reference-bound review")
        self.source_terminology_guard = source_terminology_guard
        if type(max_rounds) is not int or not 1 <= max_rounds <= 2:
            raise ValueError("at most two experimental correction rounds")
        if generator_profile not in {"qwen25-1.5b", "qwen25-7b", "qwen25-14b", "qwen3-8b-nonthinking"}:
            raise ValueError("unregistered initial model")
        if critic_profile not in {"qwen25-7b", "qwen25-14b", "qwen3-8b-nonthinking", "qwen3-8b-thinking"}:
            raise ValueError("unregistered critic model")
        limits = (
            {"generate": 192, "review": 384, "repair": 256} if stage_tokens is None else dict(stage_tokens)
        )
        if set(limits) != {"generate", "review", "repair"} or any(
            type(value) is not int
            or not 1 <= value <= (8192 if key == "review" and critic_profile == "qwen3-8b-thinking" else 2048)
            for key, value in limits.items()
        ):
            raise ValueError("stage token limits must be explicit integers within existing capacity")
        if type(repair_with_generator) is not bool:
            raise ValueError("repair provider selection must be explicit boolean")
        if critic_profile == "qwen3-8b-thinking" and not repair_with_generator:
            raise ValueError("Thinking reviewer is review-only; repair must use generator")
        if critic_profile == "qwen3-8b-thinking" and stage_tokens is None:
            limits["review"] = 8192
        self.repair_with_generator = repair_with_generator
        self.critic_profile, self.stage_tokens = critic_profile, limits
        if type(stage_deadline_ms) is not int or not 1 <= stage_deadline_ms <= 180000:
            raise ValueError("existing expanded stage ceiling exceeded")
        if prompt_version not in {
            "web-review/v1",
            "web-review/v2",
            "web-review/v3",
            "web-review/v4",
            "web-review/v5",
            "web-review/v6",
            "web-review/v7",
            "web-review/v8",
            "web-review/v9",
            "web-review/v10",
        }:
            raise ValueError("unregistered web prompt version")
        self.prompt_version = prompt_version
        self.source_locations = {
            key: SourceLocation.model_validate(value) for key, value in (source_locations or {}).items()
        }
        if generation_didactic_profile is not None and generation_didactic_profile not in STUDY_PROFILES:
            raise ValueError("Unknown generation didactic profile")
        self.generation_didactic_profile = generation_didactic_profile
        self.generator_profile, self.stage_deadline_ms = generator_profile, stage_deadline_ms
        self.generator = ReviewRepairGenerationAdapter(
            generator, budget=budget, revalidate=revalidate, record=record
        )
        self.critic = ReviewRepairGenerationAdapter(
            critic, budget=budget, revalidate=revalidate, record=record
        )
        self.max_rounds = max_rounds
        self.example_probe_enabled = example_probe_enabled

    @staticmethod
    def request(
        base,
        task,
        *,
        draft=None,
        review=None,
        prompt_version="web-review/v1",
        source_locations=None,
        didactic_profile=None,
    ):
        profile = "qwen25-1.5b" if task == "generate" else "qwen25-7b"
        request = structured_request(
            base,
            model_profile=profile,
            task=task,
            draft=draft,
            observations=review.model_dump()["issues"] if review else None,
            didactic_profile=didactic_profile,
        )
        return WebRoundRequest(
            **request.model_dump(), prompt_version=prompt_version, source_locations=source_locations or {}
        )

    async def process(self, base):
        trace = {
            "calls": [],
            "versions": [],
            "reviews": [],
            "format_retries": 0,
            "status": "running",
            "publication_allowed": False,
            "participant_display": None,
            "independent_semantics": False,
            "accepted_by_critic": False,
            "diagnostic_preview": None,
        }
        self.last_trace = trace
        previous = None
        try:
            initial_request = self.request(
                base,
                "generate",
                prompt_version=self.prompt_version,
                source_locations=self.source_locations,
                didactic_profile=self.generation_didactic_profile,
            )
            if self.prompt_version in {
                "web-review/v5",
                "web-review/v6",
                "web-review/v7",
                "web-review/v8",
                "web-review/v9",
                "web-review/v10",
            }:
                trace["source_references"] = readable_references(initial_request)
            initial_request.model_profile = self.generator_profile
            initial_request.constraints.max_tokens = self.stage_tokens["generate"]
            initial_request.constraints.deadline_ms = (
                90000 if self.generator_profile == "qwen25-1.5b" else self.stage_deadline_ms
            )
            current = await self.generator.call("generate", initial_request, trace)
            if not complete(current):
                trace["status"] = "initial_incomplete"
                return trace
            trace["versions"].append(current.model_dump())
            presented = present_academic_answer(current.text)
            trace["presentations"] = [presented]
            for round_index in range(self.max_rounds + 1):
                probe_observation = None
                if self.example_probe_enabled:
                    from oralia.course_dialogue.example_probe import probe_request

                    probe = probe_request(base, presented["text"])
                    if probe is not None:
                        probe.constraints.deadline_ms = self.stage_deadline_ms
                        probe_outcome = await self.critic.call("review", probe, trace)
                        trace["calls"][-1]["review_kind"] = "example_probe"
                        trace.setdefault("example_probes", []).append(probe_outcome.model_dump())
                        if complete(probe_outcome):
                            probe_observation = {
                                "kind": "advisory_counterexample",
                                "text": probe_outcome.text,
                                "not_source_evidence": True,
                                "not_automatic_issue": True,
                            }
                request = self.request(
                    base,
                    "review",
                    draft=presented["text"],
                    prompt_version=self.prompt_version,
                    source_locations=self.source_locations,
                )
                request.model_profile = self.critic_profile
                if probe_observation is not None:
                    request.observations = [probe_observation]
                if self.critic_profile == "qwen3-8b-thinking":
                    from oralia.course_dialogue.thinking_review_request import thinking_review_request

                    request = thinking_review_request(request, self.stage_tokens["review"])
                else:
                    request.constraints.max_tokens = self.stage_tokens["review"]
                request.constraints.deadline_ms = self.stage_deadline_ms
                outcome = await self.critic.call("review", request, trace)
                if not complete(outcome):
                    trace["status"] = "review_incomplete"
                    return trace
                try:
                    review = parse_web_review(outcome.text, request, presented["text"])
                except ValueError as error:
                    trace["reviews"].append({"round": round_index, "invalid": str(error)})
                    if trace["format_retries"] >= 1:
                        trace["status"] = "review_invalid"
                        return trace
                    trace["format_retries"] += 1
                    # Same facts/draft/schema, no oracle or assistant critique is supplied.
                    retry = request.model_copy(deep=True)
                    retry.format_reminder = True
                    outcome = await self.critic.call("review", retry, trace)
                    if not complete(outcome):
                        trace["status"] = "review_incomplete"
                        return trace
                    review = parse_web_review(outcome.text, retry, presented["text"])
                trace["reviews"].append({"round": round_index, **review.model_dump()})
                if self.prompt_version in {
                    "web-review/v5",
                    "web-review/v6",
                    "web-review/v7",
                    "web-review/v8",
                    "web-review/v9",
                    "web-review/v10",
                }:
                    trace["reviews"][-1]["references"] = readable_references(request, review)
                if self.source_terminology_guard and review.status == "no_issues_found":
                    from oralia.course_dialogue.source_terminology import terminology_finding
                    from oralia.course_dialogue.web_review_references import parse_minimal_reference_review

                    finding = terminology_finding(presented["text"], request.evidence, base.student_input)
                    if finding is not None:
                        # Preserve the model verdict. This separate witnessed host check chooses repair.
                        trace.setdefault("host_terminology_reviews", []).append(
                            {"round": round_index, **finding}
                        )
                        review = parse_minimal_reference_review(json.dumps(finding["review"]), request)
                if (
                    review.status == "no_issues_found"
                    and self.generation_didactic_profile == "study-dialogue/v4"
                ):
                    from oralia.course_dialogue.concept_keywords import keyword_terms

                    terms = keyword_terms(presented["text"])
                    trace.setdefault("keyword_checks", []).append({"round": round_index, "terms": terms})
                    if not terms:
                        finding = {
                            "status": "issues_found",
                            "issues": [
                                {
                                    "kind": "coverage",
                                    "claim": "Falta la lista final de palabras clave válida",
                                    "explanation": (
                                        "Incluye siempre Palabras clave: con uno a ocho conceptos usados, "
                                        "separados por punto y coma, sin inventar términos "
                                        "ni cambiar hechos correctos."
                                    ),
                                    "evidence": [],
                                }
                            ],
                        }
                        trace.setdefault("host_keyword_reviews", []).append(finding)
                        # Host format requirement, not an academic source claim.
                        review = AdvisoryReview.model_validate(finding)
                if review.status == "no_issues_found":
                    trace.update(
                        status="critic_finished_unverified",
                        accepted_by_critic=True,
                        diagnostic_preview=presented["text"],
                    )
                    return trace
                if review.status == "insufficient_evidence":
                    trace["status"] = "unresolved_evidence_limit"
                    return trace
                if round_index == self.max_rounds:
                    trace["status"] = "round_limit"
                    return trace
                if previous is not None and (
                    issue_signature(review) == issue_signature(previous)
                    or (
                        self.prompt_version
                        not in {
                            "web-review/v4",
                            "web-review/v5",
                            "web-review/v6",
                            "web-review/v7",
                            "web-review/v8",
                            "web-review/v9",
                            "web-review/v10",
                        }
                        and len(review.issues) >= len(previous.issues)
                    )
                ):
                    # A one-issue reviewer can find a different defect next round;
                    # equal counts alone cannot establish lack of progress in v4.
                    trace["status"] = "no_observed_improvement"
                    return trace
                repair = self.request(
                    base,
                    "repair",
                    draft=presented["text"],
                    review=review,
                    prompt_version=self.prompt_version,
                    source_locations=self.source_locations,
                )
                repair.model_profile = (
                    self.generator_profile if self.repair_with_generator else self.critic_profile
                )
                repair.constraints.max_tokens = self.stage_tokens["repair"]
                repair.constraints.deadline_ms = self.stage_deadline_ms
                repair_port = self.generator if self.repair_with_generator else self.critic
                corrected = await repair_port.call("repair", repair, trace)
                if not complete(corrected):
                    trace["status"] = "repair_incomplete"
                    return trace
                trace["versions"].append(corrected.model_dump())
                next_presented = present_academic_answer(corrected.text)
                trace["presentations"].append(next_presented)
                if next_presented["text"] == presented["text"]:
                    trace["status"] = "unchanged_candidate"
                    return trace
                previous, current = review, corrected
                presented = next_presented
        except ValueError as error:
            trace.update(status="contract_or_budget_limit", error=str(error))
        except TimeoutError:
            trace["status"] = "deadline"
        except asyncio.CancelledError:
            trace["status"] = "cancelled"
            raise
        return trace
