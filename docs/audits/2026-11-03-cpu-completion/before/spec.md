# Feature Specification:012 — Autoestudio conversacional de Ingeniería del Software

Created:2026-10-22. Status:especificación aclarada; implementación autorizada, sin commits. Sucesora de011: no modifica su aceptación extractiva ni sus evidencias.

## User Scenarios & Testing

### User Story1 — Explicación y transferencia (P1)

El participante pregunta con saludo, recibe explicación qué/porqué/cómo pertinente y un ejemplo derivado después de la explicación. Al no entender recibe otra estrategia, conserva el referente y una pregunta concreta para comprobar comprensión. Errores/rectificaciones se tratan sin nota ni inferencia académica.

Independent test: conversación real sobre la asignatura, seguimiento condicionado a la salida realmente emitida, dudas repetidas, error y cambio de foco. Oráculo de pertinencia/contenido/contexto/estado separado de grounding/autorización; puede fallar aunque estos aprueben.

Acceptance: distinguir validación de calidad/pruebas; responder a conflicto de requisitos sin limitarse al objetivo general; no sustituir explicación por cita de otro asunto; decir límite cuando no haya respaldo.

### User Story2 — Fuentes y límites visibles sin pantalla (P1)

Participante escucha/lee controles, orientación y fuentes en lenguaje comprensible, sin cascada de menús. Diferencia cita, paráfrasis y ejemplo hipotético. No se atribuye contenido derivado literalmente a una diapositiva.

Independent test: fuentes originales por página/versiones, preguntas ambiguas con aclaración concreta, instrucción maliciosa en material o entrada, controles y cierre/retención existentes.

### User Story3 — Capacidad local revisable (P1)

Usuario dispone de entorno propio, comando e informe de primeras respuestas completas. Si un recurso o gate impide publicar un tutor se informa de la causa observada; una candidata de laboratorio no se anuncia como salida aprobada al participante.

Independent test: original011/entornos/procesos intactos; candidato local real sin descargas, metadatos del proveedor, intentos congelados y primeros fallos; sin bandera de revisión humana inferida.

## Requirements

- **FR-001**: Explicar qué/porqué/cómo según duda concreta, con ejemplo pertinente después de explicación y pregunta de comprensión no calificadora cuando corresponda.
- **FR-002**: Mantener referente, objetivo/pregunta pendiente/transición; variar estrategia ante incomprensión y responder a errores/rectificaciones sin evaluar capacidad.
- **FR-003**: Atender saludo compuesto y aclarar ambigüedad concreta; orientación/fuentes/controles comprensibles sin pantalla. Texto solo acredita lógica; voz requiere prueba separada.
- **FR-004**: Fundamentar en PDF docente autorizado, un formato por documento; permitir Requisitos/Procedimiento/Testing según objetivos, con páginas originales, incidentes y versiones; excluir datos personales/evaluación histórica y alumnos.
- **FR-005**: Distinguir citas/paráfrasis/ejemplos didácticos derivados y sus testigos de fuente. No confiar en la salida del generador como evidencia ni atribuir revisión docente a validación técnica.
- **FR-006**: Conservar T090/T150, consentimiento/retención/privacidad, acceso y sesiones. No publicar texto libre mediante ranura confiable inventada ni debilitar verificador para pasar caso.
- **FR-007**: Investigar capacidad finita/determinista frente a transferencia; implementar capacidad generativa local y puertas si se necesita, usando recursos realmente instalados sin descargas ni nube. Generador propone, no autoriza.
- **FR-008**: Publicación generativa requiere G2 explícito: contrato/verificación de afirmaciones, proveedor real, tres ejecuciones por caso y revisión independiente. G3/G4 y gates históricos no se infieren. Fallo de gate conserva perfil no disponible y evidencia de candidata separada.
- **FR-009**: Congelar nuevas conversaciones/oráculos antes de ajustar; preservar primeras divergencias, marcar reserva expuesta, continuar según salidas reales y no simular éxitos.
- **FR-010**: Entorno propio utilizable, aislamiento de recursos/procesos/credenciales, operación única, cierre/cancelación y comando claro; no Reset/commits ni activación de material habitual.
- **FR-011**: Entregar transcriptos completos manejables, tabla tarea→evidencia, archivos, comandos/resultados exactos y límites. Preservar011 y paquetes anteriores, T061/T067 abiertos.
- **FR-012**: Regresiones proporcionadas/global si compartido, Black/Ruff estructural con multiplicidad contra baseline durable, paquetes experimentales nuevos cuando cambia manifiesto, sin hashes falsificados.
- **FR-013**: En el laboratorio, recuperar evidencia desde todas las páginas docentes autorizadas **ya ingeridas**, no solo una página o línea preseleccionada. Conservar unidades completas de párrafo, lista y tabla, posiciones y procedencia original; enlazar continuidad entre páginas solo cuando esté justificada. Permitir varios pasajes complementarios y supuestos explícitos dentro de presupuesto, sin equiparar citas repetidas con verificación semántica ni afirmar cobertura de la asignatura completa.

