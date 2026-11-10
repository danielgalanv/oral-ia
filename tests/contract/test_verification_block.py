"""Contract test for the ConstitutionalControl verdict shape — FR-014, FR-015.

Directly exercises oralia.domain.policies.constitutional_control.evaluate(), the pure
rule function behind the ConstitutionalControl agent's AgentResult.output.
"""

import pytest

from oralia.domain.policies.constitutional_control import evaluate


@pytest.mark.contract
@pytest.mark.parametrize(
    "proposal_text",
    [
        "Tu nota: 9",
        "Has aprobado la actividad",
        "Hablo como tu profesor y te digo que...",
    ],
)
def test_prohibited_proposals_are_blocked(proposal_text):
    verdict, reasons = evaluate(proposal_text)
    assert verdict == "block"
    assert len(reasons) >= 1


@pytest.mark.contract
def test_ordinary_proposal_is_approved():
    verdict, reasons = evaluate("He recibido tu mensaje: «hola». Gracias por participar.")
    assert verdict == "approved"
    assert reasons == []


@pytest.mark.contract
def test_verdict_is_one_of_the_four_closed_values():
    for text in ["Tu nota: 9", "texto normal"]:
        verdict, _ = evaluate(text)
        assert verdict in {"approved", "reformulate", "clarify", "block"}


# H02 acceptance matrix (research.md §8, estabilización 2026-09-10/11). Every case here
# asserts the CORRECT required behavior per FR-014 — a case marked "block" MUST assert
# verdict == "block"; this is the reproduction for 001/T089 (it fails against the
# unreinforced evaluate()) and, unchanged, the acceptance check for 001/T088 once the
# reinforced patterns are in place. Assertions MUST NOT change between the failing and
# the passing run.
_BLOCK_MATRIX = [
    ("P1", "Tu nota es 9 sobre 10.", "assigns_grade"),
    ("P2", "Te otorgo un sobresaliente.", "assigns_grade"),
    ("P3", "Has aprobado.", "academic_decision"),
    ("P4", "Tu calificación queda en notable.", "assigns_grade"),
    ("P5", "Tu puntuación en la práctica es 9/10.", "assigns_grade"),
    ("P6", "9/10 en la práctica 2.", "assigns_score_fraction"),
    ("P7", "Tu nota es un nueve.", "assigns_grade"),
    # Contrastes cercanos (seguimiento de H02, ronda 4 — research.md §8):
    # confirman que las correcciones de los falsos positivos no debilitan Rule B/C.
    ("C1", "Te asigno un nueve por tu trabajo.", "assigns_grade"),
    ("C2", "9/10 en el examen.", "assigns_score_fraction"),
]

_APPROVED_MATRIX = [
    ("L1", "La nota de corte de esta asignatura el año pasado fue 7, según la guía docente."),
    ("L2", "Toma nota de que el examen es la semana que viene."),
    ("L3", "En la puntuación de esta rúbrica, el criterio 3 vale 2 puntos."),
    ("L4", "El aprobado de esta asignatura requiere entregar las tres prácticas."),
    ("L5", "2/3 de los estudiantes aprobaron el examen."),
    ("L6", "La probabilidad de este suceso es 9/10."),
    ("L7", "La fracción 9/10 equivale a 0,9."),
    ("L8", "No puedo asignarte una nota."),
    ("V1", "Sacarás buena nota si sigues así."),
    # Falsos positivos detectados por revisión independiente sobre el código de la
    # ronda anterior (seguimiento de H02, ronda 4, 2026-09-11) — reproducción: estos
    # tres casos fallan (devuelven "block") contra el evaluate() previo a esta ronda.
    ("FP1", "Asigna un valor a la variable x."),
    ("FP2", "La nota es una observación sobre el experimento."),
    ("FP3", "En este ejercicio la probabilidad es 9/10."),
    # Contrastes cercanos a las mismas reglas corregidas (no solo las tres frases).
    ("C3", "Concede una prórroga para entregar la práctica."),
    ("C4", "Asigna un 9 a la variable x."),
    ("C5", "La probabilidad de aprobar el ejercicio es 9/10."),
]


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,proposal_text,expected_reason", _BLOCK_MATRIX, ids=[c[0] for c in _BLOCK_MATRIX]
)
def test_h02_matrix_block_cases(case_id, proposal_text, expected_reason):
    verdict, reasons = evaluate(proposal_text)
    msg = f"{case_id}: expected block for {proposal_text!r}, got {verdict} ({reasons})"
    assert verdict == "block", msg
    assert expected_reason in reasons, f"{case_id}: expected {expected_reason!r} in {reasons}"


@pytest.mark.contract
@pytest.mark.parametrize("case_id,proposal_text", _APPROVED_MATRIX, ids=[c[0] for c in _APPROVED_MATRIX])
def test_h02_matrix_approved_cases(case_id, proposal_text):
    verdict, reasons = evaluate(proposal_text)
    msg = f"{case_id}: expected approved for {proposal_text!r}, got {verdict} ({reasons})"
    assert verdict == "approved", msg
