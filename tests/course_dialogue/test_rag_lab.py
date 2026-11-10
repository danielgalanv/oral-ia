"""Fixture assessor/provider exercise wiring, never semantic model quality."""

import hashlib

import pytest

from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.rag_lab import ScopeAssessment, SufficiencyAssessment, diagnostic_rag_turn
from oralia.infrastructure.generation.generation_port import GenerationOutcome
from oralia.infrastructure.generation.ollama_adapter import _build_user_content


def page(key, text):
    filename = f"{key}.pdf"
    return {
        "id": f"{key}:1",
        "filename": filename,
        "original_sha256": hashlib.sha256(filename.encode()).hexdigest(),
        "version": 1,
        "page": 1,
        "text": text,
    }


class ProviderFixture:
    def __init__(self, text="Salida ficticia del proveedor de prueba."):
        self.requests = []
        self.text = text

    async def generate(self, request):
        self.requests.append(request)
        return GenerationOutcome(
            ok=True,
            text=self.text,
            adapter="deterministic",
            finish_reason="stop",
        )


class AssessorFixture:
    def __init__(self, *statuses):
        self.statuses = iter(statuses)
        self.seen = []

    def __call__(self, question, retrieval):
        self.seen.append((question, retrieval))
        return SufficiencyAssessment(next(self.statuses), "fixture-not-semantic-review", "control inyectado")


class ScopeAssessorFixture:
    def __init__(self, status="in_scope", **fields):
        self.status = status
        self.fields = fields
        self.seen = []

    def __call__(self, question, resolved_query, history):
        self.seen.append((question, resolved_query, len(history)))
        return ScopeAssessment(self.status, reason="alcance sintético de prueba", **self.fields)


@pytest.mark.asyncio
async def test_explicit_switch_with_trimmed_context_query_excludes_old_history():
    pages = [
        page("req", "Requisitos\nConsistencia de requisitos.\n"),
        page("test", "Testing\nPruebas de defectos.\n"),
    ]
    previous = {
        "input": "consistencia requisitos",
        "displayed_text": "consistencia requisitos",
        "displayed_kind": "laboratory_preview",
    }
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Cambiemos de tema: pruebas de defectos",
        [previous],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=ProviderFixture(),
    )
    assert row["academic_query"] == "pruebas de defectos"
    assert row["focus_change"] is True
    assert all(unit.document_id == "test.pdf" for unit in row["evidence_attempts"].delivered.units)


@pytest.mark.asyncio
async def test_explicit_switch_does_not_require_omitted_old_referent():
    pages = [page("test", "Testing\nPruebas de defectos.\n")]
    history = [
        {
            "input": "consistencia requisitos",
            "displayed_text": "Previa",
            "displayed_kind": "laboratory_preview",
        }
    ]
    history += [{"input": "control", "displayed_text": "Aviso", "displayed_kind": "operational"}] * 4
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Cambiemos de tema: pruebas de defectos",
        history,
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row.get("reason") != "history_context_limit"
    assert len(provider.requests) == 1


@pytest.mark.asyncio
async def test_sufficient_evidence_reaches_generation_port_with_visible_history():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    provider = ProviderFixture()
    first = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Explica consistencia en requisitos",
        [],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert first["displayed_kind"] == "laboratory_preview"
    assert first["publication_allowed"] is False
    assert first["participant_display"] is None
    assert first["raw_candidate"] == first["laboratory_preview"]
    assert first["citation_check"]["missing"] is True
    assert first["semantic_support"] == "unverified"
    assert provider.requests[0].general_knowledge_allowed is False
    assert provider.requests[0].evidence[0].fragment_id == first["evidence_attempts"].delivered.units[0].id
    assert (
        f'<pasaje id="{provider.requests[0].evidence[0].fragment_id}">'
        in provider.requests[0].evidence[0].text
    )
    assert provider.requests[0].evidence[0].document_id.startswith("req.pdf | páginas")
    assert "[id]" not in provider.requests[0].instruction
    assert "Fuentes consultadas" in first["displayed_text"]
    effective = _build_user_content(provider.requests[0])
    assert f'<pasaje id="{provider.requests[0].evidence[0].fragment_id}">' in effective
    assert "La consistencia evita contradicciones." in effective
    followup_scope = ScopeAssessorFixture()
    second = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "¿Por qué?",
        [first],
        scope_assessor=followup_scope,
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert "consistencia" in second["academic_query"]
    assert "consistencia" in followup_scope.seen[0][1]
    assert second["focus_change"] is False
    assert provider.requests[-1].conversation_history[-1].content == first["displayed_text"]


