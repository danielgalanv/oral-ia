"""Optional real-Ollama integration test (research.md §1) — validates
`OllamaGenerationAdapter` against an actual local Ollama server. Skipped by default:
requires `ORALIA_OLLAMA_BASE_URL` and `ORALIA_OLLAMA_MODEL` to be configured, and a
running Ollama instance with that model pulled. Never runs in the normal
`uv run pytest -q -m "not ollama"` suite."""

from __future__ import annotations

import os

import pytest

from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationRequest
from oralia.infrastructure.generation.ollama_adapter import OllamaGenerationAdapter

pytestmark = pytest.mark.ollama

_SKIP_REASON = "requires ORALIA_OLLAMA_BASE_URL/ORALIA_OLLAMA_MODEL and a running Ollama server"


@pytest.mark.skipif(
    not (os.environ.get("ORALIA_OLLAMA_BASE_URL") and os.environ.get("ORALIA_OLLAMA_MODEL")),
    reason=_SKIP_REASON,
)
async def test_ollama_adapter_produces_grounded_text_against_real_server():
    adapter = OllamaGenerationAdapter()
    request = GenerationRequest(
        purpose="explicacion",
        instruction=(
            "Eres un asistente de apoyo docente. Responde usando únicamente el "
            "contenido de las etiquetas <evidencia>. Responde en español, de forma "
            "breve."
        ),
        evidence=[
            EvidenceItem(
                fragment_id="f1",
                text="La fotosíntesis convierte luz solar en energía química mediante clorofila.",
                document_id="d1",
                document_version=1,
            )
        ],
        concepts_addressed=[],
        general_knowledge_allowed=False,
    )

    outcome = await adapter.generate(request)

    assert outcome.ok is True
    assert outcome.adapter == "ollama"
    assert outcome.text.strip()
    assert outcome.model == os.environ["ORALIA_OLLAMA_MODEL"]
