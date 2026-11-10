# Cuatro preguntas: respuestas reales y comparación

Primera versión experimental; las listas no acreditan el contenido. Todas las salidas se conservan sin retoques.

## K1 — ¿En qué se diferencian la completitud (completeness), la consistencia (consistency) y la complejidad de un sistema? Explícalo de forma sencilla.

### Nueva versión

La completitud (completeness), la consistencia (consistency) y la complejidad son tres características importantes de un sistema, especialmente en el contexto de la ingeniería de requisitos. Veamos cómo se diferencian:

### Completitud (Completeness)
La completitud se refiere a la capacidad de un conjunto de requisitos de cubrir todas las necesidades y características que el sistema debe tener para cumplir con su propósito. Un requisito completo incluye descripciones de todas las funcionalidades requeridas. Por ejemplo, si estás diseñando una aplicación de gestión de tareas, la completitud implica que el documento de requisitos debe mencionar todas las funcionalidades necesarias, como agregar tareas, marcarlas como completadas, eliminarlas, etc.

### Consistencia (Consistency)
La consistencia se refiere a la ausencia de conflictos o contradicciones dentro del conjunto de requisitos. Un requisito consistente no debe contener descripciones que se contradigan entre sí. Por ejemplo, si en un requisito se dice que la aplicación debe permitir la creación de tareas, mientras que en otro se afirma que no puede crear tareas, esto sería una falta de consistencia.

### Complejidad
La complejidad, aunque no está explícitamente definida en las fuentes proporcionadas, se refiere a la cantidad de detalles y elementos que un sistema tiene. Un sistema complejo puede tener muchos requisitos, interacciones y componentes que pueden hacer que sea difícil de entender y manejar. Por ejemplo, una aplicación de gestión de tareas que además incluya funciones de colaboración en tiempo real, seguimiento de proyectos y análisis de rendimiento sería más compleja que una simple aplicación de tareas.

### Ejemplo Hipotético
Imagina que estás diseñando una aplicación de gestión de tareas. La completitud aseguraría que todos los aspectos necesarios para la gestión de tareas estén cubiertos, como agregar, editar, marcar como completadas y eliminar tareas. La consistencia garantizaría que no haya contradicciones, como permitir y prohibir simultáneamente la creación de nuevas tareas. La complejidad podría aumentar si agregas características adicionales, como la colaboración en tiempo real, lo que haría que el sistema sea más complejo y difícil de manejar.

Palabras clave: completitud; consistencia; complejidad

### Comparación anterior

La completitud, la consistencia y la complejidad son tres características importantes de un sistema, especialmente en el contexto de la ingeniería de requisitos. Veamos cómo se diferencian:

### Completitud (Completeness)
La completitud se refiere a la exhaustividad con la que se describen todas las características y funcionalidades requeridas del sistema. Un documento de requisitos completo debería incluir todas las partes necesarias del sistema, asegurando que nada importante quede fuera. Por ejemplo, si estás diseñando una aplicación de gestión de tareas, la completitud implica que se describan todos los elementos necesarios, como la creación de nuevas tareas, la asignación de tareas, la actualización de tareas, la eliminación de tareas, etc.

**Ejemplo hipotético:** Si estás escribiendo los requisitos para un sistema de control de acceso a una oficina, la completitud significa que deberías incluir todos los aspectos necesarios, como la autenticación de usuarios, la autorización de accesos, la gestión de permisos, la generación de informes de acceso, etc.

### Consistencia (Consistency)
La consistencia se refiere a la ausencia de contradicciones o conflictos entre los diferentes requisitos del sistema. Un documento de requisitos consistente debe evitar cualquier contradicción interna o externa. Por ejemplo, si uno de los requisitos dice que el sistema debe permitir el acceso a ciertas áreas solo a empleados con un nivel de seguridad alto, mientras que otro requisito dice que cualquier empleado puede acceder a esas áreas, esto sería una contradicción.

**Ejemplo hipotético:** Si en el mismo sistema de control de acceso mencionado antes, tienes dos requisitos que dicen: "Los empleados de nivel básico pueden entrar a cualquier área" y "Los empleados de nivel básico no pueden entrar a áreas de alta seguridad", estos requisitos estarían en conflicto y el documento no sería consistente.

