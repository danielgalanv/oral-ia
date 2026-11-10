# Contrato HTTP: Agencia de defensa oral y voz opcional

Ningún endpoint de las Features 001/002/003 se modifica (FR-033). Router propio,
registrado por separado en `app.py`, mismo patrón que `self_study.router` de la Feature
003.

## Área de participante

### `POST /api/v1/defense-sessions/{session_id}/defense-turns`

Turno de defensa por **texto** (equivalente a `POST /sessions/{id}/study-turns` de la
Feature 003, endpoint propio de esta feature — no reutiliza el mismo path porque el
recurso es un turno de defensa, no de autoestudio).

**Request**: `{ "text": string }`.

Puede añadirse `requested_topic` con un valor exacto de `DefenseActivityConfig.topics`;
un valor distinto devuelve `409` antes de crear el turno.

**Response `200`**:
```json
{
  "turn_id": "uuid",
  "dialogue_action": "ask | clarify | acknowledge_missing_info | finish",
  "dialogue_purpose": "deepen_current_topic | switch_topic | null",
  "output_text": "string | null",
  "state_version": "int",
  "sources": [
    { "document_id": "uuid", "document_version": "int", "location_ref": "string", "fragment_text": "string" }
  ],
  "general_knowledge_used": "bool",
  "blocked": "bool",
  "speech": "descriptor | null"
}
```

**Reglas**: `dialogue_purpose` solo está presente cuando `dialogue_action="ask"` y
distingue profundizar de cambiar de tema (research.md §10) — nunca un valor nuevo de
`dialogue_action`. `404` si la sesión no existe o no está activa. `409` si se solicita
un tema fuera del alcance autorizado (mismo aislamiento que `MaterialRetrieverAgent`,
Feature 002, sin cambios). `clarify` en este endpoint **únicamente** representa una
ambigüedad semántica detectada por `DefenseAgency` sobre el texto ya recibido — nunca
una incidencia de baja confianza de transcripción (research.md §5/§10; esa incidencia se
resuelve enteramente en `POST /defense-turns/voice`, antes de que este endpoint —o el
pipeline cognitivo que representa— se ejecute).

Cuando la puerta final bloquea y tampoco autoriza el único mensaje operativo, responde
con `blocked=true`, `dialogue_action="finish"`, `output_text=null` y `speech=null`; nunca
incluye el candidato rechazado. Para texto aprobado y voz permitida, `speech` contiene
`{available:true,url,media_type:"audio/wav",text_sha256}`.

### `POST /api/v1/defense-sessions/{session_id}/defense-turns/voice`

Turno de defensa por **voz** — recibe audio, transcribe localmente, y **no** avanza el
turno hasta que el estudiante confirme o corrija (research.md §5).

**Request**: `multipart/form-data` con el audio capturado (`audio/wav` o `audio/webm`),
máximo 10 MiB y 300 segundos.

**Response `200`** (si `voice_input_allowed=false` para la actividad → `409`):
```json
{
  "transcript_id": "uuid",
  "raw_text": "string",
  "segments": [ { "text": "string", "start_ms": "int|null", "end_ms": "int|null", "confidence": "float" } ],
  "overall_confidence": "float",
  "low_confidence": "bool"
}
```

**Reglas**: este endpoint **no** produce una repregunta ni actualiza `CognitiveState`, ni
invoca `MaterialRetrieverAgent`/`GenerationPort`/`FollowUpQuestionAgent`/
`GroundingVerifierAgent`/`CoherenceVerifierAgent` — únicamente transcribe y devuelve la
transcripción provisional para revisión (research.md §4/§5). La respuesta **MUST NOT**
incluir ningún `dialogue_action`: el turno queda en un estado `awaiting_confirmation`
observable, previo a cualquier decisión de `DefenseAgency`. Si la transcripción falla
técnicamente, el audio ya ha sido descartado (research.md §3) y el cliente debe recurrir
a `defense-turns` (texto) para ese turno.

