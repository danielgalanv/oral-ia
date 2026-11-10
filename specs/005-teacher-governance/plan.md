# Implementation Plan: Gobierno docente local y privacidad



**Branch**: `005-teacher-governance` (sin Git) | **Date**: 2026-10-17 | **Spec**: [spec.md](spec.md)



## Summary



Completar el gobierno humano reutilizando versiones de ActivityConfiguration, T090,

T150, consentimiento de defensa y retención existentes. Añadir autenticación real que

proteja también rutas históricas, ciclo de publicación, revisión por scopes, exportación

por proyección y borrado verificable. Feature 006 queda fuera del alcance.



## Technical Context



Python 3.12/uv, FastAPI/Pydantic/SQLAlchemy/Alembic/SQLite WAL y React/TypeScript/Vite

existentes. Sin nuevas dependencias de ejecución. Credencial en ORALIA_ADMIN_SECRET;

comparación constante, tokens aleatorios de 256 bits, solo hashes en memoria y caducidad

de acceso. Cookies HttpOnly/SameSite estricto para navegador y bearer para CLI. La

credencial no se serializa ni registra. Reinicio invalida tokens, sin perder sesiones.



Una instalación, una sesión interactiva. Exportaciones máximas de 100 sesiones/lote,

construcción local en memoria y sin archivos en servidor. Sesión docente de 1 hora y

participante de 24 horas; logout revoca el token.

Sin ORALIA_ADMIN_SECRET las operaciones docentes fallan cerradas con 503, no se inventa

un secreto. El servidor sigue en 127.0.0.1; ORALIA_ALLOW_LAN=1 es un opt-in administrativo.



## Constitution Check



Gates previos y posteriores al diseño: PASS. No se modifica la constitución.



| Principio | Diseño |

|---|---|

| I | No notas, perfiles, expedientes ni autoridad académica; vistas y métricas descriptivas. |

| II | Contratos versionados; autorización y gobierno son servicios de aplicación, no agentes cognitivos duplicados. |

| III | Estado existente y parches; borrado por política posterior a sesión preserva solo recibos mínimos. |

| IV | Ninguna revisión o exportación regenera texto ni autoriza candidatos; T090 permanece obligatorio. |

| V | Versiones de material autorizadas y filtros existentes; retirada preserva historia sin recuperar en nuevas sesiones. |

| VI | Credencial local, publicación humana, configuración inmutable y exportación/eliminación explícitas. |

| VII | Propiedad de sesión, scopes, plazo finito, sin audio, alias y revisión humana de texto libre. |

| VIII | Eventos estructurados y recibos sin secretos/contenido eliminado; metadatos suficientes para auditar límites. |

| IX | Plazos de sesión de acceso, límites de lote/carga, denegaciones seguras y rollback. |

| X | Pruebas de autorización en rutas antiguas/nuevas, regresión global, navegador y migraciones. |

| XI | Monolito local y dependencias ya instaladas; secretos y sesiones de acceso en memoria, sin SSO ni servicios. |



## Project Structure



- `src/oralia/infrastructure/db/models.py` y migración `t005_governance.py`: metadatos de gobierno, preferencias y recibos.

- `src/oralia/interfaces/api/deps/local_access.py`: autenticación, autorización, origen y ownership para toda la API.

- `src/oralia/interfaces/api/deps/auth_stub.py`: sustituir no-op por comprobación real conservando punto de integración.

- `src/oralia/application/services/activity_governance_service.py`: versiones, publicación, catálogos y material seleccionado.

- `src/oralia/application/services/session_privacy_service.py`: scopes, revisión, eliminación y purga de copias.

- `src/oralia/application/services/session_export_service.py`: proyección cerrada JSON/Markdown, alias por lote, sin exportar blobs internos.

- `src/oralia/interfaces/api/routers/governance.py`: administración y privacidad de propietario.

- Integraciones explícitas: `app.py`, `start_session.py`, rutas participantes, cierres de modos, consultas técnicas y configuración de generación.

- `apps/web/src/routes/Gobierno.tsx`, cliente y rutas: autenticación, edición/publicación, revisión, exportación, borrado y métricas.

- UI participante: credencial de sesión efímera y controles de privacidad/revisión.

- Tests `test_governance_access.py`, `test_activity_governance.py`, `test_session_privacy.py`, `test_session_exports.py`, `test_governance_flow.spec.ts`.



