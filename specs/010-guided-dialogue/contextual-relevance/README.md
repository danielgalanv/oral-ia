# Pertinencia contextual tras auditoría independiente —21-10-2026

La repetición con política v4/materiales v7 refutó la conclusión anterior de 107/114 de que no quedaban brechas técnicas conocidas. El informe anterior, sus fuentes y reservas se conservan; no constituye aceptación de esta versión. [Hallazgos técnicos iniciales](preimplementation-findings.json), [recepción íntegra del auditor](audit-receipt.json) y Phase 10 / T115–121 registran las correcciones.

Las 100 peticiones capturadas son 76 entradas de guiones y 24 contrastes, no 100 fallos independientes ni aceptación. El control accidental v3 está separado. Solo se atribuyen los primeros desvíos reproducibles y los contrastes con pregunta realmente emitida; no se calcula eficacia global de las seis conversaciones fijas.

## Cambios acotados

- Proceso deíctico con ancla autorizada: se conserva el tema antes de buscar semejanza por palabras compartidas. Cada respuesta se contrasta con tema/proceso esperado además del grounding. Un tema nuevo con vocabulario ajeno no obtiene esa excepción contextual.
- Objeto decimal y propósito de procedimiento se distinguen del número de comparación. Material v8 explícito para formato decimal. Tras un fallo previo no se reutiliza el número de la última respuesta aprobada: se pide aclaración; una entrada no verificada no se convierte en autoridad.
- Petición de leer números junto al saludo atiende ambas cláusulas. Cálculo del alumno con seis intentos y cinco observaciones selecciona la explicación docente del divisor, sin calificarle ni hacer cálculo libre.
- Prefacio afirmativo seguido de orden de cierre propone la operación; no es una confirmación implícita. Conservación activa exige revocación confirmada y cierre posterior separado. Negación/cita y ausencia de propuesta siguen protegidas.
- Tres repreguntas publicadas agotadas se comunican como límite real, no falta de permiso. Plantilla aditiva explícita en `guided-screenless/v4`, revisión de política 2; no hereda permisos de mensajes anteriores. Ayuda/repetición siguen sujetas a fuentes, presupuesto y verificadores. No se inventan repreguntas ni se exime la repetición.

Materiales v1–v7 y documentos originales intactos. v8 es propuesta separada pendiente de revisión humana; se usa solo en BD temporales propias. No hay DDL, agentes, modelos, descargas, cambios de credencial o activación en la demo habitual. La política v4/revisión2 es una sucesora explícita de autorización; no se modifica ninguna actividad habitual ni se añaden permisos a su snapshot. V1–v3 conservan sus contratos.

## Evaluación

[Corpus y congelación](corpus-freeze.json):6 desarrollo / 6 reserva nuevos antes de los cambios; no se atribuye autoría humana independiente. Runner real API/SQLite/Chroma que responde únicamente a la pregunta efectivamente emitida, registra divergencia y comprueba tema, propósito/objeto, contenido, fuente y estado. Un HTTP200 no basta.

Rojo 0/6 conservado. Primera corrección incluye un error del comprobador al leer estado efímero ya eliminado tras cierre, separado de fallos de producto. También se conserva el negativo unitario de una variante de procedimiento. Desarrollo final 6/6, 39 pruebas dirigidas en 55,15 s; reserva nueva 6/6 en primera ejecución, 27,08 s. Fuente de 673 archivos congelada antes de esa reserva. Desarrollo natural anterior 6/6 como regresión en 34,66 s. Son propiedades acotadas; no demuestran comprensión general, que los 100 turnos fijos sean satisfactorios, ni calidad didáctica aprobada por personas.

[Transcriptos actuales completos: 12 bloques / 74 pasos](human-review-contextual-current.md). Revisión humana pendiente; no reemplazan el resultado negativo histórico de D01 ni aprueban las revisiones posteriores. T061 continúa con seis pérdidas históricas sin restauración/excepción, T067 con G1 humano pendiente; esas puertas no justificaban omitir las brechas técnicas que ahora se registran.

## Reproducir

PowerShell desde la raíz, dependencias/recursos locales previamente preparados. Elegir siempre una carpeta nueva para no sobrescribir primeras ejecuciones.

```powershell
$env:ORALIA_RELEVANCE_RUN = 'ruta/nueva'
$env:ORALIA_RELEVANCE_PARTITION = 'reserved'
uv run --offline --no-sync pytest tests/integration/test_contextual_relevance.py -q
```

Repetir esta reserva ya expuesta es regresión, no aceptación independiente nueva. Para desarrollo usar `development`. El comprobador nunca publica en una base habitual: exige TestClient y SQLite temporal propia.

Sucesora material reproducible, con destino nuevo:

```powershell
uv run --offline --no-sync python scripts/prepare_continuity_materials.py --mode contextual --parent materiales/docente/integracion-controlada-20261020-v7 --output ruta/sucesora-nueva
```

El archivo validation/report.md reúne validación final, comandos y límites; task-evidence-complete.md entrega la tabla íntegra. Se conservan todos los fallos y las fuentes/manifiestos anteriores.
