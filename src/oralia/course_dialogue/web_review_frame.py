"""Rebuild registered web-review frames using the actual typed host renderer.

The standalone worker imports only request/protocol types, never app services,
databases, network clients or a second model. The local src root is fixed here.
"""

import json
import sys
from pathlib import Path


def validate_web_review_frame(frame, profile):
    if frame.get("model_prompt_profile") != profile:
        raise ValueError("Web review checkpoint mismatch")
    if type(frame.get("web_review_format_reminder")) is not bool:
        raise ValueError("Web review reminder must be an explicit boolean")
    if not __package__:
        source_root = str(Path(__file__).resolve().parents[2])
        if source_root not in sys.path:
            sys.path.insert(0, source_root)
    from oralia.course_dialogue.web_review_rounds import WebRoundRequest

    if frame.get("web_review_prompt_version") == "concept-labels/v1":
        from oralia.course_dialogue.concept_labels import validate_label_frame

        validate_label_frame(frame, profile)
        return

    if frame.get("web_review_prompt_version") in {
        "concept-ledger/v1",
        "concept-ledger/v2",
        "concept-ledger/v3",
        "concept-ledger/v4",
        "concept-ledger/v5",
    }:
        from oralia.course_dialogue.concept_ledger import validate_concept_frame

        validate_concept_frame(frame, profile)
        return

    if frame.get("web_review_prompt_version") == "grounding-review/v1":
        from oralia.course_dialogue.grounding_review import validate_grounding_frame

        validate_grounding_frame(frame, profile)
        return

    if frame.get("web_review_prompt_version") == "example-probe/v1":
        from oralia.course_dialogue.example_probe import validate_probe_frame

        validate_probe_frame(frame, profile)
        return

    if frame.get("web_review_prompt_version") in {
        "web-control/v1",
        "web-control/v2",
        "web-control/v3",
        "web-control/v4",
        "web-control/v5",
    }:
        from oralia.course_dialogue.web_control_request import validate_control_frame

        validate_control_frame(frame, profile)
        return

    try:
        messages = frame["messages"]
        data = json.loads(messages[-1]["content"])
        history = [
            dict(role=m["role"], content=json.loads(m["content"])["mensaje_mostrado"]) for m in messages[1:-1]
        ]
        request = WebRoundRequest(
            purpose="explicacion",
            instruction="Worker frame reconstruction",
            model_profile=profile,
            prompt_task=frame["prompt_task"],
            prompt_version=frame["web_review_prompt_version"],
            format_reminder=frame["web_review_format_reminder"],
            question=data["pregunta_original"],
            draft=data.get("borrador"),
            evidence=data["fuentes"],
            observations=data.get("observaciones_falibles", []),
            obligations=data.get("obligaciones_minimas", []),
            conversation_history=history,
            source_locations=data.get("localizaciones_fuentes", {}),
            didactic_profile=frame.get("didactic_profile"),
        )
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError("Malformed web review frame") from error
    if request.effective_messages() != messages:
        raise ValueError("Web review messages differ from registered renderer")