@pytest.mark.asyncio
async def test_autonomous_same_topic_does_not_claim_explicit_switch():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    previous = {
        "input": "consistencia en requisitos",
        "displayed_text": "Respuesta previa",
        "displayed_kind": "laboratory_preview",
    }
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Explica consistencia en requisitos",
        [previous],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=ProviderFixture(),
    )
    assert row["academic_query"] == row["input"]
    assert row["focus_change"] is False


@pytest.mark.asyncio
async def test_missing_and_foreign_citations_never_authorize_participant_display():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    for output, missing, foreign in (
        ("Explicación sin referencia.", True, ()),
        ("Explicación con [fuente:ajena].", False, ("fuente:ajena",)),
    ):
        row = await diagnostic_rag_turn(
            pages,
            build_units(pages),
            "consistencia requisitos",
            [],
            scope_assessor=ScopeAssessorFixture(),
            assessor=AssessorFixture("sufficient"),
            provider=ProviderFixture(output),
        )
        assert row["citation_check"]["missing"] is missing
        assert row["citation_check"]["foreign"] == foreign
        assert row["participant_display"] is None
        assert row["publication_allowed"] is False
        assert row["displayed_kind"] == "laboratory_preview"


@pytest.mark.asyncio
async def test_oversized_history_is_not_silently_clipped():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    provider = ProviderFixture()
    history = [
        {"input": "consistencia", "displayed_text": "x" * 4001, "displayed_kind": "laboratory_preview"}
    ]
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "¿Por qué?",
        history,
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["reason"] == "history_context_limit"
    assert row["history_omissions"]["oversized_fields"][0]["chars"] == 4001
    assert not provider.requests


@pytest.mark.asyncio
async def test_older_contextual_turn_is_recorded_and_requires_clarification():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    provider = ProviderFixture()
    history = [
        {
            "input": "consistencia requisitos",
            "displayed_text": "Referente original",
            "displayed_kind": "laboratory_preview",
        },
        *(
            {"input": "¿Entendido?", "displayed_text": f"Turno {i}", "displayed_kind": "operational"}
            for i in range(4)
        ),
    ]
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "¿Por qué?",
        history,
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["history_omissions"]["older_turns"] == 1
    assert row["reason"] == "history_context_limit"
    assert not provider.requests


@pytest.mark.asyncio
async def test_insufficient_expands_then_limits_without_generation():
    pages = [page("a", "Requisitos\nLa consistencia evita contradicciones.\n")]
    provider = ProviderFixture()
    assessor = AssessorFixture("insufficient", "insufficient")
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Otra cuestión sin respaldo",
        [],
        scope_assessor=ScopeAssessorFixture(),
        assessor=assessor,
        provider=provider,
    )
    assert row["evidence_attempts"].expanded is not None
    assert len(assessor.seen) == 2
    assert row["reason"] == "insufficient_or_unknown"
    assert row["displayed_kind"] == "operational"
    assert not provider.requests


@pytest.mark.asyncio
async def test_expansion_may_become_sufficient_but_only_fixture_says_so():
    pages = [page("a", "Pruebas\nLos casos de prueba encuentran fallos.\n")]
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "pruebas",
        [],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("insufficient", "sufficient"),
        provider=provider,
    )
    assert row["evidence_attempts"].expanded is not None
    assert len(provider.requests) == 1
    assert row["semantic_support"] == "unverified"
    assert row["publication_allowed"] is False


@pytest.mark.asyncio
async def test_conflict_and_retired_source_do_not_reach_provider():
    pages = [
        page("a", "Reglas\nSe permiten globos azules.\n"),
        page("b", "Reglas\nSe permiten globos rojos.\n"),
    ]
    units = build_units(pages)
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        pages,
        units,
        "globos azules y rojos",
        [],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("conflict"),
        provider=provider,
    )
    assert row["reason"] == "conflict"
    assert not provider.requests
    with pytest.raises(ValueError, match="outside authorized catalog"):
        await diagnostic_rag_turn(
            pages[:1],
            units,
            "globos",
            [],
            scope_assessor=ScopeAssessorFixture(),
            assessor=AssessorFixture("sufficient"),
            provider=provider,
        )
    assert not provider.requests


