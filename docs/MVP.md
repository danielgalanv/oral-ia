> Guía de un demostrador anterior. Para el chat actual y el estado del proyecto, consultar [ESTUDIO](ESTUDIO.md) y [CONTINUAR](CONTINUAR.md). No acredita por sí sola el piloto generativo actual.

# ORAL-IA — MVP local

Asistente automático de apoyo docente, con posibilidad de error y supervisión humana.
No asigna notas ni toma decisiones académicas. Seis features acumulativas; documentación
y evidencia final en specs/005-teacher-governance y specs/006-architecture-validation.

## Instalación y arranque

Python3.12, uv, Node y pnpm. Instalar dependencias con acceso a paquetes previamente
preparados o durante instalación; las sesiones no requieren Internet. La recuperación
vectorial necesita el modelo de embeddings local preparado; no prometer instalación
sin red si no están las dependencias/modelos en caché. Texto usa reserva determinista
sin Ollama. La voz es opcional y requiere extras/modelos locales explícitos.

```powershell
uv sync --extra dev
uv run alembic upgrade head
pnpm.cmd --dir apps/web install
```

Configura ORALIA_ADMIN_SECRET con una credencial privada de al menos24 caracteres en la
terminal que arranca el API; no guardarla en el repositorio ni pasarla por URL. Después:

```powershell
uv run python apps/api/main.py
```

En otra terminal:

```powershell
pnpm.cmd --dir apps/web dev
```

API127.0.0.1:8000 y web127.0.0.1:5173. Entrar en /gobierno con la credencial instalada.
Crear curso y política finita; configurar actividad, límites, preguntas/materiales,
modelo disponible y permisos explícitos de salida. La ayuda del formulario prepara
una política para el código seudónimo destinatario: revisarla antes de aprobar. Guardar
borrador y activar. Copiar identificador de actividad en /autoestudio o /defensa.
Las configuraciones históricas sin política explícita no permiten toda salida.

## Recorrido de demostración

Usar código ficticio, leer aviso y elegir conservación. Texto permite toda función
esencial; con voz se revisa/corrige antes de confirmar. Cerrar voluntariamente o por
límite. Docente revisa solo contenido autorizado, vigente y consentido. Resumen y
transcripción son scopes distintos; participant_only no permite revisión docente.
Revisar texto libre antes de descargar JSON/Markdown. Confirmar eliminación y comprobar
que ya no es revisable/exportable. Duplicar una actividad usada crea una nueva versión
sin alterar la sesión anterior. No borrar una sesión activa: finalizar primero.

Tokens temporales en memoria/cookies HttpOnly/SameSite; docente1h, propietario24h.
Reinicio invalida accesos; no hay recuperación institucional de identidad. Código
seudónimo no autentica. Una única sesión interactiva activa. Localhost por defecto;
LAN requiere configuración explícita de host y ORALIA_ALLOW_LAN, fuera del uso ordinario.

## Validación y reproducción

```powershell
uv run --no-sync pytest tests/ -q -m "not ollama and not speech"
pnpm.cmd --dir apps/web build
pnpm.cmd --dir apps/web lint
pnpm.cmd --dir apps/web exec playwright install chromium
pnpm.cmd --dir apps/web test:e2e
uv run --no-sync python -m oralia.validation replay --package specs/006-architecture-validation/evidence
```

Playwright usaAPI8005/UI5175 y base aislada. El experimento no abre la base interactiva;
run admite solo catálogo sintético y directorio nuevo. Para repetir desde cero:

```powershell
uv run --no-sync python -m oralia.validation run --output .claude-scratch/new-validation --repetitions 2 --seed 42 --authorize-synthetic-ablations
```

Resultados abiertos y explicación: specs/006-architecture-validation/evidence/report.md.
204 celdas comparan baseline directo, agencia, ambas ablaciones, top1 y presentación.
Las ablaciones nunca se exponen a participantes. Hash de código, corpus, protocolos y
entorno fijados; replay compara decisiones estructurales y rechaza manipulación/cambio.
No afirma superioridad LLM: modelo extractivo determinista y ranking lexical controlado.

Perfil observado: Windows11 AMD64, Python3.12.11,24CPU lógicas y191.27GiB de RAM física
reportada por psutil. GPU no medida. Es el entorno observado, no un mínimo recomendado
ni una promesa de rendimiento en otros equipos. Tiempos/variabilidad en results.json;
latencia total incluye base temporal y limpieza, RSS es muestra y no pico.

## Límites pendientes de validación externa

Voz real, inferencia Ollama e índice vectorial real no se han comparado en la matriz006.
Dos pruebas de voz real se omiten sin modelos configurados. No hay piloto humano ni
observaciones de utilidad, facilidad o tiempo docente: aparecen como faltantes. Los
verificadores deterministas tienen límites semánticos; no garantizan detectar toda
inexactitud ni todos los datos personales en texto libre. Mantener revisión humana.
No hay SSO, nube, expedientes, notas, biometría ni perfiles longitudinales.
