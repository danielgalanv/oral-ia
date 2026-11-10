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


## Parte 2: implementación documental acotada I0/I1

Paquete nuevo materiales/docente/piloto-requisitos/paquete-v1 con originales, capturas, extracciones y manifiesto. PdfExtractor/PptxExtractor existentes; QA visual focal con herramientas instaladas; sin OCR/modelos. Extensión documental de Materiales en Tecnica.tsx, servida por perfil local separado oralia.documentary desde scripts/demo.ps1 -Documentary, sin SQL ni Chroma. Un único servidor localhost, originales por ID validado, acceso local explícito y cierre/reentrada; raíz habitual intacta. Consulta literal y mapa curado, sin score semántico. No ejecutar el launcher de autoestudio que carga embeddings. Registro en docs/audits/2026-10-27-part2-corpus; pruebas proporcionales de aislamiento/acceso/integridad y recorrido real de navegador si está disponible.

Estado de entrega parte2: corpus v1.1 y perfil documental implementados/verificados; navegador real y launcher con PATH habitual comprobados, servicios propios parados. [Informe](../../docs/audits/2026-10-27-part2-corpus/report.md). INCOSE sigue sin original adquirido; cuarentena y alcance visibles. No activa fases posteriores.

## Ampliación documental v2 autorizada

Reutilizar paquete-v1 y extractores CPU; paquete-v2 independiente con originales por hash, representaciones revisadas y evidencia en docs/audits/2026-10-27-requirements-block. Matriz derivada de las 89+14 páginas principales y examen focal de material docente adyacente, sin trabajos de alumnos. Añadir solo secciones complementarias justificadas. Selección optativa `demo.ps1 -Documentary -DocumentaryPackage v2`, por defecto v1.1, servidor propio en puerto distinto del8022; sin cambio a un servidor ya iniciado. QA de texto/tabla/figura, hashes/enlaces/acceso/HTML inerte y navegador real; no cargar modelos ni iniciar T077. No regenerar IDs/estados históricos.

## Recuperación v2.1 optativa, 27-10-2026

Ejecutar exclusivamente [plan incremental autorizado](../../docs/plans/2026-10-27-retrieval-increment.md), sin regenerar artefactos. Composición única en oralia.documentary.retrieval con adaptadores existentes, CPU explícita/local-only, hashes efectivos y segmentación según tokenizer; índice nuevo fuera del corpus. Rutas documentales anteriores siguen por defecto. Banco/oráculo y protocolo congelados antes del ranking; una pasada por estrategia y adopción sujeta a pérdidas por subtema. Resultado: ninguna candidata supera la tolerancia en contexto final; baseline conservado, sin otro modelo o ajuste. [Entrega y límites](../../docs/audits/2026-10-27-retrieval-increment/report.md). No integra GenerationPort o participante, ni acredita suficiencia/alcance semántico. No modifica los gates o el orden autoestudio→examen.

## E0 del primer diálogo generado autorizado, 27-10-2026

Inventario y contratos según [plan específico](../../docs/plans/2026-10-27-first-generated-study-increment.md), sin sustituir catálogo/binding del laboratorio por v2 silenciosamente. [Informe](../../docs/audits/2026-10-27-first-generated-study/report.md) y [protocolo previo](../../docs/audits/2026-10-27-first-generated-study/protocol-v1.json): helper CPU con recibos exclusivos, estado unverified/not_assessed y presupuesto rechazado antes de worker. No se activa una superficie de inspección nueva; LaboratoryConversation mantiene revisión positiva y participante cerrado. GPU ocupada vigente; no cargar encoder/GPU ni esperar automáticamente. E1/E2 no ejecutados. Corrección futura localizada: coherencia del límite60s lab/worker y nueva disponibilidad antes de inferencia, con congelación prospectiva; no modelo ni prompt alternativos.

## Cableado CPU docente autorizado, 27-10-2026

Implementación directa sobre oralia.documentary.retrieval v2.1 y GenerationPort existente, con binding propio del paquete/actividad diagnóstica y sin mezclar catálogo SQL antiguo. Nuevo estudio de inspección/API y componente Materiales optativo; normal deja proveedor desconectado, fixture explícito rotulado. Control de integridad y acceso antes/después de esperas, recibos separados de publicación, confirmación DOM, épocas/timeout, lease y purga. Protocolo sucesor50s aceptado sin cambiar backend. Índice existente reabierto CPU, sin construir; pruebas de frame del adaptador con pipe doble y recorrido real de navegador con fixture. Runner futuro solo bajo switch/autorización nuevos; no ejecutado con pesos generativos. [Entrega](../../docs/audits/2026-10-27-generated-study-cpu/report.md). T102/T103 mantienen captura/calidad y E2 reales pendientes; esta entrega completa el cableado CPU, no declara feature cerrada.
