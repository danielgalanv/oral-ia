# Datos012

Candidate v1: segments(kind,text,source_refs,source_quote,assumptions), context(topic,objective,pending_question,strategy), actual_input/output. Solo propuesta, no OutputProposalT090 ni TrustedDataReference.
SourcePage: id,original_filename,original_sha256,version,page,text,text_sha256; derivación extraída, sin marcar aprobación docente.
LabState: lista acotada de entradas/salidas reales y contexto propuesto, identificador propio. Nunca se sincroniza estado de sesión productiva desde candidata no autorizada.
GateReport: structure/source_checks,independent_semantics,pedagogy_oracles,publication_allowed=False hasta prueba completa; G2/G3/G4 explícitos.
Sin tablas productivas nuevas inicialmente. Enlace participante/versiones posteriores dependen de prueba semántica suficiente y política explícita.

Presentación documental (FR-019, 27-10-2026): `source_presentation` registra documentos consultados, páginas, versión, hash original y unidades entregadas, junto al texto legible del host. `selection=documents_of_evidence_delivered_to_generator` y `claim_support_verified=false` distinguen procedencia de apoyo de afirmaciones. Los IDs internos no son un formato exigido al texto del alumno ni una autorización de publicación.
