> Actualización20-10: documento histórico. D01 fue revisado por el usuario y requiere corrección en aquella versión. El sucesor corregido y su revisión pendiente están en D01-corrected-for-human-review.md y human-system-review-didactic-current.md; los otros23 no están aprobados.

# Revisión actual de 24 diálogos sintéticos

Implementación dialogue_contract 2.1.2, coherencia 2.1.0, reviewed-unit-renderer/v1. Datos ficticios; llamadas públicas reales al backend determinista. No son personas, voz real, modelos generativos ni evidencia de utilidad educativa.

## Decisión humana solicitada por T067

El plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». Para cada caso, valorar: pertinencia respecto a petición/objetivo; continuidad y referencia; claridad del apoyo/límite; discrepancias sin calificar; protección y fuentes; cierre y opciones comprensibles. Registrar Aceptable / Requiere corrección con caso y paso. Todos los campos permanecen **No evaluado** hasta respuesta humana explícita. Esto no acredita G3 ni voz real.

Las correcciones técnicas se detallan en technical-dialogue-audit-current.md. Prestar atención a cobertura limitada de exposición D04, claridad de órdenes compuestas D03, variedad W-H02 y reinicio de apoyo W-H04. No se solicita aprobar estos puntos de antemano.

## D01 — agua / self_study

