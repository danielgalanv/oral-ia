# Guion final: preguntas y respuestas reales

29-10-2026. Captura de API durante interacción en navegador. Texto del modelo sin reescritura. Revisión docente diagnóstica, no publicación para estudiantes.

## 1. ¿Qué diferencia hay entre verificar y validar los requisitos? Explícamelo de forma sencilla.

Estado: prepared_unverified.

La diferencia entre verificar y validar los requisitos radica en el enfoque y los aspectos que se evalúan.

**Verificar los requisitos** implica asegurarse de que cada requisito cumpla con ciertos criterios de calidad individuales. Esto incluye:

- **Comprensibilidad**: que el requisito esté redactado de manera clara y fácil de entender.
- **No ambigüedad**: que el requisito pueda interpretarse de una única manera.
- **Gramática y ortografía**: que estén correctamente escritos.
- **Realizabilidad**: que sea posible implementar el requisito con tecnologías existentes y dentro de un costo razonable.
- **Comprobabilidad**: que se puedan definir pruebas para verificar el cumplimiento del requisito de manera práctica.
- **Trazabilidad**: que el requisito esté relacionado adecuadamente con otros requisitos o casos de uso.

Por ejemplo, si tienes un requisito que dice "El sistema debe permitir a los usuarios buscar libros por título", verificar este requisito implicaría asegurarte de que está claro, no tiene ambigüedades, está bien escrito, es técnicamente factible, se puede probar fácilmente y está relacionado con otros requisitos relevantes.

**Validar los requisitos**, por otro lado, implica asegurarse de que los requisitos en conjunto sean adecuados y satisfagan los objetivos del proyecto. Esto incluye:

- **Consistencia**: que los requisitos no contengan contradicciones ni redundancias.
- **Complejidad**: que todos los requisitos necesarios estén incluidos.
- **Realismo**: que los requisitos sean factibles desde una perspectiva técnica y organizacional.
- **Verificabilidad**: que los requisitos puedan ser probados de manera efectiva.
- **Trazabilidad**: que los requisitos estén correctamente relacionados con otros documentos del proyecto.

Por ejemplo, si tienes un conjunto de requisitos para un sistema de gestión de biblioteca, validar estos requisitos implicaría asegurarte de que todos los requisitos juntos cubran todas las funcionalidades necesarias (como buscar libros, prestar libros, etc.), que no haya contradicciones entre ellos, que sean factibles de implementar y que puedan ser probados de manera efectiva.

En resumen, verificar se centra en la calidad individual de cada requisito, mientras que validar se enfoca en la integridad y adecuación del conjunto de requisitos en relación con los objetivos del proyecto.

### Fuentes recibidas

- 6 - Procedimiento requisitos.pdf, página 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 74: Requirements validation techniques
- 5 - Requisitos.pdf, página 89: Key points
- 6 - Procedimiento requisitos.pdf, página 10: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 76: Review checks

## 2. Ponme un ejemplo con una aplicación para pedir cita médica.

Estado: prepared_unverified.

Para ilustrar la diferencia entre verificar y validar los requisitos utilizando una aplicación para pedir citas médicas, consideremos los siguientes ejemplos:

### Verificar los requisitos

Supongamos que uno de los requisitos de la aplicación es:
"El sistema debe permitir a los usuarios buscar citas médicas por nombre del paciente."

**Verificar este requisito** implicaría asegurarse de que cumple con los criterios de calidad individuales:

- **Comprensible**: El requisito está claro y fácil de entender.
- **No ambiguo**: No puede interpretarse de diferentes maneras.
- **Gramaticalmente correcto**: Está bien redactado.
- **Ortográficamente correcto**: No tiene errores de ortografía.
- **Realizable**: Es posible implementarlo con las tecnologías disponibles y dentro de un costo razonable.
- **Comprobable**: Se pueden definir pruebas para verificar que el requisito se cumple correctamente.
- **Trazado**: El requisito está relacionado adecuadamente con otros requisitos o casos de uso.

Por ejemplo, si el requisito fuera "El sistema debe permitir a los usuarios buscar citas médicas por nombre del paciente", verificarlo implicaría asegurarse de que está bien redactado, no tiene ambigüedades, es técnicamente factible, se puede probar fácilmente y está relacionado con otros requisitos relevantes.

### Validar los requisitos

Ahora, **validar los requisitos** implicaría asegurarse de que el conjunto de requisitos en su totalidad cumple con los objetivos del proyecto. Por ejemplo, si tenemos varios requisitos relacionados con la búsqueda de citas médicas, validarlos implicaría:

