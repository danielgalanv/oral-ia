"""New generation guidance is opt-in and does not supply an academic answer."""

import pytest

from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.model_prompt_profiles import SELF_CONTAINED_EXAMPLES, render_messages
from oralia.course_dialogue.structured_request import structured_request


def test_new_profile_preserves_v2_messages_and_adds_only_general_guidance():
    args = ("qwen25-14b", "generate", "Una pregunta real", [])
    previous = render_messages(*args, didactic_profile="study-dialogue/v2")
    current = render_messages(*args, didactic_profile="study-dialogue/v3")
    assert current[0]["content"] == previous[0]["content"] + SELF_CONTAINED_EXAMPLES
    assert current[1:] == previous[1:]
    base = RepairGenerationRequest(
        purpose="explicacion",
        instruction="Prueba de registro",
        student_input="Una pregunta real",
        evidence=[],
    )
    actual = structured_request(
        base, model_profile="qwen25-14b", task="generate", didactic_profile="study-dialogue/v3"
    )
    assert actual.effective_messages() == current
    with pytest.raises(ValueError):
        render_messages(
            "qwen25-14b", "repair", "Pregunta", [], draft="Texto", didactic_profile="study-dialogue/v3"
        )
