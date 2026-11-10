# Siguiente incremento: primera conversación generativa de autoestudio

Estado: plan y auditoría solicitados; no implementación delegada ni modelos ejecutados. Fecha: 27 de octubre de 2026.

## Objetivo observable y alcance

El docente prueba un diálogo por chat sobre requisitos con respuestas realmente producidas por un LLM local a partir de recuperación real del corpus v2. Empieza por «¿Qué es un requisito en Ingeniería del Software?» y «¿Qué tipos de requisitos hay?», y continúa con aclaración y ejemplo. No preparar contenido académico fijo para esas entradas ni limitar el corpus a sus páginas.

Se pretende comprobar integración y calidad de una candidata, no declarar que funciona todo el bloque, que la revisión semántica está resuelta o que está listo el piloto con estudiantes. La primera entrega puede ser diagnóstica de laboratorio; debe distinguirla de una función participante autorizada.

Fuentes: [recuperación v2.1](../audits/2026-10-27-retrieval-increment/report.md), [limitación aceptada](../audits/2026-10-27-retrieval-increment/accepted-table-limitation.md), [corpus v2](../audits/2026-10-27-requirements-block/report.md), [plan general](2026-10-27-consolidated-action-plan.md), [técnicas elegidas](2026-10-27-technology-and-workflow-decisions.md).

No incluye examen, notas, rúbricas, pistas de examen, voz, web en sesión, nuevos modelos, detector especializado, reranker o más optimización de ranking. Los huecos documentales y la falta de INCOSE siguen visibles. Las tablas son una limitación aceptada; no son motivo para bloquear toda prueba, pero tampoco para atribuir cualquier error al formato.

## Entregas dentro del incremento

### E0. Contrato corto y comprobación sin inferencia

Localizar el recorrido generativo existente y sus límites. Reutilizar `GenerationPort`, adaptador local, worker y contratos de historial cuando sea posible, sin construir otro motor de agentes. Declarar qué está realmente conectado a v2 y qué no.

Antes del primer modelo, documentar tres superficies distintas:

1. Texto bruto del proveedor, con causa de terminación y errores.
2. Candidato diagnóstico visible únicamente en la revisión docente de laboratorio, con estado semántico real y advertencia persistente.
3. Salida participante, que permanece deshabilitada.

La revisión no disponible se registra `unknown/unverified`, nunca `supported` ficticio. Las pruebas con evaluadores simulados no autorizan entrega real. El contrato de `LaboratoryConversation` exige hoy un veredicto positivo para su preview; no se cambia ese veredicto para lograr mostrar respuestas. El diagnóstico de generación ya existente puede conservar candidatos en artefactos de laboratorio, sin otorgar permiso de publicación. Cualquier adaptación de la vista docente requiere una frontera explícita que permita inspeccionar el candidato sin convertirlo en salida participante o falsear el estado de revisión. Revisar esa frontera antes de activarla. Si no está justificada, entregar primero el diagnóstico y transcriptos reales al coordinador; no anunciar chat interactivo terminado.

Revalidar corpus/permiso antes y después de esperas y antes de mostrar contenido. El candidato puede contener instrucciones o HTML no confiables; renderizar como texto/Markdown seguro. No ejecutar herramientas o enlaces por instrucciones del modelo. El host conserva autoridad sobre fuentes, cancelación, cierre y conservación.

**Salida E0:** configuración y diagrama efectivo con consumidores, pruebas CPU de autoridad y entrega, modo docente identificado. No necesita probar otra vez todas las garantías históricas.

### E1. Una captura real y acotada, sin ajuste dentro del banco

**Recuperación:** utilizar v2 completo con sus 117 unidades disponibles e índice acreditado. Propuesta de candidata de este diagnóstico: rama densa existente, porque obtuvo mayor recall final y MRR que las otras en v2.1; activación explícita solo para el experimento, sin reemplazar el baseline conservado ni declarar promoción general. Registrar las pérdidas ya conocidas de esa rama. Esta es una selección prospectiva de candidata para observar el conjunto, no una reinterpretación de los resultados anteriores como aprobados.

Registrar por turno consulta original, referente realmente mostrado, candidatos, pasajes finales, omisiones y presupuesto. No seleccionar páginas por el ID de la pregunta del demostrador. No inyectar contexto fijo oculto ni suficiencia positiva inventada. Si se realiza en el futuro un control con evidencia fija, tiene que ser otro ensayo declarado y no esta demostración de RAG.

