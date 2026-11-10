# Preguntas y respuestas reales — GPU
Sin evaluación del alumno.

## A1

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: prepared_unverified

Un requisito de software es una característica o capacidad que el sistema debe poseer o realizar para satisfacer las necesidades de los usuarios y cumplir con los objetivos de negocio. Estos requisitos pueden clasificarse en varios tipos:

1. **Requisitos funcionales**: describen las acciones específicas que el sistema debe realizar. Por ejemplo, en una aplicación bancaria, un requisito funcional podría ser "el sistema debe permitir a los usuarios consultar su saldo".

2. **Requisitos no funcionales**: describen las características de calidad del sistema, como la seguridad, la usabilidad, la eficiencia, entre otras. Por ejemplo, un requisito no funcional podría ser "la aplicación debe estar segura contra accesos no autorizados".

3. **Requisitos de integración**: describen con qué otros sistemas o servicios debe interactuar el sistema. Por ejemplo, "el sistema debe integrarse con el servicio de pago para procesar transacciones".

4. **Requisitos de dominio**: describen restricciones tecnológicas o legales que el sistema debe cumplir. Por ejemplo, "el sistema debe cumplir con las regulaciones de protección de datos personales".

### Ejemplo Sencillo

Imagina que estás creando una aplicación de gestión de tareas para un equipo de trabajo. Aquí tienes algunos ejemplos de diferentes tipos de requisitos:

- **Requisito funcional**: "La aplicación debe permitir a los usuarios crear nuevas tareas".
  
- **Requisito no funcional**: "La aplicación debe ser fácil de usar y tener una interfaz intuitiva".
  
- **Requisito de integración**: "La aplicación debe integrarse con el calendario del usuario para sincronizar las tareas programadas".
  
- **Requisito de dominio**: "La aplicación debe cumplir con las normativas de privacidad de datos".

Estos requisitos ayudan a definir claramente lo que el sistema debe hacer y cómo debe hacerlo, asegurando que cumpla con las necesidades de los usuarios y los objetivos de negocio.

## A2

No he entendido bien la diferencia entre un requisito funcional y uno no funcional. ¿Puedes explicármela de otra manera?

Estado: prepared_unverified

Un requisito de software puede dividirse en dos categorías principales: los requisitos funcionales y los requisitos no funcionales. La principal diferencia entre ambos radica en lo que describen:

- **Requisitos funcionales** se refieren a las acciones específicas que el sistema debe realizar. Son aquellas características que describen lo que el sistema debe hacer para cumplir con las necesidades del usuario. Por ejemplo, en una aplicación de gestión de tareas, un requisito funcional podría ser "el sistema debe permitir a los usuarios crear nuevas tareas". Este requisito especifica una acción concreta que el sistema debe poder realizar.

- **Requisitos no funcionales**, por otro lado, describen las características de calidad del sistema, como su rendimiento, seguridad, usabilidad, eficiencia, entre otros aspectos. Estos requisitos no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo o cómo debe ser. Por ejemplo, un requisito no funcional podría ser "la aplicación debe ser segura contra accesos no autorizados". Este requisito no especifica una acción concreta, sino una propiedad del sistema que debe cumplir.

Para ilustrar esta diferencia con un ejemplo sencillo, imagina que estás diseñando una aplicación de control de temperatura para un hogar inteligente:

- Un requisito funcional sería "la aplicación debe permitir ajustar la temperatura de la casa". Esto significa que el sistema debe tener la capacidad de cambiar la temperatura según lo desee el usuario.

- Un requisito no funcional sería "la aplicación debe ser capaz de mantener la temperatura constante durante períodos prolongados". Este requisito no describe una acción específica, sino una característica del sistema que debe cumplir, relacionada con su capacidad para mantener la temperatura estable.

Espero que esto ayude a clarificar la diferencia entre estos dos tipos de requisitos.

## A3

