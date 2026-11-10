# T206–T209 — incremento CPU de autoestudio

03-11-2026, Europe/Madrid. Terminados los cuatro bloques autorizados: pasajes web largos, catálogo, informes y conciliación de pendientes. **Sin GPU ni inferencias reales de generador/revisor en CPU.** Hubo cinco descargas públicas reales y reproducción offline de sus bytes; las decisiones semánticas y respuestas del chat en las pruebas son dobles explícitos.

La entrega mejora la operación del piloto, no acredita aún la calidad académica de la conversación. Feature 012, T191 y las aceptaciones semánticas/humanas permanecen abiertas.

## Páginas largas

`web_passages.py` reutiliza la normalización y términos del recuperador existente, con ventanas literales y contexto vecino. Mantiene offsets y hashes de cada tramo, hash del texto completo y rangos omitidos. Los pasajes no contiguos se separan visiblemente en el contexto; no se reescribe su contenido ni se finge haber enviado todo el documento. El presupuesto externo conjunto sigue siendo 8.000 caracteres, incluyendo metadatos; ya no se descarta una página completa solo por superar 6.000.

`web_evidence.py` anota rangos de contenido `<main>` cuando existen. No cambia el texto extraído anterior ni su hash: navegación y cuerpo siguen en la captura original, mientras la selección prioriza el cuerpo y registra lo omitido. Las páginas sin `<main>` conservan la vía general. No se deduce verdad, suficiencia o pertenencia al curso del ranking léxico.

Las pruebas encuentran una afirmación tardía y conservan su advertencia adyacente. Un átomo que no pueda entrar sin cortarse se omite explícitamente; no se convierte en exclusión del temario. Siguen activos los controles de respaldo/compatibilidad, retirada y revisión final de T205.

[Selección final de las cinco capturas](selection-final-001/summary.json): los originales van de 4.723 a 151.884 caracteres; los contextos seleccionados quedan dentro del presupuesto. Se verificaron sus tramos contra la extracción y los hashes originales, sin descargar de nuevo. Es evidencia de selección y procedencia, no una evaluación semántica exhaustiva.

## Catálogo original acotado

[Política de laboratorio v2](policy-requirements-lab-v2.json): seis conceptos configurados y cinco originales:

- [NASA, Technical Requirements Definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/).
- [NASA, Product Validation](https://www.nasa.gov/reference/5-4-product-validation/).
- [NASA, Crosscutting Technical Management](https://www.nasa.gov/reference/6-0-crosscutting-technical-management/).
- [Ian Sommerville, Requirements and Design, St Andrews, 2011](https://archive.cs.st-andrews.ac.uk/STSE-Handbook/RequirementsandDesign/).
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt), sin presentar como incluida su actualización RFC 8174.

Las tres páginas NASA pertenecen al mismo manual, no son tres verificaciones independientes. Su ámbito es ingeniería de sistemas; el capítulo de Sommerville se centra en trabajo de campo y prototipado para obtener requisitos. El catálogo no cubre toda la asignatura ni todo Internet.

[Adquisición real](public-acquisition-001/summary.json): cuatro casos, cinco documentos, todos `acquired_unreviewed`; sin fallos de adquisición registrados. Los recibos conservan capturas completas, URLs, entidades, versiones declaradas, fechas, bytes y hashes. La insuficiencia que permitió esta prueba fue una decisión de fixture, no un juicio de un modelo real ni de un alumno.

[Replay por el chat conectado](replay-001/result.json): bytes originales de NASA/RFC, extracción y selección actuales, aviso/controles y generación simulados; dos fuentes llegaron al generador dentro del límite conjunto (7.975 caracteres). Cero peticiones nuevas de red y cero inferencias. No se mostraron menús de actualidad de NASA como evidencia seleccionada en ese caso.

[Descubrimiento y límites de acceso](source-discovery.md) registra las rutas del libro no accesibles en la herramienta web y la alternativa primaria de St Andrews. No se usaron copias de terceros ni se eludieron restricciones de INCOSE. La política nueva es explícita por actividad de autoestudio y no modifica políticas o sesiones anteriores. No activa red por defecto ni examen.

## Exportación del piloto

En **Finalizar** aparecen **Descargar sesión JSON** y **Descargar sesión Markdown**. Se puede descargar y elegir **Seguir estudiando**, o confirmar el descarte. La vista principal sigue teniendo pregunta, respuesta y controles básicos.

El snapshot incluye código seudónimo propio de sesión, fecha UTC, curso/actividad/paquete, proveedor identificado, preguntas, respuestas confirmadas como mostradas, fuentes y conteos descriptivos. Los fixtures quedan identificados como tales y no se declaran aprobaciones semánticas. Cuenta intentos completados, respuestas mostradas, respuestas con Internet e intentos sin respuesta mostrada. Las repeticiones usan únicamente normalización de espacios/mayúsculas: **no clasifica conceptos ni infiere comprensión o aprendizaje**. El profesor puede anotar conceptos después.

No exporta respuestas pendientes no mostradas, bruto, razonamiento, trazas internas, audio o calificaciones. Markdown cerca el texto para que HTML/backticks aportados no se interpreten como estructura ejecutable. La API usa la misma autorización y sesión vigente y responde como descarga con `no-store`. No recibe una ruta de escritura ni crea un almacén nuevo en el servidor. [Contrato](../../../specs/012-conversational-course-study/contracts/study-export.md).

**La copia descargada permanece en el equipo cuando se cierra el programa.** La interfaz lo explica. La conservación/eliminación de esa copia corresponde al ensayo acordado; el cierre sigue purgando la memoria del servidor. Sin descargar no aparece un archivo nuevo de transcripción del programa. Las plantillas CSV siguen siendo manuales.

Una descarga fallida muestra el error dentro del diálogo, conserva la conversación y permite reintentar; la espera está acotada a quince segundos. No consume una pregunta ni ejecuta modelos o adquisición. El foco seguro sigue en Seguir estudiando y se limpian errores de exportación al reabrir el diálogo.

También se corrigió un techo residual de **32 intentos** en `DiagnosticStudy`: el autoestudio ya no lo hereda. La prueba HTTP completa 34 preguntas y confirmaciones. El diagnóstico histórico y los cupos experimentales expresamente activados mantienen sus límites. No equivale a memoria infinita: el contexto y plazos técnicos documentados permanecen.

## Conciliación

[Mapa completo por ID](task-reconciliation.json) y [lectura de pendientes](task-reconciliation.md): 131 IDs anteriores conservan sus estados y se añaden T206–T209. Son 135 IDs en este índice compacto, con 51 abiertos; **no es el total del proyecto ni un porcentaje de aceptación**.

El mapa distingue componentes CPU reutilizables, ensayos históricos, calibración semántica, conversaciones reales y revisión humana. No reinstala formatos abandonados o cambio manual de tema por la redacción de un ensayo antiguo. Se corrigieron referencias activas obsoletas: la excepción web ya fue aprobada por la constitución 2.0.0 y el chat está cableado. No se vuelve a pedir aquella enmienda. No se da por cerrada la obligación completa de tareas antiguas solo porque exista un componente que se solape.

El estado previo íntegro de spec/plan/tasks está en `before/`. No se borraron IDs, resultados negativos, pérdidas históricas o pendientes humanos.

## Verificación

- [Regresión amplia](regression.log): **774 aprobadas**; una advertencia existente de deprecación Starlette/httpx. Diálogo, proveedores, adquisición, límites, recuperación, preparación y nuevas rutas; no toda la suite del proyecto.
- [Dirigidas finales](final-tests.log): **27 aprobadas** sobre informes, pasajes y conexión; ámbito superpuesto con la regresión, no sumar como casos únicos. La identificación del proveedor y las protecciones finales de exportación se verificaron después del refinamiento del snapshot.
- [Interfaz](ui-tests.log): **18 aprobadas**; TypeScript, [build](build-release.log) y [ESLint](lint.log) conformes.
- [Navegador final](browser-003/result.json): descargas JSON/Markdown reales desde el navegador, proveedor fixture identificado, error 503 controlado y reintento, sin llamadas adicionales, foco seguro, móvil de 320 px, continuación y cierre. Las copias quedaron locales y la exportación posterior al cierre fue rechazada. Sin errores JS o accesos públicos desde el navegador. [Móvil](browser-003/mobile-download.png), [escritorio](browser-003/desktop-download.png), [JSON descargado](browser-003/session.json), [Markdown descargado](browser-003/session.md).
- [Preservación y Ruff](final-checks.json): grupos históricos de **308/140/22** archivos intactos, sin sumarlos como únicos; **10 hallazgos existentes y 0 nuevos**, comparados por ruta/código/mensaje con multiplicidad. Black conforme. Puerto 8061 libre, servidores propios detenidos; procesos ajenos intactos.
- [Manifiesto de fuentes finales](release-manifest.json): 25 archivos archivados en `release-source`, incluidos componentes reutilizados, no 25 cambios nuevos. [Concordancia final](archive-verification.json) con el workspace.

Se conservan `passages-red.log` (módulo aún inexistente), el primer montaje de informe rechazado por no estar rotulado como fixture y el fallo de foco de `browser-001`. El primer montaje se corrigió sin debilitar el requisito del proveedor revisado; el foco se corrigió con una referencia explícita. `browser-002` y `browser-003` pasan. No se ocultaron los intentos fallidos.

Se aplicó el flujo de implementación SpecKit al incremento autorizado: prerrequisitos de Feature 012, checklists 8/8, 9/9 y 12/12, lectura de artefactos/contratos y constitución. No hay hooks de extensión configurados. Se ejecutaron pruebas CPU con datos originales de lectura y dobles rotulados; no se cierran las tareas de inferencia real fuera de este alcance. Sin dependencias nuevas, migraciones, Reset, commits, audio o cambios a los paquetes experimentales históricos. No se ejecutó un nuevo ensayo 204: este incremento no modifica sus mecanismos de arquitectura o paquetes congelados.

## Siguiente paso

Cuando se autorice GPU, probar el flujo integrado con los modelos reales, las preguntas ya acordadas, un seguimiento y una ampliación web; conservar fuentes y salidas completas y aplicar el criterio humano vigente. Los ejemplos ficticios coherentes, repetición o mejoras opcionales no deben convertirse en fallos sustantivos. No iniciar otra campaña para volver a demostrar lo ya medido en CPU.

El comando preparado, **no ejecutado aquí porque carga modelos reales**, es:

```powershell
.\scripts\study-chat.ps1 -WebPolicy .\docs\audits\2026-11-03-cpu-completion\policy-requirements-lab-v2.json
```

Las preparaciones anteriores pueden quedar obsoletas por el cambio de código: preparar una nueva sin Reset. Continúan como límites la cuarentena/tablas, los átomos que no caben, la selección léxica y la cobertura acotada del catálogo. La calidad de las respuestas, del revisor y su utilidad con estudiantes siguen necesitando la validación real; no se aprobaron G2, SC001 o publicación.
