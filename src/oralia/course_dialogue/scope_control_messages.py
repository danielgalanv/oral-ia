"""Typed control-message profile, separate from academic evidence generation."""

import json
from typing import Literal

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.scope_message_profiles import INSTRUCTIONS, control_step
from oralia.infrastructure.generation.generation_port import GenerationRequest


class ScopeControlRequest(GenerationRequest):
    control_step: Literal["target", "referent", "literal"]


def build_scope_control_messages(request):
    """Keep policy input separate from academic EvidenceItem grounding rules.

    The caller still must validate scope binding/metadata and use real finite
    decoding. This renderer grants neither content authority nor publication.
    """
    if not isinstance(request, ScopeControlRequest):
        raise ValueError("typed ScopeControlRequest required; academic requests cannot opt out of grounding")
    if (
        request.general_knowledge_allowed
        or request.evidence
        or request.conversation_history
        or request.concepts_addressed
    ):
        raise ValueError("scope-control renderer cannot carry academic answers/evidence or general knowledge")
    data = json.loads(request.student_input)
    step = control_step(data)
    if request.control_step != step or request.instruction != INSTRUCTIONS[step]:
        raise ValueError("scope-control typed step/instruction mismatch")
    if not isinstance(data["question"], str):
        raise ValueError("control question must be text")
    if step != "literal":
        if set(request.output_schema or {}) != {"type", "x-oralia-finite-outputs"}:
            raise ValueError("only the compiled finite schema is supported for control")
        if finite_json_outputs(request.output_schema) is None:
            raise ValueError("finite schema required for scope-control selection")
    elif request.output_schema is not None or data["role"] not in {
        "supporting_mention",
        "included_part",
        "excluded_standalone_part",
    }:
        raise ValueError("invalid literal control step")
    system = request.instruction
    if request.output_schema is not None:
        schema_hint = {
            key: value for key, value in request.output_schema.items() if key != "x-oralia-finite-outputs"
        }
        system += "\nEsquema de salida solicitado (no es aprobación):\n" + json.dumps(
            schema_hint, ensure_ascii=False
        )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "<scope_control_data>" + request.student_input + "</scope_control_data>"},
    ]
