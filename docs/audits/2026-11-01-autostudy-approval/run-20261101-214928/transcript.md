# Autoestudio automático — resultados

Diálogo de laboratorio; no es una sesión de alumno ni una evaluación de aprendizaje.

## A1

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: critic_finished_unverified

Un requisito de software es una declaración específica sobre lo que debe hacer o cumplir un sistema de software. Estos requisitos pueden ser funcionales o no funcionales y se utilizan para asegurar que el sistema cumpla con las necesidades de los usuarios y del negocio.

### Tipos de requisitos de software:

1. **Requisitos funcionales**: Estos describen las acciones que el sistema debe realizar. Por ejemplo:
   - **Requisitos de información**: Indican qué tipo de datos debe manejar el sistema. Por ejemplo, en una aplicación bancaria, un requisito podría ser "El sistema debe poder registrar y mostrar los movimientos de dinero de los clientes".
   - **Reglas de negocio**: Establecen las normas y restricciones que el sistema debe cumplir. Por ejemplo, en una aplicación de compras online, una regla de negocio podría ser "El sistema debe permitir la compra solo si el usuario ha iniciado sesión correctamente".
   - **Requisitos de conducta**: Se refieren a capacidades transversales o interacciones sencillas con el usuario. Por ejemplo, en una aplicación de mensajería, un requisito de conducta podría ser "El sistema debe enviar notificaciones al usuario cuando recibe un nuevo mensaje".

2. **Requisitos no funcionales**: Estos describen las características de calidad del sistema, como su rendimiento, seguridad, usabilidad, entre otros. Por ejemplo:
   - **Requisitos de integración**: Indican con qué otros sistemas debe interactuar el sistema. Por ejemplo, en una aplicación de gestión de inventario, un requisito de integración podría ser "El sistema debe estar conectado con el sistema de facturación para actualizar automáticamente los inventarios después de cada venta".
   - **Requisitos de dominio**: Establecen restricciones tecnológicas que el sistema debe cumplir. Por ejemplo, en una aplicación web, un requisito de dominio podría ser "El sistema debe ser compatible con navegadores modernos como Chrome, Firefox y Edge".

### Ejemplo sencillo

Imagina que estás creando una aplicación de control de asistencia para una escuela. Algunos requisitos podrían ser:

- **Requisito funcional**: "La aplicación debe registrar la asistencia de los estudiantes cada día".
- **Requisito no funcional**: "La aplicación debe ser capaz de procesar la asistencia de 100 estudiantes simultáneamente sin demoras".

Estos requisitos ayudan a garantizar que la aplicación cumpla con las necesidades de la escuela y funcione correctamente.

## A2

No he entendido bien la diferencia entre un requisito funcional y uno no funcional. ¿Puedes explicármela de otra manera?

Estado: critic_finished_unverified

Claro, veamos la diferencia entre un requisito funcional y uno no funcional desde una perspectiva más simplificada:

### Requisito Funcional:
Un requisito funcional se centra en lo que el sistema debe hacer. Específicamente, describe las acciones que el sistema debe realizar para cumplir con las necesidades del usuario. Estos requisitos son directamente relacionados con las operaciones que el sistema debe llevar a cabo. Por ejemplo, si estás creando una aplicación de control de asistencia escolar, un requisito funcional podría ser:

**"La aplicación debe registrar la asistencia de los estudiantes cada día."**

Este requisito funcional especifica una acción clara y concreta que el sistema debe realizar: registrar la asistencia de los estudiantes.

### Requisito No Funcional:
Un requisito no funcional, por otro lado, se refiere a las características de calidad del sistema. Estos requisitos no describen acciones específicas, sino más bien cómo debe comportarse el sistema en términos de rendimiento, seguridad, usabilidad, entre otros aspectos. Un requisito no funcional para la misma aplicación de control de asistencia podría ser:

**"La aplicación debe ser capaz de procesar la asistencia de 100 estudiantes simultáneamente sin demoras."**

Este requisito no funcional establece una expectativa sobre el rendimiento del sistema, indicando que debe ser capaz de manejar una carga de trabajo específica sin problemas de velocidad o eficiencia.

