# Preguntas y respuestas reales — GPU
Sin evaluación del alumno.

## A1

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: prepared_unverified

Un requisito de software es una especificación que define lo que el sistema debe hacer o cómo debe comportarse para satisfacer las necesidades de los usuarios y cumplir los objetivos del negocio. Estos requisitos pueden clasificarse en varios tipos:

1. **Requisitos Funcionales**: Estos describen las acciones específicas que el sistema debe realizar. Por ejemplo, en un sistema de gestión de inventario, un requisito funcional podría ser "El sistema debe permitir al usuario registrar nuevos productos".

2. **Requisitos No Funcionales**: Estos describen las características de calidad del sistema, como la velocidad de respuesta, la seguridad, la usabilidad, entre otras. Por ejemplo, un requisito no funcional podría ser "El sistema debe responder a las solicitudes del usuario en menos de dos segundos".

3. **Requisitos de Integración**: Estos describen cómo el sistema debe interactuar con otros sistemas o servicios. Por ejemplo, un requisito de integración podría ser "El sistema debe poder importar datos desde un sistema de contabilidad externo".

4. **Requisitos de Dominio**: Estos describen las restricciones tecnológicas o legales que el sistema debe cumplir. Por ejemplo, un requisito de dominio podría ser "El sistema debe estar diseñado para funcionar en un entorno operativo específico, como Windows Server 2019".

### Ejemplo Sencillo

Imagina que estás creando una aplicación móvil para un restaurante. Algunos requisitos podrían ser:

- **Requisito Funcional**: "La aplicación debe permitir a los clientes ordenar platos y bebidas".
- **Requisito No Funcional**: "La aplicación debe cargar las imágenes de los platos en menos de un segundo".
- **Requisito de Integración**: "La aplicación debe enviar las órdenes al sistema de cocina del restaurante".
- **Requisito de Dominio**: "La aplicación debe cumplir con las normativas de privacidad de datos personales vigentes".

Estos requisitos ayudan a asegurar que la aplicación cumpla con las necesidades del negocio y proporciona una experiencia adecuada a los usuarios.

## A2

No he entendido bien la diferencia entre un requisito funcional y uno no funcional. ¿Puedes explicármela de otra manera?

Estado: prepared_unverified

Un requisito de software puede dividirse en dos categorías principales: los requisitos funcionales y los requisitos no funcionales. La principal diferencia entre ambos radica en lo que describen:

- **Requisitos Funcionales**: Estos se centran en lo que el sistema debe hacer, es decir, en las acciones específicas que el sistema debe realizar para cumplir con las necesidades del usuario. Por ejemplo, en una aplicación bancaria, un requisito funcional podría ser "El sistema debe permitir a los usuarios consultar su saldo". Este requisito describe una acción específica que el sistema debe realizar.

- **Requisitos No Funcionales**: Estos se refieren a las características de calidad del sistema, como su rendimiento, seguridad, usabilidad, entre otros aspectos que no implican una acción específica sino más bien cómo debe comportarse el sistema. Por ejemplo, un requisito no funcional podría ser "El sistema debe responder a las solicitudes del usuario en menos de dos segundos". Este requisito no describe una acción específica, sino cómo debe responder el sistema a ciertas situaciones.

Para ilustrar esta diferencia, imagina que estás creando una aplicación de mensajería instantánea. 

- Un requisito funcional sería "La aplicación debe permitir a los usuarios enviar mensajes de texto a otros usuarios". Este requisito describe una acción específica que el sistema debe realizar.

- Un requisito no funcional sería "La aplicación debe garantizar que los mensajes sean entregados en menos de un minuto". Este requisito no describe una acción específica, sino cómo debe comportarse el sistema en términos de tiempo de entrega de los mensajes.

Espero que esto ayude a clarificar la diferencia entre estos dos tipos de requisitos.

## A3

Ponme un requisito funcional para una aplicación de reserva de citas y explica por qué lo es.

Estado: prepared_unverified

Un requisito funcional es una especificación que describe una acción o tarea específica que el sistema debe realizar. En el contexto de una aplicación de reserva de citas, un requisito funcional podría ser:

**"La aplicación debe permitir a los usuarios reservar una cita con un profesional específico en una fecha y hora determinadas."**

Este requisito funcional es claro y específico porque describe una acción que el sistema debe realizar: permitir a los usuarios reservar citas. Específicamente, el sistema debe permitir a los usuarios seleccionar un profesional, una fecha y una hora para la cita. Esto es crucial para cumplir con la función principal de la aplicación, que es facilitar la reserva de citas.

