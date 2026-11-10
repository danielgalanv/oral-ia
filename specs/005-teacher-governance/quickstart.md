# Quickstart — Feature 005



No usa datos reales. Configura ORALIA_ADMIN_SECRET fuera del repositorio (mínimo 24

caracteres), aplica `uv run alembic upgrade head`, inicia `uv run python apps/api/main.py`

y frontend con `pnpm.cmd --dir apps/web dev`. El servidor escucha 127.0.0.1.

No incluir el secreto en URLs, archivos exportados ni capturas.



En /gobierno, inicia sesión administrativa. Crea una actividad ficticia con plazo finito,

modelo disponible, política T090 y preguntas/materiales autorizados; activa la versión.

Inicia una sesión seudónima en /defensa o /autoestudio, revisa el aviso y elige scopes.

Completa y cierra; revisa solo lo consentido desde /gobierno. Duplica la actividad usada,

modifica un límite, publica sucesor y comprueba que la sesión anterior conserva versión.

Revisa texto libre antes de descargar JSON y Markdown. Elimina con confirmación y

comprueba que la sesión ya no aparece ni puede exportarse. Logout deniega el área docente.

Una segunda sesión sin conservación funciona y no aparece como sesión revisable.



```powershell

uv run --no-sync pytest tests/ -q -m "not ollama and not speech"

pnpm.cmd --dir apps/web build

pnpm.cmd --dir apps/web lint

pnpm.cmd --dir apps/web test:e2e

```



Pruebas focales: `test_governance_access.py`, `test_activity_governance.py`,

`test_session_privacy.py`, `test_session_exports.py` y `test_governance_flow.spec.ts`.

Registrar resultados medidos en implementation-evidence.md; todavía no se han ejecutado

pruebas de implementación de 005. Migraciones deben probarse limpias y desde t004

en bases temporales aisladas, sin modificar la base de uso normal.



Límites: única instalación, credencial docente local, sin recuperación institucional de

identidad; tokens caducan y se pierden al reiniciar. No se garantiza anonimización de

texto libre; su revisión humana es obligatoria. Voz real opcional no bloquea esta feature.



El harness E2E inicia sus propios API 8005/UI 5175 y base .e2e_governance.db; no usa

la base de desarrollo. Requiere Chromium de Playwright instalado. La política de

conservación distingue contenido y acceso: participant_only no permite revisión docente.

El estado de índice es informativo; su versión no prueba integridad. La reconstrucción

usa el botón explícito del panel y la implementación de indexado existente.

