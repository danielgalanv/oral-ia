import json

import pytest

from oralia.course_dialogue.concept_ledger import (
    ConceptLedgerRequest,
    ThinkingConceptLedgerRequest,
    UseCheck,
    answer_units,
    ledger_status,
    parse_catalog,
    parse_ledger,
    source_cards,
)
from oralia.course_dialogue.web_review_frame import validate_web_review_frame
from oralia.infrastructure.generation.generation_port import EvidenceItem


def evidence():
    return [
        EvidenceItem(
            fragment_id="doc:1",
            document_id="teacher/current",
            document_version=1,
            text=(
                "Título\n• Capacidad. Todas las acciones\nsolicitadas están presentes.\n"
                "• Claridad. Se entiende el texto.\n"
            ),
        )
    ]


def request():
    return ThinkingConceptLedgerRequest(
        purpose="explicacion",
        instruction="Test",
        question="Una pregunta",
        evidence=evidence(),
        draft="Una explicación.\n\nOtra idea.",
        selected_cards=["C1"],
        assigned_units=["U1", "U2"],
    )


def test_literal_source_units_preserve_wrapped_definition_and_context():
    cards = source_cards(evidence())
    assert len([c for c in cards if c["kind"] == "definition"]) == 2
    assert cards[-1]["kind"] == "context" and cards[-1]["text"] == evidence()[0].text
    assert cards[0]["source_name"] == "Capacidad"
    assert "acciones\nsolicitadas" in cards[0]["text"]
    for c in cards:
        assert evidence()[0].text[c["start"] : c["end"]] == c["text"]
    answer = "## Una etiqueta\n\nSu explicación\ncontinúa aquí.\n\nOtra idea."
    units = answer_units(answer)
    assert len(units) == 2
    assert "## Una etiqueta\n\nSu explicación" in units[0]["text"]
    assert units[0]["label"] == "Una etiqueta"
    assert all(answer[u["start"] : u["end"]] == u["text"] for u in units)
    separate = answer_units("**Una etiqueta:** Su definición.\n\n**Otra etiqueta:** Otra definición.")
    assert len(separate) == 2


def test_source_plan_is_blind_to_candidate_and_cannot_reference_foreign_units():
    with pytest.raises(ValueError):
        ConceptLedgerRequest(
            purpose="explicacion",
            instruction="Test",
            question="Pregunta",
            ledger_stage="catalog",
            evidence=evidence(),
            draft="No debe verlo",
        )
    with pytest.raises(ValueError):
        parse_catalog('{"selected":["FOREIGN"],"missing_definitions":[]}', evidence())
    assert parse_catalog('{"selected":["C1"],"missing_definitions":[]}', evidence()).selected == ["C1"]


@pytest.mark.parametrize(
    "checks",
    [
        [{"use_id": "U1", "card_ids": ["C1"], "verdict": "correct", "reason": "Razón"}],
        [{"use_id": "U1", "card_ids": ["C1"], "verdict": "correct", "reason": "Razón"}] * 2,
        [
            {"use_id": u, "card_ids": ["FOREIGN"], "verdict": "correct", "reason": "Razón"}
            for u in ("U1", "U2")
        ],
        [{"use_id": u, "card_ids": [], "verdict": "correct", "reason": "Razón"} for u in ("U1", "U2")],
    ],
)
def test_missing_duplicate_or_ungrounded_checks_cannot_be_accepted(checks):
    with pytest.raises(ValueError):
        parse_ledger(json.dumps({"checks": checks}), request())


def test_status_is_derived_from_each_record_not_a_free_global_label():
    checks = [
        UseCheck(use_id="U1", card_ids=["C1"], verdict="correct", reason="Correcto"),
        UseCheck(use_id="U2", card_ids=["C2"], verdict="incorrect", reason="Error"),
    ]
    assert ledger_status(checks) == "issues_found"
    with pytest.raises(ValueError):
        parse_ledger(
            json.dumps({"checks": [c.model_dump() for c in checks], "status": "no_issues_found"}), request()
        )
    checks[1].verdict = "uncertain"
    assert ledger_status(checks) == "insufficient_evidence"
    assert (
        ledger_status([UseCheck(use_id="U1", card_ids=[], verdict="not_concept", reason="Neutral")])
        == "insufficient_evidence"
    )


