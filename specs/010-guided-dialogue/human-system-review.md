# Revisión humana del sistema — 24 diálogos sintéticos

Estado: pendiente de revisión humana. No es prueba de utilidad con personas ni voz real.

Fuente del requisito: plan.md, G1: «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema».

Código: source-checkpoint-20261019.zip. Son estímulos y materiales ficticios; no se usa la transcripción ni la base personal.

## Rúbrica

| Criterio del sistema | Estado humano |
|---|---|
| Mantiene objetivo/pregunta y atribuye correctamente las fuentes | No evaluado |
| Repetir/reformular/ayuda producen lo solicitado o un límite claro | No evaluado |
| Contenido controlado suficiente y pertinente, sin anunciar generación libre | No evaluado |
| Pistas/fuentes/resumen no revelan soluciones protegidas | No evaluado |
| No califica, no infiere capacidad, no suplanta al docente | No evaluado |
| Recuperaciones y alternativas son comprensibles y ejecutables | No evaluado |

Revisión solicitada: indicar criterios cumplidos o casos/pasos que requieren corrección. Los asserts no sustituyen esta revisión.

Resultados técnicos: 24/24 diálogos con propiedades observadas; 46/48 actos, 36/36 críticos; seguridad pública 48/48. Los dos fallos ordinarios se mantienen publicados y no se ocultan.