Este requisito funcional se diferencia de un requisito no funcional, que se enfocaría en aspectos como la velocidad de respuesta del sistema, la seguridad de las reservas, la facilidad de uso, etc. En este caso, el requisito funcional se centra en la acción de reservar una cita, mientras que un requisito no funcional podría ser "La aplicación debe confirmar la reserva en menos de un segundo", que se refiere a la velocidad de respuesta del sistema.

Este requisito funcional también cumple con los criterios de trazabilidad y verificación mencionados en las fuentes proporcionadas. Es posible rastrear su origen en las necesidades del usuario y validar su implementación en el sistema final.

## A4

Pon otro ejemplo del mismo tipo, distinto del anterior.

Estado: prepared_unverified

Otro ejemplo de un requisito funcional para una aplicación de reserva de citas podría ser:

**"La aplicación debe permitir a los usuarios cancelar una cita previamente reservada."**

Este requisito funcional es específico y describe una acción clara que el sistema debe realizar: permitir a los usuarios cancelar citas que ya han sido reservadas. Este requisito es importante porque refleja una necesidad común de los usuarios de poder modificar sus reservas según sea necesario.

Este requisito funcional se diferencia de un requisito no funcional, que se centraría en aspectos como la facilidad de uso, la seguridad de la cancelación, la velocidad de respuesta del sistema, etc. En este caso, el requisito funcional se centra en la acción de cancelar una cita, mientras que un requisito no funcional podría ser "La aplicación debe confirmar la cancelación en menos de un segundo", que se refiere a la velocidad de respuesta del sistema.

Este requisito funcional cumple con los criterios de trazabilidad y verificación mencionados en las fuentes proporcionadas. Es posible rastrear su origen en las necesidades del usuario y validar su implementación en el sistema final.

## B1

En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?

Estado: prepared_unverified

La propuesta de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos es un requisito no funcional. Este tipo de requisitos se refiere a las características del sistema que no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo. En este caso, el requisito se relaciona con la propiedad de velocidad, específicamente con el tiempo de respuesta del usuario o evento, que es una medida de la capacidad del sistema para procesar transacciones o responder a eventos en un tiempo determinado.

Según la tabla de métricas para especificar requisitos no funcionales presentada en la fuente, la propiedad de velocidad puede ser medida por el tiempo de respuesta del usuario o evento. En tu ejemplo, estás estableciendo un límite temporal para la respuesta de la aplicación, lo cual es una forma común de especificar un requisito no funcional de velocidad.

Este requisito no funcional de velocidad asegura que la aplicación sea rápida y eficiente en la respuesta a las solicitudes de los usuarios, mejorando así la experiencia del usuario y la eficacia general del sistema.

## B2

¿Cómo comprobaríamos que se cumple ese requisito? Explícame qué haríamos y qué observaríamos.

Estado: prepared_unverified

Para comprobar que la aplicación de reservas cumple el requisito de responder a las búsquedas en menos de 0,3 segundos, se deben seguir estos pasos:

1. **Definir la prueba**: Diseñar una prueba que simule una búsqueda típica en la aplicación. Esta prueba debería incluir todas las operaciones necesarias para realizar una búsqueda, desde la entrada de los parámetros hasta la obtención de resultados.

2. **Configurar el entorno de prueba**: Preparar un ambiente de prueba que sea representativo del entorno real donde se utilizará la aplicación. Esto incluye tener un servidor adecuadamente configurado, una base de datos con datos de prueba similares a los que se encontrarían en producción, y un cliente que pueda simular las condiciones de uso del usuario final.

3. **Ejecutar la prueba**: Ejecutar la prueba varias veces para obtener una media de tiempos de respuesta. Es importante realizar múltiples pruebas para asegurarse de que el resultado no es una anomalía y para poder calcular una media que refleje el rendimiento promedio de la aplicación.

4. **Medir el tiempo de respuesta**: Durante cada prueba, medir el tiempo que tarda la aplicación en responder a la solicitud de búsqueda. Esto se puede hacer utilizando herramientas de medición de rendimiento, como herramientas de profiling o monitoreo de aplicaciones web.

5. **Análisis de resultados**: Comparar el tiempo de respuesta medio obtenido con el umbral de 0,3 segundos. Si el tiempo medio de respuesta es menor que 0,3 segundos, entonces el requisito se considera cumplido. Si no es así, se debe investigar por qué el tiempo de respuesta es mayor y tomar medidas correctivas.

Estos pasos permiten asegurar que el requisito de velocidad se cumple de manera consistente y que la aplicación proporciona respuestas rápidas a las solicitudes de los usuarios, mejorando así la experiencia del usuario y la eficacia del sistema.

