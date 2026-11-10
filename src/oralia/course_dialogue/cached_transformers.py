"""Opt-in GenerationPort over an owned local CUDA worker; no public API or fallback."""

import asyncio
import hashlib
import json
import os
import subprocess
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.generation_limits import REPAIR_PROFILE, REPAIR_TEXT_LIMIT, validate_budget_frame
from oralia.course_dialogue.lab_request import LabGenerationRequest, RepairGenerationRequest
from oralia.course_dialogue.model_prompt_profiles import resolve_runtime
from oralia.course_dialogue.owned_worker import OwnedWorkerTree
from oralia.course_dialogue.structured_request import StructuredGenerationRequest
from oralia.infrastructure.generation.generation_port import GenerationError, GenerationOutcome
from oralia.infrastructure.generation.ollama_adapter import _build_user_content

CUDA_PYTHON = Path(os.environ.get("ORALIA_CUDA_PYTHON", r"D:\ai-toolkit\venv\Scripts\python.exe"))
CACHED_MODEL = (
    Path.home()
    / ".cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots"
    / "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
)

CACHED_MODEL_7B = (
    Path.home()
    / ".cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots"
    / "a09a35458c702b33eeacc393d103063234e8bc28"
)

CACHED_MODEL_14B = (
    Path.home()
    / ".cache/huggingface/hub/models--Qwen--Qwen2.5-14B-Instruct/snapshots"
    / "cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8"
)

CACHED_MODEL_QWEN3_8B = (
    Path.home()
    / ".cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots"
    / "b968826d9c46dd6066d109eabc6255188de91218"
)

CACHED_MODEL_MISTRAL_24B = (
    Path.home()
    / ".cache/huggingface/hub/models--mistralai--Mistral-Small-24B-Instruct-2501/snapshots"
    / "9527884be6e5616bdd54de542f9ae13384489724"
)


