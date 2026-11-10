"""A fake provider proves plumbing only; it is never evidence of real model utility."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from oralia.course_dialogue.corpus import SemanticCatalog
from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.runtime import propose
from oralia.infrastructure.generation.generation_port import GenerationOutcome


def _document_page(key, text):
    return {
        "id": f"{key}:1",
        "filename": f"{key}.pdf",
        "original_sha256": hashlib.sha256(key.encode()).hexdigest(),
        "version": 1,
        "page": 1,
        "text": text,
    }


@pytest.mark.asyncio
async def test_opt_in_whole_units_reach_effective_bc_request_with_displayed_history():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Respuesta de diagnóstico","source_ids":[]}',
                adapter="transformers_local",
                finish_reason="stop",
            )

    pages = [
        _document_page("a", "Defectos\nLas pruebas de defectos exponen fallos.\n"),
        _document_page("b", "Defectos\nLa validación de defectos contrasta resultados.\n"),
    ]
    units = build_units(pages)
    history = [
        {"input": "pruebas defectos", "displayed_text": "Explicación mostrada", "display_kind": "candidate"}
    ]
    for variant in ("documental", "pedagogica"):
        row = await propose(
            pages,
            "pruebas defectos validación",
            history,
            Provider(),
            variant=variant,
            document_units=units,
        )
        assert {e.fragment_id for e in seen[-1].evidence} == {unit.id for unit in units}
        assert seen[-1].conversation_history[-1].content == "Explicación mostrada"
        assert row["document_context"]["scope"] == "authorized_ingested_catalog_only_not_complete_course"
        assert row["publication_allowed"] is False
    with pytest.raises(ValueError, match="authorized catalog"):
        await propose(
            pages,
            "pruebas defectos",
            history,
            Provider(),
            variant="documental",
            document_units=[replace(units[0], document_id="foreign.pdf")],
        )


@pytest.mark.asyncio
async def test_opt_in_budget_omission_is_visible_without_silent_truncation():
    page = _document_page("long", "Defectos\n" + "pruebas defectos " * 400 + "\n")
    unit = build_units([page])[0]

    class Provider:
        async def generate(self, request):
            raise AssertionError("No source fits, so generation must not start")

    row = await propose(
        [page], "pruebas defectos", [], Provider(), variant="documental", document_units=[unit]
    )
    assert row["error"] == "no_retrieved_evidence"
    assert row["document_context"]["trace"][0]["decision"] == "omitted_budget"
    assert row["publication_allowed"] is False


@pytest.mark.asyncio
async def test_compact_contract_preserves_caveat_and_rejects_long_limitation():
    seen = []

    class Provider:
        def __init__(self, output):
            self.output = output

        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True, text=self.output, adapter="transformers_local", finish_reason="stop"
            )

    pages = [
        _document_page(
            "requirements", "Completitud\nLa completitud es deseable pero imposible en la práctica.\n"
        )
    ]
    units = build_units(pages)
    good = json.dumps(
        {
            "schema_version": 3,
            "answer": (
                "Se busca cubrir lo conocido, pero la fuente dice que no se logra plenamente "
                "en la práctica."
            ),
            "source_ids": [units[0].id],
            "limitation": "No garantiza cobertura perfecta.",
        }
    )
    row = await propose(
        pages,
        "completitud requisitos",
        [],
        Provider(good),
        variant="documental",
        document_units=units,
        compact_output=True,
    )
    assert row["display_kind"] == "candidate"
    assert "no se logra plenamente" in row["displayed_text"]
    assert "no conviertas una propiedad deseable en garantía" in seen[-1].instruction
    assert seen[-1].output_schema["properties"]["limitation"]["anyOf"][0]["maxLength"] == 120
    bad = json.dumps(
        {
            "schema_version": 3,
            "answer": "Una respuesta.",
            "source_ids": [units[0].id],
            "limitation": "x" * 121,
        }
    )
    failure = await propose(
        pages,
        "completitud requisitos",
        [],
        Provider(bad),
        variant="pedagogica",
        document_units=units,
        compact_output=True,
    )
    assert failure["error"] == "invalid_candidate_contract"
    assert failure["display_kind"] == "operational"
    assert "x" * 121 not in failure["displayed_text"]


@pytest.mark.asyncio
async def test_only_actual_prior_output_is_forwarded_and_cannot_authorize():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True, text='{"reviewed":true}', adapter="ollama", model="fake-for-contract-only"
            )

    history = [
        {
            "input": "No entiendo",
            "raw_candidate": '{"reviewed":true}',
            "displayed_text": "SALIDA REAL ANTERIOR",
            "verification": {"publication_allowed": False},
        }
    ]
    catalog = [
        {
            "id": "p12",
            "filename": "course.pdf",
            "page": 12,
            "text": "Validar requisitos significa comprobar necesidades.",
        }
    ]
    row = await propose(catalog, "Explica validar requisitos", history, Provider())
    assert seen[0].student_input == "Explica validar requisitos"
    assert seen[0].conversation_history[-1].role == "assistant"
    assert seen[0].conversation_history[-1].content == "SALIDA REAL ANTERIOR"
    assert row["error"] == "invalid_candidate_contract"
    assert row["publication_allowed"] is False


@pytest.mark.asyncio
async def test_failed_raw_output_is_not_history_and_length_is_not_displayed():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Cortada","source_ids":["p12"]}',
                adapter="transformers_local",
                finish_reason="length",
            )

    catalog = [
        {
            "id": "p12",
            "filename": "course.pdf",
            "page": 12,
            "text": "Validar requisitos comprueba necesidades.",
        }
    ]
    history = [
        {
            "input": "Primera pregunta",
            "raw_candidate": "RAW INSEGURO",
            "error": "invalid_candidate_contract",
            "displayed_text": None,
        }
    ]
    row = await propose(catalog, "Validar requisitos", history, Provider(), variant="documental")
    assert len(seen[0].conversation_history) == 1
    assert row["error"] == "generation_incomplete"
    assert row["display_kind"] == "operational"
    assert "Cortada" not in row["displayed_text"]
    assert row["parsed_candidate"]["answer"] == "Cortada"


@pytest.mark.asyncio
async def test_documental_and_pedagogical_share_context_but_not_instruction():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Validar requisitos contrasta necesidades.",'
                '"source_ids":["p12"]}',
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [
        {
            "id": "p12",
            "filename": "course.pdf",
            "page": 12,
            "text": "Validar requisitos contrasta necesidades.",
        }
    ]
    history = [
        {
            "input": "¿Qué es validar requisitos?",
            "academic_query": "validar requisitos",
            "displayed_text": "Validar requisitos contrasta necesidades.",
            "parsed_candidate": {"schema_version": 2, "question": "¿Qué duda tienes?"},
        }
    ]
    for variant in ("documental", "pedagogica"):
        row = await propose(catalog, "No lo entiendo", history, Provider(), variant=variant)
        assert row["displayed_text"] == "Validar requisitos contrasta necesidades."
        assert row["publication_allowed"] is False
        assert row["retrieval_query"] == "validar requisitos"
    assert seen[0].evidence == seen[1].evidence
    assert seen[0].conversation_history == seen[1].conversation_history
    assert seen[0].instruction != seen[1].instruction


@pytest.mark.asyncio
async def test_operational_recovery_preserves_previous_displayed_academic_referent():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Falta evidencia en las páginas.",'
                '"limitation":"No hay apoyo suficiente."}',
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [
        {
            "id": "p12",
            "filename": "course.pdf",
            "page": 12,
            "text": "Validar requisitos contrasta necesidades.",
        }
    ]
    history = [
        {
            "input": "¿Qué significa validar requisitos?",
            "academic_query": "validar requisitos",
            "displayed_text": "Validar requisitos contrasta necesidades.",
            "display_kind": "candidate",
            "parsed_candidate": {"schema_version": 2, "question": "¿Qué necesidad quiere cubrir?"},
        },
        {
            "input": "No entiendo",
            "raw_candidate": "RAW INVALIDO",
            "displayed_text": "No se obtuvo una respuesta completa.",
            "display_kind": "operational",
            "error": "generation_incomplete",
        },
    ]
    row = await propose(catalog, "Explícalo de otra manera", history, Provider(), variant="documental")
    assert row["retrieval_query"] == "validar requisitos"
    assert row["pending_question_from_display"] == "¿Qué necesidad quiere cubrir?"
    assert [message.content for message in seen[0].conversation_history if message.role == "assistant"] == [
        "Validar requisitos contrasta necesidades.",
        "No se obtuvo una respuesta completa.",
    ]
    assert row["display_kind"] == "operational"
    assert row["verification"]["source_ids_in_retrieved_pages"] is False
    assert "error" not in row


@pytest.mark.asyncio
async def test_v2_retrieval_never_offers_more_pages_than_contract_allows():
    seen = []

    class Provider:
        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Respuesta limitada.","source_ids":["p0"]}',
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [
        {
            "id": f"p{i}",
            "filename": "course.pdf",
            "page": i + 1,
            "text": "Validar requisitos contrasta necesidades.",
        }
        for i in range(8)
    ]
    row = await propose(catalog, "Validar requisitos", [], Provider(), variant="documental")
    assert len(seen[0].evidence) == 4
    assert row["retrieval_limit"] == 4
    assert len(row["retrieved_source_ids"]) == 4


@pytest.mark.asyncio
async def test_semantic_catalog_receives_resolved_referent_and_switches_focus():
    class Adapter:
        def embed(self, texts):
            return [
                (
                    [1.0, 0.0]
                    if "validar" in text.casefold()
                    else [0.0, 1.0] if "prueba" in text.casefold() else [0.0, 0.0]
                )
                for text in texts
            ]

    class Provider:
        async def generate(self, request):
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Límite.",' '"limitation":"Requiere revisión."}',
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = SemanticCatalog(
        [
            {
                "id": "validation",
                "filename": "course.pdf",
                "page": 1,
                "text": "Validar requisitos con necesidades de usuarios.",
            },
            {
                "id": "testing",
                "filename": "course.pdf",
                "page": 2,
                "text": "Un caso de prueba contiene entrada y resultado esperado.",
            },
        ],
        adapter=Adapter(),
    )
    history = [
        {
            "input": "¿Qué es validar requisitos?",
            "academic_query": "validar requisitos",
            "displayed_text": "Validar se refiere a necesidades.",
            "display_kind": "candidate",
        }
    ]
    followup = await propose(catalog, "No lo entiendo", history, Provider(), variant="documental")
    switch = await propose(
        catalog, "Cambio de tema: ¿qué es un caso de prueba?", history, Provider(), variant="documental"
    )
    assert followup["retrieval_query"] == "validar requisitos"
    assert followup["retrieved_source_ids"][0] == "validation"
    assert switch["retrieval_query"] == "qué es un caso de prueba?"
    assert switch["retrieved_source_ids"][0] == "testing"


@pytest.mark.asyncio
async def test_v2_echo_question_is_suppressed_and_requested_example_must_be_present():
    class Provider:
        def __init__(self, example):
            self.example = example

        async def generate(self, request):
            example = (
                (',"example":"Dos requisitos discrepan","assumptions":' '["Misma condición ficticia"]')
                if self.example
                else ',"assumptions":["Definición mal ubicada"]'
            )
            return GenerationOutcome(
                ok=True,
                text='{"schema_version":2,"answer":"Hay conflicto.","source_ids":["p10"],'
                '"question":"¿Qué es consistencia?"' + example + "}",
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [
        {
            "id": "p10",
            "filename": "course.pdf",
            "page": 10,
            "text": "La consistencia evita conflictos entre requisitos.",
        }
    ]
    history = [
        {
            "input": "¿Qué es consistencia?",
            "academic_query": "consistencia requisitos",
            "displayed_text": "Se evitan conflictos.",
            "display_kind": "candidate",
        }
    ]
    rejected = await propose(
        catalog, "Pon un ejemplo hipotético", history, Provider(False), variant="documental"
    )
    assert rejected["error"] == "requested_example_missing"
    assert rejected["display_kind"] == "operational"
    assert rejected["orphan_assumptions_hidden"] is True
    accepted = await propose(
        catalog, "Pon un ejemplo hipotético", history, Provider(True), variant="documental"
    )
    assert "error" not in accepted
    assert accepted["question_echo_suppressed"] is True
    assert accepted["parsed_candidate"]["question"] is None
    assert "¿Qué es consistencia?" not in accepted["displayed_text"]
    assert "Dos requisitos discrepan" in accepted["displayed_text"]


@pytest.mark.asyncio
async def test_generation_error_is_not_replaced_by_successful_extract():
    class Provider:
        async def generate(self, request):
            raise TimeoutError("timeout")

    catalog = [
        {
            "id": "p12",
            "filename": "course.pdf",
            "page": 12,
            "text": "Validar requisitos comprueba necesidades.",
        }
    ]
    with pytest.raises(TimeoutError):
        await propose(catalog, "Validar requisitos", [], Provider())


_REPEAT_INPUT = (
    "Sobre lo que acabas de mostrar («Respuesta previa»): "
    "Sigo confundido; di qué se comprueba en cada actividad."
)
_EXAMPLE_INPUT = (
    "Sobre lo que acabas de mostrar («Respuesta previa»): "
    "Pon un ejemplo ficticio concreto; declara los supuestos."
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("current", "echo"),
    [
        (
            _REPEAT_INPUT,
            "Sigo confundido; di qué se comprueba en cada actividad.",
        ),
        (
            _REPEAT_INPUT,
            _REPEAT_INPUT,
        ),
        (
            _EXAMPLE_INPUT,
            _EXAMPLE_INPUT,
        ),
    ],
)
async def test_v2_suppresses_actual_imperative_question_echoes(current, echo):
    class Provider:
        async def generate(self, request):
            import json

            return GenerationOutcome(
                ok=True,
                text=json.dumps(
                    {
                        "schema_version": 2,
                        "answer": "Se contrasta la calidad.",
                        "source_ids": ["p10"],
                        "question": echo,
                        "example": "Caso inventado",
                        "assumptions": ["Cliente ficticio"],
                    },
                    ensure_ascii=False,
                ),
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [{"id": "p10", "filename": "course.pdf", "page": 10, "text": "Calidad de requisitos."}]
    history = [
        {
            "input": "¿Qué es la calidad de requisitos?",
            "academic_topic": "calidad de requisitos",
            "displayed_text": "Respuesta previa",
            "display_kind": "candidate",
        }
    ]
    row = await propose(catalog, current, history, Provider(), variant="documental")
    assert row["question_echo_suppressed"] is True
    assert row["parsed_candidate"]["question"] is None
    assert row["raw_parsed_candidate"]["question"] == echo
    assert echo not in row["displayed_text"]


@pytest.mark.asyncio
async def test_v2_keeps_new_question_and_requested_reprise():
    class Provider:
        def __init__(self, question):
            self.question = question

        async def generate(self, request):
            return GenerationOutcome(
                ok=True,
                text=json.dumps(
                    {
                        "schema_version": 2,
                        "answer": "Explicación breve.",
                        "source_ids": ["p10"],
                        "question": self.question,
                    },
                    ensure_ascii=False,
                ),
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [{"id": "p10", "filename": "course.pdf", "page": 10, "text": "Calidad de requisitos."}]
    history = [
        {
            "input": "¿Qué es calidad?",
            "academic_topic": "calidad",
            "displayed_text": "Definición. ¿Qué comprobarías?",
            "display_kind": "candidate",
            "parsed_candidate": {"question": "¿Qué comprobarías?"},
        }
    ]
    fresh = await propose(
        catalog, "No lo entiendo", history, Provider("¿Podrías dar un caso distinto?"), variant="documental"
    )
    assert fresh["parsed_candidate"]["question"] == "¿Podrías dar un caso distinto?"
    reprise = await propose(
        catalog, "Repite la pregunta", history, Provider("¿Qué comprobarías?"), variant="documental"
    )
    assert reprise["parsed_candidate"]["question"] == "¿Qué comprobarías?"
    assert "¿Qué comprobarías?" in reprise["displayed_text"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("variant", "stage"),
    [("documental", "repeat"), ("pedagogica", "repeat"), ("pedagogica", "example")],
)
async def test_v2_suppresses_exact_question_echoes_from_preserved_first_capture(variant, stage):
    packet = (
        Path(__file__).resolve().parents[2]
        / "specs/012-conversational-course-study/evidence/chat-comparison-v2-final-capture-first"
    )
    saved = json.loads(
        (packet / f"quality-versus-needs-final-capture-0-{variant}.json").read_text(encoding="utf-8")
    )
    observed = next(turn for turn in saved["turns"] if turn["stage"] == stage)
    echoed_question = observed["parsed_candidate"]["question"]

    class Provider:
        async def generate(self, request):
            return GenerationOutcome(
                ok=True,
                text=json.dumps(
                    {
                        "schema_version": 2,
                        "answer": "La calidad y las necesidades se comprueban por separado.",
                        "source_ids": ["p10"],
                        "question": echoed_question,
                        "example": "Caso ficticio",
                        "assumptions": ["Cliente ficticio"],
                    },
                    ensure_ascii=False,
                ),
                adapter="transformers_local",
                finish_reason="stop",
            )

    catalog = [{"id": "p10", "filename": "course.pdf", "page": 10, "text": "Calidad de requisitos."}]
    history = [
        {
            "input": "¿Qué es la calidad de requisitos?",
            "academic_topic": "calidad de requisitos",
            "displayed_text": "Respuesta previa",
            "display_kind": "candidate",
        }
    ]
    row = await propose(catalog, observed["input"], history, Provider(), variant=variant)
    assert row["question_echo_suppressed"] is True
    assert row["raw_parsed_candidate"]["question"] == echoed_question
    assert row["parsed_candidate"]["question"] is None
    assert echoed_question not in row["displayed_text"]