Ponme un requisito funcional para una aplicación de reserva de citas y explica por qué lo es.

Estado: prepared_unverified

Un requisito funcional es una característica específica que el sistema debe cumplir para satisfacer las necesidades del usuario. En el caso de una aplicación de reserva de citas, un requisito funcional podría ser:

"La aplicación debe permitir a los usuarios reservar una cita con un profesional específico en una fecha y hora determinadas."

Este requisito es funcional porque describe una acción concreta que el sistema debe realizar: permitir a los usuarios reservar citas. Específicamente, el sistema debe proporcionar la funcionalidad para que un usuario pueda seleccionar un profesional, una fecha y una hora disponibles, y reservar una cita con él.

Este requisito cumple con los criterios de un requisito funcional porque:
- Describe una acción específica que el sistema debe realizar.
- Es algo que el usuario puede hacer a través de la aplicación.
- Permite medir si el sistema está funcionando correctamente, ya que se puede verificar si los usuarios pueden efectivamente reservar citas.

Por ejemplo, para comprobar si este requisito funcional se cumple, podrías probar la aplicación realizando una reserva de cita. Si el usuario puede seleccionar un profesional, una fecha y una hora disponibles, y la cita se reserva correctamente, entonces el requisito funcional se ha cumplido.

## A4

Pon otro ejemplo del mismo tipo, distinto del anterior.

Estado: prepared_unverified

Otro ejemplo de un requisito funcional para una aplicación de reserva de citas podría ser:

"La aplicación debe permitir a los usuarios cancelar una cita previamente reservada."

Este requisito es funcional porque describe una acción específica que el sistema debe realizar: permitir a los usuarios cancelar citas que han reservado antes. Específicamente, el sistema debe proporcionar la funcionalidad para que un usuario pueda seleccionar una cita previamente reservada y proceder a cancelarla.

Este requisito cumple con los criterios de un requisito funcional porque:
- Describe una acción específica que el sistema debe realizar.
- Es algo que el usuario puede hacer a través de la aplicación.
- Permite medir si el sistema está funcionando correctamente, ya que se puede verificar si los usuarios pueden efectivamente cancelar citas que han reservado antes.

Para comprobar si este requisito funcional se cumple, podrías probar la aplicación realizando la cancelación de una cita que se haya reservado previamente. Si el usuario puede seleccionar una cita previamente reservada y proceder a cancelarla, entonces el requisito funcional se ha cumplido.

## B1

En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?

Estado: prepared_unverified

La propuesta de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos es un requisito no funcional. Este tipo de requisito se refiere a las características del sistema que no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo o cómo debe comportarse. Según la tabla de métricas para especificar requisitos no funcionales en la fuente proporcionada, la velocidad es uno de los aspectos que se pueden medir para especificar estos requisitos. La velocidad puede incluir el tiempo de respuesta del usuario o el tiempo de respuesta a eventos, que en este caso sería el tiempo que tarda el sistema en procesar una solicitud de búsqueda y devolver una respuesta.

Este requisito específico de velocidad se relaciona con la propiedad de "Speed" (Velocidad) en la tabla de métricas, donde se menciona el "User/event response time" (Tiempo de respuesta del usuario/a evento). Por lo tanto, el requisito de que la búsqueda responda en menos de 0,3 segundos es un requisito no funcional que especifica un límite de tiempo para la respuesta del sistema a una solicitud de búsqueda, asegurando que sea rápida y eficiente desde la perspectiva del usuario.

## B2

¿Cómo comprobaríamos que se cumple ese requisito? Explícame qué haríamos y qué observaríamos.

Estado: prepared_unverified

Para comprobar que la búsqueda en una aplicación de reservas responde en menos de 0,3 segundos, se deben seguir los siguientes pasos:

1. **Preparación**: Configurar un entorno de prueba adecuado que simule las condiciones de uso real. Esto incluye tener una base de datos con datos representativos de los que se encontrarían en producción, así como un servidor y una red configurados para reflejar las condiciones típicas de uso.

