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

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B3

Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B4

¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?

Estado: prepared_unverified

Antes de aceptar el requisito de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos, sería importante revisar varios aspectos con el cliente:

1. **Necesidad Empresarial**: Comprender si este requisito de velocidad es crucial para el negocio y si cumple con las necesidades de los usuarios finales. Esto implica validar si el tiempo de respuesta de 0,3 segundos mejora significativamente la experiencia del usuario y si es factible desde el punto de vista técnico y económico.

2. **Impacto en el Diseño y Desarrollo**: Evaluar si el sistema actual tiene la capacidad técnica para cumplir con este requisito. Esto podría implicar una revisión de la arquitectura del sistema, la infraestructura de base de datos y la capacidad de procesamiento.

3. **Costos y Recursos**: Determinar si implementar este requisito requerirá inversiones adicionales en hardware, software o recursos humanos. También es importante considerar si el costo justifica la ventaja que proporcionará.

4. **Priorización de Requisitos**: Evaluar si este requisito de velocidad es prioritario frente a otros requisitos del sistema. Esto puede implicar una discusión sobre la importancia relativa de diferentes características del sistema.

5. **Posibles Cambios Futuros**: Considerar cómo este requisito afectará la capacidad del sistema para adaptarse a futuras modificaciones o mejoras. Un requisito muy específico o restrictivo puede dificultar cambios posteriores.

6. **Comprobación de la Factibilidad**: Realizar pruebas o simulaciones para verificar si el sistema actual puede cumplir con este requisito. Esto puede implicar reuniones con el equipo técnico para evaluar la viabilidad técnica.

7. **Impacto en la Usabilidad**: Evaluar si el requisito de velocidad mejorará la usabilidad del sistema y si los usuarios percibirán una mejora significativa en la experiencia de uso.

Estas revisiones ayudarán a garantizar que el requisito esté alineado con las necesidades del negocio y los usuarios, y que sea factible y beneficioso desde todos los puntos de vista relevantes.

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

Estado: invalidated

Sin respuesta confirmada como mostrada.

## C3

Cambiemos de tema: ¿qué diferencia hay entre que los requisitos sean completos y que sean consistentes?

Estado: prepared_unverified

La diferencia entre que los requisitos sean completos y que sean consistentes radica en dos aspectos fundamentales:

1. **Completitud de los requisitos**: Implica que todos los elementos necesarios para satisfacer las necesidades del sistema están incluidos en el conjunto de requisitos. Esto significa que no falta ningún detalle importante que sea necesario para el funcionamiento adecuado del sistema. Por ejemplo, si se requiere que un sistema web permita a los usuarios realizar compras online, la completitud implicaría que se describen todos los pasos necesarios para realizar una compra, desde la selección del producto hasta el pago y confirmación del pedido.

2. **Consistencia de los requisitos**: Se refiere a la ausencia de conflictos o contradicciones entre los diferentes requisitos. Esto significa que cada requerimiento debe ser coherente con los demás y no debe contradecir a otros requerimientos. Por ejemplo, si uno de los requisitos es que el sistema debe permitir a los usuarios realizar compras sin registrarse previamente, mientras que otro requisito es que el sistema debe almacenar información personal de los usuarios para futuras compras, estos dos requisitos podrían entrar en conflicto si no se especifica cómo manejar esta situación.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe permitir a los usuarios realizar compras online de manera segura y eficiente.

**Requisitos:**

1. **Requisito 1:** El sistema debe permitir a los usuarios realizar compras sin registrarse previamente.
2. **Requisito 2:** El sistema debe almacenar información personal de los usuarios para futuras compras.

**Elemento de Diseño:**

- **Diseño del Proceso de Compra:** El sistema implementará un proceso de compra que permitirá a los usuarios realizar compras sin registro, utilizando métodos de pago seguros. Además, el sistema almacenará la información de los usuarios que decidan registrarse para futuras compras.

### Explicación

- **Completitud:** El diseño del sistema incluye todos los detalles necesarios para permitir a los usuarios realizar compras sin registro y también para almacenar la información de los usuarios que deciden registrarse. Esto asegura que todas las necesidades del usuario están cubiertas.

- **Consistencia:** Los requisitos deben ser consistentes entre sí. En este caso, se ha resuelto la posible contradicción entre los requisitos 1 y 2 al especificar que el almacenamiento de información será opcional y estará disponible solo para aquellos usuarios que deciden registrarse. De esta manera, ambos requisitos pueden coexistir sin conflicto.

Este ejemplo muestra cómo la completitud y la consistencia de los requisitos son dos características importantes que deben mantenerse en un documento de requisitos para asegurar que el sistema cumpla con todas las necesidades del usuario de manera coherente y sin errores.

## C4

Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.

Estado: prepared_unverified

Dos requisitos inconsistentes entre sí son aquellos que no pueden coexistir debido a que uno excluye al otro o ambos no pueden ser verdaderos simultáneamente. Veamos un ejemplo inventado para ilustrar esto:

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe permitir a los usuarios realizar transacciones seguras y eficientes.

**Requisitos:**

1. **Requisito 1:** El sistema debe permitir a los usuarios iniciar sesión utilizando una contraseña única.
2. **Requisito 2:** El sistema debe prohibir el uso de contraseñas únicas y exigir que los usuarios utilicen un método de autenticación de dos factores.

### Explicación

- **Requisito 1:** Este requisito establece que los usuarios deben iniciar sesión utilizando una contraseña única. Esto implica que el sistema aceptará una sola forma de autenticación basada en una contraseña.

- **Requisito 2:** Este requisito, por otro lado, establece que el sistema debe prohibir el uso de contraseñas únicas y requerir que los usuarios utilicen un método de autenticación de dos factores. Esto implica que los usuarios no podrán iniciar sesión simplemente con una contraseña, sino que deben usar un segundo factor de autenticación adicional, como un token o un código de verificación.

### Conflicto

Estos dos requisitos entran en conflicto porque uno excluye al otro. Si se implementa el Requisito 1, los usuarios podrían iniciar sesión únicamente con una contraseña, lo cual contradice el Requisito 2 que prohíbe el uso de contraseñas únicas. Por otro lado, si se implementa el Requisito 2, los usuarios no podrían iniciar sesión con una sola contraseña, lo cual contradice el Requisito 1.

Para resolver este conflicto, sería necesario tomar una decisión sobre cuál de los dos requisitos se va a implementar. Por ejemplo, si se decide implementar el Requisito 2, entonces el Requisito 1 debería ser descartado o modificado para que coincida con el nuevo enfoque de autenticación.

Este ejemplo demuestra cómo la consistencia entre los requisitos es crucial para evitar situaciones donde los requisitos se contradigan entre sí, lo que puede llevar a problemas durante la implementación del sistema.

## T-web-empty

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: invalidated

Sin respuesta confirmada como mostrada.