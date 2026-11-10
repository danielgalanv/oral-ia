# Chat de autoestudio conectado e interfaz sencilla

Implementados T188–T190. La vista `/estudio` presenta conversación, pregunta, Enviar, Cancelar mientras se prepara, Fuentes y Finalizar; Reintentar aparece solo si el servicio necesita recuperación. No muestra cambio de tema, texto bruto, presupuestos o etiquetas técnicas. La vista docente anterior se conserva.

- [Captura móvil de la vista nueva — respuestas simuladas](browser-1793620717094/student-chat.png).
- [Resultado del navegador final](browser-1793620717094/result.json).
- [Comprobaciones finales y preservación](final-checks.json).
- [Regresión amplia](regression.log) y [pruebas dirigidas tras RRF](release-tests.log).

## Conexión

El nuevo runtime optativo reutiliza WebReviewRounds v7: Qwen2.5-14B genera, Qwen3-8B con razonamiento revisa, el generador corrige si hay objeciones y vuelve a revisarse. Máximo dos correcciones y un reintento de formato del revisor. La pantalla recibe únicamente la respuesta final seleccionada; una candidata inicial no se publica mientras se revisa. Los estados sin resolución devuelven una explicación de límite y permiten continuar, sin aprobarlos por acuerdo estructural.

Usa recuperación RRF y la selección comparativa existentes, con documentos autorizados. Las localizaciones llegan desde los pasajes comprobados del host, nunca se extraen de las afirmaciones del modelo. Se revalidan permiso, fuente y reloj entre etapas. Historial y presentación conservan el texto mostrado. La API del modo simple elimina request, outcome, transporte, bruto y trazas de reparación; las fuentes llevan solo documento, página y enlace al original.

Los dos workers pertenecen al runtime. Se comprueba capacidad libre y actividad GPU antes de cargar; no se detienen procesos ajenos. El fallo al cargar el revisor cierra el generador. El reloj global y los presupuestos se comparten entre sesiones/reentradas: doce preguntas, hasta 84 llamadas de modelo, etapas de hasta 180 s y un límite de 600 s por turno, siempre acotado además por el runtime global. Recargar no reinicia esos contadores. Se conservan los perfiles históricos; el ciclo revisado requiere selección explícita.

## Contexto automático

La búsqueda parte de la pregunta actual cuando es autónoma. En seguimientos referenciales como «¿por qué?», «otro ejemplo» o «ese requisito», reutiliza la última pregunta que contiene el referente. Si falta referente pide aclaración, sin inventar una explicación académica ni consumir una generación. La conversación mostrada se mantiene aunque cambie el tema. Se conserva la capacidad previa de tres pares recientes en el request del modelo; no se declara memoria ilimitada.

Es una política conservadora de recuperación, no un nuevo clasificador semántico ni una prueba universal de interpretación. La selección de contexto en la vista simple es responsabilidad del servidor incluso si un cliente intenta enviar el antiguo control manual. La vista docente puede conservar ese control para diagnóstico.

## Pruebas CPU

- 685 pruebas de regresión aprobadas.
- 72 dirigidas tras alinear la recuperación revisada con RRF, y trece del módulo final tras endurecer el control de contexto del alumno. Son ámbitos superpuestos; no se suman como pruebas únicas.
- Quince pruebas de UI aprobadas; TypeScript, Vite y ESLint correctos. Black conforme y Ruff global conserva diez diagnósticos anteriores, cero nuevos con multiplicidad.
- Navegador real en escritorio y 390 px, GPU de renderizado desactivada, HTTP real y ciclo de revisión de producción conectado a puertos simulados explícitos. La prueba provocó una reparación y comprobó que solo apareció la versión final. Probó seguimiento, nueva pregunta, fuentes, cierre, ausencia de detalles internos y ausencia de desbordamiento horizontal. Abrir/cerrar una pestaña sin iniciar sesión no cierra la conversación activa. No hubo peticiones externas ni errores JavaScript.
- Ciclo de vida de ambos workers y fallo parcial de carga comprobados con contextos simulados; cancelación durante revisión impide entregar el borrador y conserva llamadas consumidas.

No hubo inferencias generativas ni cargas GPU. El comando de preparación sí construyó un índice real con embeddings CPU locales en una raíz nueva. Las salidas «FIXTURE» del navegador prueban la conexión y no se cuentan como respuestas académicas del modelo ni como evidencia de eficacia.

## Arranque

Desde ORALIA, cuando se autorice usar GPU:

```powershell
.\scripts\study-chat.ps1
```

Prepara interfaz e índice propios y abre `/estudio` cuando el servicio está listo. Ctrl+C cierra los procesos propios. Para preparar únicamente los recursos CPU:

```powershell
.\scripts\study-chat.ps1 -PrepareOnly -NoBrowser
```

Este último comando se ejecutó correctamente, sin modelos generativos, con salida aislada en `.claude-scratch/study-chat-20261102-124735-09a2bbf7`. La selección de puerto es explícita mediante `-Port`; no se cierra ningún proceso ajeno. No se construye sobre índices habituales ni se reinstala Node; se reutiliza una instalación local disponible.

## Alcance, fallos conservados y pendiente

Se preservaron los logs iniciales: expectativas antiguas que vaciaban historial al cambiar tema se actualizaron a la nueva necesidad; una expectativa de perfil v1 estaba desfasada respecto a v2; una prueba de recarga usaba una pregunta referencial sin contexto y se cambió a una pregunta autónoma para probar recarga. El último navegador se lanzó una vez antes de que el servidor acabara de compilar: no envió preguntas; se añadió espera de disponibilidad y se conservó ese fallo. No se borraron ni reclasificaron esos intentos como éxitos.

Se corrigió además la limpieza en StrictMode: una pestaña que aún no ha iniciado sesión no debe cerrar una conversación existente. Se conservan fuente ejecutada y snapshots de release. Los grupos históricos de 308, 140 y 22 archivos conservan sus hashes. No hubo cambios de SQL, migraciones, audio, Reset o commits. Los servidores CPU de prueba están detenidos y su puerto quedó libre.

Es una nueva vista local de ensayo bajo el acceso ya existente, no una apertura de permisos generales de participantes ni de publicación. Internet autónomo sigue en sus tareas previas. **T191 sigue pendiente:** verificar el chat integrado con ambos modelos reales cuando vuelva a autorizarse GPU. Las pruebas GPU antiguas de generación/revisión por lote no sustituyen esa comprobación. Feature 012 permanece abierta.
