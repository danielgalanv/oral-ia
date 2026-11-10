"""Readable consulted sources are presentation, never semantic authorization."""

import pytest
from test_lab_conversation import setup
from test_rag_lab import ProviderFixture, page

from oralia.course_dialogue.document_evidence import build_units


@pytest.mark.asyncio
async def test_answer_without_technical_citations_has_readable_consulted_sources():
    provider = ProviderFixture("Texto sintético sin identificadores técnicos.")
    lab, _, _ = setup(provider=provider)
    row = await lab.turn("consistencia requisitos")
    assert row["displayed_kind"] == "laboratory_preview"
    assert row["citation_check"]["missing"] is True
    assert "Fuentes consultadas: req.pdf" in row["displayed_text"]
    assert "id exacto" not in provider.requests[0].instruction
    assert "[id]" not in provider.requests[0].instruction
    assert row["source_presentation"]["claim_support_verified"] is False
    assert row["publication_allowed"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["rejected", "unknown"])
async def test_readable_reference_cannot_override_substantive_review(status):
    lab, _, _ = setup(status=status, provider=ProviderFixture("Texto sintético sin citas."))
    row = await lab.turn("consistencia requisitos")
    assert row["displayed_kind"] == "operational"
    assert row["laboratory_preview"] is None
    assert "Texto sintético" not in row["displayed_text"]
    assert row["reason"] == "post_review_" + status


def test_host_references_deduplicate_documents_preserve_exact_internal_units():
    from oralia.course_dialogue.reference_presentation import consulted_sources

    pages = [page("req", "Requisitos\nPrimer párrafo.\n\nSegundo párrafo.\n")]
    units = build_units(pages)
    result = consulted_sources(units)
    assert len(result["documents"]) == 1
    assert result["documents"][0]["unit_ids"] == [u.id for u in units]
    assert all(u.id not in result["display_text"] for u in units)
    assert result["selection"] == "documents_of_evidence_delivered_to_generator"
    assert result["claim_support_verified"] is False