Contrato cerrado de errores: `413` si el flujo supera 10 MiB; `422` si formato o
duración no son válidos o si supera 300 segundos; `503` con
`{"code":"transcription_unavailable","fallback_to_text":true}` ante fallo técnico o
timeout de STT. No existe respuesta `200 ok:false`. El router cierra siempre el
`UploadFile` en `finally`, incluido cualquier spool temporal creado por multipart.

### `POST /api/v1/defense-sessions/{session_id}/defense-turns/voice/confirm`

Confirma o corrige una transcripción provisional y avanza el turno con la versión
definitiva (research.md §4).

**Request**:
```json
{ "transcript_id": "uuid", "corrected_text": "string | null" }
```

`corrected_text: null` (o ausente) ⇒ el estudiante confirma sin modificar;
`Transcript.raw_text` pasa a ser la versión definitiva directamente, sin crear
`TranscriptCorrection` (research.md §4). `corrected_text` no nulo ⇒ crea
`TranscriptCorrection` y esa es la versión definitiva.

Una confirmación repetida sin modificación devuelve `409`. Una revisión explícita de
una transcripción ya confirmada inicia un nuevo turno con una nueva transcripción y
corrección; no modifica la pregunta, entrada ni versión confirmada del turno anterior.
No se aceptan revisiones cuando la sesión ha cerrado.

**Response `200`**: misma forma que `POST /defense-turns` (texto) — a partir de aquí el
pipeline es idéntico independientemente de la modalidad de entrada (research.md §6).

Las respuestas de turno incluyen además `session_status` y `defense_summary` nullable.
Un cierre automático entrega el resumen autorizado en esa misma respuesta, una sola vez;
una llamada posterior a `defense-end` devuelve resumen nulo.

### `GET /api/v1/defense-sessions/{session_id}/settings`

Devuelve únicamente `voice_input_allowed`, `voice_output_allowed`,
`transcript_retention_authorized` y `low_confidence_threshold` para los controles de
modalidad. No expone política, modelos, materiales ni datos de otras sesiones.

### `POST /api/v1/defense-sessions/{session_id}/defense-turns/{turn_id}/speech`

Genera o repite bajo demanda la voz del texto final aprobado. Antes de invocar TTS,
comprueba que el turno pertenece a la sesión, `Turn.output_text` no es nulo y su
`VerificationResult` final está aprobado.

**Response `200`**: cuerpo binario `audio/wav`, cabecera
`X-ORALIA-Text-SHA256: <sha256 UTF-8 exacto de Turn.output_text>` y
`Cache-Control: no-store`. `404` si no existe salida aprobada o el turno no pertenece a
la sesión; `409` si la actividad no permite voz; `503` si TTS falla o expira. Cada
llamada vuelve a sintetizar el mismo texto persistido, sin almacenar audio ni reejecutar
el turno cognitivo.

### `POST /api/v1/defense-sessions/{session_id}/defense-end`

Sin cambios de mecanismo respecto al patrón ya usado en `POST /sessions/{id}/study-end`
(Feature 003) — reutiliza `close_session_with_outcome` (Feature 001), añade
`defense_summary` (`null` si `summary_authorized=false`), y — si
`transcript_retention_authorized=true` para la actividad — acepta la decisión de
conservación del participante. Esta decisión (`ConsentRecord`, research.md §15) **no**
es un requisito para cerrar la sesión ni condiciona nada anterior al cierre — por
defecto (sin `retain: true` explícito, o si la actividad no autoriza conservación en
absoluto), `Transcript`/`TranscriptCorrection`/el `TraceEvent` de resumen de esa sesión
se eliminan en este mismo cierre.

**Request** (opcional, solo si `transcript_retention_authorized=true`):
```json
{ "retain": "bool", "scope": ["transcript", "summary"] }
```

**Response `200`**:
```json
{
  "session_id": "uuid",
  "status": "string",
  "defense_summary": { "...": "ver research.md §14" } 
}
```

Solo el llamante con `transition_won=true` ejecuta resumen, consentimiento,
retención/eliminación, evento y liberación de cierre. Una repetición o competidor
devuelve el estado persistido con `defense_summary:null` y sin efectos.

