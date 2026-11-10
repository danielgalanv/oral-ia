"""Whole-unit documentary context remains traceable and has no approval authority."""

import hashlib
from dataclasses import replace

import pytest

from oralia.course_dialogue.document_evidence import (
    RetrievalBudget,
    build_units,
    retrieve_units,
)
from oralia.course_dialogue.evidence_sets import (
    MultiPassageReview,
    PassageWitness,
    ReviewBudget,
    validate_review_set,
)


def page(key, number, text, *, document=None, **extra):
    name = document or f"{key}.pdf"
    return {
        "id": f"{key}:{number}",
        "filename": name,
        "original_sha256": hashlib.sha256(name.encode()).hexdigest(),
        "version": 1,
        "page": number,
        "text": text,
        **extra,
    }


def test_wrapped_paragraph_complete_list_and_explicit_cross_page_continuation():
    pages = [
        page(
            "one",
            1,
            "Requisitos\nUn requisito claro expresa una conducta\ny sus condiciones.\n\n"
            "• Primera condición\nque ocupa otra línea\n• Segunda condición\n",
            document="course.pdf",
        ),
        page(
            "one",
            2,
            "Requisitos (continuación)\n• Tercera condición\ny su matiz.\n",
            document="course.pdf",
            continues_from_previous=True,
        ),
    ]
    units = build_units(pages)
    assert [unit.kind for unit in units] == ["paragraph", "list"]
    assert "conducta\ny sus condiciones" in units[0].text
    assert "Primera condición\nque ocupa otra línea" in units[1].text
    assert "Tercera condición\ny su matiz" in units[1].text
    assert [span.page_id for span in units[1].positions] == ["one:1", "one:2"]
    for unit in units:
        for span in unit.positions:
            source = next(source for source in pages if source["id"] == span.page_id)
            assert source["text"][span.start : span.end] in unit.text


def test_unjustified_continuation_is_rejected_and_table_keeps_box_and_rows():
    first = page("a", 1, "Título\nTexto inicial.\n", document="course.pdf")
    distant = page("a", 3, "Título\nTexto final.\n", document="course.pdf", continues_from_previous=True)
    with pytest.raises(ValueError, match="continuation"):
        build_units([first, distant])
    table_page = page(
        "table",
        1,
        "Tabla de criterios\n",
        tables=[{"bbox": (10, 20, 100, 80), "rows": [["Criterio", "Valor"], ["plazo", "60 s"]]}],
    )
    table = build_units([table_page])[0]
    assert table.kind == "table" and "plazo | 60 s" in table.text
    assert table.positions[0].bbox == (10, 20, 100, 80)


def test_retrieval_uses_complementary_documents_and_excludes_focus_distractor():
    pages = [
        page("a", 1, "Testing\nLas pruebas de defectos buscan fallos y anomalías.\n"),
        page("b", 1, "Testing\nLa validación de defectos contrasta resultados de pruebas.\n"),
        page("c", 1, "Contratos\nLa revisión de requisitos trata pagos y contratos.\n"),
    ]
    units = build_units(pages)
    result = retrieve_units(
        units,
        pages,
        "pruebas defectos validación",
        displayed_history=("requisitos contratos",),
        focus_change=True,
        budget=RetrievalBudget(max_chars=1000, max_units=3, max_seed_units=3, max_neighbors=0),
    )
    assert {unit.document_id for unit in result.units} == {"a.pdf", "b.pdf"}
    assert result.catalog_page_ids == ("a:1", "b:1", "c:1")
    assert result.scope == "authorized_ingested_catalog_only_not_complete_course"


def test_neighbor_and_budget_preserve_whole_units_with_omission_trace():
    pages = [
        page(
            "a",
            1,
            "Defectos\nPruebas de defectos encuentran errores y anomalías en casos "
            "diseñados para exponer fallos concretos del sistema.\n",
            document="same.pdf",
        ),
        page("a", 2, "Contexto\nLos casos raros no representan el uso normal.\n", document="same.pdf"),
    ]
    units = build_units(pages)
    result = retrieve_units(
        units,
        pages,
        "pruebas defectos",
        budget=RetrievalBudget(max_chars=500, max_units=2, max_seed_units=1, max_neighbors=1),
    )
    assert [unit.positions[0].page_id for unit in result.units] == ["a:1", "a:2"]
    assert any(row.get("reason") == "adjacent_context" for row in result.trace)
    tight = retrieve_units(
        units,
        pages,
        "pruebas defectos",
        budget=RetrievalBudget(max_chars=len(units[0].text), max_units=2, max_seed_units=1, max_neighbors=1),
    )
    assert tight.units == (units[0],)
    assert any(row["decision"] == "omitted_budget" for row in tight.trace)


