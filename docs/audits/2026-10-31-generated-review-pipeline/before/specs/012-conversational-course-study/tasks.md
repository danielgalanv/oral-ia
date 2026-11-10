# Tareas 012 — índice activo compacto

## Ampliación web de autoestudio autorizada, 30-10-2026 — todavía sin implementar

Constitución 2.0.0 y [contrato](contracts/web-evidence-fallback.md). Esta lista no activa red ni habilita participantes; comienza con contratos y negativos CPU.

- [x] T114 Implementar política versionada de web por actividad, permisos, consultas mínimas seguras, presupuesto y recibos con procedencia externa, sin cambiar perfiles offline existentes (FR-021/024).
- [x] T115 Implementar adquisición pública acotada detrás de un puerto, con cancelación/retirada, URL/destinos/redirects y límites de contenido, datos tratados como no confiables y caché revocable; no enviar preguntas personales ni documentos privados (FR-024).
- [ ] T116 Diseñar y medir por separado la revisión de respaldo/validez externa y el contraste con material docente vigente pertinente: compatible/conflicto/incierto con testigos, controles positivos/negativos y sin inferir verdad de dominio/HTTP o autocrítica. No darlo por resuelto mediante fixtures (FR-022/023).
- [ ] T117 Integrar insuficiencia local → web permitida → revisión → explicación atribuida, con aviso visible y enlaces separados de material docente; conflicto/incertidumbre conservan límite y contexto. No abrir publicación sin controles vigentes (FR-014/016/019/021/024).
- [ ] T118 Verificar en CPU offline/permiso retirado, inyección, datos sensibles, destinos no públicos, fuentes duplicadas, conflicto docente fuera del primer top-k, terminología distinta sin contradicción, cancelación/timeout y continuación. Después, ensayo real acotado identificado; no presentar material simulado como web contrastada ni abrir examen (FR-021/024).

## Incremento I5 acotado, 29-10-2026 — alcance de esta ejecución

- [x] T110 Reproducir pregunta/contexto de búsqueda demasiado largos y ausencia de pasajes; comprobar historial, no generación y cupo sin consumo.
- [x] T111 Tipar los límites operativos del recuperador y ausencia de pasajes, conservar sesión y ofrecer reformulación/cambio de tema explícito sin recortes silenciosos ni juicios de alcance.
- [x] T112 Verificar mensajes y continuación en UI/API, regresiones pertinentes, estilo y build aislado; sin GPU.
- [x] T113 Probar el recorrido en navegador con recuperación real CPU y proveedor fixture identificado, conservar evidencia, parar recursos propios y entregar límites pendientes de I5. No acredita contenido generativo ni publicación.

Validado el 30-10-2026: 79 pruebas Python, 12 UI, cinco envíos reales por navegador (tres salidas fixture y dos rechazos antes de generar), cuota 1/1/2/2/3, continuación y cierre correctos. [Informe y límites](../../docs/audits/2026-10-29-study-recovery-cpu/report.md). Recuperación vacía probada con dobles, no declarada detector de insuficiencia semántica. Solo este bloque se completa; I5 global y pendientes históricos siguen abiertos.

El alcance nuevo no ejecuta ni marca pendientes históricos por inferencia. Evidencia previa: [recorrido generativo real del 29-10](../../docs/audits/2026-10-29-study-browser-acceptance/report.md). El usuario autorizó continuar; la comprobación técnica anterior no sustituye aceptación docente ni cierre global.

Usar la [hoja de ruta](evidence/verified-conversation-roadmap.md) para el orden y las puertas. El [snapshot íntegro previo a esta compactación](evidence/tasks-before-compact-2026-10-25.md) conserva referencias, estados parciales y evidencia de cada tarea; la [cronología anterior](evidence/speckit-history-2026-10-25/tasks.md) conserva las tareas históricas. Los IDs y estados siguientes son los mismos del snapshot. G2/SC001 y publicación permanecen cerrados.

## Pendientes y completadas relevantes

Bloque de calidad de estudio, 27-10-2026: perfil `pedagogy-v1` optativo y baseline preservado, con aclaración prospectiva sobre invención hipotética coherente. [Comparación pedagógica parcial](evidence/pedagogical-comparison-recovery-run-v1/report.md): un caso baseline de cuatro turnos completo y dos turnos completos de la mejora; su ejemplo se truncó y no entró en historial, por lo que se detuvieron los 17 turnos no despachados. No se obtuvo la comparación completa de tres casos ni se demuestra mejora general. Se conservan errores de fidelidad y repetición; no se promueve el perfil, no se ajusta ranking y las tareas sustantivas siguen abiertas. No sustituir este resultado por el total de pruebas CPU.

Decisión de presentación del usuario (27-10-2026), implementada en FR-019 y en el recorrido RAG: referencias documentales legibles del host bajo «Fuentes consultadas», sin exigir IDs entre corchetes por frase. Se conservan procedencia exacta y juicio de contenido independiente; `unknown/rejected` siguen bloqueando el preview revisado. ST01 se conserva rechazado bajo el contrato anterior y su error de desambiguación no se reinterpreta como aprobado. Controles nuevos L01–L03 y presupuesto separado en `evidence/readable-reference-proposal-v1`; no sustituyen reserva ni G2. Resultado y recursos en `evidence/readable-reference-run-2026-10-27` y su informe asociado; no cerrar las tareas semánticas por este cambio de presentación.

Avance CPU integrado (26-10-2026): [ejecutor, recuperación y transcripción](evidence/cpu-rag-progress-v1/report.md). `LaboratoryConversation` reutiliza el RAG existente, revalida tras esperas y revisión, conserva solo texto confirmado como mostrado y prueba cancelación/errores. Se ejecutaron seis turnos con política SQL y PDF reales de solo lectura, catálogo vigente de 139 páginas e interfaces generativas/evaluadoras simuladas. Se corrigieron dos fallos reproducidos de cambio de tema y se midieron seis controles nuevos de recuperación con vocabulario bilingüe optativo y ampliación acotada. T063/T071/T072/T073/T074 siguen abiertos: este avance no acredita clasificación semántica, apoyo de afirmaciones, utilidad pedagógica ni autorización de fuentes en runtime participante. Reserva, publicación y prueba GPU mínima permanecen intactas; no se inicia GPU automáticamente al terminar las tres horas.

