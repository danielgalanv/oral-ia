# Implementation Plan: 011 — Autoestudio real de Ingeniería del Software

**Date**:2026-10-21 | **Spec**:[spec.md](spec.md) | Sin rama ni commits: workspace no Git.

## Summary

Diagnosticar primero la reformulación extractiva y el enlace de autorización. Habilitar experiencia extractiva limitada con semántica propia del material, sin rellenar la puerta guiada. Preparación selecciona páginas10–12 del PDF original, conserva procedencia y excluye incidencias13–14; añade Testing9 solo si se estudia la distinción de pruebas/validación. Terminal local opera mediante la API ASGI real y autenticación existente, con almacenamiento propio, sin abrir servicios de red ni modificar demo.

## Technical Context

Python3.12/FastAPI/SQLAlchemy/SQLite/Chroma/pypdfium2; runtime y embeddings ya locales, offline. CLI PowerShell/Python sin modelos nuevos. Pytest, build/lint/PW global si cambia código compartido; Black/Ruff estructural durable y204/replay si cambia manifiesto. Escala: un usuario/sesión, dos documentos seleccionados como máximo, treinta turnos/900s; presupuestos existentes sin ampliación. Respuesta determinista extractiva, no tutor generativo ni comprensión/voz acreditadas.

## Constitution Check

I no notas/autoridad ni datos de alumnos;II sin agentes nuevos y contratos explícitos;III estado/API persistidos;IV verificación independiente;V T090/T150 y autorización intactos;VI consentimientos/retención y acceso normal;VII vía textual, voz pendiente;VIII primeros fallos, hashes, offsets y procedencia;IX límites/cancelación/operación única;X pruebas negativas y global;XI cambios acotados/reutilizar servicios. Las pérdidas T061 y revisión T067 de010 permanecen abiertas y referenciadas, no se resuelven por crear011. Revisión docente de contenido derivado permanece pendiente. Diseño no viola gates: no elimina ni reduce la puerta guiada.

## Decisions

A: seleccionar un formato PDF por documento y crear un extracto de páginas como derivación explícita, sin editar original. Cita del extracto incluye tabla de correspondencia original; no fingir que página local1 es original1. No datos de contacto ni evaluación.
B: reproducir con wrappers de observación que delegan resultados/excepciones sin cambiarlos; separar fallo de configuración del candidato sin enlace. La causa se documentará tras captura, no a partir de invalid_context aislado.
C: perfil extractivo existente primero; si la selección/reformulación exige nueva proyección, versionarla optativamente y reconstruir solo segmentos literales desde fragmentos vigentes. No autorizar supported_claims como fuente confiable ni introducir bypass de grounding. V1 permanece intacta.
D: no reutilizar continuity.py ni topic validacion de cantidades; contenidos propios validacion_requisitos/calidad_requisitos se identifican por fuente y objetivo del curso. La terminal no interpreta confirmaciones naturales como permisos.
E: API local en proceso con cookies/autenticación normales, secreto aleatorio efímero oculto y recursos dedicados .oralia-course-study. Solo un proceso mediante lock. No usar acceso especial de demo ni fixtures de tests para la entrada del usuario. No borrar: cancelar/cerrar solo sesión propia. Operación persistente repetible/idempotente por hashes/perfil, sin duplicar cursos cada arranque.

## Project Structure

src/oralia/application/orchestration/self_study_agency_composer.py — enlace de candidato, solo si causa demostrada.
src/oralia/domain/materials/ — proyección versionada si necesaria.
src/oralia/infrastructure/generation/ y domain/agents/response_generator_agent.py — selección extractiva optativa si necesaria, verificadores intactos.
src/oralia/course_study/ — preparación/API/terminal aislada, sin servicios nuevos de arquitectura.
scripts/course-study.ps1 — entrada local.
tests/integration/test_real_course_self_study.py y tests/unit/ — diagnóstico, transferencia, contratos, privacidad.
specs/011-real-course-self-study/evidence/ — primera ejecución, reservas, transcriptos, preservación y análisis.

## Phases

Diagnóstico → contrato/proyección mínima → fuentes/preparación → conversación completa y variante congelada → entrada operativa → regresiones y entrega. No paralelizar mutaciones del entorno; investigación delegada de solo lectura conforme a speckit-plan. No subagentes de producto.
