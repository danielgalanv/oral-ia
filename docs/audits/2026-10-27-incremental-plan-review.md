# Segunda auditoría del plan: entregas incrementales

Fecha: 27 de octubre de 2026. Revisión tras las decisiones del usuario: chat primero, voz después; corpus preparado por el asistente; preguntas/ayudas/salto configurados por el profesor; ninguna evaluación del alumno; datos descriptivos y ensayo temprano.

Objeto: [plan consolidado](../plans/2026-10-27-consolidated-action-plan.md). Método: lectura completa y contraste con decisiones y auditoría previa. No se ejecutó implementación ni modelos y no se contactó con otras tareas.

## Dictamen

**Decisión humana posterior que prevalece sobre la recomendación de orden de esta auditoría:** empezar por autoestudio y después adaptar al examen. Saltar aplaza la pregunta hasta terminar la ronda establecida y regresar a pendientes; no es omisión irreversible. Una ayuda es la aclaración que ORALIA genera a petición del alumno para comprender la pregunta y consume una unidad por ayuda válida producida, sin duplicación por reenvío. El plan consolidado recoge estas decisiones; la recomendación histórica de empezar por examen básico que aparece abajo queda sustituida. No se ha reanudado implementación.

El objetivo ya está suficientemente definido para **preparar un primer bloque de implementación acotado**, después de una orden de reanudación. No está listo para encargar todo el plan de una vez ni para activar estudiantes. No hace falta otra auditoría global antes de ese bloque.

La deficiencia mayor era organizar el trabajo por capas técnicas, lo que dejaba la prueba del usuario para demasiado tarde. El examen sin generación estaba condicionado indirectamente por problemas semánticos del autoestudio, pese a que puede funcionar sin modelo. Se añadió la sección 10 al plan para establecer entregas visibles y dependencias separadas.

## Hallazgos adicionales y correcciones propuestas

| ID | Carencia detectada | Cambio incorporado al plan |
|---|---|---|
| R01 | Fases técnicas sin producto probables hasta muy tarde. | I0–I8 con recorrido visible, prueba propuesta, dependencias y límites. Cambios internos se verifican técnicamente; no se pide revisión humana por cada script. |
| R02 | Examen básico ligado a RAG, generador o revisor sin necesidad. | I2/I3 independientes de inferencia. Preguntas del profesor, respuestas exactas y estados operativos, sin evaluación. |
| R03 | Saltar sin volver dejaba la pregunta a la vez pendiente y omitida. | Pendiente de vuelta solo si esta está permitida; omisión definitiva identificada y confirmada. Configuración coherente antes de empezar. |
| R04 | Respuesta enviada, borrador y modificación al volver no diferenciados. | Confirmación explícita, no sustitución silenciosa y revisión/versionado solo según política. No corrección automática del contenido del alumno. |
| R05 | Consumo de ayudas ambiguo ante fallos, doble clic o reconexión. | Propuesta de contabilización en entrega confirmada, una vez por identidad; límites persistentes durante la sesión; errores y duplicados no gastan otra unidad. |
| R06 | Configuración mutable e historial entre modos podían filtrar preguntas/soluciones o alterar el recorrido. | Instantánea de actividad y sesiones separadas; retirada de permisos mantiene efecto inmediato. No memoria longitudinal ni adaptación por corrección inferida. |
| R07 | Estadísticas sin definición podían contar saludos/reintentos como preguntas o crear copia oculta de contenido. | Recuentos trazables, conceptos sin clasificar cuando corresponda, categorías no necesariamente disjuntas y consentimiento por superficie; ningún diagnóstico por frecuencia. |
| R08 | Rechazo semántico podía producir otra conversación inutilizable o reintentos ilimitados. | Política de recuperación/límites prospectiva, continuidad y opciones operativas; cada nuevo intento revisado y conservado sin editar primeros fallos. |
| R09 | Detector específico podía convertirse en dependencia obligatoria de toda entrega. | Política compuesta por clases de error; detector como candidato. Pruebas docentes de laboratorio posibles sin declarar participante habilitado. |
| R10 | «Implementado» y «probado por el usuario» no tenían estados distintos. | Estados separados y entrega con guion, límites y resultado esperado. El implementador verifica antes; la prueba del usuario no sustituye controles técnicos ni eficacia. |

Son decisiones de planificación propuestas para las entregas, no pruebas de defectos nuevos del código. Su traducción exacta a contratos y tareas corresponde al incremento que se autorice.

## Primer bloque recomendado

1. Conciliar estado real de la implementación detenida, sin rehacer correcciones demostradas.
2. I0: arranque/acceso desde el entorno habitual y cierre/reentrada.
3. I2: profesor configura preguntas; alumno responde en orden y confirma; cierre y consulta consentida por el profesor. Sin ayudas generadas, salto/vuelta ni evaluación en esta primera entrega, y con límites visibles.
4. Ofrecer al usuario ese recorrido para prueba, con preguntas propias. No esperar modelos nuevos, todas las fuentes externas, analíticas o voz.
5. Continuar I3 e I1 según feedback y dependencias; preparar el resto sin cambiar silenciosamente lo que el usuario está probando.

El corpus documental tiene autorización específica de preparación y puede avanzar sin activar el producto. El examen no sustituye al objetivo de autoestudio: solo permite comprobar una capacidad independiente mientras se resuelve la vía generativa.

## Lo que queda para los incrementos posteriores

- Corpus ampliado real: el inventario inicial no equivale a documentos extraídos, revisados o indexados.
- Configuración concreta de ayudas, salto/vuelta y edición; el plan ofrece comportamiento mínimo y necesita reflejarlo en SpecKit antes de implementar cada incremento.
- Presupuesto y criterios congelados de los experimentos de generación/revisión; no necesarios para I0/I2.
- Tolerancia real de espera y frecuencia de límites, observadas con el usuario antes de decidir preparación para estudiantes.
- Topología, consentimiento y acceso del piloto humano. No se añade LAN ni se recluta automáticamente.

El piloto solo comienza cuando las funciones incluidas y sus controles estén aceptados. Las seis pérdidas históricas, las revisiones pendientes y los gates conservan su estado; se distingue su efecto en el incremento nuevo de un cierre global histórico. No se inventa aceptación ni se rebaja un gate para avanzar.

## Resultado de esta revisión

Se puede pasar a implementación incremental del primer bloque cuando el usuario lo indique. La revisión no ha iniciado esa ejecución. El plan actualizado contiene las correcciones de planificación y mantiene la pausa y la prohibición de mandar trabajo a otras tareas.
