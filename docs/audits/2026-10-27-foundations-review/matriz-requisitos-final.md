# Trazabilidad interpretada de requisitos y decisiones

El [registro JSON](requirements-register.json) y su [versión CSV](requirements-register.csv) conservan 418 identificadores FR/SC de las doce especificaciones, línea de origen y correspondencias declaradas por sus mapas de cobertura. No se aceptan automáticamente esos mapas. Los requisitos que ocupan varias líneas se consultan completos en [las especificaciones extraídas](specifications-read.txt). Esta matriz agrupa sus fronteras de producto y añade criterios independientes; no pretende una verificación manual exhaustiva de cada identificador.

## Producto y experiencia docente — R01 a R07

**Origen:** decisiones humanas actuales, apartado específico del conceptual P1043–P1051, prompt original de Feature003 y FR-001/002/005/015/019 de Feature012. Consultar [fuentes y autoridad](origen-y-metodo.md).

La intención es resolver dudas, explicar y practicar por chat, con adaptación ante incomprensión. Una conversación puede atender una afirmación incorrecta sin calificar a la persona. Los cinco submodos históricos —dudas, guía, práctica, exposición y repaso— siguen siendo horizonte funcional, pero no son cinco capacidades pedagógicas acreditadas por sus opciones de configuración.

**Comportamiento real y evidencia:** agencias003, diálogo controlado010, extractivo011 y laboratorio012. La prueba de usuario del 18 de octubre muestra bucles; la comparación pedagógica posterior conserva repeticiones y confusión de atributos. La generación y el historial existen, pero la conversación útil sigue sin aceptación suficiente.

**Aceptación:** episodio completo con duda natural, cambio material de explicación y aplicación pertinente; no respuestas académicas predefinidas ni examen obligatorio por turno. El feedback describe el enunciado y sus premisas, sin nota ni perfil de capacidad. Los escenarios ficticios son válidos; el principio y la conclusión necesitan apoyo. Referencias generales legibles bastan en pantalla; la procedencia interna sigue siendo exacta. No volver a exigir IDs por frase ni llamar «contenido verificado» a «fuentes consultadas».

## Alcance, fuentes y representaciones — R08 a R11

**Origen:** decisión humana de alcance, Feature002 original, constitución V y Feature012 FR-004/013/017/018. Un tema puede estar permitido y carecer de material suficiente. Una cuarentena o un score bajo no lo excluyen. El requisito actual pide decidir antes de generar; la preclasificación anterior a toda búsqueda es una interpretación arquitectónica por contrastar.

**Comportamiento real:** política y binding, clasificador experimental que falla, unidades de PDF en012 y recuperación densa previa en002. PDF y PPTX no extraen tablas/diagramas de forma equivalente. Hay 139 páginas incluidas y 26 en cuarentena; esto no cubre todo el temario confirmado.

**Aceptación:** fuentes vigentes y filtradas, relación verificable con página o diapositiva original, pérdidas de extracción explícitas y ausencia de indexación incompleta silenciosa. Comparar recuperación sobre el mismo corpus y autoridad. Probar alcance incierto, mixto y operativo sin afirmar exclusión por vacío. OCR avanzado era opcional en el alcance inicial; su adopción focal es una propuesta de cobertura y recursos, no una obligación original ocultada.

## Identidad local y presupuestos — R12 a R14

**Origen:** reproducibilidad y ejecución local del original, constitución I/VII/VIII/IX y recursos configurables del paquete editorial. Elegir MiniLM, NF4, greedy o 512 tokens es una decisión de implementación o ensayo, no una ley del producto.

**Comportamiento real:** F01 reproduce la caché de embeddings que sirve A a una instancia configurada como B; F02 demuestra que `setdefault` no fuerza offline ante entorno `0`; F04 muestra máximos efectivos de 512/768 aun solicitando más. Los ensayos conservan configuración, pero no todos los anteriores capturaron el frame original.

**Aceptación:** identidad efectiva igual a la configurada; índice ligado al espacio vectorial y representación; ningún intento de red cuando falta el recurso local; presupuesto solicitado/efectivo explícito y validado antes del envío. Las reconstrucciones deben seguir distinguiéndose de capturas originales. No atribuir retrospectivamente errores pedagógicos a estos defectos sin evidencia.

