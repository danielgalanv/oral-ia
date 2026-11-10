# Implementation Plan — Demostración local007

2026-10-18. Python3.12/uv/psutil/SQLAlchemy/Alembic existentes, React/Vite/PowerShell.
Sin agentes nuevos, dependencias nuevas, commits ni delegación. Extensión posterior al
MVP autorizada explícitamente, sin reinterpretar sus principios ni ampliar integraciones.

## Summary / Technical context

scripts/demo.ps1: un comando Start/Stop/Reset/Check, validación uv/venv, credencial oculta
sin argumentos/archivos/logs; restaura entorno del shell. Supervisor en src/oralia/demo/
__main__.py y launcher.py, recursos.py/path policy en resources.py, seed en fixtures.py.
Puertos8010/5180 por defecto, explícitos opcionales. No fallback de puertos.

Raíz normal única `<workspace>/.oralia-demo`, marcador de propiedad/version/workspace,
subdirs files/vector_store/tmp/vite-cache/logs, demo.db y recibos no secretos. Tests
pueden construir DemoPaths con workspace temporal, siempre .oralia-demo como hijo.
Subcomandos internos aceptan raíz solo si es .oralia-demo bajo workspace reconocido;
validar absolutas, no links/junctions/reparse ni escapes, incluido antes de borrar.

Start foreground, un supervisor exclusivo con lock de archivo; recibo PID/create_time,
run_id/puertos. Hijos Popen API y Node/Vite sin ventanas, credencial solo al API por
entorno. Readiness HTTP con nonce no secreto propio y comprobación de hijos vivos.
Ctrl+C/finally detiene árbol de hijos guardado con PID/create_time, nunca búsqueda por
puerto/nombre. Stop valida supervisor PID/create_time/cwd/identidad y solicita parada
por archivo ligado al run_id; no mata PIDs de recibos. Reset requiere supervisor parado,
ruta/marcador/árbol sin enlaces y entrada exacta BORRAR DEMO; vuelve a comprobar antes
shutil.rmtree. Un lock evita arranque/reset simultáneos; lock fuera de datos borrables.

## Resources / preparation

Overrides de ORALIA_DB_URL/vectorpath, temp/telemetría/offline y modelo determinista,
sin heredar LAN/Ollama/STT/TTS de uso habitual. Frontend recibe solo config no secreta;
cacheDir propio. Modelo embeddings ya en caché se comparte solo como recurso de lectura;
se prueba carga/encode con HF offline forzado. Si falta, salida accionable ofreciendo
-TextOnly, nunca descarga. TextOnly publica actividad sin referencias recuperables,
material breve visible en archivos y catálogo como no indexado; no afirma tener fuentes.

Migración Alembic head solo demo, verificar revision/estructura contra esquema existente.
Se completa mediante migración aditiva la tabla ya modelada index_rebuild_lock, ausente
en migraciones históricas: t007_demo_install después de t005_governance. Probar limpio
y upgrade005, DDL previo intacto y tablas/columnas contra Base.metadata. No create_all
para ocultar brechas de instalación ni cambio de contratos de la tabla existente.
Fixtures DOCX breve de agua/ciclo didáctico por pipeline ingest/activate existentes,
model deterministic real, publish_activity normal y política manual T090 para demo-007.
Dos configuraciones de actividad activas, retención1día y scopes independientes. Config
JSON sin secretos con IDs/versión/modo perfil, atomic write; si cambia perfil o fixtures
no reescribir versión usada: exigir Reset explícito. Repetir arranque no duplica ni
borra sesiones; advertir sesión activa previa. Mantener consentimiento/ownership normal.

## Navigation

Inicio.tsx en / con enlaces participante/docente y demo banner por env pública no secreta.
Gobierno añade links por modo solo para versiones activas y material/resumen mínimo;
Autoestudio/DefensaOral inicializan activity desde query no secreta, sin iniciar sesión
automáticamente ni precargar permiso. Link Volver inicio. Rutas actuales conservadas.
No nuevos endpoints públicos de contenido administrativo. Autorización continúa en API.

## Research decisions

Supervisor foreground/Stop por solicitud: evita daemon Windows/servicios y señalizar
procesos ajenos. Credencial manual: evita distribución de secretos demo persistentes.
Seed por servicios reales: evita simular indexado/controles. Cache/modelo preexistente:
no añadir embeddings alternativos ni nuevos agentes. Texto sin fuentes es degradación
explícita, no índice simulado. Vite se ejecuta con Node directo para controlar procesos.
Snapshot original006 (156archivos+paquete) preservado antes de cambios; nuevo paquete
actual en007/evidence006-current, jamás editar006 ni hashes originales.

## Constitution Check

PASS diseño previo/posterior: I IA/sin notas; II contratos existentes; III estado/parches;
IV T090 y verificadores intactos; V fuentes reales/versionadas/no evidencia explícita;
VI credencial/publicaciónmanual; VII ficticio/local/scopes/audio no requerido/texto/teclado;
VIII recibos/codehash/paquetes; IX timeouts/budgets/falloslimpios; X regresiones/offline/
Playwright/lifecycle; XI supervisor sencillo sin dependencias nuevas. T150 intacto.

## Quality gates / phases

Setup→US1 procesos/seguridad→US2 datos→US3 navegación/recorrido→US4 guion/offline→gates.
Pruebas antes de bloques. Tests Python tmp_path/puertos efímeros explícitos para aislamiento;
ensayo real PowerShell en .oralia-demo (no habitual) y Playwright contra recursos demo
sembrados en harness aislado con login real. Comprobar hashes habituales y proceso centinela
antes/después de start/stop/reset. Build/lint/global Playwright/pytest, Black inventario,
Ruff Counter baseline001. Preservar006 original y nuevo run/replay204 tras congelar código.
Informe con tareas/archivos/hardware/logs/límites, analyze y converge final hasta cero.

Integración de aislamiento: ORALIA_COOKIE_NAMESPACE=oralia_demo solo en hijos demo;
LocalAccess fija nombres al crear app, login/logout/owner usan esos nombres. Default
oralia_admin/oralia_participant intacto. Sin cambio de tokens/roles/T090/T150. Evita
colisión de cookies entre puertos del mismo host. Vite envDir propio y variables VITE_*
heredadas excluidas; no cargar .env habitual en demo. Prueba negativa previa y login/logout
cruzados reales confirman aislamiento. Preparación también es hijo propio y su timeout
limpia su árbol; API calienta embeddings antes de readiness, sin tocar límites de turno.
