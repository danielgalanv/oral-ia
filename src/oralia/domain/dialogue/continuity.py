"""Opt-in clause/context planning; references only, never grades or authorization."""

import re
from dataclasses import dataclass

from oralia.domain.dialogue.contracts import DialogueAct
from oralia.domain.dialogue.interpretation import normalized
from oralia.domain.dialogue.package_dialogue import request_for, topic_for
from oralia.domain.dialogue.policy import GuidedChoice, words

GREETING = re.compile(r"^(?:hola|buenas(?: tardes| noches)?|buenos dias|saludos)\b[\s.!¡,;:¿?]*")


CAUSAL_FILLERS = (
    "por que para que que causa cual es la causa cual es la razon "
    "a que se debe deben motivo razon eso ese esa"
)
CAUSAL_OPERATOR = re.compile(r"por que|para que|que causa|cual es la causa|cual es la razon|a que se deben?")
DEFINITION_FOCUS = re.compile(
    r"^(?:en que consiste|que se entiende por|que significa|que es(?! posible)|definicion de)\s+"
    r"(?:(?:el|la|los|las|un|una)\s+)?(?P<head>[a-z]+)\b"
)
COMPARISON_OPERATOR = re.compile(r"difer|difier|distint|igual|coincid")
COMPARISON_FILLERS = (
    "son diferente diferentes diferencia diferencias difieren difiere distinto distintos igual iguales "
    "coincide coinciden entre esas esos estas estos ambos ambas dos resumen resumenes medida medidas "
    "descripcion descripciones sale salen resulta resultan resultar"
)

NEGATED_PROCESS = re.compile(
    r"\b(?:sin|aunque no)\s+(?:\w+\s+){0,6}?"
    r"(?:hervir|hierv[ae]|hirviendo|ebullicion|condensar|condensacion|congelar|congelacion|evaporar|evaporacion)\b"
)


def object_words(text):
    """Local conjugation equivalence for clause scope, never output authority."""
    return {"sal" if term in {"salg", "salga"} else term for term in words(text)}


def is_close_request(text):
    value = normalized(text).strip(" ¡!¿?.,")
    value = re.sub(r"^(?:si|vale|de acuerdo)[.!,:; ]+", "", value)
    return bool(
        re.search(
            r"^(?:(?:yo )?(?:quiero|voy a|me gustaria|puedes|podrias|podemos|vamos a)\s+)?"
            r"(?:termina|terminar|terminemos|finaliza|finalizar|cierra|cerrar)\b",
            value,
        )
    )


@dataclass(frozen=True)
class ClauseRequest:
    body: str
    greeting: bool
    purpose: str | None
    topic: str | None
    alternate: bool = False


def numeric_object(text):
    """A format reference, never a calculation or evaluation of the participant."""
    value = normalized(text)
    decimal = re.search(
        (
            "\\b\\d+[,.]\\d+\\b|\\b(?:cero|uno|dos|tres|cuatro|cinco|seis|siete|och"
            "o|nueve) coma (?:cero|uno|dos|tres|cuatro|cinco|seis|siete|ocho|n"
            "ueve)\\b"
        ),
        value,
    )
    if decimal:
        return "decimal"
    mentions = list(re.finditer(r"\b(?:1000|mil|007|cero cero siete)\b", value))
    return ("thousand" if mentions[-1].group() in {"1000", "mil"} else "leading_zero") if mentions else None