@pytest.mark.asyncio
async def test_pipeline_binds_plan_and_repair_to_original_source_and_answer_units():
    from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer, repair_observations
    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    class Port:
        def __init__(self, text):
            self.text = text
            self.requests = []

        async def generate(self, req):
            self.requests.append(req)
            return GenerationOutcome(ok=True, text=self.text, finish_reason="stop", adapter="deterministic")

    planner = Port('{"selected":["C1","C2"],"missing_definitions":[]}')
    critic = Port(
        json.dumps(
            {
                "checks": [
                    {"use_id": "U1", "card_ids": ["C1"], "verdict": "correct", "reason": "Coincide"},
                    {
                        "use_id": "U2",
                        "card_ids": ["C2"],
                        "verdict": "incorrect",
                        "reason": "Intercambia el significado",
                    },
                ]
            }
        )
    )
    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta", evidence=evidence()
    )
    reviewer = ConceptLedgerReviewer(planner, critic, budget=CallBudget(maximum=4), revalidate=lambda: None)
    trace = await reviewer.review(base, "Primera idea.\n\nSEGUNDA IDEA ERRÓNEA.")
    assert trace["status"] == "issues_found"
    assert planner.requests[0].draft is None
    assert "SEGUNDA IDEA" not in str(planner.requests[0].effective_messages())
    observations = repair_observations(trace)
    assert observations[0]["claim"] == "SEGUNDA IDEA ERRÓNEA."
    assert observations[0]["explanation"] == "Intercambia el significado"
    assert observations[0]["evidence"] == [{"source_id": "doc:1"}]
    assert not trace["publication_allowed"] and trace["participant_display"] is None
    base.evidence[0].text += " revisión diferente"
    with pytest.raises(ValueError, match="different"):
        await reviewer.review(base, "Otra respuesta", catalogue=trace["catalogue"])


@pytest.mark.parametrize("catalog", [True, False])
@pytest.mark.parametrize(
    "version", ["concept-ledger/v1", "concept-ledger/v2", "concept-ledger/v3", "concept-ledger/v4"]
)
def test_native_frame_reconstruction_binds_catalogue_and_use_assignments(catalog, version):
    req = (
        ConceptLedgerRequest(
            purpose="explicacion",
            instruction="Test",
            question="Pregunta",
            ledger_stage="catalog",
            evidence=evidence(),
        )
        if catalog
        else request()
    )
    req.prompt_version = version
    frame = dict(
        model_prompt_profile=req.model_profile,
        prompt_task="review",
        web_review_prompt_version=req.prompt_version,
        web_review_format_reminder=False,
        messages=req.effective_messages(),
    )
    validate_web_review_frame(frame, req.model_profile)
    frame["messages"][0]["content"] += "Alteración"
    with pytest.raises(ValueError):
        validate_web_review_frame(frame, req.model_profile)


def test_compact_frame_retains_full_sources_history_answer_and_assigned_passages():
    req = request()
    req.prompt_version = "concept-ledger/v1"
    old = json.loads(req.effective_messages()[-1]["content"])
    req.prompt_version = "concept-ledger/v2"
    new = json.loads(req.effective_messages()[-1]["content"])
    assert all(old[k] == new[k] for k in ("sources", "shown_history", "answer"))
    assert new["assigned_passages"] == old["answer_units"]
    assert all("text" in c for c in new["concept_menu"] if c["kind"] == "definition")
    assert len(json.dumps(new["concept_menu"])) < len(json.dumps(old["concept_menu"]))


def test_keywords_are_kept_with_explanation_and_reference_count_matches_source_menu():
    text = "**Una propiedad:** Su explicación.\n\nPalabras clave: una propiedad"
    assert len(answer_units(text)) == 2
    merged = answer_units(text, attach_keywords=True)
    assert len(merged) == 1 and merged[0]["text"] == text
    many = [
        EvidenceItem(
            fragment_id="page",
            document_id="teacher/current",
            document_version=1,
            text="\n".join(f"• Criterio{i}. Explicación del criterio {i}." for i in range(10)),
        )
    ]
    req = ThinkingConceptLedgerRequest(
        prompt_version="concept-ledger/v3",
        purpose="explicacion",
        instruction="Test",
        question="Pregunta",
        evidence=many,
        draft="Una frase.",
        assigned_units=["U1"],
    )
    output = json.dumps(
        {
            "checks": [
                dict(
                    use_id="U1",
                    card_ids=[f"C{i}" for i in range(1, 11)],
                    verdict="correct",
                    reason="Resume varios criterios.",
                )
            ]
        }
    )
    assert len(parse_ledger(output, req).checks[0].card_ids) == 10
    req.prompt_version = "concept-ledger/v2"
    with pytest.raises(ValueError, match="legacy"):
        parse_ledger(output, req)


