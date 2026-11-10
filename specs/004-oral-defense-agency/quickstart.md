# Quickstart: Agencia de defensa oral y voz opcional

Guía de validación extremo a extremo, análoga a
`specs/003-self-study-agency/quickstart.md`. No sustituye a la suite automatizada.

## Validación ejecutable desde PowerShell

Desde la raíz del workspace, sin modificar la base de datos de uso normal:

```powershell
uv lock --check --offline
uv run --no-sync pytest tests/ -q -m "not ollama and not speech"
pnpm.cmd --dir apps/web build
pnpm.cmd --dir apps/web lint
pnpm.cmd --dir apps/web test:e2e
```

Playwright inicia su API y Vite aislados y ejecuta los flujos en serie porque el
producto tiene un único bloqueo de sesión activa. `test_defense_full_session.spec.ts`
crea curso/configuración de prueba sobre las fixtures aisladas, carga y activa un DOCX
y usa navegador y HTTP reales para pregunta, respuesta, resumen autorizado, traza,
repetición de cierre y purga. No necesita STT/TTS ni Ollama.

Las matrices reproducibles de voz usan dobles deterministas, expresamente separados
de las pruebas de modelos locales:

| Escenario | Evidencia ejecutable |
|---|---|
| A: texto, varias repreguntas, cambio de tema, cierre y resumen | `uv run --no-sync pytest tests/integration/test_defense_text_full_session.py -q` |
| B: confirmar, corregir y revisión no retroactiva | `uv run --no-sync pytest tests/integration/test_defense_voice_lifecycle.py tests/integration/test_defense_correction_not_retroactive.py -q` |
| C: fallo STT/TTS y continuidad textual | `uv run --no-sync pytest tests/failure/test_defense_speech_exceptions.py tests/failure/test_defense_worker_request_lifetime.py -q` |
| D y D': revisión STT previa y aclaración cognitiva distinta | `uv run --no-sync pytest tests/integration/test_defense_voice_lifecycle.py tests/integration/test_defense_remaining_boundaries.py tests/integration/test_defense_dialogue_contract.py -q` |
| E: bloqueo nulo y único fallback operativo autorizado | `uv run --no-sync pytest tests/contract/test_defense_output_authorization_matrix.py tests/failure/test_defense_no_evaluation.py -q` |
| F: ganador único, consentimiento, eliminación y purga aislada | `uv run --no-sync pytest tests/integration/test_defense_close_transition_outcome.py tests/integration/test_defense_retention_and_purge.py tests/contract/test_defense_end_consent.py -q` |
| WAV literal, replay, 404/409/503 | `uv run --no-sync pytest tests/contract/test_defense_speech_endpoint.py tests/contract/test_defense_voice_and_speech.py -q` |
| 10 MiB, 300 s y cierre del spool en toda salida | `uv run --no-sync pytest tests/contract/test_defense_voice_upload_limits.py tests/contract/test_defense_rolled_spool_lifecycle.py tests/failure/test_defense_speech_timeout_late_results.py -q` |

El inventario y los resultados medidos se registran en `implementation-evidence.md`.
Los ejemplos `curl` siguientes son para Bash; en PowerShell puede usarse
`Invoke-RestMethod` con `-ContentType application/json` y el mismo cuerpo JSON.

## Prerrequisitos

1. Features 001, 002 y 003 con su suite pasando
   (`uv run pytest tests/ -q -m "not ollama"`).
2. Un `Course`, una `ActivityConfiguration` con `mode = "oral_defense"` (creada, **sin**
   iniciar ninguna sesión todavía) y su `DefenseActivityConfig` asociado con al menos
   una `initial_question` o materiales autorizados.
3. **Opcional**: `ORALIA_STT_MODEL`/`ORALIA_TTS_VOICE` configurados para probar voz real;
   sin ellos, la actividad no puede habilitar `voice_input_allowed`/
   `voice_output_allowed`, y el Escenario A (texto) cubre igualmente todo el flujo.
4. Política T090 explícita para el código destinatario. Las preguntas dinámicas usan
   `generated_defense/defense-agency`; el resumen requiere por separado
   `defense_summary/persisted_session_facts`, plantilla `defense-summary@1` y scope
   `activity/oral_defense_summary/respond`. `summary_authorized=true` por sí solo no
   concede permiso de publicación. El ejemplo completo está en la prueba HTTP citada.

