"""Read local index metadata without initializing an index or claiming integrity."""

import json
from pathlib import Path

from oralia.infrastructure.vector_store.config import get_vector_store_path


def read_index_status():
    path = Path(get_vector_store_path()) / "index_version.json"
    result = {"status": "not_initialized", "version": None, "integrity_verified": False}
    if not path.exists():
        return result
    try:
        with path.open("rb") as stream:
            raw = stream.read(1025)
        if len(raw) > 1024:
            raise ValueError("invalid metadata size")
        version = json.loads(raw)["version"]
        if type(version) is not int or version < 1:
            raise ValueError("invalid version")
        return {**result, "status": "metadata_available", "version": str(version)}
    except (OSError, ValueError, KeyError, TypeError):
        return {**result, "status": "metadata_unavailable"}
