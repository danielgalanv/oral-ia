"""uvicorn entrypoint. Binds to 127.0.0.1 by default (FR-022) — never 0.0.0.0."""

from __future__ import annotations

import uvicorn


def main() -> None:
    uvicorn.run("oralia.interfaces.api.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
