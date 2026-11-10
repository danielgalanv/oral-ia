"""Valid source/authority metadata cannot make irrelevant teaching pass an oracle."""

from oralia.course_dialogue.evaluation import observe_controlled


def row(text):
    return {
        "stage": "followup",
        "input": "No entiendo la diferencia.",
        "agent_result": {"status": "ok"},
        "actual_preview": {
            "candidate_text": text,
            "publication_allowed": False,
            "unit_ids": ["VALID-ID"],
            "source_refs": [{"source_id": "procedure:11"}],
        },
        "state_before": {"current_goal": "calidad_individual"},
        "state_after": {
            "current_goal": "calidad_individual",
            "assessment": "not_assessed",
            "pending_question_id": "VALID-QUESTION",
        },
    }


EXPECT = {
    "goal": "calidad_individual",
    "concept_groups": [["constru", "implement"], ["prueb", "comprob"]],
    "question_groups": [["prueb", "comprob"]],
    "source_any": ["procedure:11"],
    "requires_example_after_explanation": True,
}


def test_grounded_generic_goal_does_not_pass_content_or_question_observations():
    actual = row("El objetivo general es estudiar requisitos. ¿Lo entiendes?")
    report = observe_controlled(actual, EXPECT)
    assert report["automatic_checks"]["sources_present"] is True
    assert report["automatic_checks"]["required_concepts"] is False
    assert report["automatic_checks"]["concrete_question"] is False
    assert report["automatic_all_pass"] is False and report["acceptance"] is False


def test_hypothetical_before_explanation_is_rejected_despite_matching_ids():
    actual = row("Ejemplo hipotético: podemos construir. Luego hay que definir pruebas. ¿Cómo comprobarlo?")
    report = observe_controlled(actual, EXPECT)
    assert report["automatic_checks"]["explanation_before_example"] is False
    assert report["automatic_all_pass"] is False


def test_metadata_cannot_hide_repeated_text_or_a_grade():
    text = (
        "Construir requiere recursos y comprobar requiere pruebas. "
        "Ejemplo hipotético: una interfaz. ¿Cómo comprobarlo? Tu nota es diez."
    )
    actual = row(text)
    report = observe_controlled(actual, EXPECT, prior=row(text))
    assert report["automatic_checks"]["different_text_strategy"] is False
    assert report["automatic_checks"]["no_grade_or_mastery"] is False


def test_primary_goal_and_valid_sources_do_not_hide_an_unsolicited_secondary_goal():
    actual = row("Construir requiere recursos y comprobar requiere pruebas. ¿Cómo comprobarlo?")
    actual["state_after"]["comparison_goal_ref"] = "no_ambiguedad"
    report = observe_controlled(actual, {**EXPECT, "single_goal_only": True, "preserve_goal_pair": True})
    assert report["automatic_checks"]["expected_goal"] is True
    assert report["automatic_checks"]["single_goal_only"] is False
    assert report["automatic_checks"]["goal_pair_preserved"] is False
    assert report["acceptance"] is False


def test_echo_of_embedded_input_question_is_not_a_comprehension_question():
    actual = row(
        "Construir requiere recursos; comprobar requiere una prueba. "
        "Ejemplo hipotético: una interfaz. ¿Cómo comprobarlo?"
    )
    actual["input"] = "No entiendo. ¿Cómo comprobarlo?"
    report = observe_controlled(actual, EXPECT)
    assert report["automatic_checks"]["concrete_question"] is False


def test_a_valid_single_goal_cannot_pass_a_required_relation():
    actual = row("Construir y comprobar no son lo mismo que interpretar sin ambigüedad.")
    expected = {
        "goals": ["calidad_individual", "no_ambiguedad"],
        "goal_pair": ["calidad_individual", "no_ambiguedad"],
    }
    report = observe_controlled(actual, expected)
    assert report["automatic_checks"]["expected_goal"] is True
    assert report["automatic_checks"]["expected_goal_pair"] is False
    actual["state_after"]["comparison_goal_ref"] = "no_ambiguedad"
    report = observe_controlled(actual, expected)
    assert report["automatic_checks"]["expected_goal_pair"] is True
    assert report["acceptance"] is False