### Ejemplo Simplificado:
Imagina que estás diseñando una aplicación de control de temperatura para un edificio. 

- **Requisito funcional**: "La aplicación debe ajustar la temperatura del edificio según la programación diaria."
  
Esta declaración indica una acción específica que el sistema debe realizar: ajustar la temperatura según una programación preestablecida.

- **Requisito no funcional**: "La aplicación debe mantener la temperatura dentro de un rango de ±1°C durante todo el día."

Este requisito no funcional establece una condición de calidad que el sistema debe cumplir: mantener la temperatura dentro de un rango específico, independientemente de las fluctuaciones externas.

Espero que esta explicación te ayude a entender mejor la diferencia entre ambos tipos de requisitos.

## A3

Ponme un requisito funcional para una aplicación de reserva de citas y explica por qué lo es.

Estado: critic_finished_unverified

Un requisito funcional es una declaración que especifica una acción o tarea que el sistema debe realizar. Este tipo de requisito se enfoca en lo que el sistema debe hacer para satisfacer las necesidades del usuario. 

Para una aplicación de reserva de citas, un requisito funcional podría ser:

**"La aplicación debe permitir a los usuarios reservar citas con profesionales médicos eligiendo una fecha y hora disponibles."**

Este requisito funcional es claro y específico porque describe una acción concreta que el sistema debe realizar: permitir a los usuarios reservar citas eligiendo una fecha y hora disponibles. Esto significa que el sistema debe tener una interfaz que muestre las fechas y horas disponibles para cada profesional médico, y permitir a los usuarios seleccionar una opción disponible para reservar una cita.

Este requisito cumple con los criterios de calidad de los requisitos mencionados en las fuentes proporcionadas, ya que es comprensible, no ambiguo, gramaticalmente correcto, ortográficamente correcto, realizable y comprobable. Además, este requisito está trazado hacia atrás a las necesidades del usuario, ya que responde a la necesidad de los usuarios de poder reservar citas de manera fácil y rápida.

## A4

Pon otro ejemplo del mismo tipo, distinto del anterior.

Estado: critic_finished_unverified

Un requisito funcional es una declaración que especifica una acción o tarea que el sistema debe realizar. Este tipo de requisito se enfoca en lo que el sistema debe hacer para satisfacer las necesidades del usuario. 

Para una aplicación de reserva de citas, un requisito funcional diferente al anterior podría ser:

**"La aplicación debe enviar una confirmación de la cita reservada al correo electrónico del usuario."**

Este requisito funcional es claro y específico porque describe una acción concreta que el sistema debe realizar: enviar una confirmación de la cita reservada al correo electrónico del usuario. Esto significa que el sistema debe tener la capacidad de generar y enviar una notificación electrónica una vez que se haya reservado una cita.

Este requisito cumple con los criterios de calidad de los requisitos mencionados en las fuentes proporcionadas, ya que es comprensible, no ambiguo, gramaticalmente correcto, ortográficamente correcto, realizable y comprobable. Además, este requisito está trazado hacia atrás a las necesidades del usuario, ya que responde a la necesidad de los usuarios de recibir una confirmación de la cita reservada para asegurarse de que la reserva se haya realizado correctamente.

## B1

En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?

Estado: critic_finished_unverified

La propuesta de que la búsqueda responda en menos de 0,3 segundos en una aplicación de reservas es un requisito no funcional. Este tipo de requisito se refiere a las características del sistema que no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo. En este caso, el requisito se centra en la velocidad de respuesta del sistema, que es una propiedad de rendimiento.

Según la tabla proporcionada en la fuente del docente sobre métricas para especificar requisitos no funcionales, la velocidad puede ser medida por el tiempo de respuesta del usuario o evento. En este caso, el requisito establece un límite temporal específico para la respuesta de la búsqueda, lo que se traduce en una medida de velocidad.

Este requisito no funcional es importante porque define una expectativa de rendimiento que afectará la experiencia del usuario. Un tiempo de respuesta rápido mejora la usabilidad y eficiencia del sistema, permitiendo a los usuarios realizar sus tareas de manera fluida y sin demoras innecesarias.

