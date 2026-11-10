# T186 — presentación y traducción, implementadas y comprobadas

El caso observado de JSON visible está corregido. El PDF original dice **Completeness**; la etiqueta **Complejidad** se introdujo en la respuesta del modelo, no en ese documento. No se modificaron fuentes docentes ni respuestas históricas.

- [Dos respuestas nuevas y vista de B3 sin envoltura](responses-mobile.html).
- [Transcripción de las dos generaciones nuevas](run-20261101-223243/transcript.md).
- [Resultados originales y trazas](run-20261101-223243/result.json).
- [Contraste con el PDF original](terminology-source-check.json) y [texto de la página 73](original-page-73.txt).
- [Aceptación humana acotada](user-review.json).

## Cambios

`academic_presentation.py` extrae únicamente un objeto JSON completo con la clave única mensaje_mostrado y un cuerpo de texto no vacío. No repara sintaxis, no admite claves duplicadas o campos adicionales en esa envoltura, ni elimina contenido académico. Los ejemplos de JSON dentro de texto o bloques de código se conservan. Los formatos ambiguos de la envoltura reconocida no llegan al historial.

`DiagnosticStudy` conserva outcome y raw_candidate originales, y entrega el texto de presentación. Solo ese texto entra al historial tras acknowledge. `WebReviewRounds` conserva las versiones y recibos brutos, registra presentaciones y envía al revisor el cuerpo que se mostrará. Las correcciones, si las hubiera, se comparan también por el contenido visible.

Se añadió el perfil optativo study-dialogue/v2, conservando v1 y los perfiles sin selección. V2 pide texto sin envolturas y una traducción conservadora de denominaciones técnicas, manteniendo el original cuando haya duda. No contiene una respuesta docente predefinida ni un diccionario especial con el término esperado. El proveedor docente real usa v2; los frames se reconstruyen y validan en el worker como antes. No se reemplaza Complejidad por Completitud automáticamente después de generar.

Se modificaron seis módulos de producción, se añadió un archivo de pruebas y se actualizó la expectativa del perfil del proveedor real en otro. No hubo cambios de UI, SQL o migraciones.

## Pruebas

Dos regresiones del fallo fallaron antes de la implementación y pasaron después. Los quince casos focales incluyen el B3 íntegro conservado, la entrega e historial, preservación del bruto, rechazo de envolturas ambiguas, ejemplos de JSON académico intactos, mantenimiento de v1 y transporte real del frame v2 con rechazo de una degradación de perfil.

La regresión ampliada terminó con **646 pruebas aprobadas y una omitida**: tests/course_dialogue, tests/unit/test_study_lab.py y tests/integration/test_real_course_diagnostic.py. La omitida requiere la variable optativa ORALIA_REAL_COURSE_DIAGNOSTIC; esta ejecución realizó por separado el ensayo GPU descrito abajo. Se conserva la advertencia existente de Starlette/httpx. Black y Ruff focales pasan. Ruff global mantiene diez diagnósticos previos y cero nuevos, comparados con multiplicidad.

El primer intento CPU restringido se interrumpió porque quedó bloqueado; la reproducción fuera del entorno restringido terminó con los dos fallos esperados. El primer preflight del arnés breve también se detuvo antes de cargar modelos por un contador copiado que todavía exigía doce IDs distintos. Se conservó esa versión, se corrigió y se comprobó que admite dos IDs únicos y rechaza duplicados. Ninguno consumió llamadas de modelo.

## Comprobación real

Dos turnos nuevos, una misma conversación sobre una aplicación de seguimiento de incidencias; RAG real e índice derivado aislado. Las preguntas preparadas por el coordinador están en questions.json. El usuario autorizó ejecutar la comprobación breve; no se afirma que validara individualmente esas dos redacciones.

Cuatro llamadas completas: dos generaciones Qwen2.5-14B NF4 y dos revisiones Qwen3-8B con razonamiento. Perfil v2 registrado en ambas generaciones y modo thinking comprobado en las revisiones. 1644 tokens nuevos, incluido razonamiento; suma de latencias 100,451 segundos. Sin truncamientos, deadlines o correcciones de contenido. El historial del segundo turno contiene exactamente la primera respuesta mostrada.

Ambas respuestas llegaron como texto normal y utilizaron **completitud (completeness)** y **consistencia (consistency)**. La extracción de la envoltura observada se acredita con los casos CPU, incluido el registro B3 real; las nuevas generaciones no requirieron extraer JSON. El resultado no garantiza todas las traducciones futuras ni demuestra una mejora semántica general. No se introdujeron críticas humanas ni respuestas esperadas en las peticiones al modelo.

## Preservación y alcance

Los grupos históricos de 308, 140 y 22 archivos conservan sus hashes. Los tres recibos B2/B3/B4 originales también permanecen intactos. Los 262 archivos congelados del nuevo ensayo están archivados y verificados. Los dos árboles propios del modelo terminaron; GPU final 0 %, aproximadamente 1 GB usado y 31 GB libres. T permanece detenido.

La revisión del usuario de B2/B3/B4 quedó registrada con las dos salvedades acordadas. Las observaciones sobre media, extensión u otras mejoras opcionales no bloquean esos casos ni se contabilizan como respuestas incorrectas. No se ha extendido esa aceptación a todos los casos o a fiabilidad general.

T186 queda completada en su alcance. Feature 012 y los pendientes semánticos previos continúan abiertos. No hubo publicación, apertura de participantes o gates, Reset ni commits.