class CachedTransformersGenerationAdapter:
    def __init__(
        self,
        process,
        model_label="cached-local-candidate",
        *,
        terminate_owned=None,
        message_profile="academic/v1",
        repair_profile_enabled=False,
        model_prompt_profile=None,
        thinking_review_enabled=False,
    ):
        if message_profile not in {"academic/v1", "scope-control/v1"}:
            raise ValueError("unsupported local message profile")
        self.message_profile = message_profile
        self.repair_profile_enabled = repair_profile_enabled
        self.model_prompt_profile = model_prompt_profile
        self.thinking_review_enabled = thinking_review_enabled
        self.process = process
        self.lock = asyncio.Lock()
        self.model_label = model_label
        self.terminate_owned = terminate_owned or process.terminate
        self.usable = True
        # In-memory transport facts for an explicitly requested synthetic diagnostic.
        # The adapter never writes prompts or responses to disk on its own.
        self.last_exchange = None

    async def generate(self, request):
        async with self.lock:
            exchange = {
                "stage": "availability",
                "purpose": request.purpose,
                "deadline_ms": request.constraints.deadline_ms,
                "returncode_before_cleanup": self.process.returncode,
                "raw_worker_response": None,
                "failure_type": None,
                "requested_message_profile": self.message_profile,
            }
            self.last_exchange = exchange
            from oralia.course_dialogue.thinking_review_request import ThinkingReviewRequest

            thinking = isinstance(request, ThinkingReviewRequest)
            if self.model_prompt_profile == "qwen3-8b-thinking" and not thinking:
                raise GenerationError("Thinking checkpoint accepts only typed thinking reviews")
            expanded = isinstance(request, RepairGenerationRequest)
            if expanded:
                if not self.repair_profile_enabled or self.message_profile != "academic/v1":
                    raise GenerationError("Expanded repair requires explicit offline provider opt-in")
                if thinking:
                    if not self.thinking_review_enabled or self.model_prompt_profile != "qwen3-8b-thinking":
                        raise GenerationError("Thinking review requires explicit provider capability")
                    from oralia.course_dialogue.concept_ledger import ThinkingConceptLedgerRequest
                    from oralia.course_dialogue.example_probe import ExampleProbeRequest
                    from oralia.course_dialogue.grounding_review import GroundingReviewRequest
                    from oralia.course_dialogue.web_control_request import WebControlRequest

                    if isinstance(request, GroundingReviewRequest):
                        GroundingReviewRequest.model_validate(request.model_dump())
                    elif isinstance(request, ThinkingConceptLedgerRequest):
                        ThinkingConceptLedgerRequest.model_validate(request.model_dump())
                    elif isinstance(request, WebControlRequest):
                        WebControlRequest.model_validate(request.model_dump())
                    elif isinstance(request, ExampleProbeRequest):
                        ExampleProbeRequest.model_validate(request.model_dump())
                    else:
                        ThinkingReviewRequest.model_validate(request.model_dump())
                else:
                    RepairGenerationRequest.model_validate(request.model_dump())
            capacity = (
                8192
                if thinking
                else 2048 if expanded else 768 if isinstance(request, LabGenerationRequest) else 512
            )
            tokens = request.constraints.max_tokens
            accepted = 1 <= tokens <= capacity
            exchange["token_budget"] = {
                "requested": tokens,
                "effective": tokens if accepted else None,
                "capacity": capacity,
                "status": "accepted" if accepted else "rejected",
                "reason": "within_backend_limit" if accepted else "outside_backend_limit",
            }
            if not accepted:
                exchange["failure_type"] = "unsupported_token_budget"
                raise GenerationError(f"El presupuesto solicitado debe estar entre 1 y {capacity} tokens.")
            if not self.usable or self.process.returncode is not None:
                self.usable = False
                exchange["failure_type"] = "worker_unavailable"
                raise GenerationError("El worker local ya no está disponible.")
            from oralia.course_dialogue.scope_control_messages import (
                ScopeControlRequest,
                build_scope_control_messages,
            )

            effective_profile = "academic/v1"
            structured = isinstance(request, StructuredGenerationRequest)
            if structured:
                if request.model_profile != self.model_prompt_profile:
                    raise GenerationError("Structured request/checkpoint profile mismatch")
                messages = request.effective_messages()
                effective_profile = "structured/v1"
            elif self.message_profile == "scope-control/v1":
                messages = build_scope_control_messages(request)
                effective_profile = (
                    "scope-control-literal/v1"
                    if request.control_step == "literal"
                    else "scope-control-finite/v1"
                )
            else:
                if isinstance(request, ScopeControlRequest):
                    raise ValueError("scope control requires explicit scope-control/v1 adapter profile")
                system = request.instruction
                if request.output_schema is not None:
                    system += "\nEsquema de salida solicitado (no es aprobación):\n" + json.dumps(
                        {
                            key: value
                            for key, value in request.output_schema.items()
                            if key != "x-oralia-finite-outputs"
                        },
                        ensure_ascii=False,
                    )
                messages = [
                    {"role": "system", "content": system},
                    *(m.model_dump() for m in request.conversation_history),
                    {
                        "role": "user",
                        "content": _build_user_content(request.model_copy(update={"student_input": ""}))
                        + "\n<pregunta_actual>"
                        + request.student_input
                        + "</pregunta_actual>",
                    },
                ]
            identifier = str(uuid.uuid4())
            frame = {
                "id": identifier,
                "messages": messages,
                "max_tokens": tokens,
                "deadline_ms": request.constraints.deadline_ms,
                "finite_outputs": finite_json_outputs(request.output_schema),
            }
            if thinking and frame["finite_outputs"] is not None:
                frame["finite_after_thinking"] = True
            if expanded:
                frame["budget_profile"] = "review-thinking/v1" if thinking else REPAIR_PROFILE
                frame["audit_config"] = True
            if structured:
                frame["construction_profile"] = "structured/v1"
                frame["model_prompt_profile"] = self.model_prompt_profile
                frame["prompt_task"] = request.prompt_task
                if request.didactic_profile is not None:
                    frame["didactic_profile"] = request.didactic_profile
                from oralia.course_dialogue.web_review_rounds import WebRoundRequest

                if isinstance(request, WebRoundRequest):
                    frame["web_review_prompt_version"] = request.prompt_version
                    frame["web_review_format_reminder"] = request.format_reminder
                    exchange["requested_web_review_prompt_version"] = request.prompt_version
                from oralia.course_dialogue.model_prompt_profiles import validate_structured_frame

                validate_structured_frame(frame, self.model_prompt_profile)
            validate_budget_frame(
                frame,
                repair_enabled=self.repair_profile_enabled,
                thinking_review_enabled=self.thinking_review_enabled,
            )
            if self.message_profile == "scope-control/v1":
                frame["message_profile"] = effective_profile
            exchange["effective_message_profile"] = effective_profile
            try:
                exchange["stage"] = "send"
                self.process.stdin.write((json.dumps(frame, ensure_ascii=False) + "\n").encode())
                await self.process.stdin.drain()
            except asyncio.CancelledError:
                self.usable = False
                exchange.update(failure_type="cancelled", returncode_before_cleanup=self.process.returncode)
                if self.process.returncode is None:
                    self.terminate_owned()
                raise
            except (BrokenPipeError, ConnectionResetError):
                self.usable = False
                exchange.update(failure_type="pipe_closed", returncode_before_cleanup=self.process.returncode)
                if self.process.returncode is None:
                    self.terminate_owned()
                raise GenerationError("El canal del worker local está cerrado.") from None
            try:
                exchange["stage"] = "read"
                line = await asyncio.wait_for(
                    self.process.stdout.readline(), timeout=request.constraints.deadline_ms / 1000 + 2
                )
            except asyncio.CancelledError:
                self.usable = False
                exchange.update(failure_type="cancelled", returncode_before_cleanup=self.process.returncode)
                if self.process.returncode is None:
                    self.terminate_owned()
                raise
            except TimeoutError:
                self.usable = False
                exchange.update(
                    failure_type="read_timeout", returncode_before_cleanup=self.process.returncode
                )
                if self.process.returncode is None:
                    self.terminate_owned()
                raise GenerationError(
                    "El worker local agotó el plazo; no se reutiliza una respuesta tardía."
                ) from None
            if not line:
                self.usable = False
                exchange.update(failure_type="eof", returncode_before_cleanup=self.process.returncode)
                if self.process.returncode is None:
                    self.terminate_owned()
                raise GenerationError("El worker local terminó sin respuesta.")
            exchange["raw_worker_response"] = line.decode("utf-8", errors="replace").rstrip("\r\n")
            try:
                exchange["stage"] = "parse"
                result = json.loads(line)
                if not isinstance(result, dict):
                    raise ValueError("worker frame must be an object")
            except (ValueError, UnicodeDecodeError):
                self.usable = False
                exchange.update(
                    failure_type="invalid_frame", returncode_before_cleanup=self.process.returncode
                )
                if self.process.returncode is None:
                    self.terminate_owned()
                raise GenerationError("Respuesta del worker local fuera de protocolo.") from None
            if result.get("id") != identifier:
                self.usable = False
                exchange.update(failure_type="wrong_id", returncode_before_cleanup=self.process.returncode)
                if self.process.returncode is None:
                    try:
                        self.terminate_owned()
                    except ProcessLookupError:
                        pass
                raise GenerationError("Respuesta local fuera de secuencia; worker descartado.")
            if result.get("type") != "result":
                exchange["failure_type"] = "worker_error_frame"
                raise GenerationError(
                    "El worker local rechazó la petición: " + result.get("error_type", "unknown")
                )
            if expanded and result.get("budget_profile") != (
                "review-thinking/v1" if thinking else REPAIR_PROFILE
            ):
                self.usable = False
                self.terminate_owned()
                raise GenerationError("Worker did not confirm expanded repair profile")
            if structured and (
                result.get("construction_profile") != "structured/v1"
                or result.get("model_prompt_profile") != self.model_prompt_profile
            ):
                self.usable = False
                self.terminate_owned()
                raise GenerationError("Worker did not confirm structured renderer")
            if "web_review_prompt_version" in frame:
                digest = hashlib.sha256(
                    json.dumps(messages, ensure_ascii=False, sort_keys=True).encode("utf8")
                ).hexdigest()
                if (
                    result.get("web_review_prompt_version") != frame["web_review_prompt_version"]
                    or type(result.get("web_review_format_reminder")) is not bool
                    or result["web_review_format_reminder"] != frame["web_review_format_reminder"]
                    or result.get("web_review_messages_sha256") != digest
                ):
                    self.usable = False
                    self.terminate_owned()
                    raise GenerationError("Worker did not confirm web review renderer")
                exchange["confirmed_web_review_prompt_version"] = result["web_review_prompt_version"]
                exchange["confirmed_web_review_messages_sha256"] = digest
            thinking_meta = None
            if thinking:
                from oralia.course_dialogue.qwen_thinking import validate_thinking_result

                try:
                    thinking_meta = validate_thinking_result(result)
                except ValueError as error:
                    self.usable = False
                    self.terminate_owned()
                    raise GenerationError(str(error)) from error
                exchange["thinking_output"] = thinking_meta
            if expanded and len(result["text"]) > REPAIR_TEXT_LIMIT:
                self.usable = False
                self.terminate_owned()
                raise GenerationError("Expanded repair exceeds text capacity; no clipping")
            exchange["stage"] = "complete"
            exchange["confirmed_message_profile"] = result.get("message_profile")
            if (
                self.message_profile == "scope-control/v1"
                and result.get("message_profile") != effective_profile
            ):
                exchange["failure_type"] = "wrong_message_profile"
                self.usable = False
                exchange["returncode_before_cleanup"] = self.process.returncode
                if self.process.returncode is None:
                    self.terminate_owned()
                raise GenerationError("El worker no confirmó el perfil de control solicitado.")
            observed = (result.get("generation_state") or {}).get("explicit_generate_kwargs", {})
            sampling_parameters = {}
            if self.model_prompt_profile is not None:
                sampling_parameters["do_sample"] = int(observed.get("do_sample", False))
                if type(result.get("generation_seed")) is int:
                    sampling_parameters["seed"] = result["generation_seed"]
            return GenerationOutcome(
                ok=result["finish_reason"] == "stop"
                and (thinking_meta is None or thinking_meta["status"] == "separated"),
                text=result["text"],
                adapter="transformers_local",
                model=self.model_label,
                finish_reason=result["finish_reason"],
                parameters={
                    "max_tokens": frame["max_tokens"],
                    "requested_max_tokens": tokens,
                    "max_tokens_capacity": capacity,
                    "temperature": observed.get("temperature", 0),
                    **sampling_parameters,
                    "input_tokens": result["input_tokens"],
                    "output_tokens": result["output_tokens"],
                    "cuda_graph_decoder": int(result.get("decoder") == "cuda_graph/v1"),
                    "finite_decoder": result.get("finite_decoder", False),
                    "finite_after_thinking": result.get("finite_after_thinking", False),
                    **(
                        {
                            "thinking_enabled": 1,
                            "reasoning_tokens": thinking_meta["reasoning_tokens"],
                            "final_tokens": thinking_meta["final_tokens"],
                        }
                        if thinking_meta
                        else {}
                    ),
                },
                latency_ms=result["latency_ms"],
            )