## Phases and dependencies



1. Persistencia y contratos de acceso/publicación/privacidad.

2. Acceso local global; adaptar harness histórico para usar credenciales explícitas.

3. Gobierno de versiones y materiales, selección de modelos disponibles, publicación.

4. Privacidad común y cierre ganador; revisión filtrada y saneamiento de rutas antiguas.

5. Exportación, eliminación/purga y métricas agregadas.

6. UI docente y participante, pruebas reales por navegador.

7. Suites globales, migraciones, quickstart ejecutado, análisis y convergencia.



Las pruebas de cada historia preceden a su implementación. No hay commits ni agentes

delegados: único escritor. El análisis es de solo lectura; converge solo añade tareas.



## Compatibility and security changes



Los contratos cognitivos y tablas históricas conservan su significado. Se añaden tablas

de gobierno y hooks explícitos, sin parchear prompts para gobernar seguridad. La API

docente previamente abierta ahora exige autorización real: cambio intencional de

seguridad de Feature 005. Los tests históricos usan una credencial de instalación

ficticia explícita; no existe bandera de bypass en producción. Las consultas técnicas

históricas preservan metadatos, pero contenido revisable requiere scopes vigentes.



Versiones históricas sin metadatos de publicación siguen siendo referencias válidas;

al administrarlas se registra su ciclo. La API histórica de creación, solo docente,

mantiene compatibilidad creando la primera versión publicada; la nueva UI permite

borradores y publicación explícita. Una versión retirada se rechaza en start_session.



## Quality gates



766 deterministas y 9 Playwright son la evidencia aceptada de 004 antes de esta feature.

El objetivo es cero regresiones no justificadas; cifras finales solo tras ejecutar.

Ruff por `(ruta,código,mensaje)` con Counter contra baseline durable 001, Black sobre

inventario de archivos tocados, build/lint y todos los Playwright. Migraciones limpia y

upgrade desde t004; quickstart con credenciales ficticias, una actividad y sesiones

ficticias consentida/efímera. Voz real sigue opcional, no se cuenta como pasada.



## Complexity Tracking



Sin excepciones constitucionales. El acceso no se basa en ocultar botones ni en códigos

seudónimos; la exportación nunca serializa modelos ORM arbitrarios.



## Precisiones verificadas durante implementación



La credencial de instalación solo se usa para login. La autorización bearer requiere

un token emitido, aleatorio y caducable; no se acepta la contraseña permanente como

token. El harness usa login real y cookies/tokens explícitos, sin bypass.



Los materiales y modelo de configuraciones históricas se fijan al primer inicio bajo

el régimen de 005. Una familia ya administrada no permite reactivar miembros antiguos

por la vía de inicio. El conjunto documental se verifica tanto en recuperación como

al reutilizar fragmentos encolados; asociar un documento posteriormente no lo incorpora.

Un índice único parcial garantiza una activa por familia incluso ante concurrencia.



El cierre voluntario transporta su elección explícita hasta T150 sin escribir

preferencias de una ejecución perdedora. Los cierres automáticos usan la elección del

turno actual. La vista de privacidad de una sesión cerrada muestra el consentimiento

que efectivamente se aplicó, sin sustituirlo por preferencias previas.



Borrado no significa perder la prueba de funcionamiento: los modos genérico/autoestudio

pueden conservar filas estructurales vacías (versión del estado, emisor/receptor/paso,

veredicto, tipo de pregunta y contadores). Nunca se conservan respuestas, conceptos,

hipótesis, prompts ni razonamiento privado sin scope. La defensa mantiene además su

borrado histórico de filas operativas. El recibo mínimo de resumen autoestudio contiene

solo turn_count/duration_seconds, nunca el resumen textual ni conceptos/fuentes.



Puertos de pruebas: API 8005, UI 5175, `.e2e_governance.db` aislada. Desarrollo normal

conserva API 8000/UI 5173 y enlace a 127.0.0.1. No se reutilizan ni detienen servidores

ajenos al harness.



La duplicación a una familia nueva conserva source_activity_configuration_id. La política

content_scope limita los scopes elegibles; access_scope participant_only permite revisión

propia, pero bloquea revisión/exportación docente. Las políticas desconocidas no amplían

permisos. El catálogo del índice lee metadatos sin crear ni validar implícitamente el índice;

integrity_verified=false se muestra como tal y la reconstrucción usa la ruta ya existente.