- **FR-014**: En el perfil conversacional, publicar afirmaciones académicas solo si una comprobación semántica independiente acredita apoyo en evidencia activa y autorizada, pertinencia y cobertura; rechazo o incertidumbre bloquean la afirmación y producen límite o aclaración. La evidencia web requiere además la política de actividad y el contraste de FR-021/024. La constitución 2.0.0 autoriza esa capacidad restringida; su implementación y validación siguen pendientes y no activan red en perfiles existentes.
- **FR-015**: La respuesta conversacional se genera a partir de pregunta, historial realmente mostrado y evidencia recuperada vigente mediante RAG. El modelo puede explicar y parafrasear, pero no aportar hechos académicos de memoria como si fueran recuperados. No sustituir el objetivo por respuestas de contenido predefinidas.
- **FR-016**: Ante evidencia insuficiente o conflictiva, ampliar de forma acotada la búsqueda local en documentos autorizados y comprobar procedencia. Si continúa insuficiente y la actividad permite web, buscar documentación externa pública mediante FR-021/024; si está deshabilitada, falla o no permite responder con respaldo, pedir aclaración concreta o indicar el límite. Un conflicto no se resuelve por mayoría de páginas web ni reemplaza el material docente. La ruta web no elude grounding ni obedece instrucciones halladas en fuentes.
- **FR-017**: Clasificar el alcance académico frente a temario o delimitación docente vigente antes de generar: distinguir dentro de alcance con evidencia, dentro de alcance con evidencia insuficiente, fuera de alcance confirmado e incierto. Solo un fuera de alcance confirmado permite decir cortésmente que el tema no forma parte de la asignatura y no necesita estudiarse para ella; no responderlo académicamente ni buscarlo en internet. La falta de pasajes, una cuarentena o un score bajo nunca prueban exclusión. En caso incierto pedir precisión sin afirmar que no necesita estudiarlo.
- **FR-018**: En preguntas mixtas, tratar únicamente la parte dentro de alcance con evidencia y señalar la parte excluida; no confundir prerrequisitos o analogías para explicar un tema con exigencias adicionales de estudio. Saludos, fuentes, controles, aclaraciones y gestión de sesión conservan su ruta operativa.
- **FR-019**: Presentar referencias legibles al documento o título, con página cuando sea útil; no exigir al modelo identificadores técnicos ni citas por frase como formato de conversación. El host puede construir la presentación desde la procedencia exacta. Si solo conoce los documentos entregados al generador, debe llamarlos «Fuentes consultadas», sin afirmar que verifican todo el texto. Conservar internamente unidades, versiones, hashes y trazas para revisar apoyo, pertinencia y cobertura; la atribución general no rebaja FR-014 ni valida ejemplos injustificados. La información externa llevará aviso visible de origen Internet y título/enlace; actualizar esta especificación no activa el acceso web.
- **FR-020**: Atender al acto pedagógico actual; ante incomprensión cambiar la estrategia explicativa sin añadir hechos académicos ajenos a fuentes. Permitir ejemplos o propuestas coherentes con valores, requisitos y escenarios inventados cuando se presentan inequívocamente como hipotéticos; no exigir respaldo literal para sus datos ficticios ni enumerar cada detalle de modo burocrático. Fundamentar el principio académico y su interpretación; hacer claros los supuestos decisivos, la condición observable y el resultado esperado. Distinguir requisito propuesto, criterio de aceptación y viabilidad demostrada. No concluir coste, tiempo, exhaustividad, impacto o garantías sin premisas suficientes; pedir o proponer el contexto que falte sin invalidar una primera formulación del alumno.

