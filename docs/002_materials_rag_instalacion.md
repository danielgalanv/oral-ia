# Feature 002 — Materiales autorizados y RAG trazable: instalación, ejecución, pruebas

Documentación operativa de la Feature 002, exigida por
`docs/ORAL-IA_SpecKit/13_definition_of_done.md`. Extiende (no sustituye)
`docs/001_core_runtime_instalacion.md` — esta feature añade capacidades al mismo proyecto
`uv`, no crea uno nuevo. Complementa `specs/002-materials-rag/quickstart.md`, que detalla
los escenarios de validación A–G.

## Requisitos adicionales sobre la Feature 001

- Los mismos de la Feature 001 (Python 3.12/`uv`; Node.js 18+ solo para `apps/web`).
- **Descarga única del modelo de embeddings**: la primera vez que se ejecuta cualquier
  flujo que indexe o consulte materiales, `sentence-transformers` descarga el modelo
  `paraphrase-multilingual-MiniLM-L12-v2` (~470 MB) desde Hugging Face Hub — requiere
  acceso a Internet **solo esa primera vez**. A partir de ahí, el modelo queda cacheado
  localmente (`~/.cache/huggingface`) y todas las ejecuciones posteriores fuerzan
  `HF_HUB_OFFLINE=1`/`TRANSFORMERS_OFFLINE=1`, garantizando cero llamadas de red en
  indexación/recuperación (Constitución Principio I).
- ChromaDB corre en modo persistente 100% local — no requiere ningún servicio externo.

## Instalación

```bash
uv sync --extra dev
PYTHONPATH=src uv run alembic upgrade head   # incluye la migración de esta feature
```

Descarga anticipada (opcional, evita la espera en la primera petición real):

```bash
PYTHONPATH=src uv run python -c "from oralia.infrastructure.embeddings.sentence_transformer_adapter import SentenceTransformerEmbeddingAdapter as A; A().embed(['aviso'])"
```

## Configuración

- `ORALIA_VECTOR_STORE_PATH`: directorio del índice vectorial persistente de ChromaDB
  (por defecto `./.oralia_data/vector_store` — ver
  `src/oralia/infrastructure/vector_store/config.py`).
- Hereda `ORALIA_DB_URL` de la Feature 001 (mismo motor SQLite/WAL, cinco tablas nuevas).

## Ejecución

Igual que la Feature 001 — no hay un proceso ni un puerto nuevos; los endpoints de esta
feature (`/api/v1/materials/*`) se sirven en la misma app FastAPI:

```bash
PYTHONPATH=src uv run uvicorn oralia.interfaces.api.app:app --host 127.0.0.1 --port 8000
```

## Pruebas

```bash
PYTHONPATH=src uv run pytest tests/ -q                 # suite completa (Feature 001 + 002)
PYTHONPATH=src uv run pytest tests/ -k material -q     # solo pruebas de esta feature
```

Todas las pruebas de esta feature fuerzan `HF_HUB_OFFLINE=1` (ver `tests/conftest.py`) y
usan un directorio ChromaDB aislado por prueba (`tmp_path`), igual que el aislamiento por
`tmp_path` que ya usa el SQLite de cada prueba.

## Limitaciones conocidas

- **Sin verificación de Node/frontend en este entorno**: la sección "Materiales" añadida
  a `apps/web/src/routes/Tecnica.tsx` sigue los mismos contratos que el backend y los
  mismos patrones de accesibilidad ya usados en la Feature 001, pero no se ha instalado
  ni ejecutado con `npm` aquí — misma limitación ya documentada en la Feature 001.
- **Tamaño máximo de archivo**: 20 MB por defecto
  (`ingest_material.py::MAX_SIZE_BYTES`) — un valor razonable no derivado de un requisito
  numérico explícito de `spec.md` (que lo deja como parámetro deferido en Assumptions).
- **Vigencia (`valid_until`) de fragmentos**: el modelo de datos soporta excluir
  fragmentos caducados de la recuperación (FR-019a), pero esta feature no expone un
  mecanismo de carga para fijar una fecha de caducidad al subir un documento — se deja
  como campo interno manipulable a nivel de datos hasta que una feature posterior defina
  el flujo docente para establecerlo.
- **Detección de conflictos y fundamentación**: heurísticas deterministas basadas en
  solapamiento de palabras clave y marcadores de negación (research.md §7) — no un
  modelo de lenguaje. Suficiente para el conjunto de pruebas de esta feature, pero no
  equivalente a una comprensión semántica real.
- **Compatibilidad `transformers`/Hugging Face Hub**: en este entorno de desarrollo, la
  versión de `transformers` instalada por `uv sync` falla con un error `401` engañoso al
  comprobar si el modelo tiene un adaptador PEFT, si se ejecuta con acceso de red
  completo. Forzar `HF_HUB_OFFLINE=1` tras la primera descarga (ya aplicado
  automáticamente por `sentence_transformer_adapter.py`) evita el problema.

## Datos de ejemplo

No se ha extendido `seed_demo.py` en esta feature — los escenarios de
`specs/002-materials-rag/quickstart.md` usan los ficheros de prueba de
`tests/fixtures/materials/` (generados una vez por `.claude-scratch/gen_fixtures.py`,
no parte del paquete instalable).
