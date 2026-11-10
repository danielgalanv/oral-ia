"""Draft authoring order is a DAG; existing API IDs are bound after creation."""

import json
from pathlib import Path
from uuid import uuid4

import pytest

from oralia.course_dialogue.authoring import draft_graph, next_draft_input


def packet():
    return json.loads(
        Path("materiales/docente/feature012-course-drafts/curriculum.json").read_text(encoding="utf8")
    )


def test_all_drafts_can_use_existing_single_unit_api_without_publishing():
    p = packet()
    graph = draft_graph(p)
    ids = {}
    seen = []
    bindings = {
        ref["source_id"]: {"document_id": str(uuid4()), "document_version": 1, "fragment_id": str(uuid4())}
        for unit in p["units"]
        for ref in unit["source_refs"]
    }
    course = str(uuid4())
    activity = str(uuid4())
    while len(ids) < len(graph):
        key, data = next_draft_input(graph, ids, course, activity, bindings)
        assert data.activity_refs == (data.activity_refs[0],)
        assert all(str(ref) in ids.values() for refs in data.relations.values() for ref in refs)
        assert "reviewed" not in data.model_dump() and "status" not in data.model_dump()
        ids[key] = str(uuid4())
        seen.append(data)
    assert len(seen) == 83
    assert len({d.subgoal_ref for d in seen}) == 7
    assert sum(d.kind == "question" and len(d.relations.get("hints", [])) == 3 for d in seen) == 7
    assert next_draft_input(graph, ids, course, activity, bindings) is None


def test_missing_source_binding_fails_before_any_api_write():
    with pytest.raises(ValueError, match="source binding"):
        next_draft_input(draft_graph(packet()), {}, str(uuid4()), str(uuid4()), {})


def test_packet_cannot_claim_review_or_publication():
    p = packet()
    p["participant_publication"] = True
    with pytest.raises(ValueError, match="pending"):
        draft_graph(p)
