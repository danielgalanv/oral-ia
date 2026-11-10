"""FastAPI app factory. Binds to 127.0.0.1 only by default (FR-022) — see apps/api/main.py."""

from __future__ import annotations

import asyncio

from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from oralia.interfaces.api.deps.local_access import LocalAccess, access_guard
from oralia.interfaces.api.routers import (
    conversation,
    governance,
    materials,
    oral_defense,
    participante,
    self_study,
    session_recovery,
    teaching_units,
    tecnica,
)


def create_app(*, semantic_runtime=None) -> FastAPI:
    app = FastAPI(
        title="ORAL-IA — Núcleo cognitivo y ejecución local",
        version="0.1.0",
        description="Local-only API (127.0.0.1). No institutional integration (FR-022).",
    )
    app.state.local_access = LocalAccess()
    app.state.semantic_runtime = semantic_runtime
    app.state.interactive_operation_lock = asyncio.Lock()
    app.middleware("http")(access_guard)
    app.include_router(governance.router)
    app.include_router(session_recovery.router)
    app.include_router(conversation.router)
    app.include_router(teaching_units.router)
    app.include_router(participante.router)
    app.include_router(tecnica.router)
    app.include_router(materials.router)
    app.include_router(self_study.router)
    app.include_router(self_study.tecnica_router)
    app.include_router(oral_defense.router)
    app.include_router(oral_defense.tecnica_router)

    @app.exception_handler(RequestValidationError)
    async def safe_validation_error(request: Request, error: RequestValidationError):
        if request.url.path.startswith("/api/v1/auth/"):
            return JSONResponse(
                {"detail": "invalid authentication request"},
                status_code=422,
                headers={"Cache-Control": "no-store"},
            )
        return await request_validation_exception_handler(request, error)

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
