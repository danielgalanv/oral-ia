from oralia.course_dialogue.concept_ledger import NOTICE_KINDS
from oralia.course_dialogue.review_notice import GUIDANCE, MESSAGES, build_notice


def trace(status, *checks):
    return dict(
        status=status,
        checks=[dict(use_id="U1", verdict=v, kind=k, reason="texto del modelo") for k, v in checks],
    )


def test_a_contradiction_or_a_wrong_concept_produces_a_notice_naming_the_kind():
    notice = build_notice(trace("issues_found", ("contradiction", "incorrect")))
    assert [i["kind"] for i in notice["items"]] == ["contradiction"]
    assert "contradice el material" in notice["items"][0]["message"] and notice["guidance"] == GUIDANCE
    both = build_notice(
        trace(
            "issues_found",
            ("wrong_concept", "incorrect"),
            ("contradiction", "incorrect"),
            ("contradiction", "incorrect"),
        )
    )
    assert [i["kind"] for i in both["items"]] == ["wrong_concept", "contradiction"]  # deduplicated, in order


def test_nothing_to_say_when_clean_or_only_doubtful_and_never_model_text():
    assert build_notice(trace("no_issues_found")) is None
    assert build_notice(trace("insufficient_evidence", ("unsupported", "uncertain"))) is None
    notice = build_notice(trace("issues_found", ("contradiction", "incorrect")))
    assert "texto del modelo" not in repr(
        notice
    )  # the model's own reason is for teachers, not for the student
    assert all(m in MESSAGES.values() for m in (i["message"] for i in notice["items"]))


def test_a_review_that_could_not_run_says_so_instead_of_staying_silent():
    notice = build_notice(dict(status="technical_failure", checks=[]))
    assert [i["kind"] for i in notice["items"]] == ["not_reviewed"]


def test_every_kind_the_host_can_flag_has_an_authorised_text():
    assert set(NOTICE_KINDS) <= set(MESSAGES)


def test_an_unbacked_attribution_notifies_but_a_doubt_about_it_does_not():
    notice = build_notice(trace("issues_found", ("attribution", "incorrect")))
    assert [i["kind"] for i in notice["items"]] == ["attribution"]
    assert "norma o fuente concreta" in notice["items"][0]["message"]
    assert build_notice(trace("insufficient_evidence", ("attribution", "uncertain"))) is None


def test_coverage_notice_is_added_even_when_the_review_found_nothing():
    from oralia.course_dialogue.review_notice import MESSAGES, build_notice

    notice = build_notice({"status": "no_issues_found", "checks": []}, ("coverage",))
    assert [item["kind"] for item in notice["items"]] == ["coverage"]
    assert notice["items"][0]["message"] == MESSAGES["coverage"]
    assert build_notice({"status": "no_issues_found", "checks": []}) is None


def _trace(unit, kind="wrong_concept"):
    return {
        "status": "issues_found",
        "answer_units": [{"id": "U1", "text": unit}],
        "checks": [{"use_id": "U1", "kind": kind, "verdict": "incorrect"}],
    }


def test_a_finding_on_a_unit_that_refutes_the_students_claim_is_not_shown():
    from oralia.course_dialogue.review_notice import build_notice, drop_corrections

    ask = "Entiendo que validar es comprobar que el sistema está bien programado. ¿Voy bien?"
    trace = _trace("La validación no se limita a comprobar que el sistema está bien programado.")
    assert build_notice(drop_corrections(trace, ask)) is None


def test_other_findings_and_other_questions_keep_their_notice():
    from oralia.course_dialogue.review_notice import build_notice, drop_corrections

    ask = "Entiendo que validar es comprobar que el sistema está bien programado. ¿Voy bien?"
    assert build_notice(drop_corrections(_trace("La validación consiste en probar el código."), ask))  # no correction marker
    assert build_notice(drop_corrections(_trace("No se limita a eso."), "¿Qué es la validación?"))  # not a self-check
    assert build_notice(drop_corrections(_trace("No es X, sino Y.", "attribution"), ask))  # not a concept finding
