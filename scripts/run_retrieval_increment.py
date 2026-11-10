"""One frozen measurement pass per strategy; no generation, tuning or overwrites."""

import argparse
import json
import math
import time
from collections import defaultdict

from oralia.documentary.retrieval import DERIVED, ROOT, Retrieval, digest

OUT = ROOT / "docs/audits/2026-10-27-retrieval-increment"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--measure", action="store_true")
    args = parser.parse_args()
    freeze = json.loads((OUT / "freeze.json").read_text(encoding="utf8"))
    for name, expected in freeze.items():
        if digest((OUT / name).read_bytes()) != expected:
            raise ValueError("frozen bank/protocol changed")
    if args.measure and any((OUT / f"results-{s}.json").exists() for s in ["lexical", "dense", "rrf"]):
        raise FileExistsError("measurement already exposed; do not rerun silently")
    started = time.monotonic()
    retrieval = Retrieval(build=args.build)
    load_seconds = time.monotonic() - started
    print(f"CPU ready: {len(retrieval.pages)} pages, {len(retrieval.fragments)} fragments", flush=True)
    if not args.measure:
        return
    bank = json.loads((OUT / "bank-v1.json").read_text(encoding="utf8"))
    for strategy in retrieval.config["strategies"]:
        target = OUT / f"results-{strategy}.json"
        rows = []
        # Reserve pass receipt before first query. Exceptions preserve partial results.
        with target.open("x", encoding="utf8") as f:
            json.dump({"state": "started", "strategy": strategy}, f)
        try:
            for case in bank:
                before = time.monotonic()
                result = retrieval.query(
                    case["question"],
                    strategy,
                    history=case.get("history", []),
                    focus_change=case.get("focus_change", False),
                )
                elapsed = time.monotonic() - before
                relevant = set(case["relevant"])
                candidates = {f["page_id"] for f in result["candidates"]}
                final = [p["id"] for p in result["passages"]]
                hits = [int(id in relevant) for id in final]
                dcg = sum(hit / math.log2(i + 2) for i, hit in enumerate(hits))
                ideal = sum(1 / math.log2(i + 2) for i in range(min(len(relevant), len(final))))
                rows.append(
                    {
                        "id": case["id"],
                        "subtopic": case["subtopic"],
                        "split": case["split"],
                        "seconds": elapsed,
                        "candidate_recall": len(candidates & relevant) / len(relevant) if relevant else None,
                        "final_recall": len(set(final) & relevant) / len(relevant) if relevant else None,
                        "mrr": (
                            next((1 / (i + 1) for i, hit in enumerate(hits) if hit), 0) if relevant else None
                        ),
                        "ndcg": dcg / ideal if ideal else None,
                        "irrelevant_context_chars": sum(
                            len(p["text"]) for p in result["passages"] if p["id"] not in relevant
                        ),
                        "context_chars": result["context_chars"],
                        "returned_pages": final,
                        "candidate_pages": sorted(candidates),
                        "omitted": result["omitted_context"],
                        "absence_control": not relevant,
                        "completed": True,
                    }
                )
                print(strategy, case["id"], "done", flush=True)
        finally:
            groups = defaultdict(list)
            for row in rows:
                groups[row["subtopic"]].append(row)
            summaries = {
                topic: {
                    key: sum(r[key] for r in group if r[key] is not None)
                    / sum(r[key] is not None for r in group)
                    for key in [
                        "candidate_recall",
                        "final_recall",
                        "mrr",
                        "ndcg",
                        "seconds",
                        "context_chars",
                        "irrelevant_context_chars",
                    ]
                    if any(r[key] is not None for r in group)
                }
                for topic, group in groups.items()
            }
            target.write_text(
                json.dumps(
                    {
                        "strategy": strategy,
                        "rows": rows,
                        "by_subtopic": summaries,
                        "load_seconds": load_seconds,
                        "completed": len(rows) == len(bank),
                        "identity": retrieval.identity,
                        "root": str(DERIVED),
                        "freeze": freeze,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf8",
            )
    print("Bounded measurement complete. No generator called.", flush=True)


if __name__ == "__main__":
    main()