- **Consistencia**: Que no haya contradicciones entre los requisitos. Por ejemplo, si uno de los requisitos dice que el sistema debe permitir buscar citas por nombre del paciente, y otro requisito dice que no debe permitir buscar por nombre, esto sería una contradicción.
- **Complejidad**: Que todos los requisitos necesarios estén incluidos. Por ejemplo, si falta un requisito que permita buscar citas por fecha, esto podría ser una omisión importante.
- **Realismo**: Que los requisitos sean factibles desde una perspectiva técnica y organizacional. Por ejemplo, si el requisito es buscar citas por nombre del paciente, pero no se cuenta con la infraestructura para almacenar y buscar nombres de pacientes, esto sería poco realista.
- **Verificabilidad**: Que los requisitos puedan ser probados de manera efectiva. Por ejemplo, si el requisito es buscar citas por nombre del paciente, se deben poder definir pruebas para verificar que esta funcionalidad funciona correctamente.
- **Trazabilidad**: Que los requisitos estén correctamente relacionados con otros documentos del proyecto. Por ejemplo, si el requisito de buscar citas por nombre del paciente está relacionado con el caso de uso de "Buscar citas médicas".

Por ejemplo, si tenemos un conjunto de requisitos para una aplicación de citas médicas, validar estos requisitos implicaría asegurarse de que todos los requisitos juntos cubren todas las funcionalidades necesarias (como buscar citas por nombre del paciente, por fecha, etc.), que no haya contradicciones entre ellos, que sean factibles de implementar y que puedan ser probados de manera efectiva.

En resumen, verificar se centra en la calidad individual de cada requisito, mientras que validar se enfoca en la integridad y adecuación del conjunto de requisitos en relación con los objetivos del proyecto.

### Fuentes recibidas

- 6 - Procedimiento requisitos.pdf, página 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 74: Requirements validation techniques
- 5 - Requisitos.pdf, página 13: Requirements imprecision
- 5 - Requisitos.pdf, página 89: Key points
- 6 - Procedimiento requisitos.pdf, página 10: Verificar la calidad de los requisitos del sistema

## 3. No entiendo la diferencia en ese ejemplo. Explícamela con otras palabras.

Estado: prepared_unverified.

Claro, veamos la diferencia entre verificar y validar los requisitos utilizando un ejemplo con una aplicación para pedir citas médicas.

### Verificar los requisitos

Cuando verificamos un requisito, nos aseguramos de que cumpla con ciertos criterios de calidad individuales. Por ejemplo, consideremos el siguiente requisito:

"El sistema debe permitir a los usuarios buscar citas médicas por nombre del paciente."

**Verificar este requisito** implicaría asegurarnos de que:

- **Es comprensible**: El requisito está claro y fácil de entender.
- **No es ambiguo**: No puede interpretarse de diferentes maneras.
- **Está gramaticalmente correcto**: Está bien redactado.
- **Está ortográficamente correcto**: No tiene errores de ortografía.
- **Es realizable**: Es posible implementarlo con las tecnologías disponibles y dentro de un costo razonable.
- **Es comprobable**: Se pueden definir pruebas para verificar que el requisito se cumple correctamente.
- **Está trazado**: El requisito está relacionado adecuadamente con otros requisitos o casos de uso.

Por ejemplo, si el requisito "El sistema debe permitir a los usuarios buscar citas médicas por nombre del paciente" está bien redactado, no tiene ambigüedades, es técnicamente factible, se puede probar fácilmente y está relacionado con otros requisitos relevantes, entonces lo consideramos verificado.

### Validar los requisitos

Al validar los requisitos, nos aseguramos de que el conjunto de requisitos en su totalidad cumple con los objetivos del proyecto. Por ejemplo, si tenemos varios requisitos relacionados con la búsqueda de citas médicas, validarlos implicaría:

- **Consistencia**: Que no haya contradicciones entre los requisitos. Por ejemplo, si uno de los requisitos dice que el sistema debe permitir buscar citas por nombre del paciente, y otro requisito dice que no debe permitir buscar por nombre, esto sería una contradicción.
- **Complejidad**: Que todos los requisitos necesarios estén incluidos. Por ejemplo, si falta un requisito que permita buscar citas por fecha, esto podría ser una omisión importante.
- **Realismo**: Que los requisitos sean factibles desde una perspectiva técnica y organizacional. Por ejemplo, si el requisito es buscar citas por nombre del paciente, pero no se cuenta con la infraestructura para almacenar y buscar nombres de pacientes, esto sería poco realista.
- **Verificabilidad**: Que los requisitos puedan ser probados de manera efectiva. Por ejemplo, si el requisito es buscar citas por nombre del paciente, se deben poder definir pruebas para verificar que esta funcionalidad funciona correctamente.
- **Trazabilidad**: Que los requisitos estén correctamente relacionados con otros documentos del proyecto. Por ejemplo, si el requisito de buscar citas por nombre del paciente está relacionado con el caso de uso de "Buscar citas médicas".