- [ ] T008 Ejecutar tres conversaciones/caso con preguntas naturales/seguimiento según salida efectiva, conservar primeros fallos y modelo/tiempos en evidence/first-generation/ y oráculos independientes en tests/course_dialogue/.
- [ ] T009 Diseñar e implementar contrato sucesor de derivaciones reconstruibles, comprobación semántica independiente y enlace optativo a autorización/estado, sin convertir texto libre en datos confiables ni bajar T090/T150; registrar pruebas en contracts/ y tests/course_dialogue/.
- [ ] T010 Completar SC001/SC002 con transferencia/conversación útil y gateG2 suficiente; conservar fallos como pendientes cuando no pase, en evidence/generative-gate.md.
- [ ] T011 Implementar referente/objetivo/pregunta pendiente/transición y estrategias de explicación verificables, salutación compuesta/ambigüedad/errores/rectificación; probar oráculos que niegan pertinencia aun con grounding válido en tests/course_dialogue/.
- [ ] T012 Integrar orientación/fuentes/controles comprensibles por vía textual autorizada; no atribuir STT/TTS/interrupciones/silencios validados en docs y pruebas.
- [ ] T013 Implementar raíz marcada/lock/proceso local propio/puerto explícito/parada/cancelación y comando scripts/course-dialogue.ps1, sin cambiar .oralia-course-study ni demo.
- [ ] T014 Probar recursos/propiedad/secretos/preservación en tests/course_dialogue/ y evidence/validation/.
- [ ] T015 Ejecutar regresiones pertinentes/global si compartido, Black/Ruff estructural y nuevo204/replay cuando cambie manifiesto; guardar evidence/validation/ sin modificar originales.
- [ ] T016 Entregar transcriptos íntegros y manejables, tabla completa de tareas/archivos/comandos/limitaciones en evidence/report.md y quickstart.md.
- [ ] T017 Ejecutar analyze/converge final; añadir trabajo obligatorio restante sin declarar convergencia si SC001 o gate fallan, en evidence/analysis-convergence.md.
- [ ] T018 CRITICAL Corregir y demostrar selección semántica de objetivo/acto: los tres cambios de foco emiten ask en vez de explicación y la rectificación interactiva no responde; preservar controlled-draft-context-exposed e interactive-context antes de nuevas pruebas,
- [ ] T019 Vincular la corrección a afirmación real y pregunta pendiente; distinguir respuesta pertinente/parcial, rectificación, aclaración y aplazamiento sin calificar ni atribuir comprensión; no usar corrección fija del objetivo como prueba de pertinencia,
- [ ] T020 Precisar apoyo de cada afirmación y supuestos de cada ejemplo; resolver matices de completitud/validación, consistencia, inspección y ambigüedad de controlled-review-context.md conservando revisiones previas del paquete,
- [ ] T021 Preparar enlace por APIs normales a unidades docentes revisables y configuración propia; impedir publicación sin revisión explícita y sin autorización T090/estado atómico vigente, sin presentar el preview como integración; comprobar mínimo G1 antes de solicitud docente concreta,
- [ ] T022 Ejecutar transferencia congelada con seguimiento condicionado a salida efectiva, respuestas a preguntas realmente emitidas y oráculos independientes de contenido/contexto/estado; conservar fallos y negar G2 cuando no supere criterios,
- [ ] T023 Completar pruebas de propiedad/cancelación/secretos y validación final después de cambios; investigar cinco fallos de Playwright-first y ejecutar suite aislada con trazas preservadas; completar tabla íntegra y analyze/converge sin declarar cierre por éxito del banco,
- [ ] T026 Implementar en laboratorio, solo si se identifica un evaluador semántico realmente independiente y medible, testigos de proposición/afirmación/cobertura con procedencia exacta, veredicto `supported/rejected/unknown` y recuperación conversacional sin aprobar por estructura o acuerdo no calibrado. No integrar en participante ni publicar borradores.
- [ ] T027 Medir el candidato T026 contra controles congelados sin falsos permisos, reserva no usada para ajuste, conversaciones completas desde estado real tres veces por caso, revisión de pertinencia/contenido/estado, tiempos y propiedad; conservar primer fallo y negar G2/SC001 si falla.
- [ ] T037 HIGH Validate the final relaxed V2 example/assumption display and explicit topic-switch retrieval in a newly frozen full development conversation, with independent claim support/relevance/coverage review and a stop condition that prevents another unbounded prompt cycle; preserve the two first trials and do not count posthoc parsing as displayed turns. Only after the development behavior and independent verifier are sufficient, exercise the untouched reserve three times per case under comparable resources and normal authorization gates.
- [ ] T040 After T038/T039 pass, freeze **new** positive/negative retrieval and sufficiency controls separately from exposed trials and the reserved conversation. Measure coverage, relevance and known source gaps; only if a distinct justified semantic candidate and resources are available, run one bounded local GPU trial with ownership/telemetry/stop condition. Keep T037/G2/SC001 open on any missing independent entailment, transfer, repetitions or teacher review.
- [ ] T048 Redesign the B/C optional example/assumption/limitation fields for a coherent bounded conversational output that can be completed without truncation or hiding invalid values. Freeze new controls before a new candidate and test contract-invalid/length paths, source caveats, real followup relevance and explicit focus switch against original pages. Preserve both full-teacher first packets and do not treat a valid JSON label as semantic support.
- [ ] T063 Auditar y versionar política de fuentes docentes activas, cambios/retirada y procedencia sobre `document_evidence.py`, `contracts/document-evidence.md` y binding de autorización ya existente; separar autorización actual de laboratorio de aceptación docente de respuestas, sin pedir reaprobar los PDF ni duplicar catálogo. Web requiere decisión explícita y enmienda constitucional separadas.
- [ ] T064 Mapear obligaciones de la pregunta a `contracts/semantic-planning.md` y afirmaciones/premisas/testigos a `claim_review.py`, `evidence_sets.py` y `contracts/document-evidence.md`; extender solo vacíos demostrados, sin certificar semántica por estructura. Congelar controles positivos y negativos **nuevos** de compatibilidad, premisa, cobertura y retirada; separar los ya expuestos como regresión.
- [ ] T065 Antes de código, registrar hipótesis de señal semántica y procedencia/identidad de un evaluador distinto del generador, diferencia con las tres vías fallidas, recursos, presupuesto, viabilidad y abandono. Solo con hipótesis justificada construir y medir en laboratorio respaldo, pertinencia y cobertura `supported/rejected/unknown`, con permisos falsos, rechazos falsos y cobertura por separado. Cero permisos falsos en controles finitos no garantiza fiabilidad externa; rechazar todo no aprueba. Sin candidato viable, documentar el bloqueo técnico y mantener RAG generativo sin publicación; no sustituirlo por contenido académico predefinido.
- [ ] T066 Probar respuesta de límite/aclaración y continuidad ante `rejected/unknown`, sin publicar texto libre; conservar T090/T150, acceso y consentimiento.
- [ ] T067 Solo tras T063–T066 y revisión docente: ejecutar conversaciones nuevas y reserva congelada tres veces/caso, revisión independiente con identidad/procedencia de contenido, pertinencia, cobertura y utilidad; gates G2/SC001 separados. Conservar primeras divergencias; no inferir voz.
- [ ] T068 Validar regresiones, Black/Ruff multiplicidad, hashes/manifiestos si se afecta código, analyze/converge y tabla completa. Mantener perfil cerrado mientras haya brechas.
- [x] T069 En laboratorio, añadir ampliación local acotada que reutilice `retrieve_units` y su validación de catálogo: resolver referente desde historial realmente mostrado, conservarlo en el segundo intento salvo cambio explícito de foco, ampliar presupuesto/vecinos y unir evidencia inicial y ampliada con trazas y deduplicación, sin red ni inferencia de suficiencia desde score. Probar seguimiento elíptico, cambio de foco, evidencia escasa, conflicto, fuente retirada y presupuesto.
- [x] T070 Definir en contrato experimental qué evidencia se entrega al LLM y cómo se informa insuficiencia/conflicto, sin inventar soporte ni incorporar texto académico predefinido. No conectar a participante ni abrir G2.
- [ ] T071 Vincular el resultado `delivered` del recuperador con `GenerationPort` solo en laboratorio, con pregunta/historial mostrado, pasajes y procedencia exacta en el contexto del LLM; guardar recibo de entrada/salida y revisar hechos académicos sin evidencia. Probar que fuente ausente, retirada o cambiada no llega al generador y que no hay respuesta de contenido predefinida.
- [ ] T072 Construir evaluación independiente de suficiencia/conflictos antes de generación y de apoyo/pertinencia/cobertura después, con positivos y negativos nuevos congelados y análisis de falsos permisos/rechazos. La recuperación léxica T069 no aporta esta evaluación.
- [ ] T073 Ejecutar conversaciones de laboratorio desde estado real con evidencia suficiente, insuficiente y conflictiva, continuidad tras aclaración, y salida completa mostrada; preservar primeros fallos. No abrir participante, reserva ni G2 sin cumplir T067 y gates históricos.
- [ ] T074 Incorporar a la frontera T063/T064/T071 una decisión de alcance previa con fuente docente/versionada: in-scope, out-of-scope confirmado, incierto, mixto y operativo. Insuficiencia/cuarentena no equivalen a out-of-scope; en mixtas enviar solo parte permitida al RAG. Probar fronteras cercanas, vacío, retirada, elipsis y operativas sin GPU.

