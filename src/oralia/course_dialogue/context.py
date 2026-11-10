"""Compositional lab context from actual inputs; no academic approval or permissions."""

import re
from dataclasses import dataclass

from oralia.domain.dialogue.interpretation import interpret, normalized

SUPPORT = {"rephrase", "example", "help", "repeat", "continue"}


@dataclass(frozen=True)
class ContextPlan:
    academic_query: str
    requested_support: tuple[str, ...]
    needs_clarification: bool
    pending_question: str | None = None
    academic_topic: str | None = None
    current_request: str | None = None


def current_request(text):
    """Remove only the comparison harness's quoted previous-output preamble."""
    return re.sub(
        r"^\s*Sobre lo que acabas de mostrar\s*\(«.*?»\)\s*:\s*",
        "",
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    ).strip()


def _previous_topic(history):
    for row in reversed(history):
        if row.get("academic_topic"):
            return row["academic_topic"]
    for row in reversed(history):
        candidate = current_request(row.get("academic_query") or row["input"])
        if row.get("display_kind") == "operational":
            continue
        confusion = re.match(r"^(?:sigo confundid[oa]|no lo capto)\b", normalized(candidate))
        if not confusion and interpret(candidate).primary_act not in SUPPORT:
            return candidate
    return None


def plan_context(text, history):
    request = current_request(text)
    last_shown = next(
        (
            row
            for row in reversed(history)
            if row.get("displayed_text") and row.get("display_kind", "candidate") == "candidate"
        ),
        None,
    )
    previous = _previous_topic(history)
    pending = (last_shown or {}).get("parsed_candidate", {}).get("question")
    if pending is None:
        pending = (last_shown or {}).get("parsed_candidate", {}).get("context", {}).get("pending_question")
    if pending and normalized(pending) == normalized((last_shown or {}).get("input", "")):
        pending = None
    act = interpret(request, pending_question=bool(pending))
    support = {act.primary_act} if act.primary_act in SUPPORT else set()
    if re.match(r"^(?:sigo confundid[oa]|no lo capto)\b", normalized(request)):
        support.add("rephrase")
    if act.primary_act == "ambiguous" and act.reason_code == "conflicting_controls":
        parts = [p.strip() for p in re.split(r"[.!?;¿¡]|\by\b", request) if p.strip()]
        acts = [interpret(part).primary_act for part in parts]
        if acts and all(name in SUPPORT for name in acts):
            support = set(acts)
    elliptical = bool(re.fullmatch(r"[¿? ]*(?:y )?(?:eso|por que|como|para que)[¿? .]*", normalized(request)))
    contextual = bool(support or (pending and act.primary_act == "content_answer") or elliptical)
    query = previous if contextual and previous else request
    explicit_subject = re.match(
        r"^(?:ahora\s*,?\s*)?(?:sobre|en cuanto a)\s+(?!lo que acabas de mostrar\b)"
        r"([^,:]{4,120})\s*[,;:]\s*\S",
        request,
        flags=re.IGNORECASE,
    )
    if explicit_subject:
        query = explicit_subject.group(1).strip()
    explicit_example_topic = re.match(
        r"^(?:pon|dame|muestra)(?:me)?\s+un\s+ejemplo\s+(?:de|sobre)\s+([^.;!?]+)",
        normalized(request),
    )
    if explicit_example_topic and not re.match(
        r"^(?:eso|esto|lo anterior|ese|esa|el mismo|la misma)\b", explicit_example_topic.group(1)
    ):
        query = explicit_example_topic.group(1).strip()
    switch = re.search(
        r"\b(?:cambi(?:o|a|emos)\s+de\s+tema|hablemos\s+de\s+otra\s+cosa)\b",
        request,
        flags=re.IGNORECASE,
    )
    if switch:
        query = request[switch.end() :].strip(" :;,.¿¡") or request
    return ContextPlan(
        query,
        tuple(sorted(support)),
        act.needs_clarification and not support,
        pending,
        query,
        request,
    )
