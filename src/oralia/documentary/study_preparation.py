"""CPU-only receipts for reusable builds/indexes; never loads an encoder or LLM."""

import argparse
import hashlib
import importlib.metadata
import json
import shutil
from pathlib import Path

from oralia.documentary.__main__ import CURRENT_PACKAGE, PACKAGES, load_package
from oralia.documentary.concepts import prepare_teacher_concepts
from oralia.documentary.retrieval import PROTOCOL, SNAPSHOT

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = "preparation.json"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def current_inputs():
    files = list((ROOT / "src/oralia").rglob("*.py"))
    files += [p for p in (ROOT / "apps/web/src").rglob("*") if p.is_file()]
    files += [
        p
        for p in (ROOT / "apps/web").iterdir()
        if p.is_file() and p.suffix in {".json", ".js", ".ts", ".yaml"}
    ]
    files += [PROTOCOL]
    package, manifest_name = PACKAGES[CURRENT_PACKAGE]
    manifest, _ = load_package(package, manifest_name)
    files += [package / manifest_name]
    files += [package / doc[key] for doc in manifest["documents"] for key in ("original", "extraction")]
    sources = {str(p.relative_to(ROOT)): digest(p) for p in files}
    encoder = {str(p.relative_to(SNAPSHOT)): digest(p) for p in SNAPSHOT.rglob("*") if p.is_file()}
    if not encoder:
        raise ValueError("Local retrieval encoder absent; no download")
    versions = {
        name: importlib.metadata.version(name)
        for name in ("sentence-transformers", "transformers", "tokenizers", "torch", "chromadb")
    }
    return {"sources": sources, "encoder": encoder, "versions": versions}


def checked_root(path):
    path = Path(path).resolve()
    if path.parent != (ROOT / ".claude-scratch").resolve() or not path.name.startswith("study-chat-"):
        raise ValueError("Prepared run must be an owned study-chat directory in .claude-scratch")
    return path


def artifacts(root):
    required = [
        "web-dist/index.html",
        "retrieval-index/identity.json",
        "retrieval-index/fragments.json",
        "retrieval-index/chroma/index_version.json",
        "concept-catalogue/manifest.json",
    ]
    if any(not (root / name).is_file() for name in required):
        raise ValueError("Prepared interface/index incomplete")
    result = {}
    for directory in ("web-dist", "retrieval-index", "concept-catalogue"):
        for path in (root / directory).rglob("*"):
            if not path.resolve().is_relative_to(root):
                raise ValueError("Prepared artifact escapes its root")
            if path.is_file():
                result[str(path.relative_to(root))] = digest(path)
    return result


def prepare_receipt(path):
    root = checked_root(path)
    if (root / RECEIPT).exists():
        raise FileExistsError(root / RECEIPT)
    prepare_teacher_concepts(root / "concept-catalogue")
    receipt = {
        "schema": "oralia-study-preparation/v2",
        "selection_profile": "comparison-coverage/v1",
        "inputs": current_inputs(),
        "artifacts": artifacts(root),
    }
    with (root / RECEIPT).open("x", encoding="utf8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)


def validate_preparation(path):
    root = checked_root(path)
    receipt = json.loads((root / RECEIPT).read_text(encoding="utf8"))
    if (
        receipt.get("schema") != "oralia-study-preparation/v2"
        or receipt.get("selection_profile") != "comparison-coverage/v1"
    ):
        raise ValueError("Unknown preparation receipt; prepare again explicitly")
    if receipt.get("inputs") != current_inputs():
        raise ValueError("Sources, application or retrieval environment changed; prepare again explicitly")
    if receipt.get("artifacts") != artifacts(root):
        raise ValueError("Prepared build/index changed; prepare again explicitly")
    return root


def materialize_index(path, destination):
    root = validate_preparation(path)
    destination = Path(destination).resolve()
    if not destination.is_relative_to(root / "launches") or destination == root / "launches":
        raise ValueError("Working index must remain in a new owned launch directory")
    shutil.copytree(root / "retrieval-index", destination)
    receipt = json.loads((root / RECEIPT).read_text(encoding="utf8"))
    expected = {
        str(Path(*Path(key).parts[1:])): value
        for key, value in receipt["artifacts"].items()
        if Path(key).parts[0] == "retrieval-index"
    }
    actual = {str(p.relative_to(destination)): digest(p) for p in destination.rglob("*") if p.is_file()}
    if actual != expected:
        raise ValueError("Working index differs from verified preparation")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "validate", "materialize"))
    parser.add_argument("root", type=Path)
    parser.add_argument("destination", type=Path, nargs="?")
    args = parser.parse_args()
    try:
        if args.action == "materialize":
            if args.destination is None:
                parser.error("materialize requires a working-index destination")
            materialize_index(args.root, args.destination)
        else:
            (prepare_receipt if args.action == "create" else validate_preparation)(args.root)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Preparation: {error}\n")
    print("Preparation receipt valid; no generative model or GPU loaded.")


if __name__ == "__main__":
    main()
