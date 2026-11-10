"""Actual serialized frames through the adapter and the same profile validator as worker."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.scope_control_messages import ScopeControlRequest
from oralia.course_dialogue.scope_finite import classify_finite_scope
from oralia.course_dialogue.scope_message_profiles import validate_frame_profile
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationError, GenerationRequest

EVIDENCE = Path(__file__).resolve().parents[2] / "specs/012-conversational-course-study/evidence"


class Process:
    returncode = None

    def __init__(self, answers, profile_reply=True, change=None):
        self.answers = iter(answers)
        self.frames = []
        self.profile_reply = profile_reply
        self.change = change
        self.stdin = SimpleNamespace(write=self.write, drain=self.drain)
        self.stdout = SimpleNamespace(readline=self.readline)

    def write(self, data):
        self.frames.append(json.loads(data))

    async def drain(self):
        pass

    async def readline(self):
        frame = self.frames[-1]
        profile = validate_frame_profile(frame)
        answer = next(self.answers)
        if self.change:
            self.change()
        reply = {
            "id": frame["id"],
            "type": "result",
            "text": answer if isinstance(answer, str) else json.dumps(answer),
            "finish_reason": "stop",
            "input_tokens": 10,
            "output_tokens": 5,
            "latency_ms": 1,
            "finite_decoder": frame["finite_outputs"] is not None,
        }
        if self.profile_reply:
            reply["message_profile"] = profile
        return json.dumps(reply).encode()

    def terminate(self):
        self.returncode = 0


def fixture_inputs():
    policy = {
        "included_blocks": ["pruebas"],
        "excluded_as_standalone_blocks_for_this_activity": ["seguridad"],
    }
    binding = SimpleNamespace(
        revalidate=lambda *_: policy, policy_sha256="fixture", assert_decision=lambda *_: None
    )
    metadata = SimpleNamespace(
        sha256="fixture",
        revalidate=lambda *_: {"blocks": [{"id": "pruebas", "title": "Pruebas", "description": "Fixture"}]},
    )
    return binding, metadata


@pytest.mark.asyncio
async def test_connected_reference_target_and_open_literal_profiles_reach_transport():
    process = Process([{"referent": "0"}, {"intent": "auxiliary", "anchor": "pruebas"}, "seguridad"])
    adapter = CachedTransformersGenerationAdapter(process, message_profile="scope-control/v1")
    binding, metadata = fixture_inputs()
    history = [{"input": "pruebas", "displayed_text": "Vista previa", "displayed_kind": "laboratory_preview"}]
    result = await classify_finite_scope(
        "Pon un ejemplo de eso con seguridad",
        history,
        provider=adapter,
        binding=binding,
        db=None,
        metadata=metadata,
    )
    assert result.assessment.status == "in_scope" and result.referent_turn == 0
    assert [frame["message_profile"] for frame in process.frames] == [
        "scope-control-finite/v1",
        "scope-control-finite/v1",
        "scope-control-literal/v1",
    ]
    assert all("<scope_control_data>" in f["messages"][1]["content"] for f in process.frames)
    assert all(
        "Responde únicamente usando el contenido de las etiquetas <evidencia>"
        not in f["messages"][1]["content"]
        for f in process.frames
    )
    assert process.frames[0]["finite_outputs"] and process.frames[1]["finite_outputs"]
    assert process.frames[2]["finite_outputs"] is None
    for receipt in result.receipts:
        exchange = receipt["exchange"]
        assert exchange["confirmed_message_profile"] == exchange["effective_message_profile"]
    assert sum(frame["max_tokens"] for frame in process.frames) <= 512
    assert all(0 < frame["deadline_ms"] <= 30000 for frame in process.frames)


@pytest.mark.asyncio
async def test_academic_default_preserves_original_serialized_messages_exactly():
    audit = json.loads((EVIDENCE / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    process = Process(["fixture"])
    await CachedTransformersGenerationAdapter(process).generate(
        GenerationRequest.model_validate(audit["original_attempt"]["request"])
    )
    assert process.frames[0]["messages"] == audit["frame"]["messages"]
    assert "message_profile" not in process.frames[0]


@pytest.mark.asyncio
async def test_academic_evidence_and_grounding_are_kept():
    process = Process(["fixture"])
    academic = GenerationRequest(
        purpose="explicacion",
        instruction="Explain from sources",
        student_input="question",
        evidence=[
            EvidenceItem(fragment_id="id", text="source passage", document_id="doc", document_version=1)
        ],
    )
    await CachedTransformersGenerationAdapter(process).generate(academic)
    user = process.frames[0]["messages"][1]["content"]
    assert '<evidencia documento="doc" version="1">\nsource passage\n</evidencia>' in user
    assert "Responde únicamente usando el contenido de las etiquetas <evidencia>" in user


@pytest.mark.asyncio
async def test_academic_misuse_is_rejected_before_any_transport_frame():
    process = Process([])
    adapter = CachedTransformersGenerationAdapter(process, message_profile="scope-control/v1")
    with pytest.raises(ValueError, match="typed"):
        await adapter.generate(GenerationRequest(purpose="explicacion", instruction="Answer academically"))
    bad = ScopeControlRequest(
        control_step="target",
        purpose="explicacion",
        instruction="Teach without evidence",
        student_input=json.dumps(
            {
                "policy_sha256": "x",
                "blocks": {},
                "metadata_sha256": "x",
                "question": "x",
                "selected_shown_history": [],
            }
        ),
        output_schema={"type": "object", "x-oralia-finite-outputs": ['{"intent":"unclear"}']},
    )
    with pytest.raises(ValueError, match="instruction mismatch"):
        await adapter.generate(bad)
    assert process.frames == []


@pytest.mark.asyncio
async def test_control_cannot_silently_use_the_default_academic_profile():
    process = Process([])
    binding, metadata = fixture_inputs()
    with pytest.raises(ValueError, match="explicit scope-control"):
        await classify_finite_scope(
            "pruebas",
            [],
            provider=CachedTransformersGenerationAdapter(process),
            binding=binding,
            db=None,
            metadata=metadata,
        )
    assert process.frames == []


@pytest.mark.asyncio
async def test_profile_confirmation_is_required_and_retirement_still_blocks():
    binding, metadata = fixture_inputs()
    process = Process([{"intent": "included", "block": "pruebas"}], profile_reply=False)
    adapter = CachedTransformersGenerationAdapter(process, message_profile="scope-control/v1")
    with pytest.raises(GenerationError, match="perfil"):
        await classify_finite_scope(
            "pruebas", [], provider=adapter, binding=binding, metadata=metadata, db=None
        )
    assert adapter.usable is False and process.returncode == 0
    active = [True]

    def current(_):
        if not active[0]:
            raise ValueError("withdrawn")
        return {
            "included_blocks": ["pruebas"],
            "excluded_as_standalone_blocks_for_this_activity": ["seguridad"],
        }

    binding.revalidate = current
    process = Process(
        [{"intent": "included", "block": "pruebas"}], change=lambda: active.__setitem__(0, False)
    )
    adapter = CachedTransformersGenerationAdapter(process, message_profile="scope-control/v1")
    with pytest.raises(ValueError, match="withdrawn"):
        await classify_finite_scope(
            "pruebas", [], provider=adapter, binding=binding, metadata=metadata, db=None
        )
    assert len(process.frames) == 1
