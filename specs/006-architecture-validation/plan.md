# Implementation Plan — Validación arquitectónica

Feature006, 2026-10-17. Sin Git/commits/agentes paralelos.

## Summary / Technical Context

Python3.12/uv/SQLAlchemy/Pydantic/psutil existentes. CLI local de mantenedor en
src/oralia/validation/{protocol,experiment,reporting,__main__}.py. Ninguna dependencia,
ruta API, tabla o migración nueva. Corpus sintético incorporado, base temporal por celda,
GenerationPort determinista directo como baseline y run_study_turn real como agencia.

## Research and integration

Reutilizar compositor, execute_agency, agentes/verificadores, T090, T150, apply_patch,
corrección de transcripción y eliminación005. Sustituciones scoped con unittest.mock.patch
solo dentro del proceso CLI experimental para puertos/fallos y ambas ablaciones; no
configuraciones de producción ni bypass. No ejecutar runner dentro de servidor/API.
Ranking lexical top1/top3 de corpus sintético y filtros de permiso existentes; no afirmar
que mide Chroma/LLM real. No utilizar helpers de tests desde código de aplicación.

## Constitution Check

PASS antes/después del diseño. I: sin notas. II: contratos existentes. III: estado
externo/versionado. IV: verificadores independientes/T090. V: corpus/versiones autorizados.
VI: protocolo manual y aislamiento. VII: solo sintético, sin audio, texto completo.
VIII: hashes/trazas/replay. IX: límites y degradación. X: comparación real y pruebas.
XI: monolito, sin dependencias nuevas. Ninguna excepción; la ablation no entrega a usuarios.

## Project Structure / Phases

protocol.py: catálogo17 y validación cerrada (reps1..5, máximo1000celdas, condiciones
allowlist). experiment.py: fixturesDB, puertos controlados, baseline/agencia, inyecciones
y medidas. reporting.py: métricas n/media/min/max/desviación, manifiestoSHA256, paquetes
y replay. __main__.py: run/replay, salida nueva y errores nozero.
Setup -> US1 comparación -> US2 ablaciones -> US3 fallos -> US4 replay -> US5 informe.
Pruebas antes de cada bloque; único escritor conforme autorización del usuario.

## Metrics / Limits

Cada métrica incluye valor/unidad/procedencia o motivo de ausencia. CPU de proceso,
latencia perf_counter y RSS antes/después (no pico); GPU/tokens ausentes sin monitor.
Contexto chars medido. Precisión/recall solo IDs etiquetados. Baseline no tiene coordinación
ni parches: declarar no comparable. Utilidad humana/tiempo docente ausentes sin inventar.
Paquete fijo protocol.json/results.json/report.md/manifest.json; lectura máximo10MB,
sin paths arbitrarios, salida debe ser nueva. Hash código ordenado por no tener Git;
replay compara solo secuencia/veredictos/fuentes/estado, excluye tiempos/UUID.

## Quality gates

CLI E2E, contrato/seguridad/fallos/métricas/replay, catálogo17 × seis condiciones
baseline/full/no_grounding/no_coherence/top1/presentation ×2 repeticiones. Indicar fallos
inaplicables/no comparables. Suite global, Black inventario, Ruff Counter baseline001,
lock offline, frontend build/lint/10Playwright. Voz real opcional. Evidencia y converge
antes de declarar MVP completo. Sin excepciones ni migraciones.

Los quince escenarios obligatorios se amplían con recursos y corrección STT (17).
Fuentes conflictivas usa anotación preparada MaterialConflictRecord; no se afirma
descubrimiento semántico automático. La puerta T090 se mide como componente de política,
no se cuenta como agente. Opiniones humanas permanecen faltantes; no se recopilan en esta
entrega ni se exige piloto humano para el cierre técnico.