Estado T063/T071 (2026-10-25): [validación del vínculo de catálogo](evidence/scope-catalog-binding-validation.md). Páginas y unidades de laboratorio quedan ligadas a la política v1 antes y después de `GenerationPort`; faltan autorización de fuente en runtime participante, clasificación semántica de alcance y poscontrol independiente. No marcar completadas.

Avance T063/T071: [revalidación en el momento de envío](evidence/dispatch-revalidation-2026-10-25.md), con cinco regresiones negativas reproducidas y corregidas antes de llamar al proveedor; 39 pruebas focales correctas. Estados pendientes conservados.

Propuesta T074 previa a inferencia: [clasificador local de alcance, veinte controles nuevos y abandono](evidence/scope-classifier-proposal-2026-10-25.md). Avanza independientemente de T065/T072; aún sin implementar ni medir. El documento distingue aceptación empírica acotada de garantía universal y corrige la interpretación del bloqueo del informe previo. No sustituir autonomía por revisión humana por respuesta.

Avance posterior T074: [contrato implementado y paquete congelado](evidence/scope-classifier-implementation-2026-10-25.md). 273 regresiones del módulo y 45 focales finales correctas; ensayo aplazado por contexto GPU ajeno antes de cargar modelo (0 llamadas, 20 no ejecutadas, matriz vacía). Falta medición semántica; no marcar completa ni confundir aplazamiento con fallo del modelo.

Ensayo posterior T074 (26-10): [revisión de recursos y primer fallo conservado](evidence/scope-classifier-resource-trial-2026-10-26.md). Preflight de carga observada permitió ejecutar 2/20 llamadas sin cambiar prompt/banco/oráculo: S01 abstención incorrecta, S02 exclusión con bandera incompatible rechazada por contrato; parada, 18 no ejecutadas. Sin transferencia ni ajustes; candidato no supera el protocolo. Periodos de rendimiento `resource-inconclusive`, salidas completas sin deadline. Árbol propio cerrado, contextos ajenos intactos; tarea abierta.

Diagnóstico posterior T074: [propuesta única de representación primaria sin booleano redundante](evidence/scope-successor-proposal-2026-10-26.md), con auditoría offline reproducible. No repara S02, no resuelve S01 ni autoriza otro ensayo; cero llamadas adicionales y tarea abierta.

Implementación posterior T074: [v2 optativo y catálogo descriptivo separado de 21 bloques](evidence/scope-v2-offline-delivery-2026-10-26.md), 58 pruebas offline/regresiones correctas. Una propuesta nueva de 28 casos queda congelada con presupuesto propio, sin inferencias ni reutilización de las 18 llamadas antiguas. Pendientes runner v2, medición real e integración de laboratorio; no marcar T074 completa.

Evaluación posterior T074: [ejecutor v2 y primer fallo del único ensayo de 28 casos](evidence/scope-v2-described-first-report-2026-10-26.md). 23 pruebas offline del ejecutor correctas; 1/28 llamadas nueva consumida, N01 rechazado por campo mixto/testigo no literal, N02–N28 no ejecutados. Presupuesto antiguo 2/20 intacto. Presión de memoria no atribuida y rendimiento inconcluyente registrados, salida completa sin deadline, árbol propio cerrado. Candidata detenida, sin variantes/reparación/integración ni publicación; T074 abierta.

Auditoría offline posterior T074: [capacidad real del decoder y propuesta de unión finita/testigos literales](evidence/scope-decoder-architecture-audit-2026-10-26.md). V1/v2 usaban schema-hint sin restricción de tokens; el backend solo restringe alternativas finitas. Prototipo de 120 variantes y localizador literal verificados offline, 15 pruebas existentes correctas, cero inferencias nuevas. Es propuesta de infraestructura, no candidato validado; memoria total no demuestra actividad ajena. T074 abierta.

Implementación finita posterior T074: [clasificador optativo con enforcement, testigos y presupuesto compartido](evidence/scope-finite-offline-delivery-2026-10-26.md). 43 pruebas offline correctas; tokenizer local real verificó 120 targets/2750 prefijos y 5 referentes/35 prefijos, EOS y no fugas, sin pesos/CUDA/inferencias. Propuesta única nueva congelada: 18 preguntas, máximo 4 llamadas/30 s/512 tokens por pregunta y 72 llamadas nuevas totales; no ejecutada. Testigos y semántica aún no certificados, publicación cerrada; T074 abierta.

Ensayo finito posterior T074: [runner con 22 pruebas offline y primera exclusión falsa](evidence/scope-finite-capacity-first-report-2026-10-26.md). F01 generó objeto legal `excluded_standalone/fiabilidad` para introducción a IS, con enforcement real 1/1; semántica incorrecta y parada. 1/72 llamadas nuevas consumida, 17 preguntas no ejecutadas, cero reintentos/variantes. Presupuestos antiguos intactos, alarma de memoria sin causalidad atribuida, árbol propio cerrado. Candidata detenida, sin integración RAG ni publicación; T074 abierta.

