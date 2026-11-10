# Revisión docente de casos de fallo

Para cada caso, marca una opción:
- **P** = debería pasar (no hay que avisar)
- **M** = debería marcarse como error
- **D** = depende / duda (di por qué)

Los casos 5–8 son errores que **yo introduje** a propósito en respuestas correctas, para medir si el revisor los detecta. Los demás son respuestas reales o controles.

Los cambios de numeración de listas («1.» → «5.») que había inyectado como «errores de cifra» los he descartado: no son errores.

---

## Caso 1 — A. Ejemplo hipotético que el revisor marcó como error

**Pregunta del alumno:** Pon un ejemplo hipotético de rendimiento y explica qué habría que comprobar, sin afirmar que ya se cumple.

**Texto de la respuesta:**
> Como ejemplo inventado, podemos proponer que las búsquedas respondan en menos de 0,3 segundos con 100 usuarios simultáneos simulados. Es una condición hipotética, no un estándar ni un resultado medido.
> 
> Para tratarlo como comprobable debemos poder definir pruebas razonables; para valorar si es realizable, revisar tecnología y coste. Proponer esas cifras no demuestra que se cumplan ni que la implementación sea viable.
> 
> Palabras clave: comprobabilidad; realizabilidad

**Lo que dice el material:**
> (el material habla de calidad de requisitos; no trae cifras de rendimiento)

