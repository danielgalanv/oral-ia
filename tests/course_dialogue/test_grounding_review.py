import json

import pytest

from oralia.course_dialogue import grounding_review as G
from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.web_review_frame import validate_web_review_frame
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationOutcome

SOURCE_A = "El sistema debe registrar cada acceso. El registro se conserva durante seis meses."
SOURCE_B = "Las copias de seguridad se hacen cada noche."
ANSWER = "Introducción breve.\n\nEl registro de accesos se conserva seis meses.\n\nSe copia cada hora."


def evidence():
    return [
        EvidenceItem(fragment_id="a", document_id="d", document_version=1, text=SOURCE_A),
        EvidenceItem(fragment_id="b", document_id="d", document_version=1, text=SOURCE_B),
    ]


def claim(unit, label, quote, **extra):
    base = dict(unit=unit, kind="source", claim="afirmación", answer_quote=quote, label=label)
    return {**base, **extra}


GOOD = claim(
    "U2",
    "supported",
    "El registro de accesos se conserva seis meses.",
    source_id="a",
    source_quote="se conserva durante seis meses",
)
BAD = claim(
    "U3",
    "contradicted",
    "Se copia cada hora.",
    source_id="b",
    source_quote="se hacen cada noche",
    reason="La fuente dice cada noche.",
)


def reply(*claims, no_claims=("U1",)):
    return json.dumps(dict(claims=list(claims), no_claims=list(no_claims)))


class Port:
    def __init__(self, *texts):
        self.texts, self.requests = list(texts), []

    async def generate(self, req):
        self.requests.append(req)
        text = self.texts[min(len(self.requests) - 1, len(self.texts) - 1)]
        return GenerationOutcome(ok=True, text=text, finish_reason="stop", adapter="deterministic")


def reviewer(port, votes=1, maximum=8):
    return G.GroundingReviewer(port, budget=CallBudget(maximum=maximum), revalidate=lambda: None, votes=votes)


def base():
    return RepairGenerationRequest(
        purpose="explicacion", instruction="t", student_input="Pregunta", evidence=evidence()
    )


@pytest.mark.asyncio
async def test_verified_contradiction_is_the_only_objection_and_binds_to_the_answer_unit():
    port = Port(reply(GOOD, BAD))
    trace = await reviewer(port).review(base(), ANSWER)
    assert trace["status"] == "issues_found" and len(port.requests) == 1 and trace["format_retries"] == 0
    obs = G.grounding_observations(trace)
    assert obs[0]["claim"] == "Se copia cada hora." and obs[0]["evidence"] == [{"source_id": "b"}]
    assert not trace["publication_allowed"] and trace["participant_display"] is None


@pytest.mark.asyncio
async def test_absence_from_sources_is_never_an_objection():
    nis = claim("U3", "not_in_sources", "Se copia cada hora.")
    trace = await reviewer(Port(reply(GOOD, nis))).review(base(), ANSWER)
    assert trace["status"] == "no_issues_found" and trace["checks"] == []
    assert trace["unsupported_claims"][0]["unit"] == "U3"  # visible to a teacher, not a defect


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bad_quote",
    [
        dict(source_quote="las copias se hacen cada hora"),  # invented source text
        dict(answer_quote="Se copia cada minuto."),  # not in the answer
        dict(source_id="zzz"),  # unknown source
        dict(reason=""),  # no explanation
    ],
)
async def test_objection_that_cannot_be_traced_to_the_text_is_discarded_not_published(bad_quote):
    trace = await reviewer(Port(reply(GOOD, {**BAD, **bad_quote}))).review(base(), ANSWER)
    assert trace["status"] == "insufficient_evidence"
    assert [c["verdict"] for c in trace["checks"]] == ["uncertain"]
    with pytest.raises(ValueError):
        G.grounding_observations(trace)  # nothing verified to repair


