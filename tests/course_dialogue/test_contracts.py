"""Candidate metadata never confers permission to publish a generated claim."""

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.contracts import Candidate, CandidateV2
from oralia.course_dialogue.verification import inspect_candidate


def sample(kind="paraphrase", text="Las necesidades del cliente orientan la validación."):
    return {
        "segments": [
            {
                "kind": kind,
                "text": text,
                "source_id": "p12",
                "source_quote": "necesidades de clientes",
                "assumptions": [],
            }
        ],
        "context": {
            "topic": "validación",
            "objective": "distinguir necesidades y calidad",
            "strategy": "definition",
            "pending_question": "¿Qué comprobarías con el cliente?",
        },
    }


def test_candidate_cannot_approve_itself():
    data = sample()
    data["reviewed"] = True
    with pytest.raises(ValidationError):
        Candidate.model_validate(data)


def test_valid_citation_is_not_semantic_proof_or_publication():
    report = inspect_candidate(Candidate.model_validate(sample()), {"p12": "Las necesidades de clientes"})
    assert report["source_checks"]
    assert not report["independent_semantics"]
    assert not report["publication_allowed"]


def test_literal_must_equal_its_source_witness():
    report = inspect_candidate(
        Candidate.model_validate(sample("literal")), {"p12": "necesidades de clientes"}
    )
    assert not report["source_checks"]


def test_invented_page_or_changed_quote_is_rejected():
    for sources in [{}, {"p12": "algo diferente"}]:
        assert not inspect_candidate(Candidate.model_validate(sample()), sources)["source_checks"]


def test_hypothetical_example_requires_explicit_assumptions():
    with pytest.raises(ValidationError):
        Candidate.model_validate(sample("illustrative_example"))


def test_missing_comprehension_and_topic_are_not_implicitly_filled():
    data = sample()
    del data["context"]["topic"]
    with pytest.raises(ValidationError):
        Candidate.model_validate(data)


def test_v2_example_requires_assumptions_and_orphans_are_not_displayed():
    base = {"answer": "Se revisa la consistencia.", "source_ids": ["p10"]}
    with pytest.raises(ValidationError):
        CandidateV2.model_validate({**base, "example": "Uno permite y otro prohíbe."})
    without_example = CandidateV2.model_validate({**base, "assumptions": ["Definición mal ubicada"]})
    assert "Definición mal ubicada" not in without_example.render_for_inspection()
    candidate = CandidateV2.model_validate(
        {**base, "example": "Uno permite y otro prohíbe.", "assumptions": ["Misma condición de acceso"]}
    )
    assert "Ejemplo hipotético:" in candidate.render_for_inspection()
