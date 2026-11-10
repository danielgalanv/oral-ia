"""Pure controlled planning over published teacher content; not an authority gate."""

import re
from dataclasses import dataclass

from oralia.domain.dialogue.contracts import DialogueAct, DialogueContext
from oralia.domain.dialogue.interpretation import normalized


@dataclass(frozen=True)
class GuidedChoice:
    unit_id: str | None = None
    notice: str | None = None
    topic_ref: str | None = None
    pending_topic: str | None = None
    is_question: bool = False
    support_step: int = 0
    additional_unit_ids: tuple[str, ...] = ()


_STOP = set(
    "el la los las un una de del a al en es se ser que como por para con sobre me lo esto eso agua programa "
    "dime sabes puede momento puedes".split()
)


def words(text):
    stems = {
        re.sub(r"(?:ar|er|ir|[aeiou]s?)$", "", w)[:5]
        for w in re.findall(r"[a-z0-9]+", normalized(text))
        if len(w) > 2 and w not in _STOP
    }
    # Small declared Spanish lexical equivalence for retrieval only. It cannot
    # create a unit, authorize its text, or provide a confidence probability.
    return {"conse" if word in {"guard", "persi"} else word for word in stems}


def retrieval_score(query, unit):
    # A negated operation is not positive evidence that this component performs
    # it. This ranking never replaces the independent disclosure/grounding gates.
    clauses = re.split(r"[.;]", normalized(unit.reviewed_content))
    positive = " ".join(re.split(r"\b(?:no|ni|sin)\b", clause)[0] for clause in clauses)
    terms = words(positive + " " + unit.topic_ref)
    matches = len(query & terms)
    return matches + matches / (1 + len(terms))


