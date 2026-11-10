"""CoherenceVerifierAgent (contracts/self-study-agents.md, research.md §5) — role
`verifier`, tercera implementación independiente de la técnica de solapamiento léxico
(distinta de `GroundingVerifierAgent` y `SolutionNonDisclosureVerifierAgent`): contrato,
umbrales y traza propios, tokenización propia en este módulo.

Detecta, de forma determinista y stateless (solo a partir de su propio
`AgentRequest.input`, sin consultar la base de datos ni el historial completo — FR-015):
`contradiccion` (vs. `prior_statements`/`active_sources`), `repeticion` (solo contra el
turno inmediatamente anterior), `perdida_objetivo`/`exceso_turnos_mismo_concepto`/
`ausencia_progreso` (a partir de `turn_number`/`max_turns`/`concepts_addressed`).
`fallo_agente`/`latencia_excesiva` los deriva el compositor directamente de
`AgencyOutcome` (Feature 001, sin cambios) — este agente nunca los produce."""

from __future__ import annotations

import re

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.infrastructure.generation import config

CONTRACT = AgentContractSchema(
    agent_id="coherence-verifier",
    version="1.0.0",
    purpose="Detecta contradicción, repetición, pérdida de objetivo y ausencia de progreso (FR-015)",
    input_schema_ref="contracts/self-study-agents.md#CoherenceVerifierAgent.input",
    output_schema_ref="contracts/self-study-agents.md#CoherenceVerifierAgent.output",
    timeout_ms=3000,
    confidence_semantics="no aplica — el veredicto en sí es la salida, no una probabilidad",
    success_criteria=["nunca aprueba una propuesta que contradice una afirmación previa o fuente activa"],
    trace_fields=["verdict", "incident_types", "recovery_action"],
)

# research.md §5: propio — distinto de `_MIN_SIGNIFICANT_WORD_LEN`/umbrales de
# GroundingVerifierAgent y SolutionNonDisclosureVerifierAgent (ni valor ni env var compartidos).
_MIN_SIGNIFICANT_WORD_LEN = 4
_REPETITION_OVERLAP_THRESHOLD = 0.6
_CONTRADICTION_SHARED_WORDS_MIN = 2
_NEGATION_RE = re.compile(r"\b(no|nunca|jamás|jamas|tampoco)\b", re.IGNORECASE)


def _significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    return {w for w in words if len(w) >= _MIN_SIGNIFICANT_WORD_LEN}


def _has_negation(text: str) -> bool:
    return bool(_NEGATION_RE.search(text))


# Finite predicate equivalences for v2 polarity checks, not an entailment model.
# Different predicates about shared nouns do not assert opposite propositions.
# Unknown predicates retain the conservative v1 overlap check.
_PREDICATES = {
    "be": r"es|son|era|eran|fue|fueron",
    "present": r"presenta|presentan|muestra|muestran|comunica|comunican",
    "store": r"guarda|guardan|conserva|conservan|almacena|almacenan",
    "receive": r"recibe|reciben",
    "check": r"comprueba|comprueban|valida|validan|verifica|verifican",
    "add": r"añade|añaden|agrega|agregan",
    "contain": r"contiene|contienen|incluye|incluyen",
    "describe": r"describe|describen|explica|explican",
    "change": r"cambia|cambian|transforma|transforman",
    "boil": r"hierve|hierven",
    "depend": r"depende|dependen",
    "equate": r"equivale|equivalen",
}


def _finite_predicate(text: str) -> tuple[int, str] | None:
    matches = [
        (match.start(), key)
        for key, pattern in _PREDICATES.items()
        if (match := re.search(r"\b(?:" + pattern + r")\b", text, re.I))
    ]
    return min(matches) if matches else None


def _detect_contradiction(proposal_text: str, statements: list[str], *, clause_polarity=False) -> bool:
    # Polarity belongs to a statement, not to an entire response/document. In
    # particular, "No contiene datos de personas" must not negate an earlier
    # sentence about water. Keep the independent lexical conflict check; copied
    # evidence never exempts a contradictory statement from another source.
    def sentences(text: str) -> list[str]:
        separator = r"(?<=[.!?])\s+|[\r\n]+"
        if clause_polarity:
            separator += r"|\s+y\s+(?=(?:no|nunca|jamás|jamas|tampoco)\b)"
        return [part for part in re.split(separator, text, flags=re.I) if part.strip()]

    def annotated(text):
        subject = None
        rows = []
        for clause in sentences(text):
            predicate = _finite_predicate(clause) if clause_polarity else None
            if predicate:
                heads = re.findall(r"\b(?:el|la|los|las)\s+([a-záéíóúñü]+)", clause[: predicate[0]], re.I)
                if heads:
                    subject = heads[-1].casefold()
            rows.append((clause, subject if predicate else None, predicate[1] if predicate else None))
        return rows

    for proposal, proposal_subject, proposed_predicate in annotated(proposal_text):
        proposal_words = _significant_words(proposal)
        for statement in statements:
            for reference, reference_subject, reference_predicate in annotated(statement):
                shared = proposal_words & _significant_words(reference)
                if len(shared) < _CONTRADICTION_SHARED_WORDS_MIN:
                    continue
                if _has_negation(proposal) != _has_negation(reference):
                    if clause_polarity:
                        if proposal_subject and reference_subject and proposal_subject != reference_subject:
                            continue
                        if (
                            proposed_predicate
                            and reference_predicate
                            and proposed_predicate != reference_predicate
                        ):
                            continue
                    return True

    return False