### Complejidad
La complejidad se refiere a la cantidad de detalles y componentes que tiene un sistema. Un sistema complejo tiene muchos elementos interrelacionados y puede ser difícil de entender y manejar. La complejidad no es una característica que se mide directamente en términos de completitud o consistencia, sino que es una propiedad inherente del sistema debido a su naturaleza y diseño.

**Ejemplo hipotético:** Un sistema de control de acceso que además de gestionar entradas y salidas también incluye funciones avanzadas como reconocimiento facial, seguimiento de movimientos dentro de la oficina, y análisis de patrones de comportamiento, sería un sistema complejo debido a la gran cantidad de funcionalidades y componentes interrelacionados.

### Conclusión
- **Completitud**: Se refiere a que el sistema tenga todas las características y funcionalidades necesarias.
- **Consistencia**: Se refiere a que los requisitos no contengan contradicciones ni conflictos.
- **Complejidad**: Se refiere a la cantidad de detalles y componentes del sistema, lo cual puede hacer que sea más difícil de entender y manejar.

Estas características son fundamentales para garantizar que el sistema cumpla con los objetivos deseados y funcione correctamente.

### Observación técnica

Distingue los conceptos. La nueva respuesta advierte que la complejidad no está definida explícitamente en los pasajes. No se demuestra superioridad general por esa diferencia.

## K2 — ¿Puede un conjunto de requisitos ser completo y contener contradicciones? Pon un ejemplo hipotético pequeño y explica qué condición comprueba cada criterio.

### Nueva versión

Un conjunto de requisitos puede ser completo y aún así contener contradicciones. Esto ocurre porque, aunque los requisitos deben incluir todas las características necesarias (completitud), es posible que algunas descripciones dentro del conjunto no sean consistentes entre sí (consistencia interna).

Para ilustrar esto, consideremos un ejemplo hipotético sobre un sistema de gestión de fotos en línea:

**Ejemplo Hipotético:**

Supongamos que tenemos un sistema de subida de fotos en una plataforma web. Los requisitos del sistema podrían ser los siguientes:

1. **Requisito 1:** El usuario debe poder subir fotos desde su computadora o tableta.
2. **Requisito 2:** Todas las fotos subidas deben tener un tamaño máximo de 5 MB.
3. **Requisito 3:** El sistema debe enviar un correo electrónico al moderador del proyecto después de cada subida de foto.
4. **Requisito 4:** El sistema debe enviar un correo electrónico al moderador del proyecto solo después de que se hayan subido 10 fotos.

En este caso, los requisitos 3 y 4 son contradictorios. Según el requisito 3, el sistema enviará un correo electrónico después de cada subida de foto, mientras que según el requisito 4, el sistema enviará un correo electrónico solo después de que se hayan subido 10 fotos. Estos dos requisitos no pueden cumplirse simultáneamente sin causar una contradicción.

**Comprobación de Criterios:**

- **Completa:** El conjunto de requisitos incluye todos los aspectos necesarios para la funcionalidad del sistema, como la subida de fotos, el tamaño máximo de las fotos y la notificación al moderador.
- **Consistente Internamente:** Este criterio no se cumple debido a la existencia de requisitos contradictorios (requisitos 3 y 4).
- **Consistente Externamente:** Este criterio no se verifica en este ejemplo hipotético, ya que no se mencionan otros documentos del proyecto.

Este ejemplo demuestra que un conjunto de requisitos puede ser completo (contiene todos los elementos necesarios) pero no consistente (contiene requisitos contradictorios). 

Palabras clave: requisitos, completitud, consistencia, contradicciones, sistema de gestión de fotos.

### Comparación anterior

Un conjunto de requisitos puede ser completo y aún así contener contradicciones. Esto ocurre porque, aunque sea imposible producir un documento de requisitos completamente y consistentemente debido a la complejidad del sistema y del entorno, es posible que un conjunto de requisitos incluya todas las características necesarias (completitud) pero tenga descripciones que se contradigan entre sí (consistencia).

### Ejemplo Hipotético

Imagina un sistema de gestión de fotos en línea llamado "KidsTakePics". Este sistema tiene dos requisitos:

1. **Requisito 1:** Los usuarios deben poder subir fotos desde su computadora o tableta.
2. **Requisito 2:** Los usuarios no pueden subir fotos desde su computadora o tableta si ya han subido más de 10 fotos.