## B2

¿Cómo comprobaríamos que se cumple ese requisito? Explícame qué haríamos y qué observaríamos.

Estado: critic_finished_unverified

Para comprobar que la búsqueda en la aplicación de reservas responde en menos de 0,3 segundos, se deben seguir estos pasos:

1. **Definir la prueba**: Diseñar una prueba que simule una búsqueda típica en la aplicación. Esta prueba debería incluir diferentes tipos de búsquedas representativas, como búsquedas por fecha, ubicación, disponibilidad, etc.

2. **Configurar el entorno de prueba**: Preparar el entorno de prueba adecuadamente. Esto podría implicar configurar servidores, bases de datos y cualquier otro recurso necesario para replicar las condiciones de producción.

3. **Ejecutar la prueba**: Ejecutar la prueba de búsqueda varias veces para obtener una media de tiempos de respuesta. Es importante realizar múltiples pruebas para asegurarse de que el resultado no sea aleatorio debido a factores externos como la carga del servidor.

4. **Medir el tiempo de respuesta**: Utilizar herramientas de medición de rendimiento para registrar el tiempo que tarda la aplicación en responder a cada solicitud de búsqueda. Estas herramientas pueden ser integradas en el propio sistema o utilizarse herramientas externas como LoadRunner, JMeter, o similares.

5. **Análisis de resultados**: Analizar los tiempos de respuesta obtenidos. Si el tiempo promedio de respuesta es menor a 0,3 segundos, entonces el requisito se considera cumplido. Si no es así, se debe identificar la causa raíz del problema y corregirlo antes de volver a realizar la prueba.

Estos pasos garantizan que se cumple el requisito de rendimiento de que la búsqueda responda en menos de 0,3 segundos. La prueba debe ser reproducible y los resultados deben ser consistentes para asegurar que el sistema cumple con el requisito de manera confiable.

## B3

Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?

Estado: critic_finished_unverified

{"mensaje_mostrado":"Poder medir que la búsqueda responda en menos de 0,3 segundos no garantiza automáticamente que el requisito sea realista. La verificabilidad es una parte importante de la calidad de los requisitos, pero también es necesario considerar otros aspectos para determinar si el requisito es realista. Según las fuentes proporcionadas, aquí hay algunos puntos clave a tener en cuenta:\n\n1. **Verificabilidad**: Como mencionas, es posible definir y realizar pruebas para comprobar que la búsqueda responde en menos de 0,3 segundos. Sin embargo, estas pruebas deben ser de coste y tiempo razonables. Por ejemplo, si la prueba requiere una infraestructura costosa o un equipo especializado, podría no ser realista desde una perspectiva económica.\n\n2. **Realizabilidad**: Además de ser verificable, el requisito debe ser técnicamente posible de implementar con la tecnología existente y dentro de un costo asumible. Por ejemplo, si el requisito implica una tecnología que aún no está disponible o que sería extremadamente costosa de implementar, no sería realista.\n\n3. **Compreensibilidad**: El requisito debe ser claro y fácil de entender. Si el requisito es comprensible, los desarrolladores podrán implementarlo correctamente.\n\n4. **Trazabilidad**: El requisito debe estar claramente relacionado con otras partes del sistema y con los objetivos del proyecto. Si el requisito no tiene una relación clara con los objetivos del proyecto, podría no ser realista.\n\n5. **Adaptabilidad**: El requisito debe poder modificarse sin causar un gran impacto en otros requisitos. Si el requisito es inflexible y no puede adaptarse a cambios futuros, podría no ser realista.\n\nPor lo tanto, aunque poder medir que la búsqueda responda en menos de 0,3 segundos es un paso importante, también es necesario considerar estos otros aspectos para determinar si el requisito es realista. Si todas estas condiciones se cumplen, entonces el requisito puede considerarse realista y viable."}

## B4

¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?

Estado: critic_finished_unverified

