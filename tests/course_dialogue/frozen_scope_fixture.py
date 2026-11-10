"""Reconstruct a test-only frozen tree; never weaken the production hash guard."""

import hashlib
import json


def archived_root(package, live_root, tmp_path):
    destination = tmp_path / "archived-root"
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        archived = package / "artifacts" / name
        source = archived if archived.is_file() else live_root / name
        contents = source.read_bytes()
        assert hashlib.sha256(contents).hexdigest() == expected, name
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    return destination
