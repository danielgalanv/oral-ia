"""CPU-only reconstruction of actual prompt length and real worker callback slicing."""

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path


def main():
    os.environ.update(CUDA_VISIBLE_DEVICES="-1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    import torch
    from transformers import AutoTokenizer

    assert not torch.cuda.is_initialized()
    root = Path(__file__).resolve().parents[1]
    evidence = root / "specs/012-conversational-course-study/evidence"
    output = evidence / "scope-effective-tokenizer-audit-v1.json"
    if output.exists():
        raise ValueError("preserve audit evidence")
    audit = json.loads((evidence / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    worker = json.loads((evidence / "scope-finite-capacity-first/worker.json").read_text(encoding="utf-8"))
    frame = audit["frame"]
    tokenizer = AutoTokenizer.from_pretrained(
        worker["source"], local_files_only=True, trust_remote_code=False
    )
    template_hash = hashlib.sha256(
        json.dumps(tokenizer.chat_template, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    assert template_hash == worker["effective_chat_template_sha256"]
    prompt = tokenizer.apply_chat_template(
        frame["messages"], tokenize=False, add_generation_prompt=True, **worker["chat_options"]
    )
    prompt_ids = tokenizer(prompt, return_tensors="pt")["input_ids"][0]  # deliberately stays on CPU
    actual = audit["original_attempt"]["outcome"]
    assert len(prompt_ids) == actual["parameters"]["input_tokens"] == 4189
    selected = tokenizer.encode(actual["text"], add_special_tokens=False)
    assert len(selected) + 1 == actual["parameters"]["output_tokens"]
    spec = importlib.util.spec_from_file_location(
        "finite_schema", root / "src/oralia/course_dialogue/finite_schema.py"
    )
    decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decoder)
    source = evidence / "scope-finite-capacity-v1/artifacts/src/oralia/course_dialogue/gpu_worker.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    callback = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "allowed"
    )
    sequences = [tokenizer.encode(text, add_special_tokens=False) for text in frame["finite_outputs"]]
    context = {
        "sequences": sequences,
        "input_length": len(prompt_ids),
        "tokenizer": tokenizer,
        "allowed_next_tokens": decoder.allowed_next_tokens,
    }
    exec(
        compile(ast.fix_missing_locations(ast.Module(body=[callback], type_ignores=[])), str(source), "exec"),
        context,
    )
    allowed = context["allowed"]
    for index in range(len(selected)):
        combined = torch.cat([prompt_ids, torch.tensor(selected[:index], dtype=prompt_ids.dtype)])
        actual_allowed = allowed(0, combined)
        assert actual_allowed == decoder.allowed_next_tokens(
            sequences, selected[:index], tokenizer.eos_token_id
        )
        assert selected[index] in actual_allowed
    complete = torch.cat([prompt_ids, torch.tensor(selected, dtype=prompt_ids.dtype)])
    assert allowed(0, complete) == [tokenizer.eos_token_id]
    assert allowed(0, prompt_ids) == decoder.allowed_next_tokens(sequences, [], tokenizer.eos_token_id)
    try:
        decoder.allowed_next_tokens(sequences, prompt_ids.tolist(), tokenizer.eos_token_id)
    except ValueError:
        pass
    else:
        raise AssertionError("prompt unexpectedly accepted as generated finite prefix")
    assert not torch.cuda.is_initialized()
    result = {
        "template_sha256": template_hash,
        "prompt_input_tokens": len(prompt_ids),
        "matches_actual_input_token_count": True,
        "selected_content_tokens": len(selected),
        "output_with_eos_matches_actual": True,
        "real_worker_callback_extracted_from_frozen_ast": True,
        "constraint_applies_after_prompt_input_length": True,
        "prompt_is_not_generated_prefix": True,
        "selected_complete_eos_checked": True,
        "cuda_initialized": False,
        "model_weights_loaded": False,
        "new_inferences": 0,
    }
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
