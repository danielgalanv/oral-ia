# Data model009

Sin tablas/migraciones. ExcerptV1 frozen: text,start,end,source_sha256. Rango sobre str
original; strip en extremos; si>400,primeros400 hasta último espacio literal y elipsis…;
perfil inmutable material-excerpt/v1. Hash sobre bytes UTF8 completos sin normalización.
Snapshot/T090 sin campos nuevos. data_ref incluye fragment:id:excerpt-v1:hash:start:end.
TraceEvent material_excerpt_bound payloadschema1 con referencias/versión/ubicación/hash
fuente/rango/hashvalor. Sin input/candidato denegado ni autoridad del modelo.

El límite es una ventana de400caracteres Python y elipsis adicional si recorta: máximo
401caracteres visibles por fuente (hasta1205para3con separadores),como en el adaptador
previo. No se promete preservar grafemas ni semántica general.

T016:uploading y uploadInFlight son estado efímero del componente, sin persistencia ni
autoridad. Estado activo solo hasta confirmar fetch/error; no representa avance interno.
Header/middleware de demora existe únicamente en harness E2E, tras endpoint real.
