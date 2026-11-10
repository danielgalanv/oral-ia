"""Standalone pipe worker for an already installed CUDA Python.

Run only through cached_transformers; sources/prompts travel through stdin, never
command arguments. Registered web frames load pure request types for validation,
not application services. stdout is a JSON protocol, not participant publication.
"""

import hashlib
import json
import os
import sys
import time
from pathlib import Path


def patch_mistral_regex(tokenizer):
    """Apply the installed Transformers intended regex in memory to its raw Tokenizer."""
    import tokenizers

    backend = tokenizer.backend_tokenizer
    state = json.loads(backend.pre_tokenizer.__getstate__())
    if (
        state.get("type") != "Sequence"
        or len(state.get("pretokenizers", [])) != 2
        or state["pretokenizers"][0].get("type") != "Split"
        or state["pretokenizers"][1]
        != {"type": "ByteLevel", "add_prefix_space": False, "trim_offsets": True, "use_regex": False}
    ):
        raise ValueError("Mistral pre-tokenizer shape changed; no local patch applied.")
    pattern = (
        r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+|"
        r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*|"
        r"\p{N}| ?[^\s\p{L}\p{N}]+[\r\n/]*|\s*[\r\n]+|\s+(?!\S)|\s+"
    )
    backend.pre_tokenizer = tokenizers.pre_tokenizers.Sequence(
        [
            tokenizers.pre_tokenizers.Split(pattern=tokenizers.Regex(pattern), behavior="isolated"),
            tokenizers.pre_tokenizers.ByteLevel(add_prefix_space=False, trim_offsets=True, use_regex=False),
        ]
    )
    patched = json.loads(backend.pre_tokenizer.__getstate__())
    if patched["pretokenizers"][0]["pattern"] != {"Regex": pattern}:
        raise ValueError("Mistral regex correction not confirmed.")


