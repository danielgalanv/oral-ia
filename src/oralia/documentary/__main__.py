"""Serve the existing web materials view and an immutable local package."""

import argparse
import hashlib
import json
import os
import socket
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from oralia.interfaces.api.deps.local_access import LocalAccess, _local_transport

WORKSPACE = Path(__file__).resolve().parents[3]
PACKAGE = WORKSPACE / "materiales/docente/piloto-requisitos/paquete-v1"
MANIFEST = "manifest-v1.1.json"
PACKAGES = {
    "v1.1": (PACKAGE, MANIFEST),
    "v2": (PACKAGE.parent / "paquete-v2", "manifest-v2.json"),
    "v3": (PACKAGE.parent / "paquete-v3", "manifest-v3.json"),  # v2 + IEEE 830 and STSE pages; teacher review pending
}
STUDY_PACKAGES = ("v2", "v3")
CURRENT_PACKAGE = os.environ.get("ORALIA_PACKAGE", "v3")  # the study chat's package; v3 (v2 + IEEE 830 and STSE, accepted 2026-11-07)
if CURRENT_PACKAGE not in STUDY_PACKAGES:
    raise ValueError("ORALIA_PACKAGE must be v2 or v3")


def _fixture_provider():
    from oralia.documentary.study_lab import FixtureGenerationPort

    return FixtureGenerationPort(delay=2)


