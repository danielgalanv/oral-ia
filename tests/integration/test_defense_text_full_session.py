import json

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.infrastructure.db import models
from tests.contract.test_defense_output_authorization_matrix import _CandidateAgent, _permit_template
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


@pytest.mark.parametrize("switch", [False, True])
@pytest.mark.parametrize("close_kind", ["voluntary", "turns", "duration"])
async def test_complete_text_defense_has_unique_grounded_followups_and_authorized_summary(
    db_session, switch, close_kind
):
    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    db_session.get(models.RetentionPolicy, activity.retention_policy_id).retention_days = 1
    activity.max_turns = 10
    _permit_template(activity, "defense-initial-question", "oral_defense", "ask")
    _permit_template(activity, "defense-summary", "oral_defense_summary", "respond")
    _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
    policy = json.loads(activity.output_authorization_policy_json)
    policy["allowed_disclosures"].append(
        {
            "category": "defense_summary",
            "provenance": "persisted_session_facts",
            "recipient": session.participant_code,
        }
    )
    activity.output_authorization_policy_json = canonical_policy_json(
        OutputAuthorizationPolicy.model_validate(policy)
    )
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(
        activity.output_authorization_policy_json
    )
    config = db_session.query(models.DefenseActivityConfig).one()
    config.summary_authorized = True
    config.transcript_retention_authorized = True
    initial = await run_defense_turn(db_session, session, "")
    assert initial.output_text == config.initial_questions[0]
    questions = [
        "¿Cómo separa arquitectura generación y verificación?",
        "¿Qué decisión modular permite aislar responsabilidades?",
        "¿Qué ejemplo muestra los límites del diseño?",
    ]
    for index, question in enumerate(questions):
        result = await run_defense_turn(
            db_session,
            session,
            "La arquitectura separa generación y verificación.",
            followup_agent=_CandidateAgent(question),
            grounding_verifier_agent=_ApprovedGrounding(),
            requested_topic="activity" if switch and index == 1 else None,
        )
        assert result.dialogue_action == "ask"
        assert result.output_text == question
    trace = (
        db_session.query(models.TraceEvent)
        .filter_by(session_id=session.id, event_type="followup_question_generated")
        .all()
    )
    for event in trace[1:]:
        assert event.payload["referenced_concept"] == "arquitectura"
        assert event.payload["evidence_fragment_ids"]
    if close_kind == "voluntary":
        summary = end_defense_session(db_session, session, config, retain=True, scope=["summary"])
    else:
        if close_kind == "turns":
            activity.max_turns = session.turn_count + 1
        else:
            from datetime import timedelta

            from oralia.infrastructure.db.timeutil import utcnow

            session.started_at = utcnow() - timedelta(seconds=activity.max_duration_seconds + 1)
        closed = await run_defense_turn(db_session, session, "arquitectura")
        summary = closed.defense_summary
        assert closed.dialogue_action == "finish"
    assert summary["questions_asked"] == [initial.output_text, *questions]
    assert summary["duration_seconds"] >= 0
    assert summary["sources_consulted_fragment_ids"]
    assert "arquitectura" in summary["concepts_mentioned"]
    assert session.status == ("closed_voluntary" if close_kind == "voluntary" else "closed_limit_reached")
    assert end_defense_session(db_session, session, config) is None
    if close_kind != "voluntary":
        # Automatic closure has no explicit retention choice, so facts and their
        # text-bearing authorization rows are delivered once and immediately removed.
        summary_proposals = (
            db_session.query(models.GeneratedProposal).filter_by(generator_agent_id="defense-summary").all()
        )
        assert summary_proposals and all("text" not in row.content for row in summary_proposals)
        return
    proposal = (
        db_session.query(models.GeneratedProposal).filter_by(generator_agent_id="defense-summary").one()
    )
    verdict = db_session.query(models.VerificationResult).filter_by(proposal_id=proposal.id).one()
    assert verdict.verdict == "approved"
    assert verdict.authorization_context["template_id"] == "defense-summary"
    assert json.loads(proposal.content["text"]) == summary
