"""Prepare reviewed synthetic content through the owned E2E API; print no credentials."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main():
    from tests.dialogue.api_fixture import prepare_guided

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["self_study", "oral_defense"], required=True)
    parser.add_argument("--domain", choices=["agua", "programa"], default="agua")
    parser.add_argument("--screenless", action="store_true")
    parser.add_argument("--pedagogy", action="store_true")
    args = parser.parse_args()
    path = ROOT / ".e2e_governance.db"
    if not path.is_file():
        raise RuntimeError("Owned E2E database is not prepared")
    engine = create_engine(
        "sqlite://",
        creator=lambda: sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, check_same_thread=False),
    )
    try:
        with httpx.Client(base_url="http://127.0.0.1:8005", timeout=60) as client:
            assert client.get("/e2e-fixture").json() == {"fixture": "oralia-owned-e2e"}
            response = client.post(
                "/api/v1/auth/login", json={"secret": "fictional-e2e-installation-secret-005"}
            )
            assert response.status_code == 200, "E2E teacher authentication failed"
            client.__db_sessionmaker__ = sessionmaker(bind=engine)
            result = prepare_guided(
                client,
                domain=args.domain,
                mode=args.mode,
                start=False,
                screenless=args.screenless,
                pedagogy=args.pedagogy,
            )
            print(json.dumps({"activity_id": result["activity"]["id"]}))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