def test_conflicting_sources_are_both_preserved_without_truth_vote():
    pages = [
        page("a", 1, "Validación\nLa validación siempre detecta ambigüedad.\n"),
        page("b", 1, "Validación\nLa validación no siempre detecta ambigüedad.\n"),
    ]
    result = retrieve_units(build_units(pages), pages, "validación detecta ambigüedad")
    assert len(result.units) == 2
    assert any("siempre detecta" in unit.text for unit in result.units)
    assert any("no siempre detecta" in unit.text for unit in result.units)


def test_retrieval_rejects_foreign_or_rewritten_unit_before_ranking():
    pages = [page("a", 1, "Título\nLas pruebas encuentran defectos.\n")]
    unit = build_units(pages)[0]
    with pytest.raises(ValueError, match="outside authorized"):
        retrieve_units((unit,), [], "pruebas defectos")
    rewritten = replace(unit, text="Las pruebas siempre encuentran defectos.")
    rewritten = replace(rewritten, text_sha256=hashlib.sha256(rewritten.text.encode()).hexdigest())
    with pytest.raises(ValueError, match="source text changed"):
        retrieve_units((rewritten,), pages, "pruebas defectos")


def test_bilingual_testing_retrieval_does_not_force_weak_document_diversity():
    pages = [
        page("procedure", 1, "Validación\nLa validación de requisitos considera pruebas.\n"),
        page("testing", 1, "Testing\nDefect testing and validation testing have different goals.\n"),
        page("testing", 2, "Testing\nValidation testing and defect testing use different cases.\n"),
    ]
    result = retrieve_units(build_units(pages), pages, "pruebas defectos validación")
    assert {unit.document_id for unit in result.units} == {"testing.pdf"}
    assert any(row["decision"] == "not_selected_low_relevance" for row in result.trace)


def test_multi_passage_and_premise_record_checks_provenance_without_entailment():
    pages = [
        page("a", 1, "Testing\nLas pruebas de defectos exponen fallos.\n"),
        page("b", 1, "Testing\nLos casos raros no prueban el uso normal.\n"),
    ]
    units = build_units(pages)
    answer = (
        "Supongamos que un caso raro falla. Los casos habituales aún no se probaron. "
        "Un fallo raro evidencia un defecto, pero no garantiza el uso normal."
    )
    quote = "Un fallo raro evidencia un defecto, pero no garantiza el uso normal."
    witnesses = tuple(PassageWitness(unit.id, 0, len(unit.text), unit.text) for unit in units)
    review = MultiPassageReview(
        answer_start=answer.index(quote),
        answer_end=answer.index(quote) + len(quote),
        claim_quote=quote,
        claim_type="inference",
        status="supported",
        passages=witnesses,
        premise_quotes=(
            "Supongamos que un caso raro falla.",
            "Los casos habituales aún no se probaron.",
        ),
        rationale="Etiqueta humana por comprobar; no es aprobación",
    )
    sources = {item["id"]: item for item in pages}
    validate_review_set(answer, review, units, sources)
    with pytest.raises(ValueError, match="budget"):
        validate_review_set(answer, review, units, sources, ReviewBudget(max_passages=1))
    with pytest.raises(ValueError, match="outside retrieved"):
        validate_review_set(
            answer, replace(review, passages=(replace(witnesses[0], unit_id="foreign"),)), units, sources
        )
    with pytest.raises(ValueError, match="identity"):
        corrupted = {**sources, "a:1": {**sources["a:1"], "original_sha256": "changed"}}
        validate_review_set(answer, review, units, corrupted)
    with pytest.raises(ValueError, match="unknown"):
        validate_review_set(answer, replace(review, conflict_unresolved=True), units, sources)
    validate_review_set(
        answer,
        replace(review, status="unknown", conflict_unresolved=True, rationale="Fuentes discrepantes"),
        units,
        sources,
    )
