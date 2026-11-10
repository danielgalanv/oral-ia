import pytest

from oralia.application.orchestration.defense_agency_composer import (
    _combined_action,
    _structurally_relevant,
)


@pytest.mark.parametrize(
    ("concept", "concepts", "evidence", "expected"),
    [
        ("arquitectura", ["arquitectura modular"], [], True),
        ("aislamiento", [], [{"text": "El aislamiento de materiales es obligatorio."}], True),
        ("tema inventado", ["arquitectura"], [{"text": "Material autorizado"}], False),
        ("", ["arquitectura"], [], False),
    ],
)
def test_relevance_is_structural_membership(concept, concepts, evidence, expected):
    assert _structurally_relevant(concept, concepts, evidence) is expected


@pytest.mark.parametrize("grounding", ["no_fundamentada", "conflictiva", "no_verificable"])
@pytest.mark.parametrize("coherence", ["approved", "reformulate", "block"])
def test_unfounded_always_wins_over_coherence(grounding, coherence):
    assert _combined_action(grounding, coherence, True) == "acknowledge_missing_info"


def test_coherence_regeneration_requires_grounded_relevance():
    assert _combined_action("fundamentada", "reformulate", True) == "regenerate"
    assert _combined_action("fundamentada", "approved", False) == "acknowledge_missing_info"
    assert _combined_action("fundamentada", "approved", True) == "ask"
