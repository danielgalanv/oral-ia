"""SolutionNonDisclosureVerifierAgent (contracts/self-study-agents.md, research.md §4) —
role `verifier`, **completamente independiente** de `GroundingVerifierAgent` (Feature
002): contrato, umbral, veredicto y traza propios. Implementa su propia función de
tokenización/solapamiento en este módulo — MUST NOT importar la función privada de
`grounding_verifier_agent.py` (Feature 002, no modificable, FR-025).

Compara `question_text` con `internal_expected_answer` — dos textos producidos por el
propio sistema — nunca evalúa ni califica al estudiante (FR-013a)."""

from __future__ import annotations

import re

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.infrastructure.generation import config

CONTRACT = AgentContractSchema(
    agent_id="solution-non-disclosure-verifier",
    version="1.0.0",
    purpose="Verifica que una pregunta de práctica no revele su propia solución (FR-013a)",
    input_schema_ref="contracts/self-study-agents.md#SolutionNonDisclosureVerifierAgent.input",
    output_schema_ref="contracts/self-study-agents.md#SolutionNonDisclosureVerifierAgent.output",
    timeout_ms=2000,
    confidence_semantics="no aplica — el veredicto en sí es la salida, no una probabilidad",
    success_criteria=[
        "nunca aprueba una pregunta cuyo texto solapa significativamente con la solución interna"
    ],
    trace_fields=["verdict", "overlap_score"],
)

DIALOGUE_CONTRACT = CONTRACT.model_copy(
    update={
        "version": "2.0.0",
        "input_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#non-disclosure-v2",
        "output_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#non-disclosure-v2",
    }
)

# research.md §4: propio, distinto del `_MIN_SIGNIFICANT_WORD_LEN`/`_SUPPORT_OVERLAP_THRESHOLD`
# de GroundingVerifierAgent (Feature 002) — ni el valor ni la variable de entorno se comparten.
_MIN_SIGNIFICANT_WORD_LEN = 4


def _significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúñü0-9]+", text.lower())
    return {
        word
        for word in words
        if len(word) >= _MIN_SIGNIFICANT_WORD_LEN or word.isdigit() or any(char.isdigit() for char in word)
    }


def _overlap_score(question_text: str, internal_expected_answer: str) -> float:
    answer_words = _significant_words(internal_expected_answer)
    if not answer_words:
        return 0.0
    question_words = _significant_words(question_text)
    if len(answer_words) == 1:
        return 1.0 if next(iter(answer_words)) in question_words else 0.0
    overlap = answer_words & question_words
    return len(overlap) / len(answer_words)


class SolutionNonDisclosureVerifierAgent:
    contract = CONTRACT
    dialogue_contract = DIALOGUE_CONTRACT

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        data = request.input
        question_text = str(data.get("question_text", ""))
        internal_expected_answer = str(data.get("internal_expected_answer", ""))

        threshold = config.get_disclosure_overlap_threshold()
        if data.get("dialogue_schema_version") == 2:
            if cancellation.is_cancelled():
                return AgentResult(status="cancelled")
            answers = data.get("internal_expected_answers")
            if (
                not isinstance(answers, list)
                or not answers
                or len(answers) > 200
                or any(not isinstance(answer, str) or not answer.strip() for answer in answers)
            ):
                return AgentResult(status="error")
            clauses = [
                clause.strip()
                for answer in answers
                for clause in re.split(r"[.;!?]", answer)
                if clause.strip()
            ]
            score = max((_overlap_score(question_text, clause) for clause in clauses), default=0.0)
            answer_numbers = {
                word
                for answer in answers
                for word in _significant_words(answer)
                if any(char.isdigit() for char in word)
            }
            question_numbers = {
                word for word in _significant_words(question_text) if any(char.isdigit() for char in word)
            }
            candidate_words = _significant_words(question_text)
            # Topic nouns alone do not state a solution. Require a complete
            # documented clause (including its predicate), or a complete short
            # answer, rather than importing v1's low whole-answer overlap cutoff
            # into short clauses. Numeric solution anchors remain protected.
            echoes_clause = any(
                len(words := _significant_words(clause)) >= 4 and words <= candidate_words
                for clause in clauses
            )
            echoes_short_answer = any(
                0 < len(words := _significant_words(answer)) <= 3 and words <= candidate_words
                for answer in answers
            )
            verdict = (
                "block"
                if echoes_clause or echoes_short_answer or bool(answer_numbers & question_numbers)
                else "approved"
            )
            return AgentResult(
                status="ok",
                output={"verdict": verdict, "overlap_score": score},
                confidence=None,
                trace={"verdict": verdict, "overlap_score": score},
            )
        score = _overlap_score(question_text, internal_expected_answer)
        verdict = "block" if score >= threshold else "approved"

        return AgentResult(
            status="ok",
            output={"verdict": verdict, "overlap_score": score},
            confidence=None,
            trace={"verdict": verdict, "overlap_score": score},
        )