## Área técnica (docente)

### `POST /api/v1/tecnica/activities/{activity_id}/defense-config`

**Request**:
```json
{
  "initial_questions": ["string", "..."],
  "difficulty_hint": "baja | media | alta",
  "voice_input_allowed": false,
  "voice_output_allowed": false,
  "summary_authorized": false,
  "transcript_retention_authorized": false
}
```

**Reglas** (research.md §12): `201`/`200` si `ActivityConfiguration.immutable_since` es
`null` (mismo patrón que `self-study-config`, Feature 003); `409` si ya es inmutable;
`422` si `initial_questions` está vacío y la actividad no tiene materiales autorizados
asociados (FR-002a).

### `GET /api/v1/tecnica/defense-sessions/{session_id}/defense-trace`

Reutiliza `reconstruct_session_trace` (Feature 001, genérico por `event_type`, sin
cambios) — incluye los `event_type` nuevos de esta feature (data-model.md). Solo admite
`session_id` como clave — ninguna ruta de esta feature acepta `participant_code` como
parámetro de agregación entre sesiones (FR-032).

### `POST /api/v1/tecnica/defense/purge-expired`

Invocación manual del profesorado/administrador (Principio VI) — mismo patrón que
`purge-expired` de la Feature 003, fichero propio (`purge_expired_defense_data`), sin
generalizar el de la Feature 003 (research.md §1).

**Response `200`**:
```json
{
  "sessions_matching_criteria": "int",
  "sessions_with_rows_deleted": "int",
  "transcripts_deleted": "int",
  "transcript_corrections_deleted": "int",
  "trace_events_deleted": "int"
}
```


## Límites de conservación y concurrencia al cierre

Habilitar `transcript_retention_authorized` sin política con `retention_days` finito y
no negativo devuelve 422. La misma validación precede a cualquier cierre con
`retain=true`, también para configuraciones antiguas. La eliminación del scope
`transcript` incluye las copias operativas de contenido en turnos, propuestas, estado,
parches, mensajes y trazas; permanecen metadatos estructurales de auditoría. El scope
`summary` controla separadamente los hechos del resumen y el texto de su propuesta.

Los recursos de defensa rechazan con 404 sesiones cuyo modo no sea `oral_defense`.
Si la sesión se cierra durante STT, se descarta el resultado sin recrear transcripción.
Si el contenido aprobado se elimina durante TTS, no se publica el audio tardío. El
navegador cancela síntesis pendiente al cerrar y libera las URL de audio.

## Corrección de cierre automático y revisión completa (2026-10-17)

Los cuerpos de `POST /defense-turns` y `POST /defense-turns/voice/confirm` aceptan
`closure_consent: {retain: boolean, scope: ["transcript", "summary"]}`. La elección
explícita actual se valida antes del turno y se aplica si ese turno cierra por límite
o cierre seguro. No crea consentimiento anticipado, no cambia la política ni autoriza
conservar por defecto. El único ganador T150 escribe ConsentRecord y ejecuta los scopes;
una llamada repetida no puede cambiar la elección ni restaurar contenido eliminado.
La configuración debe autorizar retención y tener plazo finito no negativo.

`GET /api/v1/defense-sessions/{session_id}/defense-transcript` devuelve, con
`Cache-Control: no-store`, los turnos cronológicos y los originales/correcciones de
voz de esa sesión de defensa. No genera contenido ni agrega otras sesiones. Tras borrar
contenido devuelve listas vacías. La UI permite abrir esta revisión durante la sesión;
el cierre voluntario primero carga el registro completo y después requiere
«Confirmar cierre de sesión». Las selecciones de scope viajan tanto con respuestas de
texto como con confirmaciones de voz para respetarlas al alcanzar límites.

Evidencia: `tests/contract/test_defense_automatic_close_consent.py` (16 combinaciones de
turnos/duración × texto/voz × cuatro elecciones), y recorridos reales Playwright de
cierre voluntario, límite de turnos y duración, conservación selectiva, revisión,
repetición de cierre y purga del almacenamiento aislado de pruebas.
