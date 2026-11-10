"""Transactional context updates cannot cross sessions or survive terminal closure."""

from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import CancellationToken
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.dialogue.contracts import DialogueContext
from oralia.infrastructure.db import models
from tests.unit.test_cognitive_state import seeded_session as _seeded_session

seeded_session = _seeded_session


def test_context_patch_conflict_cancel_and_closed_session(db_session, seeded_session):
    from oralia.application.services.dialogue_context_service import update_context

    session = seeded_session
    get_or_create(db_session, session.id, session.activity_configuration_id)
    token = CancellationToken()
    context = DialogueContext(content_query="consulta ficticia")
    patch = update_context(db_session, session.id, 0, context, token)
    assert patch.applied
    assert not update_context(db_session, session.id, 0, context, token).applied
    token.cancel()
    with pytest.raises(ValueError, match="cancelled"):
        update_context(db_session, session.id, 1, context, token)
    session.status = "closed_voluntary"
    db_session.flush()
    with pytest.raises(ValueError, match="inactive"):
        update_context(db_session, session.id, 1, context, CancellationToken())
    assert db_session.get(models.CognitiveState, session.id).version == 1


def test_unknown_or_foreign_turn_reference_rejected(db_session, seeded_session):
    from oralia.application.services.dialogue_context_service import update_context

    session = seeded_session
    get_or_create(db_session, session.id, session.activity_configuration_id)
    with pytest.raises(ValueError, match="reference"):
        update_context(
            db_session, session.id, 0, DialogueContext(last_approved_turn_id=uuid4()), CancellationToken()
        )
    assert db_session.query(models.StatePatch).count() == 0

    foreign = models.Session(
        activity_configuration_id=session.activity_configuration_id,
        participant_code=session.participant_code,
    )
    db_session.add(foreign)
    db_session.flush()
    turn = models.Turn(session_id=foreign.id, index=0, input_text="sintético", output_text="Texto aprobado.")
    db_session.add(turn)
    db_session.flush()
    proposal = models.GeneratedProposal(turn_id=turn.id, generator_agent_id="synthetic-contract-fixture")
    db_session.add(proposal)
    db_session.flush()
    verdict = models.VerificationResult(
        proposal_id=proposal.id, verifier_agent_id="synthetic-contract-fixture", verdict="approved"
    )
    db_session.add(verdict)
    db_session.flush()
    turn.verification_result_id = verdict.id
    db_session.flush()
    with pytest.raises(ValueError, match="reference"):
        update_context(
            db_session, session.id, 0, DialogueContext(last_approved_turn_id=turn.id), CancellationToken()
        )
    assert db_session.query(models.StatePatch).count() == 0


def test_context_patch_rolls_back_with_outer_turn_transaction(db_session, seeded_session):
    from oralia.application.services.dialogue_context_service import update_context

    session = seeded_session
    get_or_create(db_session, session.id, session.activity_configuration_id)
    db_session.commit()
    session_id = session.id
    update_context(db_session, session_id, 0, DialogueContext(content_query="sintético"), CancellationToken())
    db_session.rollback()
    state = db_session.get(models.CognitiveState, session_id)
    assert state.version == 0 and state.dialogue_context is None
    assert db_session.query(models.StatePatch).count() == 0


def test_reference_requires_actual_t090_result_linked_to_the_same_turn(db_session, seeded_session):
    from oralia.application.orchestration.final_output_gate import decide_final_output, persist_final_output
    from oralia.application.orchestration.output_authorization_context import build_authorization_snapshot
    from oralia.application.orchestration.output_proposal_builder import build_output_proposal
    from oralia.application.services.dialogue_context_service import update_context
    from oralia.domain.policies.output_template_catalog import SC007_ACKNOWLEDGEMENT

    session = seeded_session
    state = get_or_create(db_session, session.id, session.activity_configuration_id)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    turn = models.Turn(session_id=session.id, index=0, input_text="Mensaje sintético")
    db_session.add(turn)
    db_session.flush()
    snapshot = build_authorization_snapshot(session, activity)
    entry = SC007_ACKNOWLEDGEMENT
    proposal = build_output_proposal(
        snapshot, template_id=entry.template_id, template_version=entry.version, template_sha256=entry.sha256
    )
    decision = decide_final_output(snapshot, proposal, allow_operational_attempt=False)
    assert not decision.blocked
    persist_final_output(db_session, turn, decision, generator_agent_id="synthetic-contract-fixture")
    patch = update_context(
        db_session,
        session.id,
        state.version,
        DialogueContext(last_approved_turn_id=turn.id),
        CancellationToken(),
    )
    assert patch.applied
    other = models.Turn(
        session_id=session.id,
        index=1,
        input_text="Otro",
        output_text="Texto sin autorización propia.",
        verification_result_id=turn.verification_result_id,
        generated_proposal_id=turn.generated_proposal_id,
    )
    db_session.add(other)
    db_session.flush()
    with pytest.raises(ValueError, match="reference"):
        update_context(
            db_session,
            session.id,
            patch.resulting_version,
            DialogueContext(last_approved_turn_id=other.id),
            CancellationToken(),
        )


def test_erasure_removes_context_receipts_and_patch_content(db_session, seeded_session):
    from oralia.application.services.dialogue_context_service import update_context
    from oralia.application.services.session_privacy_service import erase_content

    session = seeded_session
    state = get_or_create(db_session, session.id, session.activity_configuration_id)
    update_context(
        db_session, session.id, 0, DialogueContext(content_query="contenido sintético"), CancellationToken()
    )
    db_session.add(
        models.TurnRequestReceipt(
            session_id=session.id, client_request_id=str(uuid4()), payload_sha256="b" * 64
        )
    )
    session.status = "closed_voluntary"
    db_session.flush()
    erase_content(db_session, session, scope=frozenset({"transcript"}))
    db_session.flush()
    assert state.dialogue_context is None
    assert db_session.query(models.TurnRequestReceipt).count() == 0
    assert all("dialogue_context" not in p.payload for p in db_session.query(models.StatePatch))