Este conjunto de requisitos sería completo porque cubre todos los aspectos necesarios para la funcionalidad de subir fotos. Sin embargo, también contiene una contradicción interna: el primer requisito permite a los usuarios subir fotos siempre que quieran, mientras que el segundo requiere que haya un límite de 10 fotos antes de que se bloquee la capacidad de subir más fotos.

### Comprobación de Cada Criterio

- **Completitud:** El conjunto de requisitos es completo porque abarca todas las acciones necesarias para la funcionalidad de subir fotos. Ambos requisitos describen claramente cómo los usuarios pueden interactuar con el sistema para subir fotos.

- **Consistencia Interna:** El conjunto de requisitos no es consistente internamente porque hay una contradicción entre los dos requisitos. El primer requisito permite la subida de fotos sin restricciones, mientras que el segundo introduce una restricción que no se alinea con el primero.

### Conclusión

Este ejemplo ilustra cómo un conjunto de requisitos puede ser completo (en el sentido de que cubre todas las funcionalidades necesarias) pero no consistente (porque contiene requisitos que se contradicen entre sí). La comprobación de estos criterios implica revisar cada requisito para asegurarse de que no haya contradicciones internas, incluso si el conjunto de requisitos es completo en términos de cobertura de funcionalidades.

### Observación técnica

Ambas explican que completitud y consistencia son criterios distintos. La nueva usa notificar tras cada foto frente a solo tras diez. Los ejemplos son ficticios; no se exige una especificación real exhaustiva ni se rechazan sus cifras.

## K3 — En una aplicación de reservas proponemos búsquedas en menos de 0,3 segundos, un valor inventado. ¿Qué debemos revisar con el cliente antes de aceptar ese requisito?

### Nueva versión

Antes de aceptar el requisito de que las búsquedas en una aplicación de reservas se realicen en menos de 0,3 segundos, es importante revisar varios aspectos con el cliente:

1. **Modelización de Interacciones**: De acuerdo con la fuente sobre modelos de interacción, es crucial modelizar la interacción del usuario para identificar sus requerimientos. Esto implica entender cómo el usuario interactúa con la aplicación y cuáles son sus expectativas en términos de velocidad de respuesta. Por ejemplo, si el cliente espera que la aplicación sea rápida y fluida, esta meta de tiempo de búsqueda puede ser relevante.

2. **Comprobación de Necesidades de Negocio**: Según la fuente sobre procedimiento de requisitos, es necesario validar que el sistema software se ajuste a las necesidades de negocio del cliente y usuario. Esto implica reuniones y prototipado de la interfaz de usuario para asegurar que el requisito propuesto cumpla con las expectativas del cliente. Por ejemplo, si el cliente considera que la rapidez de las búsquedas es crítica para su negocio, este requisito podría ser fundamental.

3. **Análisis de Requisitos**: La fuente también menciona que es importante mejorar los requisitos mediante la elaboración de modelos (como diagramas UML) que permitan identificar posibles problemas y detallen la solución propuesta. Esto implica analizar si el requisito de tiempo de búsqueda es factible desde una perspectiva técnica y si hay posibles problemas que podrían surgir. Por ejemplo, si el sistema tiene que procesar grandes cantidades de datos, podría ser necesario verificar si el hardware y software disponibles pueden cumplir con este requisito.

4. **Explicación del Rationale**: Según las guías para escribir requisitos, es necesario incluir una explicación de por qué un requisito es necesario. En este caso, sería útil preguntar al cliente por qué considera que las búsquedas deben realizarse en menos de 0,3 segundos. Por ejemplo, si el cliente afirma que esto mejora la experiencia del usuario, es importante confirmar si esta afirmación es válida y si hay evidencia que respalde esta declaración.

5. **Formateo Estándar**: Finalmente, según las guías para escribir requisitos, es recomendable usar un formato estándar y consistente para todos los requisitos. Esto implica asegurarse de que el requisito esté bien formateado y claro. Por ejemplo, si el requisito se expresa correctamente y de manera clara, será más fácil para el equipo técnico entender y cumplir con él.

Palabras clave: modelización de interacciones; necesidades de negocio; análisis de requisitos; explicación del rationale; formateo estándar

### Comparación anterior

Antes de aceptar el requisito de que las búsquedas en la aplicación de reservas se realicen en menos de 0,3 segundos, es importante revisar varios aspectos con el cliente:

