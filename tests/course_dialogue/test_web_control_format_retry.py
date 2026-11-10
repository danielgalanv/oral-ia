"""Bounded syntax recovery only: CPU doubles are not semantic validation."""

import asyncio
import json
from types import SimpleNamespace

import pytest

from oralia.documentary.study_errors import StudyFailure
from oralia.documentary.study_web_flow import StudyWebFlow
from tests.course_dialogue.test_web_review_rounds import Provider
from tests.unit.test_reviewed_study_chat import Owner

VALID = json.dumps({"status": "sufficient", "reason": "Explicit CPU fixture, not an academic judgement"})
BROKEN = VALID + '"'


def setup(*outputs):
    owner = Owner(None, Provider(*outputs))
    web = SimpleNamespace(
        policy=SimpleNamespace(activity="fixture", mode="self_study", concepts=["software requirements"]),
        check_policy=lambda: None,
    )
    flow = StudyWebFlow(owner, web, None, "fixture", lambda: None, None)
    base = SimpleNamespace(purpose="explicacion", student_input="Pregunta de prueba", conversation_history=[])
    return flow, owner, base, web


def test_complete_but_malformed_control_has_one_real_format_retry():
    flow, owner, base, _ = setup(BROKEN, VALID)
    verdict = asyncio.run(flow.judge("gap", base, []))
    assert verdict.status == "sufficient"
    assert len(owner.critic_adapter.requests) == 2
    first, second = owner.critic_adapter.requests
    assert not first.format_reminder and second.format_reminder
    assert first.question == second.question and first.evidence == second.evidence
    assert len(flow.trace["format_retries"]) == 1


def test_second_malformed_control_is_not_retried_again():
    flow, owner, base, _ = setup(BROKEN, BROKEN, VALID)
    with pytest.raises(StudyFailure):
        asyncio.run(flow.judge("gap", base, []))
    assert len(owner.critic_adapter.requests) == 2


@pytest.mark.parametrize(
    "text",
    [
        json.dumps({"status": "made_up", "reason": "schema mismatch"}),
        json.dumps({"status": "supported", "reason": "wrong control task"}),
    ],
)
def test_schema_or_semantic_task_mismatch_is_not_format_repaired(text):
    flow, owner, base, _ = setup(text, VALID)
    with pytest.raises(StudyFailure):
        asyncio.run(flow.judge("gap", base, []))
    assert len(owner.critic_adapter.requests) == 1


def test_unknown_is_preserved_without_a_retry_to_seek_acceptance():
    flow, owner, base, _ = setup(json.dumps({"status": "unknown", "reason": "No sufficient evidence"}), VALID)
    assert asyncio.run(flow.judge("gap", base, [])).status == "unknown"
    assert len(owner.critic_adapter.requests) == 1


def test_revocation_after_first_result_prevents_retry():
    flow, owner, base, web = setup(BROKEN, VALID)
    original = owner.critic_adapter.generate

    async def revoke(request):
        result = await original(request)

        def revoked():
            raise ValueError("withdrawn")

        web.check_policy = revoked
        return result

    owner.critic_adapter.generate = revoke
    with pytest.raises(StudyFailure):
        asyncio.run(flow.judge("gap", base, []))
    assert len(owner.critic_adapter.requests) == 1


def test_empty_local_evidence_cannot_be_declared_sufficient_by_model():
    flow, owner, base, _ = setup(VALID)
    base.evidence = []
    with pytest.raises(StudyFailure):
        asyncio.run(flow.extend(base, {}))
    assert flow.trace["status"] == "empty_local_sufficient_rejected"
    assert len(owner.critic_adapter.requests) == 1
