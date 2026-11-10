import json

import pytest

from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    OutputAuthorizationPolicy,
    TemplateReference,
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)
from oralia.domain.policies.output_template_catalog import SAFE_TECHNICAL_FALLBACK
from oralia.infrastructure.db import models
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    SentenceTransformerEmbeddingAdapter,
)
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


async def test_single_authorized_operational_fallback_replaces_blocked_candidate(db_session):
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    raw = json.loads(activity.output_authorization_policy_json)
    raw["allowed_operational_messages"] = [["safe-technical-fallback", 1]]
    raw["allowed_scopes"]["purposes"].append("technical_recovery")
    activity.output_authorization_policy_json = canonical_policy_json(
        OutputAuthorizationPolicy.model_validate(raw)
    )
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(
        activity.output_authorization_policy_json
    )
    result = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        followup_agent=_CandidateAgent("nota: 8"),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.output_text == SAFE_TECHNICAL_FALLBACK.text
    assert result.blocked and session.status == "active"
    attempts = db_session.query(models.TraceEvent).filter_by(event_type="output_authorization_attempt").all()
    assert [(row.payload["attempt"], row.payload["verdict"]) for row in attempts] == [
        (0, "block"),
        (1, "approved"),
    ]
    assert "nota: 8" not in str([row.payload for row in db_session.query(models.TraceEvent)])


class _CandidateAgent:
    contract = type("Contract", (), {"timeout_ms": 1000})()

    def __init__(self, text: str, status: str = "ok") -> None:
        self.text = text
        self.status = status

    async def execute(self, request, cancellation):
        del request, cancellation
        return AgentResult(
            status=self.status,
            output=(
                {
                    "question_text": self.text,
                    "followup_type": "profundizacion",
                    "referenced_concept": "arquitectura",
                    "generation_trace": {},
                }
                if self.status == "ok"
                else None
            ),
        )


def _permit_template(activity, template_id: str, purpose: str, action: str) -> None:
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json,
        activity.output_authorization_policy_sha256,
    )
    policy = policy.model_copy(
        update={
            "allowed_templates": (*policy.allowed_templates, TemplateReference(template_id, 1)),
            "allowed_scopes": AllowedScope(
                topics=policy.allowed_scopes.topics,
                purposes=(
                    policy.allowed_scopes.purposes
                    if purpose in policy.allowed_scopes.purposes
                    else (*policy.allowed_scopes.purposes, purpose)
                ),
                actions=(
                    policy.allowed_scopes.actions
                    if action in policy.allowed_scopes.actions
                    else (*policy.allowed_scopes.actions, action)
                ),
            ),
        }
    )
    raw = canonical_policy_json(policy)
    activity.output_authorization_policy_json = raw
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(raw)


@pytest.mark.parametrize(
    ("answer", "generated", "action", "template_id"),
    (
        ("   ", None, "clarify", "defense-clarification"),
        (
            "La arquitectura separa generación y verificación.",
            "¿Cómo separa la arquitectura generación y verificación?",
            "ask",
            "defense-dynamic-output",
        ),
    ),
)
async def test_all_visible_defense_branches_cross_the_final_gate(
    db_session, answer, generated, action, template_id
) -> None:
    session = _seed_defense(db_session)
    if not answer.strip():
        session.turn_count = 1
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    result = await run_defense_turn(
        db_session,
        session,
        answer,
        followup_agent=_CandidateAgent(generated) if generated else None,
    )
    assert result.blocked is False
    assert result.dialogue_action == action
    turn = db_session.get(models.Turn, result.turn_id)
    verification = db_session.get(models.VerificationResult, turn.verification_result_id)
    assert verification.verdict == "approved"
    assert verification.authorization_context["attempt"] == 0
    assert verification.authorization_context["template_id"] == template_id


async def test_missing_policy_and_second_block_close_without_visible_text(db_session) -> None:
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    activity.output_authorization_policy_json = None
    activity.output_authorization_policy_sha256 = None
    result = await run_defense_turn(
        db_session, session, "respuesta", followup_agent=_CandidateAgent("¿Por qué?")
    )
    assert result.blocked is True
    assert result.output_text is None
    assert result.dialogue_action == "finish"
    assert session.status == "closed_error_safe"
    turn = db_session.get(models.Turn, result.turn_id)
    proposal = db_session.get(models.GeneratedProposal, turn.generated_proposal_id)
    assert "text" not in proposal.content
    attempts = [
        event.payload
        for event in db_session.query(models.TraceEvent).filter_by(turn_id=turn.id)
        if event.event_type == "output_authorization_attempt"
    ]
    assert [item["attempt"] for item in attempts] == [0, 1]


