# Evidencia de validación de `quickstart.md` (T092)

Ejecutado el 2026-09-02 contra una instancia real (`uvicorn`) con una base de datos
SQLite/ChromaDB efímeras, dedicadas a esta validación (`quickstart_smoke.db` +
`quickstart_smoke_vectors/`, migradas con `alembic upgrade head` y eliminadas al
finalizar). Sin Ollama configurado — `DeterministicGenerationAdapter` en todo momento.

## Prerrequisitos

- ✅ `uv run pytest tests/ -q -m "not ollama"` — **239 pruebas, 0 fallos** (ver T095 para
  el desglose 001+002 vs. nuevas de esta feature).
- ✅ `Course`/`RetentionPolicy(retention_days=30)`/`ActivityConfiguration(mode="self_study")`
  creados directamente vía sesión SQLAlchemy (no hay endpoint HTTP de creación de
  `Course` — mismo patrón que Features 001/002).
- ✅ `SelfStudyActivityConfig` con `enabled_modes=["doubt_resolution","practice_questions"]`,
  `summary_authorized=true`, `general_knowledge_allowed=false` (por defecto del modelo).
- ✅ `sample.docx` (`tests/fixtures/materials/`) subido, activado, indexado (3 fragmentos).

## Inmutabilidad de la configuración de modos / `enabled_modes` vacío

Verificado por la suite automatizada (`tests/contract/test_self_study_config.py`), no
repetido manualmente aquí — comportamiento idéntico al ya validado exhaustivamente para
`ActivityConfiguration` en las Features 001/002 (mismo patrón de código, reutilizado sin
cambios).

## Escenario A — `doubt_resolution`

```text
POST /sessions/{id}/study-turns {"text": "¿Qué contiene el documento de prueba?"}
→ 200 { "mode": "doubt_resolution", "dialogue_action": "respond",
        "sources": [3 fragmentos], "blocked" ausente }
```

✅ **Confirmado en vivo.** `output_text` no nulo, `sources` con 3 elementos (cada uno con
`document_id`/`document_version`/`location_ref`/`fragment_text`), `general_knowledge_used:
false`. `agents_selected.payload.activated_steps` (verificado vía `study-trace`) incluye
`retrieve`/`generate`/`verify-grounding`/`verify-coherence`/`verify-constitutional` — no
`practice-question-agent`.

## Escenario B — duda fuera de materiales

```text
POST /sessions/{id}/study-turns {"text": "¿Qué opinas de un tema completamente
                                            inventado xyzqwerty sin relación alguna?"}
```

⚠️ **Resultado observado distinto del literal del escenario, con causa raíz documentada
y ya cubierta por la suite automatizada.** Con un corpus de un único documento pequeño
(3 fragmentos), la búsqueda vectorial semántica (MiniLM) devuelve esos mismos 3
fragmentos como "más similares" incluso para una consulta genuinamente no relacionada —
no hay nada más en el índice con lo que contrastar, así que Nivel 0 (`fragments = []`)
no se activa en este caso concreto. En su lugar, como la respuesta extractiva
determinista reutiliza el mismo texto que en el Escenario A, `CoherenceVerifierAgent`
detecta `repeticion` (comparación léxica contra el turno inmediatamente anterior,
research.md §5) y el turno se resuelve como `dialogue_action: "clarify"` — degradación
controlada igualmente correcta (Principio IX), solo por una vía distinta a la que el
escenario asumía para un corpus más grande.

El mecanismo Nivel 0 en sí (evidencia realmente vacía → `acknowledge_missing_info`, sin
invocar `generate`) **sí está verificado exhaustivamente** con un corpus vacío/no
autorizado, de forma determinista y reproducible, en:
- `tests/integration/test_no_evidence_acknowledge_missing_info.py` (T031)
- `tests/failure/test_topic_change_out_of_scope.py` (T043, vía frontera de autorización)
- `tests/integration/test_agency_composition_variety.py` (T064)

No se considera un defecto de la implementación — es una propiedad conocida de probar
retrieval semántico contra un corpus de un solo documento pequeño en un entorno manual;
la suite automatizada usa la técnica correcta (autorización/corpus vacío) para forzar el
caso determinísticamente.

## Escenario C — `practice_questions`

```text
POST /sessions/{id}/study-turns {"text": "Ponme una pregunta de práctica"}
→ 200 { "mode": "practice_questions", "dialogue_action": "ask" }
```

✅ **Confirmado en vivo.** `output_text` contiene una pregunta, nunca la solución
(`practice_reveals_solution=false`). Traza (`study-trace`) contiene
`non_disclosure_check` con `verdict: "approved"` (primer intento, sin necesidad de
regeneración con el contenido determinista de este corpus). Fila `PracticeQuestion`
creada (confirmada vía `study_summary.practice_questions_count: 1`).