Antes de aceptar el requisito de que la búsqueda responda en menos de 0,3 segundos, es necesario revisar varios aspectos con el cliente para asegurar que el requisito cumpla con los estándares de calidad y sea realista. Aquí están los puntos clave que deberías abordar:

1. **Comprensibilidad**:
   - Asegúrate de que el requisito esté redactado de manera que sea fácilmente comprensible para el cliente. Debe ser claro y evitar ambigüedades.

2. **No Ambigüedad**:
   - El requisito debe ser único y no debe admitir múltiples interpretaciones. Debe ser claro y preciso.

3. **Gramática y Ortografía**:
   - El requisito debe estar bien escrito, sin errores gramaticales ni ortográficos.

4. **Realizabilidad**:
   - Verifica que el requisito pueda implementarse utilizando la tecnología existente y dentro de un costo asumible. Esto implica discutir con el cliente sobre los recursos disponibles y la viabilidad técnica.

5. **Comprobabilidad**:
   - El requisito debe ser verificable mediante pruebas de coste y tiempo razonables. Debes poder diseñar y realizar pruebas que demuestren que el requisito se cumple.

6. **Trazabilidad**:
   - El requisito debe estar claramente relacionado con otros requisitos o casos de uso. Debe haber una conexión clara entre el requisito y los objetivos del proyecto.

7. **Adaptabilidad**:
   - Evalúa si el requisito puede modificarse sin causar un gran impacto en otros requisitos. Esto es importante para permitir cambios futuros sin afectar significativamente el resto del sistema.

8. **Feasibility**:
   - Asegúrate de que el requisito sea técnicamente posible de implementar dada la tecnología y el presupuesto disponibles.

9. **Consistencia**:
   - Verifica que el requisito no entre en conflicto con otros requisitos ya establecidos.

10. **Complejidad**:
    - Asegúrate de que todos los requisitos necesarios por el cliente estén incluidos y que el requisito cumpla con las necesidades del cliente.

11. **Razón del Requisito**:
    - Documenta la razón detrás del requisito. Esto puede incluir restricciones o conceptos operativos que justifiquen la necesidad del requisito.

12. **Asunciones**:
    - Identifica y documenta cualquier asunción que se haya hecho al escribir el requisito, como la suposición de que se completará un programa de desarrollo tecnológico o una misión tecnológica exitosa.

13. **Relaciones**:
    - Documenta las relaciones con las operaciones esperadas del producto, como las expectativas sobre cómo los interesados utilizarán el producto.

14. **Restricciones de Diseño**:
    - Documenta cualquier restricción impuesta por decisiones tomadas durante el diseño evolutivo.

Estos puntos ayudarán a garantizar que el requisito sea completo, claro, comprensible, verificable y técnicamente viable.

## C1

¿Qué es la trazabilidad bidireccional de los requisitos? Pon un ejemplo inventado que relacione una necesidad, un requisito y un elemento de diseño.

Estado: critic_finished_unverified

La trazabilidad bidireccional de los requisitos implica vincular de manera clara y única cada requerimiento con las necesidades superiores (objetivos, metas, restricciones, etc.) y también con los elementos de diseño inferiores que lo satisfacen. Esto garantiza que cada requerimiento esté justificado por una necesidad superior y que cada elemento de diseño esté respaldado por un requerimiento específico.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe permitir a los usuarios realizar transacciones seguras y eficientes.

**Requerimiento:** El sistema debe validar la identidad del usuario antes de permitir cualquier transacción.

**Elemento de Diseño:** La aplicación debe incluir un módulo de autenticación que utilice un token único generado por un servidor de seguridad.

#### Explicación:

- **Necesidad Superior:** Esta es una declaración general que define el objetivo principal del sistema. En este caso, se enfoca en la seguridad y eficiencia de las transacciones.

- **Requerimiento:** Este es un requerimiento específico que deriva directamente de la necesidad superior. La validación de la identidad del usuario es una función necesaria para cumplir con la necesidad de seguridad y eficiencia.

- **Elemento de Diseño:** Este es un componente específico del sistema que implementa el requerimiento. El módulo de autenticación con token único es una solución técnica que permite validar la identidad del usuario, cumpliendo así con el requerimiento.