def confined(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("Package path is not a regular internal file")
    return path


def load_package(root, manifest_name=MANIFEST):
    manifest = json.loads(confined(root, manifest_name).read_text(encoding="utf-8"))
    pages = {}
    for doc in manifest["documents"]:
        original = confined(root, doc["original"])
        if hashlib.sha256(original.read_bytes()).hexdigest() != doc["sha256"]:
            raise ValueError("Original hash mismatch")
        extraction = confined(root, doc["extraction"])
        if hashlib.sha256(extraction.read_bytes()).hexdigest() != doc["extraction_sha256"]:
            raise ValueError("Extraction hash mismatch")
        rows = json.loads(extraction.read_text(encoding="utf-8"))
        for row in rows:
            if hashlib.sha256(row["text"].encode()).hexdigest() != row["text_sha256"]:
                raise ValueError("Page text hash mismatch")
            if row.get("preview_sha256"):
                preview = confined(root, row["preview"])
                if hashlib.sha256(preview.read_bytes()).hexdigest() != row["preview_sha256"]:
                    raise ValueError("Preview hash mismatch")
        pages[doc["id"]] = rows
    for concept in manifest["concepts"]:
        for ref in concept["passages"]:
            if not any(
                p["id"] == ref and p["status"] == "disponible" for rows in pages.values() for p in rows
            ):
                raise ValueError("Concept maps to unavailable passage")
    return manifest, pages


def create_app(
    package=PACKAGE,
    web_root=None,
    manifest_name=MANIFEST,
    retrieval=None,
    retrieval_strategy="lexical",
    study_lab=False,
    study_provider=None,
    web_evidence=None,
    study_chat=False,
):
    if study_chat and (
        not study_lab
        or not (
            getattr(study_provider, "reviewed", False)
            or getattr(study_provider, "diagnostic_label", "").startswith("FIXTURE")
        )
    ):
        raise ValueError("Study chat requires reviewed runtime or explicit CPU fixture")
    manifest, pages = load_package(package, manifest_name)
    app = FastAPI(title="ORALIA — consulta documental aislada", docs_url=None, redoc_url=None)
    manager = LocalAccess()
    # Cookies are host-scoped, not port-scoped: opt-in versions must not revoke v1 grants.
    suffix = (
        ""
        if manifest_name == MANIFEST
        else "_" + hashlib.sha256(manifest["package_id"].encode()).hexdigest()[:12]
    )
    if study_lab:
        if retrieval is None or manifest_name not in {PACKAGES[v][1] for v in STUDY_PACKAGES}:
            raise ValueError("Study inspection requires explicit v2/v3 retrieval")
        if retrieval.manifest["package_id"] != manifest["package_id"]:
            raise ValueError("Foreign retrieval package")
        if retrieval.package.resolve() != package.resolve():
            raise ValueError("Foreign retrieval root")
        suffix += "_study_lab"
    manager.cookie_names = (f"oralia_documentary_teacher{suffix}", f"oralia_documentary_unused{suffix}")
    cookie = manager.cookie_names[0]

    def close_study(token):
        return None

    if study_lab:
        from oralia.documentary.study_lab_api import install_study_lab

        close_study = install_study_lab(
            app,
            manager,
            cookie,
            retrieval,
            study_provider,
            web_evidence=web_evidence,
            student_view=study_chat,
        )
        if hasattr(study_provider, "lifespan"):
            previous_lifespan = app.router.lifespan_context

            @asynccontextmanager
            async def real_lifespan(application):
                async with study_provider.lifespan(application):
                    async with previous_lifespan(application):
                        yield

            app.router.lifespan_context = real_lifespan

    from oralia.documentary.public_access import PublicAccess

    public_access = PublicAccess.from_env()

    @app.middleware("http")
    async def local_readonly(request: Request, call_next):
        from fastapi.responses import JSONResponse

        release = None
        try:
            outside = public_access is not None and public_access.is_public(request)
            if outside:
                public_access.check_transport(request)
                if public_access.blocked(request.url.path) or request.url.path == "/tecnica":
                    raise HTTPException(404, "Not found")
            else:
                _local_transport(request)
            if (
                request.method not in {"GET", "HEAD"}
                and request.url.path
                not in {
                    "/documentary/enter",
                    "/documentary/leave",
                }
                and not (study_lab and request.url.path.startswith("/api/v1/study-lab/"))
            ):
                raise HTTPException(405, "Read-only documentary profile")
            if request.url.path.startswith("/api/"):
                grant = manager.resolve(request.cookies.get(cookie, ""))
                if grant is None or grant.role != "teacher":
                    raise HTTPException(401, "Entre en la consulta documental local")
                if outside and request.url.path == "/api/v1/study-lab/turn":
                    release = public_access.admit_turn(request.cookies.get(cookie, ""))
            result = await call_next(request)
        except HTTPException as exc:
            result = JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        finally:
            if release is not None:
                release()
        result.headers["Cache-Control"] = "no-store"
        result.headers["X-Content-Type-Options"] = "nosniff"
        result.headers["Referrer-Policy"] = "no-referrer"
        # No external network resources, including from saved HTML/PDF references.
        result.headers["Content-Security-Policy"] = (
            "default-src 'self'; connect-src 'self'; img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; object-src 'self'; frame-src "
            "'self'; frame-ancestors 'self'"
        )
        return result

    @app.post("/documentary/enter")
    async def enter(request: Request, response: Response):
        outside = public_access is not None and public_access.is_public(request)
        email = public_access.identity(request) if outside else None  # sin identidad válida no hay concesión
        old = request.cookies.get(cookie, "")
        if old:
            close_study(old)
            manager.revoke(old)
            if public_access is not None:
                public_access.forget(old)
        token = manager.issue("teacher")
        if outside:
            public_access.register(email, token, manager)
        response.set_cookie(cookie, token, httponly=True, samesite="strict", max_age=3600, secure=outside)
        return {
            "role": "local_document_reader",
            "profile": "retrieval_cpu" if retrieval else "read_only_no_models",
        }

    @app.post("/documentary/leave")
    async def leave(request: Request, response: Response):
        close_study(request.cookies.get(cookie, ""))
        manager.revoke(request.cookies.get(cookie, ""))
        if public_access is not None:
            public_access.forget(request.cookies.get(cookie, ""))
        response.delete_cookie(cookie)
        return {"closed": True}

    @app.get("/api/v1/documentary")
    def catalog():
        result = {**manifest, "retrieval": retrieval is not None}
        result["study_chat"] = study_chat
        if study_lab:
            result["study_lab"] = True
            result["study_provider"] = getattr(
                study_provider,
                "diagnostic_label",
                "disconnected" if study_provider is None else "local_generation_port",
            )
            result["study_workflow_deadline_seconds"] = getattr(
                study_provider, "diagnostic_deadline_seconds", 50
            )
            if hasattr(study_provider, "runtime_status"):
                result["study_runtime"] = study_provider.runtime_status()
            from oralia.documentary.study_budget import study_budget

            result["study_budget"] = study_budget(
                getattr(study_provider, "study_budget_profile", "historical/v1")
            ).public()
        if retrieval is not None:
            result["scope"] = (
                "Corpus v2 revisado con huecos explícitos. Recuperación CPU aislada; "
                "suficiencia no evaluada, sin tutor generativo."
            )
            if getattr(study_provider, "diagnostic_label", "").startswith("REAL_"):
                result["scope"] = (
                    "Corpus v2 revisado con huecos explícitos. Recuperación CPU e inspección "
                    "docente con modelo local GPU; contenido no verificado. Participante cerrado."
                )
        return result

    @app.get("/api/v1/retrieval")
    def retrieve(request: Request, question: str, reference: str = "", focus_change: bool = False):
        if retrieval is None:
            raise HTTPException(404, "Recuperación no activada en este perfil")
        try:
            result = retrieval.query(
                question,
                strategy=retrieval_strategy,
                history=[reference] if reference else [],
                focus_change=focus_change,
            )
            grant = manager.resolve(request.cookies.get(cookie, ""))
            if grant is None or grant.role != "teacher":
                raise HTTPException(401, "Consulta cerrada durante la recuperación")
            return result
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.get("/api/v1/documentary/{doc_id}/pages")
    def document_pages(doc_id: str):
        if doc_id not in pages:
            raise HTTPException(404, "Unknown document")
        return pages[doc_id]

    @app.get("/api/v1/documentary/{doc_id}/original")
    def original(doc_id: str):
        doc = next((d for d in manifest["documents"] if d["id"] == doc_id), None)
        if doc is None:
            raise HTTPException(404, "Unknown document")
        # HTML archives remain inert downloads; never execute captured third-party JS.
        path = confined(package, doc["original"])
        return FileResponse(
            path,
            filename=path.name,
            content_disposition_type="inline" if path.suffix == ".pdf" else "attachment",
        )

    @app.get("/api/v1/documentary/{doc_id}/preview/{page}")
    def preview(doc_id: str, page: int):
        row = next((p for p in pages.get(doc_id, []) if p["page"] == page), None)
        if row is None or not row.get("preview"):
            raise HTTPException(404, "No reviewed preview for this page")
        return FileResponse(confined(package, row["preview"]))

    @app.get("/health")
    async def health():
        result = {
            "status": "ok",
            "profile": "retrieval_cpu" if retrieval else "documentary",
            "package": manifest["package_id"],
            "models": retrieval is not None,
        }
        report = getattr(study_provider, "health_report", None)
        if report is not None:
            services = await report()
            if retrieval is not None and hasattr(retrieval, "client"):
                try:
                    retrieval.client.get(retrieval.url + "/health", timeout=3).raise_for_status()
                    services["ranking"] = True
                except Exception:
                    services["ranking"] = False
            result["services"] = services
            if not all(services.values()):
                result["status"] = "degraded"
        if public_access is not None:
            result["turns_in_progress"] = sum(1 for busy in public_access.in_flight.values() if busy)
            result["students"] = len(public_access.by_email)
        return result

    @app.get("/")
    def home():
        return RedirectResponse("/tecnica?documental=1")

    if web_root is not None:
        app.mount("/assets", StaticFiles(directory=web_root / "assets"), name="assets")

        @app.get("/tecnica")
        def technical():
            return FileResponse(web_root / "index.html")

        if study_chat:

            @app.get("/estudio")
            def student_chat():
                return FileResponse(web_root / "index.html")

    return app


def main():
    parser = argparse.ArgumentParser(description="Consulta documental local sin modelos ni índices")
    parser.add_argument("--port", type=int, default=8022)
    parser.add_argument("--web-root", type=Path, help="Build web aislado; no sustituye builds anteriores")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--package", choices=PACKAGES, default="v1.1")
    parser.add_argument(
        "--retrieval", action="store_true", help="Recuperación v2.1 CPU aislada ya construida"
    )
    parser.add_argument("--retrieval-root", type=Path, help="Índice CPU aislado ya construido")
    parser.add_argument(
        "--modern-retrieval",
        action="store_true",
        help="Ordena con bge-m3 y reranker Qwen3 (caché local, GPU si hay); requiere --retrieval",
    )
    parser.add_argument("--study-lab", action="store_true", help="Inspección docente v2, LLM desconectado")
    parser.add_argument(
        "--web-policy",
        "--activity-policy",
        dest="web_policy",
        type=Path,
        help="Política explícita de actividad y permiso web independiente",
    )
    parser.add_argument(
        "--local-first-provider",
        action="store_true",
        help="Revisar el borrador local antes de ampliar; requiere proveedor revisado",
    )
    parser.add_argument("--test-provider", action="store_true", help="Fixture CPU explícito, sin LLM")
    parser.add_argument("--real-provider", action="store_true", help="Qwen14B NF4 docente real, optativo")
    parser.add_argument(
        "--reviewed-provider", action="store_true", help="Generación 14B y revisión Qwen3 con razonamiento"
    )
    parser.add_argument(
        "--llama-provider",
        action="store_true",
        help="Generador y revisor en servidores llama.cpp locales (modo con aviso); sin cargar modelos",
    )
    parser.add_argument(
        "--llama-concurrency", type=int, default=4, help="Turnos simultáneos (huecos de los servidores llama.cpp)"
    )
    parser.add_argument("--llama-generator-url", default="http://127.0.0.1:8090")
    parser.add_argument("--llama-reviewer-url", default="http://127.0.0.1:8089")
    parser.add_argument(
        "--notice-review",
        action="store_true",
        help="Revisión compacta: la respuesta se muestra siempre, con aviso del tipo de posible error",
    )
    parser.add_argument(
        "--study-chat", action="store_true", help="Vista simple de autoestudio, con contexto automático"
    )
    parser.add_argument("--runtime-output", type=Path)
    parser.add_argument(
        "--experimental-limits", action="store_true", help="Cupos de ensayo; no límite educativo"
    )
    parser.add_argument("--trial-clock", type=Path)
    parser.add_argument("--runtime-seconds", type=int, default=900)
    parser.add_argument(
        "--study-budget", choices=["historical/v1", "study-expanded/v1"], default="historical/v1"
    )
    parser.add_argument("--study-coverage", action="store_true", help="Selección comparativa CPU optativa")
    args = parser.parse_args()
    if args.llama_provider:
        args.real_provider = args.reviewed_provider = args.notice_review = True
    if args.reviewed_provider:
        args.real_provider = True
    if args.study_chat and (not args.study_lab or not (args.reviewed_provider or args.test_provider)):
        parser.error("--study-chat requiere study-lab y reviewed-provider o fixture explícito")
    if args.retrieval_root and not args.retrieval:
        parser.error("--retrieval-root requiere --retrieval")
    if args.web_policy and not args.study_lab:
        parser.error("--web-policy requiere --study-lab; no existe permiso web para examen")
    if args.modern_retrieval and not args.retrieval:
        parser.error("--modern-retrieval requiere --retrieval")
    if args.notice_review and not args.reviewed_provider:
        parser.error("--notice-review requiere --reviewed-provider")
    if args.local_first_provider and not (args.real_provider and args.reviewed_provider):
        parser.error("--local-first-provider requiere --real-provider y --reviewed-provider")
    if args.local_first_provider and not args.web_policy:
        parser.error("--local-first-provider requiere --web-policy para vincular el alcance de la actividad")
    if args.study_coverage and not args.study_lab:
        parser.error("--study-coverage requiere --study-lab")
    if args.study_budget != "historical/v1" and not args.real_provider:
        parser.error("--study-budget ampliado requiere --real-provider")
    if args.study_lab and (args.package not in STUDY_PACKAGES or not args.retrieval):
        parser.error("--study-lab requiere --package v2 --retrieval")
    if args.test_provider and not args.study_lab:
        parser.error("--test-provider requiere --study-lab")
    if args.real_provider and (not args.study_lab or args.test_provider or args.runtime_output is None):
        parser.error("--real-provider requires study-lab, exclusive runtime-output and no fixture")
    web_root = args.web_root or WORKSPACE / "apps/web/dist"
    if not (web_root / "index.html").is_file():
        parser.error("Falta apps/web/dist; compile la web con el Node local instalado")
    # Bind first and retain the socket: an occupied port is never reused or killed.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind(("127.0.0.1", args.port))
        listener.listen(128)
        package, manifest_name = PACKAGES[args.package]
        retrieval = None
        if args.retrieval:
            if args.package not in STUDY_PACKAGES:
                parser.error("--retrieval requiere --package v2 o v3")
            from oralia.documentary.retrieval import Retrieval

            retrieval_options = {"root": args.retrieval_root} if args.retrieval_root else {}
            retrieval_options["selection_profile"] = "comparison-coverage/v1" if args.study_coverage else None
            if args.modern_retrieval:
                from oralia.documentary.modern_retrieval import ModernRetrieval

                retrieval = ModernRetrieval(**retrieval_options)
            else:
                retrieval = Retrieval(**retrieval_options)
        provider = _fixture_provider() if args.test_provider else None
        if args.test_provider and args.experimental_limits:
            from oralia.documentary.study_lab import TrialBudget

            provider.trial_budget = TrialBudget()
        if args.real_provider:
            from oralia.documentary.real_study_provider import RealStudyProvider

            clock = json.loads(args.trial_clock.read_text(encoding="utf-8-sig")) if args.trial_clock else {}
            provider_class = RealStudyProvider
            llama_options = {}
            if args.llama_provider:
                from oralia.documentary.llama_study_provider import LlamaStudyProvider

                provider_class = LlamaStudyProvider
                llama_options = dict(
                    generator_url=args.llama_generator_url,
                    reviewer_url=args.llama_reviewer_url,
                    concurrency=args.llama_concurrency,
                )
            provider = provider_class(
                **llama_options,
                output=args.runtime_output,
                started=clock.get("started_monotonic"),
                seconds=args.runtime_seconds,
                academic_calls_used=clock.get("academic_calls_used", 0),
                study_budget_profile=args.study_budget,
                reviewed=args.reviewed_provider,
                experimental_limits=args.experimental_limits or not args.study_chat,
                local_first=args.local_first_provider,
                notice_review=args.notice_review,
            )
        web_evidence = None
        if args.web_policy:
            from oralia.documentary.web_evidence import load_web_evidence

            web_evidence = load_web_evidence(args.web_policy)
            if args.local_first_provider and web_evidence.activity_scope is None:
                parser.error("La política debe declarar activity_scope explícito para --local-first-provider")
        app = create_app(
            package=package,
            web_root=web_root,
            manifest_name=manifest_name,
            retrieval=retrieval,
            retrieval_strategy="lexical",
            study_lab=args.study_lab,
            study_provider=provider,
            web_evidence=web_evidence,
            study_chat=args.study_chat,
        )
        url = f"http://127.0.0.1:{args.port}/tecnica?documental=1"
        if args.study_chat:
            url = f"http://127.0.0.1:{args.port}/estudio"
        print(
            f"ORALIA documental: {url}\nPaquete: {package}\n"
            + (
                (
                    "Recuperación CPU; inspección docente GPU optativa, participante cerrado. "
                    if args.real_provider
                    else "Recuperación CPU aislada; sin generación ni participantes. "
                )
                if retrieval
                else "Solo lectura; sin modelos, vectores o sesiones de participante. "
            )
            + "Ctrl+C detiene este servidor.",
            flush=True,
        )
        if args.study_lab:
            print(
                "Inspección unverified/not_assessed. Proveedor: "
                + (getattr(provider, "diagnostic_label", "DESCONECTADO; no carga LLM")),
                flush=True,
            )
        if not args.no_browser:
            webbrowser.open(url)
        server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=args.port, access_log=False))
        app.state.request_shutdown = lambda: setattr(server, "should_exit", True)
        try:
            server.run(sockets=[listener])
        except KeyboardInterrupt:
            # Uvicorn has already completed lifespan shutdown on Ctrl+C.
            pass


if __name__ == "__main__":
    main()
