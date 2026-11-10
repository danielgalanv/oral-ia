# Implementation Plan: Agencia de defensa oral y voz opcional

**Branch**: `004-oral-defense-agency` | **Date**: 2026-10-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/004-oral-defense-agency/spec.md` (Clarifications, sesión 2026-09-02)

## Summary

Añadir un simulador de defensa oral (pregunta inicial, repreguntas, aclaración por
transcripción ambigua, cierre con resumen descriptivo) construido como una **nueva
composición dinámica** sobre el mismo núcleo cognitivo, RAG, `GenerationPort` y
verificadores ya implementados y validados en las Features 001–003 — no como un sistema
paralelo. Las únicas piezas genuinamente nuevas son: dos adaptadores de interfaz de voz
(`TranscriptionPort`/`SpeechSynthesisPort`, locales, opcionales), un agente de
repreguntas (`FollowUpQuestionAgent`, la única responsabilidad cognitiva realmente
distinta de lo ya existente), y persistencia mínima para transcripción/corrección/
consentimiento. `CognitiveState` no gana ningún campo nuevo (research.md §11) y
`DialogueAction` no gana ninguna acción nueva (research.md §10). Toda salida visible se
integra con la puerta final estructurada T090 de Feature 001: snapshot confiable,
plantilla catalogada, propuesta vinculada, persistencia de la decisión y cierre sin texto
si el control bloquea. El cierre reutiliza la transición ganadora T150.

## Technical Context

**Language/Version**: Python 3.12 (`uv`) — mismo runtime que Features 001–003, sin
cambios.

**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2 + Alembic (ya en uso, sin
cambios) — nuevas dependencias opcionales: `faster-whisper>=1.2.1,<2` y
`piper-tts>=1.8,<2`. Se cargan exclusivamente desde un identificador/ruta local
configurado (`ORALIA_STT_MODEL` y `ORALIA_TTS_VOICE`); la ruta normal no descarga
modelos silenciosamente.

**Storage**: SQLite en modo WAL (Feature 001, sin cambios) — cuatro tablas nuevas
(`defense_activity_config`, `transcript`, `transcript_correction`, `consent_record`;
ver data-model.md), ninguna tabla existente modificada.

**Testing**: `pytest`/`pytest-asyncio` (ya en uso). Nuevo marcador `speech` (mismo
patrón que el marcador `ollama` de la Feature 003) para las pruebas reales opcionales
con `faster-whisper`/Piper — omitidas por defecto.

**Target Platform**: Ejecución local en un único proceso (Windows/Linux/macOS) — sin
cambios respecto a Features 001–003.

**Project Type**: Monolito modular (dominio/aplicación/infraestructura/interfaces),
extendido de forma aditiva — mismo patrón exacto que las Features 001–003.

**Performance Goals**: STT/TTS se ejecutan fuera del bucle asíncrono mediante un worker
de voz dedicado con capacidad global explícita, backpressure, admisión cancelable y el
mismo plazo observado por `run_with_deadline`. Se prohíbe `asyncio.to_thread` sin límite;
un resultado tardío se descarta y no puede tocar SQLAlchemy, trazas ni respuestas.

**Constraints**: Ejecución 100% local; sin servicio cloud obligatorio (FR-036); audio
nunca persistido (FR-011/FR-011a), máximo 10 MiB y 300 s por carga; cierre verificable
de cualquier spool multipart; modalidad textual MUST cubrir el 100% del flujo sin STT/TTS
instalados (FR-003).

**Scale/Scope**: Mismo perfil de MVP local que Features 001–003 — una sesión de defensa
por instancia activa a la vez (reutiliza el mismo bloqueo de sesión única, Feature 001,
sin cambios).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Evaluación |
|---|---|
| I. Finalidad y límites institucionales | ✅ Sin robot/embodiment/vídeo/Internet obligatorio (FR-034/FR-036); todas las ramas usan la puerta final T090 y cierre sin texto cuando no existe salida autorizada |
| II. Arquitectura modular basada en contratos | ✅ `FollowUpQuestionAgent` con `AgentContractSchema` completo (contracts/defense-agents.md); `TranscriptionPort`/`SpeechSynthesisPort` son interfaces reemplazables, no agentes ocultos |
| III. Estado cognitivo explícito y memoria diferenciada | ✅ `CognitiveState` sigue siendo la única fuente de verdad, cero campos nuevos (research.md §11); sin perfiles longitudinales (FR-032) |
| IV. Separación recuperación/generación/decisión/verificación | ✅ `FollowUpQuestionAgent` nunca aprueba su salida; grounding/coherencia preceden a la puerta final T090, que recibe un `AuthorizationSnapshot` confiable y persiste propuesta/veredicto antes de publicar |
| V. Fundamentación en materiales autorizados | ✅ Reutiliza `MaterialRetrieverAgent`/`GroundingVerifierAgent` sin cambios; `general_knowledge_used` mismo patrón que Feature 003 |
| VI. Supervisión humana y gobernanza | ✅ `DefenseActivityConfig` inmutable tras primer uso (mismo patrón ya validado); purga manual, sin scheduler |
| VII. Privacidad, minimización y accesibilidad | ✅ Audio nunca persistido (research.md §3); `ParticipantCode` reutilizado sin cambios; interfaz textual completa, teclado, pausa, ritmo (FR-035) |
| VIII. Trazabilidad y reproducibilidad | ✅ Eventos de defensa y borrado de contenido, todos sobre el mecanismo genérico ya existente (research.md §17); nunca se traza audio ni razonamiento libre |
| IX. Degradación controlada y límites de recursos | ✅ Fallo STT→texto sin reintento; fallo TTS conserva texto; worker acotado con backpressure/cancelación; una sola alternativa operativa también atraviesa T090 |
| X. Calidad, pruebas y evidencia | ✅ Ver research.md §18 y quickstart.md — batería completa preparada para `/speckit-tasks`, incluida regresión 001–003 |
| XI. Simplicidad evolutiva | ✅ Cero agentes nuevos salvo el genuinamente distinto (`FollowUpQuestionAgent`); `GenerationPort` extendido de forma aditiva, no un tercer adaptador; sin microservicios/colas/Kubernetes (FR-034) |

**Resultado**: PASS sin excepciones — no se requiere `Complexity Tracking`.

## Project Structure

### Documentation (this feature)

```text
specs/004-oral-defense-agency/
├── plan.md              # This file
├── research.md           # Phase 0 output
├── data-model.md         # Phase 1 output
├── quickstart.md         # Phase 1 output
├── contracts/            # Phase 1 output
│   ├── defense-agents.md
│   └── api-oral-defense.md
└── tasks.md               # Phase 2 output (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
src/oralia/
  domain/
    agents/
      followup_question_agent.py        # NUEVO
      # PracticeQuestionAgent, GroundingVerifierAgent, CoherenceVerifierAgent,
      # MaterialRetrieverAgent: reutilizado, sin cambios
      # ConstitutionalControl: extensión aditiva de veto a caracterización personal (§27 de research.md)
  application/
    commands/
      configure_defense_activity.py     # NUEVO — mismo patrón que configure_self_study_activity.py
      submit_defense_turn.py            # NUEVO — texto
      submit_defense_voice_turn.py      # NUEVO — captura + transcripción provisional
      confirm_defense_transcript.py     # NUEVO — confirmación/corrección → avanza el turno
      end_defense_session.py            # NUEVO — mismo patrón que end_study_session.py
      purge_expired_defense_data.py     # NUEVO — mismo patrón que purge_expired_self_study_data.py, fichero propio
    services/
      defense_retention_service.py       # NUEVO — borrado por sesión y plazo finito
      defense_session_summary_service.py # NUEVO — mismo patrón que study_session_summary_service.py
    orchestration/
      defense_agency_composer.py        # NUEVO — mismo patrón que self_study_agency_composer.py, no lo importa
  infrastructure/
    speech/                              # NUEVO
      transcription_port.py
      faster_whisper_adapter.py
      synthesis_port.py
      piper_adapter.py
      blocking_speech_worker.py          # worker dedicado, acotado y process-wide
      config.py                          # ORALIA_STT_MODEL, ORALIA_TTS_VOICE, umbrales
    db/
      models.py                          # EXTENDIDO de forma aditiva: 4 clases nuevas al final del fichero
      migrations/versions/
        t004_oral_defense_tables.py # NUEVA migración, solo create_table
  interfaces/
    api/
      routers/
        oral_defense.py                  # NUEVO router, registrado en app.py de forma aditiva

