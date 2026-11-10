# Autoestudio real: entrevistas para descubrir requisitos

Tres turnos nuevos sin historial anterior. Integración directa, no navegador.

## 1. ¿Cómo se utilizan las entrevistas para descubrir requisitos y qué diferencia hay entre una entrevista abierta y una cerrada?

Las entrevistas son una herramienta clave en la fase de recolección de requisitos en ingeniería de requisitos. Se utilizan para obtener una comprensión general de lo que los interesados (stakeholders) hacen y cómo podrían interactuar con el sistema. Esto incluye entender sus necesidades, expectativas y problemas actuales que el sistema futuro debe resolver.

### Diferencias entre Entrevistas Abiertas y Cerradas

**Entrevistas Cerradas:**
- **Características**: Están basadas en una lista preestablecida de preguntas.
- **Objetivo**: Recopilar información específica y estructurada sobre temas definidos de antemano.
- **Ventajas**: Proporcionan una estructura clara y permiten comparar respuestas entre diferentes entrevistados.
- **Desventajas**: Pueden limitar la profundización en áreas no previstas o menospreciar detalles importantes que no estén en la lista de preguntas.

**Entrevistas Abiertas:**
- **Características**: Permiten explorar diversos temas sin estar limitados a preguntas específicas.
- **Objetivo**: Obtener una comprensión más amplia y detallada de las necesidades y experiencias de los interesados.
- **Ventajas**: Permite descubrir información valiosa que no estaba inicialmente considerada y permite una mayor flexibilidad en la conversación.
- **Desventajas**: Puede ser menos sistemática y puede resultar en una cantidad de información desordenada que requiere más tiempo para analizar.

En resumen, las entrevistas cerradas son útiles para recoger información específica y estructurada, mientras que las entrevistas abiertas son más adecuadas para explorar áreas desconocidas y obtener una comprensión más profunda de las necesidades y experiencias de los interesados. La combinación de ambas técnicas suele ser la más efectiva para obtener una visión completa de los requisitos del sistema.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
- nasa-handbook.pdf, p. 71: NASA §4.2 Technical Requirements Definition
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
## 2. Ponme un ejemplo de preguntas para una entrevista con el responsable de una biblioteca que quiere un sistema de préstamos.

Para realizar una entrevista con el responsable de una biblioteca que busca implementar un nuevo sistema de préstamos, es importante combinar preguntas cerradas y abiertas para obtener una comprensión tanto estructurada como detallada de sus necesidades y expectativas. Aquí te presento algunas preguntas que podrías utilizar:

### Preguntas Cerradas:
Estas preguntas están diseñadas para obtener respuestas específicas y estructuradas.

1. **¿Cuáles son los principales problemas que enfrenta actualmente con el sistema de préstamos existente?**
   - Esta pregunta ayuda a identificar los problemas más urgentes que necesita resolver el nuevo sistema.
   
2. **¿Cuántos préstamos se realizan en promedio por día en la biblioteca?**
   - Esta pregunta proporciona una idea de la escala y frecuencia de los préstamos, lo que es útil para dimensionar el sistema.

3. **¿Qué tipo de información se registra actualmente durante un préstamo?**
   - Esta pregunta ayuda a entender qué datos son relevantes y necesarios para el sistema.

4. **¿Cuál es el plazo máximo para devolver un libro?**
   - Esta pregunta define uno de los parámetros clave del sistema de préstamos.

### Preguntas Abiertas:
Estas preguntas permiten una exploración más libre y detallada de las necesidades y experiencias del responsable.

1. **¿Cómo ve usted el proceso de préstamo idealmente? ¿Qué características debería tener este proceso?**
   - Esta pregunta permite al responsable expresar su visión del proceso de préstamo, lo que puede revelar necesidades y expectativas adicionales.

2. **¿Qué aspectos del sistema de préstamos actuales le gustaría mejorar?**
   - Esta pregunta ayuda a identificar áreas específicas que el responsable considera problemáticas o insatisfactorias.

3. **¿Cómo cree que el nuevo sistema de préstamos podría beneficiar a los usuarios de la biblioteca?**
   - Esta pregunta busca entender las implicaciones del sistema desde la perspectiva de los usuarios, lo que puede revelar necesidades que no se habían considerado antes.

4. **¿Existen restricciones o políticas específicas que deben cumplirse en el nuevo sistema de préstamos?**
   - Esta pregunta ayuda a identificar cualquier reglamento o política que debe ser tenido en cuenta durante la implementación del sistema.

Estas preguntas combinan la obtención de información específica y estructurada con la exploración de áreas más amplias y detalladas, permitiendo una comprensión completa de las necesidades del responsable de la biblioteca.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 53: Problems of requirements elicitation
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
## 3. ¿Por qué no basta con entrevistar a los usuarios para conocer todos los requisitos?

No basta con entrevistar a los usuarios para conocer todos los requisitos debido a varias razones:

1. **Limitaciones en la Compreción del Dominio**: Los usuarios pueden no tener una comprensión completa o no ser capaces de expresar completamente el dominio específico del sistema. Por ejemplo, algunos términos o procesos pueden ser tan familiares para ellos que encuentran difícil articularlos o creen que no merecen ser mencionados. Esto significa que pueden omitir detalles cruciales que son obvios para ellos pero que son vitales para el desarrollo del sistema.

2. **Interpretación Ambigua de los Requisitos**: Los requisitos pueden ser interpretados de maneras diferentes por desarrolladores y usuarios. Un término como "búsqueda" puede tener diferentes significados dependiendo del contexto. Un usuario podría querer buscar el nombre de un paciente en todas las citas de todos los hospitales, mientras que un desarrollador podría interpretarlo como buscar el nombre de un paciente en un solo hospital. Esta ambigüedad puede llevar a malentendidos y a sistemas que no cumplen con las expectativas originales.

3. **Diferencias entre Interesados**: Los diferentes interesados pueden tener requisitos que entran en conflicto entre sí. Además, los interesados pueden no saber exactamente lo que quieren, o pueden expresar sus requisitos en términos propios que no sean claros para el equipo de desarrollo. Esto puede llevar a requisitos inconsistentes o incompletos.

4. **Cambios en los Requisitos**: Durante el proceso de análisis, los requisitos pueden cambiar. Puede surgir nuevos interesados o puede haber cambios en el entorno empresarial que afecten los requisitos. Esto significa que incluso después de una primera ronda de entrevistas, los requisitos pueden evolucionar y requerir revisiones adicionales.

Por estas razones, aunque las entrevistas son una herramienta valiosa para entender las necesidades generales de los usuarios y los interesados, es necesario complementarlas con otras técnicas de recolección de requisitos, como la revisión documental, la observación directa del uso del sistema actual, y la participación de múltiples interesados en el proceso de diseño y análisis de requisitos. Esto asegura una comprensión más completa y precisa de los requisitos del sistema.

Fuentes consultadas:
- 5 - Requisitos.pdf, p. 60: Interviewing
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
- 5 - Requisitos.pdf, p. 53: Problems of requirements elicitation
- 5 - Requisitos.pdf, p. 52: Requirements elicitation and analysis
