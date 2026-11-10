"""Explicit recording of synthetic inspection; input follows actual emitted output."""

import argparse
import asyncio
import json
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources

from oralia.course_dialogue.__main__ import inspect_drafts, lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum
from oralia.course_study.__main__ import owned_lock


async def run(args, output):
    curriculum = DraftCurriculum()
    with (output / "events.jsonl").open("x", encoding="utf8") as events:

        def record(value):
            events.write(json.dumps(value, ensure_ascii=False) + "\n")
            events.flush()

        def write(value):
            print(value, flush=True)
            record({"event": "console_output", "text": value})

        record(
            {
                "event": "synthetic_inspection",
                "participant_session": False,
                "human_review": "pending",
                "model_choice": args.model,
                "semantic_version": args.semantic_version,
            }
        )
        source = CACHED_MODEL_14B if args.model == "14b-nf4" else CACHED_MODEL_7B
        async with cached_provider(output, source=source, quantization="nf4") as provider:
            await inspect_drafts(
                curriculum, provider, semantic_version=args.semantic_version, write=write, on_event=record
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", choices=["7b-nf4", "14b-nf4"], required=True)
    parser.add_argument("--semantic-version", type=int, choices=[1, 2, 3, 4, 5, 6, 7], default=2)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "specs/012-conversational-course-study/evidence"):
        parser.error("La captura debe estar en una carpeta nueva de evidencia012.")
    with owned_lock(lab_root(ROOT)):
        output.mkdir(parents=True, exist_ok=False)
        freeze_sources(output)
        asyncio.run(run(args, output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