## Verificación y autorización — R15 a R16

**Origen:** constitución IV, conceptual P1971, T090 vigente y Feature012 FR-006/008/014. El generador no puede aprobar su propia salida. La eficacia de los verificadores debe medirse; el original no prueba que se exigiera una garantía formal universal de toda frase libre.

**Comportamiento real:** T090 reconstruye composición y permisos; el ledger valida estructura y etiquetas recibidas; jueces posteriores producen falsos permisos y H1 carece de puente exhaustivo al texto final. El laboratorio conserva publicación cerrada. `supported` escrito por un modelo no es autoridad suficiente.

**Aceptación:** contrato sucesor versionado y revisado para vincular texto generado, revisión independiente, fuentes, sesión y vigencia. Mantener gates actuales mientras no se apruebe ese cambio. Medir apoyo, pertinencia, cobertura, premisas y omisiones del extractor, además de falsos permisos/rechazos. No convertir cero fallos en un banco finito en promesa universal; tampoco rebajar SC-006 por decisión del auditor.

## Estado, concurrencia y entrega — R17 a R18

**Origen:** estado externo del original, T150 y Feature012 FR-002/006/015. La memoria académica puede representar lo tratado en la sesión sin diagnosticar capacidad ni crear perfil longitudinal.

**Comportamiento real:** prepare/ack/discard preserva historial mostrado en escenarios probados; el cierre usa una transición condicional de base; el lock asíncrono vive en un proceso. Hay supuestos pendientes en mutabilidad y ventana entre revisión, envío y confirmación.

**Aceptación:** idempotencia de request, cierre ganador único, rollback y ausencia de efectos tardíos tras cancelación. Ensayar dos conexiones y retirada entre fases; solo el texto realmente mostrado entra en historial. Definir el punto de commit sin prometer retractar bytes ya vistos.

## Privacidad, acceso e inyección — R19 a R22

**Origen:** constitución VII, Feature005 FR-018/021 y plan de seguridad. El docente no obtiene por su rol permiso implícito sobre contenido sin consentimiento. El texto de documentos y participantes es dato no confiable.

**Comportamiento real:** scopes, expiración, exportación y cierre existen. La proyección técnica filtra claves, pero el contraejemplo aislado conserva strings bajo claves permitidas; no demuestra una fuga alcanzable. La purga es manual y omite sesiones todavía activas. Los tokens de acceso no sobreviven al reinicio. El host comprueba origen/rol, mientras las etiquetas del prompt no son aislamiento formal.

**Aceptación:** payloads por evento y productores revisados, scopes negativos en trazas/exportación y ensayo de caída/reinicio/cierre. Diferenciar acceso expirado, borrado lógico y residuos en WAL/backups; un compromiso nuevo de borrado forense requiere decisión de amenaza. Probar inyección con datos ficticios y permisos fuera del LLM. LAN, SSO o nuevos servicios no quedan autorizados por esta revisión.

## Operación, evaluación y evolución — R23 a R27

**Origen:** instalación local del original, comparación006, criterios de piloto P1976–P1983, voz004 y decisiones humanas actuales de posposición. La arquitectura multiagente es una hipótesis por medir, no una superioridad demostrada de antemano.

**Comportamiento real:** launchers y perfiles anteriores permiten demostraciones acotadas; course-dialogue ofrece inspección y bloquea publicación. Las 204 celdas son sintéticas; A/B/C tienen contenido diferente. Hay revisiones técnicas y D01 humano negativo, pero no utilidad docente general acreditada. Voz real no se demuestra con dobles ni texto. Seis evidencias históricas perdidas no se restauran mediante una nueva ejecución.

**Aceptación:** recorrido de autoría y estudio por teclado con capacidad honesta, errores accionables y cierre comprensible. Medir transferencia, pertinencia y carga docente por separado de mecanismos técnicos; comparación arquitectónica pareada con mismas fuentes/modelo/presupuesto. Preservar primeros fallos y exposición de bancos. Retomar voz tras el chat útil y su fase autorizada, sin reintroducir robótica o perfiles longitudinales.

Las decisiones de tecnología no verificadas se pueden recomendar, pero no se convierten aquí en requisitos humanos. Los originales no recuperados permanecen como brecha de procedencia; las especificaciones y gates vigentes no se modifican por esta matriz.
