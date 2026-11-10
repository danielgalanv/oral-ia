# Feature 003 — Agencia de autoestudio: instalación, ejecución, pruebas

Documentación operativa de la Feature 003, exigida por
`docs/ORAL-IA_SpecKit/13_definition_of_done.md`. Extiende (no sustituye)
`docs/001_core_runtime_instalacion.md` y `docs/002_materials_rag_instalacion.md` — esta
feature añade capacidades al mismo proyecto `uv`, no crea uno nuevo. Complementa
`specs/003-self-study-agency/quickstart.md`, que detalla los escenarios de validación
A–G.

## Requisitos adicionales sobre las Features 001/002

- Los mismos de las Features 001/002 (Python 3.12/`uv`; Node.js 18+ solo para
  `apps/web`; modelo de embeddings cacheado localmente).
- **Ollama es completamente opcional.** Esta feature funciona íntegramente sin él — el
  `DeterministicGenerationAdapter` (extractivo, sin red, sin dependencias externas) es
  la reserva automática siempre disponible. Ollama solo se activa si se configura
  explícitamente `ORALIA_OLLAMA_MODEL` (ver más abajo).

## Instalación

```bash
uv sync --extra dev
PYTHONPATH=src uv run alembic upgrade head   # incluye la migración de esta feature
```

## Configuración

Todas las variables son opcionales — sin configurar ninguna, la feature funciona
íntegramente con el adaptador determinista (research.md §1).

| Variable | Por defecto | Notas |
|---|---|---|
| `ORALIA_OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | servidor Ollama local |
| `ORALIA_OLLAMA_MODEL` | *(sin valor)* | **obligatoria para activar Ollama** — si no está configurada, `ResponseGeneratorAgent`/`PracticeQuestionAgent` usan el adaptador determinista directamente, sin intentar contactar con Ollama |
| `ORALIA_OLLAMA_TIMEOUT_MS` | `6000` | |
| `ORALIA_OLLAMA_TEMPERATURE` | `0.2` | acotado a `[0.0, 1.0]` |
| `ORALIA_OLLAMA_MAX_TOKENS` | `256` | acotado a `[64, 512]` |
| `ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS` | `2` | intentos de regeneración acotada (no-revelación de solución) |
| `ORALIA_DISCLOSURE_OVERLAP_THRESHOLD` | `0.3` | umbral propio de `SolutionNonDisclosureVerifierAgent`, independiente de `GroundingVerifierAgent` |
| `ORALIA_COHERENCE_NO_PROGRESS_WINDOW` | `3` | turnos sin nueva entrada en `concepts_addressed` |
| `ORALIA_COHERENCE_REPETITION_WINDOW` | `1` | compara solo contra el turno inmediatamente anterior |

Hereda `ORALIA_DB_URL`/`ORALIA_VECTOR_STORE_PATH` de las Features 001/002 (mismo motor
SQLite/WAL y el mismo índice ChromaDB — ninguna infraestructura nueva).

### Activar Ollama (opcional)

```bash
# instalar/arrancar Ollama por separado (https://ollama.com), luego:
ollama pull llama3.2       # o el modelo que se prefiera
export ORALIA_OLLAMA_MODEL=llama3.2
```

Si Ollama no responde o el modelo no está disponible, cada llamada degrada
automáticamente al adaptador determinista dentro del mismo turno (research.md §1/§2) —
el turno se completa igualmente, nunca falla por esta causa.

## Ejecución

Igual que las Features 001/002 — no hay un proceso ni un puerto nuevos; los endpoints de
esta feature (`/api/v1/sessions/{id}/study-turns`, `/study-end`,
`/api/v1/tecnica/activities/{id}/self-study-config`,
`/api/v1/tecnica/sessions/{id}/study-trace`,
`/api/v1/tecnica/self-study/purge-expired`) se sirven en la misma app FastAPI:

```bash
PYTHONPATH=src uv run uvicorn oralia.interfaces.api.app:app --host 127.0.0.1 --port 8000
```

## Pruebas

```bash
PYTHONPATH=src uv run pytest tests/ -q -m "not ollama"   # suite completa (001+002+003), determinista, sin red
PYTHONPATH=src uv run pytest tests/ -k self_study -q      # solo pruebas de esta feature
PYTHONPATH=src uv run pytest tests/ollama/ -m ollama -q   # opcional: requiere Ollama real corriendo + ORALIA_OLLAMA_MODEL
```

El marcador `ollama` está registrado en `pyproject.toml` y se omite por defecto — las
pruebas normales (incluidas todas las de esta feature) son deterministas y no requieren
Ollama ni red (`ORALIA_OLLAMA_MODEL` sin configurar ⇒ `DeterministicGenerationAdapter`
siempre).

## Limitaciones conocidas

- **Sin verificación de Node/frontend en este entorno**: `apps/web/src/routes/
  Autoestudio.tsx` sigue los mismos contratos que el backend y los mismos patrones de
  accesibilidad ya usados en las Features 001/002 (etiquetas, `aria-live`, contraste,
  navegación por teclado nativa), pero no se ha instalado ni ejecutado con `npm` aquí —
  misma limitación ya documentada en las Features 001/002.
- **Purga no automatizada**: `POST /api/v1/tecnica/self-study/purge-expired` es de
  invocación manual (Principio VI); no hay scheduler — está deliberadamente fuera de
  alcance de esta feature (research.md §8, reservado a Feature 005).
- **Heurísticas deterministas de coherencia/no-revelación**: `CoherenceVerifierAgent` y
  `SolutionNonDisclosureVerifierAgent` usan solapamiento léxico de palabras
  significativas (misma técnica que `GroundingVerifierAgent` de la Feature 002, cada uno
  con su propio umbral/configuración) — no comprensión semántica real; pueden producir
  falsos negativos ante paráfrasis complejas (limitación documentada y aceptada para el
  MVP, research.md §4/§5).
- **`generator_used`/`overlap_score` nunca persisten `internal_expected_answer`**: por
  diseño (Principio VIII) — solo vive en memoria durante el turno.

## Datos de ejemplo

No se ha extendido `seed_demo.py` en esta feature — `specs/003-self-study-agency/
quickstart.md` reutiliza los ficheros de prueba de `tests/fixtures/materials/` ya
existentes de la Feature 002.
