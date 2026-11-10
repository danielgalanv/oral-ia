# Feature 002 — Materiales autorizados y RAG trazable

Añade a ORAL-IA la gestión de materiales docentes autorizados y un sistema local de recuperación documental que proporcione evidencias estructuradas a los agentes sin permitir acceso abierto a Internet.

## Propósito

El sistema debe responder a consultas sobre una asignatura a partir de una base de conocimiento controlada por el profesorado, conservar la procedencia de cada fragmento y detectar cuándo la evidencia es insuficiente, está desactualizada o entra en conflicto.

## Usuarios y objetivos

### Profesor

Debe poder crear una colección de una asignatura, cargar documentos, revisar su estado de procesamiento, activar o desactivar materiales, asignarlos a actividades, sustituir versiones, bloquear contenidos incorrectos y reconstruir el índice.

### Agentes consumidores

Deben poder solicitar evidencias mediante una consulta estructurada limitada a una sesión, asignatura, actividad y conjunto de materiales autorizados.

### Participante

Debe poder ver las fuentes utilizadas en una respuesta de forma comprensible, sin acceder a materiales o fragmentos no autorizados para su actividad.

## Materiales iniciales admitidos

La versión mínima debe aceptar PDF textual, DOCX, PPTX, TXT y Markdown. Los documentos escaneados sin texto y el OCR avanzado pueden quedar fuera, pero el sistema debe identificarlos como no procesables en vez de indexarlos silenciosamente de forma incompleta.

## Proceso de incorporación

1. Recepción del archivo y validación de formato, tamaño e integridad.
2. Cálculo de identificador de contenido para evitar duplicados accidentales.
3. Extracción de texto conservando referencias a página, diapositiva, sección o párrafo cuando sea posible.
4. Segmentación configurable y reproducible.
5. Generación de metadatos.
6. Creación local de embeddings.
7. Indexación local.
8. Comprobaciones de cobertura y errores.
9. Estado de revisión y activación manual.

Un documento no puede utilizarse en sesiones hasta que esté procesado y activo.

## Metadatos mínimos

Cada documento y fragmento debe incluir: identificador, documento de origen, versión, hash, página/diapositiva/sección, tipo de contenido, asignatura, actividad, fecha de incorporación, estado de autorización, vigencia, prioridad, idioma y estado de indexación.

## Recuperación

El agente de recuperación debe recibir una consulta, filtros de autorización, número máximo de fragmentos y presupuesto temporal. Debe devolver fragmentos, procedencia, relevancia, metadatos, versión del índice, advertencias y posibles conflictos.

No puede devolver fragmentos de otra asignatura, actividad, versión retirada o material inactivo. La recuperación debe poder repetirse utilizando la misma configuración y versión del índice.

## Fundamentación

El verificador debe poder clasificar una propuesta como fundamentada, parcialmente fundamentada, no fundamentada, conflictiva o no verificable. Debe indicar qué afirmaciones poseen soporte, cuáles carecen de él y si las referencias realmente contienen la información atribuida.

Cuando la configuración prohíba conocimiento general, una respuesta sin evidencia suficiente debe reconocer la limitación o solicitar aclaración. Cuando lo permita, el contenido general debe diferenciarse explícitamente de lo recuperado.

## Escenarios prioritarios

### Escenario A — Documento autorizado

El profesor carga un documento, revisa su procesamiento, lo activa para una actividad y una consulta recupera fragmentos correctos con referencia a su ubicación de origen.

### Escenario B — Material retirado

El profesor desactiva o sustituye una versión. Las sesiones nuevas no recuperan fragmentos de la versión retirada y el registro indica la nueva versión activa. Las sesiones antiguas conservan la referencia histórica necesaria para ser auditadas.

### Escenario C — Sin evidencia suficiente

Una consulta no tiene cobertura en los materiales permitidos. El recuperador lo indica y el sistema evita generar una respuesta específica presentada como fundamentada.

### Escenario D — Conflicto entre fuentes

Dos materiales activos contienen afirmaciones incompatibles. La recuperación devuelve ambas evidencias y marca el conflicto para que el diálogo lo comunique o solicite revisión docente.

### Escenario E — Aislamiento de autorización

Una consulta de una actividad intenta acceder a un documento de otra actividad o asignatura. El filtro impide la recuperación y el intento queda registrado.

### Escenario F — Fallo de indexación

Un archivo no se puede extraer o indexar. El profesor recibe un error accionable, el documento no se activa y el índice anterior sigue siendo utilizable.

## Fuera de alcance

- acceso web y búsqueda externa;
- OCR avanzado de documentos escaneados;
- generación automática de material docente;
- modificación de documentos originales;
- evaluación de la calidad académica del participante;
- recomendación longitudinal personalizada.

## Criterios de éxito

- Todos los fragmentos recuperados pueden atribuirse a documento, versión y ubicación.
- Ningún material inactivo o no autorizado aparece en resultados de una sesión.
- La sustitución de versiones no deja fragmentos activos obsoletos.
- Las consultas sin evidencia suficiente generan una señal explícita y trazable.
- El verificador detecta referencias que no respaldan la afirmación atribuida en el conjunto de pruebas preparado.
- El índice puede reconstruirse sin perder la relación entre documentos, fragmentos y versiones.
