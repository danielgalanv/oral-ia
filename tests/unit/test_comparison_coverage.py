from oralia.documentary.comparison_coverage import diversify, facets


def fixture():
    texts = [
        ("General", "alfa beta context"),
        ("Alfa", "alfa explanation"),
        ("General", "alfa context"),
        ("Beta", "beta explanation"),
    ]
    pages = {
        str(i): {"id": str(i), "section": title, "text": title + " " + text}
        for i, (title, text) in enumerate(texts)
    }
    index = {str(i): {"page_id": str(i)} for i in range(4)}
    return list(index), index, pages


def test_candidate_diversity_uses_both_facets_without_new_ids_or_mutation():
    ranked, index, pages = fixture()
    order, metadata = diversify(ranked, index, pages, "¿Qué diferencia hay entre alfa y beta?")
    assert order[:2] == ["1", "3"]
    assert set(order) == set(ranked) and ranked == ["0", "1", "2", "3"]
    assert metadata["semantic_support"] == "unverified"
    assert metadata["unmatched_facets"] == []


def test_missing_side_is_not_replaced_by_generic_context_and_focus_discards_history():
    ranked, index, pages = fixture()
    _, metadata = diversify(ranked, index, pages, "Compara entre alfa y gamma")
    assert len(metadata["unmatched_facets"]) == 1
    history = ["Diferencia entre alfa y beta"]
    assert facets("Explícalo de otra manera", history)
    assert facets("Ahora otro tema", history, focus_change=True) == []
    unchanged, metadata = diversify(ranked, index, pages, "Un ejemplo sencillo")
    assert unchanged == ranked and metadata["promoted_candidates"] == []


def test_opt_in_packing_keeps_page_limit_and_reports_excluded_candidates():
    from types import SimpleNamespace

    from oralia.documentary.retrieval import Retrieval, digest

    ranked, index, pages = fixture()
    retrieval = object.__new__(Retrieval)
    retrieval.selection_profile = "comparison-coverage/v1"
    retrieval.config = {"strategies": ["lexical"], "candidates": 4, "context_units": 1, "context_chars": 1000}
    retrieval.limit = 512
    retrieval.tokenizer = SimpleNamespace(encode=lambda *args, **kwargs: [1])
    retrieval.revalidate = lambda: None
    retrieval.fragments = [
        {"id": identifier, "page_id": identifier, "text": pages[identifier]["text"]} for identifier in ranked
    ]
    retrieval.by_id = {f["id"]: f for f in retrieval.fragments}
    for identifier, page in pages.items():
        page.update(
            document_id="doc",
            page=int(identifier) + 1,
            raw_text=page["text"],
            text_sha256=digest(page["text"].encode()),
            derivation="synthetic",
        )
    retrieval.pages = pages
    retrieval.documents = {
        "doc": {
            "id": "doc",
            "filename": "fixture.pdf",
            "original": "fixture.pdf",
            "author": "fixture",
            "edition": "fixture",
            "sha256": "fixture",
        }
    }
    retrieval.fingerprint = {"revision": "fixture"}
    result = retrieval.query("Diferencia entre alfa y beta", "lexical")
    assert len(result["passages"]) == 1
    assert result["passages"][0]["text"] == pages[result["passages"][0]["id"]]["text"]
    assert len(result["omitted_context"]) == 3
    assert all(row["reason"] == "context unit limit" for row in result["omitted_context"])
    assert result["sufficiency"] == "not_assessed"


def test_comparison_prefers_purpose_over_techniques_and_individual_checklist():
    # Unrelated concepts/IDs: do not teach the known answer through page exceptions.
    rows = [
        ("Revisar contratos", "Modelo de calidad para cada cláusula individualmente"),
        ("Negociar contratos: técnicas", "Reuniones y prototipos para negociar contratos"),
        ("Revisar contratos", "Objetivo: comprobar la calidad del documento completo"),
        ("Negociar contratos", "Objetivo: acordar las necesidades de ambas partes"),
    ]
    pages = {str(i): dict(id=str(i), section=h, text=h + "\n" + t) for i, (h, t) in enumerate(rows)}
    index = {key: {"page_id": key} for key in pages}
    order, _ = diversify(list(index), index, pages, "Diferencia entre revisar y negociar contratos")
    assert order[:2] == ["2", "3"]
    assert set(order) == set(index)


def test_explicit_new_question_does_not_inherit_old_comparison():
    assert facets("¿Cómo compruebo que una factura se guarda?", ["Diferencia entre alfa y beta"]) == []


def test_comparison_without_between_is_not_treated_as_no_facets():
    ranked, index, pages = fixture()
    order, metadata = diversify(ranked, index, pages, "¿En qué se diferencian alfa y beta?")
    assert order[:2] == ["1", "3"]
    assert len(metadata["facets"]) == 2