def interpret(text, context, units):
    value = normalized(text).strip(" ¡!¿?.,")
    greeting = GREETING.match(value)
    body = value[greeting.end() :] if greeting else value
    body = re.sub(r"^(?:(?:entonces|vale|pero|y|ahora|por favor)[, :¿?]*)+", "", body).strip()
    topics = {u.topic_ref for u in units}
    current = context.current_topic_ref
    anchors = [u for u in units if str(u.id) in {str(ref) for ref in context.last_approved_unit_ids}]
    named_topics = {t for t in topics if re.search(r"\b" + re.escape(t) + r"\b", body)}
    primary_topic = None
    modifier = NEGATED_PROCESS.search(body)
    if modifier:
        main = body[: modifier.start()] + " " + body[modifier.end() :]
        main_names = {t for t in topics if re.search(r"\b" + re.escape(t) + r"\b", main)}
        main = re.sub(r"\bsec(?:a|an|aba|aban|ara|aran|ando|ado|ada)s?\b", "secar", main)
        primary_topic = topic_for(main, topics, current) if len(main_names) <= 1 else None
        if primary_topic is None:
            return ClauseRequest(body, bool(greeting), "clarify_object", None)
    focus = DEFINITION_FOCUS.match(body)
    if focus:
        focused_topic = topic_for(focus["head"], topics)
        if focused_topic:
            primary_topic = focused_topic
        elif focus["head"].endswith(("ar", "er", "ir")):
            return ClauseRequest(body, bool(greeting), "clarify_object", None)
    topic = primary_topic or topic_for(body, topics, current)
    if (
        "evaporacion" in topics
        and re.search(r"vapor|tela|superficie|sec[ao]", body)
        and re.search(
            (
                "(?:sin(?: que| estar)?|aunque no(?: este)?|no(?: este)?)\\s+(?:her"
                "vir|hierva|hierve|hirviendo)"
            ),
            body,
        )
    ):
        topic = "evaporacion"
    topic = primary_topic or topic
    # Causal operators describe the current approved object when every content
    # term is within that object's published scope. New nouns do not inherit it.
    if topic is None and current and anchors and not named_topics and CAUSAL_OPERATOR.search(body):
        query = object_words(body) - object_words(CAUSAL_FILLERS)
        source_terms = set().union(
            *(object_words(u.reviewed_content) for u in units if u.topic_ref == current)
        )
        if query <= source_terms:
            topic = current
    # Closed process deixis uses an approved current objective before lexical ranking.
    process_terms = words(
        "cual como ocurre pasa sucede desarrolla proceso procedimiento ord"
        "en paso pasos primero despues ese esa eso valor numero"
    )
    deictic_process = bool(re.search(r"como|pasos|proceso|procedimiento|en orden", body))
    if (
        topic is None
        and current
        and context.last_approved_unit_ids
        and deictic_process
        and not (words(body) - process_terms)
    ):
        topic = current
    if topic is None:
        query = words(body) - words("hola buenas por que como dime explica primero antes calcular")
        scores = {
            t: max(
                (
                    len(query & words(u.reviewed_content))
                    for u in units
                    if u.topic_ref == t and u.kind in {"explanation", "fact", "example", "comparison"}
                ),
                default=0,
            )
            for t in topics
        }
        best = max(scores.values(), default=0)
        winners = [t for t, score in scores.items() if score == best and score >= 2]
        if len(winners) == 1:
            topic = winners[0]
    same_object = not named_topics or named_topics == {current}
    missing_anchor = current == "media" and any(
        re.search(r"ausen|sin (?:medid|una duracion|duracion)|no.*conoc", normalized(u.reviewed_content))
        for u in anchors
    )
    object_terms = words(
        "por que para que razon como cero dato valor falta ausente sin des"
        "conocido no sabemos conocemos ponemos poner sustituir sustituimos"
        " reemplazar reemplazamos reemplazarla esa ese eso lo la las en or"
        "den pasos procedimiento presento presentar expongo exponer hace h"
        "acer necesito otra explicacion"
    )
    object_terms.update(words(CAUSAL_FILLERS))
    object_terms.update(term for unit in anchors for term in words(unit.reviewed_content))
    if missing_anchor and same_object and not (words(body) - object_terms):
        if (
            re.search(r"cero|\b0\b", body)
            and re.search(r"falta|ausen|sin|desconoc|no.*sab|no.*conoc", body)
            and CAUSAL_OPERATOR.search(body)
        ):
            return ClauseRequest(body, bool(greeting), "object_cause", current)
        if re.search(r"como|pasos|en orden|procedimiento", body):
            return ClauseRequest(body, bool(greeting), "object_process", current)
    if "validacion" in topics:
        entry_operation = re.search(r"\b(?:escrib|tecle|recib|introduc|ingres|captur)", body)
        acceptance = re.search(r"acept|admit|valid|cumpl|permit", body)
        if (
            entry_operation
            and acceptance
            and not (focus and primary_topic)
            and re.search(r"cantidad|entrada|texto|registro", body)
        ):
            return ClauseRequest(body, bool(greeting), "acceptance_boundary", "validacion")
        outcome = re.search(r"guard|persist|escritura|archivo|fichero", body)
        reports_outcome = re.search(
            r"decir|diri|anunci|confirm|inform|describ|guardado|(?:respuesta|resultado) de (?:la )?escritura",
            body,
        )
        if outcome and reports_outcome and current in {"validacion", "almacenamiento"}:
            return ClauseRequest(body, bool(greeting), "storage_boundary", "validacion")
    # A contextual comparison is a relation of the approved object. Shared
    # descriptive nouns cannot replace it with another statistical topic.
    if (
        current
        and anchors
        and not named_topics
        and COMPARISON_OPERATOR.search(body)
        and (CAUSAL_OPERATOR.search(body) or "?" in text or "¿" in text)
    ):
        query = object_words(body) - object_words(CAUSAL_FILLERS + " " + COMPARISON_FILLERS)
        source_terms = set().union(
            *(object_words(u.reviewed_content) for u in units if u.topic_ref == current)
        )
        if query <= source_terms:
            return ClauseRequest(body, bool(greeting), "comparison", current)
    # Numeric property questions are answered from a published definition, not
    # by evaluating a learner or calculating a new number.
    if (
        topic in {"media", "mediana"}
        and re.search(r"\b(?:es|son|da|vale)\b", body)
        and re.search(r"\d|\b(?:cero|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve)\b", body)
        and ("?" in text or "¿" in text)
    ):
        return ClauseRequest(body, bool(greeting), "definition", topic)
    # Precondition and argument are read together: storing is subordinate to checking.
    why_clause = bool(
        CAUSAL_OPERATOR.search(body) or re.search(r"que (?:riesgo|ventaja|beneficio)|razon", body)
    )
    definition_clause = bool(
        re.search(r"en que consiste|que se entiende por|definicion|que es(?! posible)\b", body)
    )
    order_question = bool(
        why_clause
        and re.search(r"guard|almacen|escrib", body)
        and re.search(r"antes|luego|primero|despues", body)
    )
    identity = bool(re.search(r"desaparec|dej[ae].*exist|hidrogen|oxigen|descomp|romp", body))
    measure = bool(re.search(r"divid|repart|divisor|medid|medir|intent|pruebas|duracion|ausente", body))
    if order_question and "validacion" in topics:
        return ClauseRequest(body, bool(greeting), "causal_order", "validacion")
    if identity and "evaporacion" in topics:
        return ClauseRequest(
            body,
            bool(greeting),
            "molecular" if re.search(r"hidrogen|oxigen|descomp|romp", body) else "identity",
            "evaporacion",
        )
    if (
        current == "media"
        and context.last_approved_unit_ids
        and re.search(r"(?:\bentre|divid|repart)\b", body)
        and re.search(r"\b(?:seis|6)\b", body)
    ):
        return ClauseRequest(body, bool(greeting), "causal_count", "media")
    if measure and "media" in topics and not re.search(r"mediana", body):
        topic = "media"
        if re.search(r"divid|repart|divisor", body) and re.search(r"seis|6", body):
            return ClauseRequest(body, bool(greeting), "causal_count", topic)
        if re.search(r"cuantas|divisor|medidas validas|intento sin|sin una duracion", body) or (
            re.search(r"sin|ausente|falta", body) and re.search(r"medid|medir|duracion", body)
        ):
            return ClauseRequest(body, bool(greeting), "count", topic)
    if (
        "media" in topics
        and re.search(r"datos|valores|duraciones|observaciones|numeros|serie a", body)
        and re.search(r"lee|dime|decir|primero", body)
    ):
        return ClauseRequest(body, bool(greeting), "definition", "media")
    numeric = numeric_object(body) if "validacion" in topics else None
    numeric_deixis = bool(re.search(r"(?:ese|este|ultimo) (?:ultimo )?(?:numero|valor)|esa cantidad", body))
    if "validacion" in topics and (numeric or numeric_deixis):
        procedure = bool(re.search(r"pasos|como|en orden|procedimiento", body))
        if numeric_deixis and not numeric:
            if not context.last_approved_unit_ids or context.last_notice == "verification_failed":
                return ClauseRequest(body, bool(greeting), "clarify_numeric", None)
            numeric = numeric_object(context.content_query)
            if not numeric:
                return ClauseRequest(body, bool(greeting), "clarify_numeric", None)
        if numeric == "decimal":
            return ClauseRequest(
                body, bool(greeting), "decimal_process" if procedure else "decimal_fact", "validacion"
            )
        if procedure:
            return ClauseRequest(body, bool(greeting), "process", "validacion")
        if numeric_deixis:
            return ClauseRequest(
                body, bool(greeting), "possibility" if numeric == "thousand" else "conditions", "validacion"
            )
        return ClauseRequest(body, bool(greeting), "numeric_example", "validacion")
    question = (
        "¿" in text
        or "?" in text
        or bool(re.match(r"^(?:que|como|por que|para que|cuant\w*|cual\w*)\b", body))
    )
    alternate = not question and bool(
        re.search(
            ("no.*entiend|sin (?:ver|entender)|otra (?:manera|forma|perspectiva" "|explicacion)|me cuesta"),
            body,
        )
    )
    if alternate:
        return ClauseRequest(body, bool(greeting), None, current, True)
    if topic is None and current:
        # Closed deictic/process clauses may use an existing goal; new nouns need source overlap.
        contextual = bool(
            re.search(
                (
                    "\\b(?:eso|ese|esa|lo|sus|entonces)\\b|en orden|secuencia|procedimie"
                    "nto|paso a paso|como se (?:hace|desarrolla|produce)"
                ),
                body,
            )
        )
        source_terms = set().union(*(words(u.reviewed_content) for u in units if u.topic_ref == current))
        query = words(body) - words(
            "por que como que ocurre sucede pasa explica secuencia procedimien"
            "to orden entonces primero despues hace hacer eso ese esa lo sus"
        )
        if (contextual and not query) or (query and query <= source_terms):
            topic = current
    request = request_for(body, topics, topic)
    explicit_topic = re.sub(r"^(?:la|el)\s+", "", body).strip()
    if context.last_notice == "clarify" and explicit_topic in topics:
        topic = explicit_topic
        definition_clause = True
    if definition_clause:
        purpose = "definition"
    elif why_clause or re.search(r"moleculas", body):
        purpose = "cause"
    elif re.search(r"en orden|secuencia|procedimiento|pasos|como.*(?:pas|hac|obten|orden|sal)", body):
        purpose = "process"
    elif modifier and topic and question:
        purpose = "possibility"
    else:
        purpose = request.purpose if request else None
    if request and request.topic:
        topic = primary_topic or request.topic
    if purpose and topic:
        return ClauseRequest(body, bool(greeting), purpose, topic)
    return ClauseRequest(body, bool(greeting), None, topic)


