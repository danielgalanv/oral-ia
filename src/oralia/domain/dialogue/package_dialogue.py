"""Opt-in package dialogue: bounded clause/context planning, never output authority."""

from __future__ import annotations

import re

from oralia.domain.dialogue.contracts import DialogueAct
from oralia.domain.dialogue.interpretation import normalized
from oralia.domain.dialogue.pedagogy import PedagogicalRequest
from oralia.domain.dialogue.policy import GuidedChoice

DOUBTS = {
    "no lo entiendo",
    "explicalo de otra forma",
    "sigo sin entenderlo",
    "necesito otra explicacion",
    "otra explicacion",
    "no me queda claro",
}


def topic_for(text, topics, current=None):
    value = normalized(text)
    named = [t for t in topics if re.search(r"\b" + re.escape(normalized(t)) + r"\b", value)]
    if len(named) == 1:
        return named[0]
    if len(named) > 1:
        return current if current in named else None
    rules = {
        "evaporacion": r"evapor|secar|vapor|no hierve|sin hervir",
        "ebullicion": r"hierve|hervir|burbujas|ebullic",
        "condensacion": r"condens|gotas|vaso frio",
        "congelacion": r"congel|hielo",
        "presion": r"presion|presiones|condiciones y comparacion de fuentes",
        "validacion": r"valida|formato|rango|cantidad|digitos|cero cero siete|mil",
        "almacenamiento": r"almacena|guard|escritura|archivo",
        "entrada": r"recib|captur|recepcion",
        "salida": r"mensaje|presenta|muestra",
        "responsabilidades": r"responsabil|organiza|funciones",
        "media": r"promedio|media|suma|division",
        "mediana": r"mediana|centro del orden",
        "dispersion": r"dispersion|rango|extremo",
        "ausentes": r"ausente|seis intentos|sin medida|denominador",
        "interpretacion": r"demuestra|causal|series|iguales|mas rapida|explicacion de una comparacion",
    }
    matches = [t for t, pattern in rules.items() if t in topics and re.search(pattern, value)]
    if "condensacion" in matches and re.search(r"condens|vaso frio|gotas", value):
        return "condensacion"
    if "ebullicion" in matches and re.search(r"siempre|cien|temperatura", value):
        return "ebullicion"
    if "interpretacion" in matches and re.search(r"demuestra|iguales|mas rapida", value):
        return "interpretacion"
    if len(matches) == 1:
        return matches[0]
    if matches:
        return current if current in matches else None
    # Only explicitly deictic questions may fall back to the current objective.
    if re.fullmatch(
        (
            "[¿? ]*(?:por que (?:ocurre|es asi)|como (?:sucede|ocurre|se desar"
            "rolla)(?:,? paso a paso)?|que significa eso|como se llama ese cam"
            "bio|y si no hierve)[¿? .]*"
        ),
        value,
    ):
        return current
    return None


def request_for(text, topics, current=None):
    value = normalized(text)
    topic = topic_for(text, topics, current)
    if re.search(r"^(?:[¿? ]*)(?:que significa|que es(?! posible)|define )|definicion|como se llama", value):
        purpose = "definition"
    elif re.search(r"que es posible|es posible|puede|podria|y si no hierve", value):
        purpose = "possibility"
    elif re.search(r"bajo que condicion|en que condicion|que limite|siempre|a cien|temperatura", value):
        purpose = "conditions"
    elif re.search(r"por que|causa|para que sirve", value):
        purpose = "cause"
    elif re.search(r"paso a paso|proceso|procedimiento|como (?!se llama)", value):
        purpose = "process"
    elif re.search(r"que significa|que es|definicion|define |como se llama", value):
        purpose = "definition"
    elif re.search(r"compara|diferencia|iguales", value):
        purpose = "comparison"
    elif re.search(r"ejemplo", value):
        purpose = "example"
    else:
        return None
    return PedagogicalRequest(purpose, topic)