Por ejemplo, si tenemos un conjunto de requisitos para una aplicación de citas médicas, validar estos requisitos implicaría asegurarse de que todos los requisitos juntos cubren todas las funcionalidades necesarias (como buscar citas por nombre del paciente, por fecha, etc.), que no haya contradicciones entre ellos, que sean factibles de implementar y que puedan ser probados de manera efectiva.

En resumen, verificar se centra en la calidad individual de cada requisito, mientras que validar se enfoca en la integridad y adecuación del conjunto de requisitos en relación con los objetivos del proyecto.

### Fuentes recibidas

- 6 - Procedimiento requisitos.pdf, página 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 74: Requirements validation techniques
- 5 - Requisitos.pdf, página 13: Requirements imprecision
- 5 - Requisitos.pdf, página 89: Key points
- nasa-handbook.pdf, página 208: Appendix C: How to Write a Good Requirement— Checklist

## 4. ¿Cómo podría comprobar que una cita se reserva correctamente?

Estado: prepared_unverified.

Para comprobar que una cita se reserva correctamente en una aplicación de citas médicas, debes asegurarte de que el proceso de reserva cumpla con ciertos criterios de calidad y funcionalidad. Aquí te explico cómo podrías hacerlo:

### Verificar los requisitos

Cuando verificas un requisito específico, te aseguras de que cumpla con los criterios de calidad individuales. Por ejemplo, considera el requisito:

"El sistema debe permitir a los usuarios reservar citas médicas correctamente."

**Verificar este requisito** implicaría asegurarte de que:

- **Es comprensible**: El requisito está claro y fácil de entender.
- **No es ambiguo**: No puede interpretarse de diferentes maneras.
- **Está gramaticalmente correcto**: Está bien redactado.
- **Está ortográficamente correcto**: No tiene errores de ortografía.
- **Es realizable**: Es posible implementarlo con las tecnologías disponibles y dentro de un costo razonable.
- **Es comprobable**: Se pueden definir pruebas para verificar que el requisito se cumple correctamente.
- **Está trazado**: El requisito está relacionado adecuadamente con otros requisitos o casos de uso.

Por ejemplo, si el requisito "El sistema debe permitir a los usuarios reservar citas médicas correctamente" está bien redactado, no tiene ambigüedades, es técnicamente factible, se puede probar fácilmente y está relacionado con otros requisitos relevantes, entonces lo consideramos verificado.

### Validar los requisitos

Al validar los requisitos, te aseguras de que el conjunto de requisitos en su totalidad cumple con los objetivos del proyecto. Por ejemplo, si tienes varios requisitos relacionados con la reserva de citas médicas, validarlos implicaría:

- **Consistencia**: Que no haya contradicciones entre los requisitos. Por ejemplo, si uno de los requisitos dice que el sistema debe permitir reservar citas médicas, y otro requisito dice que no debe permitir reservar citas, esto sería una contradicción.
- **Complejidad**: Que todos los requisitos necesarios estén incluidos. Por ejemplo, si falta un requisito que permita reservar citas por fecha, esto podría ser una omisión importante.
- **Realismo**: Que los requisitos sean factibles desde una perspectiva técnica y organizacional. Por ejemplo, si el requisito es reservar citas médicas, pero no se cuenta con la infraestructura para gestionar citas, esto sería poco realista.
- **Verificabilidad**: Que los requisitos puedan ser probados de manera efectiva. Por ejemplo, si el requisito es reservar citas médicas, se deben poder definir pruebas para verificar que esta funcionalidad funciona correctamente.
- **Trazabilidad**: Que los requisitos estén correctamente relacionados con otros documentos del proyecto. Por ejemplo, si el requisito de reservar citas médicas está relacionado con el caso de uso de "Reservar citas médicas".

Por ejemplo, si tienes un conjunto de requisitos para una aplicación de citas médicas, validar estos requisitos implicaría asegurarse de que todos los requisitos juntos cubren todas las funcionalidades necesarias (como reservar citas médicas por fecha, por médico, etc.), que no haya contradicciones entre ellos, que sean factibles de implementar y que puedan ser probados de manera efectiva.