## Ampliación web autorizada (30-10-2026), pendiente de implementar

- **FR-021**: Solo ante insuficiencia local dentro de la actividad, y con política de red vigente habilitada, consultar documentación pública externa. Informar de que se está usando Internet y separar su aportación de lo encontrado en los materiales del profesor. No consultar temas confirmados fuera de alcance ni enviar entradas personales o documentos privados.
- **FR-022**: Contrastar autoría, procedencia primaria, contexto, fecha/edición pertinente y respaldo del contenido. Cuando sea necesario, corroborar con fuentes independientes; varias copias de un mismo origen no aportan independencia. Enlace válido, reputación del dominio y autocrítica del generador no bastan para declarar validez.
- **FR-023**: Comparar las afirmaciones externas candidatas con material docente vigente pertinente, ampliando la revisión local cuando proceda. Registrar pasajes y conclusiones, separar discrepancia real de distinta terminología/contexto y no afirmar compatibilidad con documentos no revisados. Si hay contradicción o incertidumbre no resuelta, no incorporar esa afirmación como explicación establecida: mostrar el límite o la discrepancia y solicitar aclaración/revisión docente cuando corresponda. No corregir silenciosamente al profesor.
- **FR-024**: Acceso y descarga acotados, cancelables y trazables, con presupuestos por actividad, defensa frente a instrucciones de páginas y destinos no públicos, y caché/versiones revocables. Inferencia y revisión locales; consultas externas minimizadas a conceptos académicos, sin historia/transcripciones, PDFs privados, identificadores ni audio. Con web deshabilitada, caída o permiso retirado, continuar localmente sin respuesta externa oculta. No activar la capacidad en examen por herencia de la sesión de estudio.

## Incremento I5 acotado — recuperación operativa (29-10-2026)

Ante una pregunta que supera la capacidad del buscador, un historial de búsqueda demasiado largo o recuperación sin pasajes, el laboratorio debe explicar una acción posible, conservar el historial ya mostrado y permitir reformular. Ninguno de esos tres casos llega al generador ni consume una llamada. No se recorta silenciosamente la pregunta o su referente; cambiar de tema es una decisión explícita. Recuperar cero pasajes no prueba que un tema esté excluido ni que una selección no vacía sea suficiente. No cambia FR-014/017, la publicación o la aceptación docente. Este bloque desarrolla parte de I5, no lo declara completo.

## Key Entities

Estado conversacional explícito, fuente/página vigente, candidata de explicación con afirmaciones y tipo, testigo, veredicto independiente, política/publicación y recibo de prueba. Reutilizar entidades/servicios existentes antes de ampliar.

## Success Criteria

- **SC-001**: Conversaciones reales nuevas (desarrollo y variante congelada) cubren saludo/pregunta, explicación, incomprensión repetida, ejemplo, error/rectificación y cambio de foco con oráculos independientes satisfactorios; no basta HTTP200 ni grounding aprobado.
- **SC-002**: Cero afirmaciones publicadas sin procedencia permitida, cero ejemplos atribuidos literalmente a fuente y cero publicación con gate fallido. Mantener evidencia separada de candidatas rechazadas.
- **SC-003**: Repetición/cierre/cancelación propios, sin cambios en originales/entornos históricos ni procesos ajenos; recursos preparados y parada propia.
- **SC-004**: Informe separa cumplimiento técnico, capacidad efectiva y aceptación/voz humana pendientes; gates fallidos son trabajo pendiente y no éxito didáctico.
- **SC-005**: Pruebas deterministas demuestran unidades sin cortes físicos, procedencia exacta, continuidad justificada, recuperación multi-fuente con vecinos, presupuesto y discrepancias conservadas; una revisión por conjuntos puede registrar varios pasajes/premisas sin otorgar aprobación semántica ni publicación. La utilidad conversacional sigue sometida a SC-001/G2 y revisión humana.

