# Prueba personal de ORALIA

Duración prevista: 10–15 minutos. Solo datos ficticios; generación determinista,
fuentes mediante embeddings locales. Voz real y utilidad con personas sin validar.

Preparación: `./scripts/demo.ps1 -Action Check`. Arranque: `./scripts/demo.ps1`.
La demo local abre el área docente sin credencial. Usar solo datos ficticios.
Abrir http://127.0.0.1:5180 y usar el código ficticio `demo-007`.

| Paso | Resultado esperado | Observación personal |
|---|---|---|
| Abrir portada y recorrer enlaces con Tab/Enter | Se entienden modos, límites y avisos | |
| Entrar en Área docente | Acceso directo sin credencial, solo en demo | |
| Abrir autoestudio del agua | Actividad preseleccionada, sin copiar ID | |
| Leer aviso y elegir transcripción/resumen | Elecciones independientes y comprensibles | |
| Preguntar «¿A qué temperatura hierve el agua?» | Respuesta con 100 grados y fuentes desplegables | |
| Abrir fuentes con teclado | Documento, versión, ubicación y fragmento legibles | |
| Finalizar y revisar desde docente | Solo sesión autorizada; entradas y respuestas distinguibles | |
| Revisar texto libre y exportar JSON/Markdown | Archivos legibles sin el código demo-007 | |
| Eliminar únicamente la sesión ficticia recién creada | Recibo; deja de estar disponible para revisión/exportación | |
| Abrir defensa y no conservar | Puede participar; al cerrar no aparece en revisión docente | |
| Parar con `./scripts/demo.ps1 -Action Stop` | Servicios detenidos y datos demo preparados | |

Registrar cada problema con paso, texto exacto del mensaje y qué se esperaba.
Valorar especialmente claridad, legibilidad, navegación por teclado y tiempos de espera.
No introducir datos personales ni extraer conclusiones sobre utilidad educativa a partir
de esta única demostración.

## Recuperación

- Puerto ocupado: el lanzador lo informa; no mata procesos ni cambia puertos solo.
- Sesión abandonada: volver a su pestaña y finalizar. Si se perdió acceso, parar y
  seguir el Reset explícito de DEMO.md, que borra exclusivamente los datos demo.
- Embeddings ausentes: preparar caché explícitamente o usar `-TextOnly`, sin fuentes.
- Reinicio: volver a entrar; los accesos anteriores dejan de ser válidos.
- Fallo de arranque: revisar `.oralia-demo/logs`; no borrar la base habitual.

## Comprobación automática repetible

`./scripts/check-demo.ps1` ejecuta pruebas de recuperación/aislamiento, el recorrido
de navegador con recursos aislados y el preflight de la demo preparada. No hace Reset.
Guarda resultado JSON y logs en `.claude-scratch/demo-checks/<fecha-hora>/`.
No sustituye la evaluación visual y personal de la tabla anterior.