**Modelo:** propuesta de única candidata: Qwen2.5-14B-Instruct NF4 local ya utilizado, sin descargas, tomando snapshot/tokenizer/plantilla efectivos del recurso existente. No se afirma que sea superior ni que sus fallos históricos estén resueltos. La hipótesis es comprobar el recorrido nuevo con fuentes recuperadas y referencias legibles, no volver a ajustar sus controles expuestos. Si no está realmente disponible o es incompatible, no sustituir automáticamente por otro modelo: informar el bloqueo y completar E0. Mantener embeddings en CPU explícita para no competir inadvertidamente por VRAM.

**Recursos prospectivos:** máximo ocho peticiones académicas más un calentamiento separado; máximo 768 tokens nuevos por respuesta y 60 segundos por petición. Estos son límites propuestos de diagnóstico, no promesa de latencia del producto. Fijar configuración y plazo global finito de 20 minutos antes de comenzar. Si el backend no admite el presupuesto, rechazar/negociar de forma explícita y congelar una revisión antes de inferir. No aplicar recortes silenciosos. Una cancelación o salida `length` no se presenta como respuesta completa.

Anunciar propósito, modelo, presupuesto y duración; comprobar disponibilidad vigente y muestrear GPU antes/durante/después. Si hay competencia o disponibilidad incierta, aplazar el trabajo propio o registrar rendimiento inconcluyente. No detener ComfyUI u otros procesos. La disponibilidad comunicada en rondas pasadas no se trata como una medición actual.

**Escenarios:** una conversación de cuatro turnos con las dos preguntas iniciales, una aclaración y un ejemplo; otra de cuatro turnos para continuidad, rectificación/cambio y un caso sin evidencia adecuada. Congelar las entradas y criterios antes de generar. Los seguimientos deben ser coherentes con lo realmente mostrado: fijar previamente la intención y una regla de selección, no fingir un historial que el docente no vio. Si una respuesta bloquea o no termina, no inventar su continuación. Los casos independientes presupuestados sí pueden ejecutarse y se contabilizan por separado.

Para conservar un seguimiento en laboratorio, registrar exactamente qué candidato diagnóstico se mostró al revisor y cuándo. No mezclarlo con el historial del participante ni llamar «respuesta autorizada» al candidato. Si se mantiene solo una captura offline, declarar que el historial corresponde al experimento y no a una sesión humana ya realizada.

La generación diagnóstica sobre pasajes recuperados no se toma como prueba de suficiencia: dejar explícito `not_assessed` cuando corresponda. No permitir inferencia sin permiso de fuente, fuente alterada o entrada inválida. Registrar ausencia/conflictos detectados y respuestas no respaldadas, aunque el texto parezca fluido.

**Salida E1:** solicitudes y salidas reales, fuentes, terminaciones, transcripciones completas y revisión técnica por turno contra originales. Sin reajustar prompt, páginas, ranking u oráculo hasta aprobar; conservar el primer fallo.

### E2. Prueba breve del usuario

Si el recorrido docente de E0 permite inspección segura y E1 produce contenido completo revisable, entregar comando y acceso en la interfaz existente con una única configuración identificada. Antes, el implementador verifica arranque, una pregunta real, seguimiento, ejemplo, espera/cancelación y cierre/reentrada. Una prueba con doble de proveedor no cumple esa comprobación de contenido.

El usuario puede empezar por definición y tipos, con fuentes visibles, y pedir después una reformulación o ejemplo. No obligarlo a revisar métricas o aprobar cada script. Puede realizarse desde su ordenador; si sigue en móvil, el coordinador maneja la interfaz y comparte los textos/capturas íntegros necesarios. Esta modalidad valida contenido con él, no su navegación directa.

No ofrecer como función correcta una salida que ya se sabe defectuosa. Los fallos observados se incluyen en el informe con sus fuentes para diagnóstico; si impiden la demostración mínima, se entrega ese resultado y la corrección localizada propuesta, sin llamarla lista para prueba ordinaria. No bloquear todo el análisis esperando a que ningún caso imaginable falle.

**Salida E2:** qué observó el usuario, cambios pedidos y estado real: implementado/verificado/disponible/probado, separados. No aceptación académica automática ni apertura de estudiantes.

## Criterios de revisión

