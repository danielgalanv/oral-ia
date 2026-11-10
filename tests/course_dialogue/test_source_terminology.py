"""Narrow regression guard: literal witnesses and no silent rewriting of model decisions."""

import pytest

from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.source_terminology import terminology_finding
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.course_dialogue.web_review_rounds import WebReviewRounds
from oralia.infrastructure.generation.generation_port import EvidenceItem
from tests.course_dialogue.test_web_review_rounds import Provider

SOURCE = "Completeness. Are all functions required by the customer\nincluded?"
BAD = (
    "9. **Complejidad**:\n - Asegúrate de que todas las funciones requeridas por el cliente estén incluidas."
)
GOOD = BAD.replace("Complejidad", "Completitud")
ITEM = EvidenceItem(fragment_id="source", document_id="fixture", document_version=1, text=SOURCE)


def test_literal_spans_and_negative_controls():
    finding = terminology_finding(BAD, [ITEM], "¿Qué revisar con el cliente?")
    a, b = finding["claim_span"]
    c, d = finding["source_span"]
    assert BAD[a:b] == finding["review"]["issues"][0]["claim"]
    assert SOURCE[c:d] == finding["literal_source"]
    assert terminology_finding(GOOD, [ITEM], "Pregunta") is None
    assert terminology_finding(BAD, [], "Pregunta") is None
    assert terminology_finding(BAD, [ITEM], "¿Qué es la complejidad?") is None
    assert (
        terminology_finding(
            "**Complejidad**: No significa que todas las funciones estén incluidas.", [ITEM], "Pregunta"
        )
        is None
    )
    assert (
        terminology_finding(
            "**Complejidad**: Se cuenta el coste de todas las funciones incluidas.", [ITEM], "Pregunta"
        )
        is None
    )


@pytest.mark.asyncio
async def test_native_acceptance_is_preserved_but_host_finding_requests_real_repair():
    generator = Provider(BAD, GOOD)
    critic = Provider('{"status":"no_issues_found","issues":[]}', '{"status":"no_issues_found","issues":[]}')
    loop = WebReviewRounds(
        generator,
        critic,
        budget=CallBudget(8),
        revalidate=lambda: None,
        generator_profile="qwen25-14b",
        critic_profile="qwen3-8b-thinking",
        repair_with_generator=True,
        prompt_version="web-review/v8",
        source_locations={
            "source": SourceLocation(
                document_id="fixture", document_version=1, document_title="Fixture", page=73
            )
        },
        source_terminology_guard=True,
    )
    request = RepairGenerationRequest(
        purpose="explicacion", instruction="Fixture", student_input="¿Qué revisar?", evidence=[ITEM]
    )
    trace = await loop.process(request)
    assert trace["diagnostic_preview"] == GOOD
    assert trace["reviews"][0]["status"] == "no_issues_found"
    assert trace["host_terminology_reviews"][0]["rule"] == "source-term-completeness/v1"
    assert len(trace["versions"]) == 2 and "Completeness" in str(generator.requests[1].observations)
