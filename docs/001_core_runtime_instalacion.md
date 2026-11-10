# Feature 001 — Núcleo cognitivo y ejecución local: instalación, ejecución, pruebas

Documentación operativa de la Feature 001, exigida por
`docs/ORAL-IA_SpecKit/13_definition_of_done.md`. Complementa (no sustituye)
`specs/001-core-cognitive-runtime/quickstart.md`, que detalla los escenarios de
validación A–E.

## Requisitos

- Python 3.12 (gestionado con [`uv`](https://docs.astral.sh/uv/)).
- Node.js 18+ y npm, **solo** si se quiere ejecutar `apps/web` o las pruebas Playwright
  (`tests/e2e/`). El backend y toda la suite de pytest funcionan sin Node.

## Instalación

```bash
uv sync --extra dev
PYTHONPATH=src uv run alembic upgrade head
```

Para el cliente web (opcional, requiere Node):

```bash
cd apps/web
npm install
```

## Configuración

- `ORALIA_DB_URL`: URL de conexión SQLAlchemy (por defecto `sqlite:///./oralia.db`, modo
  WAL activado automáticamente — `src/oralia/infrastructure/db/engine.py`).
- No existen otras variables de entorno obligatorias en esta feature: no hay integración
  con LLM, RAG ni voz (fuera de alcance — ver `spec.md`).

## Ejecución

```bash
PYTHONPATH=src uv run python -m oralia.scripts.seed_demo   # datos de demostración
PYTHONPATH=src uv run uvicorn oralia.interfaces.api.app:app --host 127.0.0.1 --port 8000
```

o, equivalentemente, `uv run python apps/api/main.py`.

Con Node disponible, en otra terminal:

```bash
cd apps/web && npm run dev
```

La API se vincula únicamente a `127.0.0.1` por defecto (FR-022) — nunca a `0.0.0.0`.

## Pruebas

```bash
PYTHONPATH=src uv run pytest tests/ -q                 # unit + contract + integration + failure
PYTHONPATH=src uv run pytest tests/ -m contract -q     # solo pruebas de contrato
PYTHONPATH=src uv run pytest tests/ -m failure -q      # solo pruebas de fallo/degradación
uv run ruff check src/ tests/                            # lint
```

Las pruebas e2e (`tests/e2e/*.spec.ts`, Playwright) están escritas pero **no se han
podido ejecutar en este entorno de desarrollo** porque no hay Node.js instalado; véase
"Limitaciones" más abajo.

## Limitaciones conocidas

- **Sin verificación de Node/Playwright/frontend en este entorno**: el código de
  `apps/web` (React/TS) y `tests/e2e/test_scenario_a.spec.ts` se escribieron siguiendo
  los mismos contratos que el backend, pero no se han instalado ni ejecutado con
  `npm`/Playwright aquí. Antes de considerar la feature verificada de extremo a extremo
  con interfaz real, deben ejecutarse en un entorno con Node.js.
- **Interpretación determinista, no un LLM real** (research.md §2): el agente
  `Interpreter` es una heurística fija; la comprensión de lenguaje natural real llega en
  features posteriores.
- **Validación de esquema de salida por agente**: se apoya en valores por defecto
  (`dict.get(..., default)`) y en la captura de excepciones (`cancellation.py`), no en un
  validador de JSON Schema formal — proporcional al alcance de esta feature
  (Constitución Principio XI).
- **Accesibilidad**: se aplicaron etiquetas, navegación por teclado, mensajes de error
  comprensibles y contraste básico (FR-025), pero no se ha ejecutado una auditoría
  automatizada (p. ej. axe-core) por la misma falta de Node.
- **Concurrencia**: una única sesión interactiva activa por instancia (FR-012a); no se
  ha probado con múltiples procesos o workers concurrentes, solo con un único proceso
  Python (research.md §3).

## Datos de ejemplo

`src/oralia/scripts/seed_demo.py` crea 1 `Course`, 1 `RetentionPolicy`, 1
`ActivityConfiguration`, 5 agentes de prueba bajo un mismo `AgentContract` y 2 agencias
que los reutilizan (SC-001, SC-002) — usado también por `quickstart.md`.
