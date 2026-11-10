# Evidencia de validación de `quickstart.md` (T076)

Ejecutado contra una base de datos SQLite temporal, seed de demostración
(`oralia.scripts.seed_demo`), y la app FastAPI real (sin mocks del framework HTTP).
Escenario E se cubre mediante la prueba automatizada
`tests/integration/test_session_reconstruction_after_restart.py`, que sí simula un
reinicio real (motor SQLAlchemy y app completamente nuevos contra el mismo archivo).

```text
=== Seed (SC-001, SC-002) ===
agents: 5 agencies: 2

=== Escenario A - sesion valida ===
start: 201 Estás interactuando con ORAL-IA, un sist ...
turn: 200 respond
end: 200 closed_voluntary
technical_summary present: True

=== Escenario B - salida bloqueada ===
blocked: True output_text: No puedo mostrar esa respuesta porque incumple los límites de este sistema de IA. ¿Puedes reformular tu pregunta sobre la actividad?

=== Escenario C - fallo de agente ===
degraded turn status: 200 clarify

=== Escenario D - conflicto de escritura ===
p1.applied: True p2.applied: False p2.rejected_reason: conflict: base_version=0 does not match current version=1

=== Escenario E - ver tests/integration/test_session_reconstruction_after_restart.py ===
(cubierto por prueba automatizada, no por este script)

=== quickstart.md validation: ALL SCENARIOS EXECUTED OK ===
```

Además, la suite automatizada completa (66 pruebas: unit, contract, integration,
failure) pasa en el mismo commit — ver salida de
`PYTHONPATH=src uv run pytest tests/ -q`.

---

## Referencia global previa a la estabilización de H02 (001/T089, 2026-09-11)

**Esta es la referencia global previa** a la implementación de H02 (control
constitucional, Feature 001) y a cualquier corrección posterior de 002/003. Capturada
**antes de tocar ningún archivo** de esta ronda (código, pruebas o documentación).
`003/T105` MUST reutilizar esta evidencia como su propio "estado inicial reproducible"
cuando se implemente esa feature — no debe volver a ejecutar la suite como si fuera la
primera vez después de que 001 ya esté corregida.

**Entorno (corregido en la ronda 4, 2026-09-11 — dato anterior erróneo)**: `uv 0.11.30`.
El intérprete que **realmente** ejecuta `uv run pytest`/`uv run ruff` es el de
`.venv` — verificado directamente: `sys.executable` = `D:\Proyecto personal\ORALIA\
.venv\Scripts\python.exe`, `sys.version` = `3.12.11 (main, Aug 18 2025, 19:17:54) [MSC
v.1944 64 bit (AMD64)]`, coherente con `.venv/pyvenv.cfg` (`version_info =
3.12.11`) y con la cabecera de la propia sesión de pytest ("Python 3.12.11"). **La
entrada anterior de este documento decía "Python 3.14.4"** — un error: esa cifra
procedía de invocar `python3 --version` directamente en la terminal, que resuelve a un
Python del sistema ajeno al proyecto, no al que `uv run` usa realmente. **No se ha
recreado ni actualizado el entorno para hacer coincidir esta corrección** — el `.venv`
es el mismo de antes y después de esta ronda (mismo `pyvenv.cfg`), por lo que la
ejecución de referencia (239 passed, 49 errores de Ruff) también corrió, con alta
confianza, sobre este mismo intérprete 3.12.11 — pero como esa ejecución concreta no
capturó `sys.executable`/`sys.version` en el momento, **ese dato histórico puntual
queda marcado como no verificado directamente**, no como "3.14.4" ni reescrito a
"3.12.11" sin más — el recuento de pruebas/hallazgos de esa ejecución no depende de
esto y no cambia. Windows (`win32`), repositorio sin control de versiones (`git` no
disponible — no hay `.git`; la referencia de estado se basa en hashes SHA-256 de los
archivos afectados, no en un commit).

**Suite determinista (001+002+003, sin Ollama real)**:

```text
PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not speech"
239 passed, 1 deselected, 1 warning in 71.23s (0:01:11)
```

- **0 fallos funcionales.** La única advertencia (`StarletteDeprecationWarning`: "Using
  `httpx` con `starlette.testclient` is deprecated") es del entorno (versión de
  dependencias de terceros), no del código de este proyecto ni de ningún requisito —
  no se cuenta como incidencia funcional.
- El marcador `speech` (previsto para la Feature 004, no implementada todavía) no está
  registrado en `pyproject.toml` — `-m "not speech"` no excluye nada hoy porque no
  existe ningún test con ese marcador; se incluye en el comando por ser el que usará
  004 en el futuro, sin efecto actual.
- **239 es el resultado real de esta ejecución concreta, no una cifra objetivo** — el
  hecho de que coincida con la cifra documentada en
  `specs/003-self-study-agency/quickstart-validation-evidence.md` (2026-09-02) es
  observación, no una meta perseguida; si tras H02 el número cambia (por las pruebas
  nuevas de reproducción/matriz), ese cambio se documenta por separado, no se fuerza a
  volver a 239.