## Arranque

```bash
uv run uvicorn oralia.interfaces.api.app:app --reload
```

## Escenario A — Defensa textual completa

```bash
curl -s -X POST localhost:8000/api/v1/sessions \
  -H 'Content-Type: application/json' \
  -d '{"participant_code":"est-001","activity_configuration_id":"<activity_id>"}'
# SESSION_ID de la respuesta

curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns \
  -H 'Content-Type: application/json' -d '{"text":""}' | jq
# Presenta la pregunta inicial antes de responder.

curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns \
  -H 'Content-Type: application/json' \
  -d '{"text":"<respuesta a la pregunta inicial>"}' | jq
```

**Esperado**: `dialogue_action: "ask"` con `dialogue_purpose` presente en los turnos
siguientes, `output_text` no nulo, `sources` con al menos un elemento cuando la
repregunta usa materiales. Repetir varios turnos y verificar (vía `defense-trace`) que
`followup_question_generated.referenced_concept` mantiene relación con la respuesta
o la evidencia; las preguntas no se repiten literalmente.

Si la puerta final bloquea el candidato y el único mensaje operativo tampoco se
autoriza, se espera `blocked:true`, `dialogue_action:"finish"`, `output_text:null` y
`speech:null`; no debe aparecer ninguna burbuja ni contenido rechazado.

## Escenario B — Defensa por voz

```bash
curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns/voice \
  -F "audio=@respuesta.wav" | jq
# TRANSCRIPT_ID de la respuesta

curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns/voice/confirm \
  -H 'Content-Type: application/json' \
  -d "{\"transcript_id\":\"$TRANSCRIPT_ID\",\"corrected_text\":null}" | jq
```

**Esperado**: el primer `curl` devuelve la transcripción provisional sin avanzar el
turno; el segundo (confirmando sin editar) avanza el turno usando `raw_text` como
definitiva — sin fila `TranscriptCorrection`. Repetir con `corrected_text` no nulo y
verificar, vía `defense-trace`, el evento `transcript_corrected`.

## Escenario C — Fallo de transcripción

Con `ORALIA_STT_MODEL` apuntando a un modelo inexistente o el servicio no disponible:

```bash
curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns/voice \
  -F "audio=@respuesta.wav" | jq
```

**Esperado**: fallo informado con claridad; `TraceEvent transcription_failed` presente;
el estado de la sesión permanece intacto; el estudiante puede continuar con
`POST /defense-turns` (texto) sin perder turnos ya completados.

Una carga mayor de 10 MiB devuelve `413`; formato/duración inválidos o más de 300 s
devuelven `422`. En ambos casos STT no se invoca y el recurso multipart queda cerrado.

## Escenario D — Transcripción de baja confianza

Con un audio de prueba deliberadamente poco claro (fixture):

**Esperado**: `low_confidence: true` en la respuesta de `/defense-turns/voice`, **sin
ningún campo `dialogue_action`** (research.md §5/§10 — esto es una incidencia de
modalidad, no una decisión de `DefenseAgency`); ningún `TraceEvent` de
`agent_execution`/`generation_call`/`verification_combined` para ese turno hasta que se
llame a `/voice/confirm`; el turno permanece `awaiting_confirmation` y no genera
repregunta hasta la confirmación o corrección.

## Escenario D' — Respuesta textual definitiva ambigua

Con una respuesta de texto (directa o ya confirmada tras voz) deliberadamente vacía de
contenido reconocible:

**Esperado**: `dialogue_action: "clarify"` — a diferencia del Escenario D, aquí
`DefenseAgency` **sí** se ejecutó sobre la transcripción/texto definitivo y decidió que
el significado era insuficiente para continuar (research.md §9/§10); los `TraceEvent`
de la agencia (`agent_execution`, `verification_combined`) sí están presentes.

## Escenario E — Intento de evaluación

Fixture de prueba (no manual): una propuesta de repregunta/resumen que contenga
`"nota: 8"` o `"has aprobado"`.

