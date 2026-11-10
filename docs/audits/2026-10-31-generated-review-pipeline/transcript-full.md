# Respuestas realmente generadas y revisiones automáticas

Generador: Qwen2.5-14B NF4. Primer revisor: Qwen3-8B NF4 no pensante. Segunda revisión: Qwen2.5-14B, mismo checkpoint que generó, en otro rol/contexto; no es independencia de modelo. Ninguna respuesta inicial fue escrita ni alterada por el coordinador.

## G01 — course

**Pregunta**: ¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

**Respuesta inicial y final, idénticas**:

Un requisito de software es una declaración formal que describe una funcionalidad, servicio o restricción que debe cumplir un sistema para satisfacer las necesidades del usuario o del negocio. Estos requisitos pueden variar desde declaraciones altamente abstractas hasta especificaciones matemáticas detalladas, dependiendo del propósito para el cual se utilizarán. Por ejemplo, si estás desarrollando una aplicación móvil para un cliente, los requisitos podrían incluir declaraciones como "la aplicación debe permitir a los usuarios registrarse con su correo electrónico" (un requisito funcional) o "la aplicación debe ser capaz de funcionar en dispositivos con diferentes tamaños de pantalla" (un requisito no funcional).

Según el tipo, los requisitos de software se pueden clasificar en varios grupos:

1. **Requisitos de usuario**: Son declaraciones en lenguaje natural, acompañadas de diagramas, que describen los servicios que el sistema proporcionará y las restricciones operativas bajo las cuales funcionará. Estos requisitos están orientados a clientes no técnicos. Por ejemplo, un cliente podría decir: "La aplicación debe permitir a los usuarios buscar productos por nombre".

2. **Requisitos del sistema**: Son documentos estructurados que contienen descripciones detalladas de las funciones, servicios y restricciones operativas del sistema. Estos requisitos definen lo que debe implementarse y pueden formar parte de un contrato entre el cliente y el contratista. Un ejemplo sería: "La aplicación debe tener una interfaz de usuario amigable y fácil de usar".

3. **Requisitos funcionales**: Son declaraciones sobre los servicios que el sistema debe proporcionar, cómo debe reaccionar ante entradas específicas y cómo debe comportarse en situaciones particulares. Por ejemplo, "Cuando un usuario ingresa su contraseña incorrecta tres veces, la cuenta debe bloquearse automáticamente".

4. **Requisitos no funcionales**: Son restricciones sobre los servicios o funciones ofrecidos por el sistema, como restricciones de tiempo, restricciones en el proceso de desarrollo, estándares, etc. Por ejemplo, "La aplicación debe cargar una página en menos de dos segundos".

5. **Requisitos de dominio**: Son restricciones sobre el sistema derivadas del entorno en el que opera. Por ejemplo, si el sistema es para un hospital, podría haber requisitos de dominio relacionados con la privacidad de los datos médicos.

Estos tipos de requisitos ayudan a asegurar que el sistema final cumpla con las expectativas del cliente y funcione correctamente en su entorno de uso.

**Revisión 8B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Revisión 14B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Contraste técnico posterior, no enviado a modelos**: Definición y tipos pertinentes. El ejemplo de requisito de sistema es poco preciso y la lista mezcla dimensiones de clasificación, pero no afirma que sean excluyentes. Se registran como mejoras didácticas opcionales, no como respuesta incorrecta.

**Fuentes consultadas**:

- 5 - Requisitos.pdf, página 3
- 5 - Requisitos.pdf, página 4
- 5 - Requisitos.pdf, página 7
- 5 - Requisitos.pdf, página 10

## G02 — course

**Pregunta**: Pon un ejemplo inventado de requisito no funcional de rendimiento para una aplicación de reservas con un tiempo de respuesta menor de 0,3 segundos. Explica por qué es no funcional y cómo podríamos comprobarlo.

**Respuesta inicial y final, idénticas**:

Un ejemplo inventado de un requisito no funcional de rendimiento para una aplicación de reservas podría ser:

**Requisito no funcional de rendimiento:** La aplicación debe responder a cualquier solicitud del usuario en menos de 0,3 segundos.

Este requisito es no funcional porque se refiere a una propiedad del sistema (en este caso, su velocidad de respuesta) más que a una funcionalidad específica. Es decir, no describe una acción específica que el sistema debe realizar, sino una característica del sistema que afecta a todas las acciones que realiza. Este requisito no especifica qué acción debe realizar el sistema, sino cuánto tiempo debe tardar en responder a cualquier solicitud del usuario.

