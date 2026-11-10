"""Real-tokenizer CPU validation of prepared diagnostic frames, not model inference."""

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
    package = evidence / "minimal-capacity-probe-v1"
    output = package / "cpu-tokenizer-check.json"
    if output.exists():
        raise ValueError("preserve CPU verification")
    resource = json.loads((evidence / "cpu-local-scope-resource-audit-v1.json").read_text(encoding="utf-8"))
    tokenizer = AutoTokenizer.from_pretrained(
        resource["source"], local_files_only=True, trust_remote_code=False
    )
    frames = json.loads((package / "frames.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location(
        "finite_schema", root / "src/oralia/course_dialogue/finite_schema.py"
    )
    decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decoder)
    rendered, rows = {}, []
    for frame in frames:
        prompt = tokenizer.apply_chat_template(frame["messages"], tokenize=False, add_generation_prompt=True)
        rendered[frame["id"]] = prompt
        input_ids = tokenizer(prompt)["input_ids"]
        assert len(input_ids) < 7000
        if frame["finite_outputs"] is not None:
            sequences = [tokenizer.encode(text, add_special_tokens=False) for text in frame["finite_outputs"]]
            for sequence in sequences:
                assert len(sequence) + 1 < frame["max_tokens"]
                for index, token in enumerate(sequence):
                    assert token in decoder.allowed_next_tokens(
                        sequences, sequence[:index], tokenizer.eos_token_id
                    )
                assert decoder.allowed_next_tokens(sequences, sequence, tokenizer.eos_token_id) == [
                    tokenizer.eos_token_id
                ]
        rows.append(
            {
                "id": frame["id"],
                "input_tokens": len(input_ids),
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "finite_outputs": len(frame["finite_outputs"] or []),
                "max_tokens": frame["max_tokens"],
            }
        )
    assert rendered["instruction_free"] == rendered["instruction_finite"]
    assert rendered["scope_free"] == rendered["scope_finite"]
    assert not torch.cuda.is_initialized()
    result = {
        "frames": rows,
        "pair_prompts_byte_identical": True,
        "all_finite_options_complete_and_eos_legal": True,
        "cuda_initialized": False,
        "model_weights_loaded": False,
        "new_model_calls": 0,
        "generation_confirmation_still_requires_future_model_object_dump": True,
    }
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
