# Implementation Plan 012 — estado vigente

Fecha 2026-10-25. Feature en curso, sin publicación ni commits. [Especificación](spec.md) · [tareas pendientes](tasks.md) · [hoja de ruta breve](evidence/verified-conversation-roadmap.md) · [plan detallado](evidence/grounded-tutor-action-plan.md).

## Summary

Mantener el tutor generativo RAG en laboratorio: recuperar evidencia docente vigente desde pregunta e historial mostrado, evaluar suficiencia y conflictos, ampliar búsqueda local de forma acotada si falta información, entregar pasajes trazables al LLM y contrastar sus afirmaciones, pertinencia y cobertura antes de publicar. La respuesta académica depende de la evidencia recuperada, no de contenido docente predefinido ni de memoria del modelo. Conservar todos los gates. La vía web es una extensión del mismo flujo, sujeta a enmienda constitucional, política y permiso docente; no se activa por este plan.

## Technical Context

Python 3.12, GenerationPort y worker local ya existentes; PDF docentes y catálogo de unidades con páginas originales en un entorno de laboratorio propio. Sin descargas, modelos nuevos, datos de participantes ni cambios de esquema en este bloque de planificación. Qwen3-8B, Qwen2.5-14B y Mistral-24B fueron diagnósticos no comparables para ranking; el último mostró 4/4 turnos pero dos falsas contradicciones. `verification.py` solo comprueba testigos estructurales: `independent_semantics=false`, `publication_allowed=false`. G2/SC001, reserva y publicación cerrados.

## Constitution Check

Principios I/V y exclusiones del MVP impiden Internet durante sesiones; permiso docente no los enmienda. Principio IV exige separar generación y verificación. Se conservan arquitectura/contratos, estado explícito, T090/T150, consentimiento, retención, acceso, aislamiento y validación de voz separada. Un `unknown` semántico no autoriza salida. No se modificó la constitución.

## Design / sequence

Decisión de capacidad posterior (27-10-2026): [no continuar ajustando el 7B sobre el banco expuesto; propuesta única 7B/14B](evidence/generator-capacity-decision-v1/decision.md). Comparación propuesta de evidencia fija frente a recuperación normal, con controles nuevos, presupuesto y baseline común; no ejecutada. El 24B disponible no se descarta universalmente ni se activa como fallback. Se deja versión auditable y la implementación quieta durante la auditoría global independiente; gates y reserva cerrados. La [adenda de conclusiones de la auditoría](evidence/generator-capacity-decision-v1/audit-followup.md) enlaza sus informes sin duplicarlos: recuperación híbrida/reranking y verificadores especializados siguen siendo candidatos de investigación, no soluciones adoptadas ni verificadores validados. No se inicia otra inferencia o incorporación de dependencias por esta adenda.

Decisión de presentación del 27-10-2026: usar documentos/títulos/páginas legibles; no pedir IDs por frase. Reutilizar la procedencia recuperada para «Fuentes consultadas» cuando no exista atribución semántica verificada. Mantener el juicio sustantivo separado y conservar ST01 bajo el contrato anterior. Implementación y pruebas CPU preceden a un ensayo nuevo y acotado de seguimiento/ejemplo; no ajustar sus oráculos tras observar respuestas.

Bloque pedagógico posterior: una extensión general optativa frente al baseline literal, sin cambiar ranking ni respuestas predefinidas. La aclaración del usuario permite ficción coherente y exige respaldo al principio/interpretación, no a cada detalle del escenario. Tres conversaciones nuevas de cuatro turnos se congelaron antes de inferir, con ramas y presupuesto. El ensayo terminó parcial por un límite de salida, tras conservar un primer fallo de telemetría y una única recuperación técnica: no se promueve el perfil por pruebas CPU ni por conversaciones incompletas. Ver [comparación y decisión](evidence/pedagogical-comparison-recovery-run-v1/report.md).

1. Versionar fuentes docentes activas, procedencia, retirada y política; mantener web apagada. Registrar el punto de extensión web condicionado, sin red en este bloque.
2. Recuperar unidades desde pregunta e historial realmente mostrado. Si la evidencia es insuficiente o conflictiva, reintentar localmente con presupuesto y trazas limitados; no inferir suficiencia a partir de solapamiento léxico.
3. Entregar al LLM solo evidencia recuperada trazable y obligaciones del turno. Generar explicación; distinguir paráfrasis, inferencia con premisas recuperadas y ejemplo hipotético, cuyo principio requiere fuente.
4. Contrastar afirmaciones, pertinencia y cobertura mediante evaluación separada del generador. Una hipótesis de verificador debe ser distinta de las tres vías fallidas y medir permisos/rechazos falsos y cobertura; un banco finito no garantiza verdad. Mantener publicación cerrada mientras no exista candidato viable.
5. En insuficiencia, conflicto o incertidumbre, conservar estado y expresar límite o pedir aclaración concreta. No usar respuesta académica prefabricada ni sustituir una pregunta difícil por otra lección.
6. Solo después: revisión docente, conversaciones desde estado real, tres repeticiones por caso, reserva no usada para ajuste, gates G2/G3/G4 y regresiones. Ningún ensayo de laboratorio autoriza publicación ni acredita voz o utilidad humana.

Contrato detallado, evidencia y criterios de avance: [plan de acción](evidence/grounded-tutor-action-plan.md). Decisiones históricas A–T, tiempos, presupuestos y alternativas quedan íntegros en el [plan anterior](evidence/speckit-history-2026-10-25/plan.md); el historial no se carga salvo para auditar una decisión concreta.

T063/T064/T071 forman una misma frontera: política vigente de fuente de la aplicación, obligaciones/afirmaciones trazables y entrega citable al generador. El [contrato unido y la hipótesis T072](evidence/rag-independent-evaluation-design.md) registran qué aporta cada módulo existente, qué sigue faltando y cómo descartar una vía semántica inviable. El preview del laboratorio jamás equivale a salida para participante.

El estudio mínimo de T072 descartó H1 (plan proposicional + comprobador determinista) como puerta para texto libre: no detecta por sí mismo cláusulas añadidas ni inversiones al realizar el plan. Se mantiene el RAG generativo en laboratorio, sin construir un compilador simbólico general ni atomizar por defecto toda la asignatura. La elección entre revisión humana de cada salida, lenguaje verificable más acotado o investigación separada de otro evaluador es una decisión material de alcance; ninguna se aplica como sustitución silenciosa.

Antes de recuperación y generación, una decisión de alcance con procedencia docente distingue `in_scope`, `out_of_scope`, `uncertain_scope`, `mixed` y peticiones operativas. La presentación de la asignatura contiene temas declarados, pero advierte que el cronograma puede cambiar y que el examen se basa en lo visto en clase; el catálogo parcial de PDF no define por complemento todo lo excluido. Por ello el laboratorio solo pronuncia «no necesitas estudiarlo» ante una exclusión explícita y vigente, no ante ausencia de resultados. La evaluación de alcance es independiente del juicio de suficiencia documental y del poscontrol semántico.

El usuario confirmó el 25-10-2026 el alcance de la [política v1](evidence/course-scope-policy-v1.json) para la actividad de laboratorio de Ingeniería del Software, sin bloques extra como bloques propios por ahora. La política liga curso/actividad/versión y hashes de fuentes; el [ensayo solo lectura](evidence/course-scope-policy-validation-v3.json) revalidó SQL y tres rutas con selección semántica inyectada. El binding no aprueba respuestas: la selección de bloques desde preguntas libres y el control semántico posterior siguen pendientes.