2. **Ejecución de pruebas**: Realizar múltiples búsquedas en la aplicación de reservas utilizando diferentes términos de búsqueda y en diferentes momentos de carga del sistema. Esto ayuda a garantizar que la aplicación cumple con el requisito en una variedad de situaciones.

3. **Medición del tiempo de respuesta**: Utilizar herramientas de medición de rendimiento para registrar el tiempo que tarda la aplicación en responder a cada solicitud de búsqueda. Estas herramientas pueden ser integradas en la aplicación o utilizarse desde fuera, como navegadores web con extensiones de medición de tiempo de respuesta, o herramientas de pruebas automatizadas.

4. **Análisis de resultados**: Analizar los tiempos de respuesta registrados para determinar si cumplen con el requisito de ser menores a 0,3 segundos. Si todos los tiempos de respuesta cumplen con este requisito, entonces se puede considerar que el requisito se ha cumplido.

5. **Replicabilidad**: Repetir las pruebas varias veces para asegurar que los resultados no son producto de condiciones atípicas o fluctuaciones temporales. Esto implica realizar pruebas durante diferentes momentos del día y bajo diferentes cargas de trabajo.

6. **Documentación**: Registrar todos los detalles de las pruebas, incluyendo el entorno de prueba, los términos de búsqueda utilizados, los tiempos de respuesta medidos y cualquier otra información relevante. Esta documentación será útil para la auditoría y para futuras revisiones del requisito.

Estos pasos aseguran que el requisito de velocidad se cumple de manera consistente y que se puede demostrar de manera objetiva que la aplicación de reservas responde a las solicitudes de búsqueda en menos de 0,3 segundos.

## B3

Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?

Estado: prepared_unverified

La capacidad de medir si una aplicación de reservas responde a las solicitudes de búsqueda en menos de 0,3 segundos no garantiza automáticamente que el requisito sea realista. La medición es una parte importante del proceso de validación, pero hay otros factores que también deben considerarse para determinar la realidad del requisito.

Según las fuentes proporcionadas, un requisito debe ser no sólo medible, sino también:

1. **Comprensible**: Debe estar redactado de manera que sea fácilmente comprensible.
2. **No ambiguo**: Debe poder interpretarse de una sola manera.
3. **Gramaticalmente y ortográficamente correcto**.
4. **Realizable**: Debe ser posible implementarlo con tecnología existente y dentro de un costo asumible.
5. **Comprobable**: Debe ser posible definir pruebas que sean razonables en términos de coste y tiempo.
6. **Trazable**: Debe haber una clara trazabilidad hacia otros requisitos o casos de uso.

Además, según la guía de la NASA, un requisito debe ser técnicamente factible y sus especificaciones de rendimiento deben ser realistas. Esto significa que aunque podamos medir si el sistema cumple con el requisito de velocidad, también debemos considerar si es técnicamente posible implementar tal velocidad con los recursos disponibles y si el requisito tiene sentido en el contexto del proyecto.

Por lo tanto, aunque la medición es crucial, también es necesario evaluar la viabilidad técnica y la factibilidad económica del requisito. Si bien podemos verificar que el sistema cumple con el requisito de velocidad, también debemos asegurarnos de que sea factible implementarlo y mantenerlo en términos de recursos y costos.

## B4

¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?

Estado: prepared_unverified

Antes de aceptar el requisito de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos, es necesario revisar varios aspectos con el cliente para asegurar que el requisito cumpla con los estándares de calidad y sea realista. Aquí están los puntos clave que deberías abordar:

1. **Comprensibilidad y Claridad**:
   - Asegúrate de que el requisito esté redactado de manera que sea fácilmente comprensible para el cliente. Esto implica que el cliente entienda exactamente lo que se espera de la aplicación en términos de velocidad de respuesta.

