"""Closed navigation planning and DB-bound metadata, never free teacher generation."""

import re
from dataclasses import dataclass, field, replace

from oralia.application.orchestration.output_authorization_context import (
    AuthorizationReferenceInput,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import BoundTemplateSlot, build_output_proposal
from oralia.application.services.dialogue_retrieval_service import authorized_unit
from oralia.application.services.session_privacy_service import privacy_view, validate_privacy_choice
from oralia.domain.dialogue.contracts import DialogueAct
from oralia.domain.dialogue.interpretation import normalized
from oralia.domain.dialogue.semantic_templates import SEMANTIC_POLICY_ID
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.domain.policies.output_template_catalog import (
    CONTINUITY_NAVIGATION_TEMPLATES,
    NAVIGATION_TEMPLATES,
    PACKAGE_NAVIGATION_TEMPLATES,
    PEDAGOGIC_NAVIGATION_TEMPLATES,
)
from oralia.infrastructure.db import models

CHOICES = {
    "none": ("nada", "no conservar nada", []),
    "summary": ("solo el resumen", "conservar solo resumen", ["summary"]),
    "transcript": ("solo la transcripción", "conservar solo transcripción", ["transcript"]),
    "both": ("el resumen y la transcripción", "conservar resumen y transcripción", ["summary", "transcript"]),
}
MODE_NAMES = {
    "doubt_resolution": "resolver una duda",
    "guided_explanation": "explicación guiada",
    "practice_questions": "preguntas de práctica",
    "presentation_preparation": "preparar una exposición",
    "concept_review": "repasar conceptos",
}


@dataclass
class NavigationPlan:
    notice: str | None = None
    updates: dict = field(default_factory=dict)
    privacy_choice: str | None = None
    act: DialogueAct | None = None


def screenless_enabled(activity, recipient=None):
    if (
        activity is None
        or not activity.output_authorization_policy_json
        or not activity.output_authorization_policy_sha256
    ):
        return False
    try:
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        )
    except ValueError:
        return False
    required = {(e.template_id, e.version) for e in NAVIGATION_TEMPLATES.values()}
    if not required <= {(e.template_id, e.version) for e in policy.allowed_templates}:
        return False
    recipients = [recipient] if recipient else policy.allowed_recipients
    return all(
        any(
            r.category == category and r.provenance == provenance and r.recipient == who
            for r in policy.allowed_disclosures
        )
        for who in recipients
        for category, provenance in [
            ("session_navigation", "current_session_configuration"),
            ("retained_session_record", "consented_owner_record"),
        ]
    )


def pedagogy_enabled(activity, recipient=None):
    if not screenless_enabled(activity, recipient):
        return False
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    return policy.policy_id in {
        "guided-screenless/v2",
        "guided-screenless/v3",
        "guided-screenless/v4",
        SEMANTIC_POLICY_ID,
    } and {(e.template_id, e.version) for e in PEDAGOGIC_NAVIGATION_TEMPLATES.values()} <= {
        (e.template_id, e.version) for e in policy.allowed_templates
    }


def advanced_pedagogy_enabled(activity, recipient=None):
    if not pedagogy_enabled(activity, recipient):
        return False
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    return policy.policy_id in {"guided-screenless/v3", "guided-screenless/v4", SEMANTIC_POLICY_ID} and {
        (e.template_id, e.version) for e in PACKAGE_NAVIGATION_TEMPLATES.values()
    } <= {(e.template_id, e.version) for e in policy.allowed_templates}


def choice_for_scope(scope):
    return next(key for key, (_, _, scopes) in CHOICES.items() if set(scopes) == set(scope))


def continuity_enabled(activity, recipient=None):
    if not advanced_pedagogy_enabled(activity, recipient):
        return False
    from oralia.domain.policies.output_template_catalog import GREETED_REVIEWED_RESPONSE

    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    needed = {(GREETED_REVIEWED_RESPONSE.template_id, GREETED_REVIEWED_RESPONSE.version)} | {
        (e.template_id, e.version) for e in CONTINUITY_NAVIGATION_TEMPLATES.values()
    }
    return policy.policy_id in {"guided-screenless/v4", SEMANTIC_POLICY_ID} and needed <= {
        (entry.template_id, entry.version) for entry in policy.allowed_templates
    }