@pytest.mark.asyncio
async def test_unverified_support_is_downgraded_and_never_counts_as_proof():
    fake = {**GOOD, "source_quote": "un texto que no está"}
    trace = await reviewer(Port(reply(fake, BAD))).review(base(), ANSWER)
    assert {r["outcome"] for r in trace["votes"][0]["records"]} == {"unverified_support", "contradicted"}
    assert trace["unsupported_claims"][0]["unit"] == "U2"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "no es json",
        reply(
            claim("U9", "not_in_sources", "Se copia cada hora."), no_claims=("U1", "U2", "U3")
        ),  # foreign unit
        json.dumps(dict(claims=[], no_claims=["U1", "U2", "U3"], status="no_issues_found")),  # model status
        reply(GOOD, BAD) + " Explicación fuera del JSON.",
    ],
)
async def test_contract_failure_gets_one_format_reask_then_stays_a_technical_state(text):
    port = Port(text)
    trace = await reviewer(port).review(base(), ANSWER)
    assert trace["status"] == "technical_failure" and trace["checks"] == []
    assert len(port.requests) == 2 and trace["format_retries"] == 1  # never a loop


@pytest.mark.asyncio
async def test_format_reask_recovers_a_malformed_first_reply():
    port = Port("```no json```", reply(GOOD, BAD))
    trace = await reviewer(port).review(base(), ANSWER)
    assert trace["status"] == "issues_found" and len(port.requests) == 2 and trace["format_retries"] == 1


@pytest.mark.asyncio
async def test_units_the_model_skipped_are_reported_not_silently_accepted():
    trace = await reviewer(Port(reply(GOOD, no_claims=()))).review(base(), ANSWER)
    assert trace["unreviewed_units"] == ["U1", "U3"] and trace["status"] == "insufficient_evidence"
    both = await reviewer(Port(reply(GOOD, BAD, no_claims=("U1", "U2")))).review(base(), ANSWER)
    assert both["unreviewed_units"] == [] and both["status"] == "issues_found"  # claims win over no_claims


@pytest.mark.asyncio
async def test_majority_vote_keeps_only_agreed_contradictions_and_rotates_source_order():
    one_vote_noise = reply(GOOD, BAD)
    quiet = reply(GOOD, claim("U3", "not_in_sources", "Se copia cada hora."))
    port = Port(one_vote_noise, quiet, quiet)
    trace = await reviewer(port, votes=3).review(base(), ANSWER)
    assert trace["status"] == "no_issues_found" and trace["aggregate"]["valid_votes"] == 3
    assert [v["source_order"] for v in trace["votes"]] == [["a", "b"], ["b", "a"], ["a", "b"]]
    port = Port(one_vote_noise, one_vote_noise, quiet)
    assert (await reviewer(port, votes=3).review(base(), ANSWER))["status"] == "issues_found"
    port = Port("garbage", "garbage", quiet, quiet)  # an invalid vote is excluded, never counted as agreement
    out = await reviewer(port, votes=3).review(base(), ANSWER)
    assert out["aggregate"]["valid_votes"] == 2 and out["votes"][0]["valid"] is False


@pytest.mark.asyncio
async def test_budget_exhaustion_and_bad_vote_counts_are_not_swallowed():
    with pytest.raises(ValueError, match="budget"):
        await reviewer(Port(reply(GOOD, BAD)), maximum=0).review(base(), ANSWER)
    with pytest.raises(ValueError):
        reviewer(Port(), votes=2)


def test_frame_is_reconstructible_and_the_policy_is_subject_neutral():
    req = G.GroundingReviewRequest(
        purpose="explicacion", instruction="t", question="Pregunta", evidence=evidence(), draft=ANSWER
    )
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        web_review_prompt_version=req.prompt_version,
        web_review_format_reminder=False,
        messages=req.effective_messages(),
    )
    validate_web_review_frame(frame, "qwen3-8b-thinking")
    frame["messages"][0]["content"] += "x"
    with pytest.raises(ValueError):
        validate_web_review_frame(frame, "qwen3-8b-thinking")
    lowered = G.GROUNDING_POLICY.lower()
    for stale in ("requisito", "trazab", "completo", "sin aumentar", "autoriza", "concreto", "status"):
        assert stale not in lowered


