# Implementation Plan009

## Summary / Technical Context

Python3.12, SQLAlchemy/Chroma/embeddings existentes, React/Playwright. Sin dependencias,
agentes, cambios T090/T150, políticas/plantillas ni esquema/migraciones. Autorización
humana verificada en chat auditor (idle) antes de editar; escritor único. Caso rojo real
HTTP archivo04 íntegro reproducido antes de corregir:2fallos autoestudio con/sin retención.

## Design / Structure

Nuevo domain/materials/extractive_excerpt.py: proyección pura cerrada material-excerpt/v1,
mismo strip/400/último espacio/elipsis de _snippet existente. Devuelve texto y rango
start/end de caracteres Python en fuente original; sha256 UTF8 fuente. Sin parámetros de
recorte controlados por generador. Adapter _snippet delega a helper, conducta idéntica.

self_study_agency_composer._decide_study_output admite coincidencia exacta con texto
completo (compatibilidad) o proyección v1 de1–3fragmentos. Matching no otorga autoridad:
validar fila vigente/curso/asignación/id/doc/version/ubicación/texto completo,scope y
recipient/disclosure igual que antes. Solo después construir valor desde fila DB y helper,
no desde texto propuesto. data_ref vincula perfil,hash,rango; builder reconstruye plantilla
inmutable y verificador T090 comprueba segmentos/hashes sin modificarse. Proyección es un
valor confiable de aplicación, no texto libre de modelo ni campo extra del contrato.

Solo si propuesta final autorizada coincide con propuesta de material proyectado registrar
TraceEvent material_excerpt_bound: schema1,perfil/version,fragment/doc/version/ubicación,
source_sha256/start/end/value_sha256; sin texto nuevo ni input de participante. Inspección técnica interna, mientras la conservación lo permite, puede relacionar
traza con material vigente y reconstruir la proyección determinista. T150 y
consentimiento siguen controlando contenido; datos derivados de fuente no de participante.
Fallback y límites3fragmentos/400caracteres por proyección sin cambios.

## Phases / Tests

Baseline/snapshot→reproducción HTTP→helper/matriz y frontera negativa→integración→navegador
con carga archivo04 por Área técnica autorizada y publicación en Gobierno→gates. Ampliar
prueba teacher_material_pack ambos archivos/modos y scopes [],transcript,summary,ambos;
verificar segundo turno autoestudio, revisión parcial,exportación/borrado. Matriz directa
_decide con DB real para399/400/401/múltiples/Unicode; dependencias sin mocks de autoridad.
Negativos alteración,recorte arbitrario,scope/provenance/doc/version/location mismatches,
curso/actividad ajenos,retirado; nulo/fallbackmáximo1. Los tests de cierre T150 existentes
se ejecutan globalmente. Playwright carga archivo04 original e indexa real en DB temporal.
No modificar frontend salvo prueba. check-demo y regresiones aisladas, nunca Reset real.

## Constitution Check

I apoyo sin notas; II contratos exactos existentes; III estado externo sin cambio;
IV decisión/verificación separada/T090; V fuente vigente y proyección trazable; VI
política docente sin modificación; VII scopes/saneamiento/aislamiento; VIII metadata
reproducible y paquetes preservados; IX límites400/3/fallback; X matrices/caso real/browser;
XI helper puro, sin agentes/deps. PASS previo/postdiseño. Snapshot006/007/008 y paquete009
actual tras freeze/run/replay204. Black/Ruff baseline001 Counter multiplicidad;global,
build/lint/Playwright/check-demo. Cierre analyze/converge y resultados sin universalizar.

## Corrección adicional demostrada

El archivo04 TXT se extrae por líneas,con fragmentos menores400. La traza real muestra
falsa contradicción por negación agregada en una fuente con frases distintas. T012
refina _detect_contradiction a pares de oraciones (puntuación/newline),sin quitar
verificador ni eximir extractivas; conservar umbral léxico2 y polaridad,comprobar
contradicción real con otras fuentes y afirmaciones previas. Probar además documento
sintético de bloque largo por HTTP real,para aislar recorte400 del fallo de negación.

T013 añade únicamente processed a estados con botón Activar en Tecnica.tsx,para completar
carga/publicación real por UI;backend/contrato ya lo permiten. Sin rediseño.

T014 alinea época del índice E2E con su DB recién creada: ruta nueva por ejecución
en scratch,no borrar directorios previos ni modificar recuperador/umbrales de producción.
Validar suite completa con caso04/aserción100,registrar fallo anterior sin ocultarlo.

La proyección cerrada technical_payload de T150 no cambia: revisión/exportación no
amplían su lista blanca para el nuevo payload;metadatos detallados de binding se
conservan internamente solo mientras el scope aplicable lo permite. Las fuentes
versionadas de revisión siguen el contrato previo. Privacidad prevalece sobre replay
del contenido no consentido o eliminado.

T015 añade teardown de clientes Chroma reales solo bajo tmp_path resuelto de la prueba,
usando close() público,orden inverso,sin clear_system_cache ni detener rutas ajenas.
No modifica consultas/asserts ni producción. El error en suite grande se conserva
y se repite batería real/global con recursos liberados entre casos.