@asynccontextmanager
async def cached_provider(
    output,
    python=CUDA_PYTHON,
    source=CACHED_MODEL,
    quantization=None,
    enable_thinking=None,
    tokenizer_fix=None,
    message_profile="academic/v1",
    preparation_seconds=90,
    repair_profile_enabled=False,
    model_prompt_profile=None,
    sampling_profile="greedy/v1",
    generation_seed=42,
    thinking_review_enabled=False,
    release_cuda_cache=False,
    graph_decoder=True,
):
    if type(graph_decoder) is not bool:
        raise ValueError("Graph decoder switch must be an explicit boolean")
    if type(release_cuda_cache) is not bool:
        raise ValueError("CUDA handoff must be an explicit boolean")
    if type(preparation_seconds) is not int or not 1 <= preparation_seconds <= 180:
        raise ValueError("Preparation budget must be an explicit integer in1..180seconds")
    if message_profile not in {"academic/v1", "scope-control/v1"}:
        raise ValueError("unsupported local message profile")
    if not python.is_file() or not (source / "config.json").is_file():
        raise ValueError("Falta runtimeGPU/modelo ya preparado; no se descargará nada.")
    if model_prompt_profile is not None:
        runtime_profile = resolve_runtime(source, model_prompt_profile, sampling_profile, generation_seed)
        from oralia.course_dialogue.qwen_thinking import thinking_selection

        enable_thinking = thinking_selection(runtime_profile, enable_thinking, thinking_review_enabled)
        if tokenizer_fix not in {None, runtime_profile["tokenizer_fix"]}:
            raise ValueError("Tokenizer fix incompatible with checkpoint profile")
        tokenizer_fix = runtime_profile["tokenizer_fix"]
    elif sampling_profile != "greedy/v1":
        raise ValueError("Sampling requires an explicit registered checkpoint profile")
    if model_prompt_profile is None:
        from oralia.course_dialogue.qwen_thinking import thinking_selection

        enable_thinking = thinking_selection(None, enable_thinking, thinking_review_enabled)
    env = {
        k: v
        for k, v in os.environ.items()
        if k.upper()
        in {
            "SYSTEMROOT",
            "PATH",
            "TEMP",
            "TMP",
            "USERPROFILE",
            "HOME",
            "LOCALAPPDATA",
            "APPDATA",
            "PROGRAMFILES",
            "NUMBER_OF_PROCESSORS",
            "PROCESSOR_ARCHITECTURE",
        }
    }
    env.update(
        {
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "NO_PROXY": "127.0.0.1,localhost",
            "HTTP_PROXY": "http://127.0.0.1:9",
            "HTTPS_PROXY": "http://127.0.0.1:9",
        }
    )
    started = time.monotonic()
    with (output / "worker-stderr.log").open("wb") as stderr:
        process = await asyncio.create_subprocess_exec(
            str(python),
            "-X",
            "utf8",
            str(Path(__file__).with_name("gpu_worker.py")),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=stderr,
            limit=262144,
            env=env,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        owned = None
        try:
            owned = OwnedWorkerTree(process.pid)
            process.stdin.write(
                (
                    json.dumps(
                        {
                            "source": str(source),
                            "quantization": quantization,
                            "enable_thinking": enable_thinking,
                            "tokenizer_fix": tokenizer_fix,
                            "repair_profile_enabled": repair_profile_enabled,
                            "thinking_review_enabled": thinking_review_enabled,
                            "model_prompt_profile": model_prompt_profile,
                            "sampling_profile": sampling_profile,
                            "generation_seed": generation_seed,
                            "release_cuda_cache": release_cuda_cache,
                            "graph_decoder": graph_decoder,
                        }
                    )
                    + "\n"
                ).encode()
            )
            await process.stdin.drain()
            (output / "worker-ownership.json").write_text(
                json.dumps({"pid": process.pid, "python": str(python), "source": str(source)}),
                encoding="utf-8",
            )
            task = asyncio.create_task(process.stdout.readline())
            try:
                for tick in range((preparation_seconds + 9) // 10):
                    done, _ = await asyncio.wait({task}, timeout=min(10, preparation_seconds - tick * 10))
                    if done:
                        break
                    print(f"[ESPERA] Preparación del modelo local: {(tick+1)*10}s transcurridos.", flush=True)
                if not task.done():
                    raise TimeoutError(
                        f"El modelo local no confirmó disponibilidad en{preparation_seconds}s."
                    )
                ready = json.loads(task.result())
            finally:
                if not task.done():
                    task.cancel()
            if ready.get("type") != "ready":
                (output / "preparation-refusal.json").write_text(json.dumps(ready), encoding="utf-8")
                raise GenerationError("El runtimeGPU no está disponible: " + ready.get("reason", "unknown"))
            (output / "worker.json").write_text(
                json.dumps(
                    {
                        **ready,
                        "pid": process.pid,
                        "python": str(python),
                        "source": str(source),
                        "ready_seconds": time.monotonic() - started,
                        "no_listener": True,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            owned.capture()
            if model_prompt_profile is not None and ready.get("model_prompt_profile") != model_prompt_profile:
                raise GenerationError("Worker checkpoint prompt identity not confirmed")
            if repair_profile_enabled and REPAIR_PROFILE not in ready.get("budget_profiles", []):
                raise GenerationError("Worker lacks explicit expanded repair capability")
            if thinking_review_enabled and (
                ready.get("enable_thinking") is not True
                or "review-thinking/v1" not in ready.get("budget_profiles", [])
            ):
                raise GenerationError("Thinking review capability not confirmed")
            if message_profile == "scope-control/v1" and not {
                "scope-control-finite/v1",
                "scope-control-literal/v1",
            }.issubset(set(ready.get("message_profiles", []))):
                raise GenerationError("El worker no soporta los perfiles explícitos de control.")
            yield CachedTransformersGenerationAdapter(
                process,
                source.parent.parent.name
                + "@"
                + source.name[:8]
                + ("/" + quantization if quantization else "/bf16"),
                terminate_owned=owned.terminate,
                message_profile=message_profile,
                repair_profile_enabled=repair_profile_enabled,
                model_prompt_profile=model_prompt_profile,
                thinking_review_enabled=thinking_review_enabled,
            )
        finally:
            if owned is not None:
                owned.capture()
            if process.returncode is None:
                try:
                    process.stdin.write(b'{"type":"stop"}\n')
                    await process.stdin.drain()
                    await asyncio.wait_for(process.wait(), timeout=10)
                except (TimeoutError, BrokenPipeError, ConnectionResetError):
                    if process.returncode is None:
                        if owned is not None:
                            owned.terminate()
                        else:
                            process.terminate()
                    await process.wait()
            identities = await asyncio.to_thread(owned.finish) if owned is not None else []
            (output / "worker-cleanup.json").write_text(
                json.dumps(
                    {
                        "pid": process.pid,
                        "returncode": process.returncode,
                        "own_process_stopped": process.returncode is not None,
                        "owned_processes": identities,
                        "owned_tree_stopped": bool(identities) and all(p["stopped"] for p in identities),
                    }
                ),
                encoding="utf-8",
            )