2. **No Ambigüedad**:
   - Verifica que el requisito no tenga ambigüedades y que pueda interpretarse de una sola manera. Esto evitará malentendidos futuros sobre lo que se espera del sistema.

3. **Realizabilidad**:
   - Evalúa si es técnicamente posible implementar este requisito con la tecnología disponible y dentro del presupuesto acordado. Esto implica discutir con el equipo técnico si es viable alcanzar una velocidad de respuesta tan rápida.

4. **Comprobabilidad**:
   - Determina si es posible definir pruebas que sean razonables en términos de coste y tiempo para verificar que el sistema cumple con el requisito. Esto incluye la posibilidad de medir y probar la velocidad de respuesta de manera consistente y precisa.

5. **Trazabilidad**:
   - Asegúrate de que el requisito esté trazado hacia otros requisitos o casos de uso relevantes. Esto facilitará la gestión y seguimiento del requisito a lo largo del desarrollo del sistema.

6. **Feasibilidad**:
   - Discute con el cliente si el requisito es técnicamente factible y si puede ser implementado dado el presupuesto y la tecnología disponibles. Esto implica evaluar si el requisito tiene sentido en el contexto del proyecto y si es posible mantenerlo a largo plazo.

7. **Validación de Necesidades**:
   - Verifica que el sistema proporcionará las funciones que mejor satisfacen las necesidades del cliente. Esto implica asegurarte de que el requisito de velocidad de búsqueda responde a una necesidad real del cliente y no es simplemente una exigencia abstracta.

8. **Consistencia**:
   - Evalúa si hay conflictos con otros requisitos ya establecidos. Esto implica asegurarse de que el nuevo requisito no entra en conflicto con otros requisitos previamente acordados.

9. **Complejidad**:
   - Asegúrate de que todas las funciones requeridas por el cliente estén incluidas. Esto implica revisar si el requisito de velocidad de búsqueda cubre todas las necesidades del cliente y no deja ninguna funcionalidad pendiente.

10. **Verificabilidad**:
    - Determina si el requisito puede ser verificado después de que el producto final esté implementado. Esto implica asegurarse de que el requisito esté formulado de manera que pueda ser probado y comprobado de manera efectiva.

Revisar estos puntos con el cliente ayudará a garantizar que el requisito de velocidad de búsqueda sea claro, comprensible, técnicamente factible, y que satisfaga las necesidades del cliente.

## C1

¿Qué es la trazabilidad bidireccional de los requisitos? Pon un ejemplo inventado que relacione una necesidad, un requisito y un elemento de diseño.

Estado: prepared_unverified

La trazabilidad bidireccional de los requisitos implica vincular cada requerimiento tanto con las necesidades superiores (trazabilidad hacia atrás) como con los elementos de diseño específicos (trazabilidad hacia adelante). Esto asegura que cada requerimiento esté justificado por una necesidad superior y que también tenga un impacto directo en el diseño del sistema.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.

**Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.

**Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicitará al usuario ingresar un código de seguridad enviado por SMS junto con su contraseña.

### Explicación

En este ejemplo:

- **Necesidad Superior**: Esta es una declaración general que define el objetivo principal del sistema. En este caso, se enfoca en la seguridad y eficiencia de las transacciones.

- **Requerimiento**: Este es un detalle específico que debe cumplirse para alcanzar la necesidad superior. Aquí, el requerimiento es la implementación de la autenticación de dos factores, que es una medida necesaria para garantizar la seguridad de las transacciones.

- **Elemento de Diseño**: Este es un componente específico del sistema que implementa el requerimiento. En este caso, el elemento de diseño es un módulo de autenticación en la aplicación móvil que cumple con el requerimiento de autenticación de dos factores.

Este ejemplo ilustra cómo cada requerimiento está vinculado tanto a una necesidad superior como a un elemento de diseño específico, proporcionando una trazabilidad bidireccional que asegura que cada parte del sistema cumpla con los objetivos definidos inicialmente.

