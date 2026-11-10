"""Finite v3 proposition/scope checks; no authorization, source mutation or candidate hash."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

VERBS = {
    "be": r"es|son|era|eran",
    "move": r"mueve|mueven",
    "have": r"tiene|tienen|tenia|tenian",
    "change": r"cambia|cambian|transforma|transforman|pasa|pasan",
    "boil": r"hierve|hierven",
    "depend": r"depende|dependen",
    "separate": r"separa|separan",
    "mean": r"significa|significan|equivale|equivalen",
    "allow": r"permite|permiten|puede|pueden",
    "store": r"guarda|guardan|almacena|almacenan|conserva|conservan",
    "receive": r"recibe|reciben|entrega|entregan",
    "check": r"valida|validan|comprueba|comprueban|verifica|verifican",
    "show": r"muestra|muestran|informa|informan|presenta|presentan",
    "contain": r"contiene|contienen|incluye|incluyen",
    "produce": r"produce|producen|ocurre|ocurren|sucede|suceden",
    "work": r"funciona|funcionan",
}
SUBJECTS = {
    "agua",
    "evaporacion",
    "ebullicion",
    "condensacion",
    "congelacion",
    "presion",
    "molecula",
    "moleculas",
    "media",
    "mediana",
    "rango",
    "registro",
    "registros",
    "entrada",
    "validacion",
    "almacenamiento",
    "salida",
    "programa",
    "dato",
    "datos",
    "valor",
    "valores",
    "tarea",
    "texto",
    "serie",
}
NUMBERS = {
    "cero": "0",
    "uno": "1",
    "dos": "2",
    "tres": "3",
    "cuatro": "4",
    "cinco": "5",
    "seis": "6",
    "siete": "7",
    "ocho": "8",
    "nueve": "9",
    "diez": "10",
    "dieciocho": "18",
    "treinta": "30",
    "cien": "100",
}


def norm(text):
    return " ".join(
        "".join(
            c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c)
        ).split()
    )


def clauses(text):
    return [
        norm(s).strip(" .¡!¿?")
        for s in re.split(r"(?<=[.!?])\s+|[;\n]+|\s+y\s+(?=(?:no|nunca|tampoco)\b)", text, flags=re.I)
        if s.strip()
    ]


@dataclass(frozen=True)
class Proposition:
    subject: str | None
    predicate: str | None
    arguments: frozenset[str]
    negative: bool
    scope: str
    numeric: str | None


def propositions(text):
    subject = None
    last_scope = ""
    result = []
    for clause in clauses(text):
        found = [
            (m.start(), m.end(), verb)
            for verb, pattern in VERBS.items()
            if (m := re.search(r"\b(?:" + pattern + r")\b", clause))
        ]
        predicate = min(found) if found else None
        before = clause[: predicate[0]] if predicate else clause
        heads = [w for w in re.findall(r"[a-z]+", before) if w in SUBJECTS]
        if heads:
            subject = heads[0]  # A property head precedes its "de la serie" qualifier.
        after = clause[predicate[1] :] if predicate else clause
        words = frozenset(w for w in re.findall(r"[a-z0-9]+", after) if len(w) > 3 or w.isdigit())
        negative = bool(
            re.search(r"\b(no|nunca|tampoco|jamas)\b", clause[: predicate[1]] if predicate else clause)
        )
        scopes = []
        for label, pattern in {
            "atmospheric": r"presion atmosferica",
            "lower_pressure": r"menor presion|presion mas baja",
            "higher_pressure": r"mayor presion|presion mas alta",
            "series_a": r"serie a\b",
            "series_b": r"serie b\b",
        }.items():
            if re.search(pattern, clause):
                scopes.append(label)
        scope = ",".join(scopes)
        if not scope and re.match(r"su\s+", clause):
            scope = last_scope
        if scopes:
            last_scope = scope
        numeric = None
        if predicate and predicate[2] == "be":
            match = re.match(r"\s*(\d+(?:[.,]\d+)?|" + "|".join(NUMBERS) + r")\b", after)
            if match:
                numeric = NUMBERS.get(match[1], match[1])
                if re.match(r"\s*,", after[match.end() :]):
                    numeric = None  # A list of observations is not a scalar property.
        predicate_name = predicate[2] if predicate else None
        if predicate_name == "allow":
            complement = re.match(r"\s+([a-z]+(?:ar|er|ir))\b", after)
            if complement:
                predicate_name += ":" + complement[1]
        result.append(Proposition(subject, predicate_name, words, negative, scope, numeric))
    return result


def compare(proposal, statements):
    conflicts = []
    uncertain = []
    for left in propositions(proposal):
        for statement in statements:
            for right in propositions(statement):
                if (
                    not left.subject
                    or left.subject != right.subject
                    or not left.predicate
                    or left.predicate != right.predicate
                ):
                    continue
                opposite = left.negative != right.negative and (
                    bool(left.arguments & right.arguments)
                    or left.numeric == right.numeric
                    and left.numeric is not None
                )
                numeric = (
                    left.numeric is not None
                    and right.numeric is not None
                    and left.numeric != right.numeric
                    and not left.negative
                    and not right.negative
                )
                if not (opposite or numeric):
                    continue
                if left.scope and right.scope and left.scope != right.scope:
                    continue
                if left.scope != right.scope:
                    uncertain.append("conditions_missing_for_comparison")
                    continue
                conflicts.append(
                    "opposite_proposition" if opposite else "different_value_same_property_and_scope"
                )
    return conflicts, uncertain


def repeated(proposal, prior):
    if not prior:
        return False
    return set(clauses(proposal)) == set(clauses(prior[-1]))