Para comprobar este requisito, podríamos utilizar pruebas de carga y tiempos de respuesta. Esto implicaría simular múltiples usuarios realizando diferentes tipos de solicitudes simultáneamente y medir el tiempo que toma el sistema para responder a cada una de ellas. Si el sistema responde a todas las solicitudes en menos de 0,3 segundos, entonces cumpliría con este requisito no funcional de rendimiento.

Este tipo de prueba puede llevarse a cabo mediante herramientas de pruebas de rendimiento y carga, como JMeter o LoadRunner, que pueden generar solicitudes simuladas y medir los tiempos de respuesta del sistema.

**Revisión 8B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Revisión 14B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Contraste técnico posterior, no enviado a modelos**: Ejemplo hipotético 0,3 s adecuado; distingue propiedad de rendimiento y acción funcional y propone medición. No se exige demostrar factibilidad de un dato hipotético. Los nombres JMeter/LoadRunner no aparecen en los pasajes: ampliación factual no trazada al RAG, no falsedad académica. Se verificaron fuera del ensayo con fuentes oficiales; esa comprobación no llegó a los modelos ni acredita fallback automático.

**Fuentes consultadas**:

- 5 - Requisitos.pdf, página 10
- 5 - Requisitos.pdf, página 15
- 5 - Requisitos.pdf, página 20
- 5 - Requisitos.pdf, página 22
- 5 - Requisitos.pdf, página 73

## G03 — course

**Pregunta**: ¿Qué diferencia hay entre que un requisito sea comprobable y que sea realista? Explícamelo con un ejemplo inventado y qué revisaríamos con el cliente.

**Respuesta inicial y final, idénticas**:

La diferencia entre que un requisito sea comprobable (verificable) y que sea realista radica en dos aspectos distintos pero relacionados del proceso de definición y validación de requisitos en ingeniería de software. Un requisito verificable se refiere a la capacidad de poder probar objetivamente si se cumple o no, mientras que un requisito realista implica que los recursos disponibles permiten implementarlo.

### Ejemplo Inventado

Supongamos que estamos desarrollando una aplicación móvil para un banco. El cliente propone lo siguiente:

**Requisito 1:** La aplicación debe ser capaz de procesar transacciones bancarias en tiempo real, garantizando que cada transacción se complete en menos de 1 segundo.

**Requisito 2:** La aplicación debe ser capaz de procesar transacciones bancarias en tiempo real, garantizando que cada transacción se complete en menos de 1 segundo, utilizando solo un servidor de bajo costo y tecnología existente.

#### Comprobabilidad (Verificabilidad)
El primer requisito es verificable porque podemos establecer pruebas específicas para medir el tiempo de procesamiento de cada transacción. Podríamos realizar pruebas de carga y tiempos de respuesta para asegurarnos de que cada transacción se completa en menos de 1 segundo. Esto es un requisito objetivo y medible.

#### Realismo
El segundo requisito añade una condición adicional sobre la infraestructura tecnológica y económica disponible. Este requisito no solo debe ser verificable, sino también factible con los recursos actuales. Si el servidor de bajo costo no tiene la capacidad de manejar la carga de transacciones en tiempo real, entonces este requisito no sería realista.

### Revisión con el Cliente
Para revisar estos requisitos con el cliente, deberíamos considerar lo siguiente:

1. **Verificabilidad**: 
   - ¿Podemos establecer métricas claras y objetivas para verificar que cada transacción se completa en menos de 1 segundo?
   - ¿Podemos diseñar pruebas de carga y tiempos de respuesta para validar esta afirmación?

2. **Realismo**:
   - ¿Existe la infraestructura tecnológica actualmente disponible para cumplir con este requisito?
   - ¿Es posible implementar este requisito dentro del presupuesto y con la tecnología actual?

Por ejemplo, podríamos discutir con el cliente si el servidor de bajo costo puede manejar la carga de transacciones en tiempo real. Si no es así, podríamos sugerir ajustar el requisito para utilizar una infraestructura más robusta o buscar alternativas técnicas que cumplan con el mismo propósito dentro del presupuesto disponible.

En resumen, un requisito verificable se enfoca en la capacidad de probar objetivamente su cumplimiento, mientras que un requisito realista se centra en la factibilidad de implementarlo con los recursos disponibles. Ambos aspectos son cruciales para asegurar que los requisitos sean tanto alcanzables como cumplibles.