Auditoría final offline T074: [request efectivo, tokenizer/callback congelado y decisión técnica](evidence/scope-effective-request-audit-2026-10-26.md). Pregunta/política/descripciones correctas; 4189 tokens y 13+EOS reproducidos, restricción aplicada al sufijo generado. Conflicto reproducible: regla académica de evidencia vacía en solicitud de control. Renderer separado probado offline (21 pruebas), no conectado ni usado para reparar el ensayo; causalidad semántica no demostrada. Cero nuevas inferencias, configuración ensayada detenida, bloqueos de alcance y verificador separados.

Corrección conectada posterior T074: [perfiles de control en adaptador/worker y regresión académica](evidence/scope-control-connected-2026-10-26.md). Tipo de request y perfiles explícitos, confirmación efectiva en recibos, frames enviados por transporte simulado y tokenizer real CPU; 86 pruebas correctas. Vía académica conserva mensajes/fuentes/grounding. Archivos originales archivados y cuatro PDF verificados; presupuestos 2/1/1 intactos. Sin pesos ni inferencias GPU, causalidad/semántica de F01 no acreditadas, medición nueva no ejecutada; publicación cerrada y T074 abierta.

Diagnóstico posterior T074: [única medición del transporte corregido y decisión de viabilidad](evidence/scope-control-diagnostic-report-2026-10-26.md). C01 intro a IS volvió a seleccionar fiabilidad excluida con perfil/decoder correctos; 1/48 llamadas nuevas, 11 preguntas no ejecutadas, candidata detenida sin integración ni variantes. Dos preflights sin llamadas conservados y revisión solo de recursos congelada antes de inferir. Telemetría completa muestra 512 MiB libres; resumen temprano se conserva y se audita/corrige offline sin reparar resultados. 27 pruebas finales correctas, árbol propio cerrado, presupuestos anteriores intactos; alcance y verificador siguen como bloqueos distintos.

Coordinación GPU vigente (instrucción expresa posterior del usuario): el usuario confirma uso concurrente durante el último diagnóstico, por lo que rendimiento/recursos no son comparables; conservar texto sin atribución causal ni conclusión general del modelo. Antes de cualquier carga de pesos/inferencia/prueba GPU, avisar con prueba/modelo/duración/presupuesto y esperar confirmación explícita de disponibilidad. La autorización general anterior no basta; telemetría posterior obligatoria y procesos ajenos intactos. Solo CPU sin inicializar CUDA puede continuar sin esa coordinación. No hay otro ensayo autorizado por defecto; gates/reserva/publicación cerrados.


## Correcciones seguras tras auditoría, 27-10-2026

Plan autorizado: [fases 0–2](../../docs/plans/2026-10-27-oralia-audit-action-plan.md). La revisión de proporcionalidad sigue abierta; estos IDs no convierten el backlog completo en requisitos nuevos. Estados históricos conservados.

- [x] T075 Preservar manifiestos, 3279 históricos, cuatro recursos personales y 49 hashes protegidos; registrar diferencias y reversión en evidence/audit-remediation-v1 (fase 0, B04, FR-010/011/012).
- [x] T076 Reproducir en CPU y corregir identidad de caché A→B→A/concurrencia y carga local explícita sin cambios globales de entorno (E1/E2, B01, F01/F02, constitución I/IX).
- [ ] T077 Rechazar incompatibilidad de espacio vectorial y distinguir índices históricos sin identidad; probar en almacenes sintéticos sin migración habitual (E3, B02, F03).
- [x] T078 Reproducir y corregir recortes silenciosos de presupuesto en adaptadores; recibo solicitado/efectivo/capacidad y negativos 256/512/768/1024/2048 sin pesos (E4, B03, F04, constitución IX).
- [x] T079 Trazar productores de registros y probar conservación/exportación con sentinels; corregir defectos reproducidos de valores técnicos (S1, B05, F11).
- [x] T080 Probar caída, reintento, cierre concurrente e idempotencia en bases propias; documentar fronteras de entrega y borrado lógico sin nuevas políticas (S2/S3/S4, B06/B07/B09, F12–F16).
- [x] T081 Consolidar regresiones CPU y Black/Ruff por identidad/multiplicidad, preservación posterior e informe de límites, sin publicación ni cambios de gates (FR-012).

Estado del bloque seguro: [informe y límites](evidence/audit-remediation-v1/report.md). T077 permanece parcial: contrato optativo estricto de fingerprint y cuatro pruebas de Chroma sintético correctas; falta enlazar identidad efectiva del encoder a los consumidores históricos antes de una comparación densa nueva. No se acredita ningún índice habitual por defecto. La revisión de proporcionalidad mantiene diferidas ampliaciones de arquitectura, las fases 3–7 y cualquier promoción. Las tareas semánticas históricas siguen abiertas.

Actualización humana de finalidad: el objetivo inmediato es un piloto de investigación acotado con pocos estudiantes, no explotación. Se pueden elegir temas dentro de los nueve bloques; no exige validar toda la asignatura, modos o voz. No abre participantes ni modifica gates.

- [x] T082 Preparar inventario de cobertura de los nueve bloques y protocolo concreto de piloto con objetivos/fuentes, perfil candidato, errores críticos, consentimiento/conservación, aislamiento, cierre/parada y medición de eficacia/limitaciones, separada del valor de arquitectura; propuestas materiales sin activación en evidence/audit-remediation-v1/pilot-preparation.md y course-coverage.md. La preparación no acredita suficiencia docente ni autoriza realización.


## Parte 1 autorizada: conciliación y fundamentos, 27-10-2026

Alcance exclusivo de esta entrega: [informe, mapa, diseño pendiente y comandos](../../docs/audits/2026-10-27-part1-foundations/report.md). No autoriza partes posteriores ni cambia los estados históricos. Autoestudio por chat primero; examen después. Sin publicación, aceptación humana ni cierre de Feature 012.

- [x] T083 Conciliar el árbol detenido con la entrega T075–T082: hashes vivos iniciales, manifiesto previo, recursos protegidos y mapa de rutas/consumidores. Separar corregido y verificado, evidencia parcial, pendiente reproducido y riesgo no reproducido; evidencia en docs/audits/2026-10-27-part1-foundations/reconciliation.json y prior-live-comparison.json.
- [x] T084 Reproducir y corregir exclusivamente P1-R01: reconstrucción desde objeto Chroma antiguo reutilizaba la versión activa; leer puntero confirmado bajo el lock de escritor existente antes de elegir candidata. Dos negativos fallan antes y pasan después; 15 pruebas de reconstrucción/identidad/lectores, sin datos habituales. Copia previa y logs en el informe T083.
- [x] T085 Reverificar en CPU caché/offline, presupuestos, snapshots, privacidad, cierre/caída y reenvíos con dobles y bases propias. Conservar errores de entorno y bloqueos del guard; distinguir vectores simulados de recuperación semántica. Black y Ruff por identidad/multiplicidad, sin suites globales.
- [x] T086 Medir solo tokenizer local disponible y segmentación sintética, sin pesos; documentar diseño pendiente de unidades limitadas por tokens, fingerprint efectivo, recuperación tras reinicio y autoridad de publicación. No activar cambios materiales de representación, datos o conservación. T077 permanece parcial y las tareas generativas siguen abiertas.