## C2

¿Tener esas relaciones de trazabilidad demuestra por sí solo que el diseño cumple correctamente el requisito?

Estado: prepared_unverified

La trazabilidad bidireccional de los requisitos asegura que cada requerimiento esté vinculado tanto a una necesidad superior como a un elemento de diseño específico. Sin embargo, tener estas relaciones de trazabilidad por sí sola no demuestra que el diseño cumpla correctamente el requisito. La trazabilidad es una herramienta importante para gestionar y controlar los requisitos, pero no garantiza automáticamente la satisfacción de estos.

Para asegurar que el diseño cumple correctamente con el requisito, es necesario realizar una serie de actividades adicionales:

1. **Verificación de la calidad del requisito**: Debe ser comprensible, no ambiguo, gramaticalmente correcto, ortográficamente correcto, realizable y comprobable. Esto significa que el requisito debe ser claro y preciso, y debe poder implementarse con tecnología existente y dentro de un costo razonable.

2. **Evaluación de la trazabilidad**: Asegurarse de que cada requerimiento esté correctamente trazado hacia atrás a una necesidad superior y hacia adelante a un elemento de diseño. Esto implica verificar que cada requerimiento tiene una fuente clara y que está vinculado adecuadamente a los elementos de diseño relevantes.

3. **Consistencia interna y externa**: Los requisitos deben ser consistentes entre sí y con otros documentos del proyecto. Esto implica evitar contradicciones internas y redundancias innecesarias, así como asegurar que los requisitos no sean inconsistentes con otros documentos del proyecto.

4. **Pruebas y validación**: Se deben definir y realizar pruebas para verificar que el diseño cumple con el requisito. Estas pruebas deben ser realizables y proporcionar resultados claros que permitan determinar si el requisito se ha cumplido correctamente.

Por ejemplo, consideremos nuevamente el ejemplo anterior:

- **Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.
- **Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.
- **Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicitará al usuario ingresar un código de seguridad enviado por SMS junto con su contraseña.

Para asegurar que el diseño cumple correctamente con el requisito, se deben realizar las siguientes acciones:

- **Verificación de la calidad del requisito**: El requisito de autenticación de dos factores debe ser claro y preciso, y debe ser posible implementarlo con tecnología existente y dentro de un costo razonable.
- **Evaluación de la trazabilidad**: Se debe verificar que el requisito de autenticación de dos factores está correctamente trazado hacia atrás a la necesidad superior de seguridad y eficiencia en las transacciones, y hacia adelante al módulo de autenticación en la aplicación móvil.
- **Consistencia interna y externa**: El requisito de autenticación de dos factores debe ser consistente con otros requisitos y documentos del proyecto, evitando contradicciones y redundancias innecesarias.
- **Pruebas y validación**: Se deben definir y realizar pruebas para verificar que el módulo de autenticación cumple con el requisito de autenticación de dos factores. Por ejemplo, se podría realizar una prueba donde se simula la entrada de un usuario con una contraseña y un código de seguridad válido, y se verifica que el sistema permita la transacción.

Estas acciones aseguran que el diseño cumple correctamente con el requisito, y no solo que existe una relación de trazabilidad entre ellos.

## C3

Cambiemos de tema: ¿qué diferencia hay entre que los requisitos sean completos y que sean consistentes?

Estado: prepared_unverified

La diferencia entre que los requisitos sean completos y que sean consistentes radica en los aspectos que cada uno aborda:

### Completitud de los requisitos:
Los requisitos deben ser completos en el sentido de que deben describir todas las características y funcionalidades necesarias para satisfacer las necesidades del usuario y del negocio. Esto significa que deben cubrir todos los aspectos del sistema que son relevantes y necesarios para su funcionamiento adecuado. Un requisito completo debe incluir detalles suficientes para que los desarrolladores comprendan completamente lo que se espera del sistema. Por ejemplo, si se requiere que el sistema permita la búsqueda de pacientes, el requisito completo debería especificar cómo se realizará esta búsqueda, en qué contexto, qué datos se utilizarán y cuáles serán los resultados esperados.