**Revisión 8B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Revisión 14B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Contraste técnico posterior, no enviado a modelos**: Distingue comprobabilidad de realismo; el ejemplo del servidor de bajo coste está condicionado a la capacidad disponible, no presupone que sea imposible o viable. La revisión con cliente es pertinente. No se penaliza extensión ni estilo.

**Fuentes consultadas**:

- 5 - Requisitos.pdf, página 20
- 5 - Requisitos.pdf, página 72
- 5 - Requisitos.pdf, página 73
- 5 - Requisitos.pdf, página 74

## G04 — course_with_nasa

**Pregunta**: ¿Qué es la trazabilidad bidireccional de los requisitos? Pon un ejemplo inventado con un requisito, su origen y un elemento de diseño.

**Respuesta inicial y final, idénticas**:

La trazabilidad bidireccional de los requisitos es la capacidad de rastrear cualquier requerimiento a su requerimiento padre y a sus hijos requerimientos asignados. Esto implica poder seguir el origen de un requerimiento hasta su fuente inicial (trazabilidad hacia atrás) y también identificar qué partes del diseño o implementación satisfacen ese requerimiento (trazabilidad hacia adelante).

Por ejemplo, consideremos un sistema de gestión de inventario para una tienda minorista:

**Requisito del usuario:** El sistema debe permitir a los empleados agregar nuevos productos al inventario.

**Origen del requerimiento:** Este requerimiento proviene de una necesidad expresada por el gerente de la tienda, quien necesita que el sistema permita la adición de nuevos productos fácilmente para mantener actualizado el inventario.

**Elemento de diseño:** En el diseño del sistema, se ha creado una funcionalidad específica dentro de la interfaz de usuario que permite a los empleados ingresar detalles sobre nuevos productos, como nombre, descripción, precio y cantidad disponible. Esta funcionalidad está vinculada directamente al requerimiento del usuario mencionado anteriormente.

En este caso, la trazabilidad bidireccional permite rastrear desde el requerimiento del usuario hasta la funcionalidad específica en el diseño del sistema (trazabilidad hacia adelante), y también permite rastrear desde la funcionalidad en el diseño hasta el requerimiento del usuario original (trazabilidad hacia atrás). Esto garantiza que cada parte del diseño cumple con los requisitos originales y que todos los requisitos están respaldados por elementos específicos en el diseño.

**Revisión 8B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Revisión 14B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Contraste técnico posterior, no enviado a modelos**: La definición y el ejemplo central son adecuados. El cierre excede lo demostrado: dice que la trazabilidad garantiza que cada parte del diseño cumple los requisitos y que todos están respaldados. Una asociación rastreable no demuestra por sí sola cumplimiento correcto, ni la descripción de una relación acredita completitud de todo el diseño. Es una conclusión académica excesiva localizada, no un error de los códigos ficticios ni una invalidación de toda la explicación.

**Fuentes consultadas**:

- https://www.nasa.gov/reference/6-0-crosscutting-technical-management/
- 6 - Procedimiento requisitos.pdf, página 13

## G05 — technical_w3c_control_not_course

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta inicial y final, idénticas**:

Un requisito no funcional comprobable de contraste para el texto normal de una web, según el criterio del W3C, sería:

**Requisito no funcional:** El contraste entre el texto normal y su fondo debe ser de al menos 4.5:1.

Este requisito cumple con los criterios establecidos por el W3C y se puede verificar objetivamente. Según el fragmento de texto proporcionado por el W3C, se especifica que el contraste mínimo para el texto normal (que no es texto grande, decorativo ni un logotipo) debe ser de al menos 4.5:1. Esto permite asegurar que el texto sea legible para la mayoría de los usuarios, incluyendo aquellos con discapacidades visuales.

Este requisito no funcional se diferencia de un objetivo general como "facilidad de uso" porque es específico y medible. Se puede probar mediante herramientas de evaluación de accesibilidad web que miden el contraste entre colores y determinan si cumple con el ratio mínimo requerido.

**Revisión 8B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Revisión 14B**:
```json
{"status":"no_issues_found","issues":[]}
```

**Contraste técnico posterior, no enviado a modelos**: El generador usa correctamente 4,5:1 para texto normal. No inventa el 3:1 del borrador negativo anterior. Responde al criterio de contraste solicitado, no certifica por sí solo toda la accesibilidad de una web. Este control W3C se informa separado del contenido de la asignatura.

**Fuentes consultadas**:

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- 5 - Requisitos.pdf, página 20
