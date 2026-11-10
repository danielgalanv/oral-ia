# Snapshot explícito de autoestudio — v1

GET `/api/v1/study-lab/export?format=json|markdown`, misma autorización docente/inspección y sesión vigente que el chat. Respuesta attachment, `Cache-Control: no-store`; no recibe rutas de archivo o destinatarios. Sin sesión/permiso vigente no entrega datos.

Formato JSON `oralia-study-report/v1`: código seudónimo propio de sesión, fecha UTC, curso/actividad/paquete/revisión, proveedor identificado, estado semántico no aprobado, intentos completados, respuestas mostradas/con Internet/no mostradas, preguntas repetidas por espacio/casefold y turnos ordenados. Un intento sin confirmación no exporta su respuesta ni fuentes internas. Las respuestas mostradas incluyen texto y referencias legibles. No incluye bruto, razonamiento, trace privado, notas/rúbricas, clasificación semántica de conceptos o audio.

Markdown contiene los mismos intercambios legibles con bloques de texto cercados más largos que cualquier secuencia de backticks del contenido, para no tratar HTML o código aportado como estructura ejecutable. JSON/Markdown son copias explícitas descargadas al navegador, no un almacén nuevo del backend. El cierre/expiración purga la sesión en el servidor; no puede eliminar las copias descargadas. La interfaz informa de ello y ofrece continuar sin descartar.

Contar usos o repeticiones no acredita aprendizaje. Exportar no genera/resuelve preguntas, cambia gates, renueva cupos ni confirma como mostrados candidatos pendientes. Los límites técnicos temporales y experimentales explícitos permanecen; el autoestudio no hereda el límite histórico de 32 intentos diagnósticos.
