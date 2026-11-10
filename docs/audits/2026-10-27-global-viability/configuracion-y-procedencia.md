# Configuración efectiva y contradicciones relevantes

Esta auditoría contrasta código y recibos; no reproduce la inferencia. [Hashes leídos](source-inventory.json) permiten identificar las versiones observadas. Las rutas a modelos locales no se incluyen en consultas externas. No se infieren capacidades por tamaño, tarjeta o nombre.

## Configuración actual corroborada

En [worker pedagógico](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/worker.json) figuran torch2.13.0+cu130, Transformers5.5.3, RTX5090, clase Qwen2ForCausalLM/Qwen2Tokenizer, snapshot Qwen2.5-7B-Instruct `a09a35458c702b33eeacc393d103063234e8bc28`. Cuantización bitsandbytes4bitNF4, double_quant=true, cómputoBF16; `model_training=false`. Huella declarada del modelo5.443.300.864bytes; `weight_bytes=15.231.271.888` no equivale al pico de VRAM del proceso. Las versiones son las del recibo, no una inspección de hardware ni instalación actual del auditor.

Plantilla efectiva SHA256 `2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`. [Frames enviados](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/sent-frames.json) contienen mensajes de sistema y usuario con pasajes reales, pregunta, historial según condición,512tokens/30s y `finite_outputs=null`. [Prompts renderizados](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/rendered-prompts.json) conservan el resultado de la plantilla. En A1 el baseline y pedagogy difieren en instrucción; el resto de entradas es idéntico. A partir de A2 cambia historial real y puede cambiar recuperación, por lo que no es una ablación exclusivamente del prompt durante toda la conversación.

**Precedencia de parámetros:** `generation_state.model_generation_config` del ready muestra `do_sample=true`, temperatura0,7/top_k20/top_p0,8 y repetition_penalty1,05. No es el valor final de la llamada: [gpu_worker.py](../../../src/oralia/course_dialogue/gpu_worker.py) suministra `do_sample=False`, `max_new_tokens=frame[max_tokens]` y `pad_token_id=tokenizer.eos_token_id`, además del Deadline y, si corresponde, callback finito. La comparación fue voraz; temperatura/top_p por defecto no son prueba de muestreo activo. El estado por petición registra overrides cuando `audit_config` está activo. No atribuir diversidad o errores a la semilla sin evidencia de sampling.

El ready declara `structured_decoder=false`, `schema_hint_only=true`, soporte finito y máximo256objetos. No es contradicción: un JSONschema arbitrario no se restringe; un conjunto finito sí. [finite_schema.py](../../../src/oralia/course_dialogue/finite_schema.py) enumera salidas y [gpu_worker.py](../../../src/oralia/course_dialogue/gpu_worker.py) aplica `prefix_allowed_tokens_fn` al sufijo posterior al prompt. El control de120alternativas/tokenizer no cargó pesos. F01/C01cumplen sintaxis sin acertar intención. EOS/forma correcta no verifican semántica.

## Procedencia de los diagnósticos

| Evidencia | Qué puede reconstruirse | Qué no debe afirmarse |
|---|---|---|
| Ensayo finito F01 | [Auditoría request](../../../specs/012-conversational-course-study/evidence/scope-effective-request-audit-2026-10-26.md):pregunta/política/descripciones/hash correctos,4189tokens y13+EOS; frame reconstruido con transporte simulado. | No captura original del pipe ni prueba de causalidad del conflicto de mensajes. |
| Diagnóstico C01 | [Perfil conectado](../../../specs/012-conversational-course-study/evidence/scope-control-connected-2026-10-26.md), [ensayo](../../../specs/012-conversational-course-study/evidence/scope-control-diagnostic-report-2026-10-26.md):perfil confirmado,4163input/14output,128máximo. | No invalidar el error completo por presión GPU ni atribuirlo a otro proceso. |
| Mínimo27oct | Frames/prompts/worker y configuración por petición,5casos completos. | No extender esa captura a ensayos previos que no la tenían. |
| ST01 | Request/raw y reconstrucción2065tokens documentada,128output,stop. | No llamar frame original a reconstrucción. No aceptar retroactivamente por nuevo formato de referencias. |
| L01–03 y pedagogía | Captura frames/prompts/recibos; NF4/BF16/overrides. | No confundir preview técnico mostrado con autorización para participantes ni con verificador autónomo. |
| Mistral24B | Snapshot `9527884be6e5616bdd54de542f9ae13384489724`,10shards presentes; arreglo regex optativo en memoria,4turnos/768tokens/50s. | No comparación causal con7B/14Bni prueba de incompatibilidad general del modelo. |
| Juez14B |7controles/16respuestas y propósito corregido preservados. | No equiparar identidad distinta con errores independientes, ni16acceptcon16respuestas fieles. |

## Contradicciones de interpretación que deben evitarse

1. **«Todo verde» frente a tutor bloqueado:** las pruebas de software suministran `PostReview`/assessors o generadores simulados. [LaboratoryConversation](../../../src/oralia/course_dialogue/conversation_lab.py) dice expresamente que no implementa semántica. `verification.py` devuelve `independent_semantics=false`, publicaciónfalse; `claim_review.aggregate_review` agrega etiquetas recibidas. Las implementaciones coinciden con el bloqueo, no con una garantía docente.
2. **«Analyze sin críticos» frente a no aceptación:** coherencia spec/plan/tasks puede pasar porque las brechas están correctamente declaradas pendientes. `converge` no concluye012; las tareas sustantivas siguen abiertas. No modificar sus estados por este informe.
3. **«T071pendiente aunque hay generación»**: existe entrega aGenerationPorten laboratorio y pruebas/capturas reales; faltan autorización normal de participante y revisión semántica. No es cero implementación ni tarea completa por cableado.
4. **«Fuentes presentes» frente a «contenido fiel»**: A1 y ST01recibieron las páginas de referencia. Su error requiere diagnóstico de uso/interpretación, no solo recuperación. En otros turnos sí hay huecos de ranking; son problemas distintos.
5. **«No literal» frente a «incorrecto»**: escenarios y números inventados son permitidos bajo hipótesis coherentes. Las falsas contradicciones de globos/cierres y tiempos sin premisas son errores en inferencia o supuesto, no ausencia literal del escenario en PDF.
6. **«Memoria ocupada» frente a «GPU ajena activa»**: contextos residentes y huella de pesos no identifican el origen de un pico. El resumen temprano de recursos omitió muestra tardía512MiB; el anexo posterior lo corrige sin alterar el original. Tiempos resource-inconclusive no se usan como benchmark; errores de texto completos se conservan sin causalidad atribuida.
7. **«139páginas autorizadas» frente a «todos los temas cubiertos»**: alcance docente confirmado más amplio que los3PDF;26páginas en cuarentena y7excluidas no delimitan negativamente el curso. El informe inicial de17páginas era válido para su momento, no el catálogo actual.
8. **«Revalidación» frente a «restauración»**: tres Playwright nuevos en010acreditan comportamientos actuales, no recuperación de seis originales perdidos. Lo pendiente de revisión humana no se limpia por crear011/012.

La reserva no se lee para diseñar nuevos controles ni se consume. Los negativos ya publicados se citan como regresión expuesta. Esta auditoría no cambia prompts, ranking, contratos o interpretación congelada de ensayos antiguos.
