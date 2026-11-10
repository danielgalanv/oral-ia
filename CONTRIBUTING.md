# Trabajar individualmente en ORALIA

Leer primero `AGENTS.md`, `docs/CONTINUAR.md` y el módulo que se vaya a cambiar. No hace falta leer todos los informes históricos. La copia de trabajo actual no tiene repositorio Git; no ejecutar `git clean`, `reset` ni inventar una historia de commits. Si se incorpora a control de versiones, revisar antes exclusiones, datos docentes, licencias y secretos.

## Instalación CPU

Python 3.12 o posterior según `pyproject.toml`, uv, Node y pnpm. Ejecutar desde la raíz; los comandos PowerShell del proyecto están preparados para Windows.

```powershell
uv sync --frozen --extra dev
pnpm.cmd --dir apps/web install --frozen-lockfile
```

La instalación puede necesitar red. Las sesiones no descargan pesos automáticamente. `uv.lock` y `apps/web/pnpm-lock.yaml` fijan dependencias; no actualizarlos como parte de otra corrección.

Para el API histórico, crear primero una carpeta propia y configurar `ORALIA_DB_URL` (por ejemplo `sqlite:///./.claude-scratch/dev-personal/oralia.db`) antes de `uv run alembic upgrade head`. No usar la base `oralia.db` de otra persona. Configurar `ORALIA_ADMIN_SECRET` privado (mínimo 24 caracteres), `uv run python apps/api/main.py` y en otra terminal `pnpm.cmd --dir apps/web dev`. Ver `docs/MVP.md`. No aplicar migraciones ni ejemplos de borrado sobre bases existentes de otra persona.

Para el piloto actual: `scripts/study-chat.ps1 -PrepareOnly -Offline -NoBrowser`. Necesita el paquete docente autorizado y el encoder local del índice. Los PDF y sus derechos no forman parte de una promesa de distribución pública. Los originales/manifest de `materiales/docente/piloto-requisitos/paquete-v2` deben corresponder entre sí; no sustituir archivos ni hashes para pasar controles. La consulta documental tiene límites y cuarentena explícitos.

## Entornos y GPU

El Python del proyecto es el coordinador CPU/API. **El trabajador CUDA es otro entorno**: no instalar el proyecto a ciegas en un entorno ajeno de ComfyUI ni depender de que exista `D:/ai-toolkit`.

```powershell
$env:ORALIA_CUDA_PYTHON = "$PWD\.venv-gpu\Scripts\python.exe"
```

Crear/preparar ese entorno con Python y PyTorch compatible con la GPU/controlador, más Transformers, Accelerate, bitsandbytes, tokenizers y safetensors. Una instantánea del entorno que ejecutó los ensayos se conserva en `config/gpu-environment.reference.json`: es una referencia comprobada, no un lock multiplataforma ni garantía de compatibilidad. El valor se lee al importar el adaptador; configurar antes de arrancar.

Modelos usados: Qwen2.5-14B-Instruct NF4 para generación y Qwen3-8B NF4 con razonamiento para revisión; encoder `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` en CPU. Las revisiones y rutas exactas están en `src/oralia/course_dialogue/cached_transformers.py` y `src/oralia/documentary/retrieval.py`; no sustituir checkpoints sin validar su perfil. Por defecto se buscan snapshots en la caché Hugging Face del usuario. No se incluyen pesos ni se descargan durante una prueba.

La ruta Windows histórica del trabajador sigue como compatibilidad, pero puede sobrescribirse con la variable anterior. Si no existen intérprete/pesos, preparar el entorno, no ocultar el error con un fixture. Antes de inferir, medir memoria/utilización; no cerrar aplicaciones ajenas sin autorización. La medición de velocidad necesita recursos comparables. Cada trabajador tiene ownership y debe cerrarse; no reactivar T por iniciativa propia.

## Comprobaciones proporcionadas al cambio

```powershell
uv run pytest -q tests/course_dialogue/test_prepared_concepts.py tests/course_dialogue/test_concept_ledger.py tests/unit/test_study_preparation.py
uv run ruff check src tests scripts
# Black: usar rutas de archivos modificados, no todo el archivo histórico.
uv run black --check --workers 1 src/oralia/course_dialogue/prepared_concepts.py
pnpm.cmd --dir apps/web lint
pnpm.cmd --dir apps/web build
```

Las primeras pruebas no hacen inferencia real. Fixtures no acreditan semántica. Hay diez diagnósticos Ruff históricos fuera del alcance de algunos cambios: comparar archivo/código/mensaje con multiplicidad, no solo conteos. Añadir pruebas negativas que reproduzcan el defecto, no pruebas que copien la implementación. Ejecutar navegador si cambia el flujo de usuario. Ampliar suites cuando cambien contratos/componentes compartidos; no repetir suites satisfactorias sin un cambio o duda concreta.

Pruebas reales usan una carpeta nueva y presupuesto explícito, entradas/oráculo separados, versiones congeladas y logs de llamadas/tokens/tiempos. No sobrescribir capturas o recibos para hacer pasar el resultado. Ningún modo debe entregar JSON interno al alumno ni una respuesta todavía sin revisar para aparentar rapidez.

## Organización y limpieza

`src/` y `apps/` son código; `tests/` pruebas; `scripts/` entradas operativas y ejecutores históricos; `config/` política de ejemplo; `specs/` requisitos/contratos; `docs/` guías/decisiones/evidencias; `materiales/` fuentes y derivados revisados. `docs/ARQUITECTURA.md` detalla qué se ejecuta realmente.

No mover código o ejecutores por estética: hay importaciones, hashes y rutas en recibos. Añadir código nuevo al componente con la responsabilidad adecuada y actualizar su entrada documental. Usar SpecKit para cambios de contratos/flujo, correcciones pequeñas directamente.

```powershell
uv run python scripts/clean_workspace.py
uv run python scripts/clean_workspace.py --apply
```

Por defecto solo muestra candidatos. Borra únicamente `.pytest_cache`, `.ruff_cache`, caché Vite y `__pycache__` de código/pruebas/scripts vivos; rechaza enlaces/junctions. No borra entornos, dependencias, modelos, bases, informes de navegador, evidencias, originales ni carpetas scratch históricas. No usar `.gitignore` como lista de borrado.

`.claude-scratch` contiene también preparaciones reutilizables, ownership, recibos y ensayos: **no es basura indiscriminada**. `.oralia*`, `oralia.db`, otros SQLite y sus WAL/SHM pueden contener estado activo; no borrarlos ni moverlos. Los `.scratch-*` anteriores se conservan hasta demostrar que son regenerables, no están en uso y no sostienen evidencias. Crear futuros ensayos solo en un directorio nuevo bajo `.claude-scratch`.

Al terminar un incremento: informar qué cambió, qué se comprobó, qué falló y qué sigue abierto; actualizar `docs/CONTINUAR.md` y el estado SpecKit pertinente. Evitar otro informe si basta con esa actualización.

La limpieza de mantenimiento del 05-11 queda registrada en `docs/maintenance/cleanup-20261105.json`; los informes cognitivos de `docs/audits` no se mezclan con esa operación.

La retirada adicional autorizada de temporales históricos está en `docs/maintenance/prune-obsolete-20261105.json`: incluyó bases **E2E ficticias inactivas**, no bases habituales. Esa excepción puntual no amplía la lista de borrado del limpiador ordinario. Se conservaron índices y evidencias todavía útiles; las antiguas preparaciones marcadas como retiradas no se reutilizan.
