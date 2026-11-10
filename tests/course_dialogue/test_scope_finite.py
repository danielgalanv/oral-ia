"""Finite enforcement, conditional steps, uncertainty and a shared wall budget."""

import json
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.scope_finite import (
    FiniteScopeError,
    classify_finite_scope,
    compile_targets,
    literal_span,
)
from oralia.infrastructure.generation.generation_port import GenerationOutcome

POLICY = {"included_blocks": ["pruebas"], "excluded_as_standalone_blocks_for_this_activity": ["seguridad"]}


class Port:
    def __init__(self, answers, *, finite=True, change=None):
        self.answers = iter(answers)
        self.requests = []
        self.last_exchange = None
        self.finite = finite
        self.change = change

    async def generate(self, request):
        self.requests.append(request)
        value = next(self.answers)
        text = json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value
        flag = bool(request.output_schema) and self.finite
        self.last_exchange = {
            "raw_worker_response": json.dumps(
                {
                    "finite_decoder": flag,
                    "text": text,
                    "message_profile": (
                        "scope-control-finite/v1"
                        if request.output_schema is not None
                        else "scope-control-literal/v1"
                    ),
                }
            )
        }
        if self.change:
            self.change()
        return GenerationOutcome(
            ok=True,
            text=text,
            adapter="deterministic",
            finish_reason="stop",
            parameters={"finite_decoder": flag},
        )


def inputs(policy=None):
    policy = policy or POLICY
    binding = SimpleNamespace(
        revalidate=lambda *_: policy, policy_sha256="policy", assert_decision=lambda *_: None
    )
    metadata = SimpleNamespace(
        sha256="metadata",
        revalidate=lambda *_: {
            "blocks": [{"id": "pruebas", "title": "Pruebas", "description": "Fixture de alcance"}]
        },
    )
    return binding, metadata


async def run(text, answers, history=(), **kwargs):
    provider = Port(answers, **kwargs.pop("port_options", {}))
    binding, metadata = inputs(kwargs.pop("policy", None))
    result = await classify_finite_scope(
        text, list(history), provider=provider, binding=binding, metadata=metadata, db=None, **kwargs
    )
    return result, provider


def test_policy_compiler_never_truncates_to_120_or_backend_capacity():
    assert len(finite_json_outputs(compile_targets(POLICY))) == 6
    expanded = {
        "included_blocks": [f"in{i}" for i in range(20)],
        "excluded_as_standalone_blocks_for_this_activity": [f"out{i}" for i in range(20)],
    }
    with pytest.raises(FiniteScopeError, match="462 alternatives.*256"):
        compile_targets(expanded)
    with pytest.raises(FiniteScopeError, match="512-character"):
        compile_targets({**POLICY, "included_blocks": ["x" * 512]})


def test_exact_unicode_literals_reject_ambiguous_and_never_normalize():
    assert literal_span("¿Ética? Sí.", "Sí") == (8, 10)
    assert literal_span("x y x", "x") is None
    assert literal_span("Ética", "ética") is None
    assert literal_span("texto", "") is None


@pytest.mark.asyncio
async def test_simple_included_one_real_finite_step_without_inapplicable_fields():
    result, provider = await run("pruebas", [{"intent": "included", "block": "pruebas"}])
    assert len(provider.requests) == 1 and result.assessment.status == "in_scope"
    assert result.rag_question == "pruebas" and result.rag_history == ()
    assert result.publication_allowed is False and result.semantic_verification == "unverified"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "choice", [{"intent": "included", "block": "pruebas"}, {"intent": "included", "block": "foreign"}]
)
async def test_no_hint_fallback_or_foreign_choice_is_accepted(choice):
    with pytest.raises(FiniteScopeError, match="finite_decoder=true") as error:
        await run("pruebas", [choice], port_options={"finite": False})
    assert len(error.value.receipts) == 1
    if choice["block"] == "foreign":
        with pytest.raises(FiniteScopeError, match="outside"):
            await run("pruebas", [choice])


@pytest.mark.asyncio
async def test_mixed_literal_spans_never_restore_excluded_history():
    history = [
        {"input": "seguridad como curso", "displayed_text": "Aviso previo", "displayed_kind": "operational"}
    ]
    result, provider = await run(
        "Explica pruebas y curso de seguridad",
        [
            {"intent": "mixed", "included_block": "pruebas", "excluded_block": "seguridad"},
            "Explica pruebas",
            "curso de seguridad",
        ],
        history,
    )
    assert len(provider.requests) == 3
    assert result.rag_question == "Explica pruebas" and result.rag_history == ()
    assert "seguridad" not in result.rag_question
    assert result.assessment.excluded_part == "curso de seguridad"
    assert all(not r.conversation_history for r in provider.requests)
    assert result.literal_decoder_constrained is False