def act_for(text, act, context, units):
    request = interpret(text, context, units)
    body = request.body
    if act.primary_act == "finish" and not is_close_request(text) and not body.startswith("confirmo"):
        act = DialogueAct(
            primary_act="content_answer" if context.pending_question_unit_id else "content_question",
            reason_code="content_input",
        )
    if context.pending_question_unit_id:
        if re.search(r"^(?:empez|comenz|repite|repetir).*pregunta", body):
            return DialogueAct(primary_act="repeat", repeat_target="question", reason_code="explicit_control")
        if re.search(r"pista|ayud|orient", body):
            return DialogueAct(primary_act="help", reason_code="explicit_control")
        statement = (
            len(body.split()) >= 4
            and not re.match(r"^(?:por que|para que|como|que|cuanto|cual)\b", body)
            and "¿" not in text
            and "?" not in text
        )
        if statement and act.primary_act not in {"repeat", "topic_switch", "finish"}:
            return DialogueAct(primary_act="content_answer", reason_code="content_input")
        if act.primary_act == "content_answer":
            return act
    if request.alternate:
        return DialogueAct(primary_act="rephrase", reason_code="explicit_control")
    if request.greeting and request.purpose:
        return DialogueAct(primary_act="content_question", reason_code="content_input")
    if request.purpose and act.primary_act not in {"repeat", "topic_switch", "finish"}:
        return DialogueAct(primary_act="content_question", reason_code="content_input")
    if request.greeting:
        return DialogueAct(primary_act="greeting", reason_code="explicit_control")
    return act


