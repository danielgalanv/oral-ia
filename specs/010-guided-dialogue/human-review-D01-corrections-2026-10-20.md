# Revisión humana D01: correcciones solicitadas

Fuente: observaciones explícitas del usuario durante la revisión interactiva de D01 completo. Esta revisión parcial no aprueba los otros diálogos ni la feature.

## Resultado humano registrado

**D01 requiere corrección.** El usuario indica que ORALIA debe atender al texto de entrada, corresponder al saludo, mantener contexto, cambiar la explicación cuando se repite una duda, distinguir qué/por qué/cómo, explicar adecuadamente cómo se evapora el agua y utilizar recursos didácticos. Considera demasiado sintéticas las respuestas y señala que un ejemplo específico no sustituye una contestación general a si el agua puede pasar a vapor.

La observación se formuló sobre el D01 previo (pasos 0–6). La transcripción posterior human-system-review-screenless-current.md conserva los problemas en pasos 1–7: no saluda; trata consulta amplia como referencia insegura; definición en lugar de mecanismo en paso7; ejemplo aislado en paso6. Esta comparación posterior es auditoría de IA, no una nueva decisión humana ni aprobación de la versión posterior.

| Hallazgo | Ejecución anterior / sin pantalla | Criterio observable de corrección |
|---|---|---|
| No corresponder a «hola» | paso0 / paso1 | saludo breve y natural seguido de orientación verbal pertinente |
| Consulta amplia tratada como ambigüedad de referencia | paso1 / paso2 | reconocer la petición general, orientar con alcance/material disponible y opciones concretas; no declarar referencia insegura por defecto |
| Preguntas distintas reciben misma definición | paso6 / paso7 | distinguir definición, causa, proceso, condición/cantidad o posibilidad usando la frase completa y el contexto; responder al propósito |
| Repetición de duda sin cambio didáctico suficiente | pasos3–6 / pasos4–7 | conservar tema y cambiar estrategia de explicación cuando la repetición indica duda; ofrecer aclaración si la necesidad no es inequívoca |
| Respuesta de posibilidad reducida a un ejemplo | paso5 / paso6 | contestar primero de forma directa y cubrir el alcance sustentado; usar ejemplo después como apoyo, no como sustituto de la explicación |
| Excesiva síntesis sin método | conjunto | profundidad proporcional a petición: secuencia, enumeración oral, contraste o ejemplo con conexión explícita; sin alargar por alargar |

## Límites y negativos

- Repetición literal explícita debe seguir siendo fiel; no imponer una paráfrasis si se pide repetir exactamente. «Dímelo» requiere contexto y no equivale siempre a pedir una explicación nueva.
- No clasificar solo por palabras sueltas: «cómo se llama», interrogaciones indirectas, negación y preguntas combinadas requieren atender al significado completo. Añadir variantes no usadas para ajustar reglas.
- Explicar evaporación no debe excluir ebullición cuando la pregunta general abarca paso de líquido a vapor; distinguir procesos/condiciones solo hasta donde las fuentes autorizadas los sustenten. Preparar unidades docentes explicativas revisadas si falta contenido, en vez de inventar conocimiento o usar un límite genérico como prueba de suficiencia.
- Formato hablado: pasos cortos, enumeraciones escuchables, ejemplos relevantes y comprobación neutral de si se necesita ampliar; sin dependencia de pantalla, lectura de IDs o comandos rígidos como única forma de hablar.
- Mantener independencia de autorización/fuentes, no revelación de solución, privacidad y presupuestos. Las pruebas de pertinencia y didáctica deben poder fallar aunque pase la autorización técnica.

## Seguimiento

SpecKit debe convertir los hallazgos en criterios/tareas verificables, conservar el corpus y resultados anteriores, corregir e incorporar reserva nueva conforme protocolo. Presentar D01 completo corregido para nueva revisión humana; no repetir solicitudes de aprobar textos que conservan los defectos ya comunicados. Audio real, utilidad G3 y pérdida histórica siguen siendo asuntos independientes.
