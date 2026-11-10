"""Narrow source-witnessed false-friend check; not a general semantic verifier."""

import re
import unicodedata

SOURCE = re.compile(
    r"\bCompleteness\.\s*Are\s+all\s+functions\s+required\s+by\s+the\s+customer\s+included\?", re.I
)
LABEL = re.compile(
    r"^\s*(?:\d+[.)]\s*)?(?:\*\*)?Complejidad(?:\*\*)?\s*:\s*(?P<definition>.+?)(?=\n\s*\n|\Z)",
    re.I | re.M | re.S,
)


def normalized(value):
    return " ".join(
        "".join(
            c for c in unicodedata.normalize("NFD", value.casefold()) if unicodedata.category(c) != "Mn"
        ).split()
    )


def terminology_finding(candidate, evidence, question):
    # Do not reinterpret a genuine question about complexity or a negated distinction.
    if re.search(r"\b(?:complejidad|complexity)\b", normalized(question)):
        return None
    witness = next(((item, match) for item in evidence if (match := SOURCE.search(item.text))), None)
    if witness is None:
        return None
    for match in LABEL.finditer(candidate):
        definition = normalized(match["definition"])
        if re.search(r"\bno (?:es|significa|equivale|se mide|debe confundirse)", definition):
            continue
        if not re.search(
            r"\btodas las funciones\b.{0,100}\b(?:esten|estan|estaran|sean)\s+incluidas\b"
            r"|\bincluir todas las funciones\b",
            definition,
        ):
            continue
        claim = match.group(0).strip()
        if len(claim) > 1000:
            continue
        item, source = witness
        quote = source.group(0)
        return {
            "rule": "source-term-completeness/v1",
            "claim_span": [
                match.start() + len(match.group(0)) - len(match.group(0).lstrip()),
                match.start() + len(match.group(0).rstrip()),
            ],
            "source_span": [source.start(), source.end()],
            "source_id": item.fragment_id,
            "literal_source": quote,
            "review": {
                "status": "issues_found",
                "issues": [
                    {
                        "kind": "contradiction",
                        "claim": claim,
                        "explanation": (
                            f"El criterio de la fuente es {quote!r}, no Complejidad. "
                            "La definición copiada trata de incluir todas las funciones. "
                            "Conserva el rótulo original Completeness o su denominación completitud; "
                            "no lo presentes como complejidad. Corrige esa denominación "
                            "y conserva el contenido válido y los datos hipotéticos."
                        ),
                        "evidence": [{"source_id": item.fragment_id}],
                    }
                ],
            },
        }
    return None