## B3

Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B4

¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?

Estado: prepared_unverified

Antes de aceptar el requisito de que la aplicación de reservas responda a las búsquedas en menos de 0,3 segundos, sería necesario revisar varios aspectos con el cliente para garantizar que el requisito es adecuado y factible. Aquí están algunos puntos clave a considerar:

1. **Necesidad del Cliente**: Comprobar que el cliente realmente necesita que la aplicación responda tan rápidamente. Esto implica entender el contexto de uso y las expectativas del cliente. Por ejemplo, si el cliente opera en un entorno donde la rapidez de respuesta es crítica, como en un servicio de atención al cliente en tiempo real, entonces este requisito podría ser muy apropiado.

2. **Impacto en el Diseño y Desarrollo**: Evaluar si el requisito es factible desde el punto de vista técnico. Esto incluye considerar si el equipo tiene la capacidad técnica para implementar tal velocidad de respuesta, y si el sistema actual o futuro puede manejar esta carga de trabajo. Por ejemplo, si el sistema actual no tiene la capacidad de procesar solicitudes tan rápidamente, podría requerir inversiones significativas en hardware o software.

3. **Costo y Beneficio**: Analizar el costo asociado con cumplir con este requisito frente a los beneficios que proporcionará. Un requisito de velocidad tan estricto podría aumentar el costo del desarrollo debido a la necesidad de optimización adicional o la adquisición de recursos adicionales. El cliente debe estar dispuesto a asumir este costo.

4. **Prioridades del Cliente**: Determinar si este requisito es una prioridad para el cliente en relación con otros requisitos. Si hay otros requisitos que son igualmente importantes o más críticos, el cliente podría preferir enfocarse en ellos primero.

5. **Flexibilidad y Adaptabilidad**: Considerar si el requisito permite cierta flexibilidad en caso de cambios futuros. Un requisito demasiado específico o rígido podría dificultar la adaptación del sistema a nuevas necesidades o tecnologías en el futuro.

6. **Medición y Monitoreo**: Establecer cómo se medirá y verificará el cumplimiento del requisito una vez implementado. Esto incluye definir las herramientas y métodos de medición, así como los procedimientos para monitorear el rendimiento continuamente.

7. **Impacto en la Experiencia del Usuario**: Evaluar cómo este requisito afectará la experiencia del usuario. Una aplicación que responde rápidamente puede mejorar la satisfacción del usuario, pero también es importante considerar otros aspectos de la experiencia, como la facilidad de uso y la funcionalidad.

Estas revisiones ayudarán a asegurar que el requisito de velocidad es adecuado, factible y beneficioso para el cliente y el usuario final.

## C1

¿Qué es la trazabilidad bidireccional de los requisitos? Pon un ejemplo inventado que relacione una necesidad, un requisito y un elemento de diseño.

Estado: prepared_unverified

La trazabilidad bidireccional de los requisitos implica vincular cada requerimiento tanto con las necesidades superiores (trazabilidad hacia atrás) como con elementos específicos del diseño o implementación (trazabilidad hacia adelante). Esto asegura que cada requerimiento esté justificado por una necesidad superior y que también pueda ser rastreado hasta un componente específico del sistema diseñado.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.

**Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.

**Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicita tanto un código SMS como una huella digital del usuario antes de permitir acceso a la función de transacciones.

En este ejemplo:

- **Necesidad Superior**: Esta es una declaración general que define una funcionalidad crítica del sistema, en este caso, la seguridad y eficiencia en las transacciones.
  
- **Requerimiento**: Este es un requerimiento específico que deriva directamente de la necesidad superior. Específicamente, el requerimiento de autenticación de dos factores asegura que la transacción sea segura y eficiente, cumpliendo así con la necesidad superior.

- **Elemento de Diseño**: Este es un componente específico del sistema que implementa el requerimiento. En este caso, el módulo de autenticación en la aplicación móvil es el elemento que cumple con el requerimiento de autenticación de dos factores.

Este ejemplo demuestra cómo cada requerimiento puede ser rastreado desde una necesidad superior hasta un elemento de diseño específico, y viceversa, asegurando que todos los componentes del sistema estén alineados con los objetivos generales del proyecto.

## C2

¿Tener esas relaciones de trazabilidad demuestra por sí solo que el diseño cumple correctamente el requisito?

Estado: invalidated

Sin respuesta confirmada como mostrada.

## C3

Cambiemos de tema: ¿qué diferencia hay entre que los requisitos sean completos y que sean consistentes?