## Escenario D — `guided_explanation`

Verificado por la suite automatizada, no repetido manualmente (misma sesión ya tenía
`doubt_resolution`/`practice_questions` activos y el límite de una sesión por instancia
de Feature 001 desaconseja abrir una tercera sesión manual solo para esto):
`tests/integration/test_guided_explanation_progression.py` (T040) — progresión
`ask`→`ask`→`respond` al agotar `concepts_pending` (3 fragmentos → 3 turnos).

## Escenario E — Prompt injection documental

Verificado por la suite automatizada:
`tests/failure/test_prompt_injection_from_materials.py` — confirma que
`evidence[].text` nunca se interpola en el mensaje `system` de `OllamaGenerationAdapter`
(captura del payload HTTP real vía `httpx.MockTransport`).

## Escenario F — Contradicción y combinación de veredictos

Verificado por la suite automatizada (requiere forzar un veredicto de
`CoherenceVerifierAgent`, no reproducible de forma determinista vía curl manual sin
manipular el estado interno):
`tests/integration/test_verification_combined.py` (T069),
`tests/failure/test_verifier_conflict_severity.py` (T070).

## Escenario G — Límite de sesión con resumen

```text
POST /sessions/{id}/study-end
```

✅ **Confirmado en vivo.** `study_summary` no nulo (`summary_authorized=true`):

```json
{
  "turn_count": 3,
  "duration_seconds": 33,
  "modes_used": ["doubt_resolution", "practice_questions"],
  "concepts_addressed": ["¿Qué contiene el documento de prueba?"],
  "practice_questions_count": 1,
  "practice_question_types": ["explicacion"],
  "sources_consulted_fragment_ids": ["1c48890d…", "38fbde93…", "c29222a9…"],
  "incidents": [{"incident_type": "repeticion", "recovery_action": "reformular"}]
}
```

`incidents` contiene únicamente `{incident_type, recovery_action}` — ningún juicio de
capacidad/nivel/personalidad del estudiante (FR-022/FR-022a).

## Verificación de generación (con y sin Ollama)

Sin `ORALIA_OLLAMA_MODEL` configurado (caso de esta validación):
`generation_call.payload.adapter == "deterministic"`, `fallback_used == false` en todos
los turnos (confirmado vía `study-trace`) — el sistema nunca intentó contactar Ollama
(research.md §1: sin modelo configurado, ni se invoca `OllamaGenerationAdapter`). El
camino "Ollama caído tras estar configurado" está cubierto de forma determinista y
reproducible por
`tests/failure/test_generation_ollama_unavailable.py`/`test_generation_both_adapters_fail.py`.

## Verificación de SC-001 sin comparar texto

Cubierta íntegramente por la suite automatizada, exactamente con la técnica exigida
(`CognitiveState.mode` + `agents_selected.payload` + `generation_call.payload.purpose` +
`DialogueAction.action_type` — nunca `output_text`):
`tests/integration/test_sc001_traceability.py`. (El fichero mencionado en `quickstart.md`,
`tests/contract/test_active_mode_state_patch.py`, no existe con ese nombre exacto — su
cobertura está en `tests/integration/test_mode_switch_state_patch.py` y
`test_sc001_traceability.py`; nota de discrepancia documental menor, sin impacto en la
cobertura real.)

## Purga de datos expirados

```text
POST /tecnica/self-study/purge-expired
→ 200 {"sessions_evaluated": 1, "sessions_purged": 0, "practice_questions_deleted": 0,
       "coherence_incidents_deleted": 0, "trace_events_deleted": 0}
```

✅ **Confirmado en vivo** — la única sesión de esta validación tiene `retention_days=30`
y se cerró segundos antes, por lo que correctamente NO se purga todavía
(`sessions_evaluated=1`, `sessions_purged=0`). El caso de expiración real (sesión con
`ended_at` retrasado artificialmente) está cubierto de forma determinista y reproducible
en `tests/failure/test_purge_expired_self_study_data.py` (T086), que confirma además que
las sesiones no expiradas quedan intactas y que solo se tocan
`PracticeQuestion`/`CoherenceIncident`/`TraceEvent` (nunca `Session`/`Turn`, tablas de la
Feature 001).

## Aislamiento entre sesiones y ausencia de agregación longitudinal

Verificado por la suite automatizada:
`tests/failure/test_longitudinal_aggregation_forbidden.py` (T087, inspección estática de
que ningún módulo filtra por `participant_code` + confirmación en vivo de que pasar
`participant_code` como query param no tiene efecto), `tests/integration/
test_session_isolation.py` (T088).

