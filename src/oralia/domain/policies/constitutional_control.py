"""FR-014, FR-015, FR-018a: the constitutional control — mandatory on every turn, never
omissible for resource savings (Constitution Principio IX), and never able to approve
its own generator's output (Constitution Principio IV: verifier != generator).

Blocks any proposal that assigns a grade, impersonates the professor, issues an academic
decision, reveals unauthorized data, or steps outside the activity's scope.
"""

from __future__ import annotations

import re

from pydantic import ValidationError

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationReason,
    AuthorizationVerdict,
)
from oralia.domain.policies.output_authorization_verifier import verify_output_authorization

CONTRACT = AgentContractSchema(
    agent_id="constitutional-control",
    version="2.0.0",
    purpose="Bloquear notas, decisiones académicas, datos no autorizados o salidas fuera de alcance",
    input_schema_ref=(
        "AgentRequest{input.proposal: OutputProposal, "
        "context.authorization_snapshot: AuthorizationSnapshot, "
        "context.activity_configuration_id: str, context.actual_recipient: str}"
    ),
    output_schema_ref=(
        "AgentResult{output.verdict: approved|block, output.reasons: list[str], "
        "output.authorization_context: object}"
    ),
    timeout_ms=1000,
    confidence_semantics="1.0 — coincidencia de reglas deterministas, no una estimación",
    success_criteria=["clasifica cada propuesta como approved o block con razones observables"],
    trace_fields=["verdict", "reasons"],
)

SAFE_BLOCKED_MESSAGE = (
    "No puedo mostrar esa respuesta porque incumple los límites de este sistema de IA. "
    "¿Puedes reformular tu pregunta sobre la actividad?"
)

# FR-014/H02 (research.md §8, seguimiento ronda 4): grade-assignment detection is split
# into three independent, deterministic rules — none of them a single
# "block N/10 unconditionally" shortcut, since a bare fraction does not by itself
# demonstrate a grade is being assigned (see Rule C).
_GRADE_NOUNS = r"nota|calificaci[oó]n|puntuaci[oó]n"
_GRANTING_VERBS = r"otorgo|otorga|concedo|concede|asigno|asigna"
_QUALITATIVE_VALUES = (
    r"sobresaliente|notable|aprobad[oa]|suspens[oa]|matr[ií]cula de honor|no apto|apto|excelente"
)
# "un"/"una" are NOT independent number words — they are the ordinary Spanish
# indefinite article and match countless unrelated sentences ("asigna un valor",
# "concede una prórroga"). They only count as part of a value when they precede one of
# the actual cardinal words below (see the optional-prefix group in _VALUE/_VALUE_GRANT).
_NUMBER_WORDS = r"cero|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez"
_FRACTION_OUT_OF_10 = r"\d{1,2}\s*/\s*10"
_EVALUATED_ITEM_NOUNS = r"pr[aá]ctica|examen|trabajo|ejercicio|tarea|prueba"
_ARTICLE_PREFIX = r"(?:un[ao]?\s+)?"
# Rule A's value set: a bare digit is unambiguous only when directly anchored to a
# grade noun/copula (see Rule A below) — that anchoring is what makes it safe here.
_VALUE = rf"(?:\d+|{_QUALITATIVE_VALUES}|{_ARTICLE_PREFIX}(?:{_NUMBER_WORDS})|{_FRACTION_OUT_OF_10})"
# Rule B's value set deliberately excludes a bare digit: "asigno/asigna" is heavily
# overloaded with the ordinary "assign a value to a variable" sense (programming/math),
# and a bare digit next to that verb does not by itself demonstrate a grade is being
# assigned — a qualitative word, a spelled-out cardinal, or an "N/10" fraction are each
# specific enough on their own not to need that anchor.
_VALUE_GRANT = rf"(?:{_QUALITATIVE_VALUES}|{_ARTICLE_PREFIX}(?:{_NUMBER_WORDS})|{_FRACTION_OUT_OF_10})"
_COPULA = r"es|ser[aá]|queda en"
_FILLER = r"(?:\s+\S+)"

_PROHIBITED_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "assigns_grade",
        re.compile(
            # Rule A (noun-anchored): immediate "nota: 9" form (unchanged), or the
            # noun followed — within up to 4 filler words — by a copulative verb and a
            # value ("Tu nota es 9 sobre 10.", "Tu puntuación en la práctica es 9/10.").
            rf"\b(?:{_GRADE_NOUNS})\s*[:=]?\s*{_VALUE}"
            rf"|\b(?:{_GRADE_NOUNS})\b{_FILLER}{{0,4}}?\s+(?:{_COPULA})\s+{_VALUE}\b"
            # Rule B (verb-anchored): a granting verb followed — within up to 3 filler
            # words — by a value (no bare digit, see _VALUE_GRANT), with no grade noun
            # required ("Te otorgo un sobresaliente.", "Te asigno un nueve.").
            rf"|\b(?:{_GRANTING_VERBS})\b{_FILLER}{{0,3}}?\s+{_VALUE_GRANT}\b",
            re.I,
        ),
    ),
    (
        "assigns_score_fraction",
        re.compile(
            # Rule C (contextual, tightened): an "N/10" fraction counts as a grade only
            # when directly linked — via "en"/"de" (+ optional article), not merely
            # "somewhere within a few words" — to an evaluated-item noun. Proximity
            # alone is not enough: "en este ejercicio la probabilidad es 9/10" has an
            # evaluated-item noun nearby but the fraction actually describes a
            # probability, not a score for that item — the direct-preposition link is
            # what "9/10 en la práctica 2." has and that sentence does not.
            rf"\b{_FRACTION_OUT_OF_10}\b\s+(?:en|de)\s+(?:el|la|los|las)?\s*\b(?:{_EVALUATED_ITEM_NOUNS})\b",
            re.I,
        ),
    ),
    (
        "academic_decision",
        re.compile(r"\b(apruebas?|suspendes?|has aprobado|has suspendido|est[aá]s aprobad)", re.I),
    ),
    ("impersonates_professor", re.compile(r"\bcomo (tu|su) profesor(a)?\b", re.I)),
    (
        "academic_decision",
        re.compile(
            r"\btu\s+(?:nivel|rendimiento|capacidad|comprensi[oó]n|competencia|dominio)"
            r"\s+(?:es|resulta|parece)\s+(?:alt[oa]|baj[oa]|excelente|insuficiente|suficiente|bueno|malo)\b"
            r"|\beres\s+(?:in)?competente\b",
            re.I,
        ),
    ),
]


