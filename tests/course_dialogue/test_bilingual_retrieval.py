"""Vocabulary normalization is a retrieval aid, never semantic certification."""

from oralia.course_dialogue.retrieval_terms import retrieval_terms


def test_technical_aliases_are_symmetric_and_do_not_inflate_duplicate_concepts():
    assert retrieval_terms("presupuesto tecnología") == retrieval_terms("budget technology")
    assert len(retrieval_terms("pruebas testing tests")) == 1
    assert retrieval_terms("stakeholders") == retrieval_terms("interesados")


def test_unlisted_terms_are_preserved_and_no_query_phrase_table_is_needed():
    assert retrieval_terms("ornitorrinco") == {"ornit"}
    assert retrieval_terms("presupuesto ornitorrinco") > retrieval_terms("budget")


def test_expansion_can_recover_complementary_document_without_single_term_noise():
    from test_rag_lab import page

    from oralia.course_dialogue.document_evidence import build_units
    from oralia.course_dialogue.local_expansion import retrieve_with_local_expansion

    pages = [
        page("a", "Alfa\nalfa beta gamma delta\n"),
        page("b", "Beta\nalfa beta\n"),
        page("noise", "Ruido\nalfa ornitorrinco\n"),
    ]
    result = retrieve_with_local_expansion(
        build_units(pages), pages, "alfa beta gamma delta", lexical_profile="bilingual-v1", insufficient=True
    )
    assert {unit.document_id for unit in result.initial.units} == {"a.pdf"}
    assert {unit.document_id for unit in result.delivered.units} == {"a.pdf", "b.pdf"}
    assert result.semantic_sufficiency == "unverified"
