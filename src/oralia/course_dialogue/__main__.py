"""Review unapproved candidates locally, never impersonate a participant service."""

import argparse
import asyncio
import json
import os
import uuid
from pathlib import Path

from oralia.course_dialogue.corpus import SemanticCatalog, load_catalog
from oralia.course_dialogue.local_provider import owned_provider
from oralia.course_dialogue.runtime import propose
from oralia.course_study.__main__ import WORKSPACE, _no_alias, owned_lock


def lab_root(workspace):
    _no_alias(workspace)
    workspace = Path(workspace).resolve()
    root = workspace / ".oralia-course-dialogue-lab"
    _no_alias(root)
    marker = {"kind": "oralia-candidate-inspection", "version": 1, "workspace": str(workspace)}
    if root.exists():
        for directory, directories, files in os.walk(root, followlinks=False):
            for name in directories + files:
                _no_alias(Path(directory) / name)
        if json.loads((root / "marker.json").read_text(encoding="utf-8")) != marker:
            raise ValueError("Entorno sin marcador propio; no se modifica.")
    else:
        root.mkdir()
        (root / "marker.json").write_text(json.dumps(marker), encoding="utf-8")
    return root


async def inspect_loop(
    catalog, read=input, write=print, *, natural_probe=False, provider=None, inference_deadline_ms=6000
):
    history = []
    write("BANCO DE CANDIDATAS NO APROBADAS. No es una sesión de participante ni un tutor habilitado.")
    write("Solo preguntas ficticias de evaluación. G2/G3/G4 pendientes. No se conservan estas entradas.")
    write("/fuentes enumera páginas; /salir detiene solo el proceso propio. Máximo30turnos.")
    for _ in range(30):
        try:
            text = read("Pregunta de evaluación: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text == "/salir":
            break
        if text == "/fuentes":
            for r in catalog:
                write(f"{r['id']}: {r['filename']}, página original {r['page']}, versión1.")
            continue
        if not text:
            continue
        if len(text) > 4000:
            write("Pregunta demasiado extensa; máximo4000caracteres.")
            continue
        try:
            row = await propose(
                catalog,
                text,
                history,
                provider,
                structured=not natural_probe,
                inference_deadline_ms=inference_deadline_ms,
            )
        except Exception as exc:
            row = {
                "input": text,
                "raw_candidate": None,
                "error": type(exc).__name__,
                "displayed_text": "No se obtuvo una respuesta completa. Puedes reformular la pregunta.",
                "display_kind": "operational",
                "publication_allowed": False,
            }
        history.append(row)
        write(
            "CANDIDATA DE LABORATORIO — publicación no autorizada:"
            if row.get("display_kind") == "candidate"
            else "ESTADO OPERATIVO DEL LABORATORIO:"
        )
        if row.get("displayed_text"):
            write(row["displayed_text"])
            if row.get("parsed_candidate"):
                for segment in row["parsed_candidate"].get("segments", []):
                    write("Referencia propuesta: " + segment["source_id"])
        else:
            write("Sin candidata completa para mostrar. Revise el diagnóstico técnico si procede.")
        write(
            "Comprobación: "
            + json.dumps(
                row.get("verification", {"error": row.get("error"), "publication_allowed": False}),
                ensure_ascii=False,
            )
        )
    write(
        "Inspección finalizada; entradas/candidatas descartadas de memoria. No hubo publicación participante."
    )


async def inspect_drafts(curriculum, provider, read=input, write=print, *, semantic_version=1, on_event=None):
    """Synthetic, memory-only preview; never creates a participant session."""
    import time
    from dataclasses import asdict

    from oralia.course_dialogue.draft_dialogue import DraftState
    from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
    from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    planner = LocalSemanticPlanner(provider)
    agent = StudyIntentInterpreterAgent(semantic_planner=planner, semantic_version=semantic_version)
    state = DraftState()
    last = None
    last_sources = []
    session = uuid.uuid4()

    def event(value):
        if on_event is not None:
            on_event(value)

    write("BORRADORES CONTROLADOS NO APROBADOS. Inspección sintética, sin sesión participante.")
    write(
        "Captura sintética explícita activada." if on_event is not None else "No se conservan estas entradas."
    )
    write(
        "El modelo propone objetivo/acto; el texto procede de unidades "
        "redactadas técnicamente y pendientes de revisión docente."
    )
    write(
        "/fuentes muestra referencias del último borrador; /estado "
        "muestra objetivo y pregunta pendiente; /salir termina. "
        "Máximo30turnos."
    )
    write("Inferencia local: límite30s por propuesta. G2/G3/G4 y utilidad humana pendientes.")
    for _ in range(30):
        try:
            text = read("Pregunta ficticia: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        event({"event": "input", "text": text})
        if text == "/salir":
            break
        if text == "/fuentes":
            refs = last_sources
            if not refs:
                write("Todavía no se ha mostrado un borrador con fuentes.")
            for ref in refs:
                write(f"{ref['filename']}, página original {ref['page']}, versión{ref['version']}.")
            continue
        if text == "/estado":
            write(json.dumps(asdict(state), ensure_ascii=False))
            continue
        if not text:
            continue
        if len(text) > 4000:
            write("Pregunta demasiado extensa; máximo4000caracteres.")
            continue
        pending = next(
            (u["draft_content"] for u in curriculum.units if u["id"] == state.pending_question_id), None
        )
        request = AgentRequest(
            session_id=session,
            turn_id=uuid.uuid4(),
            deadline_ms=30000,
            input={
                "semantic_planning_version": semantic_version,
                "text": text,
                "goals": curriculum.goals,
                "correction_options": curriculum.corrections,
                "relations": curriculum.relations,
                "context": {
                    **asdict(state),
                    "pending_question_text": pending,
                    "last_actual_preview": (last or {}).get("candidate_text"),
                },
            },
        )
        before = asdict(state)
        event({"event": "before_planning", "request": request.model_dump(mode="json")})
        planner.last_trace = None
        task = asyncio.create_task(agent.execute(request, CancellationToken()))
        started = time.monotonic()
        try:
            while not task.done():
                done, _ = await asyncio.wait({task}, timeout=5)
                if not done:
                    write(f"[ESPERA] Propuesta local: {int(time.monotonic()-started)}s transcurridos.")
            result = await task
        finally:
            if not task.done():
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        event(
            {
                "event": "planning_result",
                "result": result.model_dump(mode="json"),
                "raw_trace": planner.last_trace,
                "state_before": before,
                "elapsed_seconds": time.monotonic() - started,
            }
        )
        if result.status != "ok":
            write("No se obtuvo un plan válido; el estado se conserva. Puede concretar la duda o salir.")
            continue
        try:
            actual, next_state = curriculum.render_preview(
                result.output["semantic_plan"], state, current_input=text
            )
        except ValueError as exc:
            event(
                {"event": "preview_rejected", "error_type": type(exc).__name__, "state_after": asdict(state)}
            )
            write("La propuesta no cumple las restricciones del borrador; el estado se conserva.")
            continue
        last = actual
        if actual.get("source_refs"):
            last_sources = actual["source_refs"]
        state = next_state
        event(
            {
                "event": "actual_preview",
                "preview": actual,
                "state_before": before,
                "state_after": asdict(state),
            }
        )
        write("BORRADOR TÉCNICO — publicación no autorizada:")
        write(actual["candidate_text"])
    write(
        (
            "Inspección finalizada; captura sintética conservada. "
            if on_event is not None
            else "Inspección finalizada; entradas descartadas. "
        )
        + "No hubo publicación participante."
    )
    event(
        {
            "event": "inspection_closed",
            "state": asdict(state),
            "participant_publication": False,
            "participant_session": False,
        }
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspección técnica de candidatas; no tutor aprobado.")
    parser.add_argument("--inspect-candidates", action="store_true", required=True)
    parser.add_argument("--natural-probe", action="store_true")
    parser.add_argument("--controlled-drafts", action="store_true")
    parser.add_argument("--draft-model", choices=["7b-nf4", "14b-nf4"], default=None)
    parser.add_argument("--semantic-version", type=int, choices=[1, 2, 3, 4, 5, 6, 7], default=1)
    parser.add_argument("--provider", choices=["cached-cuda", "ollama"], default="cached-cuda")
    parser.add_argument("--port", type=int, default=None)
    args = parser.parse_args(argv)
    if not args.controlled_drafts and (args.draft_model is not None or args.semantic_version != 1):
        parser.error("El modelo/contrato de borradores solo se elige con --controlled-drafts.")
    if args.controlled_drafts and (args.natural_probe or args.provider != "cached-cuda"):
        parser.error("Los borradores controlados requieren cached-cuda y no son una sonda de texto libre.")
    if args.port is not None and not 1024 <= args.port <= 65535:
        raise ValueError("Puerto explícito fuera de rango.")
    if args.provider == "cached-cuda" and args.port is not None:
        raise ValueError("El workerCUDA no abre puertos; quite --port o elija ollama.")
    root = lab_root(WORKSPACE)
    with owned_lock(root):
        run = root / str(uuid.uuid4())
        run.mkdir()
        print("Comprobando fuentes originales y proveedor propio; la carga inicial puede tardar.", flush=True)
        catalog = None if args.controlled_drafts else SemanticCatalog(load_catalog())
        if args.provider == "cached-cuda":
            from oralia.course_dialogue.cached_transformers import (
                CACHED_MODEL,
                CACHED_MODEL_7B,
                CACHED_MODEL_14B,
                cached_provider,
            )
            from oralia.course_dialogue.draft_dialogue import DraftCurriculum

            curriculum = DraftCurriculum() if args.controlled_drafts else None

            async def run_cached():
                async with cached_provider(
                    run,
                    source=(
                        (CACHED_MODEL_14B if args.draft_model == "14b-nf4" else CACHED_MODEL_7B)
                        if args.controlled_drafts
                        else CACHED_MODEL
                    ),
                    quantization="nf4" if args.controlled_drafts else None,
                ) as provider:
                    if args.controlled_drafts:
                        await inspect_drafts(curriculum, provider, semantic_version=args.semantic_version)
                    else:
                        print("Inferencia de candidatas: límite explícito30s por petición.", flush=True)
                        await inspect_loop(
                            catalog,
                            natural_probe=args.natural_probe,
                            provider=provider,
                            inference_deadline_ms=30000,
                        )

            asyncio.run(run_cached())
        else:
            with owned_provider(run, args.port or 11436) as url:
                for key in list(os.environ):
                    if key.startswith(("ORALIA_", "VITE_")):
                        del os.environ[key]
                os.environ.update(
                    {
                        "ORALIA_OLLAMA_BASE_URL": url,
                        "ORALIA_OLLAMA_MODEL": "qwen2.5:0.5b",
                        "ORALIA_OLLAMA_TIMEOUT_MS": "6000",
                        "ORALIA_OLLAMA_MAX_TOKENS": "512",
                        "ORALIA_OLLAMA_TEMPERATURE": "0.2",
                        "NO_PROXY": "127.0.0.1,localhost",
                    }
                )
                asyncio.run(inspect_loop(catalog, natural_probe=args.natural_probe))

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelado; limpieza solo del proveedor propio.")
        raise SystemExit(130) from None
    except Exception as exc:
        print(f"Banco no disponible ({type(exc).__name__}): {exc}")
        raise SystemExit(2) from None
