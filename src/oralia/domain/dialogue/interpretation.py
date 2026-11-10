"""Deterministic act interpretation; no retrieval, authorization or state mutation."""

import re
import unicodedata

from oralia.domain.dialogue.contracts import DialogueAct, Referent


def normalized(text: str) -> str:
    return " ".join(
        "".join(
            c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c)
        ).split()
    )


_CONTROLS = {
    "finish": (
        "\\b(termin(?:ar|a|emos|en)|finaliz(?:ar|a|emos)|finalicemos|a"
        "cab(?:ar|a|emos)|concluir|concluye)\\b|hemos terminado"
    ),
    "repeat": (
        r"\b(repit(?:e|elo|ela|eme|enos|as)|"
        r"repetir(?:me|nos)?(?:lo|la|los|las)?|rele(?:er|e|elo|ela)|reitera|leela de nuevo)\b"
    ),
    "rephrase": (
        "otra (forma|manera)|otras palabras|reformula|explicalo|aclar"
        "alo|no (lo )?entiendo|mas (sencillo|simple|facil)"
    ),
    "help": (
        "\\b(ayud(?:a|ame|arme|ar|as|anos|arnos|en|es)|pistas?|indicios?|indicaciones?|indicacion|"
        "orientacion|orientame|orientes|atascado)\\b|no se\\b|no sabria"
        "|me he perdido"
    ),
    "continue": (
        r"\b(continua|continuar|continuemos|sigamos|seguimos|sigue|seguir|avancemos|siguiente)\b"
        r"|y ahora|que (paso )?sigue|que viene despues"
    ),
    "example": r"\b(ejemplo|ejemplos|ilustralo|ilustracion|situacion|caso concreto)\b",
    "comparison": (
        r"\b(compara|comparar|comparacion|contrasta|contrastar|contraste|"
        r"distingue|distinguen|distinguir|relaciona|relacionar)\b|diferencia entre"
    ),
    "topic_switch": (
        "cambi(?:ar|a|es|emos)\\s+(?:(?:de|el|al|otro|otra)\\s+){0,3}(?"
        ":tema|asunto|objetivo)|otro tema|hablemos de otra cosa"
    ),
}
_MODES = {
    "guided_explanation": r"paso a paso|explicacion guiada|guiame",
    "practice_questions": (
        r"preguntas? de practica|practicar(?: con)? preguntas|" r"ponme una pregunta|quiero practicar"
    ),
    "presentation_preparation": r"exposicion|presentacion|ensayar|ensayemos",
    "concept_review": r"repasar|repaso|repasemos|revisemos conceptos|revisar conceptos|revision de conceptos",
    "doubt_resolution": r"resolv(?:er|amos) (?:una |la )?duda|modo (de )?dudas",
}


def _repeat_target(value: str):
    operation = re.search(_CONTROLS["repeat"], value)
    if operation is None:
        return None
    subject = re.search(
        r"\b(preguntas?|explicacion|ejemplos?|comparacion|pistas?|indicios?|respuestas?)\b",
        value[operation.end() :],
    )
    if subject is None:
        return None
    word = subject.group(1).removesuffix("s")
    return {
        "pregunta": "question",
        "explicacion": "explanation",
        "ejemplo": "example",
        "comparacion": "comparison",
        "pista": "hint",
        "indicio": "hint",
        "respuesta": "last_output",
    }[word]