## Parte 2 autorizada: corpus y consulta documental I0/I1

No cierra Feature 012, T077 ni gates. Solo este bloque; sin continuación automática.

- [x] T087 Adquirir/copiar fuentes docentes y oficiales pertinentes, comprobar edición/derechos/hash y equivalencias por contenido; registrar limitaciones INCOSE sin eludir acceso (FR-010/011/013).
- [x] T088 Extraer por página/sección con originales preservados, contrastar texto/listas/tablas y muestras visuales, separar disponibles/cuarentena, mapa concepto→pasajes y discrepancias (FR-013/019, SC-005 documental). Depende de T087.
- [x] T089 Reutilizar Materiales en perfil documental aislado sin vectores ni modelos; acceso, originales/localización y versión, sin alterar catálogo/demo habituales (FR-010/019, SC-003). Depende de T088.
- [x] T091 Verificar launcher seguro desde entorno habitual, acceso, consulta, cierre y reentrada; pruebas negativas, estilo/build aplicable, informe y guion corto con límites (FR-011/012, SC-003/004). Depende de T089. T090 conserva su significado histórico.

Estado parte2: implementada y verificada técnicamente; disponible para prueba docente, aún no probada/aceptada por el usuario. [Informe y límites](../../docs/audits/2026-10-27-part2-corpus/report.md). Corpus v1.1 con43 pasajes/páginas disponibles, cuarentena explícita e INCOSE no adquirida por condiciones/acceso técnico. Consulta documental sin vectores; T077 y gates permanecen abiertos. Sin continuación automática.

## Ampliación autorizada: todo el bloque de requisitos, 27-10-2026

- [x] T092 Establecer matriz real por subtema de los PDF principales y revisar material docente adyacente pertinente sin alumnado ni duplicación de formatos; preservar v1.1 (FR-010/013).
- [x] T093 Crear paquete-v2 con QA integral docente, complementos oficiales pertinentes, derechos/hash/posiciones, discrepancias y huecos explícitos; no habilitar texto incompleto por coherencia aparente (FR-013/019, SC-005 documental).
- [x] T094 Permitir selección explícita/reversible de versión en launcher/documental existente, manteniendo v1.1 por defecto y sesiones ajenas intactas (FR-010/011, SC-003).
- [x] T095 Verificar integridad, controles y recorrido real de navegador en puerto propio, subtemas distintos, originales/tablas/figuras, cierre/reentrada y vuelta a v1.1; entregar informe y reporte único autorizado al coordinador, sin iniciar incremento posterior (FR-012, SC-003/004).

Entrega v2: [informe](../../docs/audits/2026-10-27-requirements-block/report.md) y [matriz](../../docs/audits/2026-10-27-requirements-block/coverage-matrix.md).117 unidades textuales habilitadas y12 subtemas representados con huecos;103 páginas principales revisadas visualmente. INCOSE no incorporada por403 local; figuras ysecciones incompletas continúan fuera del texto habilitado. T093 completa esta entrega con límites, no la adquisición ausente ni la extracción íntegra de todo recurso. No aceptación docente, índice, generación o participante; gates yestados históricos intactos. Sin continuación automática.

## Incremento autorizado de recuperación v2.1, 27-10-2026

- [x] T096 Inventariar corpus/recursos existentes y congelar banco de24 escenarios de12 subtemas +6 controles, oráculo de pasajes y criterios/presupuesto antes de observar rankings (FR-010/013, SC-005 limitado).
- [x] T097 Componer identidad efectiva CPU local y fragmentación por tokenizer con offsets, construir/reabrir índice nuevo aislado con adaptadores existentes y comprobar mismatch/integridad/capacidad/idempotencia; no cerrar T077 global (FR-011/012/013).
- [x] T098 Integrar consulta optativa de pasajes/originales en Materiales con revalidación tras espera y cierre/reentrada, manteniendo perfiles documentales por defecto (FR-010/019, SC-003).
- [x] T099 Comparar una vez léxico/denso/RRF según protocolo congelado, reportar preguntas/subtemas/candidatos/contexto/tiempos y decidir sin optimización adicional. Resultado negativo: denso y RRF pierden Q06 en contexto final, baseline conservado; no se acredita suficiencia semántica (SC-005 limitado).
- [x] T100 Verificar regresiones/negativos, estilo/build y navegador real; entregar guion, hashes, errores y limitaciones, detener recursos propios y reporte único al coordinador. No generación, aceptación docente ni cierre global de Feature012.

[Informe y evidencia](../../docs/audits/2026-10-27-retrieval-increment/report.md). Estos IDs describen la entrega técnica acotada, incluida su decisión negativa de promoción; no completan los consumidores históricos ni los gates semánticos/humanos.

T100: implementación, pruebas, navegador, guion y parada completados; únicamente reporte interchat pendiente. Revisión automática rechazó el envío al destinatario indicado por considerar insuficientemente acreditada autorización/destinatario. No se envió, no se intentó otra vía y se solicitó confirmación humana explícita.

T100: reporte final enviado correctamente al coordinador01a14951-9510-70d0-85e5-25d51ab1b6ec, host local, tras confirmación humana explícita («Si, no me pidas autorización»). El rechazo inicial se conserva como antecedente; no hubo mensajes a otros chats ni continuación al generador.

## Primera conversación generativa autorizada, 27-10-2026

- [x] T101 E0: inventariar consumidores/configuración, distinguir bruto/diagnóstico/participante, conservar gate positivo de LaboratoryConversation y verificar contratos CPU sin inferencia. Helper de preflight con recibos exclusivos;78 pruebas correctas. No se activa vista nueva ni se acredita generación v2. [Informe](../../docs/audits/2026-10-27-first-generated-study/report.md).
- [x] T102 E1: compatibilidad resuelta por protocolo sucesor50s sin ampliar backend; conexión densa v2 experimental y captura real14B NF4 completadas28-10-2026.8/8 preguntas stop y1calentamiento, revisión técnica con errores de contenido conservados; no promoción ni aceptación. Primer arranque90s falló mecánicamente con0preguntas/0warmups; recuperación explícita180s conserva reloj global20min y recibos exclusivos. [Informe](../../docs/audits/2026-10-28-first-generated-study-real/report.md).
- [ ] T103 E2: solo tras episodio completo revisable y frontera docente segura, verificar arranque/pregunta/seguimiento/ejemplo/cancelación/cierre/reentrada/fuentes; preparar transcripción íntegra móvil y ofrecer prueba docente honesta. Ejecución técnica real acreditada en recovery-002 de la auditoría E2 del28-10; transcripción y arranque disponibles. Aceptación personal del usuario pendiente; no se declara tutor aprobado.

T090/T150/G2/SC001 y salida participante cerrados; T077 global no completado. No cierre de Feature012. Copias de spec/plan/tasks anteriores en dossier `before/`, sin regeneración de IDs/estados.

## Seguimiento humano «sigamos con cpu», 27-10-2026

