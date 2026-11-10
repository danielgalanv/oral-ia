"""Read-only generation metadata, usable by the standalone worker without ORALIA imports."""

import copy


def _plain(value):
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def generation_snapshot(model, tokenizer, call_kwargs=None, *, finite=False):
    explicit = dict(call_kwargs or {})
    actual = model.generation_config.to_dict()
    derived = copy.deepcopy(model.generation_config)
    derived.update(**explicit)
    quantization = getattr(model.config, "quantization_config", None)
    if hasattr(quantization, "to_dict"):
        quantization = quantization.to_dict()
    parameter = next(model.parameters())
    return _plain(
        {
            "model_generation_config": actual,
            "explicit_generate_kwargs": explicit,
            "effective_config_after_explicit_overrides": derived.to_dict(),
            "quantization_config": quantization,
            "is_quantized": getattr(model, "is_quantized", None),
            "model_training": model.training,
            "representative_parameter_dtype": str(parameter.dtype),
            "representative_parameter_device": str(parameter.device),
            "tokenizer_eos_token_id": tokenizer.eos_token_id,
            "finite_prefix_constraint": finite,
            "not_a_dump_of_weight_values": True,
        }
    )
