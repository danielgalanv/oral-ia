"""Measured aggregates, conservative reports and integrity-checked replay packages."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import statistics
from pathlib import Path
from tempfile import TemporaryDirectory

import psutil

from oralia.validation.experiment import measure, run_cell
from oralia.validation.protocol import CORPUS, SCENARIOS, Protocol

FILES = ("protocol.json", "results.json", "report.md")
MAX_BYTES = 10 * 1024 * 1024


def digest(data: bytes):
    return hashlib.sha256(data).hexdigest()


def code_manifest():
    root = Path(__file__).resolve().parents[3]
    files = sorted((root / "src/oralia").rglob("*.py"))
    files += [root / "pyproject.toml", root / "uv.lock"]
    return {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in files}


def structural(cells):
    """Exclude random IDs, timestamps and resource/timing noise, preserve decisions."""
    fields = (
        "scenario",
        "condition",
        "repetition",
        "action",
        "grounding_verdict",
        "coherence_verdict",
        "retrieved_ids",
        "state",
        "status",
        "error",
        "recovery",
        "deleted",
        "transcription",
        "event_types",
        "fully_traced",
        "injection_applied",
        "ablations",
        "output_sources",
    )
    return [
        {
            **{key: c[key] for key in fields},
            "components": [
                {k: x[k] for k in ("agent_id", "status", "verdict", "incident_types")}
                for x in c["components"]
            ],
        }
        for c in cells
    ]


def distribution(values):
    return {
        "n": len(values),
        "mean": statistics.mean(values) if values else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "stdev": statistics.stdev(values) if len(values) > 1 else None,
        "missing_reason": None if values else "no valid measurements",
    }


def aggregate(cells):
    results = {}
    for condition in dict.fromkeys(c["condition"] for c in cells):
        rows = [c for c in cells if c["condition"] == condition]
        components = [x for c in rows for x in c["components"]]
        latency = {}
        for aid in sorted({x["agent_id"] for x in components}):
            latency[aid] = distribution([x["latency_ms"] for x in components if x["agent_id"] == aid])
        results[condition] = {
            "cells": len(rows),
            "errors": sum(c["error"] is not None for c in rows),
            "completed_experimental_cells": sum(c["error"] is None for c in rows),
            "abandoned_experimental_cells": sum(c["error"] is not None for c in rows),
            "closed_sessions": sum(c["status"] != "active" for c in rows),
            "blocked": sum(c["output_text"] is None or c["action"] == "block" for c in rows),
            "reformulated": sum(
                c["coherence_verdict"] == "reformulate" or c["action"] == "reformulate" for c in rows
            ),
            "outputs_without_sources": sum(bool(c["output_text"]) and not c["output_sources"] for c in rows),
            "timeouts": sum(x["status"] == "timeout" for x in components),
            "agent_failures": sum(x["status"] in {"error", "cancelled"} for x in components),
            "recoveries": sum(c["recovery"] is not None for c in rows),
            "coordination_conflicts": sum(c["state"]["stale_update_rejected"] is True for c in rows),
            "detected_contradictions": sum("contradiccion" in x["incident_types"] for x in components),
            "grounding_conflicts": sum(c["grounding_verdict"] == "conflictiva" for c in rows),
            "fully_traced_turns": sum(c["fully_traced"] for c in rows),
            "trace_denominator": len(rows) if condition != "baseline" else 0,
            "fully_traced_percent": (
                100 * sum(c["fully_traced"] for c in rows) / len(rows) if condition != "baseline" else None
            ),
            "reconstructable_cells": (
                sum(c["reconstruction"]["state_chain_valid"] for c in rows if c["reconstruction"])
                if condition != "baseline"
                else None
            ),
            "reconstruction_missing_reason": (
                "direct baseline has no agency state flow; empty fixture chain is not comparable"
                if condition == "baseline"
                else None
            ),
            "distinct_compositions": len(
                {
                    tuple(
                        x["agent_id"]
                        for x in c["components"]
                        if x["agent_id"] not in c["ablations"]
                        and x.get("kind", "agent") == "agent"
                        and x["agent_id"] != "direct-model"
                    )
                    for c in rows
                }
            ),
            "agents_per_turn": distribution(
                [
                    sum(
                        x.get("kind", "agent") == "agent"
                        and x["agent_id"] != "direct-model"
                        and x["agent_id"] not in c["ablations"]
                        for x in c["components"]
                    )
                    for c in rows
                ]
            ),
            "component_latency_ms": latency,
            "agent_latency_ms": {
                aid: distribution(
                    [
                        x["latency_ms"]
                        for c in rows
                        for x in c["components"]
                        if x["agent_id"] == aid and aid not in c["ablations"]
                    ]
                )
                for aid in latency
                if aid not in {"direct-model", "final-output-gate"}
            },
            "metrics": {
                name: distribution(
                    [c["metrics"][name]["value"] for c in rows if c["metrics"][name]["value"] is not None]
                )
                for name in rows[0]["metrics"]
            },
        }
    return results


def paired_effects(cells):
    full = {(c["scenario"], c["repetition"]): c for c in cells if c["condition"] == "full"}
    effects = {}
    for condition, field, aid in [
        ("no_grounding", "grounding_verdict", "grounding-verifier"),
        ("no_coherence", "coherence_verdict", "coherence-verifier"),
    ]:
        pairs = [
            (full[(c["scenario"], c["repetition"])], c)
            for c in cells
            if c["condition"] == condition and (c["scenario"], c["repetition"]) in full
        ]
        effects[condition] = {
            "paired_cells": len(pairs),
            "changed_verdicts": sum(a[field] != b[field] for a, b in pairs),
            "changed_delivered_outputs": sum(a["output_text"] != b["output_text"] for a, b in pairs),
            "full_verifier_cost_ms": distribution(
                [x["latency_ms"] for a, _ in pairs for x in a["components"] if x["agent_id"] == aid]
            ),
            "ablated_minus_full_latency_ms": distribution(
                [b["metrics"]["latency_ms"]["value"] - a["metrics"]["latency_ms"]["value"] for a, b in pairs]
            ),
            "limitation": "prepared synthetic cases; no causal real-world quality or speed claim",
        }
    return effects


async def run_experiment(protocol: Protocol):
    protocol = Protocol.model_validate(protocol.model_dump())
    jobs = [
        (s, condition, repeat)
        for repeat in range(protocol.repetitions)
        for s in SCENARIOS
        for condition in protocol.conditions
    ]
    random.Random(protocol.seed).shuffle(jobs)
    cells = []
    for scenario, condition, repetition in jobs:
        cells.append(await run_cell(protocol, scenario, condition, repetition))
    human = {
        name: measure(
            None, unit, None, "no consented human pilot collected; synthetic execution is not a human rating"
        )
        for name, unit in [
            ("perceived_utility", "observation"),
            ("ease_of_use", "observation"),
            ("question_quality", "observation"),
            ("explanation_preparation_utility", "observation"),
            ("teacher_review_seconds", "s"),
            ("human_completed_sessions", "count"),
            ("human_abandonments", "count"),
            ("human_session_duration_seconds", "s"),
        ]
    }
    corrections = [c for c in cells if c["transcription"]]
    composition_sets = {}
    for cell in cells:
        family = "defense" if cell["scenario"] == "transcription_correction" else "study"
        composition_sets.setdefault(family, set()).update(
            x["agent_id"]
            for x in cell["components"]
            if x["agent_id"] != "direct-model" and x.get("kind", "agent") == "agent"
        )
    return {
        "schema_version": 1,
        "protocol": protocol.model_dump(),
        "code_manifest": code_manifest(),
        "corpus": [
            {"id": key, "version": 1, "location": "line1", "text": value, "sha256": digest(value.encode())}
            for key, value in CORPUS.items()
        ],
        "scenarios": [s.model_dump(mode="json") for s in SCENARIOS],
        "hardware": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "logical_cpu_count": os.cpu_count(),
            "physical_memory_bytes": psutil.virtual_memory().total,
        },
        "limits": {
            "agent_deadlines": "production contracts, timeout injection 1ms",
            "session_turns": "20, limit scenario 1",
            "session_seconds": 300,
            "retrieval_top_k": [1, 3],
            "model_max_tokens": 256,
            "execution": "sequential seeded random cell order; isolated DB per cell",
            "max_cells": 510,
        },
        "cells": cells,
        "aggregates": aggregate(cells),
        "ablation_effects": paired_effects(cells),
        "human_indicators": human,
        "transcription_metrics": {
            "provisional_records": len(corrections),
            "reviewable_records": sum(c["transcription"]["original_preserved"] for c in corrections),
            "corrected_inputs_used": sum(c["transcription"]["corrected_input_used"] for c in corrections),
            "denominator": len(corrections),
            "source": "real confirmation command with synthetic STT port",
        },
        "reuse": {
            "agency_agent_sets": {key: sorted(value) for key, value in composition_sets.items()},
            "shared_agent_ids": (
                sorted(set.intersection(*composition_sets.values())) if composition_sets else []
            ),
            "source": "observed executed components in study and defense correction probes",
        },
        "comparability": [
            "Deterministic extractive model and lexical fixture ranking; no LLM/Chroma performance "
            "inference.",
            "Baseline uses direct model plus lexical input evidence and pure constitutional rules, "
            "lacks T090 coordination/state changes; no comparable agency trace denominator.",
            "Faults without matching baseline component are not applied there; injection_applied "
            "records this.",
            "Presentation changes purpose; correction uses defense command even in baseline cell, a "
            "shared auxiliary probe, excluded from inference of direct-model speed.",
            "Latency includes DB setup/cleanup; component latency excludes it. RSS is sampled, not "
            "peak. Cold/warm costs may differ.",
            "Synthetic proposals injected equally across conditions; this probes verifiers, not model "
            "error prevalence.",
        ],
        "structural_results": structural(cells),
    }


def render_report(result):
    lines = [
        "# Validación arquitectónica ORAL-IA",
        "",
        "## Observaciones y límites",
        "",
        "No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo "
        "determinista, recuperación lexical; no comparable con un piloto LLM real.",
        "Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son "
        "sesiones humanas completadas.",
        "",
        f"Celdas: {len(result['cells'])}; repeticiones por celda: {result['protocol']['repetitions']}.",
        "",
        "## Métricas observadas",
        "",
        "| Condición | n | Errores | Bloqueos | Timeouts | Recuperaciones | Traza completa | "
        "Latencia media ms |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for condition, a in result["aggregates"].items():
        lines.append(
            f"| {condition} | {a['cells']} | {a['errors']} | {a['blocked']}"
            f" | {a['timeouts']} | {a['recoveries']}"
            f" | {a['fully_traced_turns']}/{a['trace_denominator']}"
            f" | {a['metrics']['latency_ms']['mean']:.3f} |"
        )
    lines += [
        "",
        "JSON incluye n/media/min/max/desviación de cada métrica y latencia por agente. "
        "Desviación ausente con n<2; GPU/tokens y opiniones faltantes con motivo.",
        "",
        "## Por escenario y configuración",
        "",
        "| Escenario | Condición | Repetición | Decisión | Grounding | Coherencia | Error | Recuperación |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in result["cells"]:
        lines.append(
            f"| {c['scenario']} | {c['condition']} | {c['repetition']} | {c['action']}"
            f" | {c['grounding_verdict']} | {c['coherence_verdict']}"
            f" | {c['error']} | {c['recovery']} |"
        )
    lines += ["", "## Efectos pareados de ablación", ""]
    for condition, effect in result["ablation_effects"].items():
        lines.append(
            f"- {condition}: {effect['paired_cells']} pares, "
            f"{effect['changed_verdicts']} veredictos distintos y "
            f"{effect['changed_delivered_outputs']} salidas distintas. "
            f"Coste medio del verificador completo: {effect['full_verifier_cost_ms']['mean']} ms."
        )
    lines += ["", "## Resultados negativos y datos faltantes", ""]
    negatives = [
        c for c in result["cells"] if c["error"] or not c["fully_traced"] and c["condition"] != "baseline"
    ]
    lines.append(
        f"{len(negatives)} celdas de agencia con error o criterio de traza incompleto; "
        "no se ocultan ni cuentan como trazabilidad completa."
    )
    for condition, a in result["aggregates"].items():
        lines.append(
            f"- {condition}: {a['outputs_without_sources']} salidas con texto sin citas entregadas; "
            f"{a['agent_failures']} fallos de agente. Ver cada escenario; "
            "no inferir calidad académica."
        )
    lines += [
        "",
        "No se midieron GPU, tokens reales, utilidad/facilidad/calidad percibida, preparación de "
        "explicaciones ni tiempo docente. CPU/RSS son del proceso completo, no atribución causal "
        "por agente.",
        "",
        "## Comparabilidad",
        "",
    ] + ["- " + s for s in result["comparability"]]
    lines += [
        "",
        "## Inferencias y propuesta de evolución",
        "",
        "Las diferencias de veredicto al retirar un verificador identifican su efecto en estas "
        "fixtures; no estiman frecuencia real de errores. Los controles finales pueden seguir "
        "bloqueando o reconstruyendo la salida, de modo que aprobar grounding no implica entregar "
        "el candidato.",
        "Conservar controles constitucionales/privacidad y verificadores mientras se amplía el "
        "conjunto etiquetado. Medir Ollama/índice real en hardware declarado, separar "
        "calentamiento de ejecución y recoger piloto humano consentido antes de decidir "
        "optimizaciones. Simplificar componentes solo con beneficio medido; no activar cambios "
        "automáticamente.",
        "",
    ]
    return "\n".join(lines)


def write_package(directory: Path, result):
    directory = Path(directory).resolve()
    if directory.exists():
        raise FileExistsError("output directory must be new")
    directory.parent.mkdir(parents=True, exist_ok=True)
    # Build fully before publishing the directory. A failure leaves no final package.
    with TemporaryDirectory(prefix="oralia-package-", dir=directory.parent) as temporary:
        staging = Path(temporary) / "package"
        staging.mkdir()
        for name, value in [("protocol.json", result["protocol"]), ("results.json", result)]:
            (staging / name).write_text(
                json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"
            )
        (staging / "report.md").write_text(render_report(result), encoding="utf-8")
        manifest = {name: digest((staging / name).read_bytes()) for name in FILES}
        (staging / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        staging.rename(directory)


def verify_package(directory: Path):
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError("package symlink is not allowed")
    for name in (*FILES, "manifest.json"):
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise ValueError("invalid package size or file")
    if sum((directory / name).stat().st_size for name in (*FILES, "manifest.json")) > MAX_BYTES:
        raise ValueError("invalid package total size")
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != set(FILES):
        raise ValueError("invalid manifest file allowlist")
    if any(digest((directory / name).read_bytes()) != manifest[name] for name in FILES):
        raise ValueError("package integrity mismatch")
    result = json.loads((directory / "results.json").read_text(encoding="utf-8"))
    protocol = Protocol.model_validate_json((directory / "protocol.json").read_bytes())
    if result["protocol"] != protocol.model_dump() or result["code_manifest"] != code_manifest():
        raise ValueError("code/protocol integrity mismatch")
    if result["scenarios"] != [s.model_dump(mode="json") for s in SCENARIOS] or result["schema_version"] != 1:
        raise ValueError("catalog integrity mismatch")
    return result


async def replay(directory: Path):
    previous = verify_package(directory)
    current = await run_experiment(Protocol.model_validate(previous["protocol"]))
    matched = current["structural_results"] == previous["structural_results"]
    return {
        "matched": matched,
        "cells": len(current["cells"]),
        "comparison": "components, decisions, state, events, evidence; excludes "
        "time/resources/random identifiers",
    }
