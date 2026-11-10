"""Local expansion keeps evidence bounded and leaves semantic judgment open."""

import hashlib

import pytest

from oralia.course_dialogue.document_evidence import RetrievalBudget, build_units
from oralia.course_dialogue.local_expansion import retrieve_with_local_expansion


def page(key, text):
    filename = f"{key}.pdf"
    return {
        "id": f"{key}:1",
        "filename": filename,
        "original_sha256": hashlib.sha256(filename.encode()).hexdigest(),
        "version": 1,
        "page": 1,
        "text": text,
    }


def test_expansion_requires_signal_and_preserves_visible_history():
    pages = [
        page("requisitos", "Requisitos\nLa consistencia evita contradicciones.\n"),
        page("pruebas", "Pruebas\nLas pruebas de defectos descubren fallos.\n"),
    ]
    units = build_units(pages)
    narrow = RetrievalBudget(max_chars=200, max_units=1, max_seed_units=1, max_neighbors=0)
    wide = RetrievalBudget(max_chars=500, max_units=2, max_seed_units=2, max_neighbors=1)
    first = retrieve_with_local_expansion(
        units,
        pages,
        "pruebas defectos",
        displayed_history=("requisitos consistencia",),
        initial_budget=narrow,
        expanded_budget=wide,
    )
    assert first.expanded is None and first.delivered is first.initial
    second = retrieve_with_local_expansion(
        units,
        pages,
        "pruebas defectos",
        displayed_history=("requisitos consistencia",),
        insufficient=True,
        initial_budget=narrow,
        expanded_budget=wide,
    )
    assert second.expanded is not None
    assert second.delivered.units[0] == first.initial.units[0]
    assert second.reason == "external_insufficiency_signal"
    assert second.semantic_sufficiency == "unverified"
    assert not second.publication_allowed
    assert any(row["decision"] == "selected" for row in second.expanded.trace)


def test_elliptic_followup_keeps_referent_and_explicit_focus_change_drops_it():
    pages = [
        page("req", "Requisitos\nLa consistencia evita contradicciones.\n"),
        page("test", "Pruebas\nLos casos de prueba encuentran defectos.\n"),
    ]
    units = build_units(pages)
    followup = retrieve_with_local_expansion(
        units,
        pages,
        "¿Por qué?",
        displayed_history=("Explícame consistencia en requisitos",),
        insufficient=True,
    )
    assert any(unit.document_id == "req.pdf" for unit in followup.delivered.units)
    assert any(unit.document_id == "req.pdf" for unit in followup.expanded.units)
    changed = retrieve_with_local_expansion(
        units,
        pages,
        "Ahora, pruebas y defectos",
        displayed_history=("consistencia requisitos",),
        focus_change=True,
        insufficient=True,
    )
    assert all(unit.document_id != "req.pdf" for unit in changed.delivered.units)


def test_expansion_retains_initial_support_and_reports_added_or_omitted():
    pages = [
        page("a", "Requisitos\nLa consistencia evita contradicciones.\n"),
        page("b", "Requisitos\nLa completitud incluye funciones necesarias.\n"),
    ]
    units = build_units(pages)
    result = retrieve_with_local_expansion(
        units,
        pages,
        "requisitos consistencia completitud",
        insufficient=True,
        initial_budget=RetrievalBudget(max_chars=200, max_units=1, max_seed_units=1, max_neighbors=0),
        expanded_budget=RetrievalBudget(max_chars=400, max_units=2, max_seed_units=2, max_neighbors=0),
    )
    assert {unit.document_id for unit in result.delivered.units} == {"a.pdf", "b.pdf"}
    assert len({unit.id for unit in result.delivered.units}) == len(result.delivered.units)
    assert any(row["decision"] == "retained_initial" for row in result.delivered.trace)
    assert any(row["decision"] == "added_expanded" for row in result.delivered.trace)


def test_sparse_and_conflicting_evidence_is_never_certified():
    pages = [
        page("a", "Reglas\nSe permiten globos azules.\n"),
        page("b", "Reglas\nSe permiten globos rojos.\n"),
    ]
    result = retrieve_with_local_expansion(
        build_units(pages), pages, "globos azules y rojos", insufficient=True
    )
    assert len(result.delivered.units) == 2
    assert result.semantic_sufficiency == "unverified"
    assert not result.publication_allowed
    empty = retrieve_with_local_expansion(build_units(pages), pages, "química nuclear", insufficient=True)
    assert empty.delivered.units == ()
    assert empty.semantic_sufficiency == "unverified"


def test_changed_source_and_bad_budget_fail_closed():
    pages = [page("a", "Tema\nLa evidencia original permanece.\n")]
    units = build_units(pages)
    changed = [dict(pages[0], text="Tema\nOtra cosa.\n")]
    with pytest.raises(ValueError, match="source span changed"):
        retrieve_with_local_expansion(units, changed, "evidencia", insufficient=True)
    with pytest.raises(ValueError, match="outside authorized catalog"):
        retrieve_with_local_expansion(units, [], "evidencia", insufficient=True)
    with pytest.raises(ValueError, match="must not shrink"):
        retrieve_with_local_expansion(
            units,
            pages,
            "evidencia",
            insufficient=True,
            initial_budget=RetrievalBudget(max_chars=500),
            expanded_budget=RetrievalBudget(max_chars=200),
        )
    with pytest.raises(ValueError, match="explicit boolean"):
        retrieve_with_local_expansion(units, pages, "evidencia", insufficient="yes")