| Área | Qué se comprueba | Si falla |
|---|---|---|
| RAG real | Misma pregunta/referente produce una selección registrada sin páginas prefijadas por test. | Fallo de integración/recuperación; no atribuirlo al generador. |
| Definición | Explica servicio/restricción y no confunde requisito con el proceso de ingeniería de requisitos. | Conservar afirmaciones y pasajes; corregir la causa identificada, sin respuesta prefabricada. |
| Tipos | Presenta clasificaciones según material disponible y no mezcla destinatario/detalle con contenido como categorías excluyentes. | Revisar contexto o interpretación según lo recibido realmente. |
| Continuidad | La aclaración responde a la duda y cambia la estrategia; el ejemplo es coherente y no introduce garantías sin premisas. | Registrar si es un problema pedagógico, conceptual o de memoria. |
| Límites | No atribuye a fuentes lo no recuperado; tablas insuficientes y ausencia se reconocen sin declarar fuera de temario. | No promocionar esa capacidad. Una limitación visible y correcta no es error académico. |
| Entrega | Solo lo mostrado entra en historial de esa superficie; cierre/cancelación/retirada impiden entrega tardía. | Corregir antes de ofrecer prueba al usuario; no seguir con participante. |

Dos preguntas correctas permiten continuar el guion, no declarar cobertura de toda la asignatura. El tamaño de esta muestra sirve para integración y primera decisión docente; no mide tasa general de error o eficacia humana. La revisión del coordinador y del docente no sustituye un verificador autónomo por turno para el producto futuro.

## Decisión al terminar y preservación

Si funciona el episodio mínimo, ofrecerlo para prueba docente y preparar solo el siguiente cambio derivado de su feedback. Si falla, entregar evidencia que localice recuperación/contexto, generación, continuidad o entrega. No iniciar automáticamente más modelos, rerankers, detectores o una nueva campaña. Proponer una corrección acotada; ampliar presupuesto requiere una decisión prospectiva.

Usar SpecKit proporcionalmente, sin regenerar/compactar perdiendo estados. Modificar solo rutas necesarias con copia/manifiesto y pruebas pertinentes. No commits, Reset, alteración de paquetes v1/v2, fuentes, reserva o presupuestos antiguos; cada intento tiene carpeta/ID exclusivos y escritura que no sobrescriba recibos. El incidente de sobrescritura de v2.1 se conserva y no se presenta como restaurado. No migrar índices habituales ni detener servidores ajenos. T077 global y G2/SC001 permanecen abiertos. T090/T150 siguen vigentes.

## Auditoría del propio plan

| Riesgo detectado al redactarlo | Corrección incorporada | Pendiente real |
|---|---|---|
| Pedir un revisor positivo ficticio para mostrar una salida. | E0 separa inspección diagnóstica de publicación y prohíbe `supported` simulado. | Revisar el contrato concreto de la vista antes de activarla. |
| Promover una rama rechazada globalmente mediante una excepción de tablas. | Candidata densa explícita y limitada al diagnóstico; baseline y resultados v2.1 intactos. | Medir el contenido recibido; no se presupone suficiencia. |
| Elegir manualmente fuentes para que pasen las dos preguntas. | RAG real obligatorio y trazas, sin reglas por ID de test. | La pérdida de contexto sigue siendo una limitación documentada. |
| Convertir el primer ensayo en una campaña indefinida. | Un modelo, ocho peticiones más calentamiento y límites prospectivos. | Confirmar recurso/configuración antes de comenzar. |
| Confundir ficción coherente con una alucinación por no ser literal. | Revisar principio y conclusiones; permitir datos hipotéticos coherentes. | Casos concretos adjudicados contra fuentes, no criterio léxico universal. |
| Volver a ofrecer al usuario un recorrido roto o solo un fixture. | E1 real antes de E2 y descripción honesta si el mínimo falla. | La utilidad y calidad no pueden aprobarse por planificación. |
| Tratar «continuar» como permiso para abrir estudiantes. | Todo el incremento es docente/laboratorio y los gates no cambian. | Publicación autónoma y piloto humano son decisiones posteriores. |

**Dictamen:** plan suficiente para encargar el incremento acotado, sin una nueva auditoría general. No garantiza que el modelo dé respuestas correctas. Sus incertidumbres son precisamente lo que debe medir la entrega. No se ha enviado todavía a otra tarea.