1. **Identificar la Necesidad Real**: Comprender por qué el cliente necesita que las búsquedas sean tan rápidas. Esto puede implicar reuniones para discutir los objetivos de negocio y las necesidades del usuario final. Según la fuente "6 - Procedimiento requisitos.pdf", página 4, se recomienda realizar un estudio de la situación inicial y definir los requisitos generales para asegurar que el sistema cumpla con las necesidades de negocio del cliente y los usuarios.

2. **Modelar la Interacción del Sistema**: Utilizar modelos de interacción, como diagramas de casos de uso o secuencia, para entender cómo el sistema interactúa con los usuarios y otros sistemas. Esto ayuda a identificar si la estructura del sistema propuesto es capaz de cumplir con el rendimiento requerido. La fuente "7 - Modelos.pdf", página 35, menciona que el modelado de la interacción del sistema ayuda a entender si la estructura propuesta es probable que entregue el rendimiento y fiabilidad necesarios.

3. **Validar el Requisito**: Comprobar que el requisito propuesto se corresponde con las necesidades de negocio del cliente y los usuarios. Esto implica validar que el requisito de velocidad de búsqueda sea factible y necesario. La fuente "6 - Procedimiento requisitos.pdf", página 12, señala que es crucial obtener la aprobación del cliente para asegurar que el producto final sea adecuado y tenga alta usabilidad.

4. **Explicar la Razón del Requisito**: Incluir una explicación clara de por qué este requisito es necesario. Esto puede ayudar a evitar malentendidos y asegurar que todos comprendan la importancia de cumplir con este requisito. La fuente "5 - Requisitos.pdf", página 39, sugiere incluir una explicación (razón) de por qué un requisito es necesario.

5. **Evaluar la Factibilidad Técnica**: Analizar si el sistema actual o el sistema propuesto tiene la capacidad técnica para cumplir con este requisito. Esto puede implicar una evaluación de la arquitectura del sistema y la capacidad de los componentes para interactuar de manera eficiente. La fuente "6 - Procedimiento requisitos.pdf", página 9, menciona que es importante mejorar los requisitos mediante la elaboración de modelos que permitan identificar posibles problemas y detallen más la solución propuesta.

Por lo tanto, antes de aceptar el requisito de que las búsquedas se realicen en menos de 0,3 segundos, es fundamental validar y analizar cuidadosamente este requisito con el cliente, asegurándose de que esté bien fundamentado y sea factible desde una perspectiva técnica y de negocio.

### Observación técnica

Ambas ofrecen revisiones generales del requisito. La recuperación no incluyó las páginas 11/73 que daban directamente los criterios de calidad; añadir palabras clave no resolvió ese hueco. No se acredita una comprobación operativa completa de rendimiento.

## K4 — Si hemos incluido todas las funciones que pide el cliente, ¿podemos concluir que el sistema será fácil y barato de construir? Razona la respuesta usando el material.

### Nueva versión

Incluir todas las funciones que pide el cliente no garantiza necesariamente que el sistema será fácil y barato de construir. Según las fuentes proporcionadas, el proceso de definición de requisitos técnicos implica más que simplemente cumplir con las expectativas del cliente. Es importante considerar varios aspectos adicionales:

1. **Comunicación Iterativa con los Estadholders**: Como menciona la NASA en su sección sobre la definición de requisitos técnicos, es crucial mantener una comunicación continua con los estadholders para asegurar una comprensión mutua de cada requerimiento. Esto implica que incluso si se han incluido todas las funciones solicitadas, puede haber detalles o interpretaciones que no se hayan capturado correctamente, lo que podría llevar a soluciones incorrectas o ineficientes.

2. **Calidad de los Requisitos**: Según el procedimiento de requisitos del docente, cada requisito debe ser comprensible, no ambiguo, gramaticalmente correcto, ortográficamente correcto, realizable, comprobable y trazado. Asegurarse de que todos estos criterios estén cumplidos es fundamental para garantizar que los requisitos sean claros y precisos, lo que facilita la construcción del sistema. Sin embargo, cumplir estos criterios no garantiza automáticamente que el sistema sea fácil o económico de construir.

