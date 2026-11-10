"""V2 contract and described requests; fixtures never establish semantic quality."""

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.scope_classifier_v2 import ScopeSelectionV2, bind_v2, classify_scope_v2
from oralia.infrastructure.generation.generation_port import GenerationOutcome

POLICY = {"included_blocks": ["pruebas"], "excluded_as_standalone_blocks_for_this_activity": ["seguridad"]}
BASE = dict(
    primary_intent="excluded_standalone_request",
    included_block=None,
    excluded_block="seguridad",
    included=None,
    excluded=None,
    supporting_mention=None,
    referent_turn=None,
)


def test_exclusion_is_derived_without_a_second_model_vote():
    result = bind_v2(ScopeSelectionV2.model_validate(BASE), "Un curso de seguridad", [], POLICY, "hash")
    assert result.assessment.status == "out_of_scope"
    assert result.assessment.standalone_excluded_block is True
    assert result.rag_question is None and result.publication_allowed is False


@pytest.mark.parametrize("field", ["standalone", "status", "publication_allowed"])
def test_v2_rejects_old_or_authority_fields(field):
    with pytest.raises(ValueError):
        ScopeSelectionV2.model_validate({**BASE, field: True})


def test_auxiliary_is_not_exclusion_and_requires_anchor_and_literal_witness():
    data = {
        **BASE,
        "primary_intent": "included_with_supporting_mention",
        "included_block": "pruebas",
        "excluded_block": None,
        "supporting_mention": {"start": 0, "end": 9, "quote": "seguridad"},
    }
    result = bind_v2(ScopeSelectionV2.model_validate(data), "seguridad al probar", [], POLICY, "hash")
    assert result.assessment.status == "in_scope"
    assert result.assessment.standalone_excluded_block is False
    for patch in (
        {"included_block": None},
        {"supporting_mention": None},
        {"supporting_mention": {"start": 0, "end": 5, "quote": "falso"}},
    ):
        with pytest.raises(ValueError):
            bind_v2(
                ScopeSelectionV2.model_validate({**data, **patch}), "seguridad al probar", [], POLICY, "hash"
            )


