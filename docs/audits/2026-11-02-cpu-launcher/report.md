# Operación y documentación del chat, sin inferencias generativas

Trabajo independiente de la validación GPU. No se volvió a ejecutar el generador ni el revisor en CPU.

## Corrección comprobada

`scripts/study-chat.ps1 -PrepareOnly -NoBrowser` terminaba con éxito, pero dejaba modificadas `PYTHONPATH` y `ORALIA_DEMO_CACHE_DIR` en la consola que lo invocaba. La [reproducción anterior](environment-before.json) registra ambas restauraciones falsas y ubicación restaurada correctamente. El [script anterior](study-chat-before.ps1) y [log](before.log) se conservan.

Ahora el lanzador conserva presencia y valor de las dos variables y los restaura en `finally`, tanto en éxito como en fallo. Se distinguen variables ausentes, vacías y con contenido. También comprueba Python y Vite locales antes de crear carpetas o ejecutar la preparación. No instala dependencias ni cambia de proveedor.

## Validación CPU

**Seis pruebas aprobadas**, en [final-tests.log](final-tests.log): Python ausente, Vite ausente, fallo controlado de construcción con variables ausentes/vacías/definidas y preparación real correcta. Los controles de fallo usan repositorios temporales y no ejecutan Python. La preparación real construye interfaz e índice con embeddings locales CPU; no carga generador/revisor ni inicia el servidor.

La [comprobación posterior](environment-after.json) confirma entorno y ubicación restaurados. El [recibo de preparación](prepared-launch.json) describe un futuro arranque que requiere GPU; la carpeta de runtime no se creó. No se presenta esa preparación como inferencia o como chat real validado.

Un primer control de variable ausente utilizaba una llamada .NET que en este entorno producía cadena vacía; se corrigió el montaje del test para quitar realmente la variable y se amplió al caso vacío. El lanzador conserva ambas situaciones, sin confundirlas. [Controles intermedios](boundaries.log).

Black conforme tras formatear el test; Ruff focal sin hallazgos y global sin diagnósticos nuevos frente al baseline con multiplicidad. La regresión de 716 pruebas anterior no se cuenta como ejecutada otra vez: aquí se validó el ámbito del lanzador con PowerShell real.

## Instrucciones vigentes

Se añadió [docs/ESTUDIO.md](../../ESTUDIO.md), una entrada única para preparar, arrancar y manejar el chat: envío explícito, fuentes, cancelación, recuperación, cuota, memoria temporal y límites reales. Distingue preparación CPU de inferencia GPU y no promete reutilización automática del índice preparado.

Se enlazó desde README y quickstart. El índice del corpus señala el paquete v2 y conserva el inventario inicial como antecedente. README ya no afirma que la adquisición web no esté implementada: distingue inspección de laboratorio de integración autónoma aún no acreditada. No se han cambiado estados de aceptación, gates o el corpus.

T199 queda completada. T191 sigue pendiente de prueba GPU. No hubo inferencias generativas, cambios de modelos/prompts, nuevos servicios, procesos ajenos detenidos, Reset ni commits.
