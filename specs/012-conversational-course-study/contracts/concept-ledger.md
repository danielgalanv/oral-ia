# Contrato de registro conceptual de laboratorio

Versiones `concept-ledger/v1`–`v4` y `concept-labels/v1`, 04-11-2026. No habilitan participantes ni modifican el contrato V1 del tutor.

1. Entradas: pregunta, historial realmente mostrado y evidencia autorizada, versionada y revalidable. Cada tarjeta conserva texto completo de unidad, posiciones y hash del texto de evidencia; el hash del PDF original se comprueba separadamente por el llamador.
2. Planificador de catálogo: ve pregunta, fuentes e historial, sin borrador. Selecciona referencias existentes y puede proponer traducciones tentativas; no declara verdad ni autorización docente.
3. Revisor de usos: recibe respuesta íntegra, fuentes originales, historial y unidades asignadas. Emite referencia, juicio y motivo por cada unidad, sin omisiones ni referencias ajenas. En v4 se permiten lotes más pequeños si falla cobertura; una sola unidad recibe dictamen sin ID generado, vinculado por el host a la única entrada. No se infiere verdad de esta vinculación.
4. Revisor de nombres: recibe nombres usados y definiciones originales enlazadas, más fuentes completas. No recibe descripción del candidato ni historial. Decide equivalencia, diferencia, incertidumbre o encabezado organizativo. Admite paráfrasis, traducciones y variación gramatical. Es modelo falible; compartir checkpoint con generación no acredita independencia semántica.
5. Estado derivado: referencias/cobertura inválidas o salida incompleta son fallos técnicos; no aciertos ni errores semánticos del candidato. Se conserva el juicio nativo y el de nombres por separado. Un juicio incorrecto genera incidencia referenciada; reparación y revisión posterior conservan todas las versiones. Ficción coherente y números ilustrativos no son por sí solos errores.
6. Límites: presupuesto de llamadas del llamador, formato con un reintento acotado, 7.000 tokens de entrada sin recorte, 180 s/etapa y 600 s/caso en el ensayo. Revocación/cancelación se comprueban en el adaptador antes/después de inferir. No hay publicación, calificación, rúbrica ni consumo de reserva.
7. La extracción de viñetas no garantiza catálogo exhaustivo y el control de encabezados no cubre automáticamente cada palabra clave. Deben medirse falsas críticas, omisiones y coste, sin promover por formato o acuerdo de modelos.

[Ensayos completos y fallos conservados](../../../docs/audits/2026-11-04-explicit-concept-ledger/report.md).


## Material preparado — 05-11-2026

`prepared-concepts/v1` conserva documentos inmutables por hash y un manifiesto derivado actualizado atómicamente. Guarda evidencia, unidades literales, posiciones, nombres originales, documento/página y propuestas opcionales de denominación, nunca respuestas al alumno. Los nombres detectados por formato son candidatos, no definiciones semánticamente aprobadas; se conserva también todo el contexto disponible.

La preparación docente genera el catálogo e incorpora sus archivos al recibo `oralia-study-preparation/v2`. La revisión conceptual optativa admite `prepared=...`: enlaza solo la evidencia recuperada exacta, revalida autorización, archivo original, versión y texto y evita la planificación LLM del catálogo. El vínculo del turno se calcula de nuevo para pregunta e historial; no se reutilizan respuestas ni veredictos. La revisión de uso y de ejemplos sigue siendo necesaria. El manifiesto previo se conserva si hay retirada antes de confirmar una actualización.
