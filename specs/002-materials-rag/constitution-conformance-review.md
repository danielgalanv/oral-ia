# Revisión de conformidad constitucional (T077)

Revisión de la **implementación real** de la Feature 002 frente a cada principio de
`.specify/memory/constitution.md`. `plan.md` ya contiene una Constitution Check previa al
diseño; este documento la revalida después de escribir el código.

| Principio | Evidencia en el código | Estado |
|---|---|---|
| I. Finalidad y límites institucionales | Extracción/embeddings/índice 100% locales; `sentence_transformer_adapter.py` fuerza `HF_HUB_OFFLINE=1`/`TRANSFORMERS_OFFLINE=1` tras la descarga única del modelo, garantizando cero llamadas de red en indexación/recuperación. | PASS |
| II. Arquitectura modular basada en contratos | `MaterialRetrieverAgent`/`GroundingVerifierAgent` implementan el mismo `Executable`/`AgentContractSchema` de la Feature 001 sin modificarlo; `VectorStore`/`EmbeddingAdapter`/`DocumentExtractor` son interfaces (`Protocol`) sustituibles con un único adaptador concreto cada una. | PASS |
| III. Estado cognitivo explícito y memoria diferenciada | No se toca `CognitiveState`/`StatePatch`; los nuevos `TraceEvent` de esta feature (bloqueo por alcance, conflicto detectado) usan `memory_category="metacognitive"` explícitamente, evitando el defecto `"episodic"` que la Feature 001 tuvo que corregir en convergencia. | PASS |
| IV. Separación recuperación/generación/decisión/verificación | Esta feature implementa el rol "retriever" real; `GroundingVerifierAgent` es un verificador independiente que nunca decide la acción conversacional final (responsabilidad de la Feature 003). | PASS |
| V. Fundamentación en materiales autorizados | Núcleo de esta feature: procedencia completa por fragmento (`document_id`/`document_version`/`location_ref`), veredictos de fundamentación de 5 valores, conocimiento general etiquetado distinto de contenido fundamentado. | PASS |
| VI. Supervisión humana y gobernanza | Toda acción de estado (activar/desactivar/versionar/resolver duplicado/revisar conflicto) requiere una llamada API explícita del profesor; ninguna se dispara automáticamente. | PASS |
| VII. Privacidad, minimización y accesibilidad | Endpoints de `materials.py` heredan `127.0.0.1` por construcción (mismo `app.py`); sección "Materiales" de `Tecnica.tsx` sigue el mismo patrón de accesibilidad (etiquetas, teclado, `role="alert"`/`role="status"`, indicación de error no solo por color) ya usado en la Feature 001 — sin auditoría automatizada, misma limitación de Node.js documentada. | PASS (con limitación documentada) |
| VIII. Trazabilidad y reproducibilidad | Procedencia completa por fragmento (FR-029); recuperación reproducible por `index_version` (`test_material_retrieval_repeatable.py`); `MaterialConflictRecord` persistente y deduplicado entre consultas (FR-022b). | PASS |
| IX. Degradación controlada y límites de recursos | `time_budget_ms` agotado devuelve resultado parcial con `status="ok"` y advertencia explícita, nunca un fallo silencioso; un fallo de extracción/indexación no afecta al índice ya existente (verificado en `test_material_indexing_failure.py`); reconstrucción de índice protegida por bloqueo de un solo escritor (`index_rebuild_lock_service.py`). | PASS |
| X. Calidad, pruebas y evidencia | 67 pruebas nuevas (contract/integration/failure/unit) cubren las 7 historias de usuario más los 5 hallazgos cerrados por `/speckit-analyze`; evidencia de `quickstart.md` registrada en `quickstart-validation-evidence.md`; suite completa (139 pruebas, 72 de la Feature 001 + 67 de la Feature 002) verificada sin regresiones (T083). | PASS |
| XI. Simplicidad evolutiva | Segmentador propio (~80 líneas) en vez de un framework de chunking; heurística determinista de conflicto (solapamiento léxico + marcadores de negación) en vez de un modelo NLI; bloqueo de reconstrucción reutiliza literalmente el patrón ya validado de `session_lock_service.py` en vez de inventar uno nuevo. | PASS |

## Hallazgos corregidos durante la implementación (no violaciones finales)

1. **`MaterialFragment.indexing_status` no se actualizaba a `"retired"` al sustituir una
   versión** — la documentación (`data-model.md`) ya especificaba esta regla, pero
   `replace_material_version.py` solo fijaba `retired_at` en el documento, dejando los
   fragmentos de la versión anterior con `indexing_status="indexed"`. Esto habría violado
   FR-019 (aislamiento por versión): un fragmento retirado seguía siendo recuperable
   porque `MaterialDocument.status` no cambiaba de `"active"`. Corregido cascando la
   actualización a los fragmentos de la versión retirada; se añadió además una
   verificación defensiva de `document.retired_at` en el propio filtro del agente
   recuperador — ver `tests/integration/test_material_version_replacement.py`.
2. **`TraceEvent.session_id` tiene una FK obligatoria a `session.id`** — el diseño inicial
   del registro de intentos bloqueados (FR-026) usaba un `session_id` sinténtico
   (`"unknown"`) para consultas técnicas directas sin sesión real, lo que habría violado
   la restricción de integridad referencial de SQLite en cuanto se ejecutara con
   `PRAGMA foreign_keys=ON` (heredado de la Feature 001). Corregido: el registro de
   trazabilidad de intentos bloqueados solo se persiste cuando la consulta indica un
   `session_id` real (una sesión participante genuina, como las que compondrá la
   Feature 003); las consultas técnicas directas sin sesión quedan sin trazar por
   diseño, ya que no representan un intento real de un participante.

## Resultado

Sin violaciones abiertas. Misma limitación heredada de la Feature 001 (auditoría de
accesibilidad automatizada pendiente por falta de Node.js en este entorno) — no bloquea
el Principio VII porque los requisitos funcionales sí están implementados y siguen el
patrón ya usado, solo no verificados con herramienta automatizada.