LABELLED = "**Registro:** El registro de accesos se conserva seis meses."


def test_the_host_generates_one_mandatory_claim_per_titled_unit():
    units = G.answer_units(LABELLED, attach_keywords=True)
    required = G.required_claims(units)
    assert required == [
        dict(unit="U1", answer_quote="Registro", claim="El contenido de la unidad corresponde a «Registro»")
    ]
    req = G.GroundingReviewRequest(
        purpose="explicacion", instruction="t", question="Pregunta", evidence=evidence(), draft=LABELLED
    )
    assert json.loads(req.effective_messages()[-1]["content"])["required_claims"] == required
    assert G.required_claims(G.answer_units(ANSWER, attach_keywords=True)) == []  # untitled text: none


@pytest.mark.asyncio
async def test_a_title_the_model_did_not_judge_is_reported_as_unreviewed_not_accepted():
    body = claim(
        "U1",
        "supported",
        "El registro de accesos se conserva seis meses.",
        source_id="a",
        source_quote="se conserva durante seis meses",
    )
    title_bad = claim(
        "U1",
        "contradicted",
        "Registro",
        source_id="b",
        source_quote="se hacen cada noche",
        reason="Las fuentes llaman a eso copias.",
    )
    skipped = await reviewer(Port(reply(body, no_claims=()))).review(base(), LABELLED)
    assert skipped["unreviewed_units"] == ["U1"] and skipped["status"] == "insufficient_evidence"
    judged = await reviewer(Port(reply(body, title_bad, no_claims=()))).review(base(), LABELLED)
    assert judged["unreviewed_units"] == [] and judged["status"] == "issues_found"
    assert G.grounding_observations(judged)[0]["claim"] == "Registro"


@pytest.mark.asyncio
async def test_a_claim_backed_by_an_allowed_web_page_is_verified_against_that_page():
    web_text = "Un procedimiento de copias nocturnas es una práctica habitual y recomendada."
    web = EvidenceItem(fragment_id="w", document_id="web/ejemplo", document_version=1, text=web_text)
    page = RepairGenerationRequest(
        purpose="explicacion", instruction="t", student_input="Pregunta", evidence=[*evidence(), web]
    )
    web_claim = claim(
        "U3",
        "supported",
        "Se copia cada hora.",
        source_id="w",
        source_quote="copias nocturnas es una práctica habitual",
    )
    port = Port(reply(GOOD, web_claim))
    trace = await reviewer(port).review(page, ANSWER, web_source_ids=["w"])
    assert trace["status"] == "no_issues_found" and trace["votes"][0]["records"][1]["outcome"] == "supported"
    sent = json.loads(port.requests[0].effective_messages()[-1]["content"])["sources"]
    assert {s["fragment_id"]: s["origin"] for s in sent} == {"a": "docente", "b": "docente", "w": "web"}
    assert "página web permitida" in " ".join(G.GROUNDING_POLICY.lower().split())
    with pytest.raises(ValueError):
        await reviewer(Port(reply(GOOD, BAD))).review(page, ANSWER, web_source_ids=["zzz"])


def test_grounding_response_schema_only_admits_this_requests_ids_and_requires_every_key():
    req = G.GroundingReviewRequest(
        purpose="explicacion", instruction="t", question="Pregunta", evidence=evidence(), draft=ANSWER
    )
    schema = G.grounding_response_schema(req)
    item = schema["properties"]["claims"]["items"]
    assert item["properties"]["unit"]["enum"] == ["U1", "U2", "U3"]
    assert item["properties"]["source_id"]["enum"] == ["a", "b", ""]
    assert set(item["required"]) == set(item["properties"]) and schema["required"] == ["claims", "no_claims"]