Estado: prepared_unverified

La diferencia entre que los requisitos sean completos y que sean consistentes radica en dos aspectos fundamentales:

1. **Completitud de los requisitos**: Implica que todos los elementos necesarios para satisfacer las necesidades del sistema están incluidos en el documento de requisitos. Esto significa que no falta ningún detalle importante que pueda afectar al funcionamiento del sistema. Por ejemplo, si se requiere que un sistema web permita a los usuarios realizar compras, los requisitos deben incluir detalles sobre cómo iniciar sesión, agregar productos al carrito, pagar y confirmar la compra. Un requisito incompleto podría omitir algún paso crucial, lo que llevaría a problemas durante la implementación.

2. **Consistencia de los requisitos**: Se refiere a la ausencia de conflictos o contradicciones entre los diferentes requisitos. Los requisitos deben ser coherentes entre sí, es decir, no deben existir requisitos que se contradigan o que no puedan cumplirse simultáneamente. Por ejemplo, si uno de los requisitos establece que el sistema debe ser seguro y otro requiere que sea fácil de usar, estos requisitos deben poder cumplirse sin contradecirse. Si se propone que el sistema debe ser seguro pero también debe permitir el acceso público sin restricciones, esto sería una inconsistencia.

Un ejemplo hipotético para ilustrar esta diferencia podría ser el siguiente:

**Necesidad Superior:** El sistema debe proporcionar un servicio de mensajería instantánea que sea seguro y fácil de usar.

**Requisitos:**
- El sistema debe cifrar todas las comunicaciones entre usuarios.
- El sistema debe permitir que los usuarios accedan sin necesidad de autenticación.
- El sistema debe mostrar una interfaz amigable y fácil de navegar.

En este caso:
- **Completitud**: El requisito de cifrado de comunicaciones cubre la necesidad de seguridad, pero falta un requisito que especifique cómo se manejarán las comunicaciones no cifradas, lo que podría considerarse una omisión.
- **Consistencia**: Existe una inconsistencia entre los requisitos de cifrar las comunicaciones y permitir acceso sin autenticación, ya que ambas características son difíciles de cumplir simultáneamente sin comprometer la seguridad.

Por lo tanto, la trazabilidad bidireccional de los requisitos permite rastrear cada requerimiento desde la necesidad superior hasta el diseño, asegurando que cada requerimiento esté completo y consistente con los demás, y que cumpla con los objetivos del sistema.

## C4

Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.

Estado: prepared_unverified

Dos requisitos pueden ser inconsistentes entre sí cuando uno excluye o contradice al otro, dificultando su cumplimiento simultáneo. Aquí tienes un ejemplo hipotético:

**Necesidad Superior:** El sistema debe proporcionar un servicio de mensajería instantánea que sea seguro y fácil de usar.

**Requisito 1:** El sistema debe cifrar todas las comunicaciones entre usuarios para garantizar la seguridad.

**Requisito 2:** El sistema debe permitir que los usuarios accedan sin necesidad de autenticación para facilitar su uso.

### Explicación del Conflicto

- **Requisito 1** enfatiza la seguridad al exigir que todas las comunicaciones entre usuarios estén cifradas. Esto implica que las comunicaciones no podrían ser interceptadas o leídas por terceros no autorizados, protegiendo la privacidad y la integridad de los datos.

- **Requisito 2**, por otro lado, busca mejorar la usabilidad al eliminar la necesidad de autenticación. Sin embargo, esto reduce significativamente la seguridad, ya que cualquier persona podría acceder al sistema sin verificar su identidad, lo que aumentaría el riesgo de intrusiones y mal uso.

Estos dos requisitos son inconsistentes porque:
- **Seguridad vs. Usabilidad**: La cifrado de comunicaciones (Requisito 1) incrementa la seguridad pero puede complicar el proceso de inicio de sesión, mientras que la eliminación de la autenticación (Requisito 2) simplifica el uso pero compromete la seguridad.
- **Contradicción Directa**: Si se cumple el Requisito 1, entonces las comunicaciones estarán cifradas, lo que implica que alguien que no ha sido autenticado no podrá acceder a ellas. Sin embargo, si se cumple el Requisito 2, cualquier persona podría acceder al sistema sin autenticación, lo que contradice la necesidad de cifrar las comunicaciones.

Este ejemplo ilustra cómo dos requisitos pueden ser inconsistentes debido a sus objetivos opuestos o contradictorios, lo que dificulta su implementación simultánea sin comprometer alguno de ellos.

## T-web-empty

¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

Estado: invalidated

Sin respuesta confirmada como mostrada.