def test_label_only_frame_never_receives_author_description():
    from oralia.course_dialogue.concept_labels import ConceptLabelRequest, parse_label_relations

    req = ConceptLabelRequest(
        purpose="explicacion",
        instruction="Test",
        question="Operación",
        evidence=evidence(),
        targets=[dict(use_id="U1", label="Otra etiqueta", card_ids=["C1"])],
    )
    frame = dict(
        model_prompt_profile=req.model_profile,
        prompt_task="review",
        web_review_format_reminder=False,
        web_review_prompt_version=req.prompt_version,
        messages=req.effective_messages(),
    )
    validate_web_review_frame(frame, req.model_profile)
    assert "answer" not in json.loads(req.effective_messages()[-1]["content"])
    assert (
        parse_label_relations(
            '{"relations":[{"use_id":"U1","relation":"different","reason":"Otro significado"}]}', req
        )
        .relations[0]
        .relation
        == "different"
    )
    with pytest.raises(ValueError):
        ConceptLabelRequest(**dict(req.model_dump(), draft="Una descripción a ocultar"))


@pytest.mark.asyncio
async def test_separate_label_judgment_can_flag_a_definition_accepted_by_meaning_checker():
    from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer, repair_observations
    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    class Planner:
        async def generate(self, req):
            if hasattr(req, "targets"):
                assert req.draft is None
                text = json.dumps(
                    {
                        "relations": [
                            dict(use_id=t.use_id, relation="different", reason="Nombre distinto")
                            for t in req.targets
                        ]
                    }
                )
            else:
                text = '{"selected":["C1"],"proposed_labels":{},"missing_definitions":[]}'
            return GenerationOutcome(ok=True, text=text, finish_reason="stop", adapter="deterministic")

    class Critic:
        async def generate(self, req):
            return GenerationOutcome(
                ok=True,
                text='{"card_ids":["C1"],"verdict":"correct","reason":"Descripción adecuada"}',
                finish_reason="stop",
                adapter="deterministic",
            )

    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta", evidence=evidence()
    )
    text = "**Otra etiqueta:** Una descripción.\n\nPalabras clave: otra etiqueta"
    r = ConceptLedgerReviewer(Planner(), Critic(), budget=CallBudget(maximum=3), revalidate=lambda: None)
    trace = await r.review(base, text)
    assert trace["primary_status"] == "no_issues_found" and trace["status"] == "issues_found"
    assert trace["checks"][0]["verdict"] == "correct"
    assert repair_observations(trace)[0]["claim"] == text


@pytest.mark.asyncio
async def test_coverage_failure_splits_without_guessing_or_dropping_assignments():
    from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer
    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    class Planner:
        async def generate(self, req):
            return GenerationOutcome(
                ok=True,
                text='{"selected":["C1"],"proposed_labels":{},"missing_definitions":[]}',
                finish_reason="stop",
                adapter="deterministic",
            )

    class Critic:
        async def generate(self, req):
            row = dict(card_ids=["C1"], verdict="correct", reason="Contraste registrado")
            if len(req.assigned_units) > 1:
                text = json.dumps(dict(checks=[dict(use_id=req.assigned_units[0], **row)]))
            else:
                text = json.dumps(row)
                assert "answer_units" not in json.loads(req.effective_messages()[-1]["content"])
            return GenerationOutcome(ok=True, text=text, finish_reason="stop", adapter="deterministic")

    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta", evidence=evidence()
    )
    budget = CallBudget(maximum=5)
    reviewer = ConceptLedgerReviewer(Planner(), Critic(), budget=budget, revalidate=lambda: None)
    trace = await reviewer.review(base, "Una explicación.\n\nOtra observación.")
    assert trace["format_retries"] == 1 and budget.used == 5
    assert trace["coverage_batch_splits"][0]["assigned"] == ["U1", "U2"]
    assert [c["use_id"] for c in trace["checks"]] == ["U1", "U2"]


class _Port:
    def __init__(self, text):
        self.text = text
        self.requests = []

    async def generate(self, req):
        from oralia.infrastructure.generation.generation_port import GenerationOutcome

        self.requests.append(req)
        return GenerationOutcome(ok=True, text=self.text, finish_reason="stop", adapter="deterministic")


def _compact_reviewer(text, maximum=4):
    from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer
    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget

    port = _Port(text)
    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta", evidence=evidence()
    )
    reviewer = ConceptLedgerReviewer(
        None,
        port,
        budget=CallBudget(maximum=maximum),
        revalidate=lambda: None,
        prompt_version="concept-ledger/v5",
    )
    return reviewer, port, base