- **SC-006**: Ningún caso negativo congelado de contradicción compatible, premisa ausente, fuente retirada, respuesta parcial o inyección obtiene permiso falso; sin evaluador calibrado no se abre G2.
- **SC-007**: El laboratorio conserva trazas de recuperación inicial y ampliación local acotada, evidencia entregada al generador, respuesta completa y revisión separada de procedencia, apoyo, cobertura y continuidad. Insuficiencia persistente o conflicto no termina en afirmación académica inventada; los controles positivos también miden cobertura y rechazos falsos.
- **SC-008**: Casos positivos y negativos de frontera, recuperación vacía, fuente retirada/cuarentena, pregunta mixta, referente elíptico y controles operativos demuestran que solo una autoridad de alcance explícita habilita el aviso «no necesitas estudiarlo»; los demás casos no amplían temario ni inventan respuesta.

**SC-009 — ampliación web restringida:** pruebas de la actividad distinguen complemento
respaldado y compatible, contradicción con material docente incluso fuera del primer top-k,
terminología diferente sin conflicto e incertidumbre no resuelta. La aportación externa
visible incluye aviso y enlaces; conflicto/incertidumbre no se convierten en afirmación
establecida. Con política offline, permiso retirado o consulta no segura no hay tráfico
externo. Los dobles CPU comprueban flujo/permisos; no acreditan por sí solos juicio semántico.

## Edge Cases

Fuente insuficiente, material retirado/ajeno/cambiado, objeto ambiguo, inyección, fallo/timeout/modelo ausente, contexto obsoleto, ejemplo numérico no documentado, pregunta protegida de otro modo, error de alumno, repetición improductiva. Nunca usar el vocabulario agua/cantidades como semántica universal de validación de requisitos.

## Estado vigente y decisiones

- Decisión expresa del usuario (27-10-2026): referencia documental general suficiente para presentación; se elimina la obligación visible de reproducir IDs entre corchetes. ST01 conserva su primer resultado y rechazo bajo el contrato anterior; su desambiguación injustificada sigue siendo un problema de contenido, separado del formato. No se reescriben recibos ni se declara aprobado retrospectivamente.
- Aclaración expresa posterior (27-10-2026): la invención coherente en ejemplos no es un fallo por no estar literalmente en RAG. Un umbral de respuesta hipotético puede ilustrar rendimiento sin convertirse en estándar, recomendación universal o prueba de que se alcanza. La comparación pedagógica inicial ya estaba congelada, pero no ejecutada: se conserva y se adjunta una adenda previa a inferencia con esta aclaración, sin cambiar preguntas, prompts, presupuesto ni resultados anteriores.

- Fuente actual en ejecución: documentación docente activa y autorizada, sin red. Decisión del usuario del 30-10-2026 y constitución 2.0.0 autorizan futura ampliación web restringida conforme a FR-021/024. Se mantiene deshabilitada hasta implementar y probar sus controles; no se alteran resultados ni políticas de sesiones anteriores.
- Citas/IDs, hashes y similitud no demuestran apoyo semántico. Generador y verificador deben ser independientes; `unknown` bloquea. Ejemplos ficticios se etiquetan y su principio académico se respalda. La salida de contenido debe ser generada desde RAG documental, no de una respuesta docente predefinida.
- La política de alcance v1 de esta actividad referencia cuatro PDF docentes; alcance aprobado no significa respuestas aprobadas. Los ensayos Qwen/Mistral son diagnósticos incompatibles para ranking y no abren G2/SC001. Reserva intacta, perfil participante cerrado.
- Punto de entrada: [hoja de ruta](evidence/verified-conversation-roadmap.md). Detalle: [plan operativo](evidence/grounded-tutor-action-plan.md). Cronología de aclaraciones íntegra: [spec histórico](evidence/speckit-history-2026-10-25/spec.md).