async def test_initial_bank_question_and_limit_close_use_exact_catalog_entries(db_session) -> None:
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    initial_session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, initial_session.activity_configuration_id)
    _permit_template(activity, "defense-initial-question", "oral_defense", "ask")
    initial = await run_defense_turn(db_session, initial_session, "")
    assert initial.output_text == "Explica la decisión."
    turn = db_session.get(models.Turn, initial.turn_id)
    verification = db_session.get(models.VerificationResult, turn.verification_result_id)
    assert verification.authorization_context["template_id"] == "defense-initial-question"

    activity.max_turns = initial_session.turn_count
    _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
    limited = await run_defense_turn(db_session, initial_session, "otra respuesta")
    assert limited.dialogue_action == "finish"
    assert initial_session.status == "closed_limit_reached"


async def test_missing_evidence_and_generation_failure_never_invent_a_question(
    db_session,
) -> None:
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    session = _seed_defense(db_session)
    session.turn_count = 1
    db_session.query(models.MaterialFragment).delete()
    missing = await run_defense_turn(db_session, session, "respuesta concreta")
    assert missing.dialogue_action == "acknowledge_missing_info"
    missing_turn = db_session.get(models.Turn, missing.turn_id)
    missing_verification = db_session.get(models.VerificationResult, missing_turn.verification_result_id)
    assert missing_verification.authorization_context["template_id"] == ("defense-missing-information")

    # Restore one usable fragment so this branch reaches generation itself.
    document = db_session.query(models.MaterialDocument).one()
    restored_fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=1,
        text="Contenido autorizado.",
        location_ref="p2",
        sequence_index=1,
        embedding_ref="c" * 64,
        course_id=document.course_id,
        activity_configuration_ids=[session.activity_configuration_id],
    )
    db_session.add(restored_fragment)
    db_session.flush()
    ChromaVectorStore().add(
        restored_fragment.id,
        SentenceTransformerEmbeddingAdapter().embed([restored_fragment.text])[0],
        {"course_id": document.course_id},
    )
    failed = await run_defense_turn(
        db_session,
        session,
        "otra respuesta",
        followup_agent=_CandidateAgent("unused", status="error"),
    )
    assert failed.output_text is not None
    assert failed.dialogue_action == "acknowledge_missing_info"


@pytest.mark.parametrize(
    "forbidden",
    [
        "Tu nota es 9.",
        "Has aprobado.",
        "Tu nivel es alto.",
        "Tu rendimiento es excelente.",
        "Tu capacidad es baja.",
        "Tu comprensión es insuficiente.",
        "Eres competente en arquitectura.",
    ],
)
async def test_rejected_generated_text_is_absent_from_persisted_output_chain(db_session, forbidden) -> None:
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    session = _seed_defense(db_session)
    result = await run_defense_turn(
        db_session,
        session,
        "La arquitectura separa generación y verificación.",
        followup_agent=_CandidateAgent(forbidden),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.output_text is None
    persisted = [
        *(row.content for row in db_session.query(models.GeneratedProposal).all()),
        *(row.authorization_context for row in db_session.query(models.VerificationResult).all()),
        *(row.payload for row in db_session.query(models.TraceEvent).all()),
    ]
    assert forbidden not in str(persisted)


async def test_outer_rollback_removes_whole_turn_and_retry_is_clean(db_session) -> None:
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn

    session = _seed_defense(db_session)
    session_id = session.id
    db_session.commit()
    await run_defense_turn(
        db_session,
        session,
        "respuesta",
        followup_agent=_CandidateAgent("¿Por qué separaste las capas?"),
    )
    db_session.rollback()
    assert db_session.query(models.Turn).filter_by(session_id=session_id).count() == 0
    session = db_session.get(models.Session, session_id)
    assert session.status == "active" and session.turn_count == 0
    retried = await run_defense_turn(
        db_session,
        session,
        "respuesta",
        followup_agent=_CandidateAgent("¿Qué responsabilidad conserva cada capa?"),
    )
    assert retried.blocked is False
