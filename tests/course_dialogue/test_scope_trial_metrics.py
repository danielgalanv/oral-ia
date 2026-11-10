"""Stop metrics never misclassify unexecuted cases as semantic failures."""

from types import SimpleNamespace

from scripts.trial_course_scope import compute_pids, evaluate, metrics


def test_no_calls_is_not_twenty_failures():
    result = metrics([])
    assert result["executed"] == result["incorrect_executed"] == 0
    assert result["not_executed"] == 20
    assert result["matrix"] == {}


def test_early_stop_counts_only_executed():
    rows = [dict(expected="in_scope", actual="out_of_scope", correct=False)]
    result = metrics(rows)
    assert result["not_executed"] == 19
    assert result["incorrect_executed"] == result["false_exclusions"] == 1


def test_valid_offsets_with_wrong_semantic_split_fail_frozen_oracle():
    expected = dict(
        status="mixed",
        included_block="pruebas",
        excluded_block="seguridad",
        included_quote="Explica pruebas",
        excluded_quote="curso de seguridad",
    )
    selection = SimpleNamespace(
        status="mixed",
        included_block="pruebas",
        excluded_block="seguridad",
        referent_turn=None,
        excluded=SimpleNamespace(quote="curso de seguridad"),
    )
    result = SimpleNamespace(selection=selection, rag_question="Explica pruebas y curso de seguridad")
    row = evaluate({"id": "synthetic"}, expected, result)
    assert row["critical"] and not row["correct"]


def test_desktop_contexts_are_distinct_from_compute():
    assert compute_pids({"process_table": "| 0 N/A N/A 123 C+G desktop.exe N/A |"}) == []
    assert compute_pids({"process_table": "| 0 N/A N/A 456 C python.exe N/A |"}) == [456]
