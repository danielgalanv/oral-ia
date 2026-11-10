"""CPU-only historical prompt/config verification with each trace's real tokenizer."""

import ast
import copy
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path


def main():
    os.environ.update(CUDA_VISIBLE_DEVICES="-1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    import torch
    from transformers import AutoTokenizer, GenerationConfig
    from transformers.generation.logits_process import RepetitionPenaltyLogitsProcessor
    from transformers.generation.utils import GenerationMixin

    assert not torch.cuda.is_initialized()
    root = Path(__file__).resolve().parents[1]
    evidence = root / "specs/012-conversational-course-study/evidence"
    output = evidence / "cpu-scope-trace-tokenizer-audit-v1.json"
    if output.exists():
        raise ValueError("preserve tokenizer audit")
    traces = json.loads((evidence / "cpu-effective-scope-traces-v1.json").read_text(encoding="utf-8"))[
        "traces"
    ]
    tokenizer = AutoTokenizer.from_pretrained(
        traces[0]["worker"]["source"], local_files_only=True, trust_remote_code=False
    )
    disk_config = GenerationConfig.from_pretrained(traces[0]["worker"]["source"], local_files_only=True)
    rows = []
    for trace in traces:
        worker, frame, original = trace["worker"], trace["frame"], trace["original_raw_result"]
        template_hash = hashlib.sha256(
            json.dumps(tokenizer.chat_template, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()
        assert template_hash == worker["effective_chat_template_sha256"]
        prompt = tokenizer.apply_chat_template(
            frame["messages"], tokenize=False, add_generation_prompt=True, **worker["chat_options"]
        )
        ids = tokenizer(prompt, return_tensors="pt")["input_ids"][0]
        assert len(ids) == original["input_tokens"] < 7000
        tree = ast.parse((root / trace["worker_snapshot"]).read_text(encoding="utf-8"))
        call = next(
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "model"
            and n.func.attr == "generate"
            and any(k.arg == "stopping_criteria" for k in n.keywords)
        )
        assert any(
            k.arg == "do_sample" and isinstance(k.value, ast.Constant) and k.value.value is False
            for k in call.keywords
        )
        effective = copy.deepcopy(disk_config)
        effective.update(
            do_sample=False, max_new_tokens=frame["max_tokens"], pad_token_id=tokenizer.eos_token_id
        )
        constrained = frame["finite_outputs"] is not None
        callback_checked = False
        if constrained:
            decoder_path = root / trace["worker_snapshot"].replace("gpu_worker.py", "finite_schema.py")
            # The historical package may not have copied this helper; its live
            # bytes are unchanged, verified separately in its manifests.
            if not decoder_path.exists():
                decoder_path = root / "src/oralia/course_dialogue/finite_schema.py"
            spec = importlib.util.spec_from_file_location("audit_finite", decoder_path)
            decoder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(decoder)
            sequences = [tokenizer.encode(text, add_special_tokens=False) for text in frame["finite_outputs"]]
            selected = tokenizer.encode(original["text"], add_special_tokens=False)
            assert len(selected) + 1 == original["output_tokens"]
            callback = next(
                n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "allowed"
            )
            context = {
                "sequences": sequences,
                "input_length": len(ids),
                "tokenizer": tokenizer,
                "allowed_next_tokens": decoder.allowed_next_tokens,
            }
            exec(
                compile(
                    ast.fix_missing_locations(ast.Module(body=[callback], type_ignores=[])),
                    "<frozen-callback>",
                    "exec",
                ),
                context,
            )
            for index, token in enumerate(selected):
                joined = torch.cat([ids, torch.tensor(selected[:index], dtype=ids.dtype)])
                allowed = context["allowed"](0, joined)
                assert token in allowed
                assert allowed == decoder.allowed_next_tokens(
                    sequences, selected[:index], tokenizer.eos_token_id
                )
            assert context["allowed"](0, torch.cat([ids, torch.tensor(selected, dtype=ids.dtype)])) == [
                tokenizer.eos_token_id
            ]
            callback_checked = True
        rows.append(
            {
                "run": trace["run"],
                "id": trace["id"],
                "input_tokens": len(ids),
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "template_matches": True,
                "message_roles": [m["role"] for m in frame["messages"]],
                "finite_outputs": len(frame["finite_outputs"] or []),
                "generated_tail_callback_checked": callback_checked,
                "generation_config_derivation_not_historical_object_dump": {
                    key: getattr(effective, key)
                    for key in (
                        "do_sample",
                        "max_new_tokens",
                        "pad_token_id",
                        "eos_token_id",
                        "repetition_penalty",
                        "temperature",
                        "top_p",
                        "top_k",
                    )
                },
                "temperature_top_p_top_k_inactive_when_greedy": True,
            }
        )
    logits = torch.tensor([[2.0, 2.0, 2.0, 2.0]])
    penalized = RepetitionPenaltyLogitsProcessor(disk_config.repetition_penalty)(
        torch.tensor([[1, 2]]), logits.clone()
    )
    assert (
        disk_config.repetition_penalty == 1.05
        and penalized[0, 1] < logits[0, 1]
        and penalized[0, 0] == logits[0, 0]
    )
    source = inspect.getsource(GenerationMixin._get_logits_processor)
    assert "generation_config.repetition_penalty" in source and "PrefixConstrainedLogitsProcessor" in source
    assert not torch.cuda.is_initialized()
    output.write_text(
        json.dumps(
            {
                "traces": rows,
                "inherited_repetition_penalty_cpu_effect_reproduced": True,
                "processor_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                "cuda_initialized": False,
                "model_weights_loaded": False,
                "new_model_calls": 0,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified_traces": len(rows),
                "input_tokens": [r["input_tokens"] for r in rows],
                "repetition_penalty": disk_config.repetition_penalty,
                "cuda_initialized": False,
            }
        )
    )


if __name__ == "__main__":
    main()
