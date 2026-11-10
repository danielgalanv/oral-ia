"""Real demo launcher against an isolated E2E workspace, with a runtime-only test credential."""

import os
import subprocess
import sys

from oralia.demo.launcher import reset
from oralia.demo.resources import SOURCE_ROOT, DemoPaths


def main():
    paths = DemoPaths(SOURCE_ROOT / ".claude-scratch/demo-e2e")
    paths.workspace.mkdir(parents=True, exist_ok=True)
    if paths.root.exists():
        reset(paths, confirmation="BORRAR DEMO")
    secret = os.environ.pop("ORALIA_DEMO_TEST_SECRET")
    os.environ["ORALIA_DEMO_ADMIN_SECRET"] = secret
    raise SystemExit(
        subprocess.call(
            [
                sys.executable,
                "-m",
                "oralia.demo",
                "start",
                "--workspace",
                str(paths.workspace),
                "--api-port",
                "8015",
                "--web-port",
                "5185",
                "--no-browser",
            ],
            cwd=SOURCE_ROOT,
        )
    )


if __name__ == "__main__":
    main()
