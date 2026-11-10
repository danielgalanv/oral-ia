# Plan de actuación ORALIA — después de las pruebas reales

**Objetivo:** que una persona pueda estudiar material docente autorizado y ensayar su explicación con una conversación que mantiene el tema, ofrece apoyo pertinente y permite recuperarse sin ayuda técnica. ORALIA no evalúa ni pone notas.

## Qué enseñaron las pruebas

Las pruebas anteriores acreditaban una parte importante de infraestructura y seguridad, pero no bastaron para acreditar la conversación. Autoestudio perdió el referente de «dímelo» y entró en avisos repetidos. Defensa interpretó peticiones de ayuda/repetición como contenido temático y dejó de formular un siguiente paso útil. La demostración de dos frases y un generador extractivo no puede sostener todas las explicaciones anunciadas.

También hubo fricción de arranque, identificación, sesión ocupada, modalidad textual y localización de fuentes. Algunas reparaciones ya existen: este plan las trata como regresiones que deben mantenerse, no como fallos nuevos todos pendientes. Evidencia y diagnóstico en research.md y docs/HALLAZGOS-PRUEBA-USUARIO.md.

## Orden propuesto

| Bloque | Resultado que debe poder comprobarse | Tareas |
|---|---|---|
| 1. Evidencia y fundamentos | reproducir fallos, contratos y contexto seguros, corpus reservado congelado | T001–T013 |
| 2. Autoestudio | saludo, tema, referentes, cinco modos, repetir/reformular y salida de bucles | T014–T019 |
| 3. Defensa | pregunta persistente, pistas permitidas, repreguntas pertinentes y discrepancias neutrales | T020–T024 |
| 4. Contenido y generación | dos dominios desarrollados, fuentes y transformaciones autorizadas, capacidades honestas | T025–T034 |
| 5. Uso autónomo | entrada válida, recuperación de sesión, texto accesible e idempotencia | T035–T042 |
| 6. Aceptación y cierre | privacidad, corpus completo, navegador real, migraciones y evidencia por capacidad | T043–T056 |

No basta añadir palabras clave ni conectar un LLM al verificador extractivo actual. Primero se ofrece diálogo guiado mediante contenido docente revisado y decisiones verificables. En paralelo lógico se estudia generación local real; no se habilita texto libre si su autorización no puede verificarse suficientemente. No se promete que este enfoque limitado sustituya toda explicación abierta.

## Qué significa terminar

33 requisitos funcionales y 9 criterios medibles están trazados a **60 tareas originales, ampliadas por converge**. G0 técnico y G1 de diálogo son obligatorios: secuencias históricas y variantes, 24 conversaciones, 48 entradas reservadas, dos dominios, ambos modos, permisos y privacidad sin excepciones. G2 habilita generación abierta solo si se acredita; una conclusión negativa del estudio no acredita esa capacidad. G3 es utilidad con personas, todavía pendiente de un piloto consentido.

Antes de otra demostración, deben pasar los casos que fallaron con el proveedor efectivo y sin sustituir respuestas del sistema. Un total grande de pruebas no compensa fallar una acción esencial. Se publicarán casos fallidos y límites, además de los aprobados.

## Conversaciones sintéticas de herramientas

Además de los 24 diálogos, se añaden 16 escenarios sintéticos para comprobar búsqueda/fuentes, explicación, memoria/modos, defensa/pistas, recuperación de sesión, revisión/exportación, borrado y fallos/reintentos. Verifican operaciones, permisos, argumentos, efectos y lo que se comunica al usuario, con herramientas reales y datos aislados. Ocho casos quedan reservados. T057–T060 son obligatorias antes del cierre; protocolo en [synthetic-tool-conversations.md](synthetic-tool-conversations.md).

## Después de este alcance

Priorizar piloto docente y revisión de carga de autoría; después decidir generación local más flexible y voz real según evidencia y recursos. No incorporar nube, SSO, evaluación del participante o concurrencia múltiple como arreglos de esta feature.

Artefactos: spec.md (alcance), plan.md (arquitectura), tasks.md (ejecución), acceptance-matrix.md (aceptación), risk-register.md (complicaciones), requirement-coverage.md (trazabilidad) y quickstart.md (operación del plan). Estado: implementación parcial; progreso y brechas en tasks.md y task-evidence.md.

