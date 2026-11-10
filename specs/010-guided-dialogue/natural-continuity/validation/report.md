# Validación de continuidad natural —21-10-2026

Implementación técnica v4 en Feature010, con materiales sucesores v7 y API/compositor/verificadores reales. No activada en datos habituales. Los límites del planificador finito, la propuesta docente pendiente y los primeros fallos permanecen visibles.

| Comprobación | Resultado medido |
|---|---|
| Desarrollo + controles negativos + contratos + unidades |29 pruebas,53,81 s; desarrollo6/6 |
| Prefijos auditados con contexto real |rojo0/3 conservado; verde3/3;13 pruebas en54,15 s junto a unidades antes de añadir un caso unitario más |
| Tercera reserva nueva, primera ejecución |6/6,32,57 s; fuente658 congelada antes |
| Primera reserva expuesta, regresión actual |6/6,32,49 s; primer resultado3/6 preservado |
| Global |1250 passed, 943 skipped, 1 warning, 303,47 s |
| Frontend build/lint |ambos correctos; build TypeScript y Vite |
| Black |151 archivos sin cambios pendientes |
| Ruff estructural |baseline 49 / current 10 heredados / 0 nuevos; Counter(ruta,código,mensaje), multiplicidad |
| Arquitectura sintética |204 celdas,0 errores; replay coincidente |
| Comparación de paquetes |protocolo/resultados estructurales iguales a006–009,010tablas e integración anterior |

La suite global omite corridas optativas que se ejecutaron por separado con sus variables y salidas nuevas. La advertencia es la deprecación de Starlette/httpx ya registrada; no es un fallo oculto. El experimento de 204 celdas es regresión arquitectónica determinista, no medida de calidad didáctica, aprendizaje, rendimiento mejorado o voz real.

Los logs primeros y posteriores se conservan en esta carpeta con sus nombres originales. README y corpus-freeze registran cada versión/reserva; una reserva ejecutada se convierte en regresión expuesta. La segunda reserva6/6 pertenece a642 archivos anteriores; las brechas semánticas auditadas posteriores requirieron una tercera, sin renombrar el resultado anterior como aceptación actual.

## Navegador

La primera suite fue interrumpida después de9 pases y 3 fallos en cascada. El primer caso de transporte aún esperaba el commit de route.fetch cuando el assert de interfaz agotó su espera; la sesión quedó activa y afectó casos posteriores. Los tres contextos de error están en browser-failure-first. El pase dirigido2/2 posterior sobre aquella versión no sustituye la suite completa. La prueba actual sincroniza con commit/abort reales y libera solo la sesión propia en finally; no fabrica respuestas ni modifica el plazo de aplicación. La suite completa actual pasa: **27/27 en 3,5 min**. La guardia compara 229 archivos históricos antes/después y detecta 0 cambios.

## Preservación y revisión

preservation-before-browser.json verifica658 fuentes estables,229 entradas históricas/0 cambios nuevos y6 pérdidas previas; SHA de datos habituales sin cambio, perfiles preparados conservados. original-receipts-verified.json verifica21 archivos docentes originales y22 archivos del auditor sin discrepancias. Manifiestos v1–v7 válidos. Las copias históricas no se han reescrito ni se han alterado hashes para aparentar coincidencia.

human-review-summary.json y [paquete íntegro de15 bloques/98 pasos](../human-review-natural-current.md) conservan salidas, fuentes, estados, verificación y pregunta realmente emitida. Revisión humana pendiente; D01 histórico negativo no se limpia. T061 CRITICAL y T067 HIGH impiden cierre, con cinco tareas dependientes abiertas. No G2 generativo, G3 utilidad ni G4 voz aprobados por estos pases.

## Comandos

Desde la raíz, recursos locales previamente preparados:

```powershell
uv run --offline --no-sync pytest -q --junitxml=.claude-scratch/feature010-natural-v7-global.xml
pnpm.cmd --dir apps/web run build
pnpm.cmd --dir apps/web run lint
pnpm.cmd --dir apps/web run test:e2e
uv run --offline --no-sync python -m oralia.validation run --output specs/010-guided-dialogue/evidence-natural-20261021 --repetitions 2 --authorize-synthetic-ablations
uv run --offline --no-sync python -m oralia.validation replay --package specs/010-guided-dialogue/evidence-natural-20261021
```

Los últimos comandos ya están ejecutados: para repetir, elegir una carpeta de experimento nueva. Los comandos adaptativos y sus variables están en README; python-files.json delimita Black. feature010-natural-v7-ruff-comparison.json documenta la comparación durable. No commits, Reset, descargas ni señales a procesos ajenos.


Preservación final: preservation-final.json y ports-final.json. Demo de trabajo en 8026/5196 y procesos E2E en 8005/8015/5175 detenidos; procesos habituales en 8010 (PID 51816) y 5180 (PID 68296) conservados. Fuente final de 658 archivos estable en source-natural-verified-20261021.json/ZIP.


Estado final: **107/114 tareas completadas**. [Tabla completa](../task-evidence-complete.md), [archivos de fuente modificados](modified-files.md), [análisis/convergencia](../analysis-convergence-current.md). No converged por las puertas existentes; no nuevas brechas de construcción sin cubrir. El inventario artifact-inventory-natural-current.json enumera los artefactos y sus hashes actuales.