@pytest.mark.asyncio
async def test_confirmed_external_scope_requires_teacher_authority_and_skips_rag():
    provider = ProviderFixture()
    with pytest.raises(ValueError, match="teacher scope authority"):
        await diagnostic_rag_turn(
            [],
            [],
            "Calcula una integral",
            [],
            scope_assessor=ScopeAssessorFixture("out_of_scope"),
            assessor=AssessorFixture("sufficient"),
            provider=provider,
        )
    row = await diagnostic_rag_turn(
        [],
        [],
        "Calcula una integral",
        [],
        scope_assessor=ScopeAssessorFixture("out_of_scope", authority_ref="teacher-scope-fixture:v1"),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["scope_result"] == "out_of_scope"
    assert "no necesitas estudiarlo" in row["scope_notice"]
    assert row["evidence_attempts"] is None
    assert not provider.requests


@pytest.mark.asyncio
async def test_empty_or_quarantined_catalog_is_insufficient_not_external():
    provider = ProviderFixture()
    uncertain = await diagnostic_rag_turn(
        [],
        [],
        "Tema no encontrado",
        [],
        scope_assessor=ScopeAssessorFixture("uncertain_scope"),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert uncertain["scope_result"] == "uncertain_scope"
    assert "no necesitas" not in uncertain["displayed_text"]
    inside = await diagnostic_rag_turn(
        [],
        [],
        "Tema que consta en el temario pero está en página en cuarentena",
        [],
        scope_assessor=ScopeAssessorFixture(),
        assessor=AssessorFixture("insufficient", "insufficient"),
        provider=provider,
    )
    assert inside["scope_result"] == "in_scope_insufficient_evidence"
    assert "no necesitas" not in inside["displayed_text"]
    assert inside["evidence_attempts"].expanded is not None
    assert not provider.requests


@pytest.mark.asyncio
async def test_mixed_question_only_sends_inside_part_and_reports_exclusion():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        "Explica consistencia de requisitos y calcula una integral",
        [],
        scope_assessor=ScopeAssessorFixture(
            "mixed",
            authority_ref="teacher-scope-fixture:v1",
            in_scope_question="Explica consistencia de requisitos",
            excluded_part="calcula una integral",
        ),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["scope_result"] == "mixed_in_scope_with_evidence"
    assert "no necesitas estudiarla" in row["scope_notice"]
    assert "integral" not in provider.requests[0].student_input
    assert row["participant_display"] is None


@pytest.mark.asyncio
async def test_operational_request_bypasses_academic_scope_and_generation():
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        [],
        [],
        "¿Qué fuentes usas?",
        [],
        scope_assessor=ScopeAssessorFixture("operational"),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["scope_result"] == "operational"
    assert "no necesitas" not in row["displayed_text"]
    assert row["generation_request"] is None and not provider.requests


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("question", "scope_status", "expected"),
    [
        ("¿Cómo ayuda programar pruebas a verificar software?", "in_scope", "in_scope_with_evidence"),
        ("Usa una analogía sencilla para explicar pruebas", "in_scope", "in_scope_with_evidence"),
        ("¿Debo estudiar toda la sintaxis de Python?", "uncertain_scope", "uncertain_scope"),
    ],
)
async def test_near_scope_boundaries_do_not_turn_prerequisites_into_exclusions(
    question, scope_status, expected
):
    pages = [page("test", "Pruebas\nLas pruebas ejecutan software y observan fallos.\n")]
    provider = ProviderFixture()
    row = await diagnostic_rag_turn(
        pages,
        build_units(pages),
        question,
        [],
        scope_assessor=ScopeAssessorFixture(scope_status),
        assessor=AssessorFixture("sufficient"),
        provider=provider,
    )
    assert row["scope_result"] == expected
    assert "no necesitas" not in (row["scope_notice"] or "")
