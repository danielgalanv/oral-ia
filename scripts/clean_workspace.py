"""Preview/remove regenerable caches only. Never clean data, evidence or dependencies."""

import argparse
import json
import os
import shutil
from pathlib import Path

DIRECT = (".pytest_cache", ".ruff_cache", "apps/web/node_modules/.vite")
LIVE = ("src", "tests", "scripts", "apps/api")


def linked(path):
    return path.is_symlink() or path.is_junction()


def targets(root):
    root = Path(root).resolve()
    candidates = [root / name for name in DIRECT]
    for name in LIVE:
        base = root / name
        if not base.is_dir() or linked(base):
            continue
        for parent, directories, _ in os.walk(base, followlinks=False):
            directories[:] = [d for d in directories if not linked(Path(parent) / d)]
            if "__pycache__" in directories:
                candidates.append(Path(parent) / "__pycache__")
                directories.remove("__pycache__")
    result = []
    for path in candidates:
        if not path.is_dir() or linked(path) or not path.resolve().is_relative_to(root):
            continue
        # Refuse a whole candidate if it contains a link/junction; never follow it.
        unsafe = False
        size = 0
        for parent, directories, files in os.walk(path, followlinks=False):
            children = [Path(parent) / child for child in directories + files]
            if any(linked(child) or not child.resolve().is_relative_to(root) for child in children):
                unsafe = True
                break
            size += sum((Path(parent) / child).stat().st_size for child in files)
        if not unsafe:
            result.append((path, size))
    return result


def clean(root, *, apply=False):
    root = Path(root).resolve()
    selected = targets(root)
    removed, errors = [], []
    if apply:
        for path, _ in selected:
            # Recheck the explicit allowlist immediately before recursive deletion.
            allowed = path.relative_to(root).as_posix() in DIRECT or (
                path.name == "__pycache__" and any(path.is_relative_to(root / base) for base in LIVE)
            )
            if not allowed or linked(path) or not path.resolve().is_relative_to(root):
                raise ValueError("cache target changed or escaped workspace")
            try:
                shutil.rmtree(path)
                removed.append(str(path.relative_to(root)))
            except OSError as exc:
                errors.append(dict(path=str(path.relative_to(root)), error=str(exc)))
    return dict(
        apply=apply,
        candidates=[str(p.relative_to(root)) for p, _ in selected],
        candidate_bytes=sum(size for _, size in selected),
        removed=removed,
        errors=errors,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="delete only the previewed cache categories")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.output and (
        args.output.suffix != ".json"
        or args.output.exists()
        or args.output.is_symlink()
        or not args.output.resolve().is_relative_to(root)
    ):
        raise ValueError("output must be a new JSON file inside the workspace")
    result = clean(root, apply=args.apply)
    if args.output:
        with args.output.open("x", encoding="utf8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
    print(
        f"Caches: {len(result['candidates'])}; {result['candidate_bytes']/1024/1024:.2f} MiB; "
        f"removed: {len(result['removed'])}; errors: {len(result['errors'])}; apply={args.apply}"
    )
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
