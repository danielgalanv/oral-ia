# Ampliación documental web del autoestudio

Versión 1 — 30-10-2026. Autorización humana y constitución 2.0.0.
**Contrato de desarrollo; sin implementación ni acceso web activo en las sesiones actuales.**

## Flujo

1. Recuperar material docente vigente dentro de la actividad y comprobar qué parte de la
   pregunta sigue sin respaldo. Un ranking bajo no demuestra insuficiencia ni exclusión.
   La clasificación/valoración semántica sigue requiriendo evidencia de funcionamiento.
2. Si falta información, comprobar permiso web por actividad, alcance y presupuestos.
   Informar «Voy a consultar información de Internet para completar esta explicación».
   Con permiso ausente/retirado, consulta no segura o tema excluido, no hacer la petición.
3. Construir una consulta mínima sobre el concepto, sin copiar la conversación, datos
   personales, archivos del profesor o datos de alumnos. No se consulta una API externa de
   generación; extracción, contraste y generación siguen locales.
4. Buscar/descargar documentación pública pertinente, dando prioridad a fuentes originales
   identificables. Conservar título, autor/entidad, URL, fecha de consulta, edición/fecha de
   publicación disponible, fragmentos exactos y hash de la captura. Un snippet del buscador
   no sustituye al documento. Respetar condiciones de acceso/uso, sin eludir restricciones.
5. Valorar por separado el respaldo de las afirmaciones externas: autoría, contexto,
   aplicabilidad y vigencia cuando importe. Si hay controversia o respaldo incierto,
   contrastar otras fuentes independientes; copias/sitios que citan el mismo origen no
   equivalen a corroboración independiente. No exigir un número fijo de sitios por regla.
6. Comparar las afirmaciones candidatas con el material docente vigente pertinente,
   buscando pasajes complementarios del tema y páginas vecinas cuando corresponda,
   no solo el primer top-k usado para redactar. Registrar lo revisado y los huecos de
   extracción/cobertura. Distinguir matiz de terminología/contexto de contradicción real.
7. Generar la explicación desde evidencia permitida y revisarla por separado. Mostrar
   qué procede del material docente y qué es ampliación externa, con «Información de
   Internet» y enlaces legibles. Citar no prueba que la revisión esté superada.

## Resultado del contraste

La revisión emite dos decisiones separadas y trazables:

- **Respaldo externo:** sustentado, rechazado o incierto, con pasajes y motivo observable.
- **Compatibilidad docente:** compatible con lo revisado, conflicto o incierto,
  identificando versiones/pasajes docentes comparados y límites de cobertura.

HTTP 200, dominio reputado, consenso aparente de páginas o autocrítica del generador no
constituyen por sí solos esas decisiones. La validez de un texto externo y su coherencia
con el curso son preguntas distintas. La implementación deberá medir falsos permisos,
falsos conflictos y cobertura antes de atribuirse capacidad de validación semántica.

Un conflicto o incertidumbre no resueltos impiden presentar la afirmación afectada como
explicación establecida de la asignatura. ORALIA puede advertir «La fuente externa plantea
una diferencia con el material de clase; no la doy por resuelta» y mostrar la procedencia
relevante para aclaración/revisión docente. No sustituye silenciosamente al profesor ni
afirma que el material docente es infalible. La parte de la pregunta con respaldo puede
contestarse sin incorporar la afirmación conflictiva.

«Compatible con lo revisado» no garantiza compatibilidad con páginas que no se han podido
leer o documentos ausentes. Si el hueco es decisivo para responder, comunicar el límite.
Un fallo de búsqueda, revisión o red conserva la conversación y no inventa una respuesta.

## Controles de ejecución

La política versionada de actividad especificará permiso, alcance de fuentes y presupuestos
finitos de búsquedas/páginas/bytes/tiempo/reintentos. Defaults offline. Cada descarga revalida
permiso y destino, incluidos redirects; rechaza destinos privados/locales, protocolos no
permitidos e instrucciones operativas incluidas en páginas. Cancelación, retirada y entrega
tardía siguen sujetas a controles del host. La caché es versionada y revocable, no material
docente aprobado automáticamente. No se alteran sesiones existentes ni se hereda permiso
web al examen. La presentación debe informar del acceso externo antes de utilizarlo.

## Pruebas requeridas y alcance de esta entrega

Empezar con transportes HTTP simulados en CPU: complemento compatible; afirmación externa
respaldada pero contradictoria; contradicción en una página docente fuera del top-k inicial;
dos formulaciones compatibles con distinta terminología; incertidumbre; fuente falsa o
duplicada; inyección; extracción incompleta; URL no pública/redirect; consulta con datos
personales; permiso retirado/cancelación y red caída. Verificar atribución, procedencia,
preservación de contexto y bloqueo de la afirmación afectada, no solo formato de recibo.

Estos controles CPU no acreditan por sí mismos revisión semántica real. T114–T118 permanecen
pendientes hasta su implementación y evidencia; no se activa red, publicación o GPU al
guardar este contrato. Las pruebas y perfiles históricos permanecen bajo sus condiciones
originales y no se reinterpretan como si hubieran usado Internet.