## D01 — agua / self_study / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | hola | Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica. | greeting / orientation |
| 1 | dime que sabes sobre el agua? | ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión. | content_question / clarify |
| 2 | ¿A qué temperatura hierve el agua? | A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal. | content_question / ∅ |
| 3 | el agua puede pasar a ser vapor en algun momento? | La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición. | content_question / ∅ |
| 4 | dimelo | La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición. | repeat / ∅ |
| 5 | el agua puede pasar a ser vapor en algun momento? | Un paño húmedo puede secarse por evaporación sin hervir el agua que contiene. | content_question / ∅ |
| 6 | ¿Cómo pasa el agua líquida a vapor? | La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición. | content_question / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D02 — agua / self_study / guided_explanation

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Explícame paso a paso la condensación | La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie. | mode_switch / ∅ |
| 1 | no lo entiendo | La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor. | rephrase / ∅ |
| 2 | dame un ejemplo | Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire. | example / ∅ |
| 3 | compara con evaporación | Evaporación y ebullición producen vapor; se distinguen por dónde ocurre el cambio y por sus condiciones. | comparison / ∅ |
| 4 | puedes repetir? | Evaporación y ebullición producen vapor; se distinguen por dónde ocurre el cambio y por sus condiciones. | repeat / ∅ |
| 5 | quiero cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 6 | confirmo: congelación | La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio. | content_question / ∅ |
| 7 | dímelo | La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio. | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D03 — agua / self_study / practice_questions

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Ponme una pregunta de práctica sobre presión | ¿Qué información pedirías antes de comparar dos temperaturas de ebullición? | mode_switch / ∅ |
| 1 | no sé | Enumera las magnitudes que aparecen. | help / ∅ |
| 2 | otra pista | Comprueba unidades, condiciones y si se habla de una aproximación. | help / ∅ |
| 3 | dame la solución | ¿Qué tendría que coincidir para que la comparación de dos valores fuese pertinente? | content_answer / ∅ |
| 4 | no repitas; otro ejemplo | ¿Qué información pedirías antes de comparar dos temperaturas de ebullición? | example / ∅ |
| 5 | otra pregunta | ¿Qué tendría que coincidir para que la comparación de dos valores fuese pertinente? | content_answer / ∅ |
| 6 | terminar la sesión | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D04 — programa / self_study / presentation_preparation

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Quiero preparar una exposición sobre responsabilidades | El recorrido válido es entrada, validación, almacenamiento y salida. Un registro inválido pasa de validación a un aviso de salida sin conservarse como aceptado. Cada parte conserva su función declarada. Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación. El recorrido válido incluye almacenamiento; el recorrido rechazado produce un aviso sin conservar el registro como aceptado. | mode_switch / ∅ |
| 1 | ¿Cómo la organizo? | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | content_question / verification_failed |
| 2 | un ejemplo | Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación. | example / ∅ |
| 3 | ¿Y la entrada? | En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo. La entrada recibe un registro de inventario ficticio con un campo cantidad y lo pasa a validación. La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta. | content_question / ∅ |
| 4 | eso | En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo. La entrada recibe un registro de inventario ficticio con un campo cantidad y lo pasa a validación. La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta. | repeat / ∅ |
| 5 | me refiero a la entrada | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | content_question / verification_failed |
| 6 | reformula el objetivo | La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta. | rephrase / ∅ |
| 7 | terminar la sesión | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D05 — programa / self_study / concept_review

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Quiero repasar validación | ¿Qué justificarías hacer cuando falta un campo requerido? | mode_switch / ∅ |
| 1 | explica el rechazo de datos | ¿Cómo explicarías el recorrido de un registro incompleto? | content_answer / ∅ |
| 2 | compara entrada y almacenamiento | ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión. | comparison / clarify |
| 3 | otro ejemplo | ¿Qué justificarías hacer cuando falta un campo requerido? | example / ∅ |
| 4 | no sé cómo seguir | Identifica qué requisito no se cumple. | help / ∅ |
| 5 | y ahora? | Separa el camino válido y el caso incompleto. | continue / ∅ |
| 6 | puedes repetir? | ¿Qué justificarías hacer cuando falta un campo requerido? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D06 — programa / self_study / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | buenos días | Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica. | greeting / orientation |
| 1 | ¿Qué hace el programa? | ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión. | content_question / clarify |
| 2 | ¿Quién guarda los resultados? | El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos. | content_question / ∅ |
| 3 | dímelo | El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos. | repeat / ∅ |
| 4 | no entiendo, dilo de otra forma | Conservar un registro y presentar su resultado son responsabilidades diferentes. | rephrase / ∅ |
| 5 | cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 6 | confirmo: salida | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | content_question / verification_failed |
| 7 | continúa | Un registro aceptado por validación se conserva en el almacenamiento local ficticio. | continue / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D07 — agua / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | a los 99 grados | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | no sé justificarlo | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 3 | y ahora? | Revisa qué condición del entorno acompaña a la temperatura en el material. | continue / ∅ |
| 4 | puedes repetir? | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | repeat / ∅ |
| 5 | no entiendo, dilo de otra forma | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | rephrase / ∅ |
| 6 | otra pista | Organiza tu justificación en magnitud, unidad y condición. | help / ∅ |
| 7 | siguiente pregunta | El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar. | continue / limited |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D08 — agua / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | A presión atmosférica | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | ¿Qué unidad debo justificar? | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | content_question / ∅ |
| 3 | ayúdame | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 4 | repite la pregunta | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | repeat / ∅ |
| 5 | pon un ejemplo sin respuesta | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | example / verification_failed |
| 6 | otra forma | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | rephrase / ∅ |
| 7 | continuar | Revisa qué condición del entorno acompaña a la temperatura en el material. | continue / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D09 — agua / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | La evaporación ocurre en la superficie | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | dame la solución | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | content_answer / verification_failed |
| 3 | una pista | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 4 | y ahora? | Revisa qué condición del entorno acompaña a la temperatura en el material. | continue / ∅ |
| 5 | cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 6 | confirmo: condensación | ¿Cómo explicarías el origen de gotas en la superficie de un vaso frío? | content_answer / ∅ |
| 7 | repite | ¿Cómo explicarías el origen de gotas en la superficie de un vaso frío? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D10 — programa / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | La entrada recibe datos | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | no sé justificarlo | Identifica la operación que llega primero. | help / ∅ |
| 3 | ¿puedes ayudarme? | ¿Cómo justificarías separar recepción y validación? | content_question / ∅ |
| 4 | repite | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 5 | no entiendo la pregunta | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | rephrase / ∅ |
| 6 | otra pista | Identifica la operación que llega primero. | help / ∅ |
| 7 | siguiente | Distingue recibir un registro de decidir si cumple requisitos. | continue / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D11 — programa / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | El almacenamiento guarda resultados | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | compara los roles | ¿Cómo justificarías separar recepción y validación? | comparison / ∅ |
| 3 | eso | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 4 | la pregunta de almacenamiento | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 5 | otra forma | No se ha podido verificar una respuesta para este turno. Puedes pedir otra pregunta, elegir otro tema o terminar. | rephrase / verification_failed |
| 6 | puedes repetir? | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 7 | terminar la sesión | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## D12 — programa / oral_defense / defensa

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | La validación rechaza datos inválidos | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | ¿Y si falta un campo? | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | content_question / confirm_topic |
| 3 | ayuda | Identifica la operación que llega primero. | help / ∅ |
| 4 | repite la pregunta pendiente | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 5 | otra pista | Distingue recibir un registro de decidir si cumple requisitos. | help / ∅ |
| 6 | cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 7 | confirmo: salida | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | content_answer / ∅ |
| 8 | seguir | Identifica el resultado que llega a la salida. | continue / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H01 — agua / self_study / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ¿Qué diferencia hay entre ebullición y evaporación? | ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión. | content_question / clarify |
| 1 | elijo evaporación | La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición. | content_question / ∅ |
| 2 | Un ejemplo, por favor | Un paño húmedo puede secarse por evaporación sin hervir el agua que contiene. | example / ∅ |
| 3 | Repite la explicación | Un paño húmedo puede secarse por evaporación sin hervir el agua que contiene. | repeat / ∅ |
| 4 | Necesito una comparación | Evaporación y ebullición producen vapor; se distinguen por dónde ocurre el cambio y por sus condiciones. | comparison / ∅ |
| 5 | Necesito una pista | La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición. | help / ∅ |
| 6 | Dilo de otra manera | Evaporación y ebullición producen vapor; se distinguen por dónde ocurre el cambio y por sus condiciones. | rephrase / ∅ |
| 7 | Concluir | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H02 — agua / self_study / guided_explanation

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Quiero una explicación guiada sobre condensación | La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie. | mode_switch / ∅ |
| 1 | Continúa | Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire. | continue / ∅ |
| 2 | ¿Qué viene después? | La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor. | continue / ∅ |
| 3 | Dímelo | La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor. | repeat / ∅ |
| 4 | Un indicio | La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie. | help / ∅ |
| 5 | Otra forma | La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor. | rephrase / ∅ |
| 6 | Repite la pregunta | La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor. | repeat / ∅ |
| 7 | Quiero terminar | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H03 — agua / self_study / presentation_preparation

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Quiero preparar mi exposición sobre congelación | La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio. En un recipiente que se enfría puede formarse hielo a partir del agua líquida. Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido. | mode_switch / ∅ |
| 1 | Un ejemplo concreto | En un recipiente que se enfría puede formarse hielo a partir del agua líquida. | example / ∅ |
| 2 | Una comparación, por favor | Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido. | comparison / ∅ |
| 3 | Repite eso | Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido. | repeat / ∅ |
| 4 | Otra forma | En un recipiente que se enfría puede formarse hielo a partir del agua líquida. | rephrase / ∅ |
| 5 | Necesito una orientación | La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio. | help / ∅ |
| 6 | Quiero cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 7 | confirmo: presión | Una temperatura aislada no identifica por sí sola las condiciones de ebullición. El material declara presión atmosférica y una temperatura aproximada; otra condición o una aproximación requiere aclaración antes de concluir que existe una discrepancia. Dos afirmaciones con temperaturas próximas pueden necesitar aclarar presión y aproximación antes de compararlas. Comparar valores bajo las mismas condiciones permite discutirlos; mezclar condiciones impide una comparación directa. | content_question / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H04 — programa / self_study / practice_questions

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Preguntas de práctica sobre entrada | ¿Cómo justificarías separar recepción y validación? | mode_switch / ∅ |
| 1 | El registro no contiene el campo requerido | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | Necesito una orientación | Identifica la operación que llega primero. | help / ∅ |
| 3 | Un indicio | Distingue recibir un registro de decidir si cumple requisitos. | help / ∅ |
| 4 | Otra pista | Explica qué recibe y entrega cada parte sin atribuirle funciones extra. | help / ∅ |
| 5 | Repite la pregunta | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 6 | Dilo de otra forma | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | rephrase / ∅ |
| 7 | Finalizar | La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad. | finish / finish |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H05 — programa / self_study / concept_review

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | Quiero repasar validación | ¿Qué justificarías hacer cuando falta un campo requerido? | mode_switch / ∅ |
| 1 | Una pista, por favor | Identifica qué requisito no se cumple. | help / ∅ |
| 2 | Repite la pregunta | ¿Qué justificarías hacer cuando falta un campo requerido? | repeat / ∅ |
| 3 | Otra pista | Separa el camino válido y el caso incompleto. | help / ∅ |
| 4 | Dilo de otra manera | ¿Cómo explicarías el recorrido de un registro incompleto? | rephrase / ∅ |
| 5 | Quiero cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 6 | confirmo: salida | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | content_answer / ∅ |
| 7 | Repite la pregunta actual | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H06 — programa / self_study / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ¿Qué comprueba almacenamiento? | El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos. | content_question / ∅ |
| 1 | Un caso concreto | Un registro aceptado por validación se conserva en el almacenamiento local ficticio. | example / ∅ |
| 2 | Una comparación de responsabilidades | El recorrido válido incluye almacenamiento; el recorrido rechazado produce un aviso sin conservar el registro como aceptado. | comparison / ∅ |
| 3 | Repite la comparación | ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión. | ambiguous / clarify |
| 4 | Dilo de otra forma | Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación. | rephrase / ∅ |
| 5 | Necesito una orientación | El recorrido válido es entrada, validación, almacenamiento y salida. Un registro inválido pasa de validación a un aviso de salida sin conservarse como aceptado. Cada parte conserva su función declarada. | help / ∅ |
| 6 | Cambiar de tema | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 7 | confirmo: entrada | En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo. | content_question / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H07 — agua / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | 99 grados Celsius a presión atmosférica | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 4 | Dilo de otra manera | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | rephrase / ∅ |
| 5 | Otra pista, por favor | Revisa qué condición del entorno acompaña a la temperatura en el material. | help / ∅ |
| 6 | ¿Qué viene después? | Organiza tu justificación en magnitud, unidad y condición. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: congelación | ¿Qué estados necesitas identificar para describir la congelación? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Qué estados necesitas identificar para describir la congelación? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H08 — agua / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | La presión afecta a la temperatura | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 4 | Dilo de otra manera | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | rephrase / ∅ |
| 5 | Otra pista, por favor | Revisa qué condición del entorno acompaña a la temperatura en el material. | help / ∅ |
| 6 | ¿Qué viene después? | Organiza tu justificación en magnitud, unidad y condición. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: congelación | ¿Qué estados necesitas identificar para describir la congelación? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Qué estados necesitas identificar para describir la congelación? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H09 — agua / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | ambiguous / ∅ |
| 1 | 100 grados Fahrenheit aproximadamente | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica primero qué magnitud describe la pregunta. | help / ∅ |
| 4 | Dilo de otra manera | ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno? | rephrase / ∅ |
| 5 | Otra pista, por favor | Revisa qué condición del entorno acompaña a la temperatura en el material. | help / ∅ |
| 6 | ¿Qué viene después? | Organiza tu justificación en magnitud, unidad y condición. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: congelación | ¿Qué estados necesitas identificar para describir la congelación? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Qué estados necesitas identificar para describir la congelación? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H10 — programa / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | La persistencia valida los campos | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica la operación que llega primero. | help / ∅ |
| 4 | Dilo de otra manera | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | rephrase / ∅ |
| 5 | Otra pista, por favor | Distingue recibir un registro de decidir si cumple requisitos. | help / ∅ |
| 6 | ¿Qué viene después? | Explica qué recibe y entrega cada parte sin atribuirle funciones extra. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: salida | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H11 — programa / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | La validación escribe datos en disco | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica la operación que llega primero. | help / ∅ |
| 4 | Dilo de otra manera | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | rephrase / ∅ |
| 5 | Otra pista, por favor | Distingue recibir un registro de decidir si cumple requisitos. | help / ∅ |
| 6 | ¿Qué viene después? | Explica qué recibe y entrega cada parte sin atribuirle funciones extra. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: salida | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].

