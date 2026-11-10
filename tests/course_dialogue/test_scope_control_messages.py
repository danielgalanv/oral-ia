"""Reproduce the original packaging mismatch and test a narrow offline correction."""

import json
from pathlib import Path

import pytest

from oralia.course_dialogue.scope_control_messages import ScopeControlRequest, build_scope_control_messages
from oralia.course_dialogue.scope_message_profiles import INSTRUCTIONS
from oralia.infrastructure.generation.generation_port import EvidenceItem

EVIDENCE = Path(__file__).resolve().parents[2] / "specs/012-conversational-course-study/evidence"


def request():
    audit = json.loads((EVIDENCE / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    return ScopeControlRequest.model_validate(
        {**audit["original_attempt"]["request"], "control_step": "target"}
    )


def test_original_conflict_is_preserved_and_corrected_renderer_preserves_control_data():
    audit = json.loads((EVIDENCE / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    old = audit["frame"]["messages"]
    assert (
        "Responde únicamente usando el contenido de las etiquetas <evidencia> anteriores" in old[1]["content"]
    )
    assert "<evidencia documento=" not in old[1]["content"]
    req = request()
    corrected = build_scope_control_messages(req)
    assert [m["role"] for m in corrected] == ["system", "user"]
    assert req.student_input in corrected[1]["content"]
    assert (
        "Responde únicamente usando el contenido de las etiquetas <evidencia>" not in corrected[1]["content"]
    )
    assert "x-oralia-finite-outputs" not in corrected[0]["content"]
    assert req.general_knowledge_allowed is False


@pytest.mark.parametrize(
    "patch",
    [
        {"general_knowledge_allowed": True},
        {"evidence": [EvidenceItem(fragment_id="a", text="academic", document_id="b", document_version=1)]},
        {"student_input": "ordinary academic prompt"},
        {"output_schema": None},
    ],
)
def test_narrow_control_renderer_does_not_relax_academic_generation(patch):
    with pytest.raises(ValueError):
        build_scope_control_messages(request().model_copy(update=patch))


def test_referent_and_literal_routes_keep_their_own_contracts():
    req = request()
    ref = req.model_copy(
        update={
            "control_step": "referent",
            "instruction": INSTRUCTIONS["referent"],
            "student_input": json.dumps({"question": "eso", "shown_history": []}),
        }
    )
    assert build_scope_control_messages(ref)[1]["content"].startswith("<scope_control_data>")
    quote = req.model_copy(
        update={
            "output_schema": None,
            "control_step": "literal",
            "instruction": INSTRUCTIONS["literal"],
            "student_input": json.dumps(
                {
                    "question": "pruebas y seguridad",
                    "selected_target": {"intent": "mixed"},
                    "role": "included_part",
                }
            ),
        }
    )
    assert "pruebas y seguridad" in build_scope_control_messages(quote)[1]["content"]
