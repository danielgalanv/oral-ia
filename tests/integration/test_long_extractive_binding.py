"""Finite boundary matrix: trusted DB projection, real T090 verifier, no model authority."""

import asyncio
import hashlib
import json
import uuid

import pytest

from oralia.application.orchestration.final_output_gate import persist_final_output
from oralia.application.orchestration.self_study_agency_composer import _decide_study_output
from oralia.domain.materials.extractive_excerpt import extractive_excerpt
from oralia.infrastructure.db import models
from oralia.infrastructure.generation.deterministic_adapter import DeterministicGenerationAdapter
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationRequest
from tests.integration.test_t090_self_study_fallback_red import _local_context


def raw_text(length):
    return ("El agua hierve a 100 grados. " + "café 🧪 é presión líquido " * 100)[:length]


def seed_fragments(db, count, length):
    rows = []
    for i in range(count):
        if i == 0:
            row = db.get(models.MaterialFragment, "fragment-t096")
        else:
            original = rows[0]
            row = models.MaterialFragment(
                id=f"fragment-009-{i}",
                document_id=original.document_id,
                document_version=1,
                location_ref=f"p. {i+1}",
                sequence_index=i,
                embedding_ref=f"embedding-{i}",
                content_type="texto",
                course_id=original.course_id,
                activity_configuration_ids=original.activity_configuration_ids,
                indexing_status="indexed",
            )
            db.add(row)
        row.text = raw_text(length) + ("" if i == 0 else f" Fuente{i}")
        rows.append(row)
    db.flush()
    return [
        {
            "fragment_id": r.id,
            "document_id": r.document_id,
            "document_version": r.document_version,
            "location_ref": r.location_ref,
            "text": r.text,
        }
        for r in rows
    ]


def candidate(fragments):
    request = GenerationRequest(
        purpose="explicacion",
        instruction="explicar agua",
        evidence=[EvidenceItem(**{k: v for k, v in f.items() if k != "location_ref"}) for f in fragments],
    )
    return asyncio.run(DeterministicGenerationAdapter().generate(request)).text


def decide(db, session, fragments, text):
    turn = models.Turn(
        id=str(uuid.uuid4()), session_id=session.id, index=1, input_text="agua", status="in_progress"
    )
    db.add(turn)
    db.flush()
    result = asyncio.run(
        _decide_study_output(
            db,
            session=session,
            turn_id=turn.id,
            text=text,
            fragments_used=fragments,
            general_knowledge_used=False,
        )
    )
    return result, turn


@pytest.mark.parametrize("length", [399, 400, 401, 800])
@pytest.mark.parametrize("count", [1, 2, 3, 4])
def test_canonical_projection_lengths_multiple_unicode_and_trace(tmp_path, length, count):
    templates = [
        ["material-fragment-response", 1],
        ["material-fragment-response-2", 1],
        ["material-fragment-response-3", 1],
    ]
    with _local_context(tmp_path, mode="doubt_resolution", allowed_templates=templates) as (
        db,
        session,
        _,
        _,
    ):
        fragments = seed_fragments(db, count, length)
        text = candidate(fragments)
        result, turn = decide(db, session, fragments, text)
        assert not result.blocked and result.output_text == text
        assert len(result.attempts) == 1 and not result.final_verdict.reason_codes
        assert len(result.final_proposal.segments) == min(count, 3) * 2 - 1
        for segment, fragment in zip(result.final_proposal.segments[::2], fragments[:3], strict=True):
            expected = extractive_excerpt(fragment["text"])
            assert segment.expected_text == expected.text
            assert segment.value_sha256 == hashlib.sha256(expected.text.encode()).hexdigest()
        events = (
            db.query(models.TraceEvent).filter_by(turn_id=turn.id, event_type="material_excerpt_bound").all()
        )
        if any(extractive_excerpt(f["text"]).text != f["text"] for f in fragments[:3]):
            assert len(events) == 1
            bindings = events[0].payload["bindings"]
            assert len(bindings) == min(count, 3)
            for binding, fragment in zip(bindings, fragments[:3], strict=True):
                excerpt = extractive_excerpt(fragment["text"])
                assert binding["source_sha256"] == hashlib.sha256(fragment["text"].encode()).hexdigest()
                assert (
                    binding["document_version"] == 1 and binding["location_ref"] == fragment["location_ref"]
                )
                assert fragment["text"][binding["start"] : binding["end"]] in excerpt.text
                assert "text" not in binding


@pytest.mark.parametrize(
    "mutation",
    [
        "altered",
        "arbitrary_prefix",
        "fragment_text",
        "document",
        "version",
        "location",
        "foreign_course",
        "foreign_activity",
        "retired",
        "category",
        "scope",
        "provenance",
    ],
)
def test_projection_does_not_grant_authority_to_mutations(tmp_path, mutation):
    overrides = {}
    if mutation == "scope":
        overrides = {
            "allowed_scopes": {
                "topics": ["elsewhere"],
                "purposes": ["material_response"],
                "actions": ["respond"],
            }
        }
    if mutation == "provenance":
        overrides = {
            "allowed_disclosures": [
                {"category": "texto", "provenance": "elsewhere", "recipient": "participant-a"}
            ]
        }
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
        allowed_templates=[["material-fragment-response", 1]],
        policy_overrides=overrides,
    ) as (db, session, _, _):
        fragments = seed_fragments(db, 1, 800)
        text = candidate(fragments)
        row = db.get(models.MaterialFragment, fragments[0]["fragment_id"])
        if mutation == "altered":
            text += " UNAUTHORIZED_SENTINEL"
        elif mutation == "arbitrary_prefix":
            text = text[:150]
        elif mutation == "fragment_text":
            fragments[0]["text"] = text
        elif mutation == "document":
            fragments[0]["document_id"] = "foreign-document"
        elif mutation == "version":
            fragments[0]["document_version"] = 2
        elif mutation == "location":
            fragments[0]["location_ref"] = "p. 999"
        elif mutation == "foreign_course":
            db.add(models.Course(id="other-course", name="Foreign", subject_code="FOREIGN"))
            db.flush()
            row.course_id = "other-course"
        elif mutation == "foreign_activity":
            row.activity_configuration_ids = ["other-activity"]
        elif mutation == "retired":
            db.get(models.MaterialDocument, row.document_id).status = "retired"
        elif mutation == "category":
            row.content_type = "unauthorized"
        db.flush()
        result, turn = decide(db, session, fragments, text)
        assert result.blocked and result.output_text is None and len(result.attempts) <= 2
        assert result.final_proposal is None
        persist_final_output(db, turn, result, generator_agent_id="test-mutant")
        persisted = json.dumps([p.content for p in db.query(models.GeneratedProposal)], ensure_ascii=False)
        assert text not in persisted and "UNAUTHORIZED_SENTINEL" not in persisted
        assert not db.query(models.TraceEvent).filter_by(event_type="material_excerpt_bound").count()


def test_profile_preserves_exact_source_offsets_and_legacy_truncation():
    for raw in ["  café é 🧪  ", "x" * 399, "x" * 400, "x" * 401, "   " + raw_text(800) + "  "]:
        projection = extractive_excerpt(raw)
        stripped = raw.strip()
        expected = stripped if len(stripped) <= 400 else stripped[:400].rsplit(" ", 1)[0] + "…"
        assert projection.text == expected
        assert projection.source_sha256 == hashlib.sha256(raw.encode()).hexdigest()
        assert raw[projection.start : projection.end] == expected.removesuffix("…")