def main():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    import graph_decoder as graph_module
    import torch
    import transformers
    from generation_observability import generation_snapshot
    from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList

    config = json.loads(sys.stdin.readline())
    from generation_limits import REPAIR_PROFILE, REPAIR_TEXT_LIMIT, validate_budget_frame

    repair_enabled = config.get("repair_profile_enabled") is True
    from model_prompt_profiles import native_tokens, resolve_runtime, validate_structured_frame

    model_prompt_profile = config.get("model_prompt_profile")
    runtime_profile = None
    if model_prompt_profile is not None:
        runtime_profile = resolve_runtime(
            config["source"],
            model_prompt_profile,
            config.get("sampling_profile", "greedy/v1"),
            config.get("generation_seed", 42),
        )
    source = config["source"]
    from qwen_thinking import split_thinking_output, thinking_selection

    thinking_review_enabled = config.get("thinking_review_enabled", False)
    enable_thinking = thinking_selection(
        runtime_profile, config.get("enable_thinking"), thinking_review_enabled
    )
    if config.get("enable_thinking") != enable_thinking:
        raise ValueError("Explicit thinking mode not confirmed in configuration")
    chat_options = {"enable_thinking": enable_thinking} if enable_thinking is not None else {}
    if runtime_profile is not None and chat_options != runtime_profile["chat_options"]:
        raise ValueError("Explicit checkpoint/thinking configuration mismatch")
    if not torch.cuda.is_available():
        raise RuntimeError("El runtime elegido no dispone de CUDA.")
    started = time.monotonic()
    free, total = torch.cuda.mem_get_info()
    weights = sum(p.stat().st_size for p in Path(source).glob("*.safetensors"))
    quantization = config.get("quantization")
    tokenizer_fix = config.get("tokenizer_fix")
    if runtime_profile is not None and tokenizer_fix != runtime_profile["tokenizer_fix"]:
        raise ValueError("Checkpoint/tokenizer correction mismatch")
    if tokenizer_fix not in {None, "mistral_regex_local"}:
        raise ValueError("Unknown tokenizer correction")
    if tokenizer_fix == "mistral_regex_local":
        model_config = json.loads((Path(source) / "config.json").read_text(encoding="utf-8"))
        if model_config.get("model_type") != "mistral":
            raise ValueError("Mistral regex correction requested for a non-Mistral model")
    if quantization not in {None, "nf4"}:
        raise ValueError("Cuantización no registrada.")
    estimate = int(weights * (0.45 if quantization == "nf4" else 1.15) + 1024**3)
    if free < estimate:
        print(
            json.dumps(
                {
                    "type": "unavailable",
                    "reason": "insufficient_gpu_memory",
                    "free_bytes": free,
                    "estimated_required_bytes": estimate,
                }
            ),
            flush=True,
        )
        return 2
    print(
        json.dumps(
            {"stage": "loading_local_weights", "free_bytes": free, "estimated_required_bytes": estimate}
        ),
        file=sys.stderr,
        flush=True,
    )
    tokenizer_options = {"fix_mistral_regex": False} if tokenizer_fix == "mistral_regex_local" else {}
    tokenizer = AutoTokenizer.from_pretrained(
        source, local_files_only=True, trust_remote_code=False, **tokenizer_options
    )
    if tokenizer_fix == "mistral_regex_local":
        patch_mistral_regex(tokenizer)
    kwargs = {}
    if quantization == "nf4":
        from transformers import BitsAndBytesConfig

        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
    model = AutoModelForCausalLM.from_pretrained(
        source,
        dtype=torch.bfloat16,
        device_map="cuda",
        local_files_only=True,
        trust_remote_code=False,
        **kwargs,
    )
    model.eval()
    print(
        json.dumps(
            {
                "stage": "weights_loaded",
                "elapsed_seconds": time.monotonic() - started,
                "device": str(next(model.parameters()).device),
            }
        ),
        file=sys.stderr,
        flush=True,
    )
    warm = tokenizer(
        tokenizer.apply_chat_template(
            [{"role": "user", "content": "Responde únicamente listo."}],
            tokenize=False,
            add_generation_prompt=True,
            **chat_options,
        ),
        return_tensors="pt",
    ).to("cuda")
    with torch.inference_mode():
        model.generate(**warm, max_new_tokens=1, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    graph_decoder = None
    if (
        config.get("graph_decoder", True) is True
        and model.config.model_type in graph_module.SUPPORTED_MODEL_TYPES
    ):
        eos = model.generation_config.eos_token_id
        eos_ids = [eos] if isinstance(eos, int) else list(eos or [])
        if tokenizer.eos_token_id is not None:
            eos_ids.append(tokenizer.eos_token_id)
        graph_decoder = graph_module.GraphDecoder(torch, model, eos_ids)
        try:
            graph_module.install_gqa_decode_attention(torch, model)
        except Exception as exc:  # stock attention stays; only slower on long contexts
            print(
                json.dumps(
                    {
                        "stage": "gqa_attention_unavailable",
                        "error": type(exc).__name__ + ": " + str(exc)[:300],
                    }
                ),
                file=sys.stderr,
                flush=True,
            )
        prewarm_started = time.monotonic()
        try:
            graph_decoder.prewarm()
            print(
                json.dumps({"stage": "graph_decoder_ready", "seconds": time.monotonic() - prewarm_started}),
                file=sys.stderr,
                flush=True,
            )
        except Exception as exc:  # no graph decoding for this process; generate stays available
            print(
                json.dumps(
                    {
                        "stage": "graph_decoder_unavailable",
                        "error": type(exc).__name__ + ": " + str(exc)[:300],
                    }
                ),
                file=sys.stderr,
                flush=True,
            )
            graph_decoder = None
    print(
        json.dumps(
            {
                "type": "ready",
                "torch": torch.__version__,
                "transformers": transformers.__version__,
                "gpu": torch.cuda.get_device_name(0),
                "load_seconds": time.monotonic() - started,
                "graph_decoder_available": graph_decoder is not None,
                "structured_decoder": False,
                "schema_hint_only": True,
                "finite_enum_decoder_supported": True,
                "finite_json_decoder_max_outputs": 256,
                "enable_thinking": enable_thinking,
                "quantization": quantization,
                "tokenizer_fix": tokenizer_fix,
                "weight_bytes": weights,
                "effective_chat_template": tokenizer.chat_template,
                "effective_chat_template_sha256": hashlib.sha256(
                    json.dumps(tokenizer.chat_template, ensure_ascii=False, sort_keys=True).encode()
                ).hexdigest(),
                "chat_options": chat_options,
                "effective_model_class": type(model).__name__,
                "effective_tokenizer_class": type(tokenizer).__name__,
                "memory_footprint_bytes": model.get_memory_footprint(),
                "message_profiles": ["academic/v1", "scope-control-finite/v1", "scope-control-literal/v1"],
                "budget_profiles": ["historical/v1"]
                + ([REPAIR_PROFILE] if repair_enabled else [])
                + (["review-thinking/v1"] if thinking_review_enabled else []),
                "generation_state": generation_snapshot(model, tokenizer),
                "model_prompt_profile": model_prompt_profile,
                "runtime_prompt_profile": runtime_profile,
            }
        ),
        flush=True,
    )
    for line in sys.stdin:
        frame = json.loads(line)
        if frame.get("type") == "stop":
            break
        budget_profile = validate_budget_frame(
            frame, repair_enabled=repair_enabled, thinking_review_enabled=thinking_review_enabled
        )
        started = time.monotonic()
        deadline = started + frame["deadline_ms"] / 1000

        class Deadline(StoppingCriteria):
            def __call__(self, input_ids, scores, deadline=deadline, **kwargs):
                return time.monotonic() >= deadline

        try:
            from scope_message_profiles import validate_frame_profile

            message_profile = validate_frame_profile(frame)
            structured = frame.get("construction_profile") == "structured/v1"
            if frame.get("construction_profile") not in {None, "structured/v1"}:
                raise ValueError("Unknown construction profile")
            if structured:
                if runtime_profile is None or frame.get("model_prompt_profile") != model_prompt_profile:
                    raise ValueError("Unbound structured checkpoint")
                validate_structured_frame(frame, model_prompt_profile)
                message_profile = "structured/v1"
                prompt, _ = native_tokens(tokenizer, frame["messages"], chat_options)
                inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to("cuda")
            else:
                prompt = tokenizer.apply_chat_template(
                    frame["messages"], tokenize=False, add_generation_prompt=True, **chat_options
                )
                inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
            input_length = inputs["input_ids"].shape[-1]
            if input_length > 7000:
                raise ValueError("Contexto del banco excede7000tokens; no se truncó silenciosamente.")
            finite_outputs = frame.get("finite_outputs")
            generation_options = {}
            if finite_outputs is not None:
                from finite_schema import allowed_next_tokens, allowed_thinking_tokens

                if (
                    not isinstance(finite_outputs, list)
                    or not 1 <= len(finite_outputs) <= 256
                    or any(not isinstance(text, str) or len(text) > 512 for text in finite_outputs)
                ):
                    raise ValueError("Invalid finite alternatives")
                sequences = [tokenizer.encode(text, add_special_tokens=False) for text in finite_outputs]

                def allowed(
                    batch_id,
                    input_ids,
                    sequences=sequences,
                    input_length=input_length,
                    eos_token_id=tokenizer.eos_token_id,
                    finite_after_thinking=frame.get("finite_after_thinking"),
                ):
                    if finite_after_thinking is True:
                        if enable_thinking is not True:
                            raise ValueError("Finite thinking requires thinking mode")
                        return allowed_thinking_tokens(
                            sequences,
                            input_ids[input_length:].tolist(),
                            eos_token_id,
                            model.config.vocab_size,
                            tokenizer.convert_tokens_to_ids("</think>"),
                        )
                    return allowed_next_tokens(sequences, input_ids[input_length:].tolist(), eos_token_id)

                generation_options["prefix_allowed_tokens_fn"] = allowed
            generation_state = None
            sample_options = runtime_profile["generate_kwargs"] if runtime_profile else {"do_sample": False}
            if runtime_profile is not None:
                torch.manual_seed(runtime_profile["seed"])
                torch.cuda.manual_seed_all(runtime_profile["seed"])
            if frame.get("audit_config") is True:
                generation_state = generation_snapshot(
                    model,
                    tokenizer,
                    {
                        "max_new_tokens": frame["max_tokens"],
                        **sample_options,
                        "pad_token_id": tokenizer.eos_token_id,
                    },
                    finite=finite_outputs is not None,
                )
            generated = None
            decoder_used = "hf_generate"
            if graph_decoder is not None and graph_module.eligible(
                model.config.model_type, sample_options, finite_outputs, input_length, frame["max_tokens"]
            ):
                try:
                    with torch.inference_mode():
                        generated = graph_decoder.generate(
                            inputs["input_ids"], frame["max_tokens"], sample_options, deadline
                        )
                    decoder_used = graph_module.DECODER_NAME
                except Exception as exc:  # fall back for this request; the failure stays visible in the log
                    print(
                        json.dumps(
                            {
                                "stage": "graph_decoder_fallback",
                                "error": type(exc).__name__ + ": " + str(exc)[:300],
                            }
                        ),
                        file=sys.stderr,
                        flush=True,
                    )
                    generated = None
                    if sample_options.get("do_sample") and runtime_profile is not None:
                        torch.manual_seed(runtime_profile["seed"])
                        torch.cuda.manual_seed_all(runtime_profile["seed"])
            if generated is None:
                with torch.inference_mode():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=frame["max_tokens"],
                        **sample_options,
                        stopping_criteria=StoppingCriteriaList([Deadline()]),
                        pad_token_id=tokenizer.eos_token_id,
                        **generation_options,
                    )
                generated = outputs[0, input_length:]
            thinking_meta = None
            if enable_thinking is True:
                if frame.get("prompt_task") != "review" or budget_profile != "review-thinking/v1":
                    raise ValueError("Thinking checkpoint is registered for reviews only")
                text, thinking_meta = split_thinking_output(generated.tolist(), tokenizer)
            else:
                text = tokenizer.decode(generated, skip_special_tokens=True)
            if budget_profile in {REPAIR_PROFILE, "review-thinking/v1"} and len(text) > REPAIR_TEXT_LIMIT:
                raise ValueError("Expanded repair exceeds text capacity; no clipping")
            elapsed = time.monotonic() - started
            reason = (
                "deadline"
                if elapsed >= frame["deadline_ms"] / 1000
                else "length" if len(generated) >= frame["max_tokens"] else "stop"
            )
            result = {
                "type": "result",
                "id": frame["id"],
                "text": text,
                "finish_reason": reason,
                "latency_ms": int(elapsed * 1000),
                "decoder": decoder_used,
                "input_tokens": input_length,
                "output_tokens": len(generated),
                "finite_decoder": finite_outputs is not None,
                "finite_after_thinking": frame.get("finite_after_thinking", False),
                **({"enable_thinking": True, "thinking_output": thinking_meta} if thinking_meta else {}),
                "message_profile": message_profile,
                "generation_state": generation_state,
                "budget_profile": budget_profile,
                "construction_profile": "structured/v1" if structured else "historical/v1",
                "model_prompt_profile": model_prompt_profile,
                "sampling_profile": (
                    runtime_profile["sampling_profile"] if runtime_profile else "historical-greedy"
                ),
                "generation_seed": runtime_profile["seed"] if runtime_profile else None,
                **(
                    {
                        "web_review_prompt_version": frame["web_review_prompt_version"],
                        "web_review_format_reminder": frame["web_review_format_reminder"],
                        "web_review_messages_sha256": hashlib.sha256(
                            json.dumps(frame["messages"], ensure_ascii=False, sort_keys=True).encode("utf8")
                        ).hexdigest(),
                    }
                    if "web_review_prompt_version" in frame
                    else {}
                ),
            }
            # Drop transient tensor references before releasing this process's unused pool.
            # Model weights remain live; a different worker can now use the released memory.
            inputs = outputs = generated = None
            from cuda_handoff import cuda_handoff

            result["cuda_memory_handoff"] = cuda_handoff(torch, config.get("release_cuda_cache", False))
            print(json.dumps(result, ensure_ascii=False), flush=True)
        except Exception as exc:
            print(
                json.dumps({"type": "error", "id": frame["id"], "error_type": type(exc).__name__}), flush=True
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