- [x] T104 Implementar conexión ejecutable v2.1 densa experimental → GenerationPort existente → recibo de bruto/candidata → inspección docente temporal unverified/not_assessed, con binding propio v2/actividad fija, fuentes legibles, renderer inerte e historial de lo mostrado. Proveedor habitual desconectado; fixture rotulado optativo. Permiso de inspección no publica ni simula suficiencia; LaboratoryConversation intacto.
- [x] T105 Congelar protocolo sucesor50.000ms/768tokens/8peticiones+1warmup/20min sin alterar v1 rechazado; verificar exactitud/negativos del adaptador, aislamiento, retirada, duplicados/ocupado, cancelación tardía, timeout, truncado, retención/purga y regresiones, recuperación densa real CPU y UI fixture.98 pruebas correctas, estilo/build/ESLint correctos. Preparar runner futuro sin ejecutar LLM y entregar evidencia móvil; detener servidores propios.

[Informe CPU y contrato efectivo](../../docs/audits/2026-10-27-generated-study-cpu/report.md). T102 sigue pendiente exclusivamente de ejecución/captura/revisión generativa real; su cableado CPU ahora está implementado por T104/T105. T103 sigue pendiente E2 con contenido real; UI fixture verificada no lo completa. Protocolo50s nuevo preparado, no autorización de inferir durante este seguimiento. T090/T150/G2/SC001 y participante cerrados; T077 global y Feature012 no cerrados. Sin nuevos modelos, campañas, examen o voz.

## E1 real autorizado y detenido, 28-10-2026

- [x] T106 Ejecutar captura real congelada14B NF4/denso v2.1/CPU encoder, preservar primer fallo mecánico de arranque y corregir solo su presupuesto de preparación con pruebas; mantener reloj global y cupo,8preguntas+1warmup, bruto/contexto/finish_reason/historial completos; revisar contra originales y entregar transcriptos móvil.69regresiones CPU correctas,8/8stop pero errores de significado A3/B1 y cobertura/terminología; ambos árboles propios detenidos. [Informe](../../docs/audits/2026-10-28-first-generated-study-real/report.md).

Actualización de estado posterior a la entrega CPU: T102 completa captura/revisión técnica E1 con resultado negativo de calidad, no autorización de tutor. La nota anterior que la mantenía pendiente corresponde al seguimiento CPU del27-10 y se conserva como historial. T103 continúa pendiente de UI real/E2 y decisión docente; las8llamadas ya consumidas no habilitan otra interacción. No otro modelo, ajuste del banco, reserva, examen o voz; T077global y feature abiertos, T090/T150/G2/SC001/participante cerrados. Tras reporte único al coordinador termina el alcance.

## Revisión/reparación solicitada y rectificación del revisor, 28-10-2026

- [x] T107 Implementar composición diagnóstica optativa de GenerationPort: crítica con testigos, una reparación, post-revisión, presupuesto por llamada, permiso/retención/cancelación y trazas por sesión; conservar historial solo de final mostrado y exponer cadena inerte en Materiales. Default histórico y participante intactos; contratos CPU/UI fixture y build comprobados.
- [x] T108 Medir autocrítica del14B por separado sobre4respuestas expuestas+4nuevas cercanas, protocolo congelado,14llamadas+1warmup y resultados íntegros:0mejoras claras,2errores prioritarios intactos,1reparación más larga sin ganancia. No se valida un verificador semántico; [informe negativo](../../docs/audits/2026-10-28-review-repair/report.md).
- [x] T109 Rectificar según objeción humana la sustitución de la revisión del asistente por autocrítica: congelar críticas explícitas del asistente contra fuentes de4casos expuestos, ejecutar una corrección local por caso, revisar resultados reales por el asistente y conservar antes/después/coste.2objetivos corregidos y2mejoras parciales; defectos residuales y ausencia de autonomía explícitos. [Informe](../../docs/audits/2026-10-28-agent-assisted-repair/report.md).

T107–T109 completan implementación y experimentos diagnósticos, no una puerta semántica aprobada. La fase actual no equivale a E2 real de T103, no cierra T072/T077global o Feature012 y conserva T090/T150/G2/SC001/participante cerrados. No mensajes interchat adicionales ni uso de reserva o nuevos modelos por esta petición.


## Phase 1: Convergence — incremento web restringido, 30-10-2026

Revisión acotada T114–T118 (no cierre de Feature012). [Informe y evidencia](../../docs/audits/2026-10-30-web-fallback-runtime/report.md). T114/T115 completan política/adquisición operativa, incluida adquisición real; no validación del contenido. T116 tiene contratos separados y cobertura docente ampliada, sin evaluadores acreditados. T117 integra inspección atribuida mediante decisión docente explícita, sin explicación web automática. T118 acredita negativos CPU y adquisición real; faltan controles semánticos reales y casos independientes sin ajuste. Sus tres casillas permanecen abiertas. No cambian FR-014, T090/T150, G2/G3/G4, consentimiento, reserva ni sesiones anteriores.

- [ ] T151 Acreditar evaluadores locales separados de respaldo externo y compatibilidad docente con testigos, contexto/edición, independencia de fuentes y huecos de extracción; reutilizar los contratos de `web_review.py` sin aprobar por citas/HTTP/autocrítica (FR-022/023, T116; partial).
- [ ] T152 Conectar una decisión autónoma de alcance/insuficiencia acreditada tras ampliación local con adquisición/revisión/generación/revisión final y atribución; conservar la parte respaldada y bloquear afirmaciones conflictivas o inciertas, sin usar la inspección manual como sustituto (FR-014/016/021/023, T117; partial).
- [ ] T153 Medir una vez controles semánticos nuevos no usados para ajustar: complemento compatible, contradicción fuera del top-k, terminología distinta, fuente falsa/duplicada e incertidumbre; informar permisos/conflictos falsos y cobertura, con conversación íntegra y continuaciones reales antes de cualquier promoción (SC-009, FR-022/023/024, T118; partial).


## Ensayo semántico y navegador reales — 30-10-2026

- [x] T154 Ejecutar dos ensayos locales CPU finitos con casos/oráculos separados y congelados, medir decisiones de contenido reales frente a controles no usados para ajustar, preservar errores de arranque y salidas completas, y rechazar promoción por los fallos observados (FR-022/023, SC-009; no completa T116/T151).
- [x] T155 Completar navegador real de la nueva inspección web: aviso previo, descarga pública, enlace/edición, límite incierto, continuación local sin contaminar historial/cuota, expiración, reentrada/cierre y parada propia; fixture generativo identificado, sin acreditar semántica ni explicación web autónoma (FR-021/024, parte de T118).

[Informe](../../docs/audits/2026-10-30-web-semantic-cpu/report.md). T116–T118 y T151–T153 permanecen pendientes. Esta medición aporta resultados reales de dos mecanismos candidatos; ninguno satisface el criterio de promoción y no se conectan a respuestas. No se usó la reserva histórica ni se reinterpretó una contradicción artificial como discrepancia real del profesor.