def evaluate(proposal_text: str) -> tuple[str, list[str]]:
    """Pure rule evaluation — used directly by tests and by the agent wrapper below."""
    reasons = [name for name, pattern in _PROHIBITED_PATTERNS if pattern.search(proposal_text)]
    verdict = "block" if reasons else "approved"
    return verdict, reasons


def constitutional_verdict_or_block(
    result: AgentResult | None,
    *,
    fallback_attempt: int = 0,
) -> AuthorizationVerdict:
    """Interpret an agent invocation result without any implicit approval path."""

    reasons = [AuthorizationReason.INVALID_CONTEXT]
    if fallback_attempt == 1:
        reasons.append(AuthorizationReason.UNSAFE_FALLBACK)

    def blocked() -> AuthorizationVerdict:
        return AuthorizationVerdict(
            verdict="block",
            reason_codes=tuple(reasons),
            fallback_attempt=1 if fallback_attempt == 1 else 0,
            message_type="operational" if fallback_attempt == 1 else "normal",
        )

    if result is None or result.status != "ok" or not isinstance(result.output, dict):
        return blocked()
    if set(result.output) != {"verdict", "reasons", "authorization_context"}:
        return blocked()
    output_reasons = result.output.get("reasons")
    context = result.output.get("authorization_context")
    if not isinstance(output_reasons, list) or not isinstance(context, dict):
        return blocked()
    try:
        authorization = AuthorizationVerdict.model_validate(
            {
                **context,
                "verdict": result.output.get("verdict"),
                "reason_codes": output_reasons,
            }
        )
    except (TypeError, ValidationError):
        return blocked()
    expected_message_type = "operational" if fallback_attempt == 1 else "normal"
    if authorization.fallback_attempt != fallback_attempt:
        return blocked()
    if authorization.message_type != expected_message_type:
        return blocked()
    if authorization.verdict == "approved" and any(
        value is None
        for value in (
            authorization.activity_configuration_id,
            authorization.activity_version,
            authorization.policy_id,
            authorization.policy_version,
            authorization.schema_version,
            authorization.policy_sha256,
            authorization.template_id,
            authorization.template_version,
            authorization.template_sha256,
        )
    ):
        return blocked()
    return authorization


def constitutional_result_or_block(
    result: AgentResult | None,
    *,
    fallback_attempt: int = 0,
) -> tuple[str, list[str]]:
    authorization = constitutional_verdict_or_block(
        result,
        fallback_attempt=fallback_attempt,
    )
    return authorization.verdict, [reason.value for reason in authorization.reason_codes]


class ConstitutionalControl:
    """Verifier role only (Principio IV) — never registered as a generator step."""

    contract = CONTRACT

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        if cancellation.is_cancelled():
            return AgentResult(status="cancelled", output=None, confidence=1.0)

        proposal = request.input.get("proposal")
        snapshot = request.context.get("authorization_snapshot")
        attempt = request.input.get("fallback_attempt", 0)
        try:
            if proposal is not None:
                proposal_text = request.input.get("proposal_text")
                proposal_value = (
                    proposal.model_dump(mode="json") if hasattr(proposal, "model_dump") else proposal
                )
                if (
                    proposal_text is not None
                    and isinstance(proposal_value, dict)
                    and proposal_text != proposal_value.get("text")
                ):
                    proposal_value = {**proposal_value, "text": ""}
                proposal = proposal_value
            authorization = verify_output_authorization(
                proposal,
                snapshot,
                actual_session_id=str(request.session_id),
                actual_activity_configuration_id=request.context.get("activity_configuration_id"),
                actual_recipient=request.context.get("actual_recipient"),
                fallback_attempt=attempt if type(attempt) is int else 1,
                h02_evaluator=evaluate,
            )
            verdict = authorization.verdict
            reasons = [reason.value for reason in authorization.reason_codes]
            authorization_context = authorization.model_dump(
                mode="json",
                exclude={"verdict", "reason_codes"},
                exclude_none=True,
            )
        except Exception:
            verdict = "block"
            reasons = ["invalid_context"]
            if attempt == 1:
                reasons.append("unsafe_fallback")
            authorization_context = {"fallback_attempt": attempt if attempt in (0, 1) else 1}
        return AgentResult(
            status="ok",
            output={
                "verdict": verdict,
                "reasons": reasons,
                "authorization_context": authorization_context,
            },
            confidence=1.0,
            trace={"verdict": verdict, "reasons": reasons},
        )


__all__ = [
    "CONTRACT",
    "SAFE_BLOCKED_MESSAGE",
    "ConstitutionalControl",
    "constitutional_result_or_block",
    "constitutional_verdict_or_block",
    "evaluate",
]
