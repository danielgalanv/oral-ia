# Quickstart: validar Núcleo cognitivo y ejecución local

Guía de validación extremo a extremo. No sustituye a `tasks.md` (aún no generado) ni
contiene código de implementación — solo pasos ejecutables y resultados esperados,
referenciando `data-model.md` y `contracts/`.

## Prerrequisitos

- Python 3.12 con `uv` instalado.
- Node.js LTS (para `apps/web`).
- Ningún servicio externo ni conexión a Internet requerida (Principio VII, FR-022).

## Preparación del entorno

```bash
uv sync
uv run alembic upgrade head
uv run python -m oralia.scripts.seed_demo   # crea: 1 Course, 1 RetentionPolicy,
                                             # 1 ActivityConfiguration de prueba,
                                             # ≥5 Agent de prueba bajo el mismo AgentContract,
                                             # ≥2 Agency que reutilizan esos agentes
```

```bash
uv run uvicorn oralia.interfaces.api.app:app --host 127.0.0.1 --port 8000
cd apps/web && npm install && npm run dev
```

## Escenario A — Sesión válida (User Story 2, SC-007)

1. Abrir `/participante`, iniciar sesión con un código seudónimo sobre la actividad de
   demo (`POST /api/v1/sessions` — `contracts/api-participante.md`).
   - **Esperado**: se muestra el aviso de sistema automático antes de aceptar el primer
     mensaje (FR-010).
2. Enviar un mensaje de texto (`POST /api/v1/sessions/{id}/turns`).
   - **Esperado**: respuesta `200` con `dialogue_action` y `output_text`; `state_version`
     incrementado respecto al estado inicial.
3. Finalizar la sesión voluntariamente (`POST /api/v1/sessions/{id}/end`).
   - **Esperado**: el participante recibe solo `confirmation_message` (FR-012b), sin
     calificación ni resumen técnico completo.
4. Desde `/tecnica`, consultar `GET /api/v1/sessions/{id}` y `GET /api/v1/sessions/{id}/trace`.
   - **Esperado**: se reconstruye la secuencia completa (agentes ejecutados, mensajes
     internos, cambios de estado, decisión de acción) — valida SC-004.

## Escenario B — Salida bloqueada (User Story 3, SC-005)

1. Ejecutar el agente de prueba configurado para proponer una salida prohibida (asigna
   nota / decisión académica) dentro de una `Agency` de demo.
2. Enviar un turno que dispare ese agente.
   - **Esperado**: `output_text` no revela el contenido prohibido; `blocked: true`
     (`contracts/api-participante.md`).
3. Consultar `GET /api/v1/sessions/{id}/trace`.
   - **Esperado**: un `VerificationResult` con `verdict = "block"` y `reasons` observables.

**Limitación conocida (estabilización 2026-09-10, research.md §8)**: el agente de prueba
de este escenario usa frases con el patrón léxico ya cubierto por
`constitutional_control.py`. La matriz de aceptación de research.md §8 documenta casos
adicionales (calificación cualitativa, verbo intermedio) que el mecanismo todavía no
bloquea hasta que se complete la tarea de refuerzo de convergencia — no se presenta este
escenario como cobertura de esos casos.

## Escenario C — Fallo de agente (User Story 4, SC-006)

1. Ejecutar un turno con un agente de prueba configurado para superar `timeout_ms` (o
   devolver una salida que no cumple su `output_schema_ref`).
   - **Esperado**: `Turn.status = "degraded"` o `"failed"` según configuración de
     fallback; ningún cambio parcial queda aplicado a `CognitiveState` (verificar
     `state_version` sin cambios inconsistentes).
2. Consultar `GET /api/v1/sessions/{id}/trace`.
   - **Esperado**: un `TraceEvent` de tipo error/timeout, trazable.

## Escenario D — Conflicto de escritura (User Story 5)