## Parte 2 autorizada: consulta documental I0/I1, 27-10-2026

Incremento limitado por orden humana posterior al plan consolidado: corpus real local de requisitos y consulta documental de solo lectura en perfil aislado, sin vectores, pesos, inferencias ni participantes. Reutiliza FR-010/011/012/013/019 y SC-003/004/005 solo en su dimensión documental. Originales intactos, extracción por página/sección, derechos y edición trazados, deduplicación por contenido, cuarentena visible y mapa concepto→pasajes. La comprobación técnica no equivale a aceptación docente. No habilita FR-014/015, G2, SC-001, T090 o T150.

Resultado I0/I1 del paso2: consulta documental disponible para prueba docente según [informe](../../docs/audits/2026-10-27-part2-corpus/report.md); revisión técnica parcial del corpus, sin aceptación humana ni habilitación generativa. Se preservan los requisitos históricos y gates.

## Ampliación autorizada del bloque de requisitos, 27-10-2026

La orden humana posterior exige cubrir el bloque efectivo de requisitos desde los PDF docentes, no seleccionar solo páginas para definición/tipos. Esas preguntas son un guion inicial de demostración. Versión nueva preservando v1.1; matriz de todos los subtemas reales y huecos, QA integral de los dos documentos principales y complementos pertinentes, sin incorporar toda la asignatura. Diferenciar extracción fallida, no revisado, administrativo, duplicado y fuera del subconjunto. Fuentes oficiales NASA, Sommerville e INCOSE cuando su adquisición y condiciones lo permitan; acceso bloqueado no se simula como incorporación. La consulta selecciona explícitamente versión, sin cambiar sesiones o catálogo habituales. No indexar, generar, examinar ni abrir participante; T077, T090/T150, G2/SC001 conservan estado. Entrega técnica y aceptación docente separadas.

## Incremento autorizado de recuperación v2.1, 27-10-2026

Solo pregunta docente→pasajes recuperados con documento/página/procedencia/original, en perfil optativo. CPU local offline del encoder/tokenizer existente, representación e índice aislados; comparación congelada de léxico/denso/RRF. No generación, evaluación del alumno ni cambio de gates. [Informe y resultado negativo de promoción](../../docs/audits/2026-10-27-retrieval-increment/report.md). La suficiencia sigue no evaluada; una media mejor no compensa una pérdida por subtema superior al criterio prospectivo. No cerrar T077 global ni consumidores históricos por integrar este perfil.

## Primera conversación generativa autorizada, 27-10-2026

Alcance único E0/E1/E2 del [plan auditado](../../docs/plans/2026-10-27-first-generated-study-increment.md): diagnóstico docente local sobre recuperación real v2, candidata densa experimental, Qwen2.5-14B NF4 existente, hasta ocho preguntas/un calentamiento,768 tokens/60s y20min globales. Separar bruto, inspección diagnóstica unverified y participante cerrado; no falsear suficiencia o PostReview para abrir LaboratoryConversation. Sin notas, examen, voz o nuevas candidatas. [E0 y bloqueo vigente](../../docs/audits/2026-10-27-first-generated-study/report.md): GPU ocupada y contrato de50s rechaza60s; cero inferencias, E1/E2 pendientes. Sin aceptación humana ni cierre de feature/gates.

## Seguimiento CPU autorizado del primer diálogo, 27-10-2026

Orden humana «sigamos con cpu»: conexión ejecutable v2.1 densa experimental → GenerationPort → recibo e inspección docente unverified/not_assessed con historial de texto mostrado y participante cerrado. Autoridad de inspección distinta de publicación; no evaluadores supported simulados ni debilitamiento de LaboratoryConversation. API/UI y consentimiento/retención/acceso/cancelación vigentes conforme al contrato [diagnóstico v2](contracts/generated-study-diagnostic-v2.md). [Informe CPU](../../docs/audits/2026-10-27-generated-study-cpu/report.md). Protocolo sucesor50.000ms exactos; v1 rechazado preservado. Cero inferencias LLM en esta continuación; calidad, E1/E2 reales y aceptación humana pendientes.

## E1 real autorizado, 28-10-2026

