"""Course-specific evaluation oracles, never generation/routing rules."""

from oralia.course_dialogue.evaluation import inspect_pedagogy


def test_general_objective_does_not_pass_conflict_oracle_even_with_grounding():
    row = {
        "parsed_candidate": {
            "segments": [
                {
                    "kind": "paraphrase",
                    "text": "Verificar la calidad de los requisitos cumple el modelo de calidad.",
                }
            ],
            "context": {"pending_question": None},
        },
        "verification": {"source_checks": True},
        "stage": "switch",
    }
    report = inspect_pedagogy(row, "development", [])
    assert not report["automatic_checks"]["conflict_requires_resolution_action"]
    assert report["human_review"] == "pending"
    assert not report["acceptance"]


def test_reference_checks_never_imply_comprehension_or_human_acceptance():
    report = inspect_pedagogy(
        {
            "raw_candidate": "necesidades clientes calidad",
            "verification": {"source_checks": True},
            "stage": "first",
        },
        "development",
        [],
    )
    assert not report["acceptance"]


def test_changed_strategy_metadata_cannot_hide_identical_explanation():
    old = {
        "input": "Qué significa validar",
        "parsed_candidate": {
            "segments": [{"kind": "paraphrase", "text": "Definición repetida"}],
            "context": {"strategy": "first"},
        },
    }
    row = {
        "input": "No entiendo",
        "stage": "followup",
        "parsed_candidate": {
            "segments": [{"kind": "paraphrase", "text": "Definición repetida"}],
            "context": {"strategy": "different label", "pending_question": "Qué significa validar"},
        },
        "verification": {"source_checks": True},
    }
    checks = inspect_pedagogy(row, "development", [old])["automatic_checks"]
    assert not checks["different_observable_strategy"]
    assert not checks["question_present_and_not_input_echo"]


def test_client_word_alone_cannot_pass_reserved_correction():
    row = {
        "stage": "correction",
        "parsed_candidate": {
            "segments": [
                {
                    "kind": "paraphrase",
                    "text": "Sin contradicciones sabemos que cumple necesidades del cliente.",
                }
            ],
            "context": {},
        },
        "verification": {"source_checks": True},
    }
    report = inspect_pedagogy(row, "reserved", [])
    assert not report["automatic_checks"]["noncontradiction_not_sufficient_marker"]
    assert not report["acceptance"]