1. Disparar dos `StatePatch` con el mismo `base_version` de forma simultánea (script de
   prueba de integración, no manual desde la UI).
   - **Esperado**: solo uno queda `applied = true`; el otro persiste con
     `rejected_reason` (`data-model.md` → StatePatch).
2. Consultar el historial de patches de esa sesión.
   - **Esperado**: ambos intentos son visibles, ninguno se perdió silenciosamente.

## Escenario E — Reinicio y reconstrucción (User Story 6, SC-004)

1. Cerrar la sesión del Escenario A. Detener el proceso `uvicorn`.
2. Reiniciarlo y, desde `/tecnica`, abrir la misma sesión (`GET /api/v1/sessions/{id}`).
   - **Esperado**: configuración, turnos, agentes ejecutados y decisiones se reconstruyen
     de forma idéntica al estado antes del reinicio.

## Validación de criterios de éxito adicionales

- **SC-001 / SC-002**: verificar en el seed que ≥5 `Agent` comparten `AgentContract` y ≥2
  `Agency` reutilizan agentes sin cambios en `orchestration/`.
- **SC-003**: inspeccionar que ningún `CognitiveState`/`StatePatch` se generó dentro de un
  prompt de LLM (no aplica en esta feature — sin LLM real, ver `research.md` §2 y §7).
- **SC-008**: en pruebas de contrato, sustituir un `Agent` registrado por otro que cumpla el
  mismo `AgentContract` y confirmar que ninguna `Agency` ni el orquestador requieren cambios.
- **FR-012a**: intentar iniciar una segunda sesión mientras la primera está activa y
  confirmar `409` (`contracts/api-participante.md`).

## Validación prevista de T090 (2026-10-13)

Esta sección describe aceptación futura; no afirma que las pruebas existan ni que T090 esté implementada. Referencia de diseño: `contracts/constitutional-output.md`. Preparación prevista: fixture con dos configuraciones versionadas y políticas explícitas diferentes, dos destinatarios seudónimos, catálogo interno versionado, referencias confiables de dato/alcance y una plantilla que permita reconstruir el texto exacto. Ejecutar las futuras pruebas de contrato e integración por la suite local (PowerShell: `$env:PYTHONPATH='src'; uv run pytest tests/ -q -m "not ollama and not speech"`); la matriz de abajo define sus casos, sin añadir tareas ahora.

| Condición FR-014/FR-015 | Responsable | Prueba positiva y negativa prevista |
|---|---|---|
| Política explícita, versionada y destinatario | Creación de actividad, orquestador y control | Misma categoría/procedencia aprobada para destinatario A y bloqueada para B; política ausente → `missing_policy`, mal formada o versión equivocada → `invalid_context`; configuración histórica nula nunca permite todo. |
| Categoría, procedencia y datos permitidos | Constructor de instantánea y control | Triple permitido aprobado; procedencia prohibida y categoría desconocida → `unauthorized_data`, aun con igual valor textual. |
| Temas, propósitos y acciones de la actividad | Constructor confiable y control | Cada referencia permitida aprobada; tema, propósito o acción ajenos → `out_of_scope`; conocimiento general `false` se bloquea y `true` no amplía alcance. |
| Vinculación completa con texto final | Constructor y control | Texto reconstruido íntegro aprobado; referencia inventada, intervalo fuera de límites/solapado, texto distinto, contenido sin cobertura y etiqueta falsificada por generador → `unverified_binding`/`invalid_context`, nunca aprobación. |
| Aplicación a toda salida, incluida alternativa | Orquestación principal y ambos compositores de autoestudio | Misma propuesta positiva/negativa en ruta normal, pregunta práctica, reconocimiento de falta de información, fallback técnico y de generación; sin bypass por `evaluate(str)`, `SAFE_BLOCKED_MESSAGE`, timeout o resultado de verificador ausente. |
| Bloqueo, causa y privacidad | Control, orquestadores, trazas y API | Una salida bloqueada no aparece en API, `Turn.output_text`, `CognitiveState` ni trazas; traza contiene código/versión/ID, nunca dato sensible ni texto bloqueado. |
| Único fallback operativo seguro | Catálogo, orquestador y control | Mensaje catalogado y permitido se muestra tras segunda verificación; entrada no permitida o verificación fallida → `unsafe_fallback`, exactamente un intento, `output_text=null`, cierre seguro sin contenido. |
| Conservación de H02 | Subfunción léxica H02 del control | Ejecutar íntegra la matriz preexistente `tests/contract/test_verification_block.py` y sus pruebas de integración/fallo, sin cambiar patrones ni aserciones. |
| Separación de Feature 002 | Grounding, admisión de materiales y control | Mantener iguales los veredictos existentes de grounding y aislamiento de materiales; un fragmento recuperado permitido por Feature 002 pero prohibido por política de salida se bloquea solo al presentar, sin alterar el verificador de materiales. |

