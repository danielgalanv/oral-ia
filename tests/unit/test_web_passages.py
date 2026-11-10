"""Literal selection must find a late passage without rewriting its conditions."""

import hashlib

from oralia.documentary.web_evidence import extract_public, main_text_ranges
from oralia.documentary.web_passages import select_web_passages


def test_late_relevant_passage_keeps_adjacent_caveat_and_offsets():
    text = (
        "Navigation news unrelated landing content.\n" * 300
        + "Traceability connects requirements with design and tests.\n"
        + "This connection does not guarantee that a requirement is correct.\n"
        + "Other unrelated material.\n" * 300
    )
    result = select_web_passages(text, "Explain traceability", "requirements traceability", (), 2800)
    assert "Traceability connects" in result["text"]
    assert "does not guarantee" in result["text"]
    assert len(result["text"]) <= 2800 and result["omitted_ranges"]
    for span in result["spans"]:
        assert text[span["start"] : span["end"]] == span["text"]
        assert hashlib.sha256(span["text"].encode()).hexdigest() == span["sha256"]


def test_small_document_is_not_rejected_for_lexical_mismatch():
    text = "The stakeholders define their needs. Examples may use hypothetical numbers."
    result = select_web_passages(text, "¿Qué necesitan?", "requirements", (), 1000)
    assert result["text"] == text and not result["omitted_ranges"]


def test_giant_unbroken_atom_is_explicitly_omitted_without_truncation():
    result = select_web_passages("traceability" * 1000, "traceability", "requirements", (), 1000)
    assert result["text"] == "" and result["omitted_ranges"] == [[0, 12000]]


def test_missing_overlap_is_not_interpreted_as_outside_the_course():
    result = select_web_passages("Unrelated navigation.\n" * 500, "rendimiento", "performance", (), 1000)
    assert result["text"] == "" and "scope" not in result


def test_html_main_selection_omits_navigation_without_changing_extracted_source():
    body = (
        b"<nav>Requirements news menu</nav><main><h1>Requirements</h1><p>"
        + b"Stakeholders identify needs. " * 8
        + b"</p></main><footer>Requirements links</footer>"
    )
    text, _, _ = extract_public(body, "text/html")
    result = select_web_passages(
        text,
        "requirements",
        "requirements",
        (),
        800,
        preferred_ranges=main_text_ranges(body, "text/html", text),
    )
    assert "news menu" in text and "news menu" not in result["text"] and "links" not in result["text"]
    assert "Stakeholders identify" in result["text"] and result["omitted_ranges"]
    assert all(text[s["start"] : s["end"]] == s["text"] for s in result["spans"])
