"""One public RFC acquisition, CPU only, no model/reviewer or private input.

Run with a NEW output path. This receipt establishes transport/extraction only.
"""

import argparse
import asyncio
import json
from pathlib import Path

from oralia.documentary.web_evidence import (
    CuratedPublicSearch,
    LocalGap,
    PublicHTTPS,
    PublicSource,
    WebEvidence,
    WebPolicy,
)


async def run(output):
    source = PublicSource(
        "https://www.rfc-editor.org/rfc/rfc2119.txt",
        "RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels",
        "S. Bradner / RFC Editor",
        "March 1997; BCP 14; RFC 8174 updates are not included in this capture",
        "Public RFC text; no restricted resource or access bypass",
    )
    policy = WebPolicy(
        "public-acquisition-cpu-probe-2026-10-30",
        enabled=True,
        concepts=("software requirements",),
        destinations=("www.rfc-editor.org",),
        max_searches=1,
        max_pages=1,
        max_bytes=32768,
        request_seconds=10,
        seconds=20,
        redirects=1,
    )
    web = WebEvidence(
        policy,
        current_policy=lambda: policy,
        search=CuratedPublicSearch({"software requirements": (source,)}),
        acquisition=PublicHTTPS(policy.destinations),
    )
    gap = LocalGap(
        policy.activity,
        "software requirements",
        "in_scope",
        "insufficient",
        "probe-purpose-v1",
        "development_acquisition_probe",
        "Probe requirement-level terminology acquisition only; no semantic finding",
        "no-student-session-development-probe",
    )

    async def notice(text):
        print(text, flush=True)
        return True

    row = await web.acquire("public-probe-001", gap, notice)
    row["purpose"] = (
        "Public original-source transport/extraction only, not semantic validity or teacher compatibility"
    )
    with Path(output).open("x", encoding="utf-8") as handle:
        json.dump(row, handle, ensure_ascii=False, indent=2)
    print(json.dumps({"status": row["status"], "errors": row["errors"], "usage": row["usage"]}))
    return row["status"] == "acquired_unreviewed"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; evidence is never overwritten")
    raise SystemExit(0 if asyncio.run(run(args.output)) else 1)
