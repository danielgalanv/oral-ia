# Experimental schema v1

Protocol: schema_version1, synthetic_only true, ablations_authorized bool, seed int,
repetitions1..5, conditions allowlist; extra forbidden. Catálogo15 incorporado únicamente.
Scenario: id/input/evidence/relevant IDs/prior/fault/propuesta controlada.
Cell: condición/repetición, resultado, traza/veredictos/versiones, secuencia, fuentes,
metrics(value,unit,source,missing_reason), recuperación/error/status.
Run: protocolo/corpus/hash/modelo/params/límites/hardware, celdas, agregados, indicadores
humanos(null+motivo) y firma estructural. No identidad real/código participante/audio.
Package: protocol.json, results.json, report.md y manifest.json SHA256 allowlist.
Lifecycle validate->temp cell->report->new directory->verify/replay. Sin tablas nuevas.