def choose(
    units,
    act: DialogueAct,
    context: DialogueContext,
    raw_text: str,
    *,
    protected: bool,
    initial_question=None,
    study_mode=None,
):
    """Select references only. Caller must revalidate every selected unit before rendering."""
    by_id = {u.id: u for u in units}
    topics = sorted({u.topic_ref for u in units})
    topic = context.current_topic_ref
    pending = by_id.get(str(context.pending_question_unit_id)) if context.pending_question_unit_id else None
    last = [by_id[str(ref)] for ref in context.last_approved_unit_ids if str(ref) in by_id]
    primary = act.primary_act
    if (
        protected
        and context.pending_question_unit_id is None
        and primary in {"ambiguous", "content_question", "help", "continue"}
        and (not raw_text.strip() or re.search(r"\b(pregunta|empezar|comenzar)\b", normalized(raw_text)))
    ):
        question = next(
            (u for u in units if u.kind == "question" and u.reviewed_content == initial_question), None
        )
        if question:
            return GuidedChoice(question.id, topic_ref=question.topic_ref, is_question=True)
    value = normalized(raw_text)
    confirmed = value.startswith(("confirmo", "elijo "))
    named_topics = [t for t in topics if re.search(r"\b" + re.escape(normalized(t)) + r"\b", value)]
    if len(named_topics) > 1 and act.requested_topic is None and primary != "repeat":
        return GuidedChoice(notice="clarify", topic_ref=topic)
    explicit_topic = act.requested_topic or (named_topics[0] if named_topics else None)
    if (
        primary == "content_answer"
        and pending
        and explicit_topic
        and topic
        and explicit_topic != topic
        and not confirmed
        and normalized(explicit_topic)
        not in normalized(
            pending.reviewed_content
            + " "
            + " ".join(u.reviewed_content for u in units if u.topic_ref == topic and u.kind == "explanation")
        )
    ):
        return GuidedChoice(notice="confirm_topic", topic_ref=topic, pending_topic=explicit_topic)
    keep_objective = topic is not None and primary in {
        "repeat",
        "rephrase",
        "help",
        "continue",
        "example",
        "comparison",
    }
    if explicit_topic and primary not in {"topic_switch", "content_answer"} and not keep_objective:
        if pending and topic and explicit_topic != topic and not confirmed:
            return GuidedChoice(notice="confirm_topic", topic_ref=topic, pending_topic=explicit_topic)
        topic = explicit_topic
    if confirmed and (explicit_topic or context.pending_topic_ref):
        topic = explicit_topic or context.pending_topic_ref
        primary = "content_question"
    elif primary == "topic_switch":
        next_topic = explicit_topic or next((t for t in topics if t != topic), None)
        return GuidedChoice(notice="confirm_topic", topic_ref=topic, pending_topic=next_topic)
    if primary == "finish":
        return GuidedChoice(notice="finish", topic_ref=topic)
    if primary == "greeting":
        return GuidedChoice(notice="orientation", topic_ref=topic)
    if primary == "ambiguous":
        return GuidedChoice(notice="clarify", topic_ref=topic)
    if primary == "repeat":
        if act.repeat_target in {"explanation", "example", "comparison", "hint"}:
            selected = next((u for u in last if u.kind == act.repeat_target), None)
        elif act.repeat_target == "question":
            selected = pending or next((u for u in last if u.kind == "question"), None)
        elif act.repeat_target == "last_output":
            selected = last[0] if last else None
        else:
            selected = pending or (last[0] if last else None)
        repeat_parts = act.repeat_target in {None, "last_output"} and (
            pending is None or act.repeat_target == "last_output"
        )
        return (
            GuidedChoice(
                selected.id,
                topic_ref=selected.topic_ref,
                is_question=selected.kind == "question",
                support_step=context.support_step,
                additional_unit_ids=tuple(u.id for u in last[1:]) if repeat_parts else (),
            )
            if selected
            else GuidedChoice(
                notice="orientation" if act.repeat_target == "question" else "clarify", topic_ref=topic
            )
        )
    if protected and primary in {"example", "comparison"}:
        # The current publication contract reserves safe_hint to hint units.
        # Study-only examples/comparisons cannot be relabelled or replaced by a question.
        return GuidedChoice(notice="limited", topic_ref=topic, support_step=context.support_step)
    if protected and re.search(r"\b(?:dame|muestra|revela)\s+(?:la\s+)?solucion\b", value):
        return GuidedChoice(notice="limited", topic_ref=topic, support_step=context.support_step)
    if primary in {"help", "continue"} and pending:
        hints = pending.relations.get("hints", [])
        index = context.support_step
        hint = by_id.get(hints[index]) if index < len(hints) else None
        if hint and hint.kind == "hint" and hint.reveal_policy == "safe_hint":
            return GuidedChoice(hint.id, topic_ref=topic, support_step=min(index + 1, 3))
        return GuidedChoice(notice="limited", topic_ref=topic, support_step=context.support_step)
    if primary == "rephrase" and pending:
        alternative = next(
            (by_id[ref] for ref in pending.relations.get("rephrases", []) if ref in by_id), None
        )
        if alternative:
            if last and alternative.id == last[0].id:
                return GuidedChoice(notice="limited", topic_ref=topic, support_step=context.support_step)
            return GuidedChoice(
                alternative.id, topic_ref=topic, is_question=True, support_step=context.support_step
            )
    if primary == "content_answer" and pending:
        # A participant claim never becomes a new topic or the source's assertion.
        # Keep the pending question; follow-up help is selected by its objective.
        followup = next((by_id[ref] for ref in pending.relations.get("rephrases", []) if ref in by_id), None)
        return (
            GuidedChoice(followup.id, topic_ref=topic, is_question=True)
            if followup
            else GuidedChoice(pending.id, topic_ref=topic, is_question=True)
        )
    contextual = (
        primary in {"help", "continue", "example", "comparison", "rephrase", "mode_switch"}
        or act.reason_code == "explicit_control"
    )
    if not contextual and not confirmed:
        query = words(raw_text)
        scores = {
            t: max(
                (retrieval_score(query, u) for u in units if u.topic_ref == t and u.kind == "explanation"),
                default=0,
            )
            for t in topics
        }
        best = max(scores.values(), default=0)
        winners = [t for t, score in scores.items() if score == best and best > 0]
        if explicit_topic:
            winners = [explicit_topic]
        if len(winners) == 1:
            if pending and topic and winners[0] != topic and not confirmed:
                return GuidedChoice(notice="confirm_topic", topic_ref=topic, pending_topic=winners[0])
            topic = winners[0]
        elif not topic:
            return GuidedChoice(notice="orientation", topic_ref=None)
    if topic is None and primary == "mode_switch":
        first = next((u for u in units if u.kind == "explanation"), None)
        topic = first.topic_ref if first else None
    if topic is None:
        return GuidedChoice(notice="orientation")
    if protected or (study_mode == "concept_review" and primary not in {"example", "comparison"}):
        kind = "question"
    else:
        kind = {
            "example": "example",
            "comparison": "comparison",
            "rephrase": "comparison",
            "continue": "example",
        }.get(primary, "explanation")
    if study_mode == "guided_explanation" and primary == "continue" and last:
        kind = {"explanation": "example", "example": "comparison", "comparison": "question"}.get(
            last[0].kind, "question"
        )
    if study_mode == "presentation_preparation" and primary in {
        "content_question",
        "mode_switch",
        "continue",
    }:
        selected_parts = [
            next((u for u in units if u.topic_ref == topic and u.kind == kind), None)
            for kind in ("explanation", "example", "comparison")
        ]
        if all(selected_parts):
            if tuple(u.id for u in selected_parts) == tuple(
                str(ref) for ref in context.last_approved_unit_ids
            ):
                return GuidedChoice(notice="limited", topic_ref=topic)
            return GuidedChoice(
                selected_parts[0].id,
                topic_ref=topic,
                additional_unit_ids=tuple(u.id for u in selected_parts[1:]),
            )
    candidates = [u for u in units if u.topic_ref == topic and u.kind == kind]
    # Main questions have reviewed hint relations; alternative formulations are not
    # selected as a replacement merely because their UUID sorts first.
    candidates.sort(key=lambda u: (not bool(u.relations.get("hints")), u.version, u.id))
    selected = candidates[0] if candidates else None
    if selected and last and selected.id == last[0].id and primary != "repeat":
        alternate = next(
            (u for u in units if u.topic_ref == topic and u.kind == "example" and u.id != selected.id), None
        )
        if not protected and alternate:
            selected = alternate
        else:
            return GuidedChoice(notice="limited", topic_ref=topic, support_step=context.support_step)
    return (
        GuidedChoice(selected.id, topic_ref=topic, is_question=kind == "question")
        if selected
        else GuidedChoice(notice="limited", topic_ref=topic)
    )