Fuente: [D01.json](development-runs/2026-10-19-semantic-verified/D01.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** hola

**Respuesta:** Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica.

**Paso 1. Entrada:** dime que sabes sobre el agua?

**Respuesta:** ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión.

**Paso 2. Entrada:** ¿A qué temperatura hierve el agua?

**Respuesta:** A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal.

**Paso 3. Entrada:** el agua puede pasar a ser vapor en algun momento?

**Respuesta:** La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.

**Paso 4. Entrada:** dimelo

**Respuesta:** La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.

**Paso 5. Entrada:** el agua puede pasar a ser vapor en algun momento?

**Respuesta:** Un paño húmedo puede secarse por evaporación sin hervir el agua que contiene.

**Paso 6. Entrada:** ¿Cómo pasa el agua líquida a vapor?

**Respuesta:** La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D02 — agua / self_study

Fuente: [D02.json](development-runs/2026-10-19-semantic-verified/D02.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Explícame paso a paso la condensación

**Respuesta:** La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie.

**Paso 1. Entrada:** no lo entiendo

**Respuesta:** La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor.

**Paso 2. Entrada:** dame un ejemplo

**Respuesta:** Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire.

**Paso 3. Entrada:** compara con evaporación

**Respuesta:** La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor.

**Paso 4. Entrada:** puedes repetir?

**Respuesta:** La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor.

**Paso 5. Entrada:** quiero cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 6. Entrada:** confirmo: congelación

**Respuesta:** La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio.

**Paso 7. Entrada:** dímelo

**Respuesta:** La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D03 — agua / self_study

Fuente: [D03.json](development-runs/2026-10-19-semantic-verified/D03.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Ponme una pregunta de práctica sobre presión

**Respuesta:** ¿Qué información pedirías antes de comparar dos temperaturas de ebullición?

**Paso 1. Entrada:** no sé

**Respuesta:** Enumera las magnitudes que aparecen.

**Paso 2. Entrada:** otra pista

**Respuesta:** Comprueba unidades, condiciones y si se habla de una aproximación.

**Paso 3. Entrada:** dame la solución

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 4. Entrada:** no repitas; otro ejemplo

**Respuesta:** Elige explícitamente otro objetivo publicado, pide una pregunta de práctica o termina y solicita revisión docente. El contenido que no se ha verificado no se mostrará.

**Paso 5. Entrada:** otra pregunta

**Respuesta:** ¿Qué tendría que coincidir para que la comparación de dos valores fuese pertinente?

**Paso 6. Entrada:** terminar la sesión

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D04 — programa / self_study

Fuente: [D04.json](development-runs/2026-10-19-semantic-verified/D04.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Quiero preparar una exposición sobre responsabilidades

**Respuesta:** El recorrido válido es entrada, validación, almacenamiento y salida. Un registro inválido pasa de validación a un aviso de salida sin conservarse como aceptado. Cada parte conserva su función declarada. Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación. El recorrido válido incluye almacenamiento; el recorrido rechazado produce un aviso sin conservar el registro como aceptado.

**Paso 1. Entrada:** ¿Cómo la organizo?

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 2. Entrada:** un ejemplo

**Respuesta:** Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación.

**Paso 3. Entrada:** ¿Y la entrada?

**Respuesta:** En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo. La entrada recibe un registro de inventario ficticio con un campo cantidad y lo pasa a validación. La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

**Paso 4. Entrada:** eso

**Respuesta:** En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo. La entrada recibe un registro de inventario ficticio con un campo cantidad y lo pasa a validación. La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

**Paso 5. Entrada:** me refiero a la entrada

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 6. Entrada:** reformula el objetivo

**Respuesta:** La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

**Paso 7. Entrada:** terminar la sesión

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D05 — programa / self_study

Fuente: [D05.json](development-runs/2026-10-19-semantic-verified/D05.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Quiero repasar validación

**Respuesta:** ¿Qué justificarías hacer cuando falta un campo requerido?

**Paso 1. Entrada:** explica el rechazo de datos

**Respuesta:** ¿Cómo explicarías el recorrido de un registro incompleto?

**Paso 2. Entrada:** compara entrada y almacenamiento

**Respuesta:** ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión.

**Paso 3. Entrada:** otro ejemplo

**Respuesta:** Si falta el campo cantidad requerido, validación rechaza el registro y explica el campo que falta.

**Paso 4. Entrada:** no sé cómo seguir

**Respuesta:** Identifica qué requisito no se cumple.

**Paso 5. Entrada:** y ahora?

**Respuesta:** Separa el camino válido y el caso incompleto.

**Paso 6. Entrada:** puedes repetir?

**Respuesta:** ¿Qué justificarías hacer cuando falta un campo requerido?

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D06 — programa / self_study

Fuente: [D06.json](development-runs/2026-10-19-semantic-verified/D06.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** buenos días

**Respuesta:** Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica.

**Paso 1. Entrada:** ¿Qué hace el programa?

**Respuesta:** ¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la pregunta pendiente o termina la sesión.

**Paso 2. Entrada:** ¿Quién guarda los resultados?

**Respuesta:** El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos.

**Paso 3. Entrada:** dímelo

**Respuesta:** El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos.

**Paso 4. Entrada:** no entiendo, dilo de otra forma

**Respuesta:** Conservar un registro y presentar su resultado son responsabilidades diferentes.

**Paso 5. Entrada:** cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 6. Entrada:** confirmo: salida

**Respuesta:** La salida presenta un resultado comprensible: confirmación de registro aceptado o aviso de validación. Presentar ese resultado no añade por sí mismo otra operación de almacenamiento.

**Paso 7. Entrada:** continúa

**Respuesta:** La salida muestra un aviso cuando falta un campo requerido, sin afirmar que el registro fue guardado.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D07 — agua / oral_defense

Fuente: [D07.json](development-runs/2026-10-19-semantic-verified/D07.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** a los 99 grados

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 2. Entrada:** no sé justificarlo

**Respuesta:** Identifica primero qué magnitud describe la pregunta.

**Paso 3. Entrada:** y ahora?

**Respuesta:** Revisa qué condición del entorno acompaña a la temperatura en el material.

**Paso 4. Entrada:** puedes repetir?

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 5. Entrada:** no entiendo, dilo de otra forma

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 6. Entrada:** otra pista

**Respuesta:** Organiza tu justificación en magnitud, unidad y condición.

**Paso 7. Entrada:** siguiente pregunta

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D08 — agua / oral_defense

Fuente: [D08.json](development-runs/2026-10-19-semantic-verified/D08.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** A presión atmosférica

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 2. Entrada:** ¿Qué unidad debo justificar?

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 3. Entrada:** ayúdame

**Respuesta:** Identifica primero qué magnitud describe la pregunta.

**Paso 4. Entrada:** repite la pregunta

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 5. Entrada:** pon un ejemplo sin respuesta

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 6. Entrada:** otra forma

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 7. Entrada:** continuar

**Respuesta:** Revisa qué condición del entorno acompaña a la temperatura en el material.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D09 — agua / oral_defense

Fuente: [D09.json](development-runs/2026-10-19-semantic-verified/D09.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** La evaporación ocurre en la superficie

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 2. Entrada:** dame la solución

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 3. Entrada:** una pista

**Respuesta:** Identifica primero qué magnitud describe la pregunta.

**Paso 4. Entrada:** y ahora?

**Respuesta:** Revisa qué condición del entorno acompaña a la temperatura en el material.

**Paso 5. Entrada:** cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 6. Entrada:** confirmo: condensación

**Respuesta:** ¿Cómo explicarías el origen de gotas en la superficie de un vaso frío?

**Paso 7. Entrada:** repite

**Respuesta:** ¿Cómo explicarías el origen de gotas en la superficie de un vaso frío?

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D10 — programa / oral_defense

Fuente: [D10.json](development-runs/2026-10-19-semantic-verified/D10.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** La entrada recibe datos

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 2. Entrada:** no sé justificarlo

**Respuesta:** Identifica la operación que llega primero.

**Paso 3. Entrada:** ¿puedes ayudarme?

**Respuesta:** Distingue recibir un registro de decidir si cumple requisitos.

**Paso 4. Entrada:** repite

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 5. Entrada:** no entiendo la pregunta

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 6. Entrada:** otra pista

**Respuesta:** Explica qué recibe y entrega cada parte sin atribuirle funciones extra.

**Paso 7. Entrada:** siguiente

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D11 — programa / oral_defense

Fuente: [D11.json](development-runs/2026-10-19-semantic-verified/D11.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** El almacenamiento guarda resultados

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 2. Entrada:** compara los roles

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 3. Entrada:** eso

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 4. Entrada:** la pregunta de almacenamiento

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 5. Entrada:** otra forma

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 6. Entrada:** puedes repetir?

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 7. Entrada:** terminar la sesión

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## D12 — programa / oral_defense

Fuente: [D12.json](development-runs/2026-10-19-semantic-verified/D12.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** La validación rechaza datos inválidos

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 2. Entrada:** ¿Y si falta un campo?

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 3. Entrada:** ayuda

**Respuesta:** Identifica la operación que llega primero.

**Paso 4. Entrada:** repite la pregunta pendiente

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 5. Entrada:** otra pista

**Respuesta:** Distingue recibir un registro de decidir si cumple requisitos.

**Paso 6. Entrada:** cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 7. Entrada:** confirmo: salida

**Respuesta:** ¿Cómo harías que un aviso refleje lo que realmente ocurrió?

**Paso 8. Entrada:** seguir

**Respuesta:** Identifica el resultado que llega a la salida.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H01 — agua / self_study

Fuente: [W-H01.json](holdout-runs/2026-10-19-semantic-verified/W-H01.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Saludos, buenas noches

**Respuesta:** Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica.

**Paso 1. Entrada:** ¿A qué temperatura hierve el agua?

**Respuesta:** A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal.

**Paso 2. Entrada:** Repite la explicación

**Respuesta:** A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal.

**Paso 3. Entrada:** Compara con evaporación

**Respuesta:** La ebullición forma vapor en el volumen del líquido; la evaporación sucede en su superficie.

**Paso 4. Entrada:** Un ejemplo, por favor

**Respuesta:** Al calentar agua en una olla abierta se forman burbujas en el líquido cuando alcanza la ebullición en esas condiciones.

**Paso 5. Entrada:** Repite el ejemplo

**Respuesta:** Al calentar agua en una olla abierta se forman burbujas en el líquido cuando alcanza la ebullición en esas condiciones.

**Paso 6. Entrada:** Dilo de otra forma

**Respuesta:** La ebullición forma vapor en el volumen del líquido; la evaporación sucede en su superficie.

**Paso 7. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H02 — agua / self_study

Fuente: [W-H02.json](holdout-runs/2026-10-19-semantic-verified/W-H02.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Explicación guiada sobre condensación

**Respuesta:** La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie.

**Paso 1. Entrada:** Continúa

**Respuesta:** Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire.

**Paso 2. Entrada:** Repite el ejemplo

**Respuesta:** Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire.

**Paso 3. Entrada:** Compara con evaporación

**Respuesta:** La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor.

**Paso 4. Entrada:** Repite la comparación

**Respuesta:** La condensación pasa de vapor a líquido; la evaporación sigue la dirección de líquido a vapor.

**Paso 5. Entrada:** ¿Puedes ayudarme?

**Respuesta:** La condensación transforma vapor de agua en agua líquida. En el ejemplo del vaso frío, el vapor del aire puede formar gotas sobre su superficie.

**Paso 6. Entrada:** Continúa

**Respuesta:** Sobre la cara exterior de un vaso frío pueden aparecer gotas procedentes del vapor del aire.

**Paso 7. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H03 — agua / self_study

Fuente: [W-H03.json](holdout-runs/2026-10-19-semantic-verified/W-H03.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Voy a ensayar una exposición sobre congelación

**Respuesta:** La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio. En un recipiente que se enfría puede formarse hielo a partir del agua líquida. Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido.

**Paso 1. Entrada:** Repite la explicación

**Respuesta:** La congelación es el paso de agua líquida a sólida. El material usa un recipiente con agua que se enfría hasta formar hielo como ejemplo del cambio.

**Paso 2. Entrada:** Una comparación

**Respuesta:** Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido.

**Paso 3. Entrada:** Repite la comparación

**Respuesta:** Congelación y condensación tienen estados iniciales y finales distintos: líquido a sólido y vapor a líquido.

**Paso 4. Entrada:** Un ejemplo

**Respuesta:** En un recipiente que se enfría puede formarse hielo a partir del agua líquida.

**Paso 5. Entrada:** Repite el ejemplo

**Respuesta:** En un recipiente que se enfría puede formarse hielo a partir del agua líquida.

**Paso 6. Entrada:** Cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 7. Entrada:** confirmo: presión

**Respuesta:** Una temperatura aislada no identifica por sí sola las condiciones de ebullición. El material declara presión atmosférica y una temperatura aproximada; otra condición o una aproximación requiere aclaración antes de concluir que existe una discrepancia. Dos afirmaciones con temperaturas próximas pueden necesitar aclarar presión y aproximación antes de compararlas. Comparar valores bajo las mismas condiciones permite discutirlos; mezclar condiciones impide una comparación directa.

**Paso 8. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H04 — programa / self_study

Fuente: [W-H04.json](holdout-runs/2026-10-19-semantic-verified/W-H04.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Preguntas de práctica sobre validación

**Respuesta:** ¿Qué justificarías hacer cuando falta un campo requerido?

**Paso 1. Entrada:** Necesito una pista

**Respuesta:** Identifica qué requisito no se cumple.

**Paso 2. Entrada:** Repite la pista de la pregunta

**Respuesta:** Identifica qué requisito no se cumple.

**Paso 3. Entrada:** Falta un campo requerido

**Respuesta:** ¿Cómo explicarías el recorrido de un registro incompleto?

**Paso 4. Entrada:** Dilo de otra forma

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 5. Entrada:** Repite la pregunta

**Respuesta:** ¿Qué justificarías hacer cuando falta un campo requerido?

**Paso 6. Entrada:** Otra pista

**Respuesta:** Identifica qué requisito no se cumple.

**Paso 7. Entrada:** Dame la solución

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 8. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H05 — programa / self_study

Fuente: [W-H05.json](holdout-runs/2026-10-19-semantic-verified/W-H05.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** Quiero repasar salida

**Respuesta:** ¿Cómo harías que un aviso refleje lo que realmente ocurrió?

**Paso 1. Entrada:** Dame un ejemplo

**Respuesta:** La salida muestra un aviso cuando falta un campo requerido, sin afirmar que el registro fue guardado.

**Paso 2. Entrada:** Repite el ejemplo

**Respuesta:** La salida muestra un aviso cuando falta un campo requerido, sin afirmar que el registro fue guardado.

**Paso 3. Entrada:** Necesito una comparación

**Respuesta:** La salida comunica resultados; el almacenamiento conserva datos aceptados.

**Paso 4. Entrada:** Repite la comparación

**Respuesta:** La salida comunica resultados; el almacenamiento conserva datos aceptados.

**Paso 5. Entrada:** Repite la pregunta

**Respuesta:** ¿Cómo harías que un aviso refleje lo que realmente ocurrió?

**Paso 6. Entrada:** Una pista

**Respuesta:** Identifica el resultado que llega a la salida.

**Paso 7. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H06 — programa / self_study

Fuente: [W-H06.json](holdout-runs/2026-10-19-semantic-verified/W-H06.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** ¿Qué recibe la entrada?

**Respuesta:** En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo.

**Paso 1. Entrada:** Compara con validación

**Respuesta:** La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

**Paso 2. Entrada:** Repite la comparación

**Respuesta:** La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

**Paso 3. Entrada:** Cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 4. Entrada:** confirmo: almacenamiento

**Respuesta:** El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos.

**Paso 5. Entrada:** Un ejemplo

**Respuesta:** Un registro aceptado por validación se conserva en el almacenamiento local ficticio.

**Paso 6. Entrada:** Repite el ejemplo

**Respuesta:** Un registro aceptado por validación se conserva en el almacenamiento local ficticio.

**Paso 7. Entrada:** Dilo de otra forma

**Respuesta:** Conservar un registro y presentar su resultado son responsabilidades diferentes.

**Paso 8. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H07 — agua / oral_defense

Fuente: [W-H07.json](holdout-runs/2026-10-19-semantic-verified/W-H07.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** 99 grados Celsius a presión atmosférica

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 2. Entrada:** Repite la pregunta

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 3. Entrada:** Ayúdame

**Respuesta:** Identifica primero qué magnitud describe la pregunta.

**Paso 4. Entrada:** Repite la pista

**Respuesta:** Identifica primero qué magnitud describe la pregunta.

**Paso 5. Entrada:** Continúa

**Respuesta:** Revisa qué condición del entorno acompaña a la temperatura en el material.

**Paso 6. Entrada:** Dilo de otra forma

**Respuesta:** ¿Cómo justificarías una temperatura sin omitir las condiciones del entorno?

**Paso 7. Entrada:** Cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 8. Entrada:** confirmo: condensación

**Respuesta:** ¿Cómo explicarías el origen de gotas en la superficie de un vaso frío?

**Paso 9. Entrada:** El vapor forma gotas

**Respuesta:** ¿Qué cambio de estado justificaría las gotas del ejemplo?

**Paso 10. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H08 — agua / oral_defense

Fuente: [W-H08.json](holdout-runs/2026-10-19-semantic-verified/W-H08.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** Quiero cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 2. Entrada:** confirmo: congelación

**Respuesta:** ¿Qué estados necesitas identificar para describir la congelación?

**Paso 3. Entrada:** Necesito una pista

**Respuesta:** Nombra lo que hay antes del cambio.

**Paso 4. Entrada:** Repite la pista

**Respuesta:** Nombra lo que hay antes del cambio.

**Paso 5. Entrada:** Dilo de otra forma

**Respuesta:** ¿Cómo describirías el antes y el después del cambio a hielo?

**Paso 6. Entrada:** Un ejemplo sin solución

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 7. Entrada:** Siguiente

**Respuesta:** Nombra lo que observas después.

**Paso 8. Entrada:** Repite la pregunta

**Respuesta:** ¿Qué estados necesitas identificar para describir la congelación?

**Paso 9. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H09 — agua / oral_defense

Fuente: [W-H09.json](holdout-runs/2026-10-19-semantic-verified/W-H09.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?

**Paso 1. Entrada:** La evaporación ocurre en la superficie

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 2. Entrada:** confirmo: evaporación

**Respuesta:** ¿Cómo distinguirías evaporación y ebullición en una situación cotidiana?

**Paso 3. Entrada:** Repite la pregunta

**Respuesta:** ¿Cómo distinguirías evaporación y ebullición en una situación cotidiana?

**Paso 4. Entrada:** No sé justificarlo

**Respuesta:** Describe primero lo que observas.

**Paso 5. Entrada:** Repite la pista

**Respuesta:** Describe primero lo que observas.

**Paso 6. Entrada:** Dame la solución

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 7. Entrada:** Continúa

**Respuesta:** Separa el lugar del cambio y las condiciones del líquido.

**Paso 8. Entrada:** Dilo de otra forma

**Respuesta:** ¿En qué te fijarías para justificar cuál de los dos procesos ocurre?

**Paso 9. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H10 — programa / oral_defense

Fuente: [W-H10.json](holdout-runs/2026-10-19-semantic-verified/W-H10.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** La validación escribe registros en disco

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 2. Entrada:** Repite la pregunta

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 3. Entrada:** Dame una pista

**Respuesta:** Identifica la operación que llega primero.

**Paso 4. Entrada:** Repite la pista

**Respuesta:** Identifica la operación que llega primero.

**Paso 5. Entrada:** Compara los roles

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 6. Entrada:** Continúa

**Respuesta:** Distingue recibir un registro de decidir si cumple requisitos.

**Paso 7. Entrada:** Cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 8. Entrada:** confirmo: salida

**Respuesta:** ¿Cómo harías que un aviso refleje lo que realmente ocurrió?

**Paso 9. Entrada:** Muestra el resultado del registro

**Respuesta:** ¿Qué comprobarías antes de anunciar que un registro está guardado?

**Paso 10. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H11 — programa / oral_defense

Fuente: [W-H11.json](holdout-runs/2026-10-19-semantic-verified/W-H11.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** Cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 2. Entrada:** confirmo: almacenamiento

**Respuesta:** ¿Qué condición justificarías antes de conservar un registro?

**Paso 3. Entrada:** Se guarda antes de validar

**Respuesta:** ¿Cómo explicarías qué registros pueden llegar a almacenamiento?

**Paso 4. Entrada:** Necesito una pista

**Respuesta:** Ubica el almacenamiento en el recorrido.

**Paso 5. Entrada:** Repite la pista

**Respuesta:** Ubica el almacenamiento en el recorrido.

**Paso 6. Entrada:** Otra pista

**Respuesta:** Identifica la comprobación previa declarada.

**Paso 7. Entrada:** Repite la pregunta

**Respuesta:** ¿Qué condición justificarías antes de conservar un registro?

**Paso 8. Entrada:** Dilo de otra forma

**Respuesta:** ¿Cómo explicarías qué registros pueden llegar a almacenamiento?

**Paso 9. Entrada:** Quiero terminar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.

## W-H12 — programa / oral_defense

Fuente: [W-H12.json](holdout-runs/2026-10-19-semantic-verified/W-H12.json). Revisión humana: **No evaluado**.

**Paso 0. Entrada:** 

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 1. Entrada:** Repite la pregunta

**Respuesta:** ¿Cómo justificarías separar recepción y validación?

**Paso 2. Entrada:** No quiero cambiar de tema; dame una pista

**Respuesta:** Identifica la operación que llega primero.

**Paso 3. Entrada:** Repite la pista

**Respuesta:** Identifica la operación que llega primero.

**Paso 4. Entrada:** Otra pista

**Respuesta:** Distingue recibir un registro de decidir si cumple requisitos.

**Paso 5. Entrada:** Dilo de otra forma

**Respuesta:** ¿Qué responsabilidad atribuyes a cada parte al recibir un registro?

**Paso 6. Entrada:** No repitas, compara

**Respuesta:** El material vigente no incluye ese apoyo para este objetivo. Puedes elegir otro tema disponible, pedir una pregunta o terminar.

**Paso 7. Entrada:** Quiero cambiar de tema

**Respuesta:** Confirma el nuevo tema para cambiar de objetivo o pide continuar con la pregunta pendiente.

**Paso 8. Entrada:** confirmo: validación

**Respuesta:** ¿Qué justificarías hacer cuando falta un campo requerido?

**Paso 9. Entrada:** Falta un campo

**Respuesta:** ¿Cómo explicarías el recorrido de un registro incompleto?

**Paso 10. Entrada:** Seguir

**Respuesta:** Identifica qué requisito no se cumple.

**Paso 11. Entrada:** Finalizar

**Respuesta:** La sesión ha terminado. La conservación se aplica únicamente conforme a tu elección y la política de esta actividad.

Resultado de los seis criterios: No evaluado. Correcciones propuestas por la persona revisora: pendientes.



Revisión humana organizada en [seis bloques de cuatro diálogos](human-review-blocks/README.md). Responder por bloque con IDs aceptables o caso/paso/motivo de corrección; no se atribuye aprobación por continuar. La selección de temas junto a la conversación es una mejora de interfaz: no modifica los textos de las transcripciones API ni convierte avisos en prueba de utilidad.
