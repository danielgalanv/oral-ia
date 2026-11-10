"""Standalone CPU-only check using the actual local worker tokenizer, never model weights."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--alternatives", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("preserve tokenizer evidence")
    os.environ.update(CUDA_VISIBLE_DEVICES="-1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    import torch
    import transformers
    from transformers import AutoTokenizer

    if torch.cuda.is_initialized():
        raise ValueError("CPU-only verification required")
    root = Path(__file__).resolve().parents[1]
    decoder_path = root / "src/oralia/course_dialogue/finite_schema.py"
    spec = importlib.util.spec_from_file_location("finite_schema", decoder_path)
    decoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decoder)
    tokenizer = AutoTokenizer.from_pretrained(
        str(args.source), local_files_only=True, trust_remote_code=False
    )
    groups = json.loads(args.alternatives.read_text(encoding="utf-8"))
    checked = []
    for label, alternatives in groups.items():
        schema = {"type": "object", "x-oralia-finite-outputs": alternatives}
        assert decoder.finite_json_outputs(schema) == alternatives
        sequences = [tokenizer.encode(text, add_special_tokens=False) for text in alternatives]
        assert len({tuple(sequence) for sequence in sequences}) == len(alternatives)
        assert all(
            tokenizer.decode(sequence, skip_special_tokens=False) == text
            for sequence, text in zip(sequences, alternatives, strict=True)
        )
        prefixes_checked = 0
        for sequence in sequences:
            for index, token in enumerate(sequence):
                prefix = sequence[:index]
                allowed = decoder.allowed_next_tokens(sequences, prefix, tokenizer.eos_token_id)
                expected = {
                    s[index] if len(s) > index else tokenizer.eos_token_id
                    for s in sequences
                    if s[:index] == prefix
                }
                assert set(allowed) == expected and token in allowed
                if not any(s == prefix for s in sequences):
                    assert tokenizer.eos_token_id not in allowed
                prefixes_checked += 1
            assert decoder.allowed_next_tokens(sequences, sequence, tokenizer.eos_token_id) == [
                tokenizer.eos_token_id
            ]
        try:
            decoder.allowed_next_tokens(sequences, [len(tokenizer) + 100], tokenizer.eos_token_id)
        except ValueError:
            pass
        else:
            raise AssertionError("foreign prefix accepted")
        checked.append(
            {
                "group": label,
                "alternatives": len(alternatives),
                "prefixes_checked": prefixes_checked,
                "maximum_tokens": max(map(len, sequences)),
                "all_eos_checked": True,
            }
        )
    assert not torch.cuda.is_initialized()
    tracked = ["tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"]
    result = {
        "source": str(args.source),
        "tokenizer_class": type(tokenizer).__name__,
        "transformers": transformers.__version__,
        "torch": torch.__version__,
        "cuda_visible_devices": os.environ["CUDA_VISIBLE_DEVICES"],
        "cuda_initialized": False,
        "model_weights_loaded": False,
        "model_inferences": 0,
        "groups": checked,
        "tokenizer_files": {
            name: hashlib.sha256((args.source / name).read_bytes()).hexdigest() for name in tracked
        },
        "decoder_sha256": hashlib.sha256(decoder_path.read_bytes()).hexdigest(),
        "alternatives_sha256": hashlib.sha256(args.alternatives.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"groups": checked, "cuda_initialized": False, "model_weights_loaded": False}))


if __name__ == "__main__":
    main()
