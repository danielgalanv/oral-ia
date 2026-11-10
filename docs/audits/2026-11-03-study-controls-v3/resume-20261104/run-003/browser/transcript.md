# Preguntas y respuestas reales — GPU
Sin evaluación del alumno.

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

La capacidad de medir un requisito no garantiza automáticamente que sea realista. Un requisito es considerado realista si puede ser implementado con tecnología existente y dentro de un costo razonable, además de ser testeable de manera práctica. Según las fuentes proporcionadas, un requisito debe cumplir varios criterios para ser considerado de alta calidad, entre ellos:

1. **Realizable**: Debe poder implementarse utilizando tecnología disponible y con un costo asumible.
2. **Comprobable**: Debe ser posible definir pruebas que sean factibles en términos de tiempo y costo para verificar que el requisito se cumple.

En el caso específico de que la búsqueda responda en menos de 0,3 segundos, aunque podamos medir el tiempo de respuesta, aún debemos considerar si es técnicamente factible implementar esta velocidad de respuesta con la tecnología actual y si las pruebas para verificar este requisito son prácticas y económicas.

Por ejemplo, si la infraestructura actual de la aplicación no puede manejar la carga de datos necesaria para responder en menos de 0,3 segundos, entonces el requisito no sería realizable. Además, si las pruebas para verificar este requisito implicaran un alto costo o tiempo excesivo, también podría considerarse que no es comprobable de manera práctica.

Por lo tanto, aunque el requisito de velocidad es medible, también es necesario verificar su factibilidad técnica y económica antes de considerarlo realista.

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

## N1-private-outside

¿Cómo se prepara una tortilla de patata?

Estado: prepared_unverified

Esa pregunta está fuera de los contenidos habilitados para esta actividad. No necesitas estudiar ese tema para esta actividad. Podemos continuar con los temas autorizados.

## N2-private-outside

¿Cuál es la capital de Australia?

Estado: prepared_unverified

Esa pregunta está fuera de los contenidos habilitados para esta actividad. No necesitas estudiar ese tema para esta actividad. Podemos continuar con los temas autorizados.

## T-web-empty

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: prepared_unverified

Un requisito de software es una especificación precisa que describe una característica o funcionalidad que debe cumplir el sistema. Estos requisitos pueden ser funcionales, no funcionales o de interfaz. Los requisitos funcionales describen lo que el sistema debe hacer, mientras que los requisitos no funcionales definen aspectos como la calidad, rendimiento y seguridad del sistema. Los requisitos de interfaz se refieren a cómo el sistema interactúa con otros sistemas o componentes.

Para ilustrar esto con un ejemplo sencillo, imagina que estás desarrollando una aplicación móvil para un gimnasio. Un requisito funcional podría ser:

**Requisito funcional RF1:** La aplicación debe permitir a los usuarios reservar clases de spinning.

Este requisito indica claramente una acción específica que la aplicación debe realizar. 

Un requisito no funcional podría ser:

**Requisito no funcional RN1:** La aplicación debe responder a las solicitudes de reserva en menos de 2 segundos.

Este requisito se refiere a la velocidad de respuesta de la aplicación, que es una característica no funcional.

Un requisito de interfaz podría ser:

**Requisito de interfaz RI1:** La aplicación debe integrarse con el sistema de reservas del gimnasio para verificar la disponibilidad de las clases.

Este requisito describe cómo la aplicación debe interactuar con otro sistema existente.

Estos ejemplos muestran cómo los requisitos de software proporcionan una base clara para el desarrollo del sistema, asegurando que se cumplan las expectativas de los usuarios y se satisfagan las necesidades del negocio.