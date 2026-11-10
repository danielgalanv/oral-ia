"""Context-bound natural control aliases; never a free-text consent inference."""

import re

from oralia.application.services.session_privacy_service import privacy_view
from oralia.domain.dialogue.continuity import is_close_request
from oralia.domain.dialogue.contracts import DialogueAct
from oralia.domain.dialogue.interpretation import normalized


def plan_pending_operation(db, session, text, context):
    from oralia.application.services.screenless_navigation_service import NavigationPlan

    value = normalized(text).strip(" ¡!¿?.,")
    if not value:
        return None
    quoted = bool(re.search(r'["«»]', value))
    negative = bool(
        re.search(
            (
                "\\b(?:no|nunca)\\s+(?:lo\\s+)?(?:confirm|quiero\\s+(?:cerr|termin|fin"
                "aliz)|termines|cierres|finalices)"
            ),
            value,
        )
    )
    if quoted or negative:
        if context.close_confirmation_pending or context.pending_conservation:
            return NavigationPlan(
                "cancelled", {"close_confirmation_pending": False, "pending_conservation": None}
            )
        return None
    # A generic confirmation has no operation of its own. Leave a sole topic
    # proposal to its existing canonical resolver; never reinterpret it as close.
    generic_confirmation = value in {"confirmo", "lo confirmo"}
    if (
        generic_confirmation
        and context.pending_topic_ref
        and not context.close_confirmation_pending
        and not context.pending_conservation
    ):
        return None if value == "confirmo" else NavigationPlan("confirm_topic")
    finish = is_close_request(text)
    confirms = generic_confirmation or bool(
        re.fullmatch(
            (
                "(?:lo confirmo|confirmo (?:el cierre|terminar|finalizar|cerrar)(?: sin cons"
                "ervar(?:los| nada| el resumen ni la transcripcion)?)?|(?:estoy )?"
                "de acuerdo[, :]+(?:termina|finaliza|cierra))"
            ),
            value,
        )
    )
    none = bool(re.search(r"sin (?:guardar|conservar)|no (?:guard(?:es|ar)|conserv(?:es|ar))", value))
    privacy = privacy_view(db, session)
    if (finish or confirms) and none and privacy["retain"]:
        return NavigationPlan(
            "privacy_pending",
            {"pending_conservation": "none", "close_confirmation_pending": False, "pending_topic_ref": None},
        )
    if confirms:
        only_close = (
            context.close_confirmation_pending
            and context.last_notice == "close_confirm"
            and not context.pending_conservation
            and not context.pending_topic_ref
        )
        only_privacy = (
            context.pending_conservation == "none"
            and context.last_notice == "privacy_pending"
            and not context.close_confirmation_pending
            and not context.pending_topic_ref
        )
        if only_privacy:
            if not generic_confirmation:
                return NavigationPlan("privacy_pending")
            return NavigationPlan("privacy_confirmed", {"pending_conservation": None}, privacy_choice="none")
        if only_close:
            return NavigationPlan(
                "finish",
                {"close_confirmation_pending": False},
                act=DialogueAct(primary_act="finish", reason_code="explicit_control"),
            )
        return NavigationPlan("clarify", {"close_confirmation_pending": False})
    if finish and not value.startswith("confirmo"):
        if context.pending_conservation:
            return NavigationPlan("privacy_pending")
        return NavigationPlan(
            "close_confirm", {"close_confirmation_pending": True, "pending_topic_ref": None}
        )
    if context.close_confirmation_pending and value not in {"confirmo cerrar", "si"}:
        return NavigationPlan(updates={"close_confirmation_pending": False})
    return None
