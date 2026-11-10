"""CPU receipt regression: preserve diagnostic failure before stopping, no model."""

import json

import pytest

from scripts import run_study_review_probe as runner


def test_missing_citation_is_persisted_before_protocol_stop(tmp_path):
    record = {"outcome": {"text": "Synthetic answer without citations"}}
    records = [record]
    output = tmp_path / "records.json"
    with pytest.raises(ValueError, match="invalid citations"):
        runner.persist_citation_check(record, {"source:1"}, records, output)
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved[0]["citation_check"] == {"missing": True, "foreign": [], "semantic_support": "unverified"}


def test_foreign_and_known_citations_do_not_become_semantic_verdicts(tmp_path):
    for text, foreign in [("Synthetic [foreign]", ["foreign"]), ("Synthetic [source:1]", [])]:
        record = {"outcome": {"text": text}}
        output = tmp_path / ("foreign.json" if foreign else "known.json")
        if foreign:
            with pytest.raises(ValueError, match="invalid citations"):
                runner.persist_citation_check(record, {"source:1"}, [record], output)
        else:
            runner.persist_citation_check(record, {"source:1"}, [record], output)
        check = json.loads(output.read_text(encoding="utf-8"))[0]["citation_check"]
        assert check["foreign"] == foreign
        assert check["semantic_support"] == "unverified"