**Lo que dijo el revisor:** El ejemplo introduce un escenario hipotético de rendimiento (tiempo de respuesta y usuarios simultáneos) que no está cubierto en las fuentes, que se enfocan en calidad de requisitos (comprensible, no 

**Qué hay que decidir:** El ejemplo está declarado como inventado y explica qué habría que comprobar.

**Tu decisión:** P / M / D

---

## Caso 2 — A. Ejemplo hipotético que el revisor marcó como error

**Pregunta del alumno:** ¿Qué diferencia hay entre un requisito de usuario y un requisito del sistema?

**Texto de la respuesta:**
> Un requisito de usuario describe lo que el usuario necesita o espera del sistema. Por ejemplo, un requisito de usuario podría ser: "El usuario debe poder buscar un producto por su nombre". Este requisito se centra en la funcionalidad desde la perspectiva del usuario, sin entrar en detalles sobre cómo el sistema debe implementar esa funcionalidad.

**Lo que dice el material:**
> etalle cómo debe interactuar el sistema con sus usuarios. • Requisitos funcionales. Se deben enunciar a un nivel de detalle suficiente como para que a partir de ellos pueda implementarse una solución. Se clasifican en: • Requisitos de información, describen la información que debe almacenar y gestionar el sistema. • Re

**Lo que dijo el revisor:** El ejemplo de 'requisito de usuario' (buscar por nombre) y 'requisito del sistema' (estructura de base de datos) no está respaldado por las fuentes. Las fuentes solo describen 'requisitos funcionales'

**Qué hay que decidir:** Un ejemplo sencillo («buscar un producto por su nombre») para ilustrar una diferencia conceptual.

**Tu decisión:** P / M / D

---

## Caso 3 — B. La respuesta añade algo que la fuente no dice (sin contradecirla)

**Pregunta del alumno:** ¿Qué es un requisito realizable y qué relación tiene con el coste?

**Texto de la respuesta:**
> La relación entre un requisito realizable y el coste se basa en que el requisito debe ser implementable con recursos y tecnología disponibles, y el coste de implementarlo debe ser manejable dentro del presupuesto del proyecto. Esto implica que el requisito no debe requerir tecnologías o recursos que no estén disponibles o que superen el presupuesto asignado, asegurando así que el proyecto sea viable desde una perspectiva económica.

**Lo que dice el material:**
> • Gramaticalmente correcto. • Ortográficamente correcto. • Realizable. Puede implementarse mediante tecnología existente y con un coste asumible • Comprobable. Se pueden definir una o más pruebas, de coste y tiempo razonables. • Trazado. Las dependencias del requisito están trazadas hacia otros requisitos o casos de u

**Lo que dijo el revisor:** La fuente no menciona explícitamente el 'presupuesto del proyecto' como criterio para la realizabilidad, solo el 'coste asumible' sin referir a recursos disponibles o restricciones presupuestarias.

**Qué hay que decidir:** La fuente habla de «coste asumible»; la respuesta lo traduce a «presupuesto del proyecto».

**Tu decisión:** P / M / D

---

## Caso 4 — B. La respuesta añade algo que la fuente no dice (sin contradecirla)

**Pregunta del alumno:** ¿Qué significa que un requisito no sea ambiguo?

**Texto de la respuesta:**
> Un requisito no ambiguo admite una única interpretación. Tener buena ortografía es otra propiedad y no basta para garantizar esa única interpretación.
> 
> Palabras clave: ausencia de ambigüedad; ortografía

**Lo que dice el material:**
> nsible. Redactado de forma que es fácilmente compresible. • No ambiguo. Sólo puede interpretarse de una sola manera. • Gramaticalmente correcto. • Ortográficamente correcto. • Realizable. Puede implementarse mediante tecnología existente y con un coste asumible • Comprobable. Se pueden definir una o más pruebas, de cos

**Lo que dijo el revisor:** La respuesta menciona 'ortografía' como propiedad relacionada con la ambigüedad, pero la fuente no vincula la ortografía con la claridad interpretativa. La ambigüedad se refiere a la unicidad de inter

**Qué hay que decidir:** Dice que la ortografía es otra propiedad distinta; la fuente las lista por separado.

**Tu decisión:** P / M / D

---

## Caso 5 — C. Confusión de concepto (un título o nombre no corresponde a su contenido)

**Pregunta del alumno:** ¿Qué es un requisito correcto según el modelo de calidad?

**Texto de la respuesta:**
> l proyecto. Esto implica que el requisito debe ser claro y directo, evitando lenguaje técnico excesivo o ambigüedad. 2. **Comprensible**: Debe ser posible interpretar el requisito de una sola manera. Esto significa que no debe haber lugar a dudas sobre lo que se espera que haga el sistema. Un requisito ambiguo puede llevar a malentendidos y a implementaciones incorrectas. 3. **Gramaticalmente correcto**: El requisito debe estar bien red

**Lo que dice el material:**
> nsible. Redactado de forma que es fácilmente compresible. • No ambiguo. Sólo puede interpretarse de una sola manera. • Gramaticalmente correcto. • Ortográficamente correcto. • Realizable. Puede implementarse mediante tecnología existente y con un coste asumible • Comprobable. Se pueden definir una o más pruebas, de cos

**Lo que dijo el revisor:** (v5 lo detectó; el de fundamentación dijo «sin incidencias» sobre otro caso similar)

**Qué hay que decidir:** El título «Comprensible» encabeza la definición de «No ambiguo». Cambio hecho por mí: «No ambiguo» → «Comprensible».

**Tu decisión:** P / M / D

---

## Caso 6 — C. Confusión de concepto (un título o nombre no corresponde a su contenido)

**Pregunta del alumno:** ¿Qué diferencia hay entre un requisito comprensible y uno trazado?

**Texto de la respuesta:**
> Un requisito No ambiguo está redactado de modo que se entiende fácilmente. Un requisito trazado tiene sus dependencias identificadas hacia otros requisitos o casos de uso. Son propiedades distintas.
> 
> Palabras clave: comprensibilidad; trazabilidad

**Lo que dice el material:**
> • Modelo de calidad para cada requisito individualmente: • Comprensible. Redactado de forma que es fácilmente compresible. • No ambiguo. Sólo puede interpretarse de una sola manera. • Gramaticalmente correcto. • Ortográficamente correcto. • Realizable. Puede implementarse mediante tecnología existente y con un coste a

**Lo que dijo el revisor:** (v5 lo detectó; el de fundamentación no)

**Qué hay que decidir:** «Un requisito No ambiguo está redactado de modo que se entiende fácilmente» (eso es «comprensible»). Cambio hecho por mí: «Comprensible» → «No ambiguo».

**Tu decisión:** P / M / D

---

## Caso 7 — D. Cambio de sentido (palabra contraria)

**Pregunta del alumno:** ¿Qué significa que un conjunto de requisitos sea completo?

**Texto de la respuesta:**
> Un conjunto de requisitos es completo cuando abarca ninguno los aspectos necesarios para describir el sistema a desarrollar, asegurando que no se omitan detalles cruciales que puedan afectar a su funcionamiento o a su adecuación a las necesidades de negocio. Esto significa que el conjunto de requisitos d

**Lo que dice el material:**
> ntar. • Los casos de uso que se considere necesario, se van completando con más información. • Los requisitos generales se van detallando en requisitos funcionales, no funcionales, de integración y de dominio (restricciones técnicas). 30/10/2014 Chapter 4 Requirements Engineering 6

**Lo que dijo el revisor:** (v5 lo detectó; el de fundamentación no)

**Qué hay que decidir:** «abarca ninguno los aspectos necesarios». Cambio hecho por mí: «todos» → «ninguno».

**Tu decisión:** P / M / D

---

## Caso 8 — D. Cambio de sentido (palabra contraria)

**Pregunta del alumno:** ¿Qué es la ingeniería de requisitos?

**Texto de la respuesta:**
> os usuarios utilizarán el sistema futuro para realizar sus tareas dentro de los procesos de negocio de la organización. Esto excluye la definición de casos de uso del sistema en una versión inicial. 2. **Documentación de los requisitos del sistema**: En esta fase, se continúa con la definición del sistema software a desarrollar, tomando como punto de partida los requisitos gene

**Lo que dice el material:**
> Documentar los requisitos del sistema • Salida: • Casos de uso del sistema (versión detallada). Describen con detalle cómo debe interactuar el sistema con sus usuarios. • Requisitos funcionales. Se deben enunciar a un nivel de detalle suficiente como para que a partir de ellos pueda implementarse una solución

**Lo que dijo el revisor:** (ninguno de los dos revisores lo detectó)

**Qué hay que decidir:** «Esto excluye la definición de casos de uso…». Cambio hecho por mí: «incluye» → «excluye».

**Tu decisión:** P / M / D

---

## Caso 9 — E. Matiz de alcance (¿demasiado pillado?)

**Pregunta del alumno:** ¿Qué es un requisito correcto según el modelo de calidad?

**Texto de la respuesta:**
> Un requisito correcto según el modelo de calidad debe cumplir varios criterios que aseguren su calidad y utilidad. Según las fuentes proporcionadas, un requisito correcto debe ser:

**Lo que dice el material:**
> • Modelo de calidad para la especificación de requisitos: • Correcta. Acorde a la estructura y contenidos. • Completa. Contempla todo lo que se conoce que debe hacer el sistema software a desarrollar • Consistente internamente. No contiene contradicciones internas ni redundancias innecesarias • Consistente externamente

**Lo que dijo el revisor:** La fuente menciona 'Correcta' como criterio para la especificación de requisitos, no para cada requisito individual. La respuesta asume que 'correcto' es un requisito individual, lo que altera la atri

**Qué hay que decidir:** La fuente aplica «correcta» a la especificación completa; la respuesta lo aplica a cada requisito.

**Tu decisión:** P / M / D

---

## Caso 10 — E. Matiz de alcance (¿demasiado pillado?)

**Pregunta del alumno:** ¿Qué es un requisito realizable y qué relación tiene con el coste?

**Texto de la respuesta:**
> Un requisito realizable es aquel que puede ser implementado mediante tecnología existente y con un coste que sea asumible dentro del contexto del proyecto. Este requisito debe cumplir con ciertos criterios para ser considerado realizable, como ser comprensible, no ambiguo, gramaticalmente correcto y ortográficamente correcto. Además, debe ser posible definir pruebas para comprobar su cumplimiento, y estas pruebas deb

**Lo que dice el material:**
> • Gramaticalmente correcto. • Ortográficamente correcto. • Realizable. Puede implementarse mediante tecnología existente y con un coste asumible • Comprobable. Se pueden definir una o más pruebas, de coste y tiempo razonables. • Trazado. Las dependencias del requisito están trazadas hacia otros requisitos o casos de u

**Lo que dijo el revisor:** La definición incluye características adicionales (comprensible, no ambiguo, etc.) que no forman parte del concepto de 'realizable' según la fuente, que solo menciona 'coste asumible' y tecnología exi

**Qué hay que decidir:** La respuesta lista como parte de «realizable» propiedades que la fuente define aparte.

**Tu decisión:** P / M / D

---
