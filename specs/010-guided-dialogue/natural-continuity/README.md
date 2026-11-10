# Continuidad natural — Feature010, 21-10-2026

Política `guided-screenless/v4` optativa y sucesora material v7. La demo habitual no se activa ni modifica. Este bloque corrige los primeros desvíos del auditor mediante propósito/cláusula/contexto, referentes autorizados, seguimiento acotado de la pregunta emitida y confirmación de una operación vigente. Conserva verificadores, T090/T150, fuentes, consentimiento y políticas v1–v3.

## Evidencia y alcance

- [Recepción de auditoría](audit-receipt.json): 76 peticiones y 24 contrastes originales íntegros. HTTP200/captura no es aceptación; la divergencia de un guion que responde a preguntas no emitidas no cuenta como fallos independientes.
- [Congelación inicial](corpus-freeze.json), [segunda reserva](reserve-second-freeze.json), [tercera reserva](reserve-third-freeze.json). Son casos sintéticos congelados antes de sus ajustes; no se atribuye autoría humana independiente. El runner decide la respuesta por la pregunta real y registra divergencia antes de continuar.
- Desarrollo v3: 0/6. Primeras incidencias v4 y sus logs se conservan, incluido NameError, conflicto T090 con una frase docente y falta de alternativas. No se cambió el control T090 para hacerla pasar.
- Primera reserva v4: **3/6**; después de exponer/corregir se trata como regresión. Segunda reserva: **6/6** en su primera ejecución, versión histórica de642 archivos. Las brechas posteriores de los prefijos auditados impiden usar ese pase como aceptación de la versión actual.
- Prefijos auditados: **0/3** en rojo con contexto correcto; **3/3** tras corrección de unidades/propósito. La primera prueba roja sin contexto se conserva como defecto del protocolo, sin atribuirlo al producto.
- Versión actual: desarrollo6/6 y controles/autorización/unidades **29 pruebas,53,81 s**; tercera reserva nueva **6/6,32,57 s** en primera ejecución. [658 archivos congelados antes de ejecutarla](../source-natural-before-reserve3-20261021.json), ZIP homónimo. Los cambios de documentación no modifican esos archivos.

## Materiales

v1–v6 y paquete original preservados. v7 contiene101 unidades de agua, 103 de programa y 102 de datos: 306 únicas/409 instancias al preparar los cuatro formatos. v4/v5 no se borran ni se presentan como versiones aceptadas. v7 añade hecho molecular literal de la fuente primaria y definición funcional de validación en suplemento explícito. Son propuestas pendientes de revisión humana, incluidas sus preguntas/pistas. Publicación técnica en BD temporal no certifica suficiencia didáctica. El guion y los oráculos nunca se ingieren.

La variante molecular usa una unidad específica después de la causa; el control de repetición continúa activo. Las alternativas solo seleccionan relaciones publicadas y terminan con límite explícito. La aclaración «La media» necesita una aclaración pendiente y un tema publicado. Una confirmación natural solo puede operar sobre la propuesta vigente; no concede conservación positiva, no reutiliza una propuesta caducada ni combina revocación y cierre.

## Revisión

[Transcriptos actuales íntegros:15 bloques/98 pasos](human-review-natural-current.md), con fuentes/veredictos/contexto/estado y respuesta a pregunta emitida. Todos pendientes. La evaluación negativa histórica de D01 se conserva y no se sustituye por «no evaluado». El paquete humano anterior mantiene sus24 bloques y su propio estado.

T061 sigue CRITICAL: seis pérdidas históricas sin restauración ni excepción. T067 sigue HIGH: G1 humano pendiente. Las tareas dependientes permanecen abiertas. Las pruebas sintéticas no validan utilidad humana, conversación general ni voz real. El planificador finito puede pedir aclaración o alcanzar un límite; no es un modelo nuevo.

## Reproducción

Recursos/dependencias preparados localmente; ejecutar en PowerShell desde la raíz. Usar una carpeta nueva en cada ejecución para preservar resultados anteriores.

```powershell
$env:ORALIA_NATURAL_RUN = 'ruta/nueva'
$env:ORALIA_NATURAL_POLICY = '4'
$env:ORALIA_NATURAL_PARTITION = 'reserved_third'
$env:ORALIA_NATURAL_CORPUS = 'tests/dialogue/fixtures/natural-continuity-v3.json'
$env:ORALIA_NATURAL_ORACLES = 'tests/dialogue/fixtures/natural-continuity-oracles-v3.json'
uv run --offline --no-sync pytest tests/integration/test_natural_continuity.py -q
```

Esto repite una reserva ya expuesta; no crea una nueva reserva. Para desarrollo, quitar las variables CORPUS/ORACLES y seleccionar development. Los controles negativos están en test_continuity_pending_controls.py. Los prefijos usan ORALIA_NATURAL_PREFIXES con carpeta nueva y test_natural_audit_prefixes.py. No ejecutar estas operaciones sobre bases habituales: la preparación exige TestClient y BD temporal propia.

Sucesora reproducible, siempre en destino nuevo:

```powershell
uv run --offline --no-sync python scripts/prepare_continuity_materials.py --mode atoms --parent materiales/docente/integracion-controlada-20261020-v6 --output ruta/sucesora-nueva
```

Validación global/frontend/experimento y preservación final se registran en validation/report.md y validation/summary.json. Se conservan los intentos fallidos del navegador: el primer recorrido completo fue interrumpido tras una carrera de transporte en la prueba; el pase dirigido posterior2/2 no sustituye la suite completa. La prueba espera ahora el commit/abort real antes de comprobar estado incierto y limpia solo su propia sesión.
