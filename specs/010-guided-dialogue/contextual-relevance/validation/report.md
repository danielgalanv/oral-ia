# Validación de las correcciones de pertinencia contextual —21-10-2026

La auditoría independiente v4/v7 invalidó la conclusión técnica anterior de 107/114. Se conservaron sus 100 capturas y el control v3 separado, se registraron seis hallazgos HIGH y siete tareas de construcción/validación T115–121, y se corrigieron casos reproducibles con pruebas de tema/proceso/propósito/objeto/estado. No se atribuyen 76 fallos independientes a un guion que diverge ni se presenta captura como aceptación.

## Resultados de la fuente actual

| Comprobación | Resultado medido |
|---|---|
| Desarrollo contextual nuevo |0/6 en rojo; 6/6 final |
| Dirigidas, permisos y controles |39 correctas en 55,15 s |
| Reserva contextual nueva |6/6 en primera ejecución, 27,08 s; 673 archivos congelados antes |
| Desarrollo natural anterior |6/6 como regresión, 34,66 s |
| Global |1260 passed, 944 skipped, 1 warning en 335,81 s |
| Frontend build/lint |ambos correctos |
| Black |152 archivos comprobados |
| Ruff estructural |baseline 49 / current 10 heredados / 0 nuevos, con multiplicidad por ruta/código/mensaje |
| Arquitectura |204 celdas / 0 errores; replay coincidente; protocolo/resultados estructurales coinciden con 006–009 y tres paquetes anteriores 010 |

La omisión global incluye corridas optativas ejecutadas por separado. La advertencia conocida es Starlette/httpx. Duraciones observadas no son una comparación de rendimiento ni estimación de carga inicial/fría. Las 204 celdas son evidencia arquitectónica determinista; no evalúan suficiencia didáctica humana, aprendizaje ni audio.

La primera corrida posterior al rojo encontró además un error del comprobador al leer CognitiveState tras cierre efímero, ya eliminado correctamente, y se conserva. Se corrigió el comprobador sin cambiar ese contrato. Un negativo unitario detectó una variante de procedimiento sin ancla contextual; su fallo también se conserva. No se ajustaron las expectativas reservadas después de ejecutarlas.

## Construcción verificada

| Hallazgo inicial | Corrección / evidencia |
|---|---|
| A01/7, evaporación sustituida por condensación |Deixis cerrada con ancla precede a semejanza; DEV-W exige unidades evaporacion, propósito process y excluye condensación/superficie fría. Variante reservada pasa con redacción distinta. |
| A02/6–7, decimal y referente |Reconocimiento de formato decimal y propósito de procedimiento; propuesta v8 ligada a suplemento explícito. Oráculo exige decimal-fact y decimal-process; variante 7,25. Tras fallo previo se pide aclaración en lugar de usar el número aprobado anterior. |
| A03/1, saludo pierde lectura |Saludo fijo más unidad docente con números literales de serie A; petición compuesta conserva ambas intenciones y fuente. |
| A03/3, división del alumno |Ancla media y observaciones disponibles seleccionan causal-count, sin afirmar una nota ni cálculo libre. |
| A03/12, orden tras afirmación |Prefacio finito más orden explícita crea propuesta; confirmación posterior cierra. Negación/cita/sí aislado no confirman y conservación sigue separada. |
| O01/5, apoyo no permitido |Trazas muestran tres repreguntas consumidas. Plantilla explícita de agotamiento en política v4/revisión 2, sin aumentar la escalera ni eximir repetición; pregunta original y evaluación not_assessed conservadas. |

Las respuestas orales sintéticas se eligen por la pregunta efectivamente emitida. Si no hay pregunta reconocible, el runner registra divergencia antes de inventar que el participante ha respondido a otra. Tres preguntas de seguimiento distintas y agotamiento se verifican en los tres dominios; no se divulgan unidades de solución o autoestudio. Permiso incompleto de saludo o agotamiento no habilita continuidad.

## Archivos y fuentes

[Lista de 25 rutas de fuente nuevas/modificadas](modified-files.md), respecto a la entrega verificada anterior de 658 archivos. Materiales v1–v7 y originales se conservan. v8 agrega dos unidades de decimal y su suplemento, propuesta pendiente de revisión humana. La publicación técnica solo ocurre en SQLite temporal propia, con testigos literales/UUID/versiones reales. Fuente congelada en source-contextual-before-reserve-20261021.json/ZIP; no se reescribe la fuente natural anterior.

[Transcriptos íntegros de 12 bloques / 74 pasos](../human-review-contextual-current.md), todos pendientes de revisión humana. El resultado negativo histórico de D01 no se borra ni se sustituye por «no evaluado». No se infiere G2 generativo, G3 utilidad o G4 voz.

## Comandos

PowerShell desde la raíz con recursos locales preparados. Cada salida debe ser nueva:

```powershell
$env:ORALIA_RELEVANCE_RUN = 'ruta/nueva'
$env:ORALIA_RELEVANCE_PARTITION = 'reserved'
uv run --offline --no-sync pytest tests/integration/test_contextual_relevance.py -q
```

Quitar esas variables para la suite global:

```powershell
uv run --offline --no-sync pytest -q --junitxml=.claude-scratch/feature010-relevance-global.xml
pnpm.cmd --dir apps/web run build
pnpm.cmd --dir apps/web run lint
pnpm.cmd --dir apps/web run test:e2e
uv run --offline --no-sync python -m oralia.validation run --output specs/010-guided-dialogue/evidence-contextual-20261021 --repetitions 2 --authorize-synthetic-ablations
uv run --offline --no-sync python -m oralia.validation replay --package specs/010-guided-dialogue/evidence-contextual-20261021
```

Los paquetes experimentales ya existen: usar una carpeta nueva para repetir. python-files.json delimita Black; ruff-comparison.json compara el baseline durable. Logs de primeras ejecuciones y posteriores completos en esta carpeta.

## Estado de cierre

Los fallos de pertinencia eran técnicos, no pendientes humanos; preimplementation-findings.json y Phase 10 conservan ese diagnóstico. La primera suite de navegador termina con 26 pases / 1 fallo en 4,7 min: no apareció confirmación de borrado. El contexto se conserva en browser-first-failure. La captura no prueba su causa; el test no esperaba habilitación del botón ni respuesta DELETE antes de verificar el texto. Se añade esa sincronización y assert HTTP 200 real, sin ampliar plazos ni modificar la aplicación. post-reserve-source-diff.json acredita que solo cambia ese archivo E2E, sin cambios de producción/Python/corpus. La reserva semántica permanece sobre la misma producción y no se presenta la repetición como reserva nueva. La suite final y la preservación se registrarán al terminar. T061 CRITICAL conserva seis pérdidas históricas sin restauración ni excepción; T067 HIGH exige revisión humana de G1. Ningún pase de estas correcciones cumple esas puertas. No commits, Reset, descargas ni manipulación de procesos o datos habituales.


Segundo intento: la aplicación confirmó el borrado, pero el nuevo observador de la prueba esperaba erróneamente `/governance/sessions/{id}/content`; la ruta real es `/api/v1/sessions/{id}/content`. Este fallo del comprobador se conserva en browser-second-failure y su log interrumpido; se corrigió solo la prueba. La interrupción fue del runner propio y dejó sus puertos libres; no se señalaron procesos ajenos. post-reserve-source-diff-v2.json acredita que producción, Python y corpus permanecen idénticos a la primera reserva. La tercera suite completa usa source-contextual-browser2-20261021.json/ZIP.


Tercer intento: borrado y respuesta DELETE correctos, pero faltó la transición a acceso docente cerrado. El botón de logout también depende de busy y el test no esperaba su habilitación. Se conserva el contexto y el log interrumpido, y se añade la espera de habilitación más HTTP 200 de logout real. No se modificaron producción, plazos, permisos o el corpus. Se ejecuta primero la prueba de gobierno dirigida; su pase no sustituirá la suite completa.


El comando que pretendía filtrar gobierno (`pnpm.cmd --dir apps/web run test:e2e -- test_governance_flow.spec.ts`) ejecutó 27 pruebas según su salida. Se registra como suite completa, no como prueba dirigida. El archivo de log conserva su nombre original feature010-relevance-browser-governance-targeted.log para trazabilidad. El recorrido de gobierno pasa con las verificaciones de borrado/logout en 2,7 s; falta terminar el resto de la suite. La fuente final candidata es source-contextual-browser3-20261021.json/ZIP y post-reserve-source-diff-final.json muestra solo el cambio de sincronización en E2E.


Cuarto intento: gobierno pasa con borrado/logout reales; el escenario básico busca la burbuja a los 5 segundos mientras sigue pendiente el envío. Se conserva el contexto y log interrumpido. El comprobador espera ahora HTTP 200 de turno/cierre/listado y verifica la salida real, además de limpiar solo su sesión temporal ante fallo. No cambia la aplicación ni sus plazos. Ambas pruebas dirigidas pasan 2/2 en 57,3 s con arranque. La suite completa final usa source-contextual-browser4-20261021.json/ZIP; el diff final2 contiene exclusivamente dos archivos E2E, sin cambios de producción/Python/corpus posteriores a la reserva.


## Resultado completo final

**27/27 Playwright en 4,3 min**, con guardia de 229 archivos / 0 cambios históricos nuevos. Preservación final y puertos en preservation-final.json y ports-final.json: datos habituales sin cambios, demo de trabajo preparada/detenida, servicios propios 8005/8015/5175 detenidos y procesos habituales 8010 (PID 51816) / 5180 (PID 68296) conservados. 673 fuentes verificadas en source-contextual-verified-20261021.json/ZIP.

**114/121 tareas completadas.** Se entregan la tabla completa, los seis hallazgos de construcción iniciales y sus pruebas/correcciones acotadas. Los primeros fallos y errores de comprobadores no se eliminan. Esto no acredita que los 100 turnos de guiones fijos o todas las conversaciones naturales sean satisfactorios; el reconocedor sigue siendo finito. Revisión humana de G1 pendiente y pérdida T061 sin restauración/excepción.


[Tabla completa de121tareas](../task-evidence-complete.md), [hallazgos/análisis final](../analysis-convergence-current.md), [auditoría JSON](../postimplementation-audit.json). El inventario actual se guarda en artifact-inventory-contextual-current.json; los inventarios y paquetes anteriores se conservan como instantáneas, sin editar sus hashes.