### Consistencia de los requisitos:
Los requisitos deben ser consistentes, lo que significa que no deben haber contradicciones entre ellos. Esto implica que los requisitos no deben ser mutuamente excluyentes ni entrar en conflicto entre sí. Por ejemplo, si se requiere que el sistema permita la búsqueda de pacientes en tiempo real, no puede haber otro requisito que especifique que la búsqueda debe ser lenta y detallada. La consistencia también implica que los requisitos deben ser coherentes con los objetivos del sistema y con otras partes del documento de requisitos.

### Ejemplo Hipotético:
Supongamos que estamos diseñando un sistema de gestión de pacientes en un hospital.

- **Completitud**:
    - **Requisito Completo**: "El sistema debe permitir la búsqueda de pacientes por nombre, apellido y número de seguro médico. La búsqueda debe devolver todos los registros médicos asociados al paciente."
    - Este requisito es completo porque describe claramente qué debe hacer el sistema y qué información se necesita para realizar la búsqueda.

- **Consistencia**:
    - **Requisito Consistente**: "El sistema debe permitir la búsqueda de pacientes por nombre, apellido y número de seguro médico. La búsqueda debe devolver todos los registros médicos asociados al paciente."
    - Este requisito es consistente con otros requisitos que pueden existir, como "El sistema debe almacenar todos los registros médicos de los pacientes de manera organizada y accesible".
    - Sin embargo, si hubiera otro requisito que dijera "El sistema debe buscar pacientes por nombre y apellido, pero no por número de seguro médico", esto sería inconsistente ya que entra en conflicto con el primer requisito.

### Conclusión:
La completitud se refiere a la exhaustividad de los requisitos, asegurando que todos los aspectos necesarios estén cubiertos. La consistencia se refiere a la ausencia de contradicciones entre los requisitos, asegurando que todos los requisitos sean coherentes entre sí y con los objetivos del sistema. Ambos son fundamentales para garantizar que el sistema final cumpla con las expectativas y funcione correctamente.

## C4

Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.

Estado: prepared_unverified

Dos requisitos inconsistentes entre sí son aquellos que contienen elementos que entran en conflicto o que no pueden cumplirse simultáneamente. Aquí tienes un ejemplo hipotético de dos requisitos que son inconsistentes:

### Ejemplo Hipotético

**Requisito 1:** "El sistema debe permitir que los usuarios ingresen y modifiquen sus datos personales en tiempo real."

**Requisito 2:** "El sistema debe bloquear cualquier intento de modificación de datos personales durante las horas pico de uso, que se definen como entre las 10:00 y las 14:00 horas."

### Explicación del Conflicto

- **Requisito 1** establece que los usuarios deben poder modificar sus datos personales en cualquier momento, incluidas las horas pico.
- **Requisito 2**, por otro lado, especifica que durante las horas pico (entre las 10:00 y las 14:00), el sistema debe bloquear cualquier intento de modificación de datos personales.

Estos dos requisitos son inconsistentes porque:
- **Requisito 1** permite modificaciones en tiempo real, lo cual implica que los usuarios pueden cambiar sus datos en cualquier momento.
- **Requisito 2** impide modificaciones durante un período específico (horas pico), lo cual entra en conflicto con la posibilidad de modificaciones en tiempo real.

### Conclusión

Este ejemplo ilustra cómo dos requisitos pueden ser inconsistentes debido a restricciones temporales que limitan la funcionalidad que otro requisito exige. La resolución de este conflicto podría implicar revisar y ajustar los requisitos para encontrar una solución que equilibre ambas necesidades, tal como permitir modificaciones fuera de las horas pico o establecer mecanismos alternativos para manejar las modificaciones durante las horas pico.