Este ejemplo ilustra cómo cada nivel (necesidad, requerimiento y diseño) está conectado y justificado por el nivel superior. La trazabilidad bidireccional asegura que cada parte del sistema tenga un propósito claro y esté alineada con los objetivos generales del proyecto.

## C2

¿Tener esas relaciones de trazabilidad demuestra por sí solo que el diseño cumple correctamente el requisito?

Estado: critic_finished_unverified

La trazabilidad bidireccional de los requisitos demuestra que existe una relación clara entre los requisitos y las necesidades superiores, así como entre los requisitos y los elementos de diseño inferiores. Sin embargo, tener estas relaciones de trazabilidad por sí sola no garantiza que el diseño cumpla correctamente con el requisito. La trazabilidad es una herramienta importante para asegurar que cada requerimiento esté justificado y que cada elemento de diseño esté respaldado por un requerimiento específico, pero no es suficiente para confirmar que el diseño cumple con el requisito de manera adecuada.

Para asegurarse de que el diseño cumple correctamente con el requisito, es necesario realizar otras actividades adicionales, como:

1. **Comprobación de la corrección**: Cada requerimiento debe estar correctamente formulado y ser técnicamente factible. Esto implica que el requerimiento debe ser claro, comprensible y gramaticalmente correcto, y que pueda ser implementado con tecnología existente y dentro de un costo razonable.

2. **Pruebas y validación**: Deben definirse pruebas específicas que permitan comprobar que el diseño cumple con el requerimiento. Estas pruebas deben ser realizables y proporcionar resultados claros y medibles que demuestren que el diseño cumple con el requerimiento.

3. **Consistencia y coherencia**: Los requisitos deben ser consistentes interna y externamente, es decir, no deben contener contradicciones ni redundancias innecesarias, y deben ser coherentes con otros documentos del proyecto.

4. **Feasibilidad técnica**: El requerimiento debe ser técnicamente factible, es decir, debe ser posible implementarlo con la tecnología disponible y dentro de los recursos disponibles.

Por ejemplo, si tenemos una necesidad superior de que el sistema debe permitir a los usuarios realizar transacciones seguras y eficientes, un requerimiento específico podría ser que el sistema debe validar la identidad del usuario antes de permitir cualquier transacción. Un elemento de diseño podría ser un módulo de autenticación que utilice un token único generado por un servidor de seguridad.

La trazabilidad bidireccional nos asegura que el módulo de autenticación está relacionado con el requerimiento de validación de la identidad, que a su vez está relacionado con la necesidad superior de seguridad y eficiencia. Sin embargo, para asegurarnos de que el diseño cumple correctamente con el requerimiento, debemos realizar pruebas específicas que comprueben que el módulo de autenticación efectivamente valida la identidad del usuario de manera segura y eficiente.

En resumen, aunque la trazabilidad bidireccional es crucial para establecer la relación entre los requisitos y las necesidades superiores y los elementos de diseño, es necesario realizar otras actividades adicionales para garantizar que el diseño cumple correctamente con el requisito.

## C3

Cambiemos de tema: ¿qué diferencia hay entre que los requisitos sean completos y que sean consistentes?

Estado: critic_finished_unverified

La diferencia entre que los requisitos sean completos y que sean consistentes radica en dos aspectos fundamentales de la ingeniería de requisitos:

1. **Completitud**: Se refiere a la inclusión de todas las características y funcionalidades necesarias para satisfacer las necesidades del sistema. Un requisito completo debe describir todos los elementos y capacidades requeridos para que el sistema funcione correctamente. Por ejemplo, si se necesita un sistema de gestión de pacientes en un hospital, la completitud implica que todos los detalles necesarios para gestionar a los pacientes, como sus datos médicos, citas, historiales, etc., estén incluidos en los requisitos.

