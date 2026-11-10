"""Single T090 final-output gate and its transaction-local persistence helpers."""

from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session as SASession

from oralia.application.orchestration.output_proposal_builder import (
    ProposalConstructionError,
    build_output_proposal,
)
from oralia.application.services.trace_service import record_event
from oralia.domain.policies.constitutional_control import evaluate
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationReason,
    AuthorizationSnapshot,
    AuthorizationVerdict,
    OutputProposal,
    ScopeReference,
    TrustedTemplate,
)
from oralia.domain.policies.output_authorization_verifier import verify_output_authorization
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    SAFE_TECHNICAL_FALLBACK,
    OutputTemplateCatalog,
    OutputTemplateEntry,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

UpstreamStatus = Literal["ok", "error", "timeout", "cancelled", "missing"]


class FinalOutputGateError(RuntimeError):
    """The gate cannot safely construct or persist a final result."""


class AuthorizationAttemptEvidence(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    attempt: Literal[0, 1]
    verdict: Literal["approved", "block"]
    reason_codes: tuple[AuthorizationReason, ...]
    activity_configuration_id: str | None
    activity_version: int | None
    policy_id: str | None
    policy_version: int | None
    schema_version: int | None
    policy_sha256: str | None
    template_id: str | None
    template_version: int | None
    template_sha256: str | None
    message_type: Literal["normal", "operational"] | None
    text_length: int


class FinalOutputDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    output_text: str | None
    blocked: bool
    turn_status: Literal["completed", "degraded", "blocked"]
    dialogue_action: Literal["respond", "clarify", "finish"]
    final_verdict: AuthorizationVerdict
    final_proposal: OutputProposal | None
    attempts: tuple[AuthorizationAttemptEvidence, ...]
    upstream_status: UpstreamStatus


class PersistedFinalOutput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", arbitrary_types_allowed=True)

    proposal_id: str
    verification_result_id: str
    trace_event_ids: tuple[str, ...]


def _trusted_template(entry: OutputTemplateEntry) -> TrustedTemplate:
    return TrustedTemplate(
        template_id=entry.template_id,
        template_version=entry.version,
        message_type=entry.message_type,
        text=entry.text,
        sha256=entry.sha256,
        scope=ScopeReference(
            topic_ref=entry.topic_ref,
            purpose_ref=entry.purpose_ref,
            action_ref=entry.action_ref,
        ),
    )


def _with_template(
    snapshot: AuthorizationSnapshot,
    entry: OutputTemplateEntry,
) -> AuthorizationSnapshot:
    identity = (entry.template_id, entry.version, entry.sha256)
    if any(
        (template.template_id, template.template_version, template.sha256) == identity
        for template in snapshot.templates
    ):
        return snapshot
    return AuthorizationSnapshot(
        configuration=snapshot.configuration,
        recipient=snapshot.recipient,
        policy=snapshot.policy,
        configuration_general_knowledge_allowed=(
            snapshot.configuration_general_knowledge_allowed
        ),
        templates=(*snapshot.templates, _trusted_template(entry)),
        data_references=snapshot.data_references,
    )


def _attempt(
    verdict: AuthorizationVerdict,
    proposal: OutputProposal | None,
    attempt: Literal[0, 1],
) -> AuthorizationAttemptEvidence:
    return AuthorizationAttemptEvidence(
        attempt=attempt,
        verdict=verdict.verdict,
        reason_codes=verdict.reason_codes,
        activity_configuration_id=verdict.activity_configuration_id,
        activity_version=verdict.activity_version,
        policy_id=verdict.policy_id,
        policy_version=verdict.policy_version,
        schema_version=verdict.schema_version,
        policy_sha256=verdict.policy_sha256,
        template_id=verdict.template_id,
        template_version=verdict.template_version,
        template_sha256=verdict.template_sha256,
        message_type=verdict.message_type,
        text_length=len(proposal.text) if proposal is not None else 0,
    )


def _blocked_fallback_verdict(
    snapshot: AuthorizationSnapshot,
    entry: OutputTemplateEntry | None,
) -> AuthorizationVerdict:
    identity = snapshot.configuration
    return AuthorizationVerdict(
        verdict="block",
        reason_codes=(
            AuthorizationReason.INVALID_CONTEXT,
            AuthorizationReason.UNSAFE_FALLBACK,
        ),
        activity_configuration_id=identity.activity_configuration_id,
        activity_version=identity.activity_version,
        policy_id=identity.policy_id,
        policy_version=identity.policy_version,
        schema_version=identity.schema_version,
        policy_sha256=identity.policy_sha256,
        template_id=entry.template_id if entry else None,
        template_version=entry.version if entry else None,
        template_sha256=entry.sha256 if entry else None,
        fallback_attempt=1,
        message_type="operational" if entry else None,
    )


def _context_failure_verdict(
    snapshot: AuthorizationSnapshot | None,
    reason: AuthorizationReason,
    attempt: Literal[0, 1],
) -> AuthorizationVerdict:
    identity = snapshot.configuration if snapshot is not None else None
    reasons = (reason,) if attempt == 0 else (reason, AuthorizationReason.UNSAFE_FALLBACK)
    return AuthorizationVerdict(
        verdict="block",
        reason_codes=reasons,
        activity_configuration_id=(identity.activity_configuration_id if identity else None),
        activity_version=identity.activity_version if identity else None,
        policy_id=identity.policy_id if identity else None,
        policy_version=identity.policy_version if identity else None,
        schema_version=identity.schema_version if identity else None,
        policy_sha256=identity.policy_sha256 if identity else None,
        fallback_attempt=attempt,
        message_type="normal" if attempt == 0 else "operational",
    )


def decide_final_output(
    snapshot: AuthorizationSnapshot | None,
    initial_proposal: OutputProposal | dict | None,
    *,
    initial_verdict: AuthorizationVerdict | None = None,
    initial_failure_reason: AuthorizationReason | None = None,
    context_failure_reason: AuthorizationReason = AuthorizationReason.MISSING_POLICY,
    upstream_status: UpstreamStatus = "ok",
    catalog: OutputTemplateCatalog = DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    operational_template_id: str = SAFE_TECHNICAL_FALLBACK.template_id,
    operational_template_version: int = SAFE_TECHNICAL_FALLBACK.version,
    operational_template_sha256: str = SAFE_TECHNICAL_FALLBACK.sha256,
    allow_operational_attempt: bool = True,
) -> FinalOutputDecision:
    """Decide the final visible output without closing sessions or committing."""

    attempts: list[AuthorizationAttemptEvidence] = []
    if snapshot is None:
        blocked = _context_failure_verdict(None, context_failure_reason, 0)
        attempts.append(_attempt(blocked, None, 0))
        if allow_operational_attempt:
            blocked = _context_failure_verdict(None, context_failure_reason, 1)
            attempts.append(_attempt(blocked, None, 1))
        return FinalOutputDecision(
            output_text=None,
            blocked=True,
            turn_status="blocked",
            dialogue_action="finish",
            final_verdict=blocked,
            final_proposal=None,
            attempts=tuple(attempts),
            upstream_status=upstream_status,
        )

    if upstream_status == "ok" and initial_proposal is not None:
        if initial_verdict is None:
            initial_verdict = verify_output_authorization(
                initial_proposal,
                snapshot,
                actual_session_id=snapshot.configuration.session_id,
                actual_activity_configuration_id=(
                    snapshot.configuration.activity_configuration_id
                ),
                actual_recipient=snapshot.recipient,
                fallback_attempt=0,
                h02_evaluator=evaluate,
            )
        parsed_initial = None
        try:
            parsed_initial = OutputProposal.model_validate(initial_proposal)
        except (TypeError, ValueError):
            pass
        attempts.append(_attempt(initial_verdict, parsed_initial, 0))
        if initial_verdict.verdict == "approved" and parsed_initial is not None:
            return FinalOutputDecision(
                output_text=parsed_initial.text,
                blocked=False,
                turn_status="completed",
                dialogue_action="respond",
                final_verdict=initial_verdict,
                final_proposal=parsed_initial,
                attempts=tuple(attempts),
                upstream_status=upstream_status,
            )
        if not allow_operational_attempt:
            return FinalOutputDecision(
                output_text=None,
                blocked=True,
                turn_status="blocked",
                dialogue_action="finish",
                final_verdict=initial_verdict,
                final_proposal=None,
                attempts=tuple(attempts),
                upstream_status=upstream_status,
            )
    elif upstream_status == "ok" and initial_failure_reason is not None:
        failed_initial = _context_failure_verdict(snapshot, initial_failure_reason, 0)
        attempts.append(_attempt(failed_initial, None, 0))
        if not allow_operational_attempt:
            return FinalOutputDecision(
                output_text=None,
                blocked=True,
                turn_status="blocked",
                dialogue_action="finish",
                final_verdict=failed_initial,
                final_proposal=None,
                attempts=tuple(attempts),
                upstream_status=upstream_status,
            )

    entry = None
    fallback_proposal = None
    try:
        entry = catalog.resolve(
            operational_template_id,
            operational_template_version,
            operational_template_sha256,
        )
        if entry.message_type != "operational":
            raise ProposalConstructionError("fallback catalog entry must be operational")
        fallback_snapshot = _with_template(snapshot, entry)
        fallback_proposal = build_output_proposal(
            fallback_snapshot,
            template_id=entry.template_id,
            template_version=entry.version,
            template_sha256=entry.sha256,
            catalog=catalog,
            require_policy_permission=False,
        )
        fallback_verdict = verify_output_authorization(
            fallback_proposal,
            fallback_snapshot,
            actual_session_id=snapshot.configuration.session_id,
            actual_activity_configuration_id=(
                snapshot.configuration.activity_configuration_id
            ),
            actual_recipient=snapshot.recipient,
            fallback_attempt=1,
            h02_evaluator=evaluate,
        )
    except (KeyError, TypeError, ValueError):
        fallback_verdict = _blocked_fallback_verdict(snapshot, entry)
    if initial_failure_reason is not None:
        fallback_verdict = _context_failure_verdict(
            snapshot,
            initial_failure_reason,
            1,
        )
        fallback_proposal = None
    attempts.append(_attempt(fallback_verdict, fallback_proposal, 1))

    if fallback_verdict.verdict == "approved" and fallback_proposal is not None:
        return FinalOutputDecision(
            output_text=fallback_proposal.text,
            blocked=True,
            turn_status="degraded",
            dialogue_action="clarify",
            final_verdict=fallback_verdict,
            final_proposal=fallback_proposal,
            attempts=tuple(attempts),
            upstream_status=upstream_status,
        )
    return FinalOutputDecision(
        output_text=None,
        blocked=True,
        turn_status="blocked",
        dialogue_action="finish",
        final_verdict=fallback_verdict,
        final_proposal=None,
        attempts=tuple(attempts),
        upstream_status=upstream_status,
    )


def _authorization_context(verdict: AuthorizationVerdict) -> dict[str, object]:
    context = verdict.model_dump(
        mode="json",
        exclude={"verdict", "reason_codes", "fallback_attempt"},
        exclude_none=True,
    )
    context["attempt"] = verdict.fallback_attempt
    return context


def _safe_proposal_content(decision: FinalOutputDecision) -> dict[str, object]:
    verdict = decision.final_verdict
    content: dict[str, object] = {
        "template_id": verdict.template_id,
        "template_version": verdict.template_version,
        "template_sha256": verdict.template_sha256,
        "message_type": verdict.message_type,
        "attempt": verdict.fallback_attempt,
    }
    if verdict.verdict == "approved" and decision.output_text is not None:
        content["text"] = decision.output_text
    return {key: value for key, value in content.items() if value is not None}


def persist_final_output(
    db: SASession,
    turn: models.Turn,
    decision: FinalOutputDecision,
    *,
    generator_agent_id: str,
) -> PersistedFinalOutput:
    """Persist one final proposal/verdict and safe attempt traces without commit."""

    existing = (
        db.query(models.VerificationResult)
        .join(
            models.GeneratedProposal,
            models.VerificationResult.proposal_id == models.GeneratedProposal.id,
        )
        .filter(models.GeneratedProposal.turn_id == turn.id)
        .count()
    )
    if existing:
        raise FinalOutputGateError("a final constitutional result already exists for this turn")

    proposal = models.GeneratedProposal(
        turn_id=turn.id,
        generator_agent_id=generator_agent_id,
        content=_safe_proposal_content(decision),
        created_at=utcnow(),
    )
    db.add(proposal)
    db.flush()
    verdict = decision.final_verdict
    verification = models.VerificationResult(
        proposal_id=proposal.id,
        verifier_agent_id="constitutional-control",
        verdict=verdict.verdict,
        reasons=[reason.value for reason in verdict.reason_codes],
        authorization_context=_authorization_context(verdict),
        created_at=utcnow(),
    )
    db.add(verification)
    db.flush()

    turn.output_text = decision.output_text
    turn.status = decision.turn_status
    turn.generated_proposal_id = proposal.id
    turn.verification_result_id = verification.id
    db.add(turn)
    db.flush()

    event_ids: list[str] = []
    for attempt in decision.attempts:
        payload = attempt.model_dump(mode="json", exclude_none=True)
        payload["reason_codes"] = [reason.value for reason in attempt.reason_codes]
        payload["component"] = "constitutional-control"
        if attempt.attempt == verdict.fallback_attempt:
            payload["verification_result_id"] = verification.id
        event = record_event(
            db,
            session_id=turn.session_id,
            turn_id=turn.id,
            event_type="output_authorization_attempt",
            agent_id="constitutional-control",
            payload=payload,
            memory_category="metacognitive",
        )
        event_ids.append(event.id)

    return PersistedFinalOutput(
        proposal_id=proposal.id,
        verification_result_id=verification.id,
        trace_event_ids=tuple(event_ids),
    )


__all__ = [
    "AuthorizationAttemptEvidence",
    "FinalOutputDecision",
    "FinalOutputGateError",
    "PersistedFinalOutput",
    "decide_final_output",
    "persist_final_output",
]