## Phase 2: Convergence — contraste real CPU y navegador, 30-10-2026

Análisis acotado final: FR-014/016/017/019/021/022/023/024 y SC-008/009 con cobertura de tareas, sin nueva contradicción constitucional ni autorización de salida. Tres hallazgos altos parciales; no se cierra la feature. Estos IDs concretan los pendientes originales, no los sustituyen ni autorizan otra campaña automáticamente.

- [ ] T156 Acreditar un mecanismo de respaldo externo y compatibilidad que distinga oposiciones reales de diferencias de contexto y ausencia de evidencia, con fuentes originales, testigos y procedencia/independencia; los candidatos CPU 1.5B y 7B medidos no cumplen, sin resolverlo con reparación de JSON (FR-022/023, T116/T151; partial).
- [ ] T157 Conectar y medir la ruta autónoma de alcance e insuficiencia tras revisión local ampliada, adquisición autorizada, doble contraste, generación y revisión independiente, con explicación útil en el positivo y límite/contexto en negativos, dentro de presupuestos de la actividad (FR-014/016/021/024, T117/T152; partial).
- [ ] T158 Verificar esa ruta en cuatro situaciones nuevas sin ajustar sobre C01–C04 o D01–D04 ni usar la reserva histórica, separar permisos/rechazos/conflictos falsos y abstenciones, comprobar fuentes/edición y conversaciones reales antes de promoción (SC-009, T118/T153; partial).


## Rondas de revisión/corrección propuestas por el usuario — 30-10-2026

- [x] T159 Implementar y probar composición optativa y autónoma de crítica de respaldo/compatibilidad, objeciones con testigos, reparación localizada y nueva revisión, con dos rondas/caso, presupuestos y parada por falta de mejora; reutilizar mecanismos existentes sin publicar por autocrítica (FR-014/022/023, T116/T117/T151/T152).
- [x] T160 Congelar y ejecutar ensayo CPU pequeño con positivos, oposición real de afirmaciones en el mismo contexto, términos compatibles e insuficiencia; comparar inicial/final, críticas equivocadas, errores nuevos y falsas aceptaciones, conservar fuentes/versiones/tiempos y límites sin reinterpretar C/D ni críticos humanos anteriores como automatizados (SC-009, T118/T153/T158).


Entrega T159/T160: [rondas CPU con resultado negativo](../../docs/audits/2026-10-30-web-rounds-successor-cpu/report.md). T159 completa orquestación/prototipo de ejecución y controles CPU, no capacidad semántica ni despliegue; T160 completa medición/conservación del ensayo, no utilidad acreditada.0mejoras aplicadas/4casos; dos reparaciones completas idénticas, parche14B incompleto, críticas falsas/omisiones registradas.137pruebas CPU; ni fixtures ni acuerdo de modelos se presentan como validación. El sucesor consumió11/12llamadas,1517,625s/1800s; el predecesor cerró15intentos/1531,437s sin reiniciarse. No se reinterpreta ningún resultado anterior ni se usa reserva. T116–T118/T151–T153/T156–T158 y gates siguen pendientes.


## Phase 3: Convergence — rondas automáticas CPU, 30-10-2026

Analyze acotado: FR-014/016/019/021/022/023/024 y SC-009 con tareas trazadas, sin nueva contradicción constitucional o requisito del incremento sin tarea. Tres hallazgos altos parciales; no autorización semántica. Las fases y recuperaciones mantienen evidencia/presupuestos distintos, no se convierten en una campaña validada ni en aprobación por acuerdo de modelos.

- [ ] T161 Acreditar un crítico automático que encuentre las inferencias sin premisa y conserve las etiquetas conceptuales de las fuentes; distinguir fuente que sustenta una atribución de oposición docente sobre esa proposición, sin falsas objeciones a ejemplos coherentes/no exhaustivos (FR-014/022/023, T116/T151/T156; partial).
- [ ] T162 Lograr y medir una corrección autónoma completa que mejore el defecto localizado, conserve lo válido y permita post-revisión real dentro de recursos explícitos; no declarar avance por cambios de estilo, texto idéntico, parche incompleto o acuerdo de críticos (FR-014/016/023/024, T117/T152/T157; partial).
- [ ] T163 Validar el ciclo sobre casos nuevos no usados para ajustar R01–R04 o C/D, con críticos/pasajes/procedencia y aceptación falsa/daño/abstención separados, antes de conectar la ruta web autónoma y de cualquier promoción (SC-009, T118/T153/T158; partial).

## Corrección de instrucciones del revisor — autorización del usuario, 30-10-2026

- [x] T164 Añadir perfil optativo web-review/v2 con roles de revisor/corrector propios, sin heredar la prohibición de IDs del tutor; conservar datos protegidos, versión v1 y evidencia/objeciones automáticas (FR-022/023, T161).
- [x] T165 Probar CPU el perfil y ejecutar diagnóstico acotado sobre borradores expuestos, conservando críticas y cambios completos, sin introducir las objeciones humanas en el prompt ni promover por acuerdo (T162; no sustituye T163).

- [x] T166 Implementar sustitución literal localizada a partir de la primera objeción automática anclable, rechazando ambigüedades y cambios fuera del objetivo; tratar comillas como presentación sin inventar citas, preservar brutos y distinguir corrección mecánica de juicio semántico (FR-014/020/023, T162).
- [x] T167 Ensayar una sustitución localizada CPU y post-revisión sobre R01 expuesto, comparar con la regeneración completa, conservar críticas equivocadas y defectos del selector detectados sin atribuir generalización ni cambiar presupuestos previos (FR-011/012, SC-009, T162/T163).

Entrega acotada: [perfil v2 y parche localizado](../../docs/audits/2026-10-30-web-review-prompt-v2/report.md).
128 pruebas CPU; ocho llamadas reales en tres presupuestos conservados. La regeneración
completa mantiene el error; el parche elimina la inferencia indebida en un caso
expuesto, pero el crítico posterior rechaza ficción admisible y exige cobertura
innecesaria. Comillas y selector corregidos con negativos previos; el último ajuste
del selector solo tiene validación CPU, sin otra inferencia. No cierra T161–T163,
los pendientes web anteriores, Feature012 ni gates/participantes.

## Phase 4: Convergence — perfil de revisión y parche localizado, 30-10-2026

Análisis acotado de FR-011/012/014/019/020/022/023 y SC-009: cobertura de tareas del
incremento, sin contradicción crítica nueva ni publicación por acuerdo. Dos brechas
altas parciales, relacionadas con T161–T163; no sustituyen los pendientes originales.

- [ ] T168 Acreditar una revisión que no rechace valores hipotéticos coherentes por ausencia literal ni exija listas completas cuando la pregunta pide un ejemplo; detectar a la vez inferencias sin premisas y falsas atribuciones, con objeciones justificadas y controles positivos/negativos nuevos (FR-014/020/022/023, T161; partial, HIGH).
- [ ] T169 Validar en casos nuevos el selector corregido, el parche y la revisión posterior con fuentes vigentes, conservación de contenido válido, permisos/rechazos falsos y latencia; conectar la ruta autónoma solo tras evidencia suficiente, sin promover el resultado R01 expuesto ni reabrir presupuestos anteriores (SC-009, FR-014/023, T162/T163; partial, HIGH).