def navigation_plan(db, session, text, context, units):
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    if continuity_enabled(activity, session.participant_code):
        from oralia.application.services.continuity_navigation import plan_pending_operation

        natural = plan_pending_operation(db, session, text, context)
        if natural is not None:
            if natural.notice or natural.act or natural.privacy_choice:
                return natural
            # Cancelling a pending operation must not swallow the new request.
            next_context = context.model_copy(update=natural.updates)
            canonical = _canonical_navigation_plan(db, session, text, next_context, units)
            return replace(canonical, updates={**natural.updates, **canonical.updates})
    return _canonical_navigation_plan(db, session, text, context, units)


def _canonical_navigation_plan(db, session, text, context, units):
    value = normalized(text).strip(" ¡!¿?.,")
    topics = {u.topic_ref for u in units}
    if value in {"que temas hay", "que temas existen", "repite opciones", "repetir opciones"}:
        return NavigationPlan("orientation")
    if value in {"mas opciones", "otros temas"}:
        pages = max(1, (len(topics) + 2) // 3)
        return NavigationPlan("orientation", {"navigation_page": (context.navigation_page + 1) % pages})
    if value.startswith("elijo "):
        matches = [t for t in {u.topic_ref for u in units} if normalized(t) == value[6:]]
        if len(matches) != 1:
            return NavigationPlan("unknown_topic", {"pending_topic_ref": None})
        return NavigationPlan(
            updates={"close_confirmation_pending": False, "pending_conservation": None},
            act=DialogueAct(
                primary_act="topic_switch", requested_topic=matches[0], reason_code="explicit_control"
            ),
        )
    if value in {"cancelar cambio", "cancelar conservacion", "continuar sesion"}:
        return NavigationPlan(
            "cancelled",
            {"pending_topic_ref": None, "pending_conservation": None, "close_confirmation_pending": False},
        )
    for mode, label in MODE_NAMES.items():
        if value == normalized("quiero " + label):
            return NavigationPlan(
                act=DialogueAct(primary_act="mode_switch", requested_mode=mode, reason_code="mode_request")
            )
    if value in {"que modos hay", "como puedo estudiar"}:
        return NavigationPlan("modes")
    if value in {"que puedo decir", "repite las instrucciones"}:
        return NavigationPlan("controls")
    if value == "mas sobre la fuente":
        return NavigationPlan("sources_more")
    if value in {"de donde sale eso", "que fuente usaste", "lee la fuente", "repite la fuente"}:
        return NavigationPlan("sources")
    if value in {"que conservaras", "estado de conservacion"}:
        return NavigationPlan("privacy", {"close_confirmation_pending": False})
    for key, (_, phrase, scopes) in CHOICES.items():
        if value == normalized(phrase):
            try:
                validate_privacy_choice(db, session, retain=bool(scopes), scope=scopes)
            except ValueError:
                return NavigationPlan("privacy_forbidden")
            return NavigationPlan(
                "privacy_pending",
                {"pending_conservation": key, "close_confirmation_pending": False, "pending_topic_ref": None},
            )
        if value == normalized("confirmo " + phrase):
            if context.pending_conservation != key:
                return NavigationPlan("privacy_pending" if context.pending_conservation else "privacy")
            try:
                validate_privacy_choice(db, session, retain=bool(scopes), scope=scopes)
            except ValueError:
                return NavigationPlan("privacy_forbidden", {"pending_conservation": None})
            return NavigationPlan("privacy_confirmed", {"pending_conservation": None}, privacy_choice=key)
    if value in {"si", "confirmo conservacion"} and context.pending_conservation:
        return NavigationPlan("privacy_pending")
    if value in {"terminar la sesion", "terminar", "finalizar la sesion", "cerrar sesion"}:
        if context.pending_conservation:
            return NavigationPlan("privacy_pending")
        return NavigationPlan(
            "close_confirm", {"close_confirmation_pending": True, "pending_topic_ref": None}
        )
    if value == "confirmo cerrar":
        if not context.close_confirmation_pending or context.pending_conservation:
            return NavigationPlan(
                "close_confirm", {"close_confirmation_pending": True, "pending_topic_ref": None}
            )
        return NavigationPlan(
            "finish",
            {"close_confirmation_pending": False},
            act=DialogueAct(primary_act="finish", reason_code="explicit_control"),
        )
    if value.startswith("confirmo: "):
        matches = [t for t in {u.topic_ref for u in units} if normalized(t) == value[10:]]
        if len(matches) == 1:
            # Preserve the existing explicit named confirmation. It is not a bare
            # yes and never confirms conservation or a session closure.
            return NavigationPlan(
                updates={"pending_conservation": None, "close_confirmation_pending": False},
                act=DialogueAct(
                    primary_act="content_question", requested_topic=matches[0], reason_code="explicit_control"
                ),
            )
        return NavigationPlan("unknown_topic", {"pending_topic_ref": None})
    if value.startswith("confirmo") and value != "confirmo":
        return NavigationPlan("confirm_topic" if context.pending_topic_ref else "clarify")
    if value == "confirmo" and not context.pending_topic_ref:
        return NavigationPlan("privacy_pending" if context.pending_conservation else "clarify")
    return NavigationPlan()


def render_navigation(
    db, session, activity, name, context, units, *, topic=None, chosen=None, review_index=None
):
    """Bind only DB-revalidated metadata or closed enums to manually authored templates.

    There is deliberately no candidate-text, message or supplied-slot-values argument.
    T090 independently checks the resulting template, each reference and its policy.
    """
    if not screenless_enabled(activity, session.participant_code):
        raise ValueError("Esta actividad no autoriza navegación conversacional sin pantalla.")
    from oralia.application.services.dialogue_output_catalog import activity_output_catalog

    catalog = activity_output_catalog(activity)
    scope = ScopeReference(topic_ref="activity", purpose_ref="guided_control", action_ref="respond")
    protected = activity.mode == "oral_defense"
    state = db.get(models.CognitiveState, session.id)
    study = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity.id)
        .one_or_none()
    )
    protected = protected or bool(
        state and state.mode == "practice_questions" and study and not study.practice_reveals_solution
    )
    live = []
    for unit in units:
        try:
            live.append(authorized_unit(db, session, unit.id, scope, allow_solution=not protected))
        except ValueError:
            continue
    topics = sorted({u.topic_ref for u in live})
    values = {}
    if name in {
        "orientation",
        "clarify",
        "unknown_topic",
        "didactic_greeting",
        "didactic_overview",
        "package_welcome",
        "outside_source",
    }:
        from oralia.application.services.guided_dialogue_service import pending_question_view

        if name == "clarify" and pending_question_view(db, session, context) is not None:
            name = "clarify_question"
        elif not topics:
            name = "empty"
        else:
            pages = (len(topics) + 2) // 3
            offset = (context.navigation_page % pages) * 3
            values["options"] = ", ".join(topics[offset : offset + 3])
    if name == "package_topic_confirmed":
        if context.current_topic_ref not in topics:
            raise ValueError("Confirmed topic no longer authorized")
        values["topic"] = context.current_topic_ref
    if name == "package_welcome":
        if context.current_topic_ref in topics:
            values["topic"] = context.current_topic_ref
        else:
            name = "didactic_greeting"
    if name == "confirm_topic":
        proposed = topic or context.pending_topic_ref
        if proposed not in topics:
            name = "empty"
        else:
            values["topic"] = proposed
    if name == "modes":
        if study:
            values["modes"] = ", ".join(MODE_NAMES[m] for m in study.enabled_modes if m in MODE_NAMES)
        else:
            name = "defense_controls"
    if name in {"sources", "sources_more"}:
        by_id = {u.id: u for u in live}
        turn = (
            db.get(models.Turn, str(context.last_approved_turn_id)) if context.last_approved_turn_id else None
        )
        event = (
            db.query(models.TraceEvent)
            .filter_by(session_id=session.id, turn_id=turn.id, event_type="guided_dialogue_decision")
            .one_or_none()
            if turn and turn.session_id == session.id
            else None
        )
        verdict = db.get(models.VerificationResult, turn.verification_result_id) if turn else None
        expected = [str(ref) for ref in context.last_approved_unit_ids]
        prior = (
            [by_id[ref] for ref in expected if ref in by_id]
            if (
                event
                and verdict
                and verdict.verdict == "approved"
                and event.payload.get("unit_ids") == expected
            )
            else []
        )
        refs = [ref for unit in prior for ref in unit.source_refs]
        descriptions = []
        for ref in refs:
            doc = db.get(models.MaterialDocument, ref["document_id"])
            fragment = db.get(models.MaterialFragment, ref["fragment_id"])
            if doc and fragment:
                title = re.sub(r"\.[^.]+$", "", doc.filename).replace("_", " ").replace("-", " ")
                item = f"{title}, sección {fragment.location_ref}"
                if name == "sources_more":
                    item += f", versión {doc.version}, formato " + (
                        "PDF" if doc.mime_type == "application/pdf" else "texto"
                    )
                if item not in descriptions:
                    descriptions.append(item)
        if descriptions:
            values["source"] = "; ".join(descriptions[:3])
        else:
            name = "no_sources"
    if name in {
        "privacy",
        "privacy_closed",
        "privacy_pending",
        "privacy_confirmed",
        "close_confirm",
        "finish",
    }:
        view = privacy_view(db, session)
        effective_scope = view["scope"] if set(view["scope"]) <= set(view["allowed_scopes"]) else []
        key = (
            chosen
            or (context.pending_conservation if name == "privacy_pending" else None)
            or choice_for_scope(effective_scope)
        )
        if name == "privacy_pending" and not set(CHOICES[key][2]) <= set(view["allowed_scopes"]):
            return render_navigation(db, session, activity, "privacy_forbidden", context, units)
        values["choice"] = CHOICES[key][0]
        if name == "privacy":
            values["privacy_options"] = "; ".join(
                phrase for _, phrase, scopes in CHOICES.values() if set(scopes) <= set(view["allowed_scopes"])
            )
        if name in {"privacy", "privacy_closed", "privacy_pending"}:
            values["days"] = (
                f"{view['retention_days']} días"
                if view["retention_authorized"]
                else "sin conservación autorizada"
            )
        if name == "privacy_pending":
            values["confirmation"] = "confirmo " + CHOICES[key][1]
    if name == "review":
        from oralia.application.services.session_privacy_service import own_transcript

        records = own_transcript(db, session)["turns"]
        if review_index is None or not 1 <= review_index <= min(len(records), 200):
            name = "no_record"
        else:
            record = records[review_index - 1]
            values = {
                "index": str(review_index),
                "input": record["input_text"] or "sin entrada",
                "output": record["output_text"] or "sin salida",
            }
    entry = (
        PEDAGOGIC_NAVIGATION_TEMPLATES.get(name.removeprefix("didactic_"))
        if name.startswith("didactic_") and pedagogy_enabled(activity, session.participant_code)
        else NAVIGATION_TEMPLATES.get(name, NAVIGATION_TEMPLATES["limited"])
    )
    if name in PACKAGE_NAVIGATION_TEMPLATES:
        if not advanced_pedagogy_enabled(activity, session.participant_code):
            raise ValueError("Package navigation not authorized")
        entry = PACKAGE_NAVIGATION_TEMPLATES[name]
    if name in CONTINUITY_NAVIGATION_TEMPLATES:
        if not continuity_enabled(activity, session.participant_code):
            raise ValueError("Continuity navigation not authorized")
        entry = CONTINUITY_NAVIGATION_TEMPLATES[name]
    refs = tuple(
        AuthorizationReferenceInput(
            data_ref=f"navigation:{session.id}:{field}",
            category=(
                "retained_session_record"
                if name == "review" and field in {"input", "output"}
                else "session_navigation"
            ),
            provenance=(
                "consented_owner_record"
                if name == "review" and field in {"input", "output"}
                else "current_session_configuration"
            ),
            recipient=session.participant_code,
            scope=scope,
            value=value,
        )
        for field, value in values.items()
    )
    snapshot = build_authorization_snapshot(session, activity, data_references=refs, catalog=catalog)
    proposal = build_output_proposal(
        snapshot,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        slots=tuple(
            BoundTemplateSlot(placeholder=field, data_ref=ref.data_ref)
            for field, ref in zip(values, refs, strict=True)
        ),
        catalog=catalog,
    )
    return snapshot, proposal