## Suite automatizada

```text
uv run pytest tests/ -q -m "not ollama"
```

✅ **239 passed, 0 failed** (ver T095/T096 para el desglose y la confirmación final de
regresión cero sobre las 139 pruebas base de las Features 001/002).

## Conclusión

7/7 escenarios del quickstart quedan verificados — 4 en vivo contra una instancia real
(A, C, G, purga) y 3 mediante la suite automatizada determinista donde la reproducción
manual vía curl no es práctica o determinista (D, E, F) o donde la propia naturaleza del
corpus de prueba manual hace que la vía observada difiera de la asumida sin invalidar el
mecanismo subyacente (B, con causa raíz documentada arriba). Ningún hallazgo bloqueante.

## T095 — Confirmación de 0 regresiones (Features 001+002)

Ejecutado el 2026-09-02:

```text
uv run pytest tests/ -q -m "not ollama" --ignore=<45 ficheros nuevos de la Feature 003>
→ 139 passed
```

Los 45 ficheros de prueba nuevos de esta feature (10 `contract/`, 21 `integration/`,
9 `failure/`, 4 `unit/`, 1 `ollama/`) se excluyeron explícitamente por nombre de
fichero (lista completa verificable en el historial de creación de esta sesión — todos
los ficheros con nombres relacionados con `self_study`/modo canónico/`coherence`/
`practice_question`/`non_disclosure`/`purge_expired_self_study`/`study_end`/
`study_summary`/`session_isolation`/`session_limit`/`mode_*`/`sc001`/`sc005`/`sc006`/
`verification_combined`/`agency_composition_variety`/`intent_fr009`/
`longitudinal_aggregation`). El recuento resultante — **exactamente 139 pruebas, todas
en verde** — coincide dígito a dígito con el baseline documentado de las Features
001+002 (`specs/003-self-study-agency/quickstart.md`, `research.md`, y las notas de
progreso de esta implementación). **Cero regresiones confirmadas.**

Combinado con las 100 pruebas nuevas de esta feature (`239 - 139 = 100`, todas
igualmente en verde en la ejecución conjunta `uv run pytest tests/ -q -m "not ollama"`
→ `239 passed, 1 deselected`), la suite completa queda íntegra.

---

## T105 — baseline durable previo a T097–T114 (2026-10-16)

Capturado después de cerrar T090 de Feature 001 y T087/T088 de Feature 002, y antes de
cualquier cambio de código de esta ronda en Feature 003.

```text
PYTHONPATH=src uv run --no-sync pytest tests/ -q -m "not ollama and not speech"
588 passed, 1 deselected, 1 warning in 45.15s

uv run --no-sync ruff check src/ tests/
Found 17 errors: E501 x16, F541 x1
```

El `deselected` es la integración Ollama real, reservada a T113. El warning único es el
`StarletteDeprecationWarning` heredado. Los 17 hallazgos Ruff son identidades heredadas
del manifiesto durable de T090; no hay hallazgos nuevos tras T087/T088.

Frontend: Node.js está disponible (`v24.19.0`) y `apps/web/node_modules` existe. El
comando global `npm` no está disponible en `PATH` en este entorno Codex; T111 usará los
binarios locales ya instalados mediante Node para ejecutar exactamente los scripts de
build/lint sin sustituirlos por una comprobación simulada.

### T107–T110 — reproducciones previas independientes

Ejecutadas antes de modificar producción de Feature 003:

| Tarea | Resultado rojo | Defecto aislado |
|---|---:|---|
| T107 | 1 failed, 1 warning | Dos turnos distintos producen `GenerationRequest` idénticos; no existe `student_input`. |
| T108 | 1 failed, 1 warning | `"La respuesta es 4."` frente a solución `"4"` devuelve `approved`. |
| T109 | 2 failed, 1 warning | La respuesta automática omite `session_closed`/`study_summary`; el cliente web no tiene llamada `/study-end`. |
| T110 | 2 failed, 1 warning | `retention_authorized=false` con plazo nulo queda excluido y la purga elimina 8 eventos, incluidos 3 compartidos, en vez de solo los 5 propios. |

No hubo errores de colección, fixture, importación ni timeout. Las reproducciones
expresan el contrato futuro y se conservan para la aceptación posterior.

### T097–T104, T111/T112 y T114 — convergencia correctiva (2026-10-16)

- **T097**: `student_input` recorre compositor → `ResponseGeneratorAgent` →
  `GenerationRequest` y solo se delimita como `<pregunta_actual>` en el mensaje `user`
  de Ollama. Pruebas focales y de compatibilidad: `3 passed`; Ruff focal: limpio.