## Tolerancia del revisor autorizada por el usuario — 30-10-2026

- [x] T170 Implementar perfil optativo web-review/v3 de adecuación a la pregunta, separado de perfeccionismo/cobertura opcional y datos ficticios; conservar controles de errores materiales, fuentes y gates; calibrar una pareja expuesta correcta/defectuosa en CPU sin acreditar generalización (FR-014/020/022/023, T168).

[Perfil y medición de tolerancia](../../docs/audits/2026-10-30-review-tolerance-v3/report.md):
131 pruebas dirigidas y tres llamadas CPU. Acepta el ejemplo correcto y detecta una
contradicción explícita; omite la inferencia de medibilidad a realizabilidad.
T170 completa implementación/calibración, no acreditación semántica. T168/T169 y
los pendientes de integración/publicación siguen abiertos. Sin GPU ni cambios de gates.

## Variedad de contenidos web y afinado CPU — petición del usuario, 30-10-2026

- [x] T171 Corregir el rechazo de cabeceras Link repetidas legales observado en páginas NASA, mantener rechazo de cabeceras críticas ambiguas y conservar fallos previos, negativos y adquisiciones reales posteriores (FR-024).
- [x] T172 Construir fuentes/casos de revisión variados y congelados, medir v3 en seis casos nuevos de desarrollo y, si hay causa justificable, ensayar como máximo un ajuste sin usar los resultados de transferencia para afinar (FR-011/012/020/022/023, T168).
- [x] T173 Medir una sola vez cuatro casos técnicos separados de transferencia sobre otros temas del curso con el candidato seleccionado, conservando juicio por contenido, contratos, tiempos, permisos/rechazos falsos e incertidumbre; no abrir gates por esta muestra (SC-009, T168/T169).

[Resultado CPU y transcripción](../../docs/audits/2026-10-30-review-web-variety/report.md):
cinco fuentes primarias, seis casos de desarrollo y cuatro de transferencia.
v3 acepta los cinco ejemplos válidos, pero no entrega revisiones utilizables de
los cinco defectuosos; cuatro detectan el problema principal y uno razona mal.
Un único ajuste v4 no promovido por falsa objeción y contraste docente no probado.
Intento de calibración inválido por copia con codificación equivocada conservado,
corregido y separado de los resultados evaluables. 139 pruebas finales; Ruff sin
hallazgos nuevos. T172/T173 completas como medición, no acreditación. T168/T169 y
publicación siguen abiertas; sin GPU, Reset ni commits.


## Referencias legibles también en el revisor — 31-10-2026

- [x] T174 Implementar contrato de revisión/corrección por referencia al documento/página o URL, sin citas literales ni copia exacta del claim; componer presentación desde metadatos enlazados a fuentes/versiones, rechazar referencias ajenas y verificar el bucle con pruebas CPU, sin promover semántica ni participantes (FR-019/022/023, T168/T169).
- [ ] T175 Medir el nuevo contrato con modelo real y controles positivos/negativos nuevos: formato, pertinencia, apoyo, contraste docente y reparación; distinguir mejoras de formato de mejoras de contenido y no reetiquetar las salidas históricas como ensayos v5 (FR-014/019/022/023, T168/T169).

[Contrato, pruebas y límites](../../docs/audits/2026-10-31-review-source-locations/report.md):
160 pruebas CPU. Perfil v5 conectado al bucle de laboratorio con metadatos del host;
no hay inferencias nuevas ni acreditación semántica. Versiones anteriores preservadas.

- [x] T176 Repetir una sola vez los diez casos conocidos de variedad web bajo v5 en CPU, conservando preguntas/pasajes/oráculos y separando formato de contenido; registrar referencias legibles, falsos juicios, tiempos y límites, sin contar esta regresión expuesta como controles nuevos para T175 (FR-019/022/023).

- [x] T177 Recuperar la política completa de tolerancia v3 para fuentes docentes y web con igual criterio; conservar el contrato por documento/página o URL y distinguir contradicción externa de conflicto docente; verificar con pruebas CPU y cuatro controles expuestos pareados, sin usar datos ficticios coherentes ni mejoras opcionales como motivo de rechazo (FR-019/020/022/023, petición expresa del usuario 31-10).

[Repetición v5 completada](../../docs/audits/2026-10-31-review-locations-retest/report.md): diez salidas completas CPU, referencias por identificador conocido, cinco defectos principales detectados pero cinco respuestas correctas rechazadas. Sin promoción. La petición posterior de igualar la tolerancia se continúa por separado en T177.

[Criterio común y medición](../../docs/audits/2026-10-31-equal-review-criteria/report.md): prefijo v3 conservado íntegro, referencias sin citas, 169 pruebas CPU. Cuatro llamadas reales: recupera aceptación de un ejemplo ficticio y detecta ambos errores principales; persiste rechazo falso del mínimo 5:1 y falta de justificación docente en una clasificación. T177 completa implementación/medición; no acredita T168/T175 ni abre publicación.

## Avance autónomo autorizado con GPU — 31-10-2026

- [x] T178 Registrar y revalidar el perfil de revisión y sus metadatos en adaptador/worker GPU, confirmar el perfil efectivo en recibos y preservar rechazos de manipulación sin afectar frames históricos (FR-014/019/024, T169).
- [x] T179 Comparar candidatos locales que quepan en la GPU libre con criterios iguales docente/web, sin tocar modelos ajenos; solo avanzar a controles nuevos si mejora la adecuación semántica, separando formato, recursos y calidad (FR-020/022/023, T168/T175).
- [ ] T180 Si un candidato supera desarrollo, medir revisión/corrección/revisión en casos nuevos con generación real, fuentes y referencias vigentes, conservación de contenido válido y criterios de parada; no inferir publicación por acuerdo del modelo (FR-014/015/023, T169).

[Transporte y comparación GPU](../../docs/audits/2026-10-31-gpu-review-progress/report.md): 544 pruebas del módulo, ocho llamadas completas, ningún candidato promovido. T180 no ejecutada por no superar desarrollo.

- [x] T181 Implementar y medir una variante optativa de veredicto primario único: el host deriva solo acción mecánica y conserva respaldo/compatibilidad desconocidos, sin inferir verdad ni alterar versiones previas; distinguir propuestas hipotéticas, atribuciones y postura docente, con negativos CPU y una única calibración expuesta de cuatro llamadas. Solo si supera todos los controles, congelar transferencia nueva para T175/T180 (FR-019/020/022/023).

[Decisión única medida](../../docs/audits/2026-10-31-minimal-review-successor/report.md): cuatro llamadas completas, contrato 4/4, revisión adecuada 3/4, persiste falso permiso material. No promovida; T175/T180 siguen abiertas. Eliminar redundancia no acredita respaldo ni contraste docente.
