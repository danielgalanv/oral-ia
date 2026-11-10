"""Student-facing notice built from a review trace. Fixed texts: no model output ever reaches the student.

The answer is shown unchanged (no rejection, no automatic repair); when the review found something the
teacher criteria treat as an error, the student also sees a notice naming the *kind* of possible error.
"""

import re

from oralia.course_dialogue.concept_ledger import NOTICE_KINDS

NOTICE_VERSION = "review-notice/v1"
MESSAGES = {
    "contradiction": (
        "Esta respuesta puede contener una afirmación que contradice el material de la asignatura."
    ),
    "wrong_concept": "Esta respuesta puede confundir un concepto con otro.",
    "attribution": (
        "Esta respuesta atribuye contenido a una norma o fuente concreta que no hemos podido comprobar "
        "en el material."
    ),
    "coverage": "Esta respuesta puede incluir contenido que el material de la asignatura no desarrolla.",
    "not_reviewed": "Esta respuesta no se ha podido revisar automáticamente.",
}
GUIDANCE = "Contrasta lo importante con tus apuntes o pregunta a tu profesorado."
assert set(NOTICE_KINDS) <= set(MESSAGES)  # every kind the host can flag has an authorised text


# The student states an idea and asks whether it is right: a good answer quotes the idea in order to refute it, and the
# reviewer (24B) then reads the refuted idea as the answer's own claim (labelled false alarms: 3 of 4 on this class).
_CHECK = re.compile(
    r"\b(creo que|entiendo que|pienso que|mi resumen|¿es correcto|¿voy bien|¿es verdad que|¿es así|¿es cierto que"
    r"|¿estoy en lo cierto)",
    re.I,
)
_CORRECTS = re.compile(
    r"\b(confundiendo|no se limita|no es |sino |en contraste|por el contrario|no se trata de|no consiste en"
    r"|en realidad|en cambio)",
    re.I,
)
_CONCEPT_KINDS = {"wrong_concept", "contradiction"}


def drop_corrections(trace, question):
    """The trace without the concept findings that fall on a unit refuting what the student just asserted."""
    if not _CHECK.search(question or ""):
        return trace
    units = {u["id"]: u["text"] for u in trace.get("answer_units", [])}
    checks = [
        dict(c, verdict="uncertain")
        if c.get("kind") in _CONCEPT_KINDS
        and c.get("verdict") == "incorrect"
        and _CORRECTS.search(units.get(c.get("use_id"), ""))
        else c
        for c in trace.get("checks", [])
    ]
    still = any(c.get("verdict") == "incorrect" for c in checks)
    return dict(trace, checks=checks, status=trace.get("status") if still or trace.get("status") != "issues_found" else "no_issues_found")


def build_notice(trace, extra=()):
    """None when there is nothing to tell; otherwise {version, items:[{kind, message}], guidance}."""
    status = trace.get("status")
    if status == "technical_failure":
        kinds = ["not_reviewed"]
    elif status == "issues_found":
        found = [c.get("kind") for c in trace.get("checks", []) if c.get("verdict") == "incorrect"]
        kinds = [k for k in dict.fromkeys(found) if k in NOTICE_KINDS]
    else:  # no_issues_found, or only unresolved doubts: not worth alarming the student
        kinds = []
    kinds = list(dict.fromkeys([*kinds, *extra]))
    if not kinds:
        return None
    return dict(
        version=NOTICE_VERSION, items=[dict(kind=k, message=MESSAGES[k]) for k in kinds], guidance=GUIDANCE
    )