def _detect_repetition(proposal_text: str, prior_statements: list[str]) -> bool:
    if not prior_statements:
        return False
    last = prior_statements[-1]
    if not last:
        return False
    proposal_words = _significant_words(proposal_text)
    prior_words = _significant_words(last)
    if not proposal_words or not prior_words:
        return False
    overlap = proposal_words & prior_words
    return len(overlap) / len(proposal_words | prior_words) >= _REPETITION_OVERLAP_THRESHOLD


class CoherenceVerifierAgent:
    contract = CONTRACT
    dialogue_contract = CONTRACT.model_copy(
        update={
            "version": "2.1.0",
            "input_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#verification-v2",
        }
    )

    package_contract = CONTRACT.model_copy(
        update={
            "version": "2.2.0",
            "input_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#verification-v3",
        }
    )

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        data = request.input
        proposal_text = str(data.get("proposal_text", ""))
        prior_statements = [s for s in data.get("prior_statements", []) if s]
        active_sources = [s for s in data.get("active_sources", []) if s]
        concepts_addressed = list(data.get("concepts_addressed", []))
        turn_number = int(data.get("turn_number", 0))
        max_turns = int(data.get("max_turns", 0))
        dialogue_v2 = data.get("dialogue_schema_version") in {2, 3}
        dialogue_v3 = data.get("dialogue_schema_version") == 3
        exact_requested_repeat = (
            dialogue_v2
            and data.get("intentional_repeat") is True
            and bool(prior_statements)
            and proposal_text == prior_statements[-1]
        )
        requested_focus = (
            dialogue_v2
            and data.get("requested_focus")
            in {"example", "comparison", "help", "rephrase", "repeat_component"}
            and proposal_text == data.get("focused_reviewed_unit")
            and proposal_text in active_sources
            and bool(prior_statements)
            and proposal_text != prior_statements[-1]
            and proposal_text in prior_statements[-1]
        )
        structural_progress = dialogue_v2 and data.get("structural_progress") is True

        incident_types: list[str] = []
        recovery_action: str | None = None
        verdict = "approved"

        v3_conflicts = []
        v3_uncertain = []
        if dialogue_v3:
            from oralia.domain.agents.coherence_propositions import compare, repeated

            v3_conflicts, v3_uncertain = compare(proposal_text, prior_statements + active_sources)
        if v3_conflicts or (
            not dialogue_v3
            and _detect_contradiction(
                proposal_text, prior_statements + active_sources, clause_polarity=dialogue_v2
            )
        ):
            incident_types.append("contradiccion")
            verdict = "block"
            recovery_action = "pedir_aclaracion"
        elif dialogue_v3 and v3_uncertain:
            incident_types.append("condiciones_no_comparables")
            verdict = "reformulate"
            recovery_action = "pedir_aclaracion"
        elif (
            not exact_requested_repeat
            and not requested_focus
            and (
                repeated(proposal_text, prior_statements)
                if dialogue_v3
                else _detect_repetition(proposal_text, prior_statements)
            )
        ):
            incident_types.append("repeticion")
            verdict = "reformulate"
            recovery_action = "reformular"

        no_progress_window = config.get_coherence_no_progress_window()
        if verdict == "approved" and not structural_progress and turn_number >= no_progress_window:
            if not concepts_addressed:
                incident_types.append("ausencia_progreso")
                verdict = "reformulate"
                recovery_action = "reformular"
            elif len(concepts_addressed) == 1:
                incident_types.append("exceso_turnos_mismo_concepto")
                verdict = "reformulate"
                recovery_action = "pedir_aclaracion"

        near_session_limit = max_turns > 0 and turn_number >= max_turns - 1
        if (
            verdict == "approved"
            and not structural_progress
            and near_session_limit
            and len(concepts_addressed) < 2
        ):
            incident_types.append("perdida_objetivo")
            verdict = "reformulate"
            recovery_action = "reducir_respuesta"

        return AgentResult(
            status="ok",
            output={"verdict": verdict, "incident_types": incident_types, "recovery_action": recovery_action},
            confidence=None,
            trace={"verdict": verdict, "incident_types": incident_types},
        )