@pytest.mark.asyncio
async def test_compact_review_is_one_call_without_planner_and_binds_incidents_to_units():
    from oralia.course_dialogue.concept_review_loop import repair_observations

    reply = {
        "issues": [
            {
                "use_id": "U2",
                "card_ids": ["C2"],
                "kind": "contradiction",
                "verdict": "incorrect",
                "reason": "Cambia el sentido",
            }
        ],
    }
    reviewer, port, base = _compact_reviewer(json.dumps(reply))
    trace = await reviewer.review(base, "Primera idea.\n\nSEGUNDA IDEA ERRÓNEA.\n\nTercera.")
    assert len(port.requests) == 1 and len(trace["calls"]) == 1 and trace["format_retries"] == 0
    assert port.requests[0].assigned_units == ["U1", "U2", "U3"]
    assert trace["status"] == "issues_found" and not trace["publication_allowed"]
    obs = repair_observations(trace)
    assert obs[0]["claim"] == "SEGUNDA IDEA ERRÓNEA." and obs[0]["evidence"] == [{"source_id": "doc:1"}]
    clean, port, base = _compact_reviewer('{"issues":[]}')
    assert (await clean.review(base, "Una idea.\n\nOtra."))["status"] == "no_issues_found"
    assert len(port.requests) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "no es json",
        '{"status":"no_issues_found","issues":[]}',  # the model no longer declares status
        '{"issues":[{"use_id":"U9","card_ids":["C1"],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
        '{"issues":[{"use_id":"U1","card_ids":["FOREIGN"],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
        '{"issues":[{"use_id":"U1","card_ids":[],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
    ],
)
async def test_compact_contract_failure_is_kept_as_technical_state_without_a_second_call(text):
    from oralia.course_dialogue.concept_review_loop import repair_observations

    reviewer, port, base = _compact_reviewer(text)
    trace = await reviewer.review(base, "Una idea.\n\nOtra.")
    assert trace["status"] == "technical_failure"
    assert trace["technical_failure"]["reason"] == "invalid_contract"
    assert len(port.requests) == 1 and trace["checks"] == [] and trace["invalid_outputs"]
    with pytest.raises(ValueError):
        repair_observations(trace)


@pytest.mark.asyncio
async def test_compact_review_rejects_foreign_catalogue_and_propagates_budget_exhaustion():
    reviewer, port, base = _compact_reviewer('{"issues":[]}', maximum=0)
    with pytest.raises(ValueError, match="budget"):
        await reviewer.review(base, "Una idea.")
    reviewer, port, base = _compact_reviewer('{"issues":[]}')
    with pytest.raises(ValueError, match="different"):
        await reviewer.review(base, "Una idea.", catalogue=dict(binding="x", decision={"selected": []}))
    assert not port.requests


def test_compact_frame_is_reconstructible_and_smaller_than_the_assigned_passage_variant():
    req = request()
    req.prompt_version = "concept-ledger/v5"
    frame = dict(
        model_prompt_profile=req.model_profile,
        prompt_task="review",
        web_review_prompt_version=req.prompt_version,
        web_review_format_reminder=False,
        messages=req.effective_messages(),
    )
    validate_web_review_frame(frame, req.model_profile)
    assert "assigned_passages" not in frame["messages"][-1]["content"]
    req.assigned_units = ["U1"]
    with pytest.raises(ValueError, match="whole answer"):
        req.effective_messages()


def test_compact_status_is_derived_by_the_host_from_the_incidents():
    from oralia.course_dialogue.concept_ledger import parse_compact

    req = request()
    req.prompt_version = "concept-ledger/v5"

    def one(verdict):
        return json.dumps(
            {
                "issues": [
                    {
                        "use_id": "U1",
                        "card_ids": ["C1"],
                        "kind": "contradiction",
                        "verdict": verdict,
                        "reason": "x",
                    }
                ]
            }
        )

    assert parse_compact('{"issues":[]}', req).status == "no_issues_found"
    assert parse_compact(one("uncertain"), req).status == "insufficient_evidence"
    assert parse_compact(one("incorrect"), req).status == "issues_found"


