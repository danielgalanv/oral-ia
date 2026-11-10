"""Local page for the teacher to evaluate the logged review notices.

Separate from the student chat on purpose: the log holds the students' questions, so this server listens only on
127.0.0.1 and is started by the teacher:  python -m oralia.documentary.notice_review_app [--port 8038]
"""

import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from oralia.documentary import notice_review

PAGE = (Path(__file__).with_name("notice_review_page.html")).read_text(encoding="utf8")
LOCAL_HOSTS = {"127.0.0.1", "localhost"}


class Mark(BaseModel):
    veredicto: str
    nota: str = Field(default="", max_length=1000)


def create_review_app(directory=None):
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    def local_only(request: Request):
        host = (request.headers.get("host") or "").rsplit(":", 1)[0]
        origin = request.headers.get("origin")
        if host not in LOCAL_HOSTS or (origin and origin.split("://")[-1].rsplit(":", 1)[0] not in LOCAL_HOSTS):
            raise HTTPException(403, "Solo acceso local")

    @app.get("/", response_class=HTMLResponse)
    async def page(request: Request):
        local_only(request)
        return HTMLResponse(PAGE, headers={"Cache-Control": "no-store"})

    @app.get("/api/avisos")
    async def list_notices(request: Request):
        local_only(request)
        return {"avisos": notice_review.notices(directory), "resumen": notice_review.summary(directory)}

    @app.post("/api/avisos/{identifier}/marca")
    async def mark(request: Request, identifier: str, body: Mark):
        local_only(request)
        try:
            return notice_review.mark(identifier, body.veredicto, body.nota, directory)
        except KeyError:
            raise HTTPException(404, "Aviso desconocido") from None
        except ValueError:
            raise HTTPException(422, "Veredicto no válido") from None

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8038)
    port = parser.parse_args().port
    print(f"Revisión docente de avisos: http://127.0.0.1:{port}  (Ctrl+C para parar)", flush=True)
    uvicorn.run(create_review_app(), host="127.0.0.1", port=port, access_log=False)


if __name__ == "__main__":
    main()