3. **Complejidad y Consistencia de los Requisitos**: El docente también señala que, en la práctica, debido a la complejidad del sistema y del entorno, es imposible producir un documento de requisitos completo y consistente. Esto significa que incluso si se han incluido todas las funciones solicitadas, puede haber conflictos o contradicciones que no se hayan detectado inicialmente, lo que podría dificultar la implementación del sistema.

4. **Análisis de Requisitos**: El análisis de requisitos implica la elaboración de modelos (como UML) para identificar posibles problemas y detallar la solución propuesta. Identificar problemas en esta fase es crucial para prevenir costos exponenciales en el futuro. Por lo tanto, aunque se hayan incluido todas las funciones, el análisis de requisitos puede revelar problemas que podrían hacer que la construcción del sistema sea más difícil o costosa.

En resumen, aunque se hayan incluido todas las funciones solicitadas por el cliente, es necesario realizar una evaluación exhaustiva de la calidad, consistencia y complejidad de los requisitos para asegurar que el sistema será fácil y barato de construir. La inclusión de todas las funciones es solo el primer paso en un proceso más amplio que requiere una cuidadosa gestión de requisitos y comunicación continua con los estadholders.

Palabras clave: requisitos técnicos; comunicación iterativa; calidad de los requisitos; consistencia de los requisitos; análisis de requisitos

### Comparación anterior

Para responder a la pregunta "Si hemos incluido todas las funciones que pide el cliente, ¿podemos concluir que el sistema será fácil y barato de construir?", es necesario analizar varios aspectos relacionados con la definición y validación de los requisitos técnicos, según las fuentes proporcionadas.

Primero, según la fuente de la NASA (nasa-seh:64), la definición de requisitos técnicos implica transformar las expectativas de los interesados en una descripción del problema y luego en un conjunto completo de requisitos técnicos validados expresados como declaraciones de "deber" ("shall"). Estos requisitos deben permitir describir todos los inputs, outputs y relaciones requeridas entre ellos, incluyendo restricciones y las interacciones del sistema con operadores, mantenimiento y otros sistemas. La definición de requisitos es un proceso recursivo e iterativo que desarrolla las necesidades de los interesados, los requisitos del producto y los requisitos de productos/subproductos de nivel inferior. Es importante destacar que el equipo no debe depender únicamente de los requisitos recibidos para diseñar y construir el sistema. La comunicación e iteración con los interesados relevantes son esenciales para garantizar una comprensión mutua de cada requisito. Esto significa que incluso si se han incluido todas las funciones que pide el cliente, aún podría haber riesgos de malentendidos o implementaciones incorrectas si no se ha asegurado una comunicación clara y continua con los interesados.

Segundo, según el procedimiento del docente (docente-procedimiento:11), cada requisito debe cumplir con ciertos criterios de calidad, entre ellos ser realizable, es decir, que pueda implementarse mediante tecnología existente y con un costo asumible. Además, los requisitos deben ser comprensibles, no ambiguos, gramaticalmente correctos, ortográficamente correctos y trazables, es decir, que sus dependencias estén vinculadas a otros requisitos o casos de uso. Esto implica que aunque se hayan incluido todas las funciones solicitadas, no podemos asumir que el sistema será fácil y barato de construir si no se ha verificado que cada uno de estos requisitos cumpla con estos criterios de calidad.

Tercero, según el docente (docente-requisitos:14), en la práctica, debido a la complejidad del sistema y del entorno, es imposible producir un documento de requisitos completo y consistente. Esto significa que incluso si se han incluido todas las funciones solicitadas, todavía podrían existir conflictos o contradicciones en las descripciones de las facilidades del sistema que podrían dificultar la construcción del sistema.

Por lo tanto, aunque se hayan incluido todas las funciones que pide el cliente, no podemos concluir que el sistema será fácil y barato de construir sin verificar que los requisitos sean completos, consistentes, comprensibles, no ambiguos, gramaticalmente correctos, ortográficamente correctos, realistas desde el punto de vista técnico y trazables. Además, es crucial asegurar una comunicación continua y clara con los interesados para evitar malentendidos y garantizar que el sistema se construya según las intenciones originales del cliente.

### Observación técnica

Ambas niegan que incluir todas las funciones implique facilidad o bajo coste. La nueva contiene la errata «estadholders» y una conclusión que convendría formular sin sugerir una garantía de facilidad/coste. Su lista prioriza términos generales y no nombra completitud. No es una respuesta impecable.

