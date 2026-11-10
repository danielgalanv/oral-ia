from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    SentenceTransformerEmbeddingAdapter,
)
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore


def _seed_defense(db_session):
    course = models.Course(name="Defensa", subject_code="DEF")
    retention = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, retention])
    db_session.flush()
    policy = OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": "defense-policy",
            "policy_version": 1,
            "allowed_recipients": ["participant-a"],
            "allowed_disclosures": [
                {
                    "category": "generated_defense",
                    "provenance": "defense-agency",
                    "recipient": "participant-a",
                }
            ],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["oral_defense", "missing_information", "clarify_response"],
                "actions": ["ask", "acknowledge_missing_info", "clarify"],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [
                ["defense-dynamic-output", 1],
                ["defense-missing-information", 1],
                ["defense-clarification", 1],
            ],
            "allowed_operational_messages": [],
        }
    )
    raw = canonical_policy_json(policy)
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Defensa",
        subject="Arquitectura",
        objective="justificar decisiones",
        mode="oral_defense",
        language="es",
        max_turns=5,
        max_duration_seconds=900,
        retention_policy_id=retention.id,
        output_authorization_policy_json=raw,
        output_authorization_policy_sha256=canonical_policy_sha256(raw),
    )
    participant = models.ParticipantCode(code="participant-a")
    db_session.add_all([activity, participant])
    db_session.flush()
    config = models.DefenseActivityConfig(
        activity_configuration_id=activity.id,
        initial_questions=["Explica la decisión."],
        topics=["activity"],
    )
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="active",
        turn_count=0,
    )
    document = models.MaterialDocument(
        course_id=course.id,
        activity_configuration_ids=[activity.id],
        filename="material.txt",
        content_hash="a" * 64,
        mime_type="text/plain",
        size_bytes=20,
        status="active",
    )
    db_session.add_all([config, session, document])
    db_session.flush()
    fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=1,
        text="La arquitectura separa generación y verificación.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref="b" * 64,
        course_id=course.id,
        activity_configuration_ids=[activity.id],
    )
    db_session.add(fragment)
    db_session.flush()
    ChromaVectorStore().add(
        fragment.id,
        SentenceTransformerEmbeddingAdapter().embed([fragment.text])[0],
        {"course_id": course.id},
    )
    return session


class _GradeAgent:
    contract = type("Contract", (), {"timeout_ms": 1000})()

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "question_text": "Tu nota es 9.",
                "followup_type": "profundizacion",
                "referenced_concept": "arquitectura",
                "generation_trace": {"adapter": "deterministic", "fallback_used": False},
            },
        )


class _ApprovedGrounding:
    contract = type("Contract", (), {"agent_id": "grounding-verifier", "timeout_ms": 1000})()

    async def execute(self, request, cancellation):
        del request, cancellation
        return AgentResult(
            status="ok",
            output={
                "verdict": "fundamentada",
                "supported_claims": [],
                "unsupported_claims": [],
            },
        )


async def test_text_turn_persists_sanitized_t090_chain(db_session) -> None:
    session = _seed_defense(db_session)
    result = await run_defense_turn(
        db_session,
        session,
        "La arquitectura separa generación y verificación.",
    )
    assert result.blocked is False
    assert result.dialogue_action == "ask"
    assert result.output_text
    turn = db_session.get(models.Turn, result.turn_id)
    verification = db_session.get(models.VerificationResult, turn.verification_result_id)
    proposal = db_session.get(models.GeneratedProposal, turn.generated_proposal_id)
    assert verification.verdict == "approved"
    assert verification.authorization_context["attempt"] == 0
    assert proposal.content["text"] == result.output_text


async def test_evaluative_candidate_closes_without_publishing(db_session) -> None:
    session = _seed_defense(db_session)
    result = await run_defense_turn(
        db_session,
        session,
        "La arquitectura separa generación y verificación.",
        followup_agent=_GradeAgent(),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.blocked is True
    assert result.output_text is None
    assert result.dialogue_action == "finish"
    turn = db_session.get(models.Turn, result.turn_id)
    proposal = db_session.get(models.GeneratedProposal, turn.generated_proposal_id)
    assert "Tu nota es 9." not in str(proposal.content)
    assert session.status == "closed_error_safe"
