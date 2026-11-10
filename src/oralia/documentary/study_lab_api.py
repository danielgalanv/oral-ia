"""Local teacher inspection permission, independent of semantic publication."""

import asyncio
import copy
import json
import time
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field

from oralia.documentary.study_budget import study_budget
from oralia.documentary.study_errors import StudyFailure
from oralia.documentary.study_lab import DiagnosticStudy, TrialBudget, request_identifier
from oralia.documentary.study_report import markdown_report, session_report
from oralia.documentary.web_evidence import LocalGap
from oralia.documentary.web_review import review_web


class OpenInspection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ephemeral_inspection_consent: bool


class TurnInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(max_length=36)
    question: str = Field(min_length=1, max_length=2000)
    focus_change: bool | None = None


class WebInspectionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(max_length=36)
    local_receipt: str = Field(max_length=36)
    concept: str = Field(max_length=80)
    # Explicit teacher diagnostic decision, never inferred from retrieval score.
    confirmed_in_scope_gap: bool
    notice_shown: bool


def install_study_lab(app, manager, cookie, retrieval, provider, *, web_evidence=None, student_view=False):
    sessions = {}
    budget = TrialBudget(maximum=None if student_view else 8)
    budget = getattr(provider, "trial_budget", budget)
    sweeper = None

    def visible_receipt(row):
        if not student_view:
            return row
        result = {
            k: row.get(k)
            for k in (
                "id",
                "question",
                "status",
                "diagnostic_preview",
                "failure_code",
                "provider_kind",
                "web_sources",
                "review_notice",
            )
        }
        result["retrieval"] = {
            "passages": [
                {k: p[k] for k in ("filename", "page", "original_url")}
                for p in row.get("retrieval", {}).get("passages", [])
            ]
        }
        return result

    def close(token):
        session = sessions.pop(token, None)
        if session:
            session.close()

    def authorized(token):
        grant = manager.resolve(token)
        return bool(grant and grant.role == "teacher")

    def runtime_status():
        return provider.runtime_status() if hasattr(provider, "runtime_status") else None

    def check_runtime(token):
        status = runtime_status()
        if status is not None and status["expired"]:
            close(token)
            raise HTTPException(
                410,
                {
                    "code": "runtime_expired",
                    "message": "El runtime global ha caducado; requiere un nuevo arranque explícito.",
                },
            )

    def state_fields():
        web_enabled = False
        if web_evidence:
            try:
                web_evidence.check()
                web_enabled = True
            except ValueError:
                pass
        return {
            "web": {
                "enabled": web_enabled,
                "concepts": list(web_evidence.policy.concepts) if web_evidence else [],
                "policy_version": web_evidence.policy.version if web_evidence else None,
                "semantic_review": "unavailable",
            },
            "runtime": runtime_status(),
            "inspection_lease_seconds": 15,
            "provider_ready": getattr(provider, "ready", True),
            "provider_preparing": getattr(provider, "preparing", False),
            "quota": budget.status(),
            "study_budget": study_budget(getattr(provider, "study_budget_profile", "historical/v1")).public(),
        }

    def get(request):
        token = request.cookies.get(cookie, "")
        if not authorized(token):
            close(token)
            raise HTTPException(
                401, {"code": "permission_expired", "message": "Permiso docente cerrado o caducado."}
            )
        check_runtime(token)
        session = sessions.get(token)
        if session is None:
            raise HTTPException(
                409, {"code": "inspection_closed", "message": "Abra inspección temporal con consentimiento."}
            )
        lease_expired = time.monotonic() - session.last_seen > 15
        try:
            session.validate()
        except ValueError as error:
            close(token)
            raise HTTPException(
                409,
                {
                    **(
                        error.detail()
                        if isinstance(error, StudyFailure)
                        else {
                            "code": "lease_expired" if lease_expired else "inspection_invalidated",
                            "message": "La inspección se invalidó por una causa técnica.",
                        }
                    ),
                },
            ) from None
        return session

    @app.post("/api/v1/study-lab/open")
    async def open_inspection(request: Request, body: OpenInspection):
        token = request.cookies.get(cookie, "")
        if not body.ephemeral_inspection_consent or not authorized(token):
            raise HTTPException(403, "Permiso de inspección temporal requerido")
        check_runtime(token)
        close(token)
        session = DiagnosticStudy(
            retrieval,
            provider,
            authority=lambda: authorized(token),
            budget=budget,
            course="ingenieria-software",
            activity="requirements-teacher-diagnostic-v2",
            lease_seconds=15,
            attempt_limit=None if student_view else 32,
        )
        if student_view and web_evidence is not None:
            if not hasattr(session.provider, "configure_web"):
                raise HTTPException(409, "Connected web requires reviewed runtime")
            session.provider.configure_web(web_evidence, retrieval, session.binding[3], session.notify_web)
        try:
            session.validate()
        except ValueError as error:
            check_runtime(request.cookies.get(cookie, ""))
            if isinstance(error, StudyFailure):
                raise HTTPException(409, error.detail()) from None
            raise HTTPException(409, str(error)) from None
        sessions[token] = session
        return {
            "inspection_authority": "local_teacher_diagnostic_only",
            "binding": session.binding,
            "semantic_support": "unverified",
            "sufficiency": "not_assessed",
            "publication_allowed": False,
            "retention": "ephemeral_memory_until_close_or_expiry",
            "provider": getattr(
                provider, "diagnostic_label", "disconnected" if provider is None else "local"
            ),
            **state_fields(),
        }

    @app.post("/api/v1/study-lab/turn")
    async def turn(request: Request, body: TurnInput):
        try:
            session = get(request)
            result = await session.turn(
                body.question,
                request_identifier(body.id),
                focus_change=None if student_view else body.focus_change,
            )
            check_runtime(request.cookies.get(cookie, ""))
            return {**result, **state_fields()}
        except ValueError as error:
            check_runtime(request.cookies.get(cookie, ""))
            if isinstance(error, StudyFailure):
                raise HTTPException(409, error.detail()) from None
            raise HTTPException(409, str(error)) from None

    @app.post("/api/v1/study-lab/web-inspect")
    async def web_inspect(request: Request, body: WebInspectionInput):
        session = get(request)
        if web_evidence is None:
            raise HTTPException(409, "Actividad offline; no se realiza acceso a Internet")
        if session.task is not None or session.pending is not None:
            raise HTTPException(409, "Hay una petición o entrega pendiente")
        if not body.confirmed_in_scope_gap or not body.notice_shown:
            raise HTTPException(409, "Confirme alcance, insuficiencia y aviso visible")
        identifier = request_identifier(body.id)
        local_id = request_identifier(body.local_receipt)
        if local_id not in session.receipts:
            raise HTTPException(409, "Se requiere un recibo local de esta inspección")
        if web_evidence.policy.activity != session.binding[3]:
            raise HTTPException(409, "Política de otra actividad")
        gap = LocalGap(
            session.binding[3],
            body.concept,
            "in_scope",
            "insufficient",
            identifier,
            "teacher_diagnostic_attestation",
            "Explicit inspection decision; not autonomous semantic assessment",
            local_id,
        )

        async def visible_notice(_):
            session.validate()
            return body.notice_shown

        session.task = asyncio.current_task()
        try:
            result = await web_evidence.acquire(identifier, gap, visible_notice)
            session.validate()
            # All available active pages, independently of the initial retrieval.
            pages = {
                key: value["text"]
                for key, value in retrieval.pages.items()
                if value["status"] == "disponible"
            }
            gaps = [key for key, value in retrieval.pages.items() if value["status"] != "disponible"]
            result["review"] = await review_web(result["documents"], pages, coverage_gaps=gaps)
            session.validate()
            try:
                web_evidence.check()
            except ValueError:
                result["documents"] = []
                result["status"] = "unavailable_before_delivery"
            # No external text reaches the generator or the confirmed conversation.
            return result
        except ValueError as error:
            raise HTTPException(409, str(error)) from None
        finally:
            session.task = None

    @app.get("/api/v1/study-lab/state")
    async def state(request: Request):
        session = get(request)
        return {
            "web_notice": session.web_notice,
            "active": True,
            "semantic_support": "unverified",
            "publication_allowed": False,
            **state_fields(),
        }

    @app.get("/api/v1/study-lab/partial")
    async def partial(request: Request):
        """Text of the answer being written (before its review), for the student's own session only."""
        session = get(request)
        provider_session = session.provider
        running = session.task is not None
        return {
            "phase": getattr(provider_session, "phase", "idle") if running else "idle",
            "text": (getattr(provider_session, "partial", "") or "") if running else "",
        }

    @app.post("/api/v1/study-lab/web-notice/{identifier}/shown")
    async def web_notice_shown(request: Request, identifier: str):
        try:
            get(request).acknowledge_web_notice(request_identifier(identifier))
            return {"shown": True}
        except ValueError as error:
            raise HTTPException(409, str(error)) from None

    @app.post("/api/v1/study-lab/prepare")
    async def prepare(request: Request):
        session = get(request)
        if not hasattr(provider, "request_prepare"):
            raise HTTPException(409, "Este proveedor no necesita recarga")
        if budget.maximum is not None and budget.used >= budget.maximum:
            raise HTTPException(409, StudyFailure("budget_exhausted").detail())
        try:
            provider.request_prepare(session.validate)
        except ValueError as error:
            raise HTTPException(409, str(error)) from None
        return state_fields()

    @app.get("/api/v1/study-lab/export")
    async def export_session(request: Request, format: Literal["json", "markdown"] = "json"):
        report = session_report(get(request))
        text = (
            json.dumps(report, ensure_ascii=False, indent=2) if format == "json" else markdown_report(report)
        )
        extension = "json" if format == "json" else "md"
        return Response(
            text,
            media_type="application/json" if format == "json" else "text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="oralia-{report["session_code"]}.{extension}"',
                "Cache-Control": "no-store",
            },
        )

    @app.get("/api/v1/study-lab/resume")
    async def resume(request: Request):
        session = get(request)
        # One event-loop snapshot: only acknowledged messages become history.
        messages = [visible_receipt(copy.deepcopy(row)) for row in session.receipts.values() if row["shown"]]
        candidate = None
        if session.pending:
            try:
                candidate = visible_receipt(session.display(session.pending))
            except StudyFailure:
                pass  # A revoked pending external answer is not recoverable; shown history remains.
        return {
            "messages": messages,
            "candidate": candidate,
            "busy": session.task is not None,
            **state_fields(),
        }

    @app.get("/api/v1/study-lab/{identifier}/display")
    async def display(request: Request, identifier: str):
        try:
            return visible_receipt(get(request).display(request_identifier(identifier)))
        except (KeyError, ValueError) as error:
            raise HTTPException(409, str(error)) from None

    @app.get("/api/v1/study-lab/{identifier}/receipt")
    async def receipt(request: Request, identifier: str):
        try:
            return visible_receipt(get(request).receipt(request_identifier(identifier)))
        except (KeyError, ValueError) as error:
            raise HTTPException(409, str(error)) from None

    @app.post("/api/v1/study-lab/{identifier}/shown")
    async def shown(request: Request, identifier: str):
        try:
            return get(request).acknowledge(request_identifier(identifier))
        except (KeyError, ValueError) as error:
            raise HTTPException(409, str(error)) from None

    @app.post("/api/v1/study-lab/cancel")
    async def cancel(request: Request):
        get(request).cancel()
        return {"cancelled": True}

    @app.post("/api/v1/study-lab/close")
    async def close_inspection(request: Request):
        close(request.cookies.get(cookie, ""))
        return {"closed": True, "content_purged": True}

    async def sweep():
        while True:
            await asyncio.sleep(1)
            for token in list(sessions):
                if not authorized(token) or time.monotonic() - sessions[token].last_seen > 15:
                    close(token)

    async def startup():
        nonlocal sweeper
        sweeper = asyncio.create_task(sweep())

    async def shutdown():
        if sweeper:
            sweeper.cancel()
            await asyncio.gather(sweeper, return_exceptions=True)
        for token in list(sessions):
            close(token)

    previous_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(application):
        async with previous_lifespan(application):
            await startup()
            try:
                yield
            finally:
                await shutdown()

    app.router.lifespan_context = lifespan
    return close
