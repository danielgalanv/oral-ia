"""Reproducible synthetic candidate study; no participant publication or simulated model."""

import argparse
import asyncio
import hashlib
import json
import os
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL, CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.corpus import SemanticCatalog, load_catalog
from oralia.course_dialogue.evaluation import inspect_pedagogy
from oralia.course_dialogue.local_provider import owned_provider
from oralia.course_dialogue.runtime import propose
from oralia.course_study.__main__ import owned_lock

ROOT = Path(__file__).resolve().parents[1]


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def freeze_sources(output):
    previous = json.loads((ROOT / "specs/011-real-course-self-study/evidence/source-final.json").read_text())[
        "sha256"
    ]
    paths = set(previous)
    for directory in [ROOT / "src", ROOT / "tests"]:
        paths.update(p.relative_to(ROOT).as_posix() for p in directory.rglob("*.py"))
    paths.update(
        {
            "scripts/rehearse_course_dialogue.py",
            "scripts/course-dialogue.ps1",
            "scripts/rehearse_controlled_drafts.py",
            "scripts/inspect_controlled_drafts.py",
            "materiales/docente/feature012-course-drafts/curriculum.json",
            "materiales/docente/feature012-course-drafts/manifest.json",
            ".gitignore",
        }
    )
    hashes = {}
    with zipfile.ZipFile(output / "source-before.zip", "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(paths):
            data = (ROOT / name).read_bytes()
            hashes[name] = hashlib.sha256(data).hexdigest()
            archive.writestr(name, data)
    save(output / "source-before.json", hashes)


async def run(args, output, catalog, scenarios, provider):
    with (output / "request-events.jsonl").open("x", encoding="utf-8") as events:
        for scenario in scenarios:
            for repetition in range(args.repetitions):
                history = []
                target = output / f"{scenario['id']}-{repetition}.json"
                for stage in ["first", "followup", "correction", "repeat", "switch"]:
                    if stage not in scenario:
                        continue
                    text = scenario[stage]
                    if history and not history[-1].get("raw_candidate"):
                        text = "No he recibido una respuesta. " + text
                    captured = {}

                    def trace(
                        request, captured=captured, scenario=scenario, repetition=repetition, stage=stage
                    ):
                        captured.update(request)
                        events.write(
                            json.dumps(
                                {
                                    "event": "before_generation",
                                    "case": scenario["id"],
                                    "repetition": repetition,
                                    "stage": stage,
                                    "request": request,
                                },
                                ensure_ascii=False,
                            )
                            + "\n"
                        )
                        events.flush()

                    started = time.perf_counter()
                    try:
                        row = await propose(
                            catalog,
                            text,
                            history,
                            provider,
                            structured=not args.natural_probe,
                            inference_deadline_ms=args.deadline_ms,
                            trace=trace,
                        )
                    except Exception as exc:
                        row = {
                            "input": text,
                            "raw_candidate": None,
                            "error": type(exc).__name__,
                            "diagnostic": str(exc),
                            "publication_allowed": False,
                        }
                    row.update(
                        {
                            "request_snapshot": captured,
                            "stage": stage,
                            "elapsed_seconds": time.perf_counter() - started,
                        }
                    )
                    row["pedagogy"] = inspect_pedagogy(row, args.partition, history)
                    history.append(row)
                    save(
                        target,
                        {
                            "case": scenario,
                            "partition": args.partition,
                            "repetition": repetition,
                            "turns": history,
                            "synthetic_inputs": True,
                            "actual_local_model": True,
                            "participant_publication": False,
                            "human_review": "pending",
                        },
                    )
                    events.write(
                        json.dumps(
                            {
                                "event": "after_generation",
                                "case": scenario["id"],
                                "repetition": repetition,
                                "stage": stage,
                                "error": row.get("error"),
                                "finish_reason": row.get("provider", {}).get("finish_reason"),
                            }
                        )
                        + "\n"
                    )
                    events.flush()
                    print(
                        scenario["id"],
                        repetition,
                        stage,
                        row.get("error", "candidate"),
                        round(row["elapsed_seconds"], 2),
                        flush=True,
                    )


def main():
    parser = argparse.ArgumentParser(description="Synthetic candidate study, not participant acceptance")
    parser.add_argument("--synthetic-only", action="store_true", required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--partition", choices=["development", "reserved", "transfer"], default="development")
    parser.add_argument("--repetitions", type=int, choices=[1, 2, 3], default=3)
    parser.add_argument("--provider", choices=["cached-cuda", "ollama"], default="cached-cuda")
    parser.add_argument("--deadline-ms", type=int, choices=[6000, 15000, 30000], default=30000)
    parser.add_argument("--cached-model", choices=["1.5b", "7b-nf4"], default="1.5b")
    parser.add_argument("--natural-probe", action="store_true")
    args = parser.parse_args()
    if args.provider == "ollama" and args.deadline_ms != 6000:
        parser.error("Ollama study preserves6000ms; select that budget explicitly")
    output = args.output.resolve()
    if not output.is_relative_to(ROOT):
        parser.error("Study output must be inside workspace")
    output.mkdir(parents=True, exist_ok=False)
    cases_bytes = args.cases.read_bytes()
    cases = json.loads(cases_bytes)
    scenarios = cases["scenarios"] if args.partition == "transfer" else cases[args.partition]
    save(output / "cases.json", cases)
    save(
        output / "run-manifest.json",
        {
            "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
            "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
            "participant_publication": False,
            "human_review": "pending",
            "full_g2_repetitions": args.repetitions == 3,
        },
    )
    freeze_sources(output)
    catalog = SemanticCatalog(load_catalog())
    save(output / "source-catalog.json", list(catalog))
    root = lab_root(ROOT)
    with owned_lock(root):
        if args.provider == "cached-cuda":

            async def execute():
                async with cached_provider(
                    output,
                    source=CACHED_MODEL_7B if args.cached_model == "7b-nf4" else CACHED_MODEL,
                    quantization="nf4" if args.cached_model == "7b-nf4" else None,
                ) as provider:
                    await run(args, output, catalog, scenarios, provider)

            asyncio.run(execute())
        else:
            with owned_provider(output) as url:
                os.environ.update(
                    {
                        "ORALIA_OLLAMA_BASE_URL": url,
                        "ORALIA_OLLAMA_MODEL": "qwen2.5:0.5b",
                        "ORALIA_OLLAMA_TIMEOUT_MS": "6000",
                        "ORALIA_OLLAMA_MAX_TOKENS": "256",
                        "NO_PROXY": "127.0.0.1,localhost",
                    }
                )
                asyncio.run(run(args, output, catalog, scenarios, None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