## V-H12 — programa / oral_defense / doubt_resolution

Revisión humana: pendiente.

| Paso | Entrada sintética | Salida observada | Acto / aviso |
|---|---|---|---|
| 0 | ∅ | ¿Cómo justificarías separar recepción y validación? | ambiguous / ∅ |
| 1 | La entrada muestra todos los avisos | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | content_answer / ∅ |
| 2 | Repite la pregunta actual | ¿Cómo justificarías separar recepción y validación? | repeat / ∅ |
| 3 | Necesito que me orientes | Identifica la operación que llega primero. | help / ∅ |
| 4 | Dilo de otra manera | ¿Qué responsabilidad atribuyes a cada parte al recibir un registro? | rephrase / ∅ |
| 5 | Otra pista, por favor | Distingue recibir un registro de decidir si cumple requisitos. | help / ∅ |
| 6 | ¿Qué viene después? | Explica qué recibe y entrega cada parte sin atribuirle funciones extra. | continue / ∅ |
| 7 | Hablemos de otra cosa | Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente. | topic_switch / confirm_topic |
| 8 | confirmo: salida | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | content_answer / ∅ |
| 9 | Repite la pregunta | ¿Cómo harías que un aviso refleje lo que realmente ocurrió? | repeat / ∅ |

Proveedor: reviewed-unit-renderer/v1. Fallos de propiedades automáticas: [].


Actualización semántica 19-10-2026: paquete vigente [24 diálogos completos](human-system-review-current.md) y [auditoría técnica de IA](technical-dialogue-audit-current.md). El paquete anterior se conserva como histórico; T067 no está aprobado.
