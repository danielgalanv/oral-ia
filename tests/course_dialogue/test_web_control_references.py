"""Bibliographic metadata is not a gate for a semantic verdict."""

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.web_control_request import WebControlRequest, WebControlVerdict


@pytest.mark.parametrize(
    "references",
    [
        [
            {"document_id": "oralia-requisitos-20261027-v2/docente-procedimiento", "page": 8},
            {"document_id": "oralia-requisitos-20261027-v2/docente-requisitos", "page": 15},
        ],
        {"document": "Material docente", "pages": [8, 15]},
        "Material docente, páginas 8 y 15",
        [],
    ],
)
def test_bibliographic_shapes_remain_untrusted_metadata(references):
    verdict = WebControlVerdict.model_validate(
        {
            "status": "sufficient",
            "reason": "Unchanged advisory decision",
            "concept": "nonfunctional requirements",
            "references": references,
        }
    )
    assert verdict.status == "sufficient" and verdict.references == references


def test_unknown_semantic_status_is_still_rejected():
    with pytest.raises(ValidationError):
        WebControlVerdict.model_validate({"status": "automatically_true", "reason": "test"})


@pytest.mark.parametrize(
    "control,statuses",
    [
        ("gap", "sufficient/needs_web/unknown/outside"),
        ("support", "supported/rejected/unknown"),
        ("compatibility", "compatible/conflict/unknown"),
    ],
)
def test_host_selects_control_in_trusted_instruction(control, statuses):
    request = WebControlRequest(
        purpose="explicacion",
        instruction="control",
        question="Consulta académica",
        control=control,
        evidence=[],
    )
    system = request.effective_messages()[0]["content"]
    assert f"Tarea actual del host: {control}" in system
    assert system.endswith(f"Esta llamada solo admite status: {statuses}.\n")