**Análisis estático (`ruff`, sin `--fix`)**:

```text
uv run ruff check src/ tests/
Found 49 errors.
```

Desglose por regla: `E501` (línea > 110 caracteres) × 45, `F401` (import sin usar) × 2,
`F841` (variable sin usar) × 1, `F541` (f-string sin marcador) × 1. **Los 49 son
hallazgos reales de esta ejecución, no la cifra de la auditoría externa previa
reutilizada sin comprobar** — coincide con ella, ahora confirmada por ejecución directa,
no asumida. Ninguno de los 49 está en
`src/oralia/domain/policies/constitutional_control.py` (verificado por separado:
`uv run ruff check src/oralia/domain/policies/constitutional_control.py` → "All checks
passed!") — el archivo que esta ronda modifica parte limpio de Ruff.

**Distinción fallos funcionales vs. problemas de entorno**: no hay fallos funcionales
que distinguir en esta ejecución (0 de 239 fallaron); el único ruido (el warning de
`starlette`/`httpx`) es de entorno, documentado como tal, no como una incidencia a
resolver en esta ronda.

**Distinción explícita (pedida en la ronda 4, 2026-09-11)**: "la suite no detectó
ningún fallo" (hecho observado: 239/239 pasaron) **no equivale a** "no existen
defectos funcionales" (una afirmación sobre el sistema, no sobre la suite). La segunda
no se deriva de la primera — una suite solo prueba lo que sus casos ejercitan; los tres
falsos positivos de H02 encontrados y corregidos en la ronda 4 (ver más abajo) son
prueba directa de ello: la suite de la ronda 3 pasaba 255/255 y aun así contenía un
defecto funcional real (tres frases legítimas bloqueadas indebidamente) que ningún caso
existente ejercitaba todavía. Este documento registra qué detectó cada ejecución
concreta, nunca "ausencia de defectos" como conclusión general.

---

## Seguimiento de H02 — 3 falsos positivos corregidos (001/T091, ronda 4, 2026-09-11)

Ejecutado inmediatamente después de la referencia global anterior, sobre el mismo
`.venv` (Python 3.12.11, verificado por `sys.executable`/`sys.version` — ver más
arriba).

```text
PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not speech"
Antes de esta tarea:  255 passed, 1 deselected
Después de esta tarea: 266 passed, 1 deselected (+11: 8 casos de matriz + 3 pruebas de
                        integración/fallback nuevas — 0 regresiones)

uv run ruff check src/ tests/
Antes: 49 errores → tras añadir las pruebas nuevas: 50 (1 línea larga propia, corregida)
→ 49 (estado final, igual que la referencia global)
```

Detalle completo de causas, corrección y matriz en `research.md` §8.1 y en
`tasks.md` → Phase 15 → T091.

---

## T092 — línea base Ruff previa a T090 (2026-10-14)

La captura se realizó **antes de crear o modificar pruebas o código de producción**. Ruff
terminó con código 1 por los hallazgos heredados esperados; `src/` y `tests/` se
compararon por contenido antes y después de la ejecución y no cambiaron.

- Versión: `ruff 0.15.22`.
- Comando exacto: `uv run --no-sync ruff check src/ tests/ --output-format json --no-cache`.
- Alcance: `src/` y `tests/`.
- Total: **49** hallazgos; `E501`: 45, `F401`: 2, `F541`: 1, `F841`: 1.
- Manifiesto durable: `specs/001-core-cognitive-runtime/t090-ruff-baseline.json`.
- SHA-256 de los bytes exactos del manifiesto: `3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

El manifiesto se releyó como JSON válido: las 49 entradas y la suma por código
coinciden; contiene rutas relativas normalizadas y orden estable. Se conserva hasta
T145 para comparar identidades `ruta + código + mensaje` con multiplicidad; línea y
columna son datos de ubicación, no identidad estable.

### T092 — reproducción contractual roja

Se añadió `tests/contract/test_t090_policy_authorization_red.py` usando exclusivamente
`ConstitutionalControl`, `AgentRequest`, `CancellationToken` y diccionarios locales de
propuesta, referencia de dato y política. El texto ordinario no activa H02; el defecto
aislado es que el control actual ignora `AgentRequest.context` y la referencia contextual.

```text
PYTHONPATH=src uv run --no-sync pytest tests/contract/test_t090_policy_authorization_red.py -q
6 failed, 1 passed, 1 warning in 0.26s

uv run --no-sync ruff check tests/contract/test_t090_policy_authorization_red.py --no-cache
All checks passed!
```

`allowed_triple` pasó con `approved` y sin causas. Los seis negativos
(`denied_category`, `denied_provenance`, `denied_recipient`, `unknown_category`,
`missing_policy`, `invalid_policy_version`) fallaron por aserción porque el control
devolvió `approved` en vez de `block`; no hubo errores de importación, colección,
fixture ni timeout. El warning único es el ya conocido de Starlette/httpx del entorno.

---

## T093 — reproducción contractual roja de vinculación estructural (2026-10-14)

Se añadió `tests/contract/test_t090_output_binding_red.py`. El archivo usa únicamente
`ConstitutionalControl`, `AgentRequest`, `CancellationToken`, biblioteca estándar y
diccionarios/helpers locales. Esos diccionarios representan identidad de
configuración/política, destinatario real, plantilla confiable versionada con SHA-256,
referencias confiables de datos y alcance, propuesta con texto final exacto y segmentos
`[start,end)` medidos como puntos de código de `str`. Cada segmento conserva texto
esperado, tipo fijo/ranura, `data_ref` opcional y referencias de tema, propósito y acción.
`input.proposal_text` contiene siempre el mismo texto final que la propuesta.

| Caso | Observado | Esperado |
|---|---|---|
| `exact_ascii_binding` | PASS (`approved`, causas `[]`) | PASS |
| `exact_unicode_codepoint_binding` | PASS (`approved`, causas `[]`) | PASS |
| `invented_data_reference` | FAIL: devolvió `approved` | `block` + `unverified_binding` |
| `forged_scope_label` | FAIL: devolvió `approved` | `block` + `unverified_binding` |
| `one_character_gap` | FAIL: devolvió `approved` | `block` + `invalid_proposal` |
| `overlapping_segments` | FAIL: devolvió `approved` | `block` + `invalid_proposal` |
| `uncovered_space` | FAIL: devolvió `approved` | `block` + `invalid_proposal` |
| `uncovered_punctuation` | FAIL: devolvió `approved` | `block` + `invalid_proposal` |
| `wrong_utf16_or_byte_offset` | FAIL: devolvió `approved` | `block` + `invalid_proposal` |
| `unicode_normalization_mismatch` | FAIL: devolvió `approved` | `block` + `unverified_binding` |

```text
PYTHONPATH=src uv run --no-sync pytest tests/contract/test_t090_output_binding_red.py -q
8 failed, 2 passed, 1 warning in 0.16s

uv run --no-sync ruff check tests/contract/test_t090_output_binding_red.py --no-cache
All checks passed!
```

Los ocho fallos finales son fallos de aserción conductuales previstos: el control actual
devuelve `approved` porque todavía ignora la propuesta y su vinculación estructural. No
hubo errores de importación, colección, fixture ni timeout. El único warning es el ya
conocido `StarletteDeprecationWarning` de Starlette/httpx. No se declara implementado
ningún verificador. La huella del manifiesto durable de T092 se volvió a calcular y sigue
siendo `3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva del arnés T093 (2026-10-14)

El primer arnés de `wrong_utf16_or_byte_offset` mezclaba varios defectos: calculaba una
posición en bytes UTF-8 y sustituía los segmentos completos por un único intervalo
interior, dejando también prefijo y sufijo sin cobertura. Por ello no aislaba la unidad
de índice equivocada.

El caso corregido conserva la misma propuesta, plantilla, política, referencias y
alcance, y usa tres segmentos válidos, contiguos y sin solapamiento que cubren exactamente
`[0,len(_UNICODE_TEXT))`: `[0,13)`, `[13,15)` y `[15,17)`. Los segmentos primero y
tercero declaran sus cortes Python exactos. El segmento central declara `"🙂"`, pero usa
su ancho UTF-16 de 2 unidades en vez de su ancho Python de 1 punto de código; el corte
real `_UNICODE_TEXT[13:15]` es `"🙂 "`. Asserts locales comprueban inicio 0, continuidad,
fin 17, rangos válidos, cobertura exacta una sola vez, discordancia del corte central y
diferencia entre ambos anchos. Así, la única discordancia es el ancho UTF-16 del emoji.

```text
PYTHONPATH=src uv run --no-sync pytest tests/contract/test_t090_output_binding_red.py -q
8 failed, 2 passed, 1 warning in 0.34s

uv run --no-sync ruff check tests/contract/test_t090_output_binding_red.py --no-cache
All checks passed!
```

`wrong_utf16_or_byte_offset` volvió a fallar por la aserción conductual prevista: el
control actual devolvió `approved` en lugar de `block`; no hubo errores de importación,
colección, fixture ni timeout. El SHA-256 del manifiesto T092 permanece intacto:
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T094 — reproducción contractual roja de puerta final (2026-10-14)

Se añadió `tests/contract/test_t090_final_gate_red.py` sin importar la puerta ni tipos
futuros. Usa `ConstitutionalControl.execute`, `run_turn`, estructuras locales, una SQLite
temporal creada por el propio archivo y dobles locales. El timeout se coordina mediante
`asyncio.Event` y el deadline contractual; no usa sleeps. El fallback contador demuestra
un único intento operativo.

| Caso | Resultado actual observado | Expectativa contractual congelada |
|---|---|---|
| Propuesta estructurada autorizada | PASS: `approved`, `reasons=[]` | `approved`, `[]` |
| Texto sin propuesta/contexto | FAIL: `approved` | `block`, `[missing_policy]` |
| Política ausente + propuesta mal formada | FAIL: `approved` | solo `[missing_policy]` |
| Contexto incongruente + propuesta mal formada | FAIL: `approved` | solo `[invalid_context]` |
| Segmentos inválidos + referencia inventada | FAIL: `approved` | solo `[invalid_proposal]` |
| Datos denegados + fuera de alcance + H02 | FAIL: solo `[assigns_grade]` | `[unauthorized_data, out_of_scope, assigns_grade]` |
| Verificador `ok` sin output | FAIL: aprobación implícita y turno `completed` | bloqueo y cierre seguro sin texto |
| Timeout determinista del verificador | FAIL: publica fallback y queda `degraded` | un intento y cierre seguro sin texto |
| Fallback único bloqueado | FAIL: devuelve `SAFE_BLOCKED_MESSAGE` como tercer texto | bloqueo y cierre seguro sin texto |

```text
PYTHONPATH=src uv run --no-sync pytest tests/contract/test_t090_final_gate_red.py -q
8 failed, 1 passed, 1 warning in 0.91s

uv run --no-sync ruff check tests/contract/test_t090_final_gate_red.py --no-cache
All checks passed!
```

Los ocho rojos son fallos de aserción conductuales previstos. No hubo errores de
importación, colección, fixtures, coordinación ni timeout del propio arnés. El único
warning es el `StarletteDeprecationWarning` ya conocido. El SHA-256 del manifiesto T092
permanece intacto:
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva del arnés T094 (2026-10-14)

Se corrigieron tres fisuras sin cambiar las expectativas contractuales. Primero,
`_proposal(text)` calculaba la huella de `_ORDINARY_TEXT` incluso al recibir otro texto;
ahora calcula `template_sha256` desde el mismo `text`, y el caso acumulado comprueba antes
de ejecutar el control que coincide con la plantilla confiable del snapshot. Segundo, la
referencia denegada incluía una huella de valor confiable; ahora contiene exclusivamente
categoría, procedencia, destinatario y alcance, con asserts que excluyen `value` y
`value_sha256`. La reclamación de hash permanece solo en el segmento no confiable de la
propuesta, de modo que `unauthorized_data` puede decidirse sin leer el valor denegado.

Tercero, el fixture asignaba un diccionario y `str(dict)` a los campos físicos previstos,
y usaba un participante distinto. Ahora persiste la política como JSON canónico
(`sort_keys=True`, separadores `(',', ':')`, `ensure_ascii=False`, `allow_nan=False`),
calcula SHA-256 sobre sus bytes UTF-8 exactos y usa `participant-a`. Asserts locales
verifican tipo `str`, round-trip JSON, huella y destinatario. La política declara
`allowed_recipients=['participant-a']`, `general_knowledge_allowed=false` y
`allowed_operational_messages=[]`; este último conjunto vacío es la causa intencional por
la que los fallbacks no pueden producir contenido visible.

```text
PYTHONPATH=src uv run --no-sync pytest tests/contract/test_t090_final_gate_red.py -q
8 failed, 1 passed, 1 warning in 0.53s

uv run --no-sync ruff check tests/contract/test_t090_final_gate_red.py --no-cache
All checks passed!
```

Los ocho fallos siguen correspondiendo a las mismas expectativas contractuales; ninguna
preparación local falló. El SHA-256 del manifiesto T092 continúa siendo
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T095 — reproducción roja de autorización en el turno principal (2026-10-14)

Se añadió `tests/integration/test_t090_main_turn_red.py`. Cada caso crea su propia base
SQLite temporal, actividad, participante, sesión y política, y libera siempre la sesión
SQLAlchemy y el engine mediante un context manager local. No usa fixtures compartidos ni
tipos futuros.

La política se guarda como JSON canónico con SHA-256 sobre sus bytes UTF-8 exactos. Permite
solo `participant-a`, la plantilla normal `sc007-acknowledgement` versión 1, tema
`actividad`, propósito `acuse_turno`, acción `continuar`, sin conocimiento general ni
mensajes operativos. Sus asserts locales verifican round-trip, recanonización, huella y
campos cerrados antes de llamar a `run_turn`.

| Caso | Resultado actual observado | Expectativa contractual congelada |
|---|---|---|
| Control positivo SC-007 | PASS: turno `completed`, texto visible y `VerificationResult.approved` sin causas | salida normal autorizada, sin congelar el eco histórico |
| Dato privado `T090_PRIVATE_SENTINEL_7F31` | FAIL: el marcador reaparece en `result.output_text` | acuse seguro sin reproducir la entrada privada |
| Destinatario real `participant-b` | FAIL: turno `completed`, `blocked=false` y texto visible | cierre `closed_error_safe` sin texto |
| Tema distinto de `actividad` | FAIL: turno `completed`, `blocked=false` y texto visible | cierre `closed_error_safe` sin texto |
| Propósito distinto de `acuse_turno` | FAIL: turno `completed`, `blocked=false` y texto visible | cierre `closed_error_safe` sin texto |
| Acción distinta de `continuar` | FAIL: turno `completed`, `blocked=false` y texto visible | cierre `closed_error_safe` sin texto |

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_main_turn_red.py -q
5 failed, 1 passed, 1 warning in 0.50s

uv run --no-sync ruff check tests/integration/test_t090_main_turn_red.py --no-cache
All checks passed!
```

Los cinco rojos son fallos de aserción conductuales previstos. No hubo errores de
importación, colección, fixture ni liberación de recursos. El warning único es el
`StarletteDeprecationWarning` ya conocido. El SHA-256 del manifiesto T092 permanece
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva del caso privado T095 (2026-10-14)

La primera versión solo exigía que el marcador privado desapareciera, por lo que un
bloqueo excesivo podía producir un falso verde. El caso ahora exige simultáneamente un
turno no bloqueado y `completed`, sesión todavía `active`, cero invocaciones al fallback,
`VerificationResult.approved` sin causas y el acuse SC-007 exacto tanto en el resultado
como en `Turn.output_text`, sin el marcador. Continúa rojo únicamente porque la ruta actual
devuelve el antiguo eco.

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_main_turn_red.py -q
5 failed, 1 passed, 1 warning in 0.54s

uv run --no-sync ruff check tests/integration/test_t090_main_turn_red.py --no-cache
All checks passed!
```

El SHA-256 del manifiesto T092 continúa siendo
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T097 — reproducciones rojas de persistencia y privacidad (2026-10-14)

Se añadió `tests/integration/test_t090_persistence_privacy_red.py` usando únicamente
`run_turn`, modelos existentes, SQLite temporal y dobles locales restaurados por
`monkeypatch`. Cada caso crea una política completa como JSON canónico, comprueba tipo,
round-trip, recanonización, SHA-256 y destinatario real, y libera siempre sesión y
engine. Los campos futuros se leen solo mediante `getattr(..., None)`.

| Caso | Tablas/campos inspeccionados | Resultado actual y punto de fallo |
|---|---|---|
| Salida legítima y traza no sensible | `Turn`, `GeneratedProposal.content`, `VerificationResult`, `TraceEvent.payload` y sus relaciones | PASS: turno completado, texto aprobado conservado, veredicto `approved`, eventos esperados y ninguna política completa, razonamiento privado ni clave de valor sensible en trazas |
| Candidato rechazado | `GeneratedProposal.content`, todos los `InternalMessage.content` del control, todos los `TraceEvent.payload` y `VerificationResult.authorization_context` | FAIL: `T090_REJECTED_SECRET_31C8` aparece en el `InternalMessage` dirigido a `constitutional-control`, dentro de `content.input.proposal_text` |
| Bloqueo visible | `Turn.output_text`, resultado, acción y estado de sesión | FAIL: `result.output_text` contiene directamente `SAFE_BLOCKED_MESSAGE`; se exige cierre sin texto |
| Metadatos insuficientes | `GeneratedProposal.content`, `VerificationResult.verdict/authorization_context` y eventos constitucionales | FAIL: `authorization_context` es inexistente (`None`); además la propuesta rechazada queda representada mediante texto ambiguo y los eventos carecen del contrato completo de intento/veredicto/causas |
| Alternativa tras fallo upstream | contadores del intérprete/fallback, `InternalMessage` al fallback, `GeneratedProposal`, `VerificationResult` y `TraceEvent` | FAIL: hubo un fallo upstream y exactamente una alternativa, pero no existe un evento constitucional con `attempt=1`; la ruta histórica carece de puerta y metadatos estructurados |

El marcador rechazado se origina exclusivamente en el doble intérprete; la entrada del
participante es ordinaria. El caso de alternativa comienza directamente por fallo
upstream y no construye la secuencia rechazo inicial → fallback aprobado reservada para
T125. Ningún rojo exige como salida futura un texto defectuoso actual.

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_persistence_privacy_red.py -q
4 failed, 1 passed, 1 warning in 0.50s

uv run --no-sync ruff check tests/integration/test_t090_persistence_privacy_red.py --no-cache
All checks passed!
```

No hubo errores de importación, colección, fixture ni liberación. El único warning es el
`StarletteDeprecationWarning` conocido. El SHA-256 del manifiesto T092 permanece
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T096 — reproducciones rojas de rutas de autoestudio (2026-10-14)

Se añadió `tests/integration/test_t090_self_study_fallback_red.py` con SQLite temporal,
política JSON canónica y dobles locales instalados mediante `monkeypatch`. La política
comprueba tipo `str`, round-trip, recanonización, SHA-256, destinatario real coherente,
conocimiento general desactivado y conjunto vacío de mensajes operativos. Cada contexto
libera la sesión SQLAlchemy y el engine; el doble de timeout espera `asyncio.Event`, se
libera en `finally` y no usa `sleep`.

| Caso | Demostración previa de la rama | Resultado actual y expectativa congelada |
|---|---|---|
| Control positivo | Generador, grounding y control constitucional se ejecutan una vez; verificación persistida `approved`; sesión `active` | PASS: `completed`, no bloqueado, salida no vacía e idéntica en resultado y `Turn` |
| Error upstream | Generador devuelve `error`; grounding no se ejecuta; fallback se consume exactamente una vez | FAIL: publica `SAFE_FALLBACK_TEXT`, queda `degraded` y no bloqueado; se espera cierre seguro sin texto |
| Timeout upstream | El evento confirma inicio, la traza registra `generate/timeout`, el `finally` confirma liberación y hay exactamente un fallback | FAIL: publica `SAFE_FALLBACK_TEXT`, queda `degraded` y no bloqueado; se espera cierre seguro sin texto |
| Fallback generativo de pregunta | Dos intentos configurados y dos bloqueos de no divulgación; `PracticeQuestion.non_disclosure_attempts=2`; adaptador determinista llamado una vez y traza `fallback_used=true` | FAIL: publica la pregunta determinista; se espera cierre seguro sin texto |
| Pregunta práctica normal | Un intento aprobado de no divulgación; adaptador de fallback no llamado; traza `fallback_used=false` | FAIL: publica la pregunta normal; se espera cierre seguro sin texto |
| Falta de evidencia | Recuperación vacía, generador con cero llamadas, paso `generate` ausente y control textual recibe `_ACKNOWLEDGE_MISSING_INFO_TEXT` | FAIL: publica el mensaje Nivel 0; se espera cierre seguro sin texto |
| Transformación posterior | Evidencia suficiente; el espía constitucional recibe y aprueba solo el texto ordinario inicial; grounding sustituye después por `Tu nota es 9.` | FAIL: el texto H02 transformado aparece en resultado y `Turn`; se espera reverificación y cierre seguro sin texto |

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_self_study_fallback_red.py -q
6 failed, 1 passed, 1 warning in 1.95s

uv run --no-sync ruff check tests/integration/test_t090_self_study_fallback_red.py --no-cache
All checks passed!
```

Los seis rojos son fallos de aserción conductuales previstos posteriores a la
demostración de su rama. No hubo errores de importación, colección, fixture,
coordinación ni liberación. El único warning es el `StarletteDeprecationWarning` ya
conocido. El SHA-256 del manifiesto T092 permanece intacto:
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva de las aserciones congeladas de T096 (2026-10-14)

La primera versión demostraba cada bypass y después exigía también que el contenido
histórico inseguro apareciera en `result.output_text`; esas aserciones contradecían el
estado final que la misma prueba reclamaba. Se retiraron todas las expectativas visibles
de `SAFE_FALLBACK_TEXT`, pregunta normal, pregunta determinista, mensaje Nivel 0 y texto
H02 transformado. Los contadores, eventos, filas `PracticeQuestion`, pasos seleccionados
y trazas continúan demostrando cada rama por separado antes de aplicar exclusivamente la
expectativa visible final de cierre seguro.

El caso de transformación ya no congela una sola llamada constitucional. Comprueba que
la evidencia suficiente llegó al generador, que el control recibió el texto inicial y
que alguna solicitud posterior recibe exactamente `Tu nota es 9.`; el código actual
falla en esta segunda verificación ausente. Los otros cinco rojos alcanzan
`_assert_safe_close` y fallan en `blocked is True` con la implementación actual.

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_self_study_fallback_red.py -q
6 failed, 1 passed, 1 warning in 1.22s

uv run --no-sync ruff check tests/integration/test_t090_self_study_fallback_red.py --no-cache
All checks passed!
```

No hubo errores de importación, colección, fixture, coordinación ni liberación. El
SHA-256 del manifiesto T092 continúa siendo
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva del arnés T097 (2026-10-14)

El control positivo ahora comprueba `GeneratedProposal.content.get("text")` y permite
metadatos seguros adicionales sin exigir que el diccionario contenga una única clave;
las relaciones entre `Turn`, `GeneratedProposal` y `VerificationResult` permanecen
congeladas.

Cada caso H02 configura `activity.normal_output_template` con el candidato final exacto
que compone la ruta observable `respond`, incluida su huella SHA-256 calculada desde ese
mismo texto. Asserts previos a `run_turn` comprueban igualdad candidato/plantilla, huella
y presencia de `Tu nota es 9.`; el caso de privacidad comprueba además el marcador
`T090_REJECTED_SECRET_31C8`. Así una implementación futura puede alcanzar H02 con
identidad y huella coherentes, sin quedar desviada antes por contexto o vinculación.

El escaneo del candidato rechazado cubre ahora todos los `InternalMessage` del turno con
`type="agent_invocation"`, manteniendo aparte la prueba de que existe transporte hacia
`constitutional-control`. El marcador actual aparece en el transporte del intérprete y
en el del control; no procede de `Turn.input_text`.

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_persistence_privacy_red.py -q
4 failed, 1 passed, 1 warning in 0.56s

uv run --no-sync ruff check tests/integration/test_t090_persistence_privacy_red.py --no-cache
All checks passed!
```

Los cuatro puntos rojos siguen siendo: marcador en transporte, publicación directa de
`SAFE_BLOCKED_MESSAGE`, `authorization_context` ausente y evento constitucional de
`attempt=1` ausente. El SHA-256 del manifiesto T092 permanece
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T098 — ciclo positivo y tres resultados finales T090 (2026-10-14)

Se añadió `tests/integration/test_t090_positive_cycle_red.py` con SQLite aislada por
caso, política JSON canónica y plantillas locales versionadas. La plantilla normal es
`sc007-acknowledgement` v1 con el texto SC-007; la operativa es
`safe-technical-fallback` v1 con el texto técnico actual. Ambas incluyen SHA-256 del
UTF-8 exacto y referencias de tema, propósito y acción. La política comprueba tipo,
round-trip, recanonización, huella, destinatario y el permiso operativo exacto: el par
operativo en el recorrido aprobado y lista vacía en el bloqueado.

| Caso | Evidencia de recorrido | Resultado actual y punto rojo |
|---|---|---|
| Ciclo histórico | `start_session` deja sesión `active` con bloqueo; `run_turn` completa y relaciona `Turn`/`GeneratedProposal`/`VerificationResult`; `end_session_voluntarily` persiste `closed_voluntary`, `ended_at`, resumen, libera bloqueo y emite un `session_closed` | PASS |
| Normal SC-007 sin eco | sesión activa, veredicto final `approved`, cero mensajes al fallback y contexto 0/normal si existe | FAIL: `result.output_text` contiene el eco de `T090_NO_ECHO_SENTINEL_5A72` en vez de SC-007 |
| Fallback operativo aprobado | intérprete falla una vez, fallback se solicita una vez, existe un único transporte constitucional de reserva y una única traza `verify-fallback`; no hubo propuesta constitucional inicial | FAIL: texto operativo y estado `degraded` están presentes, pero `result.blocked` es `false`; se exige `true` y contexto estructurado del intento 1 |
| Fallback operativo no autorizado | mismo fallo, mismo texto, mismo único fallback e inicio directo operativo; la única diferencia es `allowed_operational_messages=[]` | FAIL: `result.blocked` es `false`; la ruta publica el fallback histórico y mantiene la sesión activa en vez de cerrar sin texto |

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_positive_cycle_red.py -q
3 failed, 1 passed, 1 warning in 0.83s

uv run --no-sync ruff check tests/integration/test_t090_positive_cycle_red.py --no-cache
All checks passed!
```

No hubo errores de importación, colección, fixtures ni liberación. Cada contexto cierra
la sesión SQLAlchemy y dispone el engine en `finally`; `monkeypatch` restaura los dobles.
El único warning es el `StarletteDeprecationWarning` conocido. El SHA-256 del manifiesto
T092 permanece `3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

### Nota correctiva del arnés T098 (2026-10-14)

La evidencia previa de los recorridos operativos ya no depende del número de mensajes al
control, del texto de `InternalMessage.objective` ni de los nombres históricos
`verify-fallback`/`fallback` en `TraceEvent.payload.step_id`. El helper comprueba solo
invariantes estables: una ejecución upstream cuyo resultado controlado es `error` sin
propuesta válida, una única llamada al fallback y como máximo un mensaje observable de
transporte hacia ese fallback. No fija contenido bruto ni una segunda representación
interna del intento.

La identidad constitucional del intento operativo permanece definida por el único
`VerificationResult` final y por `authorization_context.attempt=1`,
`message_type=operational` e identidades/versiones/huellas de política y plantilla; el
caso no autorizado conserva además la causa final `unsafe_fallback`.

```text
PYTHONPATH=src uv run --no-sync pytest tests/integration/test_t090_positive_cycle_red.py -q
3 failed, 1 passed, 1 warning in 0.47s

uv run --no-sync ruff check tests/integration/test_t090_positive_cycle_red.py --no-cache
All checks passed!
```

Los puntos rojos siguen siendo el eco normal, `blocked=false` en el fallback aprobado y
`blocked=false` en el fallback no autorizado. El SHA-256 del manifiesto T092 permanece
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

---

## T144–T147 — validación final de T090 (2026-10-16)

Esta sección añade la evidencia final sin sustituir las reproducciones rojas históricas
anteriores. Esas reproducciones describen el estado en que fueron creadas; la ejecución
actual confirma que los contratos T090 ya están verdes. La carrera del índice de
materiales de Feature 002 permanece deliberadamente pendiente y se distingue de las
regresiones de T090.

### T144 — suite exacta y reproducciones externas

Se ejecutó literalmente la suite con los únicos dos `--deselect` previstos:

```powershell
$env:PYTHONPATH='src'
uv run --no-sync pytest tests/ -q -m "not ollama and not speech" `
  --deselect tests/integration/test_material_index_rebuild_race_reproduction.py::test_A_reader_paused_mid_resolution_survives_one_concurrent_rebuild `
  --deselect tests/integration/test_material_index_rebuild_race_reproduction.py::test_B_reader_paused_survives_two_concurrent_rebuilds_needs_retry
```

Resultado real: **581 passed, 3 deselected, 1 warning in 46.30s**. No hubo fallos
inesperados. El warning único es el `StarletteDeprecationWarning` heredado de
`fastapi.testclient`/`httpx`.

Los tres node IDs se ejecutaron además, cada uno en un proceso pytest independiente:

| Caso | Resultado | Evidencia del resultado |
|---|---:|---|
| Reproducción A | **1 failed**, 1 warning, 1.00s | Fallo de aserción previsto en la línea 167: el lector obtiene `[]` tras recrearse N vacío; coordinación, fixture e hilo completaron sin timeout ni excepción. |
| Reproducción B | **1 failed**, 1 warning, 0.82s | Fallo de aserción previsto en la línea 251: obtiene `set()` en vez de `{"frag-v3"}`; no hubo timeout, error de fixture/importación ni excepción descontrolada. |
| Experimento empírico de Chroma | **1 passed**, 1 warning, 0.83s | Confirma el comportamiento empírico de un objeto colección borrado. |

A y B son evidencia roja deliberada de la carrera T087/T092 de **Feature 002**. No se
contabilizan como regresiones de T090 y esta ronda no las corrige.

### T145 — comparación Ruff por identidad estable

- Ruff: `ruff 0.15.22`.
- Comando JSON exacto: `uv run --no-sync ruff check src/ tests/ --output-format json --no-cache`.
- Comando de recuento: `uv run --no-sync ruff check src/ tests/ --statistics --no-cache`.
- Alcance: `src/` y `tests/`.
- SHA-256 del manifiesto durable: `3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.
- El código de salida fue 1 por hallazgos heredados, no por un error de ejecución.

Resultado actual: **17** hallazgos (`E501`: 16, `F541`: 1). La comparación usa
`(ruta normalizada, código, mensaje)` con multiplicidad; línea y columna solo clasifican
la ubicación:

| Clasificación | Total | Por código |
|---|---:|---|
| Heredados en la misma ubicación | 12 | E501: 11; F541: 1 |
| Heredados desplazados | 5 | E501: 5 |
| Heredados eliminados | 32 | E501: 29; F401: 2; F841: 1 |
| Realmente nuevos | **0** | — |

Los cinco desplazados conservan identidad y multiplicidad en
`tests/integration/test_sc001_traceability.py`: líneas antiguas/nuevas
`61→68`, `77→84`, `110→117`, `128→135` y `129→136`. No se compensaron altas con
bajas. Al no existir ningún hallazgo nuevo global, hay también **cero nuevos en los
archivos creados o modificados por T090**.

### T146 — evidencia consolidada de contratos e integración

La comprobación focal consolidada ejecutó política/catálogo, verificador, migración,
contratos congelados, persistencia y privacidad, H02, grounding Feature 002, rutas de
Feature 003, SC-007 y la corrección concurrente T150:

```text
263 passed, 1 warning in 13.30s
```

La suite focal incluye los modelos y serialización canónica T099–T103, equivalencia de
migración/`create_all` T104–T111, frontera estricta y precedencia T112–T121, puerta y
persistencia privada T122–T125, integraciones y API T126–T137, matrices T138–T142,
ciclo/cierre T143 y la carrera del resumen de autoestudio T150. La matriz H02 permanece
intacta; grounding/admisión de Feature 002 conserva sus veredictos; Feature 003 no
publica candidatos no vinculados. Las pruebas de privacidad comprueban propuesta
rechazada saneada, transporte y trazas sin texto/valores prohibidos, y reconstrucción
solo con metadatos seguros.

T148 cerró la validación estricta de identidad de sesión/configuración/destinatario,
contratos Pydantic cerrados y referencias denegadas metadata-only. T149 cerró política
ausente/inválida, autoridad real de fragmentos y una sola decisión constitucional por
intento. T150 expone el ganador real del `UPDATE active -> terminal`: con dos
`SASession` obsoletas, solo el ganador genera el resumen autorizado; hay exactamente un
resumen técnico, un `session_closed`, una liberación y como máximo un resumen de
autoestudio. La prueba de rollback restaura estado activo, bloqueo, resúmenes y eventos.

No existen llamadas `.commit()` en `end_session.py`, `end_study_session.py`,
`submit_turn.py` ni `submit_study_turn.py`; el commit continúa en el límite exterior.

### T147 — auditoría de cierre

La auditoría progresiva comprobó T092–T146 y las convergencias T148–T150 contra los
archivos y pruebas nombrados en cada tarea. Todas las hijas están satisfechas, la suite
T090 no presenta fallos inesperados, no quedan permisos implícitos ni persistencia de
texto rechazado detectados por las matrices, y `.specify/feature.json` sigue apuntando a
`specs/001-core-cognitive-runtime`. La única limitación externa conocida son las dos
reproducciones rojas de Feature 002 descritas en T144. Tras esta auditoría se marcaron
T147 y el hallazgo padre T090; su cierre se apoya en la suite exacta T144, la comparación
Ruff T145, la evidencia consolidada T146 y la comprobación focal final de contratos
(**65 passed, 1 warning in 1.03s**).