**Esperado**: la puerta final T090 la bloquea (`verdict="block"`) y el candidato no se
publica. Puede aparecer un único mensaje operativo solo si su segundo veredicto es
`approved`; de lo contrario `output_text` es `null` y la sesión cierra en seguro.

## Reproducción de voz aprobada

```bash
curl -s -X POST \
  localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-turns/$TURN_ID/speech \
  -D speech.headers -o speech.wav
```

**Esperado**: `audio/wav`, `Cache-Control: no-store` y
`X-ORALIA-Text-SHA256` igual al SHA-256 UTF-8 del `Turn.output_text` aprobado. Repetir la
llamada regenera el mismo texto sin conservar audio ni reejecutar el turno. Un turno con
`output_text:null` devuelve `404`.

## Escenario F — Cierre y consentimiento

```bash
curl -s -X POST localhost:8000/api/v1/defense-sessions/$SESSION_ID/defense-end \
  -H 'Content-Type: application/json' \
  -d '{"retain": false}' | jq
```

**Esperado**: `defense_summary` no nulo si `summary_authorized=true` y la política
autoriza exactamente el resumen; sin
`ConsentRecord` si `transcript_retention_authorized=false` para la actividad (nada que
decidir); con `retain:false` y retención autorizada, `Transcript`/`TranscriptCorrection`
de la sesión dejan de ser recuperables inmediatamente tras el cierre.

Repetir la petición, también de forma concurrente: solo una llamada gana la transición y
ejecuta resumen/consentimiento/retención/evento/liberación; las demás devuelven el estado
persistido con `defense_summary:null`.

## Verificación de trazabilidad completa

```bash
curl -s localhost:8000/api/v1/tecnica/defense-sessions/$SESSION_ID/defense-trace | jq
```

**Esperado**: la secuencia completa descrita en research.md §17 es reconstruible;
ningún evento contiene audio.

## Purga de datos expirados

```bash
curl -s -X POST localhost:8000/api/v1/tecnica/defense/purge-expired | jq
```

**Esperado**: `200` con los contadores de `PurgeResult` (data-model.md); una sesión
expirada pierde transcripciones, correcciones y contenido operativo de sus scopes
conservados. Permanecen metadatos estructurales de auditoría sin ese contenido; una
sesión no expirada no se ve afectada. Autorizar conservación requiere un plazo finito
y no negativo en `RetentionPolicy.retention_days`.

## Suite automatizada

```bash
uv run pytest tests/ -q -m "not ollama and not speech"   # deterministas, obligatorio en CI
uv run pytest tests/ -q -m "speech"                       # solo con faster-whisper/Piper instalados
```

Voz real opcional, sin descarga silenciosa:

```powershell
uv sync --extra dev --extra speech
$env:ORALIA_STT_MODEL = 'C:\modelos\faster-whisper-local'
$env:ORALIA_TTS_VOICE = 'C:\modelos\voz-local.onnx'
uv run --no-sync pytest tests/ -q -m speech
```

La fixture `tests/fixtures/defense_voice.wav` es voz sintética local de Windows,
con el texto inglés «The system separates generation and verification». No contiene
audio de participantes. Sin las variables, las dos pruebas reales se omiten con motivo
explícito; no se cuentan como aprobadas ni afectan a la puerta determinista.

**Esperado**: la suite completa (001+002+003+004, sin marcadores `ollama`/`speech`) pasa
sin regresiones sobre el baseline vigente de 608 pruebas deterministas de las Features
001–003. Las pruebas reales Ollama y `speech` se informan por separado.

## Regresión de consentimiento en cierre automático

```powershell
uv run --no-sync pytest tests/contract/test_defense_automatic_close_consent.py -q
pnpm.cmd --dir apps/web test:e2e
```

Antes de responder, marca los scopes deseados. Cada respuesta textual y confirmación
STT envía `closure_consent`; si alcanza el límite de turnos o duración, el cierre ganador
aplica esa elección. Sin elección se elimina. Abre «Revisar transcripción completa»
durante la sesión para consultar el registro persistido, incluidos originales y
correcciones de voz. «Finalizar sesión» carga esa revisión; revisa los scopes y pulsa
«Confirmar cierre de sesión». La purga elimina también las copias operativas al expirar.
Los tres recorridos HTTP reales de Playwright verifican estos pasos y la idempotencia.