def package_act(text, act, context, units):
    value = normalized(text).strip(" ¡!¿?.,")
    topics = {u.topic_ref for u in units}
    if re.match(r"^(hola|buenas tardes|buenos dias|buenas noches|saludos)\b", value):
        return DialogueAct(primary_act="greeting", reason_code="explicit_control")
    if value in DOUBTS:
        return DialogueAct(primary_act="rephrase", reason_code="explicit_control")
    if re.match(r"^(?:cambia a|quiero cambiar de tema a|pasemos a|hablemos de)\b", value):
        topic = topic_for(value, topics)
        return (
            DialogueAct(primary_act="topic_switch", requested_topic=topic, reason_code="explicit_control")
            if topic
            else DialogueAct(primary_act="ambiguous", reason_code="ambiguous_reference")
        )
    return act


def navigation_text(text):
    value = normalized(text).strip(" ¡!¿?.,")
    if re.fullmatch(r"de donde (?:procede|sale)(?: esa explicacion| esa pregunta| eso)", value):
        return "de donde sale eso"
    return text


def package_choice(units, act, context, text, *, protected):
    topics = {u.topic_ref for u in units}
    value = normalized(text).strip(" ¡!¿?.,")
    if act.primary_act == "greeting":
        topic = topic_for(text, topics, context.current_topic_ref)
        return GuidedChoice(notice="package_welcome", topic_ref=topic), (
            {"current_topic_ref": topic} if topic else {}
        )
    if protected or act.primary_act in {"repeat", "topic_switch", "finish"}:
        return None, {}
    if value == "confirmo" and context.pending_topic_ref in topics:
        return GuidedChoice(notice="package_topic_confirmed", topic_ref=context.pending_topic_ref), {
            "current_topic_ref": context.pending_topic_ref,
            "pending_topic_ref": None,
            "pending_question_unit_id": None,
            "pending_question_turn_id": None,
            "last_approved_unit_ids": (),
            "last_approved_turn_id": None,
            "current_subgoal_ref": None,
            "content_query": "",
            "support_step": 0,
        }
    alternate = value in DOUBTS or act.primary_act in {"rephrase", "help"}
    request = request_for(context.content_query if alternate else text, topics, context.current_topic_ref)
    if request is None:
        return GuidedChoice(notice="outside_source", topic_ref=context.current_topic_ref), {}
    if request.topic is None:
        return GuidedChoice(notice="outside_source", topic_ref=context.current_topic_ref), {}
    if context.pending_question_unit_id:
        return None, {}
    if request.purpose in {"comparison", "example"}:
        candidates = [
            u
            for u in units
            if u.topic_ref == (context.current_topic_ref or request.topic) and u.kind == request.purpose
        ]
        candidates.sort(key=lambda u: (u.created_at, u.id))
        return (
            GuidedChoice(candidates[0].id, topic_ref=candidates[0].topic_ref)
            if candidates
            else GuidedChoice(notice="limited", topic_ref=request.topic)
        ), {}
    by_id = {u.id: u for u in units}
    refs = [
        ref
        for u in units
        if u.topic_ref == request.topic
        for ref in u.relations.get("didactic_" + request.purpose, [])
    ]
    variants = [
        by_id[ref]
        for ref in dict.fromkeys(refs)
        if ref in by_id and by_id[ref].kind == "explanation" and by_id[ref].topic_ref == request.topic
    ]
    if not variants:
        return GuidedChoice(notice="limited", topic_ref=request.topic), {}
    selected = variants[0]
    step = 0
    if alternate:
        refs = selected.relations.get("rephrases", [])
        step = context.support_step
        if step >= len(refs):
            return GuidedChoice(notice="limited", topic_ref=request.topic, support_step=step), {}
        selected = by_id.get(refs[step])
        step += 1
        if not selected or selected.kind != "explanation" or selected.topic_ref != request.topic:
            return GuidedChoice(notice="limited", topic_ref=request.topic), {}
    return GuidedChoice(selected.id, topic_ref=request.topic, support_step=min(step, 3)), {}
