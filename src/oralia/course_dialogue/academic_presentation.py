"""Lossless presentation of the one observed transport wrapper, not academic repair."""

import hashlib
import json


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def present_academic_answer(raw):
    """Keep ordinary prose/code unchanged; unwrap only one exact, complete object."""
    result = {"text": raw, "format": "plain_text", "raw_sha256": hashlib.sha256(raw.encode()).hexdigest()}
    if not raw.lstrip().startswith("{"):
        return result
    try:
        value = json.loads(raw, object_pairs_hook=_unique_object)
    except ValueError:
        if '"mensaje_mostrado"' in raw:
            raise ValueError("Invalid academic presentation wrapper") from None
        return result
    if not isinstance(value, dict) or "mensaje_mostrado" not in value:
        return result
    body = value["mensaje_mostrado"]
    if set(value) != {"mensaje_mostrado"} or not isinstance(body, str) or not body.strip():
        raise ValueError("Ambiguous academic presentation wrapper")
    if body.lstrip().startswith("{") and '"mensaje_mostrado"' in body:
        raise ValueError("Nested academic presentation wrapper")
    return {**result, "text": body, "format": "mensaje_mostrado_json"}
