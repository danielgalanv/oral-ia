# Prueba por navegador: recorrido de autoestudio

Respuestas reales sin reescritura. Pregunta, ejemplo, aclaración y cambio explícito de tema.

## 1. ¿Cómo se utilizan las entrevistas para descubrir requisitos?

Las entrevistas son una herramienta importante en el proceso de descubrimiento de requisitos en ingeniería de software. Se utilizan principalmente para obtener una comprensión general de lo que los interesados (stakeholders) hacen y cómo podrían interactuar con el sistema. Aquí te explico cómo se utilizan las entrevistas para este propósito:

1. **Método Mixto de Entrevistas**: Generalmente, las entrevistas combinan preguntas cerradas y abiertas. Las preguntas cerradas permiten obtener respuestas específicas y directas, mientras que las preguntas abiertas facilitan una discusión más amplia y exploratoria.

2. **Entrevistas Formales e Informales**: Estas pueden ser formales, basadas en una lista preestablecida de preguntas, o informales, donde se exploran diversos temas con los interesados. Ambos tipos tienen sus ventajas: las formales aseguran que se cubran todos los puntos importantes, mientras que las informales permiten una mayor flexibilidad y profundización en áreas específicas según sea necesario.

3. **Objetivo Principal**: Las entrevistas buscan entender el dominio de aplicación, los servicios que el sistema debería proporcionar y las restricciones operativas del sistema. Esto implica trabajar con clientes y otros interesados para recopilar información sobre el entorno en el que funcionará el sistema.

4. **Límites de las Entrevistas**: Aunque las entrevistas son útiles para obtener una comprensión general, no son adecuadas para entender los requisitos específicos del dominio. Los ingenieros de requisitos pueden tener dificultades para comprender la terminología específica del dominio, y algunos conocimientos del dominio pueden ser tan familiares que resulta difícil para las personas expresarlos claramente.

5. **Efectividad en las Entrevistas**: Es crucial ser abierto de mente durante las entrevistas, evitar prejuicios y estar dispuesto a escuchar a los interesados. Se puede utilizar una pregunta inicial (springboard question), una propuesta de requisito o trabajar juntos en un prototipo del sistema para iniciar y mantener la conversación.

### Ejemplo Hipotético

Supongamos que estás trabajando en un proyecto de software para una empresa de logística. Durante las entrevistas con los gerentes de operaciones, descubres que necesitan un sistema que les permita rastrear el estado de los envíos en tiempo real. Sin embargo, también encuentras que hay ciertos términos relacionados con el transporte que los gerentes consideran obvios y no creen necesario explicarlos detalladamente. Por ejemplo, "entrega rápida" podría ser un término que asumen que todos entienden, pero que en realidad podría requerir una definición más precisa para garantizar que el sistema cumpla con sus expectativas.

Este ejemplo ilustra cómo las entrevistas pueden ayudar a identificar necesidades generales y a generar una comprensión básica del uso del sistema, pero también muestra que es posible que se omitan detalles importantes debido a la familiaridad con el dominio.

En resumen, las entrevistas son valiosas para obtener una visión general de los requisitos y las interacciones del sistema, pero deben complementarse con otras técnicas para capturar los detalles específicos del dominio.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
- 5 - Requisitos.pdf, p. 87: Key points
- 5 - Requisitos.pdf, p. 54: Requirements elicitation
## 2. Ponme un ejemplo de preguntas para el responsable de una biblioteca que quiere un sistema de préstamos.

Para el responsable de una biblioteca que busca implementar un nuevo sistema de préstamos, las entrevistas son una excelente herramienta para descubrir los requisitos necesarios. Aquí tienes algunas preguntas que podrías realizar:

1. **Cierre de tipo cerrado**:
   - ¿Cuáles son los principales problemas que enfrentan actualmente con el sistema de préstamos?
   - ¿Qué características debe tener el nuevo sistema para mejorar la eficiencia en la gestión de préstamos?
   - ¿Cuánto tiempo lleva en promedio procesar un préstamo desde que el usuario lo solicita hasta que se entrega el libro?

2. **Tipo abierto**:
   - ¿Cómo ve usted el futuro del sistema de préstamos en la biblioteca? ¿Qué cambios espera ver en los próximos años?
   - ¿Qué aspectos del sistema actual le gustaría mejorar o eliminar?
   - ¿Qué tipo de información adicional le gustaría tener disponible en el sistema de préstamos?

Estas preguntas combinan tanto preguntas cerradas como abiertas para obtener una comprensión completa de las necesidades del responsable de la biblioteca. Las preguntas cerradas permiten obtener respuestas específicas y directas, mientras que las preguntas abiertas permiten una discusión más amplia y exploratoria.

