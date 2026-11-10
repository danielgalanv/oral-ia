# Implementation Plan: Núcleo cognitivo y ejecución local

**Branch**: `001-core-cognitive-runtime` | **Date**: 2026-07-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-core-cognitive-runtime/spec.md`

## Summary

Construir un monolito modular local (un único proceso Python, sin microservicios) que
implemente el núcleo cognitivo mínimo de ORAL-IA: catálogo versionado de agentes y
agencias, contrato común de agente, mensajería interna estructurada, una pizarra cognitiva
externa al LLM con versionado optimista y detección de conflictos, gestión del ciclo de
vida de una única sesión interactiva activa por instancia, un control constitucional que
bloquea salidas prohibidas antes de mostrarlas, degradación controlada ante fallos de
agente, trazabilidad completa reconstruible tras un reinicio, y una interfaz web local
mínima (área de participante + área técnica). La interpretación de turno es determinista/
simulada (sin LLM real) en esta feature; RAG, voz y evaluación quedan fuera de alcance.

## Technical Context

**Language/Version**: Python 3.12 (backend, gestionado con `uv`); TypeScript (frontend
mínimo)

**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2 + Alembic, `structlog`,
`psutil`; React + Vite + TypeScript para `apps/web`. Ver `research.md` §6 para los
componentes de la pila propuesta en `11_plan_prompt.md` que se difieren explícitamente
(ChromaDB/VectorStore, embeddings, extracción documental, adaptadores LLM, STT/TTS,
Docker Compose) por no ser necesarios en esta feature (Principio XI).

**Storage**: SQLite en modo WAL, detrás de repositorios/adaptadores sustituibles
(Principio XI); ver `data-model.md` para el esquema.

**Testing**: `pytest` + `pytest-asyncio` (unit, contract, integration, failure);
Playwright para los flujos web críticos de participante y área técnica (e2e). Sin
integración de LLM real en esta feature (`research.md` §7).

**Target Platform**: aplicación local de un único usuario/instancia, vinculada por
defecto a `127.0.0.1` (FR-022); multiplataforma (Windows/Linux/macOS) vía Python/Node
estándar.

**Project Type**: aplicación web local reducida (API + cliente web mínimo) — variante
recortada de la Opción 2 del template, sin separación en repos ni despliegue distribuido.

**Performance Goals**: no hay objetivo de throughput (una sesión interactiva activa por
instancia — FR-012a); cada turno MUST completarse o degradarse dentro del `timeout_ms`
configurado por agente (Principio IX), sin cifra universal fijada en el requisito
(`10_clarification_decisions.md` → "Errores y recursos").

**Constraints**: sin acceso a Internet durante la ejecución (Principio I); estado
cognitivo siempre externo al contexto del LLM y versionado (Principio III); ningún
control constitucional u de privacidad puede omitirse por ahorro de recursos (Principio
IX); sin microservicios ni colas (Principio XI).

**Scale/Scope**: 1 instancia local, 1 sesión interactiva activa + N sesiones históricas
conservadas; catálogo de validación con ≥5 agentes de prueba y ≥2 agencias (SC-001,
SC-002).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Evaluación | Estado |
|---|---|---|
| I. Finalidad y límites institucionales | Sin robots, Moodle, Internet, expedientes; aviso explícito de sistema de IA (FR-010); ningún agente asigna notas ni decide académicamente (FR-014/015). | PASS |
| II. Arquitectura modular basada en contratos | `AgentContract` único y versionado (`contracts/agent-contract.md`); agentes en el mismo proceso; sin microservicios. | PASS |
| III. Estado cognitivo explícito y memoria diferenciada | `CognitiveState`/`StatePatch` fuera del contexto del LLM, versionados, con `memory_category` distinguiendo las 5 categorías mínimas; sin perfiles longitudinales. | PASS |
| IV. Separación recuperación/generación/decisión/verificación | `ExecutionStep.role` distingue generador/verificador; un generador no puede ser su propio verificador (regla explícita en el contrato); verificación por reglas observables, no por "reflexión" del modelo (no hay LLM en esta feature). | PASS |
| V. Fundamentación en materiales autorizados | No aplica todavía (sin materiales reales ni conocimiento general activado); `general_knowledge_allowed` default `false`. | PASS (alcance diferido) |
| VI. Supervisión humana y gobernanza | Configuración de actividad creada manualmente por el profesor/administrador vía API; sin modificación de reglas por agentes en sesión; sin K-lines en esta feature. | PASS |
| VII. Privacidad, minimización y accesibilidad | `127.0.0.1` por defecto; `ParticipantCode` seudónimo sin PII; sin audio (texto obligatorio); interfaz mínima usable por teclado (tarea de UI). | PASS |
| VIII. Trazabilidad y reproducibilidad | `TraceEvent` + `StatePatch` append-only permiten reconstrucción completa tras reinicio (US6); sin cadenas de razonamiento privadas almacenadas. | PASS |
| IX. Degradación controlada y límites de recursos | Timeout/cancelación por agente vía `AgentRequest.deadline_ms`; fallback y terminación segura definidos en `AgencyDefinition`. | PASS |
| X. Calidad, pruebas y evidencia | Pruebas de contrato por agente, integración por agencia, e2e para Escenario A, pruebas de fallo/timeout/conflicto/bloqueo (`tests/failure`). | PASS (a verificar en tasks/implementación) |
| XI. Simplicidad evolutiva | Se difieren explícitamente componentes no necesarios (`research.md` §6); SQLite + proceso único; toda dependencia nueva justificada. | PASS |

**Resultado**: sin violaciones. No se requiere `Complexity Tracking`.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-cognitive-runtime/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md         # Phase 1 output (/speckit-plan command)
├── quickstart.md         # Phase 1 output (/speckit-plan command)
├── contracts/            # Phase 1 output (/speckit-plan command)
│   ├── agent-contract.md
│   ├── api-participante.md
│   └── api-tecnica.md
└── tasks.md              # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
apps/
  api/                     # Entrypoint FastAPI/uvicorn, vincula 127.0.0.1 (FR-022)
  web/                     # React + Vite + TS: rutas /participante y /tecnica

src/oralia/
  domain/
    agents/                # Agent, AgentDescriptor, AgentContract
    agencies/               # Agency/AgencyDefinition, ExecutionStep
    messages/                # InternalMessage y tipos
    cognitive_state/         # CognitiveState, StatePatch, versionado optimista
    sessions/                 # Session, Turn, ActivityConfiguration, ParticipantCode, RetentionPolicy
    policies/                  # Control constitucional (bloqueo de notas/decisiones académicas)
    validation/                 # GeneratedProposal, VerificationResult, DialogueAction (selección)
  application/
    commands/                    # create_activity, start_session, submit_turn, end_session
    queries/                      # get_catalog, get_session, reconstruct_session_trace
    orchestration/                 # TurnOrchestrator, AgencyComposer, cancelación/timeout
    services/                       # trazabilidad, monitor de recursos (FR-016, FR-017)
  infrastructure/
    db/                               # Modelos SQLAlchemy, engine SQLite WAL, Alembic
    telemetry/                         # structlog, psutil
  interfaces/
    api/                                 # Routers FastAPI: participante, tecnica
    web/                                  # Cliente API tipado usado por apps/web

tests/
  unit/
  contract/                                 # 1 por AgentContract / endpoint
  integration/                               # 1 por Agency / flujo de sesión
  e2e/                                        # Escenario A vía Playwright
  failure/                                     # Escenarios B, C, D (bloqueo, fallo, conflicto)
```

