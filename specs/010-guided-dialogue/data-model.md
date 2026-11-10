# Data model — 010 (migración aditiva probada en bases temporales; demo personal sin migrar)

## DialogueContext v1

Campo JSON opcional en CognitiveState y snapshot. Default vacío con schema_version=1;
sesiones previas sin campo se leen en modo legacy y se inicializan solo en turno activo
compatible. No reconstruir un objetivo histórico a partir de tokens sin evidencia.

| Campo | Tipo/límite | Regla |
|---|---|---|
| current_topic_ref | str o null | tema permitido por actividad/unidad, no token libre |
| content_query | str <=500 | consulta temática vigente; jamás sustituida por «repítelo» |
| pending_question_turn_id | UUID o null | de esta sesión y salida autorizada |
| pending_question_unit_id | UUID o null | pregunta publicada vinculada al turno original |
| claim_followup | optional ClaimFollowup | owned participant turn, reviewed original/follow-up question, same subgoal and current source IDs; assessment always not_assessed; no copied text |
| last_approved_unit_ids | hasta3 UUID | composición publicada; revalidar en cada uso |
| pending_topic_ref | str <=100 o null | tema propuesto, aún sin sustituir el objetivo |
| last_approved_turn_id | UUID o null | volver a revalidar al usar |
| candidate_referents | hasta4 referencias tipadas | turno/unidad/tema, scope sesión |
| selected_referent | referencia o null | solo si inequívoco o elegido explícitamente |
| intent_hypotheses | hasta3 | label/confidence_kind/reason_code; sin pensamiento libre |
| current_subgoal_ref | str o null | perteneciente a unidad docente publicada |
| relevant_concepts | hasta8 referencias | derivadas de tema/evidencia; no tokens libres de órdenes |
| support_step | entero0..3 | paso de ayuda, no nivel del participante |
| stalled_signature | hash o null | acción+tema+evidencia+salida aprobada |
| stalled_count | entero0..2 | cap2 dispara opciones; no valor de capacidad |
| last_notice | str <=40 o null | alternar estrategia, nunca autoridad para publicar |
| offered_actions | hasta4 enums | opciones implementadas, válidas para actividad |
| effective_profile | enum | extractive_limited/guided_controlled/generative_local_candidate/degraded |
| evidence_refs | hasta5 | documento/versión/fragmento; sin cache de texto indefinida |

Cambios mediante StatePatch base_version; campo tipado en su payload y verificación
de rutas/referencias. Ningún patch de un turno cancelado o cerrado se aplica.
Releer el estado tras conflicto y decidir una sola vez; no replay ciego de acciones.

## TeachingUnit y paquete publicado

Identidad estable, family/version, course/activity_refs, estado draft/published/retired,
kind (fact/explanation/example/comparison/question/hint), topic/subgoal, source_refs,
reviewed_content, relations, reveal_policy y approver técnico local sin identidad extra.
El renderer recibe referencia, no un texto que el candidato haga pasar por revisado.
Publicación inmutable; edición genera sucesora. Modelo físico: tabla aditiva
teaching_units con unicidad family/version y relaciones al material existente;
la publicación usa la gobernanza y autorización existentes. La migración t010 añade
esta tabla sin alterar el DDL histórico. No usar JSON sin validación como bypass.

## DialogueAct v2 / ProposalPlan

Acto estructurado y argumentos, clasificación incierta, referente y reason_code;
ProposalPlan lleva plantilla versionada, bindings y transformaciones cerradas. El
contenido libre recibido se mantiene como input; no equivale al contenido autorizado.
No se almacena CandidateText rechazado.

## TurnRequestReceipt

Tabla aditiva turn_request_receipts en t010. client_request_id + session_id únicos; payload_sha256; turn_id resultante, estado
pending/completed/reconciled. Expiración y borrado siguen la sesión; no conserva
payload completo ni respuestas eliminadas. Duplicado idéntico no consume otro turno.
Respuesta reconciliada se proyecta de nuevo según permisos/estado actuales.

## Retención y reconstrucción

Contexto/recibos con referencia a texto requieren scope transcript; no exportarlos
por defecto. Summary-only elimina el contexto textual, conserva solo resumen autorizado
y metadatos mínimos. Borrado y caducidad limpian referencias, caches, propuestas y nuevos
campos en todos los modos. No retener anclas como incidentes perpetuos. Las migraciones
requieren clean+upgrade desde head actual, prueba rollback, compatibilidad de snapshots
anteriores y preservación de trazas ya autorizadas sin reescribirlas.


## Ampliación conversacional optativa, 2026-10-20

La política `guided-screenless/v1` mantiene `guided_controlled` y habilita contexto JSON schema 2: página de navegación acotada, conservación pendiente enumerada y confirmación de cierre pendiente. Schema 1 omite esos tres campos al serializar y mantiene su forma previa. No cambia el esquema SQL ni se reescriben actividades usadas. Antes de volver a una versión de código que solo lea schema 1, finalizar/purgar las sesiones v2 según sus permisos y desactivar las nuevas actividades; no entregar contexto v2 a lectores antiguos.

La navegación usa configuración actual autorizada; la revisión histórica usa registros propios conservados y caducables. Son categorías distintas de evidencia. No son afirmaciones académicas ni aprobación de utilidad. Tras cerrar no se crea contexto, turno o recibo nuevo para navegar por el registro.

## Sucesión didáctica v2

Las unidades mantienen kind y subgoal_ref existentes. La explicación base puede enlazar variantes publicadas mediante didactic_definition, didactic_cause, didactic_process, didactic_possibility y didactic_conditions (máximo cinco UUID por relación, curso validado). Rephrases enlaza otra estrategia del mismo propósito. El selector requiere que variante y alternativa pertenezcan al mismo tema y sean explanation; referencias retiradas no se sustituyen por ejemplos. El renderer vuelve a autorizar cada referencia/fuente con la política vigente. No hay DDL ni relajación de cobertura de objetivos: se conservan explicación/ejemplo/contraste/pregunta/pista por subobjetivo. Política guided-screenless/v2 optativa con plantillas aditivas didactic-greeting y didactic-overview; v1 no cambia. Materiales agua-v2/programa-v2 son propuestas docentes sintéticas publicadas explícitamente en fixtures; requieren revisión humana de suficiencia, no se presentan como contenido revisado por una persona.
