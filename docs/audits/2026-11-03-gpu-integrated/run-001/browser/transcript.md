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

Estado: invalidated

Sin respuesta confirmada como mostrada.

## A3

Ponme un requisito funcional para una aplicación de reserva de citas y explica por qué lo es.

Estado: prepared_unverified

Un requisito funcional es una especificación que describe una acción específica que el sistema debe realizar. En el contexto de una aplicación de reserva de citas, un requisito funcional podría ser:

**"La aplicación debe permitir a los usuarios reservar una cita con un profesional específico en una fecha y hora disponibles."**

Este requisito es funcional porque especifica una acción concreta que el sistema debe realizar: permitir a los usuarios reservar citas. Este requisito incluye detalles sobre quién realiza la acción (usuarios), qué acción realizan (reservar una cita), con quién (un profesional específico) y en qué condiciones (fecha y hora disponibles).

Este tipo de requisito es importante porque define claramente una funcionalidad esencial de la aplicación, asegurando que los usuarios puedan realizar la tarea principal para la cual fue creada la aplicación.

## A4

Pon otro ejemplo del mismo tipo, distinto del anterior.

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B1

En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B2

¿Cómo comprobaríamos que se cumple ese requisito? Explícame qué haríamos y qué observaríamos.

Estado: prepared_unverified

¿A qué concepto o ejemplo te refieres?

## B3

Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?

Estado: invalidated

Sin respuesta confirmada como mostrada.

## B4

¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?

Estado: prepared_unverified

¿A qué concepto o ejemplo te refieres?

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

Estado: invalidated

Sin respuesta confirmada como mostrada.

## C4

Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.

Estado: prepared_unverified

Dos requisitos pueden ser inconsistentes entre sí cuando ambos no pueden cumplirse simultáneamente debido a restricciones técnicas, económicas o de tiempo. Aquí hay un ejemplo inventado que ilustra este concepto:

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe proporcionar una alta disponibilidad y una alta seguridad.

**Requisito 1:** El sistema debe estar disponible al menos el 99.99% del tiempo.

**Requisito 2:** El sistema debe realizar una verificación de identidad triple factor (por ejemplo, token físico, biometría y pregunta secreta) antes de permitir el acceso a cualquier recurso sensible.

### Explicación del Conflicto

- **Requisito 1 (Alta Disponibilidad):** Este requisito busca garantizar que el sistema esté operativo casi siempre, minimizando el tiempo de inactividad. Para lograr esto, se deben implementar mecanismos de redundancia y recuperación rápida, como múltiples servidores en diferentes ubicaciones geográficas y sistemas de respaldo automatizados.

- **Requisito 2 (Alta Seguridad):** Este requisito busca asegurar que solo los usuarios autorizados puedan acceder a recursos sensibles. La verificación de identidad triple factor aumenta significativamente la seguridad, pero también introduce un mayor tiempo de espera y posibles fallas en el proceso de autenticación.

### Conflicto entre los Requisitos

El problema surge cuando intentamos cumplir ambos requisitos simultáneamente:

- **Tiempo de Inicio:** La verificación de identidad triple factor puede llevar varios minutos, incluso si todo funciona correctamente. Esto podría interrumpir la disponibilidad del sistema durante períodos de alta carga, ya que los usuarios tendrían que esperar para iniciar sesión.

- **Fallos en la Autenticación:** Si alguno de los métodos de autenticación falla (por ejemplo, el token físico se pierde o la biometría no funciona), el sistema podría quedarse bloqueado hasta que se resuelva el problema. Esto podría causar períodos prolongados de inactividad, afectando la disponibilidad del sistema.

- **Recuperación Rápida:** Para mantener la alta disponibilidad, el sistema necesita recuperarse rápidamente de cualquier fallo. Sin embargo, la implementación de un sistema de autenticación triple factor puede complicar la recuperación rápida, ya que requiere un proceso más complejo y detallado para restaurar el acceso.

### Solución Potencial

Para resolver este conflicto, se podrían considerar alternativas como:

- Implementar un sistema de autenticación de dos factores para la mayoría de los usuarios y reservar la verificación triple factor solo para accesos críticos.
- Utilizar un sistema de autenticación adaptativa que ajuste el nivel de seguridad según el riesgo percibido, permitiendo un acceso rápido en situaciones seguras y un proceso más riguroso en casos de alto riesgo.

Este ejemplo muestra cómo dos requisitos pueden entrar en conflicto debido a restricciones técnicas y operativas, y cómo es necesario encontrar soluciones equilibradas para satisfacer ambas necesidades de manera efectiva.

## T-recovery

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