def select(units, act, context, text, *, protected, initial_question=None):
    request = interpret(text, context, units)
    by_id = {u.id: u for u in units}
    pending = by_id.get(str(context.pending_question_unit_id)) if context.pending_question_unit_id else None
    if protected:
        if act.primary_act == "greeting" and pending is None:
            q = next(
                (u for u in units if u.kind == "question" and u.reviewed_content == initial_question), None
            )
            return (GuidedChoice(q.id, topic_ref=q.topic_ref, is_question=True), {}) if q else (None, {})
        if pending and act.primary_act == "content_answer":
            refs = pending.relations.get("rephrases", [])
            previous = str(context.claim_followup.followup_unit_id) if context.claim_followup else None
            index = refs.index(previous) + 1 if previous in refs else 0
            follow = by_id.get(refs[index]) if index < len(refs) else None
            return (
                (GuidedChoice(follow.id, topic_ref=pending.topic_ref, is_question=True), {})
                if follow
                else (GuidedChoice(notice="followups_exhausted", topic_ref=pending.topic_ref), {})
            )
        return None, {}
    if act.primary_act in {"repeat", "topic_switch", "finish"} or context.pending_topic_ref:
        return None, {}
    if request.alternate:
        last = [by_id[str(ref)] for ref in context.last_approved_unit_ids if str(ref) in by_id]
        direct = [
            by_id[ref]
            for unit in last
            for ref in unit.relations.get("rephrases", [])
            if ref in by_id
            and by_id[ref].topic_ref == context.current_topic_ref
            and by_id[ref].kind == "explanation"
            and ref not in {str(x.id) for x in last}
        ]
        if direct and context.support_step < 3:
            return (
                GuidedChoice(
                    direct[0].id, topic_ref=direct[0].topic_ref, support_step=context.support_step + 1
                ),
                {},
            )
        anchor = interpret(context.content_query, context, units)
        anchor_purpose = "process" if anchor.purpose in {"molecular", "identity"} else anchor.purpose
        bases = [
            u
            for u in units
            if u.topic_ref == anchor.topic and "didactic_" + str(anchor_purpose) in u.relations
        ]
        variants = [
            by_id[r]
            for u in bases
            for r in u.relations.get("didactic_" + str(anchor_purpose), [])
            if r in by_id
        ]
        refs = variants[0].relations.get("rephrases", []) if variants else []
        index = context.support_step
        target = by_id.get(refs[index]) if index < min(3, len(refs)) else None
        if target and target.kind == "explanation" and target.topic_ref == anchor.topic:
            return GuidedChoice(target.id, topic_ref=target.topic_ref, support_step=index + 1), {}
        return GuidedChoice(notice="limited", topic_ref=context.current_topic_ref), {}
    purpose = request.purpose
    topic = request.topic
    if topic is None and re.search(r"ese ultimo|la otra|el otro|\beso\b", request.body):
        return GuidedChoice(notice="clarify", topic_ref=context.current_topic_ref), {}
    if purpose in {"clarify_numeric", "clarify_object"}:
        return GuidedChoice(notice="clarify", topic_ref=context.current_topic_ref), {}
    if not purpose or not topic:
        return None, {}
    bases = [
        u
        for u in units
        if u.topic_ref == topic and u.kind == "explanation" and "didactic_definition" in u.relations
    ]
    if not bases:
        return None, {}
    base = bases[0]

    def related(key):
        return [by_id[r] for r in base.relations.get(key, []) if r in by_id and by_id[r].topic_ref == topic]

    if purpose in {"object_cause", "object_process"}:
        relation = "didactic_cause" if purpose == "object_cause" else "didactic_process"
        anchors = [by_id[str(ref)] for ref in context.last_approved_unit_ids if str(ref) in by_id]
        candidates = [
            by_id[ref]
            for u in anchors
            for ref in u.relations.get(relation, [])
            if ref in by_id and by_id[ref].topic_ref == topic
        ]
    elif purpose == "acceptance_boundary":
        definitions = related("didactic_definition")
        candidates = [
            by_id[ref]
            for u in definitions
            for ref in u.relations.get("comparisons", [])
            if ref in by_id and by_id[ref].topic_ref == topic
        ]
    elif purpose == "storage_boundary":
        bridges = [u for u in related("comparisons") if u.relations.get("next")]
        chain = list(bridges)
        for _ in range(2):
            chain.extend(
                by_id[ref]
                for u in tuple(chain)
                for ref in u.relations.get("next", [])
                if ref in by_id and by_id[ref].topic_ref == topic and by_id[ref] not in chain
            )
        anchors = [by_id[str(ref)] for ref in context.last_approved_unit_ids if str(ref) in by_id]
        active = next((u for u in anchors if u in chain), None)
        candidates = (
            [
                by_id[ref]
                for ref in active.relations.get("next", [])
                if ref in by_id and by_id[ref].topic_ref == topic
            ]
            if active
            else bridges
        )
    elif purpose == "comparison":
        candidates = related("comparisons")
    elif purpose in {"decimal_fact", "decimal_process"}:
        kind = "fact" if purpose == "decimal_fact" else "explanation"
        candidates = [
            u
            for u in related("next")
            if u.kind == kind and "separador decimal" in normalized(u.reviewed_content)
        ]
    elif purpose in {"causal_order", "causal_count"}:
        candidates = [u for u in related("next") if u.kind == "explanation"]
    elif purpose == "count":
        candidates = [u for u in related("next") if u.kind == "fact"]
    elif purpose == "identity":
        process = related("didactic_process")
        candidates = [
            by_id[r]
            for p in process
            for r in p.relations.get("rephrases", [])
            if r in by_id and re.search(r"desaparec|deja.*exist", normalized(by_id[r].reviewed_content))
        ]
    elif purpose == "molecular":
        candidates = [
            u
            for u in related("next")
            if u.kind == "fact"
            and "hidrogen" in normalized(u.reviewed_content)
            and "oxigen" in normalized(u.reviewed_content)
        ] or related("didactic_cause")
    elif purpose == "numeric_example":
        token = "mil" if re.search(r"1000|\bmil\b", request.body) else "siete"
        candidates = [
            u
            for u in units
            if u.topic_ref == topic and u.kind == "example" and token in normalized(u.reviewed_content)
        ]
    else:
        candidates = related("didactic_" + purpose)
    if not candidates:
        return GuidedChoice(notice="limited", topic_ref=topic), {}
    chosen = candidates[0]
    if purpose == "definition":
        family = [
            chosen,
            *[
                by_id[ref]
                for ref in chosen.relations.get("rephrases", [])
                if ref in by_id and by_id[ref].topic_ref == topic and by_id[ref].kind == "explanation"
            ],
        ]
        previous = next(
            (
                i
                for i, unit in enumerate(family)
                if str(unit.id) in {str(ref) for ref in context.last_approved_unit_ids}
            ),
            None,
        )
        if previous is not None:
            if previous + 1 >= len(family):
                return GuidedChoice(notice="limited", topic_ref=topic), {}
            chosen = family[previous + 1]
    return GuidedChoice(chosen.id, topic_ref=topic), {}