Captura de8turnos reales sobre recuperación densa v2.1 con14B NF4 local, protocolo50s/768tokens/20min, una candidata y sin nuevas preguntas fuera del cupo. Los ocho terminan stop y se muestran en consola experimental, pero la revisión detecta inversión conceptual A3 y fusión validez/estructura B1, entre otras limitaciones. [Resultado y evidencia íntegra](../../docs/audits/2026-10-28-first-generated-study-real/report.md). No se transforma unverified en supported ni se declara E2 lista, aceptación académica o feature cerrada. E1 termina como diagnóstico completo con contenido defectuoso conservado, no éxito universal del tutor.

## Revisión y reparación solicitadas, 28-10-2026

Nueva petición humana: generar candidata, revisar contra fuentes, reparar una vez y comprobar la mejora. Implementación diagnóstica optativa sobre GenerationPort, con inicial/crítica/reparación/final separados, procedencia, presupuesto, guard por sesión y estado unverified. [Contrato](contracts/advisory-review-repair.md). Primer ensayo eligió otra llamada al mismo14B, no la revisión del asistente:0mejoras claras/8casos. El usuario corrigió esa sustitución; control separado con críticas reales del asistente y una corrección local:2objetivos corregidos y2mejoras parciales en4casos expuestos. No se confunden ambos diseños ni se infiere eficacia general, verificador autónomo validado o aceptación docente. [Control y resultados](../../docs/audits/2026-10-28-agent-assisted-repair/report.md).


## Estado operativo del incremento web — 30-10-2026

T114/T115 implementan política optativa de nueva actividad y adquisición pública acotada. Los perfiles existentes siguen offline. T116–T118 siguen parciales: no hay evaluador semántico independiente acreditado ni explicación externa automática. La interfaz admite únicamente inspección docente explícita con procedencia y límite; no reemplaza el objetivo autónomo de FR-014/016/021–024. Véase [evidencia operativa y pendientes](../../docs/audits/2026-10-30-web-fallback-runtime/report.md). No cambia ningún gate histórico ni aceptación.


## Ensayo semántico CPU autorizado — 30-10-2026

Sucesor de la auditoría independiente web: medir cuatro situaciones nuevas (complemento, conflicto, terminología compatible e incertidumbre) con un modelo local revisor que no genera la respuesta. Fuentes, criterios y presupuesto se congelan antes de inferir. El conflicto puede usar una variante experimental explícita, aislada y no atribuida al profesor. La medición no activa sesiones ni publicación. Después comprobar navegador real con fixture identificado; SSR no lo sustituye. Mantener T116–T118 y T151–T153 según evidencia real.


Resultado del bloque semántico CPU: 1.5B no entrega decisiones completas utilizables; 7B acierta los dos controles compatibles pero omite un conflicto controlado y crea un conflicto sin respaldo ante incertidumbre. No hay promoción ni explicación autónoma nueva. Navegador real sí acredita aviso, adquisición pública atribuida, preservación de conversación, plazo/reentrada y cierre, usando proveedor fixture explícito. [Informe](../../docs/audits/2026-10-30-web-semantic-cpu/report.md).


## Rondas automáticas web autorizadas — 30-10-2026

Probar generación, revisión separada de respaldo externo y compatibilidad docente, corrección localizada a partir de objeciones con pasajes y revisión posterior. Una atribución correcta «la fuente afirma X» puede coexistir con discrepancia docente sobre X; evaluar ambos ejes sin confundir ausencia, terminología o contexto con oposición. No rechazar estilo, extensión, repetición o ficción coherente. Nuevos casos, todas las versiones conservadas y medición externa de mejoras/errores/críticas/falsas aceptaciones; el acuerdo de modelos no valida por sí mismo. Máximo dos correcciones por caso y parada por repetición/no cambio/no disminución de incidencias como heurística de recursos. Sin modificar presupuestos históricos ni gates.


## Resultado de las rondas automáticas CPU — 30-10-2026

