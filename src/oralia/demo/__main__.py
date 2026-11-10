"""PowerShell-facing CLI. Secrets enter by environment/getpass, never arguments."""

import argparse
import json
import os
import secrets
import sys
from pathlib import Path

from oralia.demo.progress import Progress
from oralia.demo.resources import SOURCE_ROOT, DemoError, DemoPaths


def main():
    # Stable Spanish output for redirected PowerShell/scripts and direct Python calls.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Demostración local ORALIA, solo datos ficticios")
    parser.add_argument("action", choices=["start", "check", "stop", "reset", "prepare", "serve-api"])
    parser.add_argument("--api-port", type=int, default=8010)
    parser.add_argument("--web-port", type=int, default=5180)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--text-only", action="store_true")
    parser.add_argument("--workspace", type=Path, default=SOURCE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--run-id", default="", help=argparse.SUPPRESS)
    args = parser.parse_args()
    paths = DemoPaths(args.workspace)
    progress = Progress(paths=paths)
    # Register process-only credentials for redaction before any diagnostic.
    progress.protect(os.environ.get("ORALIA_DEMO_ADMIN_SECRET", ""))
    progress.protect(os.environ.get("ORALIA_ADMIN_SECRET", ""))
    try:
        from oralia.demo import launcher

        if args.action == "check":
            print(
                json.dumps(
                    launcher.check(
                        paths, args.api_port, args.web_port, text_only=args.text_only, progress=progress
                    ),
                    ensure_ascii=False,
                )
            )
        elif args.action == "start":

            def credential():
                secret = os.environ.pop("ORALIA_DEMO_ADMIN_SECRET", "") or secrets.token_urlsafe(32)
                progress.protect(secret)
                progress.say("[DEMO LOCAL] Área docente sin credencial; solo datos ficticios.")
                return secret

            launcher.start(
                paths,
                secret_factory=credential,
                progress=progress,
                api_port=args.api_port,
                web_port=args.web_port,
                text_only=args.text_only,
                no_browser=args.no_browser,
            )
        elif args.action == "stop":
            launcher.stop(paths)
        elif args.action == "reset":
            paths.validate(tree=True)
            print("Se borrará exclusivamente: " + str(paths.root))
            launcher.reset(paths, confirmation=input("Escriba BORRAR DEMO para confirmar: "))
        elif args.action == "prepare":
            from oralia.demo.fixtures import prepare

            print(json.dumps(prepare(paths, text_only=args.text_only), ensure_ascii=False))
        else:
            paths.validate()
            from oralia.demo.fixtures import verify_schema

            verify_schema(paths)
            if json.loads((paths.root / "fixtures.json").read_text(encoding="utf-8"))["profile"] == "full":
                from oralia.demo.resources import check_embeddings

                # Warm before readiness; preserve the existing turn budget.
                check_embeddings()
            import uvicorn

            from oralia.interfaces.api.app import create_app

            app = create_app()
            from oralia.demo.access import enable_demo_teacher_access

            enable_demo_teacher_access(app, paths)

            @app.get("/demo-ready")
            def ready():
                return {"run_id": args.run_id}

            uvicorn.run(app, host="127.0.0.1", port=args.api_port, reload=False)
        return 0
    except KeyboardInterrupt:
        progress.say("[CANCELADO] Operación demo; datos conservados.")
        return 130
    except Exception as exc:
        progress.diagnostic(exc)
        cause = str(exc) if isinstance(exc, DemoError) else f"causa no determinada ({type(exc).__name__})"
        progress.say("Demo: " + cause + " Revise los logs demo antes de reintentar.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