@pytest.mark.asyncio
@pytest.mark.parametrize("quote", ["pruebas", "inventado"])
async def test_repeated_or_absent_literal_returns_uncertainty(quote):
    result, provider = await run(
        "pruebas y pruebas",
        [
            {"intent": "auxiliary", "anchor": "pruebas"},
            quote,
        ],
    )
    assert result.assessment.status == "uncertain_scope" and result.rag_question is None
    assert len(provider.requests) == 2


@pytest.mark.asyncio
async def test_reference_is_conditional_and_ambiguous_reference_stops_early():
    history = [{"input": "pruebas", "displayed_text": "Vista previa", "displayed_kind": "laboratory_preview"}]
    result, provider = await run("¿Por qué?", [{"referent": "none"}], history)
    assert result.assessment.status == "uncertain_scope" and len(provider.requests) == 1
    result, provider = await run(
        "¿Por qué?", [{"referent": "0"}, {"intent": "included", "block": "pruebas"}], history
    )
    assert result.referent_turn == 0 and len(provider.requests) == 2
    assert result.rag_question == "Pruebas\n¿Por qué?"


@pytest.mark.asyncio
async def test_shared_budget_expires_between_steps_and_receipts_survive():
    now = [0.0]
    captured = []
    result, provider = await run(
        "pruebas y seguridad",
        [{"intent": "mixed", "included_block": "pruebas", "excluded_block": "seguridad"}],
        clock=lambda: now[0],
        port_options={"change": lambda: now.__setitem__(0, 29.5)},
        receipt_sink=lambda rows: captured.append(len(rows)),
    )
    assert len(provider.requests) == 1 and len(result.receipts) == 1
    assert result.assessment.status == "uncertain_scope" and captured


@pytest.mark.asyncio
async def test_withdrawal_during_step_blocks_even_with_a_finite_result():
    binding, metadata = inputs()
    active = [True]

    def revalidate(_):
        if not active[0]:
            raise ValueError("withdrawn")
        return POLICY

    binding.revalidate = revalidate
    captured = []
    provider = Port([{"intent": "included", "block": "pruebas"}], change=lambda: active.__setitem__(0, False))
    with pytest.raises(ValueError, match="withdrawn"):
        await classify_finite_scope(
            "pruebas",
            [],
            provider=provider,
            binding=binding,
            metadata=metadata,
            db=None,
            receipt_sink=lambda rows: captured.append(rows),
        )
    assert len(provider.requests) == 1 and captured[-1][0]["outcome"] is not None


@pytest.mark.asyncio
async def test_four_conditional_steps_share_512_tokens_and_one_wall_deadline():
    now = [0.0]
    history = [{"input": "pruebas", "displayed_text": "Vista previa", "displayed_kind": "laboratory_preview"}]
    result, provider = await run(
        "Pon un ejemplo de eso y seguridad como curso",
        [
            {"referent": "0"},
            {"intent": "mixed", "included_block": "pruebas", "excluded_block": "seguridad"},
            "Pon un ejemplo de eso",
            "seguridad como curso",
        ],
        history,
        clock=lambda: now[0],
        port_options={"change": lambda: now.__setitem__(0, now[0] + 1)},
    )
    assert len(provider.requests) == 4 and result.assessment.status == "mixed"
    assert sum(r.constraints.max_tokens for r in provider.requests) == 512
    deadlines = [r.constraints.deadline_ms for r in provider.requests]
    assert deadlines == sorted(deadlines, reverse=True) and deadlines[-1] < deadlines[0]
    assert result.rag_history == () and result.rag_question == "Pon un ejemplo de eso"


@pytest.mark.asyncio
async def test_overlapping_witnesses_return_uncertainty_without_repair():
    result, provider = await run(
        "pruebas y seguridad",
        [
            {"intent": "mixed", "included_block": "pruebas", "excluded_block": "seguridad"},
            "pruebas",
            "pruebas",
        ],
    )
    assert len(provider.requests) == 3 and result.reason == "mixed_literals_overlap"
    assert result.rag_question is None