Petición expresa posterior de suavizar el revisor: juzgar si la respuesta es adecuada
y académicamente correcta para la pregunta, sin exigir perfección, todos los apartados
de una lista docente o respaldo literal de datos ficticios coherentes. Separar
propuestas/ejemplos de hechos/conclusiones: la ficción no exime de fundamentar el
principio académico ni permite atribuciones falsas o cumplimiento/viabilidad sin
premisas. Implementación optativa v3 y calibración expuesta correcta/defectuosa;
no habilita publicación ni cierra la acreditación del evaluador (T170).

Corrección posterior autorizada: el revisor usa un rol propio con referencias internas
permitidas y separa respaldo de compatibilidad. Una incidencia debe explicar la frase
problemática, su evidencia y el cambio necesario, sin obligar al corrector a aceptar
críticas equivocadas. Se preserva el perfil anterior. El diagnóstico sobre borradores
ya expuestos prueba instrucciones y capacidad local acotada; no acredita transferencia
ni abre participantes o gates (T164/T165).

Se implementó el orquestador experimental y se ejecutaron cuatro preguntas con crítica/corrección automática. No hubo mejoras aplicadas: las dos correcciones completas fueron idénticas y un parche14B quedó incompleto; no hubo post-revisión real de una corrección completa distinta. Críticos7B/14B omitieron un error de viabilidad y confundieron atribución sustentada con oposición docente. Se conserva la propuesta como hipótesis, no se valida ni se descarta universalmente. [Informe completo](../../docs/audits/2026-10-30-web-rounds-successor-cpu/report.md). Permanecen cerrados participante/gates y pendientes los evaluadores y la integración autónoma.


## Referencias por localización — decisión del usuario, 31-10-2026

FR-019 se aplica también al formato de revisión: no exigir al modelo copiar pasajes
ni reproducir literalmente la frase criticada. El revisor explica el problema y
señala fuentes recibidas; el host presenta documento/página o URL desde metadatos
autorizados, sin inventarlos. Una referencia válida acredita identidad/localización,
no apoyo semántico: FR-014/022/023 se mantienen. Los contratos históricos se conservan
para reproducibilidad; el nuevo contrato se mide por separado antes de promoverlo.

La adecuación de FR-020 usa el mismo criterio para fuentes docentes y de Internet. El origen externo no justifica exigir existencia literal de cifras/nombres ficticios coherentes, listas completas ni precisiones no necesarias para contestar. Se mantienen el contraste de conceptos, las atribuciones fieles y la justificación de conclusiones académicas.


Variante de laboratorio v7: el modelo emite una decisión primaria y objeciones materiales con referencias; la acción mecánica puede derivarse en el host. No se infiere respaldo externo ni compatibilidad docente de un no_issues_found: ambos quedan desconocidos si no se han acreditado. Se mantiene revisión tras reparación y salida participante cerrada. El objetivo sigue siendo una respuesta generada y académicamente adecuada, no un JSON consistente ni acuerdo del modelo.


## Diagnóstico CPU por segmentos — 01-11-2026

Orden del usuario: otro ensayo pequeño CPU con enfoque distinto. Reutilizar G03/G04 realmente generadas como desarrollo expuesto; enfocar mecánicamente primer párrafo y última frase manteniendo toda la respuesta como contexto. La selección parcial nunca permite aprobar el conjunto. Crítica automática falible; sustitución local solo tras objeción emitida y revisión del texto cambiado. Preservar contenido fuera del segmento y evaluar aciertos/errores fuera del modelo. Ningún gate ni perfil de aplicación cambia.

## Corrección de presentación autorizada, 01-11-2026

T186: extraer únicamente la envoltura JSON reconocida mensaje_mostrado para el texto visible, conservar la generación original y enviar a revisión/historial el texto realmente mostrado. No reparar JSON ambiguo ni reemplazar palabras académicas automáticamente. Registrar perfil didáctico v2 manteniendo v1, con instrucción genérica de texto visible y traducción conservadora. La aceptación humana de B2/B3/B4 mantiene solo JSON y Complejidad como correcciones; el resto de observaciones no bloquea esos casos. Verificar fuente original, negativos CPU y dos turnos nuevos con RAG/modelos reales, sin transformar esta aceptación en aprobación general o publicación.

