import pytest

from oralia.domain.policies.constitutional_control import evaluate


@pytest.mark.parametrize(
    "candidate",
    [
        "Tu nota es 8.",
        "Has aprobado.",
        "Tu nivel es alto.",
        "Tu rendimiento es excelente.",
        "Tu capacidad es baja.",
        "Tu comprensión es insuficiente.",
        "Eres competente en arquitectura.",
    ],
)
def test_personal_academic_characterizations_are_blocked(candidate):
    assert evaluate(candidate)[0] == "block"


@pytest.mark.parametrize(
    "candidate",
    [
        "La capacidad del sistema es de diez solicitudes.",
        "¿Cómo justificas la arquitectura?",
        "Se solicitó una aclaración.",
    ],
)
def test_observable_system_facts_and_subject_terms_are_allowed(candidate):
    assert evaluate(candidate)[0] == "approved"
