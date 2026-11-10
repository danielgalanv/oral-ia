"""A complete conversational body is allowed; malformed output stays undisplayed."""

import hashlib
import json

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.contracts import CandidateV4
from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.runtime import propose
from oralia.infrastructure.generation.generation_port import GenerationOutcome


def test_v4_accepts_full_explanation_with_limit_and_fictional_assumptions():
    body = (
        "La completitud pide describir lo conocido que el sistema debe hacer. "
        "La consistencia pide que esas descripciones no se contradigan. "
        "No son garantías perfectas: la complejidad del sistema y del entorno impide "
        "producir en la práctica un documento enteramente completo y consistente. "
        "Ejemplo hipotético: una tienda ficticia documenta pagos con tarjeta, pero omite "
        "la devolución; agregar esa necesidad mejora la cobertura sin prometer perfección. "
        "Inferencia: revisar con quienes conocen el uso puede revelar huecos, aunque no todos."
    )
    assert len(body) > 400
    candidate = CandidateV4(
        body=body,
        source_ids=["requirements:14"],
        modes=["documentary", "fictional_example", "inference"],
        fictional_assumptions=["La tienda y la devolución son ficticias"],
    )
    assert "Supuestos ficticios" in candidate.render_for_inspection()
    with pytest.raises(ValidationError, match="Fictional example"):
        CandidateV4(
            body=body,
            source_ids=["requirements:14"],
            modes=["documentary", "fictional_example"],
            fictional_assumptions=[],
        )
    with pytest.raises(ValidationError, match="Inference must be labelled"):
        CandidateV4(
            body="Una conclusión sin rótulo.",
            source_ids=["requirements:14"],
            modes=["documentary", "inference"],
            fictional_assumptions=[],
        )


@pytest.mark.asyncio
async def test_v4_request_and_negative_provider_paths_keep_history_and_provenance():
    name = "teacher.pdf"
    page = {
        "id": "teacher:1",
        "filename": name,
        "original_sha256": hashlib.sha256(name.encode()).hexdigest(),
        "version": 1,
        "page": 1,
        "text": "Completitud\nNo se garantiza un documento completo por complejidad.\n",
    }
    unit = build_units([page])[0]
    history = [
        {
            "input": "Primera duda",
            "displayed_text": "Una explicación realmente mostrada",
            "display_kind": "candidate",
            "raw_candidate": "RAW NO MOSTRADO",
        }
    ]
    requests = []

    class Provider:
        def __init__(self, output, finish="stop"):
            self.output = output
            self.finish = finish

        async def generate(self, request):
            requests.append(request)
            return GenerationOutcome(
                ok=True,
                text=self.output,
                adapter="transformers_local",
                finish_reason=self.finish,
            )

    valid = json.dumps(
        {
            "schema_version": 4,
            "body": "La completitud se busca, pero no se garantiza en la práctica por la complejidad.",
            "source_ids": [unit.id],
            "modes": ["documentary"],
            "fictional_assumptions": [],
        }
    )
    args = dict(variant="documental", document_units=[unit], conversational_output=True)
    good = await propose([page], "completitud", history, Provider(valid), **args)
    assert good["display_kind"] == "candidate" and good["publication_allowed"] is False
    assert requests[-1].output_schema["properties"]["body"]["maxLength"] == 3500
    assert requests[-1].conversation_history[-1].content == "Una explicación realmente mostrada"
    assert "RAW NO MOSTRADO" not in json.dumps(requests[-1].model_dump())
    partial = await propose([page], "completitud", history, Provider(valid, "length"), **args)
    assert partial["error"] == "generation_incomplete" and partial["display_kind"] == "operational"
    foreign = valid.replace(unit.id, "foreign:1")
    wrong = await propose([page], "completitud", history, Provider(foreign), **args)
    assert wrong["error"] == "unretrieved_source_reference"
    assert wrong["display_kind"] == "operational"
    invalid = await propose([page], "completitud", history, Provider("{"), **args)
    assert invalid["error"] == "invalid_candidate_contract"
    assert invalid["display_kind"] == "operational"
