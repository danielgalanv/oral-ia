"""Real dense CPU retrieval -> GenerationPort fixture -> diagnostic receipt.

No generator weights, downloads, CUDA, warmup or LLM inference. Explicit synthetic
evidence recording is confined to an exclusive audit folder, not product sessions.
"""

import argparse
import asyncio
import hashlib
import json
import socket
import sys
import uuid
from pathlib import Path

from oralia.documentary.retrieval import DERIVED, Retrieval
from oralia.documentary.study_lab import DiagnosticStudy, FixtureGenerationPort, TrialBudget


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def verify(output):
    output.mkdir(parents=True, exist_ok=False)
    tracked = [DERIVED / "identity.json", DERIVED / "fragments.json", DERIVED / "chroma/index_version.json"]
    before = {str(p): digest(p) for p in tracked}
    original_connect = socket.socket.connect
    attempts = []

    def offline(sock, address):
        if isinstance(address, tuple) and address[0] not in {"127.0.0.1", "localhost", "::1"}:
            attempts.append(str(address))
            raise RuntimeError("external network denied by CPU verification")
        return original_connect(sock, address)

    socket.socket.connect = offline
    try:
        retrieval = await asyncio.to_thread(Retrieval)
        assert str(retrieval.model.device) == "cpu"
        lab = DiagnosticStudy(
            retrieval,
            FixtureGenerationPort(),
            authority=lambda: True,
            budget=TrialBudget(),
            course="ingenieria-software",
            activity="requirements-teacher-diagnostic-v2",
        )
        receipts = []
        # Real ranking, not pages chosen by question/test ID. Fixture answers only
        # exercise transport/history. No academic quality is inferred from them.
        for question in ["¿Qué es un requisito en Ingeniería del Software?", "¿Qué tipos de requisitos hay?"]:
            result = await lab.turn(question, str(uuid.uuid4()))
            assert result["status"] == "prepared_unverified", result
            row = lab.display(result["id"])
            assert row["request"]["evidence"] and row["retrieval"]["strategy"] == "dense"
            assert row["request"]["constraints"]["deadline_ms"] == 50000
            assert row["semantic_support"] == "unverified" and not row["publication_allowed"]
            receipts.append(row)
            # This is a simulated display acknowledgement to test transport.
            # The separate browser evidence verifies actual DOM acknowledgement.
            (output / f"{row['id']}.json").write_text(
                json.dumps(row, ensure_ascii=False, indent=2), encoding="utf8"
            )
            lab.acknowledge(row["id"])
        assert (
            receipts[1]["request"]["conversation_history"][-1]["content"] == receipts[0]["diagnostic_preview"]
        )
        lab.close()
        assert not lab.history and not lab.receipts
        summary = {
            "kind": "REAL_CPU_RETRIEVAL_WITH_GENERATION_FIXTURE_NOT_LLM",
            "encoder_device": str(retrieval.model.device),
            "identity": retrieval.fingerprint,
            "pages": len(retrieval.pages),
            "index_version": retrieval.store.get_index_version(),
            "tracked_files_unchanged": before == {str(p): digest(p) for p in tracked},
            "external_network_attempts": attempts,
            "llm_requests": 0,
            "warmups": 0,
            "fixture_requests": len(receipts),
            "publication_allowed": False,
            "display_acknowledgement": "simulated_transport_check_not_human_session",
            "generator_model_loaded": False,
            "transformers_cuda_worker_imported": "oralia.course_dialogue.gpu_worker" in sys.modules,
        }
        (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf8")
        print(json.dumps(summary, indent=2), flush=True)
    finally:
        socket.socket.connect = original_connect


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    asyncio.run(verify(parser.parse_args().output))
