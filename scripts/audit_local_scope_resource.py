"""CPU metadata/header audit: never instantiate a model or initialize CUDA."""

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "cpu-local-scope-resource-audit-v1.json"


def audit_resource(source):
    config = json.loads((source / "config.json").read_text(encoding="utf-8"))
    generation = json.loads((source / "generation_config.json").read_text(encoding="utf-8"))
    index = json.loads((source / "model.safetensors.index.json").read_text(encoding="utf-8"))
    tensors, shards = {}, []
    sizes = {"BF16": 2, "F16": 2, "F32": 4, "F64": 8, "I64": 8, "I32": 4}
    for name in sorted(set(index["weight_map"].values())):
        path = source / name
        with path.open("rb") as stream:
            length = int.from_bytes(stream.read(8), "little")
            if not 0 < length <= 16 * 1024 * 1024:
                raise ValueError("unsafe/unexpected safetensors header length")
            header_raw = stream.read(length)
        header = json.loads(header_raw)
        data_size = path.stat().st_size - 8 - length
        for key, value in header.items():
            if key == "__metadata__":
                continue
            if key in tensors or index["weight_map"].get(key) != name:
                raise ValueError("weight index/header mapping mismatch")
            start, end = value["data_offsets"]
            if not 0 <= start <= end <= data_size:
                raise ValueError("tensor range outside shard")
            if value["dtype"] in sizes and end - start != math.prod(value["shape"]) * sizes[value["dtype"]]:
                raise ValueError("tensor shape/dtype/byte count mismatch")
            tensors[key] = value
        shards.append(
            {
                "name": name,
                "file_bytes": path.stat().st_size,
                "header_bytes": length,
                "header_sha256": hashlib.sha256(header_raw).hexdigest(),
            }
        )
    if set(tensors) != set(index["weight_map"]):
        raise ValueError("tensor inventory mismatch")
    total_bytes = sum(row["data_offsets"][1] - row["data_offsets"][0] for row in tensors.values())
    if total_bytes != index["metadata"]["total_size"]:
        raise ValueError("weight total_size mismatch")
    expected = [config["vocab_size"], config["hidden_size"]]
    if (
        tensors["model.embed_tokens.weight"]["shape"] != expected
        or tensors["lm_head.weight"]["shape"] != expected
    ):
        raise ValueError("embedding/head inconsistent with declared config")
    layers = {int(key.split(".")[2]) for key in tensors if key.startswith("model.layers.")}
    if layers != set(range(config["num_hidden_layers"])):
        raise ValueError("layer inventory mismatch")
    return {
        "source": str(source),
        "config": config,
        "generation_config_on_disk": generation,
        "shards": shards,
        "tensor_count": len(tensors),
        "layer_count": len(layers),
        "parameter_elements_from_headers": sum(math.prod(row["shape"]) for row in tensors.values()),
        "data_bytes": total_bytes,
        "file_bytes": sum(row["file_bytes"] for row in shards),
        "dtypes": sorted({row["dtype"] for row in tensors.values()}),
        "adapter_config_present": (source / "adapter_config.json").exists(),
        "metadata_sha256": {
            name: hashlib.sha256((source / name).read_bytes()).hexdigest()
            for name in (
                "config.json",
                "generation_config.json",
                "model.safetensors.index.json",
                "tokenizer_config.json",
            )
        },
        "weight_values_read": False,
        "upstream_weight_checksum_verified": False,
        "identity_claim": "local_shard_structure_consistent_with_declared_config_not_upstream_authentication",
    }


def main():
    if OUTPUT.exists():
        raise ValueError("preserve audit")
    runs = [
        "scope-classifier-resource-v2",
        "scope-v2-described-first",
        "scope-finite-capacity-first",
        "scope-control-diagnostic-resource-run",
    ]
    workers = {
        name: json.loads((EVIDENCE / name / "worker.json").read_text(encoding="utf-8")) for name in runs
    }
    sources = {row["source"] for row in workers.values()}
    if len(sources) != 1 or any(row["quantization"] != "nf4" for row in workers.values()):
        raise ValueError("compared runs do not share the declared resource")
    resource = audit_resource(Path(next(iter(sources))))
    for worker in workers.values():
        if (
            worker["weight_bytes"] != resource["file_bytes"]
            or worker["effective_model_class"] not in resource["config"]["architectures"]
        ):
            raise ValueError("worker/resource metadata mismatch")
    resource["worker_runs"] = {
        name: {
            key: row.get(key)
            for key in (
                "source",
                "python",
                "torch",
                "transformers",
                "quantization",
                "effective_model_class",
                "effective_tokenizer_class",
                "effective_chat_template_sha256",
                "chat_options",
                "weight_bytes",
            )
        }
        for name, row in workers.items()
    }
    resource["historical_actual_dtype_quantization_processor_dump_available"] = False
    resource["model_instantiated"] = False
    resource["gpu_inference_calls"] = 0
    OUTPUT.write_text(json.dumps(resource, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                key: resource[key]
                for key in ("tensor_count", "layer_count", "parameter_elements_from_headers", "dtypes")
            }
        )
    )


if __name__ == "__main__":
    main()