def test_compact_policy_is_domain_neutral_and_has_no_development_notes():
    from oralia.course_dialogue.concept_ledger import COMPACT_POLICY

    lowered = COMPACT_POLICY.lower()
    for stale in ("requisito", "trazab", "completo", "autoriza", "sin aumentar", "sin endurecer"):
        assert stale not in lowered
    assert "contraste concreto" not in lowered  # a literal placeholder was copied as the answer
    assert "nunca fuera del json" in lowered
    assert "status" not in lowered  # derived by the host, not requested from the model


def test_compact_reader_forgives_form_slips_but_not_substance():
    from oralia.course_dialogue.concept_ledger import parse_compact

    req = request()
    req.prompt_version = "concept-ledger/v5"
    # trailing stray character after a complete verdict
    assert parse_compact('{"issues":[]}"', req).status == "no_issues_found"
    trailing = chr(10) * 2 + '{"issues":[]}' + chr(10) * 2 + "Explicación fuera del JSON."
    assert parse_compact(trailing, req).status == "no_issues_found"
    # a source identifier where a card id was expected maps to that source's context card
    review = parse_compact(
        '{"issues":[{"use_id":"U1","card_ids":["doc:1"],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
        req,
    )
    assert review.issues[0].card_ids == [c["id"] for c in source_cards(evidence()) if c["kind"] == "context"]
    # two incidents on the same unit are merged and the more severe verdict wins
    merged = parse_compact(
        '{"issues":[{"use_id":"U1","card_ids":["C1"],"kind":"unsupported","verdict":"uncertain","reason":"a"},'
        '{"use_id":"U1","card_ids":["C2"],"kind":"contradiction","verdict":"incorrect","reason":"b"}]}',
        req,
    )
    assert len(merged.issues) == 1 and merged.issues[0].verdict == "incorrect"
    assert merged.issues[0].card_ids == ["C1", "C2"] and merged.status == "issues_found"
    # substance is still enforced: no usable reference for an incorrect use, or a unit that does not exist
    for bad in (
        '{"issues":[{"use_id":"U1","card_ids":["nothing"],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
        '{"issues":[{"use_id":"U9","card_ids":["C1"],"kind":"contradiction","verdict":"incorrect","reason":"x"}]}',
        "sin json",
    ):
        with pytest.raises(ValueError):
            parse_compact(bad, req)


def test_compact_policy_defines_the_discrepancy_kinds_without_subject_vocabulary():
    from oralia.course_dialogue.concept_ledger import COMPACT_POLICY, ISSUE_KINDS

    lowered = " ".join(COMPACT_POLICY.lower().split())
    for kind in ISSUE_KINDS:
        assert kind + ":" in lowered
    for needed in ("paráfrasis", "ejemplo que ilustra bien", "invierte o contradice"):
        assert needed in lowered
    for stale in ("requisito", "trazab", "completo", "ortograf"):
        assert stale not in lowered


def test_the_host_table_not_the_model_decides_which_discrepancies_are_objections():
    from oralia.course_dialogue.concept_ledger import OBJECTION_KINDS, parse_compact

    req = request()
    req.prompt_version = "concept-ledger/v5"

    def reply(kind, verdict="incorrect"):
        issue = dict(use_id="U1", kind=kind, card_ids=["C1"], verdict=verdict, reason="x")
        return json.dumps({"issues": [issue]})

    assert OBJECTION_KINDS == ("contradiction", "wrong_concept")
    for kind in ("contradiction", "wrong_concept"):
        assert parse_compact(reply(kind), req).status == "issues_found"
    for kind in ("related_concept", "scope", "label", "unsupported"):
        review = parse_compact(reply(kind), req)
        assert review.status == "no_issues_found" and [n.kind for n in review.notes] == [kind]
    assert parse_compact(reply("unsupported", "uncertain"), req).status == "insufficient_evidence"
    merged = parse_compact(
        json.dumps(
            {
                "issues": [
                    dict(use_id="U1", kind="label", card_ids=["C1"], verdict="incorrect", reason="a"),
                    dict(use_id="U1", kind="contradiction", card_ids=["C1"], verdict="incorrect", reason="b"),
                ]
            }
        ),
        req,
    )
    assert merged.status == "issues_found" and merged.issues[0].kind == "contradiction"
    with pytest.raises(ValueError):  # a kind outside the table is a contract error, not a silent default
        parse_compact(reply("invented"), req)