En resumen, verificar se centra en la calidad individual de cada requisito, mientras que validar se enfoca en la integridad y adecuación del conjunto de requisitos en relación con los objetivos del proyecto.

### Fuentes recibidas

- 5 - Requisitos.pdf, página 13: Requirements imprecision
- nasa-handbook.pdf, página 210: Appendix C: How to Write a Good Requirement— Checklist
- 6 - Procedimiento requisitos.pdf, página 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 61: Interviews in practice
- 7 - Modelos.pdf, página 38: Tabular description of the ‘Transfer data’ use-case

## 5. ¿Qué significa que un requisito sea realizable y comprobable? ¿Es lo mismo?

Estado: prepared_unverified.

Un requisito debe ser tanto realizable como comprobable, pero estos dos términos tienen significados distintos y no son necesariamente lo mismo.

**Realizable**: Un requisito es realizable si puede ser implementado utilizando tecnología existente y dentro de un costo razonable. Esto implica que el requisito no debe ser tan avanzado o complejo que no pueda ser cumplido con los recursos disponibles. Por ejemplo, si se requiere que un software pueda procesar datos en tiempo real, este requisito sería realizable si existe tecnología disponible y suficiente presupuesto para desarrollarla.

**Comprobable**: Un requisito es comprobable si se puede verificar después de que el producto final ha sido implementado. Esto significa que debe estar claramente definido cómo se va a probar que el requisito se ha cumplido. Por ejemplo, si se requiere que un sistema de seguridad funcione correctamente en un 99% de los casos, esto es comprobable porque se puede establecer una prueba que muestre que el sistema cumple con esta especificación.

En resumen, un requisito realizable asegura que el objetivo puede ser alcanzado con los recursos disponibles, mientras que un requisito comprobable garantiza que se puede verificar que el objetivo ha sido alcanzado. Ambos son importantes para asegurar que los requisitos sean viables y efectivos en la práctica.

### Fuentes recibidas

- nasa-handbook.pdf, página 70: NASA §4.2 Technical Requirements Definition
- 6 - Procedimiento requisitos.pdf, página 11: Verificar la calidad de los requisitos del sistema
- nasa-handbook.pdf, página 208: Appendix C: How to Write a Good Requirement— Checklist

## 6. Dame un ejemplo de un requisito realizable pero difícil de comprobar.

Estado: prepared_unverified.

Un requisito puede ser realizable pero difícil de comprobar. Aquí tienes un ejemplo hipotético que ilustra esta situación:

**Ejemplo:**

Supongamos que estás desarrollando un sistema de reconocimiento facial para controlar el acceso a una instalación. Uno de los requisitos podría ser:

**Requisito:** El sistema debe identificar correctamente al menos el 95% de los usuarios registrados en un período de uso normal.

Este requisito es **realizable** porque, con la tecnología actual en reconocimiento facial, es técnicamente posible diseñar un sistema que logre una tasa de identificación del 95%. Sin embargo, este requisito puede ser **difícil de comprobar** debido a varios factores:

1. **Muestra de pruebas insuficiente:** Para verificar que el sistema cumple con el requisito, se necesita una muestra representativa de todos los usuarios registrados. Si la muestra de pruebas es pequeña o no representa adecuadamente a todos los usuarios, puede ser difícil determinar si el sistema cumple con el requisito.

2. **Variables ambientales:** El rendimiento del sistema puede variar según las condiciones ambientales, como la iluminación, la distancia entre la cámara y el usuario, y la presencia de objetos que puedan interferir con la imagen capturada. Estas variables pueden hacer que sea difícil establecer una prueba única y consistente para verificar el requisito.

3. **Definición de "uso normal":** El término "uso normal" puede ser subjetivo y difícil de definir con precisión. Esto hace que sea complicado establecer un marco de referencia claro para medir el rendimiento del sistema.

Por lo tanto, aunque el requisito es técnicamente posible de implementar (realizable), puede ser difícil establecer una prueba objetiva y consistente para verificar que el sistema cumple con él (comprobable).

Este ejemplo demuestra que un requisito puede ser realizable desde una perspectiva técnica, pero puede presentar desafíos significativos en términos de cómo se puede verificar su cumplimiento de manera efectiva y precisa.

### Fuentes recibidas

- nasa-handbook.pdf, página 209: Appendix C: How to Write a Good Requirement— Checklist
- Ch4 Req Eng.pptx, página 76: Review checks
- 5 - Requisitos.pdf, página 20: Goals and requirements
- nasa-handbook.pdf, página 208: Appendix C: How to Write a Good Requirement— Checklist