def test_mixed_preserves_literal_boundary_and_never_appends_history():
    text = "Pruebas y seguridad"
    data = {
        **BASE,
        "primary_intent": "included_and_excluded_standalone_requests",
        "included_block": "pruebas",
        "included": {"start": 0, "end": 7, "quote": "Pruebas"},
        "excluded": {"start": 10, "end": 19, "quote": "seguridad"},
    }
    result = bind_v2(ScopeSelectionV2.model_validate(data), text, [], POLICY, "hash")
    assert result.rag_question == "Pruebas" and result.assessment.standalone_excluded_block
    with pytest.raises(ValueError):
        bind_v2(ScopeSelectionV2.model_validate({**data, "referent_turn": 0}), text, [], POLICY, "hash")
    with pytest.raises(ValueError):
        bind_v2(
            ScopeSelectionV2.model_validate({**data, "excluded": data["included"]}), text, [], POLICY, "hash"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("withdraw", [False, True])
async def test_descriptions_reach_request_and_are_revalidated(withdraw):
    seen = []
    state = {"active": True}
    descriptions = {
        "schema_version": 1,
        "blocks": [{"id": "pruebas", "title": "Pruebas", "description": "Tema sintético con fuente"}],
    }

    def revalidate(*_):
        if not state["active"]:
            raise ValueError("withdrawn")
        return POLICY

    class Provider:
        async def generate(self, request):
            seen.append(request)
            state["active"] = not withdraw
            return GenerationOutcome(
                ok=True, text=json.dumps(BASE), adapter="deterministic", finish_reason="stop"
            )

    binding = SimpleNamespace(revalidate=revalidate, policy_sha256="hash", assert_decision=lambda *_: None)
    metadata = SimpleNamespace(revalidate=lambda *_: descriptions, sha256="fixture-metadata-hash")
    if withdraw:
        with pytest.raises(ValueError):
            await classify_scope_v2(
                "curso de seguridad", [], provider=Provider(), binding=binding, db=None, metadata=metadata
            )
    else:
        result, _, _ = await classify_scope_v2(
            "curso de seguridad", [], provider=Provider(), binding=binding, db=None, metadata=metadata
        )
        assert result.assessment.status == "out_of_scope"
    payload = json.loads(seen[0].student_input)
    assert payload["block_descriptions"] == descriptions
    assert payload["block_metadata_sha256"] == "fixture-metadata-hash"
    assert "standalone" not in seen[0].output_schema["properties"]


def test_real_metadata_has_all_blocks_and_original_page_witnesses():
    from oralia.course_dialogue.corpus import SOURCE_ROOT
    from oralia.course_dialogue.scope_block_metadata import BlockMetadata

    root = Path(__file__).resolve().parents[2]
    evidence = root / "specs/012-conversational-course-study/evidence"
    path = evidence / "course-block-descriptions-v1.json"
    policy_path = evidence / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    binding = SimpleNamespace(
        source_root=SOURCE_ROOT, policy_sha256=hashlib.sha256(policy_path.read_bytes()).hexdigest()
    )
    catalog = BlockMetadata(path, hashlib.sha256(path.read_bytes()).hexdigest())
    data = catalog.revalidate(binding, policy)
    assert len(data["blocks"]) == 21
    assert all(row["title"] and row["description"] and row["provenance"] for row in data["blocks"])


@pytest.mark.parametrize("mutation", ["bytes", "inventory", "quote", "foreign_policy", "foreign_document"])
def test_metadata_corruption_blocks_delivery_before_provider(tmp_path, mutation):
    from oralia.course_dialogue.corpus import SOURCE_ROOT
    from oralia.course_dialogue.scope_block_metadata import BlockMetadata

    root = Path(__file__).resolve().parents[2]
    evidence = root / "specs/012-conversational-course-study/evidence"
    policy_path = evidence / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    raw = (evidence / "course-block-descriptions-v1.json").read_bytes()
    data = json.loads(raw)
    if mutation == "inventory":
        data["blocks"].pop()
    elif mutation == "quote":
        data["blocks"][0]["provenance"]["quote"] = "not a teacher quotation"
    elif mutation == "foreign_policy":
        data["policy_sha256"] = "foreign"
    elif mutation == "foreign_document":
        data["blocks"][0]["provenance"]["document"] = "student.pdf"
    path = tmp_path / "metadata.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    digest = hashlib.sha256(raw if mutation == "bytes" else path.read_bytes()).hexdigest()
    binding = SimpleNamespace(
        source_root=SOURCE_ROOT, policy_sha256=hashlib.sha256(policy_path.read_bytes()).hexdigest()
    )
    with pytest.raises(ValueError):
        BlockMetadata(path, digest).revalidate(binding, policy)


@pytest.mark.asyncio
async def test_real_described_request_delivers_every_policy_block():
    from oralia.course_dialogue.corpus import SOURCE_ROOT
    from oralia.course_dialogue.scope_block_metadata import BlockMetadata

    evidence = Path(__file__).resolve().parents[2] / "specs/012-conversational-course-study/evidence"
    policy_path = evidence / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    path = evidence / "course-block-descriptions-v1.json"
    catalog = BlockMetadata(path, hashlib.sha256(path.read_bytes()).hexdigest())
    binding = SimpleNamespace(
        source_root=SOURCE_ROOT,
        policy_sha256=hashlib.sha256(policy_path.read_bytes()).hexdigest(),
        revalidate=lambda *_: policy,
        assert_decision=lambda *_: None,
    )
    requests = []

    class Provider:
        async def generate(self, request):
            requests.append(request)
            return GenerationOutcome(
                ok=True, text=json.dumps(BASE), adapter="deterministic", finish_reason="stop"
            )

    result, _, _ = await classify_scope_v2(
        "bloque autónomo de seguridad", [], provider=Provider(), binding=binding, db=None, metadata=catalog
    )
    payload = json.loads(requests[0].student_input)
    assert len(payload["block_descriptions"]["blocks"]) == 21
    assert payload["block_metadata_sha256"] == catalog.sha256
    assert result.publication_allowed is False
    assert requests[0].evidence == []  # scope descriptions are not answer evidence
