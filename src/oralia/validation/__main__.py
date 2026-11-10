"""Text-only local maintainer CLI; no external data input or API integration."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from oralia.validation.protocol import CONDITIONS, Protocol
from oralia.validation.reporting import replay, run_experiment, write_package


async def execute(args):
    if args.command == "replay":
        result = await replay(args.package)
        print(json.dumps(result))
        return 0 if result["matched"] else 1
    if args.output.exists():
        raise FileExistsError("output directory must be new")
    protocol = Protocol(
        seed=args.seed,
        repetitions=args.repetitions,
        ablations_authorized=args.authorize_synthetic_ablations,
        conditions=list(CONDITIONS) if args.authorize_synthetic_ablations else ["baseline", "full"],
    )
    result = await run_experiment(protocol)
    write_package(args.output, result)
    print(
        json.dumps(
            {
                "package": str(args.output.resolve()),
                "cells": len(result["cells"]),
                "errors": sum(c["error"] is not None for c in result["cells"]),
            }
        )
    )
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="ORAL-IA synthetic architecture validation; no participant data"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--repetitions", type=int, default=2)
    run.add_argument("--authorize-synthetic-ablations", action="store_true")
    reproduction = sub.add_parser("replay")
    reproduction.add_argument("--package", type=Path, required=True)
    try:
        return asyncio.run(execute(parser.parse_args()))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
