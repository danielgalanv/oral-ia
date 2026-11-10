# Analyze y converge — tablas nativas,20-10-2026

Estado: **no converged**;88/95tareas completadas. Se revisan43FR,12SC,33escenarios,13decisiones A–M,11principios y58elementos de checklist completos. Analyze no detecta contradicciones críticas entre artefactos de intención. Converge no detecta una brecha nueva de construcción en la corrección tabular; las tareas existentes siguen cubriendo las puertas pendientes.

| Hallazgo vigente | Tipo | Severidad | Fuente | Evidencia pendiente |
|---|---|---|---|---|
| T061 | contradicts | CRITICAL | FR027/028/032; Constitución VIII/X | Seis archivos históricos aún no coinciden con baseline inicial; sin copia/restauración o excepción aprobada. |
| T067 | partial | HIGH | plan G1; FR016/030/041 | D01 anterior requiere corrección según revisión humana; sucesor y otros23 esperan revisión. La comprobación de extracción no los aprueba. |

T053/T054/T055/T056/T065 permanecen abiertos por esas dependencias. No se duplican las tareas ni se reinterpretan pérdidas como restauración ni se declara converged por totales de pruebas. El plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema»; esta fase no sustituye ese requisito.

## Correspondencia con intención y contratos

FR042/T091–093: DOCX/PPTX incorporan tablas nativas, orden documental/fila/columna, coordenadas de origen y literalidad007/1000/3,5. DOCX conserva párrafos anteriores, combinadas/anidado≤4 y error explícito sin indexación parcial. PPTX conserva texto/diapositiva, recorre grupos y omite celdas spanned. Contexto estructural≤160por referencia sin truncar la celda principal ni declarar cabeceras semánticas.

FR043/T093–095: notas de presentador excluidas, notas-only no procesable, exclusiones documentadas y processed distinto de aprobación/cobertura visual total. Versiones anteriores no se reprocesan; incorporación mediante sucesora/activación explícita. API y metadatos de fuente siguen iguales; no DDL, dependencia o agente nuevo. Relación con002/FR002/006–008/010–011 y010/FR015–020/032/041 registrada sin reescribir artefactos previos.

SC012/T094–095:17regresiones pertinentes, incluidos cuatro entregables ficticios externos por copiasSHA; casos normales/merges/anidado/grupos/notas/límite y ciclo API con DB/índice/embeddings reales aislados. Curso/actividad/activación/versiones/retiro y UUID/ubicación/texto se comparan con registros reales. No se publica el paquete docente externo ni se importan sus210propuestas/guías/oráculos ni se ejecutan sus60casos/conversaciones del tercer dominio. No se usan UUID ficticios para afirmar procedencia.

## Evidencia final

- table-extraction-validation/report.md y summary.json:1198Python/935omitidas/1aviso,27Playwright,17pertinentes, build/lint, Black134rutas, Ruff10heredadas/0nuevas por Counter(ruta,código,mensaje) con multiplicidad.
- table-extraction-comparison.json: Word programa77→101bloques con24celdas; PPTX13→37con24celdas en diapositiva12; Word agua74párrafos sin tabla yPDF7páginas sin cambios. Textos/ubicaciones anteriores preservados, archivos originalesSHAiguales. OOXML no equivale a validación visual nativa.
- source-tables-verified-20261020.json/zip:593archivos estables durante validación. tables-modified-files.json detalla13cambios de fuente/fixtures, incluidas cuatro copias inmutables; no modifica los entregables originales de la otra auditoría.
- evidence-tables-20261020:204celdas/0errores y replay coincide. tables-experiment-comparison.json mantiene protocolo/resultados estructurales de006–009 y anterior010; paquetes originales intactos.
- table-extraction-preservation.json y guard:229archivos históricos/0cambios nuevos,223SHAiniciales coinciden y6pérdidas anteriores explícitas. SHAoralia.db/demo.db/fixtures.json intactos. Puertos propios8026/5196/8005/8015/5175 libres; procesos ajenos no tocados; perfil demo propio conservado, sin Reset ni commits.

## Límites y puertas

La extracción no aprueba suficiencia docente, cobertura visual completa o fuentes de soluciones ocultas; las notas no se leen y el cuerpo exige revisión/activación. La publicación de unidades del paquete externo sigue requiriendo su propia revisión de fuentes, UUID, sucesoras y conversaciones por formato/dominio. No hay validación de audio real, G3 o G2 generativo nuevo. Los primeros fallos se conservan: siete omisiones rojas y dos supuestos erróneos de pruebas corregidos sin alterar material.

El análisis/convergencia se realizó en solo lectura sobre spec/plan/tasks, con hashes antes/después. Este informe se registra después en implementación/evidencia; no modifica la intención ni añade excepciones ni atribuye aprobación humana.
