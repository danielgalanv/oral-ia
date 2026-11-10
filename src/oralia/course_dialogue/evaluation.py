"""Negative-capable evaluation rubric, independent of generator and authorization.

These automatic checks are necessary observations, not an entailment proof or
human acceptance. They are never consulted to generate or authorize a response.
"""

import re

from oralia.domain.materials.query_excerpt import normalized


def observe_controlled(row, expected, prior=None):
    """Necessary, negative-capable observations, never a publication/semantic verdict.

    Expectations belong to the evaluator and are never sent to the model. These
    bounded lexical/state observations cannot replace reviewing an actual claim.
    """
    actual = row.get("actual_preview", {})
    text = normalized(actual.get("candidate_text", ""))
    state = row.get("state_after", {})
    before = row.get("state_before", {})

    def groups_present(groups, value):
        return all(any(normalized(word) in value for word in group) for group in groups)

    refs = {r.get("source_id") for r in actual.get("source_refs", [])}
    checks = {
        "completed_preview": row.get("agent_result", {}).get("status") == "ok" and bool(text),
        "publication_denied": actual.get("publication_allowed") is False,
        "sources_present": bool(refs),
        "source_relevance_observation": bool(refs & set(expected.get("source_any", refs))),
        "required_concepts": groups_present(expected.get("concept_groups", []), text),
        "expected_goal": state.get("current_goal") in expected.get("goals", [expected.get("goal")]),
        "no_grade_or_mastery": state.get("assessment") == "not_assessed"
        and not any(
            phrase in text
            for phrase in ["tu nota", "has aprobado", "dominas el tema", "has demostrado comprender"]
        ),
    }
    if "goal_pair" in expected:
        actual_pair = {state.get("current_goal"), state.get("comparison_goal_ref")} - {None}
        checks["expected_goal_pair"] = len(actual_pair) == 2 and actual_pair == set(expected["goal_pair"])
    if expected.get("single_goal_only"):
        checks["single_goal_only"] = state.get("comparison_goal_ref") is None
    if expected.get("preserve_goal_pair"):
        checks["goal_pair_preserved"] = (state.get("current_goal"), state.get("comparison_goal_ref")) == (
            before.get("current_goal"),
            before.get("comparison_goal_ref"),
        )
    if row.get("stage") in {"followup", "repeat"}:
        questions = re.findall(r"¿([^?]+)\?", actual.get("candidate_text", ""))
        question = normalized(questions[-1]) if questions else ""
        input_questions = [normalized(q) for q in re.findall(r"¿([^?]+)\?", row.get("input", ""))]
        checks["concrete_question"] = bool(
            question
            and groups_present(expected.get("question_groups", []), question)
            and question != normalized(row.get("input", "")).strip("¿?")
            and question not in input_questions
            and question not in {"lo entiendes", "entiendes"}
        )
        checks["pending_question"] = bool(state.get("pending_question_id"))
        checks["referent_preserved"] = before.get("current_goal") == state.get("current_goal")
        if prior is not None:
            old = normalized(prior.get("actual_preview", {}).get("candidate_text", ""))
            checks["different_text_strategy"] = bool(text and text != old)
    if expected.get("requires_example_after_explanation"):
        position = text.find("ejemplo hipotetico")
        checks["explanation_before_example"] = position >= 30 and groups_present(
            expected.get("concept_groups", []), text[:position]
        )
    if expected.get("requires_non_equivalence"):
        checks["non_equivalence_observation"] = any(
            marker in text
            for marker in [
                "no equivale",
                "no basta",
                "no garantiza",
                "no demuestra",
                "no se reduce",
                "no define",
                "no justifica",
                "no deben darse",
            ]
        )
    return {
        "automatic_checks": checks,
        "automatic_all_pass": all(checks.values()),
        "human_review": "pending",
        "independent_semantics": "not_accredited",
        "acceptance": False,
    }


def inspect_pedagogy(row, partition, prior):
    parsed = row.get("parsed_candidate", {})
    segments = parsed.get("segments", [])
    text = normalized(" ".join(s["text"] for s in segments))
    stage = row.get("stage")
    checks = {
        "candidate_contract": bool(parsed),
        "source_witnesses": bool(row.get("verification", {}).get("source_checks")),
    }
    kinds = [s["kind"] for s in segments]
    if stage == "followup":
        checks["explanation_before_hypothetical_example"] = (
            "paraphrase" in kinds
            and "illustrative_example" in kinds
            and kinds.index("paraphrase") < kinds.index("illustrative_example")
        )
        question = parsed.get("context", {}).get("pending_question") or ""
        echoed_inputs = [normalized(row.get("input", "")) for row in [*prior, row]]
        checks["question_present_and_not_input_echo"] = bool(
            question and normalized(question) not in echoed_inputs
        )
        previous = prior[-1].get("parsed_candidate", {}).get("context", {}) if prior else {}
        old_text = (
            normalized(" ".join(s["text"] for s in prior[-1].get("parsed_candidate", {}).get("segments", [])))
            if prior
            else ""
        )
        checks["different_observable_strategy"] = bool(
            parsed
            and parsed.get("context", {}).get("strategy") != previous.get("strategy")
            and text
            and text != old_text
        )
    if stage == "switch" and partition == "development":
        checks["conflict_requires_resolution_action"] = any(
            w in text for w in ["negoci", "prioriz", "resolver", "resolv"]
        )
    if stage == "correction" and partition == "reserved":
        checks["noncontradiction_not_sufficient_marker"] = any(
            marker in text for marker in ["no basta", "no implica", "no garantiza", "no necesariamente"]
        )
    if stage == "first":
        checks["needs_not_numeric_validation"] = any(w in text for w in ["necesidad", "cliente", "usuario"])
    return {
        "automatic_checks": checks,
        "automatic_all_pass": all(checks.values()),
        "human_review": "pending",
        "independent_semantics": "not_accredited",
        "acceptance": False,
    }
