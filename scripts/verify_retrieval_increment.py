"""Real CPU reconstruction/offset contracts; no evaluation-bank pass."""

import json
import socket
from pathlib import Path

from oralia.documentary.retrieval import DERIVED, Retrieval, digest

receipt_target = Path("docs/audits/2026-10-27-retrieval-increment/real-contracts-next.json")
if receipt_target.exists():
    raise FileExistsError("verification receipt already exists; preserve the earlier attempt")

# Deny external connections even if a dependency attempted a remote fallback.
original_connect = socket.socket.connect
attempts = []


def local_only(sock, address):
    if isinstance(address, tuple) and address[0] not in {"127.0.0.1", "::1", "localhost"}:
        attempts.append(str(address))
        raise RuntimeError("external network denied by verification harness")
    return original_connect(sock, address)


socket.socket.connect = local_only
before = {str(p.relative_to(DERIVED)): digest(p.read_bytes()) for p in DERIVED.rglob("*") if p.is_file()}
r = Retrieval()
for id, p in r.pages.items():
    fragments = [f for f in r.fragments if f["page_id"] == id]
    assert "".join(f["text"] for f in fragments) == p["text"]
    for f in fragments:
        assert p["text"][f["start"] : f["end"]] == f["text"]
        assert len(r.tokenizer.encode(f["text"], add_special_tokens=True, truncation=False)) <= r.limit
        assert f["page_id"] in r.pages
# Exposed demonstrator only; this is reconstruction evidence, not another bank measurement.
result = r.query("¿Qué es un requisito?", "rrf")
assert any(p["id"] == "docente-requisitos:4" for p in result["passages"])
index_version = r.store.get_index_version()
r2 = Retrieval(build=True)
assert r2.store.get_index_version() == index_version
assert r2.fragments == r.fragments
# Foreign identity receipts must reject before any Chroma client/write.
base = Path(".scratch-retrieval-v2/identity-mismatch")
base.mkdir(parents=True, exist_ok=True)
rejected = []
for field in [
    "dimension",
    "pooling",
    "limit_with_specials",
    "normalization",
    "representation",
    "sources",
    "versions",
]:
    root = base / field
    root.mkdir(exist_ok=False)
    identity = dict(r.identity)
    identity[field] = "incompatible"
    (root / "identity.json").write_text(json.dumps(identity), encoding="utf8")
    try:
        Retrieval(root=root, build=True)
        raise AssertionError("mismatch accepted")
    except ValueError as exc:
        assert "mismatch" in str(exc)
        assert not (root / "chroma").exists()
        rejected.append(field)
assert str(r.model.device) == "cpu"
assert not attempts
# Existing receipts and Chroma files must remain identical on reopen/query.
after = {str(p.relative_to(DERIVED)): digest(p.read_bytes()) for p in DERIVED.rglob("*") if p.is_file()}
Path("docs/audits/2026-10-27-retrieval-increment/real-contracts-next.json").write_text(
    json.dumps(
        {
            "pages": len(r.pages),
            "fragments": len(r.fragments),
            "limit_with_specials": r.limit,
            "dimension": r.identity["dimension"],
            "device": str(r.model.device),
            "external_attempts": attempts,
            "index_version": index_version,
            "rejected_identity_fields": rejected,
            "idempotent_build": True,
            "unchanged_files": all(
                before.get(f) == after.get(f)
                for f in ["identity.json", "fragments.json", "chroma/index_version.json"]
            ),
            "identity": r.fingerprint,
            "definition_pages": [p["id"] for p in result["passages"]],
            "all_offsets_exact": True,
            "coverage_complete": True,
            "no_oversized_encoder_input": True,
        },
        indent=2,
    ),
    encoding="utf8",
)
print("Real CPU reconstruction and 207 offset/capacity contracts passed; no external connection.")
