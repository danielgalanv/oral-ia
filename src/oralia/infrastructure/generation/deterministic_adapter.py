"""DeterministicGenerationAdapter (research.md §1): reserve implementation of
`GenerationPort` — extractive over `evidence`, always produces a valid output when
evidence is present. No LLM, no network."""

from __future__ import annotations

import json
import time

from oralia.domain.materials.extractive_excerpt import extractive_excerpt
from oralia.infrastructure.generation.generation_port import GenerationOutcome, GenerationRequest

_MAX_EVIDENCE_ITEMS = 3

_NO_EVIDENCE_TEXT = (
    "No dispongo de información suficiente en los materiales autorizados para responder "
    "con precisión a esto."
)


def _snippet(text: str) -> str:
    return extractive_excerpt(text).text


def _extractive_answer(request: GenerationRequest) -> str:
    if not request.evidence:
        if request.general_knowledge_allowed:
            return (
                "No encuentro esto en los materiales de la actividad; se trata de "
                "conocimiento general, no verificado frente a los materiales."
            )
        return _NO_EVIDENCE_TEXT
    if request.constraints.material_excerpt_version == 2:
        from oralia.domain.materials.query_excerpt import select_query_excerpts

        spans = select_query_excerpts(request.evidence, request.student_input)
        return " ".join(span.text for span in spans) if spans else _NO_EVIDENCE_TEXT
    return " ".join(_snippet(item.text) for item in request.evidence[:_MAX_EVIDENCE_ITEMS])


def _practice_question(request: GenerationRequest) -> tuple[str, str]:
    concept = request.concepts_addressed[-1] if request.concepts_addressed else "el tema tratado"
    question_text = f"Explica con tus propias palabras qué sabes sobre: {concept}."
    expected_answer = _extractive_answer(request)
    return question_text, expected_answer


def _followup_question(request: GenerationRequest) -> str:
    concept = request.concepts_addressed[-1] if request.concepts_addressed else "el tema tratado"
    if request.evidence:
        excerpt = _snippet(request.evidence[0].text).rstrip(".?!")
        try:
            context = json.loads(request.student_input)
        except (ValueError, TypeError):
            context = {}
        if isinstance(context, dict) and isinstance(context.get("target_topic"), str):
            return f"¿Cómo relacionas {context['target_topic']} con {excerpt}?"
        return f"¿Cómo justificas que {excerpt}?"
    return f"¿Puedes explicar con más detalle tu respuesta sobre {concept}?"


class DeterministicGenerationAdapter:
    async def generate(self, request: GenerationRequest) -> GenerationOutcome:
        started = time.monotonic()

        if request.purpose == "pregunta_practica":
            text, expected_answer = _practice_question(request)
        elif request.purpose == "repregunta":
            text = _followup_question(request)
            expected_answer = None
        else:
            text = _extractive_answer(request)
            expected_answer = None

        latency_ms = int((time.monotonic() - started) * 1000)
        return GenerationOutcome(
            ok=True,
            text=text,
            internal_expected_answer=expected_answer,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=latency_ms,
        )
