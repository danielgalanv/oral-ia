"""Bounded clause-level requests over explicitly published pedagogical variants.

Selection is not a publication or quality gate. Unknown requests retain the
existing planner; protected practice never uses these study-only explanations.
"""

import re
from dataclasses import dataclass

from oralia.domain.dialogue.interpretation import normalized


@dataclass(frozen=True)
class PedagogicalRequest:
    purpose: str
    topic: str | None
    alternate: bool = False


def request_purpose(text, topics, current_topic=None):
    value = normalized(text).strip("¿?¡!. ")
    # Explicitly negated clauses cannot supply a positive request. Coordinated
    # positive requests with different purposes remain ambiguous.
    clauses = re.split(r"[;]|\bpero\b", value)
    purposes = []
    positive_clauses = []
    for clause in clauses:
        clause = clause.strip()
        if re.match(r"no (quiero|expliques|repitas|me expliques)\b", clause):
            continue
        positive_clauses.append(clause)
        found = None
        if re.search(r"\b(como se llama|que es|que significa|definicion de)\b", clause):
            found = "definition"
        elif re.search(r"\b(a que temperatura|bajo que condiciones|en que condiciones)\b", clause):
            found = "conditions"
        elif re.search(
            (
                "\\b(puede|pueden|podria|podrian|es posible)\\b.*\\b(pasar|convertirse|vap"
                "or|guardarse|almacenar|almacenarse|guardar)\\b"
            ),
            clause,
        ):
            found = "possibility"
        elif re.search(r"\b(por que|cual es la causa|razon de)\b", clause):
            found = "cause"
        elif re.search(
            (
                "\\b(paso a paso|en pasos|proceso para|como (?:se |el programa )?(?:pasa"
                "|evapora|condensa|valida|comprueba|funciona))\\b"
            ),
            clause,
        ):
            found = "process"
        if found:
            purposes.append(found)
            # A clause may explicitly request both cause and process. Do not
            # silently choose whichever interrogative appeared first.
            if found == "cause" and re.search(r"\bcomo (?:pasa|funciona|ocurre)\b", clause):
                purposes.append("process")
    if len(set(purposes)) > 1:
        return PedagogicalRequest("ambiguous", current_topic)
    if not purposes:
        return None
    if (
        purposes[0] == "conditions"
        and "ebullicion" in topics
        and re.search(r"\b(hierve|hervir|ebullicion)\b", value)
    ):
        return PedagogicalRequest("conditions", "ebullicion")
    # Topic-bearing arguments precede relational destinations: asking the name
    # of a check before storage is not asking for a definition of storage.
    positive = " ; ".join(positive_clauses)
    focus = re.split(r"\b(?:anterior al?|previa al?|previo al?|antes de(?:l)?)\b", positive)[0]
    predicate = re.search(
        r"\b(?:como|por que|proceso para)\s+(?:(?:se|el programa|el agua)\s+)?"
        r"(condensa|evapora|valida|comprueba|comprobar)\b",
        focus,
    )
    predicate_topics = {
        "condensa": "condensacion",
        "evapora": "evaporacion",
        "valida": "validacion",
        "comprueba": "validacion",
        "comprobar": "validacion",
    }
    if predicate and predicate_topics[predicate[1]] in topics:
        return PedagogicalRequest(purposes[0], predicate_topics[predicate[1]])
    named = [t for t in topics if re.search(r"\b" + re.escape(normalized(t)) + r"\b", focus)]
    aliases = {
        "condensacion": r"vaso frio|gotas",
        "evaporacion": r"vapor|evapora",
        "validacion": r"validar|valida|comprobar|comprobacion|registro|registros",
    }
    if not named:
        named = [t for t, pattern in aliases.items() if t in topics and re.search(pattern, focus)]
    topic = named[0] if len(named) == 1 else current_topic
    if len(named) > 1 and current_topic not in named:
        return PedagogicalRequest("ambiguous", None)
    return PedagogicalRequest(purposes[0], topic)


def pedagogical_choice(units, act, context, text, *, protected):
    if protected or act.primary_act == "repeat":
        return None
    topics = {u.topic_ref for u in units}
    request = request_purpose(text, topics, context.current_topic_ref)
    if act.primary_act in {"rephrase", "help"} and request is None and context.current_topic_ref:
        request = request_purpose(context.content_query, topics, context.current_topic_ref)
        if request:
            request = PedagogicalRequest(request.purpose, request.topic, True)
    if request is None:
        return None
    from oralia.domain.dialogue.policy import GuidedChoice

    if request.purpose == "ambiguous" or request.topic is None:
        return GuidedChoice(notice="clarify", topic_ref=context.current_topic_ref)
    if context.pending_question_unit_id:
        # Existing practice/answer policy owns pending questions.
        return None
    by_id = {u.id: u for u in units}
    refs = [
        ref
        for u in units
        if u.topic_ref == request.topic
        for ref in u.relations.get("didactic_" + request.purpose, [])
    ]
    variants = [
        by_id[ref]
        for ref in refs
        if ref in by_id and by_id[ref].topic_ref == request.topic and by_id[ref].kind == "explanation"
    ]
    alternatives = [
        by_id[ref]
        for u in variants
        for ref in u.relations.get("rephrases", [])
        if ref in by_id and by_id[ref].topic_ref == request.topic and by_id[ref].kind == "explanation"
    ]
    variants.sort(key=lambda u: (u.version, u.id))
    alternatives.sort(key=lambda u: (u.version, u.id))
    last = {str(ref) for ref in context.last_approved_unit_ids}
    repeated = bool(variants and variants[0].id in last)
    candidates = alternatives if request.alternate or repeated else variants
    if not candidates:
        return GuidedChoice(notice="limited", topic_ref=request.topic)
    return GuidedChoice(candidates[0].id, topic_ref=request.topic)


def regular_teaching_units(units):
    """Purpose variants are reachable only by their explicit reviewed relation.

    They must not perturb generic retrieval/UUID ordering of the base lessons.
    """
    variants = {
        ref
        for unit in units
        for name, refs in unit.relations.items()
        if name.startswith("didactic_")
        for ref in refs
    }
    variants.update(
        ref for unit in units if unit.id in variants for ref in unit.relations.get("rephrases", [])
    )
    return [unit for unit in units if unit.id not in variants]