La aceptación exige ambas direcciones de cada contraste (permitido y denegado), más casos de error/timeout y compatibilidad de API con `output_text: null`. Si el generador actual no aporta composición verificable, la prueba esperada es bloqueo y cierre en seguro; no se puede etiquetar el texto libre como autorizado por conveniencia.

### Ampliación de matriz T090 (2026-10-13)

| Caso discriminante adicional | Componente | Resultado esperado |
|---|---|---|
| Dos segmentos con hueco de un carácter, o con espacio/signo fuera de segmentos | Constructor/verificador | `invalid_proposal`; ninguno se omite por ser «no sustantivo». |
| Texto con `á`, emoji y carácter suplementario; índices medidos como `len(str)` Python, no UTF-8/UTF-16 | Constructor/verificador | Intervalos contiguos por punto de código se aprueban; desplazamientos en bytes/unidades o normalización Unicode tácita se bloquean. |
| Inicio de sesión con política explícita y plantilla normal `He recibido tu mensaje. Continuemos con la actividad.` | Actividad, orquestador, control, API | Segmento fijo `[0,len(text))`, `VerificationResult.approved`, `Turn.output_text` y API con texto visible; cierre voluntario completa SC-007 sin eco del participante. |
| Bloqueo inicial seguido de fallback catalogado aprobado | Orquestador, `VerificationResult`, `TraceEvent` | Intentos 0/1 trazados; fila final `approved`, `reasons=[]`, identidades/versiones/huellas finales persistidas, `Turn.status=degraded`, API muestra solo texto operativo con `blocked=true`. |
| Fallan propuesta y única alternativa | Control, persistencia, API/web | Fila final `block`, causas ordenadas con `unsafe_fallback`, `Turn.output_text=NULL`, API `output_text:null`, vista sin burbuja, acción de cierre, sin tercer intento. |
| Catálogo con dos versiones del mismo ID y contenido diferente | Catálogo, política, traza | Cada versión/huella resuelve su texto histórico; reutilizar una versión con contenido distinto o quitar una referenciada produce bloqueo `invalid_context`. |
| Mutar un dict JSON decodificado después del inicio o reasignar el campo persistido | Configuración y migración | Dict no modifica `TEXT` canónico; hash detecta corrupción; guardia/trigger rechaza reasignación en configuración inmutable. |
| Configuración histórica con ambas columnas de política `NULL` | Migración, control | `missing_policy`, intento operativo único rechazado, cierre sin texto; no hay allow-all. Nueva versión docente con política explícita sí puede completar SC-007. |
| Dos o más causas independientes y error temprano | Control y trazas | Códigos deduplicados en orden contractual; falta de política/contexto/estructura detiene inspección; nunca se lee un valor denegado para reunir razones extra. |

Para el recorrido positivo, el seed/fixture debe usar una política mínima real y una versión conservada de plantilla. Los tests históricos que exigen eco literal en la ruta principal requieren adaptar esa expectativa de salida cuando se implemente T090; la matriz H02 cerrada conserva intactas sus frases, reglas y aserciones. La migración prevista solo agrega columnas de política y metadatos finales, no modifica la nulabilidad de `Turn.output_text`.
