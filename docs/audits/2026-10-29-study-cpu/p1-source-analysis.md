# P1: distinción y cobertura, sin inferencia nueva

Leído el informe del coordinador `2026-10-28-coordinator-six-turns/report.md`, que conserva como cierre de P1 «verificar se centra en la calidad individual ... validar ... conjunto» y enumera Requisitos89, Procedimiento11/10, Requisitos76 y NASA208 como contexto recibido. No se inventa una transcripción completa que ese informe no contiene.

Se contrastaron las extracciones revisadas del corpusv2 directamente, sin modelos o índices nuevos:

- Procedimiento10: la verificación comprueba calidad de la **especificación**, incluida completitud y consistencia interna/externa. Ya contradice usar «solo individual» como diferencia definitoria.
- Procedimiento11: continúa con calidad de cada requisito individual. Son dos escalas de la misma actividad.
- Procedimiento12: validar comprueba correspondencia del sistema descrito con necesidades de negocio de clientes y usuarios, con su aprobación.
- Requisitos72: validación trata de demostrar que los requisitos definen lo que el cliente realmente quiere. Requisitos73 incluye validez/necesidades y además consistencia, completitud, realismo y verificabilidad.
- Requisitos89, recibido en P1, enumera esos controles de validación pero no desarrolla la relación con necesidades. NASA208 aplica su checklist de validación a características individuales y del conjunto: tampoco justifica una partición rígida por escala.

Conclusión proporcionada: la respuesta tiene contenido útil sobre calidad, pero la dicotomía individual/conjunto puede enseñar una diferencia equivocada. No se trata de exigir más exhaustividad NASA ni de condenar todos sus ejemplos. La finalidad de las actividades y la escala de los objetos son ejes distintos. Existen fuentes para la finalidad de validación; su ausencia en los pasajes entregados es cobertura incompleta, no ausencia del concepto en el corpus. Aun con esa cobertura incompleta, Procedimiento10 recibido bastaba para evitar la exclusividad individual.

El empaquetado anterior terminaba al alcanzar cinco páginas y no registraba como omisiones las candidatas posteriores; `omitted_context=[]` no demostraba cobertura exhaustiva. Para P2 el coordinador informa de candidatas Procedimiento12/Requisitos72 que no entraron, con4917caracteres y cinco páginas. No se extrapola ese ranking concreto a P1, cuyos candidatos completos no están en el informe.

Se preparó selección CPU optativa `comparison-coverage/v1`: deriva dos facetas de construcciones comparativas generales, favorece términos discriminativos y encabezados **solo dentro de candidatas existentes**, sin IDs de documentos, más contexto, nuevas búsquedas ni respuestas predefinidas. Los seguimientos solo usan las preguntas mostradas recibidas; cambio de tema descarta esas facetas. Registra facetas sin coincidencia y omisiones por límite de páginas. Mantiene páginas enteras, hashes, límites, índice y estado unverified/not_assessed.

Límites: es una heurística de diversidad léxica, no comprobación semántica. No cubre todas las formas de comparación; tampoco puede promover un pasaje que no llegó a las candidatas. Una página promovida puede no caber por caracteres. Las pruebas con corpus sintético demuestran selección/aislamiento, **no que P1 real esté corregida**. Aumentar tokens tampoco garantiza la distinción correcta y podría ampliar una explicación equivocada. La validación del contenido real queda pendiente por la instrucción humana de no usar GPU.
