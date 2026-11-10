"""Bounded JSON alternatives, never a semantic or publication verdict."""

import json


def finite_json_outputs(schema):
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return None
    if "x-oralia-finite-outputs" in schema:
        outputs = schema["x-oralia-finite-outputs"]
        if (
            not isinstance(outputs, list)
            or not 1 <= len(outputs) <= 256
            or any(not isinstance(text, str) or len(text) > 512 for text in outputs)
        ):
            raise ValueError("invalid bounded finite JSON outputs")
        if any(not isinstance(json.loads(text), dict) for text in outputs):
            raise ValueError("finite JSON outputs must be objects")
        return outputs
    properties = schema.get("properties", {})
    if (
        not isinstance(properties, dict)
        or len(properties) != 1
        or schema.get("additionalProperties") is not False
    ):
        return None
    key, field = next(iter(properties.items()))
    if not isinstance(key, str) or len(key) > 128 or not isinstance(field, dict):
        return None
    values = field.get("enum")
    if schema.get("required") != [key] or not isinstance(values, list) or not 1 <= len(values) <= 32:
        return None
    if any(type(value) not in {str, int} or len(str(value)) > 128 for value in values):
        return None
    return [json.dumps({key: value}, ensure_ascii=False) for value in values]


def allowed_next_tokens(sequences, generated, eos_token_id):
    """Only prefixes of the explicitly enumerated alternatives can be emitted."""
    prefix = list(generated)
    allowed = set()
    for sequence in sequences:
        if sequence[: len(prefix)] == prefix:
            allowed.add(sequence[len(prefix)] if len(prefix) < len(sequence) else eos_token_id)
    if not allowed:
        raise ValueError("finite decoder prefix outside declared alternatives")
    return sorted(allowed)


def allowed_thinking_tokens(sequences, generated, eos_token_id, vocabulary_size, closing_token_id):
    """Leave reasoning untouched; constrain only tokens after its single end marker."""
    closes = [i for i, token in enumerate(generated) if token == closing_token_id]
    if not closes:
        return range(vocabulary_size)
    if len(closes) != 1:
        raise ValueError("multiple thinking end markers")
    return allowed_next_tokens(sequences, generated[closes[0] + 1 :], eos_token_id)