2. **Consistencia**: Se refiere a la ausencia de conflictos o contradicciones entre los diferentes requisitos. Un requisito consistente no debe entrar en conflicto con otros requisitos o descripciones del sistema. Por ejemplo, si uno de los requisitos es que el sistema debe permitir a los usuarios buscar pacientes por nombre, otro requisito no puede ser que el sistema no debe permitir ninguna búsqueda por nombre.

### Ejemplo Hipotético

Supongamos que estamos diseñando un sistema de gestión de inventario para una tienda minorista. 

- **Requisito Completo**: "El sistema debe permitir a los empleados agregar nuevos productos al inventario, actualizar información sobre productos existentes y eliminar productos del inventario."
  
- **Requisito Consistente**: "El sistema debe permitir a los empleados agregar nuevos productos al inventario" y "El sistema debe permitir a los empleados actualizar información sobre productos existentes". Estos dos requisitos no entran en conflicto entre sí, ya que ambos son necesarios y complementarios para la gestión del inventario.

Sin embargo, si tuviéramos un requisito inconsistente como "El sistema debe permitir a los empleados agregar nuevos productos al inventario" y "El sistema no debe permitir la eliminación de productos del inventario", esto sería una contradicción porque el segundo requisito entra en conflicto con la necesidad de poder eliminar productos, que es una operación común en la gestión de inventarios.

### Importancia de Ambos Aspectos

- **Completitud**: Asegura que todos los elementos necesarios para el funcionamiento del sistema estén cubiertos. Si falta algún requisito, el sistema podría no cumplir con las necesidades del negocio o los usuarios.
  
- **Consistencia**: Asegura que los requisitos no entren en conflicto entre sí, lo que evitaría problemas durante la implementación y el mantenimiento del sistema.

Ambos aspectos son cruciales para garantizar que el sistema final cumpla con las expectativas y necesidades del negocio y los usuarios. La trazabilidad bidireccional ayuda a mantener estos requisitos organizados y relacionados correctamente, pero no es suficiente por sí sola para garantizar que el diseño cumpla con los requisitos de manera adecuada. Es necesario realizar otras actividades como pruebas y validaciones para asegurar que el diseño cumpla correctamente con los requisitos.

## C4

Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.

Estado: critic_finished_unverified

Dos requisitos pueden ser inconsistentes entre sí si uno entra en conflicto con el otro, es decir, si no pueden cumplirse simultáneamente. Aquí tienes un ejemplo hipotético de dos requisitos inconsistentes:

### Ejemplo Hipotético

**Requisito 1:** "El sistema debe permitir a los usuarios modificar sus propias contraseñas."

**Requisito 2:** "El sistema no debe permitir a los usuarios modificar sus propias contraseñas."

### Explicación del Conflicto

- **Requisito 1** establece que los usuarios deben tener la capacidad de cambiar sus propias contraseñas. Esto es común en muchos sistemas para mejorar la seguridad y la autonomía de los usuarios.

- **Requisito 2**, por otro lado, establece que los usuarios no deben tener la capacidad de cambiar sus propias contraseñas. Esto podría ser una medida de seguridad adicional, pero entra en conflicto directamente con el primer requisito.

Estos dos requisitos son inconsistentes porque no pueden cumplirse simultáneamente. Si se implementa el primer requisito, el segundo no puede ser cumplido, y viceversa. 

### Implicaciones

- **Inconsistencia**: La presencia de estos dos requisitos en un documento de requisitos llevaría a confusiones y problemas durante la fase de diseño y desarrollo. Los desarrolladores no podrían determinar cuál de los dos requisitos debe ser implementado, lo que podría llevar a errores en el sistema final.

- **Solución**: Para resolver esta inconsistencia, se debería revisar y ajustar los requisitos para que sean coherentes. Por ejemplo, se podría eliminar uno de los requisitos o reformularlos para que no entren en conflicto. Si ambas partes tienen razones válidas para estos requisitos, se podría buscar una solución intermedia que equilibre ambas necesidades, como permitir la modificación de contraseñas bajo ciertas condiciones de seguridad adicionales.

Este ejemplo ilustra cómo la consistencia entre los requisitos es crucial para evitar conflictos y asegurar que el sistema final sea coherente y funcional.