def test_compact_review_tells_the_model_which_sources_are_allowed_web_pages():
    from oralia.course_dialogue.concept_ledger import COMPACT_POLICY

    web = EvidenceItem(
        fragment_id="web:1",
        document_id="web/ejemplo",
        document_version=1,
        text="Un hecho que solo dice la web.",
    )
    req = ThinkingConceptLedgerRequest(
        purpose="explicacion",
        instruction="Test",
        question="Una pregunta",
        evidence=[*evidence(), web],
        draft="Una explicación." + chr(10) * 2 + "Otra idea.",
        assigned_units=["U1", "U2"],
        prompt_version="concept-ledger/v5",
        web_source_ids=["web:1"],
    )
    messages = req.effective_messages()
    sources = json.loads(messages[-1]["content"])["sources"]
    assert {s["fragment_id"]: s["origin"] for s in sources} == {"doc:1": "docente", "web:1": "web"}
    lowered = " ".join(COMPACT_POLICY.lower().split())
    assert (
        "página web permitida" in lowered and "evidencia válida" in lowered and "se tratan igual" in lowered
    )
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        web_review_prompt_version=req.prompt_version,
        web_review_format_reminder=False,
        messages=messages,
    )
    validate_web_review_frame(frame, "qwen3-8b-thinking")  # reconstructible, web ids included
    with pytest.raises(ValueError):
        ThinkingConceptLedgerRequest(
            purpose="explicacion",
            instruction="Test",
            question="x",
            evidence=evidence(),
            draft="Una explicación." + chr(10) * 2 + "Otra idea.",
            assigned_units=["U1", "U2"],
            prompt_version="concept-ledger/v5",
            web_source_ids=["web:1"],
        ).effective_messages()


def test_only_objections_need_a_backing_source_concept():
    from oralia.course_dialogue.concept_ledger import parse_compact

    req = request()
    req.prompt_version = "concept-ledger/v5"

    def reply(kind):
        issue = dict(use_id="U1", kind=kind, card_ids=[], verdict="incorrect", reason="x")
        return json.dumps({"issues": [issue]})

    review = parse_compact(
        reply("unsupported"), req
    )  # content the sources do not mention has no card to cite
    assert review.status == "no_issues_found" and [n.kind for n in review.notes] == ["unsupported"]
    for kind in ("contradiction", "wrong_concept"):
        with pytest.raises(ValueError, match="backs it"):
            parse_compact(reply(kind), req)


def test_an_unbacked_attribution_is_a_noticeable_issue_without_needing_a_card():
    from oralia.course_dialogue.concept_ledger import CompactReview

    def review(verdict):
        return CompactReview.model_validate(
            {"issues": [dict(use_id="U1", kind="attribution", card_ids=[], verdict=verdict, reason="x")]}
        )

    assert review("incorrect").status == "issues_found" and review("incorrect").notes == []
    assert review("uncertain").status == "insufficient_evidence"


def test_unseen_designators_finds_standard_like_names_that_no_source_contains():
    from oralia.course_dialogue.concept_ledger import unseen_designators

    sources = ["El estándar IEEE define algo", "Horario 0830-17.30", "ISO/IEC/IEEE 29148 describe"]
    assert unseen_designators("El IEEE 830 propone una estructura", sources) == ["IEEE 830"]
    assert unseen_designators("La norma ISO/IEC/IEEE 29148 recomienda", sources) == []
    assert unseen_designators("El estándar IEEE recomienda", sources) == []
    assert unseen_designators("El IEEE 830 propone", ["IEEE/ANSI 830-1998 sugiere esta estructura"]) == []
    assert unseen_designators("cifrar con AES 256 y devolver HTTP 404", ["nada"]) == []  # examples, not standards
    assert unseen_designators("El IEEE 8300 propone", ["IEEE/ANSI 830-1998 sugiere esta estructura"]) == ["IEEE 8300"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kind,verdict,answer,status,promoted",
    [
        ("unsupported", "uncertain", "El estándar ISO 99999 propone esto.", "issues_found", True),  # named and unseen
        ("attribution", "incorrect", "Una frase sin ninguna norma.", "insufficient_evidence", False),  # stays a doubt
        ("unsupported", "uncertain", "Una frase sin ninguna norma.", "insufficient_evidence", False),
    ],
)
async def test_the_host_settles_attribution_from_named_designators_absent_from_every_source(
    kind, verdict, answer, status, promoted
):
    reply = {"issues": [dict(use_id="U1", kind=kind, card_ids=[], verdict=verdict, reason="x")]}
    reviewer, _, base = _compact_reviewer(json.dumps(reply))
    trace = await reviewer.review(base, answer)
    assert trace["status"] == status and bool(trace.get("attribution_promoted")) is promoted
    if promoted:
        assert trace["checks"][0]["kind"] == "attribution"