def interpret(
    text: str, *, pending_question: bool = False, referents: tuple[Referent, ...] = ()
) -> DialogueAct:
    value = normalized(text)
    if not value:
        return DialogueAct(primary_act="ambiguous", reason_code="missing_input", needs_clarification=True)
    # Unresolved deixis and requests to override scope are not content answers.
    scope_pattern = (
        r"(?:activ|us|permit).*?(?:todos los modos|prohibid|deshabilitad|sin restricciones)"
        r"|(?:salta|ignora|desactiva|omite).*?(?:politica|consentimiento)"
        r"|(?:datos privados|sesion ajena|otra sesion)"
        r"|recuper.*?sesion.*?(?:solo|unicamente).*?(?:seudonimo|codigo)"
        r"|(?:inventa|inventar).*?(?:dato|respuesta)|revel.*?solucion.*?prohibid"
    )

    def negated_scope(match):
        prefix = re.split(r"[;,.]", value[: match.start()])[-1]
        return bool(re.search(r"\b(?:no|sin)\s+(?:\w+\s+){0,3}$", prefix))

    if any(not negated_scope(match) for match in re.finditer(scope_pattern, value)):
        return DialogueAct(
            primary_act="ambiguous", reason_code="conflicting_controls", needs_clarification=True
        )
    if re.search(
        (
            "\\b(aquello|lo de antes|lo anterior|segunda parte|cualquiera "
            "de los dos|esa parte|cualquiera de esas|la otra|la segunda|l"
            "o mismo)\\b"
        ),
        value,
    ):
        return DialogueAct(
            primary_act="ambiguous", reason_code="ambiguous_reference", needs_clarification=True
        )
    # A noun governed by a repeat verb names its object, not a second command.
    # Coordinated operations ("repite y compara") remain separate and ambiguous.
    control_value = re.sub(
        r"((?:" + _CONTROLS["repeat"] + r")\s+"
        r"(?:(?:la|el|una|un|esa|ese|esta|este|ultima|ultimo)\s+){0,2})"
        r"(?:comparacion|ejemplos?|pistas?|indicios?|orientacion)\b",
        r"\1contenido",
        value,
    )
    control_value = re.sub(
        r"((?:" + _CONTROLS["continue"] + r")\s+(?:despues de(?:l)?|de|del|tras|con|sobre)\s+"
        r"(?:(?:la|el|una|un|esa|ese|esta|este|ultima|ultimo)\s+){0,2})"
        r"(?:comparacion|ejemplos?|pistas?|indicios?|orientacion)\b",
        r"\1contenido",
        control_value,
    )
    found = {act for act, pattern in _CONTROLS.items() if re.search(pattern, control_value)}
    negated = {
        act
        for act, pattern in _CONTROLS.items()
        if any(
            re.search(r"\b(?:no|sin)\s+(?:\w+\s+){0,3}(?:" + pattern + r")", clause)
            for clause in re.split(r"[;,.]", control_value)
        )
    }
    # The operation pattern consumes inability idioms itself; a separate no/sin
    # negates only a following operation, including short polite auxiliaries.
    active = found - negated
    if "help" in active and re.search(r"no (?:se|sabria) (?:como )?seguir", value):
        active.discard("continue")
    contradictory = any(
        act in negated
        and any(
            re.search(pattern, clause) and not re.search(r"\b(no|sin)\b", clause)
            for clause in re.split(r"\by\b|[;,.]", control_value)
        )
        for act, pattern in _CONTROLS.items()
    )
    if contradictory or len(active) > 1:
        return DialogueAct(
            primary_act="ambiguous",
            reason_code="conflicting_controls",
            negated_acts=tuple(sorted(negated)),
            needs_clarification=True,
        )
    if active:
        return DialogueAct(
            primary_act=next(iter(active)),
            reason_code="explicit_control",
            negated_acts=tuple(sorted(negated)),
            repeat_target=_repeat_target(value) if active == {"repeat"} else None,
        )
    if negated:
        return DialogueAct(
            primary_act="ambiguous",
            reason_code="negated_control",
            negated_acts=tuple(sorted(negated)),
            needs_clarification=True,
        )
    modes = [
        mode
        for mode, pattern in _MODES.items()
        if any(
            re.search(pattern, clause) and not re.search(r"\b(?:no|sin)\b", clause)
            for clause in re.split(r"[;,.]", value)
        )
    ]
    if len(modes) > 1:
        return DialogueAct(
            primary_act="ambiguous", reason_code="conflicting_controls", needs_clarification=True
        )
    if len(modes) == 1:
        return DialogueAct(primary_act="mode_switch", requested_mode=modes[0], reason_code="mode_request")
    greeting = r"(?:hola|buen dia|buenos dias|buenas tardes|buenas noches|buenas|saludos)"
    if re.fullmatch(r"[¡!¿?., ]*" + greeting + r"(?:[, .]+" + greeting + r")?[¡!¿?., ]*", value):
        return DialogueAct(primary_act="greeting", reason_code="explicit_control")
    reference_value = re.sub(r"\b(?:por favor|ahora)\b", "", value)
    if re.fullmatch(r"[¡!¿?., ]*(dimelo|eso|esto|aclara eso)[¡!¿?., ]*", reference_value):
        return DialogueAct(
            primary_act="repeat" if len(referents) == 1 else "ambiguous",
            reason_code="explicit_control" if len(referents) == 1 else "ambiguous_reference",
            referent_candidate_refs=referents[:4],
            needs_clarification=len(referents) != 1,
        )
    question = "?" in value or re.match(r"^(que|como|por que|donde|cuando|a que|el agua puede)\b", value)
    return DialogueAct(
        primary_act="content_question" if question or not pending_question else "content_answer",
        reason_code="content_input",
    )