Además, es importante ser abierto de mente durante estas entrevistas, evitar prejuicios y estar dispuesto a escuchar al responsable de la biblioteca. También se puede utilizar una pregunta inicial (springboard question) o trabajar juntos en un prototipo del sistema para iniciar y mantener la conversación.

Por ejemplo, podrías comenzar la entrevista con una pregunta inicial como "¿Cuál es el objetivo principal que desea alcanzar con el nuevo sistema de préstamos?" Esto podría ayudarte a entender mejor las necesidades y expectativas del responsable de la biblioteca antes de entrar en detalles más específicos.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 54: Requirements elicitation
- 5 - Requisitos.pdf, p. 57: Requirements discovery
## 3. No entiendo por qué no basta con hacer esas preguntas. Explícamelo de otra manera.

Las entrevistas son una técnica útil para descubrir los requisitos necesarios para desarrollar un nuevo sistema de préstamos en una biblioteca, pero no son suficientes por sí solas. Aquí te explico por qué:

1. **Limitaciones en la Comprensión del Dominio**: Las entrevistas pueden ayudar a obtener una comprensión general de lo que los responsables de la biblioteca desean en un nuevo sistema de préstamos. Sin embargo, pueden fallar en capturar detalles específicos del dominio. Por ejemplo, el responsable de la biblioteca puede asumir que ciertos términos relacionados con el préstamo, como "renewal" (prórroga) o "overdue" (atraso), son conocidos por todos y no necesita explicarlos detalladamente. Esto puede llevar a que estos términos queden ambiguos o mal interpretados por los ingenieros de requisitos.

2. **Ambigüedad en las Respuestas**: Durante las entrevistas, los responsables de la biblioteca pueden expresar sus necesidades utilizando términos que ellos consideran claros, pero que pueden ser ambiguos para los ingenieros de requisitos. Por ejemplo, si el responsable dice "queremos que el sistema facilite la búsqueda de libros", esto puede ser interpretado de diferentes maneras. ¿Significa buscar por título, autor, género, ubicación física, etc.? La ambigüedad en las respuestas puede llevar a requisitos imprecisos que luego causen problemas durante el desarrollo del sistema.

3. **Necesidad de Complementar con Otras Técnicas**: Las entrevistas son solo una parte del proceso de recolección de requisitos. Para obtener una comprensión completa y precisa de los requisitos, es necesario complementarlas con otras técnicas como análisis de documentos existentes, observación directa de las operaciones actuales, y reuniones con múltiples partes interesadas. Estas técnicas pueden ayudar a llenar los vacíos que las entrevistas pueden dejar.

4. **Cambios en los Requisitos**: Durante el proceso de análisis, los requisitos pueden cambiar debido a factores organizacionales, políticos, o simplemente porque nuevas partes interesadas emergen o el entorno de negocio cambia. Las entrevistas realizadas al inicio del proyecto pueden no reflejar completamente los requisitos finales del sistema.

Por lo tanto, aunque las entrevistas son una herramienta valiosa para obtener una comprensión general de los requisitos, es necesario utilizar otras técnicas para asegurarse de que los requisitos sean precisos y completos.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
- 5 - Requisitos.pdf, p. 53: Problems of requirements elicitation
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
## 4. Ahora cambiamos de tema: ¿qué es un requisito no funcional? Ponme un ejemplo.

Un requisito no funcional es una característica o propiedad del sistema que no se relaciona directamente con las funciones específicas que debe realizar, sino con cómo debe realizarlas. Estos requisitos definen propiedades y restricciones del sistema, como la confiabilidad, el tiempo de respuesta, los requerimientos de almacenamiento, entre otros.

Por ejemplo, supongamos que estás desarrollando una aplicación web que permite a los usuarios buscar información sobre productos. Un requisito funcional podría ser que la aplicación debe permitir a los usuarios buscar productos por nombre. Sin embargo, un requisito no funcional sería que la aplicación debe responder a las consultas de búsqueda en menos de dos segundos. Este requisito no especifica ninguna función específica del sistema, sino que establece una condición sobre el rendimiento del sistema.

Este tipo de requisito puede ser crucial para el éxito del sistema, ya que si no se cumple, el sistema podría ser inútil o insatisfactorio para los usuarios, incluso si todas las funciones funcionan correctamente. Por ejemplo, si la aplicación tarda demasiado en responder, los usuarios podrían perder la paciencia y abandonarla.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 16: Non-functional requirements implementation
- 5 - Requisitos.pdf, p. 15: Non-functional requirements
- Ch4 Req Eng.pptx, p. 19: Non-functional requirements
- nasa-handbook.pdf, p. 70: NASA §4.2 Technical Requirements Definition
- 5 - Requisitos.pdf, p. 20: Goals and requirements