## Chat simple con revisión, 02-11-2026

Incremento autorizado T188–T190: vista /estudio con pregunta, conversación, enviar/cancelar, fuentes y finalizar. El tema se decide en recuperación a partir de la pregunta actual y referencias de seguimiento; el historial mostrado se conserva. Sin referente suficiente se pide aclaración. Reutilizar WebReviewRounds v7 y perfiles v2/14B/Qwen3-thinking, sin otro evaluador. Dos workers en runtime optativo, hasta dos correcciones, tiempo por etapa 180 s y por turno 600 s, reloj global y presupuestos compartidos sin renovación por reentrada; salida solo de la versión final seleccionada. Perfil nuevo de laboratorio local con acceso existente: no abrir publicación ni permisos generales de participantes. Separar vista simple y recibos técnicos también por API. Implementación y ensayos actuales solo CPU; no cargar GPU bajo la restricción vigente.

## Recuperación transitoria CPU — T192

Recuperar exclusivamente estado del servidor tras pérdida de red del chat simple: nunca reenviar automáticamente ni inferir entrega por timeout. Separar mensajes confirmados, candidata preparada y generación en curso. Mantener privacidad del recibo y expiración global; conservación visible offline acotada por la última conexión válida y lease de 15 s (purga local en hasta 16 s). Sin almacenamiento persistente nuevo ni nuevas cargas de modelo/GPU.


## Refinamiento CPU del chat — T194–T197 (02-11)

La vista sencilla conserva un borrador nuevo al confirmar una respuesta recuperada; facilita foco de teclado y presentación móvil sin cambio manual de tema. Mantiene el heartbeat mientras la pestaña del alumno está en segundo plano para consultar fuentes, sin renovar el plazo global ni ampliar el lease de quince segundos si no llegan peticiones. No añade persistencia. Cobertura documental y pruebas simuladas no acreditan calidad académica ni completan T191.

## Autoestudio libre y preparación reutilizable — T201–T204

El autoestudio no tiene cupo educativo de preguntas ni un corte acumulativo de llamadas al revisor. Los cupos son controles explícitos de ensayos; no se confunden con las ayudas de examen configuradas por el profesor. Permanecen los plazos técnicos y las rondas acotadas por respuesta. La interfaz distingue autores y agrupa referencias por documento/página. La preparación puede reutilizarse solo tras validar entradas y artefactos vigentes, con índice de trabajo separado por arranque. La guía del piloto recoge uso descriptivo, sin calificación, rúbrica, audio ni persistencia automática nueva. No se abren gates ni se acredita eficacia con estas pruebas CPU.

## Alcance de cierre confirmado: ampliación por Internet incluida

La ampliación por Internet es parte obligatoria del autoestudio solicitado, no una opción que se descarte al cerrar el perfil local. Reutilizar las adquisiciones, fuentes externas, generación, revisión/corrección y criterios de tolerancia ya ensayados; no presentarlos como inexistentes ni reiniciar sus campañas por defecto. Para el cierre debe funcionar el recorrido integrado: insuficiencia local dentro del temario → acceso web permitido y aviso → contraste de respaldo y compatibilidad docente → respuesta con atribución externa y URL → seguimiento. Los ejemplos ficticios coherentes y mejoras opcionales reciben el mismo criterio que con material docente. T205 conecta ese recorrido con pruebas CPU simuladas; T117/T152/T157 y T191 conservan la validación semántica/real pendiente. Superar únicamente el chat local o simulado no completa este alcance.

T205: política explícita por actividad de autoestudio, sin permisos de examen. Aviso mostrado antes de buscar/descargar; fuentes externas contrastadas con originales docentes activos, incluidos los ajenos al top-k. Referencias públicas archivadas no se reclasifican como originales docentes. Política revalidada durante el recorrido y antes de entregar una candidata pendiente. Bibliografía opcional del revisor no constituye prueba semántica ni bloqueo formal; la procedencia exacta la conserva el host. La interfaz muestra «Información de Internet» y URL. Sin política habilitada se conserva el recorrido local; las simulaciones no abren gates.
