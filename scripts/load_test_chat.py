"""Prueba de carga del chat de autoestudio: N alumnos simultáneos, cada uno con su sesión (proyecto venv).

    python scripts/load_test_chat.py --url http://127.0.0.1:8037 --students 10 --turns 3 [--think 0]

Cada alumno entra, abre sesión, mantiene la conexión (como el navegador, cada 3 s) y hace sus preguntas una tras
otra (con una pausa de `--think` segundos entre respuesta y pregunta). Todos arrancan a la vez: es el peor caso
(10 preguntas en el mismo instante). Muestra latencia por turno (media, p50, p95, máx.), fallos y turnos por minuto.
"""

import argparse
import asyncio
import json
import statistics
import time
import uuid
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = [
    "¿Qué es un requisito no funcional y qué ejemplos hay?",
    "¿Para qué sirve la trazabilidad de requisitos?",
    "¿Cómo se validan los requisitos con el cliente?",
    "¿Qué diferencia hay entre requisitos de usuario y de sistema?",
    "¿Qué técnicas existen para elicitar requisitos?",
    "¿Qué es un caso de uso y para qué sirve en ingeniería de requisitos?",
    "¿Qué es la gestión de cambios en los requisitos?",
    "¿Cuál es el propósito de un prototipo en la ingeniería de requisitos?",
    "¿Qué significa que un requisito sea verificable?",
    "¿Qué es una especificación tabular y cuándo se usa?",
    "¿Cómo se redacta un buen requisito funcional?",
    "¿Qué actividades generales hay en todos los procesos de ingeniería de requisitos?",
]


async def student(index, url, turns, think, results, errors):
    async with httpx.AsyncClient(base_url=url, timeout=600) as client:
        entered = await client.post("/documentary/enter")
        entered.raise_for_status()
        opened = await client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True})
        opened.raise_for_status()
        alive = True

        async def keepalive():
            while alive:
                try:
                    await client.get("/api/v1/study-lab/state")
                except httpx.HTTPError:
                    pass
                await asyncio.sleep(3)

        pinger = asyncio.create_task(keepalive())
        try:
            for turn in range(turns):
                question = QUESTIONS[(index * turns + turn) % len(QUESTIONS)]
                identifier = str(uuid.uuid4())
                started = time.monotonic()
                try:
                    response = await client.post("/api/v1/study-lab/turn", json={"id": identifier, "question": question})
                    response.raise_for_status()
                    result = response.json()
                    status = result["status"]
                    if status == "prepared_unverified":
                        shown = await client.get(f"/api/v1/study-lab/{result['id']}/display")
                        shown.raise_for_status()
                        await client.post(f"/api/v1/study-lab/{result['id']}/shown", json={})
                    results.append(dict(student=index, turn=turn, seconds=time.monotonic() - started, status=status, failure=result.get("failure_code")))
                except Exception as error:  # a failed turn is a result, not a crash of the test
                    errors.append(dict(student=index, turn=turn, error=f"{type(error).__name__}: {str(error)[:160]}"))
                    break
                await asyncio.sleep(think)
        finally:
            alive = False
            pinger.cancel()
            await asyncio.gather(pinger, return_exceptions=True)
            await client.post("/api/v1/study-lab/close")


def pct(values, q):
    values = sorted(values)
    return values[min(len(values) - 1, int(round(q * (len(values) - 1))))]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8037")
    parser.add_argument("--students", type=int, default=10)
    parser.add_argument("--turns", type=int, default=3)
    parser.add_argument("--think", type=float, default=0.0)
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    results, errors = [], []
    started = time.monotonic()
    await asyncio.gather(*[student(i, args.url, args.turns, args.think, results, errors) for i in range(args.students)])
    wall = time.monotonic() - started
    seconds = [r["seconds"] for r in results]
    ok = [r for r in results if r["status"] == "prepared_unverified"]
    summary = dict(
        students=args.students, turns_per_student=args.turns, think_s=args.think, wall_s=round(wall, 1),
        turns_done=len(results), turns_answered=len(ok), errors=len(errors),
        turns_per_minute=round(len(results) / wall * 60, 1) if wall else 0,
        latency_s=dict(mean=round(statistics.mean(seconds), 1), p50=round(pct(seconds, 0.5), 1), p95=round(pct(seconds, 0.95), 1), max=round(max(seconds), 1)) if seconds else None,
        statuses={s: sum(r["status"] == s for r in results) for s in {r["status"] for r in results}},
        failure_codes={f: sum(r["failure"] == f for r in results) for f in {r["failure"] for r in results if r["failure"]}},
        first_errors=errors[:3],
    )
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if args.out:
        Path(args.out).write_text(json.dumps(dict(summary=summary, results=results, errors=errors), ensure_ascii=False, indent=1), encoding="utf8")


asyncio.run(main())
