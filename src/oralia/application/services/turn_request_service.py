"""Transaction-local request identity; receipts never duplicate session content."""

import hashlib
import json

from sqlalchemy import update

from oralia.application.orchestration.final_output_gate import decide_final_output
from oralia.application.services.reviewed_unit_renderer import render_plan
from oralia.domain.dialogue.catalog import GUIDED_CATALOG
from oralia.domain.dialogue.contracts import ProposalPlan
from oralia.infrastructure.db import models


def begin_request(db, session, request_id, payload):
    """Serialize on the session before checking identity, in the caller's transaction.

    Cancellation/exception rolls back both receipt and turn through get_db. There
    is no separately committed pending row or second writer that can win closure.
    """
    if request_id is None:
        return None, None
    db.execute(
        update(models.Session).where(models.Session.id == session.id).values(status=models.Session.status)
    )
    db.refresh(session)
    if session.status != "active":
        from oralia.application.services.session_privacy_service import valid_retained_scope

        if "transcript" not in valid_retained_scope(db, session):
            raise ValueError("La sesión está cerrada; no hay un recibo vigente para volver a proyectar.")
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    existing = (
        db.query(models.TurnRequestReceipt)
        .filter_by(session_id=session.id, client_request_id=str(request_id))
        .one_or_none()
    )
    if existing is not None:
        if existing.payload_sha256 != digest:
            raise ValueError("Este identificador de envío ya corresponde a otro contenido.")
        return existing, replay_turn(db, session, existing)
    if session.status != "active":
        raise ValueError("La sesión está cerrada; el envío no se ha repetido.")
    receipt = models.TurnRequestReceipt(
        session_id=session.id, client_request_id=str(request_id), payload_sha256=digest, status="pending"
    )
    db.add(receipt)
    db.flush()
    return receipt, None


def complete_request(db, receipt, turn_id):
    if receipt is None:
        return
    # Ephemeral/summary closure may have erased the receipt during this turn.
    # Never recreate it after privacy enforcement.
    db.execute(
        update(models.TurnRequestReceipt)
        .where(models.TurnRequestReceipt.id == receipt.id)
        .values(turn_id=turn_id, status="completed")
    )


def receipt_view(receipt):
    return {
        "client_request_id": receipt.client_request_id,
        "status": receipt.status,
        "turn_id": receipt.turn_id,
    }


def replay_turn(db, session, receipt):
    """Project the same turn; revalidate current reviewed content before disclosure.

    No cached response, sources or summary is stored in the receipt. Legacy output
    has no reconstructible reviewed plan and is conservatively withheld on replay.
    The caller can reconcile identity even when content has expired or been retired.
    """
    turn = db.get(models.Turn, receipt.turn_id) if receipt.turn_id else None
    if turn is None or turn.session_id != session.id:
        raise ValueError("El envío aún no tiene un resultado confirmado; consulta su recibo.")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    action = db.get(models.DialogueAction, turn.dialogue_action_id)
    state = db.get(models.CognitiveState, session.id)
    event = (
        db.query(models.TraceEvent)
        .filter_by(turn_id=turn.id, event_type="guided_dialogue_decision")
        .one_or_none()
    )
    output = None
    if session.status == "active" and turn.output_text is not None and event is not None:
        content = event.payload
        refs = content.get("unit_ids", [])
        if refs:
            proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
            try:
                plan = ProposalPlan(
                    template_id=proposal.content["template_id"],
                    template_version=str(proposal.content["template_version"]),
                    template_sha256=proposal.content["template_sha256"],
                    action="repeat",
                    unit_refs=tuple(refs),
                    transformation="select_reviewed_unit" if len(refs) == 1 else "compose_reviewed_units",
                )
                snapshot, rendered = render_plan(db, session, plan)
                decision = decide_final_output(
                    snapshot, rendered, catalog=GUIDED_CATALOG, allow_operational_attempt=False
                )
                if decision.output_text == turn.output_text:
                    output = decision.output_text
            except (ValueError, KeyError):
                pass  # Revoked/expired/unsupported content stays withheld, never regenerated.
    result = {
        "turn_id": turn.id,
        "output_text": output,
        "state_version": state.version if state else None,
        "mode": state.mode if state else activity.mode,
        "dialogue_action": action.action_type if action else "clarify",
        "dialogue_purpose": None,
        "sources": [],
        "general_knowledge_used": False,
        "blocked": turn.status == "blocked",
        "speech": None,
        "defense_summary": None,
        "session_closed": session.status != "active",
        "session_status": session.status,
        "request_replayed": True,
        "replay_content_withheld": output is None,
    }
    from oralia.application.services.screenless_navigation_service import screenless_enabled

    if screenless_enabled(activity, session.participant_code):
        from oralia.application.services.session_privacy_service import privacy_view

        view = privacy_view(db, session)
        result["dialogue_status"] = {
            "screenless_text_ready": True,
            "effective_profile": (
                (state.dialogue_context or {}).get("effective_profile", "degraded") if state else "degraded"
            ),
            "provider": (
                (event.payload or {}).get("provider", "fixed-dialogue-template/v1")
                if event
                else "fixed-dialogue-template/v1"
            ),
            "conservation": {"retain": view["retain"], "scope": view["scope"]},
        }
    return result