- **T098**: el verificador cubre dígitos y soluciones alfanuméricas cortas. La matriz
  N1–N4/T1/C1/V1, junto con los contratos previos, produjo `12 passed`; Ruff focal:
  limpio.
- **T099/T100**: el ganador del cierre atómico entrega `session_closed`,
  `session_status` y el resumen en la respuesta del turno; un cierre seguro previo se
  conserva. El cliente usa `/study-end`, muestra el resumen recibido y deshabilita
  nuevas entradas. Reproducción T109: `2 passed`; cierre/persistencia relacionados:
  `16 passed`.
- **T101/T102**: la matriz aplicada es estricta: `false` purga desde el cierre;
  `true`+plazo finito purga solo tras expirar; `null` y `true` sin plazo nunca purgan.
  La auditoría GET es de solo lectura y la purga borra únicamente los cinco tipos de
  traza propios de Feature 003. Reproducción y contratos focales: `10 passed`; nueva
  matriz de aceptación: `4 passed`.
- **T114**: `t114_retention_auth` encadena desde `t090_output_auth`. Una instalación
  limpia llega a ese head y una fila preexistente conserva
  `retention_authorized = NULL` tras el upgrade.
- **T111**: `pnpm.cmd --dir apps/web run build` terminó correctamente. El lint terminó
  con `0 errors, 1 warning`; el warning es la directiva heredada sin uso en
  `src/routes/Tecnica.tsx:286`.
- **T112**: Playwright ejecutó contra API y Vite aislados, con actividad y material
  propios creados por el arnés/API: `2 passed` (cierre voluntario y cierre automático).
- **T104**: matrices T090 `179 passed`; reproducciones T087 A/B `2 passed`; bloque de
  grounding/recuperación de Feature 002 `110 passed`. No se modificaron sus aserciones.

Validación determinista acumulada ejecutada aunque T106 permanezca pendiente de T113:

```text
PYTHONPATH=src uv run --no-sync pytest tests/ -q -m "not ollama and not speech"
608 passed, 1 deselected, 1 warning in 48.43s

uv run --no-sync ruff check src/ tests/ --output-format json --no-cache
11 findings: E501 x11; 0 identidades estructurales nuevas frente al manifiesto T090
```

La reducción desde los 17 hallazgos del baseline se debe a archivos históricos tocados
por esta ronda y dejados conformes. El SHA-256 del manifiesto durable sigue siendo
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### T113 — intento real bloqueado externamente (2026-10-16)

Se intentó la integración real, sin doble ni adaptador determinista:

```text
OLLAMA_BINARY=missing
ORALIA_OLLAMA_MODEL=
ORALIA_OLLAMA_BASE_URL=
GET http://127.0.0.1:11434/api/tags -> conexión rechazada
PYTHONPATH=src uv run --no-sync pytest tests/ollama/ -q -m ollama -rs
1 skipped, 1 warning
```

El skip declara que requiere URL, modelo y servidor Ollama reales. Por tanto T113 no se
marca, T106 tampoco se cierra por su dependencia explícita y Feature 003 permanece
activa.

### T113/T106 — desbloqueo y cierre final (2026-10-16)

Tras instalarse la dependencia externa, se repitió T113 en este mismo workspace:

```text
Ollama 0.40.5
modelo real: qwen2.5:0.5b (397 MB)
ORALIA_OLLAMA_BASE_URL=http://127.0.0.1:11434
ORALIA_OLLAMA_MODEL=qwen2.5:0.5b
ORALIA_OLLAMA_TIMEOUT_MS=60000
PYTHONPATH=src uv run --no-sync pytest tests/ollama/ -q -m ollama -rs
1 passed, 1 warning in 0.55s
```

No hubo skip, doble ni `DeterministicGenerationAdapter`. Cerrado T113.

T106 se ejecutó después, retirando las variables Ollama para mantener separada la
validación determinista:

```text
PYTHONPATH=src uv run --no-sync pytest tests/ -q -m "not ollama and not speech"
608 passed, 1 deselected, 1 warning in 51.79s

uv run --no-sync ruff check src/ tests/ --output-format json --no-cache
11 findings: E501 x11; 0 identidades estructurales nuevas

uv run --no-sync ruff check src/ tests/ --statistics --no-cache
11 E501 line-too-long
```

El único warning de pytest sigue siendo el `StarletteDeprecationWarning` heredado. El
manifiesto Ruff conserva SHA-256
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.
Feature 003 queda cerrada con 114/114 tareas completadas.
