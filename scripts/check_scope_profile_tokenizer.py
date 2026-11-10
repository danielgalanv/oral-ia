"""CPU-only real-tokenizer verification of the connected serialized message profiles."""

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
    output = evidence / "scope-control-profile-tokenizer-v1.json"
    if output.exists():
        raise ValueError("preserve tokenizer check")
    worker = json.loads((evidence / "scope-finite-capacity-first/worker.json").read_text(encoding="utf-8"))
    frames = json.loads((evidence / "scope-control-transport-frames-v1.json").read_text(encoding="utf-8"))[
        "frames"
    ]
    tokenizer = AutoTokenizer.from_pretrained(
        worker["source"], local_files_only=True, trust_remote_code=False
    )
    template_hash = hashlib.sha256(
        json.dumps(tokenizer.chat_template, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    assert template_hash == worker["effective_chat_template_sha256"]
    path = root / "src/oralia/course_dialogue/scope_message_profiles.py"
    spec = importlib.util.spec_from_file_location("scope_message_profiles", path)
    profiles = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profiles)
    rows = []
    for record in frames:
        frame = record["frame"]
        profile = profiles.validate_frame_profile(frame)
        prompt = tokenizer.apply_chat_template(
            frame["messages"], tokenize=False, add_generation_prompt=True, **worker["chat_options"]
        )
        tokens = tokenizer(prompt)["input_ids"]
        assert len(tokens) < 7000
        if record["label"] != "academic":
            assert "<scope_control_data>" in frame["messages"][1]["content"]
            assert "Responde únicamente usando el contenido de las etiquetas <evidencia>" not in prompt
            assert profile == record["exchange"]["confirmed_message_profile"]
        else:
            assert '<evidencia documento="fixture" version="1">' in prompt
            assert "Responde únicamente usando el contenido de las etiquetas <evidencia>" in prompt
        rows.append(
            {
                "label": record["label"],
                "effective_profile": profile,
                "input_tokens": len(tokens),
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            }
        )
    assert not torch.cuda.is_initialized()
    output.write_text(
        json.dumps(
            {
                "frames": rows,
                "source": worker["source"],
                "template_sha256": template_hash,
                "cuda_initialized": False,
                "model_weights_loaded": False,
                "model_inferences": 0,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(rows))


if __name__ == "__main__":
    main()