**Carpetas deliberadamente no creadas en esta feature** (evitar acoplamiento prematuro,
Principio XI, `research.md` §6): `infrastructure/llm/`, `infrastructure/embeddings/`,
`infrastructure/vector_store/`, `infrastructure/documents/`, `infrastructure/speech/`,
`domain/materials/`. Se introducirán en las Features 002 (materiales/RAG) y 004 (voz) del
roadmap de la constitución.

**Structure Decision**: monolito modular en un único paquete Python (`src/oralia`) con
separación dominio/aplicación/infraestructura/interfaces, más un cliente web mínimo
(`apps/web`) y un entrypoint API (`apps/api`) — variante recortada de la "Opción 2:
Web application" del template, ajustada a la organización recomendada en
`docs/ORAL-IA_SpecKit/11_plan_prompt.md` y limitada al alcance real de esta feature.

## Complexity Tracking

*Sin violaciones de la Constitution Check — tabla no aplicable.*

## Adenda T090 — autorización constitucional contextual (2026-10-13)

**Alcance y estado**: diseño de FR-014/FR-015 exclusivamente; T090 permanece pendiente. Esta adenda no sustituye las decisiones históricas de este plan. Los detalles de política, propuesta y validación están en [research.md](research.md#9-decisiones-de-diseño-de-t090-2026-10-13), [data-model.md](data-model.md#adenda-t090--modelo-lógico-2026-10-13) y [contracts/constitutional-output.md](contracts/constitutional-output.md). La guía de aceptación está en [quickstart.md](quickstart.md#validación-prevista-de-t090-2026-10-13).

### Contexto técnico y puertas constitucionales de T090

La configuración existente `ActivityConfiguration` ya tiene `id`, `family_id`, `version` e inmovilidad desde el primer uso (`src/oralia/infrastructure/db/models.py`, `src/oralia/application/commands/create_activity.py`). Se amplía con una política de salida explícita por **versión de configuración**, sin tabla ni servicio de políticas. `AgentRequest` ya tiene `input` y `context` filtrado; la vía de ejecución del control puede transportar allí una propuesta estructurada y una instantánea confiable, manteniendo el contrato común de agentes. El texto libre actual no demuestra autorización contextual.

Puertas antes y después del diseño: I y VI, la política es docente, versionada e inmutable durante la sesión; II y IV, la propuesta estructurada y el verificador independiente impiden que el generador se autorice a sí mismo; V, el conocimiento general solo se usa con permiso explícito, sin modificar la verificación de materiales de Feature 002; VII y VIII, la instantánea mínima y las trazas con códigos evitan copiar datos sensibles; IX, todo fallo cierra en seguro tras como máximo una alternativa; X, la matriz positiva/negativa cubre rutas completas; XI, se reutilizan configuración, agente y orquestación existentes. **Resultado de diseño: PASS condicionado a implementar y verificar T090; no implica conformidad actual.**

### Integración y orden de evaluación previstos

1. Al crear o versionar una actividad, validar política y guardar identidad/versión junto a la configuración. Antes de cada salida, el orquestador construye desde la configuración de la sesión una instantánea mínima de política, destinatario, referencias de datos y alcance autorizables; ninguna consulta indiscriminada ocurre dentro de `ConstitutionalControl`. Congelar esa instantánea durante la evaluación y vincularla al `activity_configuration_id`/versión de la sesión.
2. El compositor autorizado construye `OutputProposal` con **texto final exacto** y segmentos demostrables. Solo plantillas confiables y ranuras de valor exacto, o composición estructural equivalente, pueden aprobarse en el MVP. El texto libre o una etiqueta de tema aportados exclusivamente por un generador no constituyen prueba y se bloquean. La capa constitucional aplica H02 sin cambiar sus reglas y autorización estructural FR-014 con la precedencia/cortocircuitos fijados en `contracts/constitutional-output.md`; un error temprano no obliga a inspeccionar más contenido. Grounding y admisión de materiales Feature 002 conservan sus verificadores y veredictos; su resultado no sustituye la autorización de salida.
3. Toda salida normal, pregunta de práctica, reconocimiento de falta de evidencia, fallback técnico o de generación y mensaje de bloqueo se somete a **una única función de autorización final** antes de API, persistencia visible o `CognitiveState`. Incorporar esta llamada a `turn_orchestrator.py` (pasos `verify` y `verify-fallback`) y a `self_study_agency_composer.py` (pregunta de práctica y turno de autoestudio, pasos `verify-constitutional` y `verify-fallback`). `study_turn_orchestrator.py` delega en esos compositores. El resultado de agente ausente/error/timeout se trata como bloqueo, nunca como `approved` por defecto.
4. Si la propuesta falla, registrar causas estructuradas sin texto ni valores sensibles y seleccionar **como máximo una** entrada de un catálogo interno de mensajes operativos mínimos. Construirla de fuente confiable sin reutilizar la propuesta rechazada; comprobar catálogo, identificador permitido por la política, texto exacto y H02 mediante el mismo control. Si política/contexto inválidos impiden autorizarla, terminar el turno sin contenido (`output_text = null`); no encadenar fallback. Una salida aprobada por la agencia pero posteriormente transformada debe verificarse nuevamente como texto final.
5. Conservar `evaluate(str)` solamente como clasificador léxico H02 interno/compatibilidad de pruebas existentes; no exponerlo como autorización final. La interfaz constitucional versionada exige propuesta + contexto estructurados y bloquea solicitudes solo textuales. Cambiar cada invocación directa de `constitutional_evaluate(candidate_text)` y cada publicación de `SAFE_BLOCKED_MESSAGE` para que no haya rutas de elusión. Las compatibilidades API del participante se documentan en `contracts/api-participante.md`.

### Entrega por etapas y compatibilidad

La implantación futura requiere: migración nullable de política para filas históricas (sin permiso implícito), validación en creación/configuración, catálogo confiable, constructor de propuestas, verificador estructural y adaptadores de todos los compositores, actualización de factories/seed y pruebas de contrato/integración/fallo. Configuraciones antiguas sin política se bloquean con `missing_policy`; una nueva versión docente o inicialización explícita asigna una política mínima de actividad antes de retomar salidas. No derivar permisos de `objective`. Mantener la versión antigua de H02 como subfunción, sin cambiar patrones ni expectativas de sus pruebas. Los riesgos de texto libre y compatibilidad con Feature 003 figuran en research.md §9.

### Revisión correctiva T090 (2026-10-13)

**Decisión física cerrada**: dos columnas en `ActivityConfiguration` (`output_authorization_policy_json` como `Text`/SQLite `TEXT` canónico nullable y `output_authorization_policy_sha256` como `String(64)` nullable) y una columna `VerificationResult.authorization_context` como `JSON` nullable; migración Alembic aditiva, sin backfill de permisos. `Turn.output_text` **ya es nullable** y no necesita migración. Validación Pydantic inmutable, serialización/hash deterministas, trigger de inmutabilidad y sucesión explícita de actividades históricas se especifican en `data-model.md` y `research.md` §10. No se añade tabla de política ni de veredicto.

**Fuente de verdad**: el veredicto final constitucional es exactamente el `VerificationResult.verdict` existente (`approved`/`block`); `reformulate`/`clarify` siguen disponibles contractualmente, sin cambio. `AuthorizationVerdict` vive solo durante la evaluación y se proyecta en esa fila, sus `reasons` y `authorization_context`. `TraceEvent` conserva los intentos 0/1 y el primer rechazo, sin crear un segundo veredicto final. Grounding/coherencia permanecen independientes. Orden de errores, cortocircuitos y privacidad: `contracts/constitutional-output.md` §«Corrección de diseño T090».

**Recorrido positivo mínimo SC-007**: seed o nueva configuración explícita con política para destinatario participante, tema `actividad`, propósito `acuse_turno`, acción `continuar`, y plantilla normal versionada `He recibido tu mensaje. Continuemos con la actividad.` sin ranuras. El compositor confiable la construye como texto exacto con un único segmento fijo `[0,len(text))`; el control verifica identidad/huella, cobertura, alcance y H02 y devuelve `approved`. Se presenta ese texto al participante, `Turn.status=completed`, `Turn.output_text` no nulo, se completa el turno y la finalización voluntaria mantiene la confirmación histórica. No se inserta ni repite el texto libre del participante. Los tests históricos que afirman eco literal en respuesta deben adaptarse **solo al comportamiento contractual de salida**; la matriz H02 directa y sus patrones no se tocan. Salida normal autorizada usa tipo `normal`; respuesta tras bloqueo/fallo usa tipo `operational`, catálogo y `attempt=1`; si falla esa única alternativa, el cierre usa `output_text=null` y no muestra mensaje.

**Integración de tipos/API**: la persistencia del turno ya admite `NULL`. `TurnResult.output_text` y `StudyTurnResult.output_text` pasan de `str` a `str | None`; los routers de participante/autoestudio lo serializan como `null`, los tipos TypeScript de `apps/web/src/api/client.ts` pasan a `string | null` y las vistas omiten la burbuja de respuesta si es `null`. El contrato público añade esa variante, sin migración de `Turn.output_text`. Una salida operativa aprobada pero con intento inicial bloqueado comunica `blocked=true` y estado degradado; el `VerificationResult` final sigue `approved`.

**Puertas post-diseño**: principios I/IV/V/VI, autoridad docente y verificación final independiente; VII/VIII, sin texto prohibido en API/trazas; IX, cierre seguro tras un intento; X, recorrido positivo y matriz negativa; XI, tres columnas aditivas y ningún servicio/tabla nuevo. PASS de **diseño**, sujeto a implementar guardia/migración, adaptar todas las salidas y aprobar pruebas; no representa cumplimiento actual de T090.