apps/web/src/routes/
  DefensaOral.tsx                        # NUEVO — mismo patrón de accesibilidad que Autoestudio.tsx
apps/web/src/api/client.ts               # EXTENDIDO — contratos de defensa y audio binario
apps/web/src/main.tsx                    # EXTENDIDO — registro explícito de /defensa

tests/
  contract/        # nuevos: FollowUpQuestionAgent, TranscriptionPort/SpeechSynthesisPort (dobles), endpoints
  integration/      # nuevos: escenarios A–F, equivalencia texto/voz, trazabilidad completa
  failure/          # nuevos: fallo STT, fallo TTS, baja confianza, tema fuera de alcance, evaluación bloqueada
  unit/             # nuevos: mapeo CognitiveState, umbral de confianza configurable
  speech/           # NUEVO — pruebas reales opcionales con faster-whisper/Piper, marcador `speech`
```

**Structure Decision**: mismo monolito modular ya establecido por las Features 001–003
(`domain/application/infrastructure/interfaces`) — esta feature añade únicamente
ficheros nuevos en las mismas carpetas ya existentes (`domain/agents/`,
`application/commands|services|orchestration/`, `infrastructure/`, `interfaces/api/routers/`)
más una carpeta nueva (`infrastructure/speech/`, análoga a `infrastructure/generation/`
de la Feature 003) para los dos adaptadores de voz. Los puntos de integración de las
Features 001–003 solo reciben extensiones aditivas documentadas: propósito/adaptador de
generación, catálogo/plantillas T090, registro del router en `app.py`, cliente API y ruta
web. Sus regresiones históricas demuestran que el comportamiento previo se conserva.

## Diseño W0 vinculante (2026-10-16)

### Puerta final T090 en todas las ramas

`defense_agency_composer` construye el candidato y sus bindings, pero no lo publica.
Para cada pregunta inicial, repregunta, aclaración, falta de evidencia, degradación,
mensaje de cierre y texto de resumen visible, el límite de aplicación:

1. resuelve una entrada exacta del catálogo por `(template_id, version, sha256)`;
2. construye `AuthorizationSnapshot` desde `Session`, `ActivityConfiguration`, política
   canónica y referencias autorizadas, nunca desde datos del generador;
3. persiste `GeneratedProposal` saneada y el `VerificationResult` final con su
   `authorization_context` dentro de la misma transacción del turno;
4. solo copia a `Turn.output_text` el texto aprobado; un bloqueo persiste
   `blocked=true`, `output_text=NULL` y `DialogueAction.finish` cuando no queda una
   alternativa autorizada;
5. permite como máximo un mensaje operativo de catálogo (`attempt=1`), sometido a una
   segunda verificación independiente. Un segundo bloqueo cierra en
   `closed_error_safe` sin una tercera salida.

Ninguna transformación posterior a la verificación puede publicarse. Toda transformación
crea otra propuesta y otro veredicto. La puerta no hace `commit` ni cierra la sesión; el
límite exterior mantiene el único commit.

### Cierre T150 e idempotencia

`end_defense_session` invoca `close_session_with_outcome`. Solo si
`transition_won=True` construye/entrega el resumen, escribe consentimiento, conserva o
elimina datos, registra los eventos propios del cierre y libera el bloqueo. Los
competidores devuelven el estado ya persistido, con resumen nulo, sin repetir efectos.
Todos los efectos del ganador pertenecen a la misma transacción y un rollback permite
un reintento limpio.

### Offload bloqueante y audio efímero

`blocking_speech_worker.py` reutiliza el contrato probado por
`BoundedBlockingWorker` de Feature 002: `ThreadPoolExecutor` dedicado, capacidad global
al proceso, cola/admisión FIFO cancelable, liberación del permiso ante fallo de envío y
construcción singleton protegida. El callable de worker procesa bytes/modelo y devuelve
un valor; nunca usa sesiones SQLAlchemy. El coroutine propietario decide si aún puede
persistir el resultado. Timeout o cancelación invalidan cualquier terminación tardía.

El router lee el `UploadFile` por bloques contabilizados hasta 10 MiB, valida formato y
duración máxima de 300 s antes de STT y siempre ejecuta `await upload.close()` en
`finally`. Las pruebas fuerzan el rollover de `SpooledTemporaryFile` y verifican el
cierre y la desaparición del artefacto temporal en éxito, rechazo, timeout y cancelación.
No se crea un archivo temporal nombrado adicional.

### Entrega y repetición de TTS

`POST /api/v1/defense-sessions/{session_id}/defense-turns/{turn_id}/speech` devuelve
`audio/wav` binario y `X-ORALIA-Text-SHA256`. Antes de sintetizar, comprueba pertenencia
del turno, `output_text` no nulo y `VerificationResult.verdict=approved`; usa exactamente
el texto persistido. Cada llamada, incluida «repetir», regenera audio efímero. Un turno
bloqueado/no autorizado devuelve `404`; un fallo técnico devuelve `503` y no altera el
turno ni oculta su texto aprobado.

### Cliente web

`client.ts` tipa todos los endpoints de defensa, admite `output_text: string | null`,
sube multipart y obtiene el WAV como `Blob`. `main.tsx` registra `/defensa`.
`DefensaOral.tsx` no crea burbuja ni solicita audio cuando `output_text` es nulo; para
texto aprobado crea/revoca un object URL, permite reproducir de nuevo mediante una nueva
petición y conserva el flujo textual cuando STT/TTS no están disponibles.

### Baseline y puertas de calidad

La línea base vigente antes de Feature 004 es 608 pruebas deterministas aprobadas y una
prueba Ollama real aprobada (2026-10-16). La suite obligatoria excluye `ollama` y
`speech`; las pruebas reales de voz se ejecutan por separado. El baseline Ruff durable
de T090 conserva su huella documentada y cualquier hallazgo nuevo pertenece a esta
feature.

## Complexity Tracking

*Sin violaciones que justificar — Constitution Check en PASS.*

## Cierre y revisión — integración final

Texto y confirmación STT transportan `closure_consent` explícito en cada petición;
el compositor lo valida y el cierre ganador aplica los scopes también por límites.
Un GET de transcripción por sesión, sin caché, expone turnos cronológicos y originales/
correcciones para revisión; el cierre voluntario requiere una confirmación posterior.
No se añaden tablas ni permisos implícitos. Las pruebas HTTP de 16 combinaciones y los
recorridos reales Playwright respaldan FR-020/FR-030/FR-031/FR-041.
