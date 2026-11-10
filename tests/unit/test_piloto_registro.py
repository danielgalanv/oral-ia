import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "piloto_registro", Path(__file__).resolve().parents[2] / "scripts" / "piloto_registro.py"
)
pr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pr)


def test_codes_are_unique_and_not_overwritten(tmp_path):
    assert pr.main(["--dir", str(tmp_path), "codigos", "18"]) == 0
    rows = pr.read_rows(tmp_path / "codigos.csv")
    assert len(rows) == 18 and len({r["codigo_participante"] for r in rows}) == 18
    assert pr.main(["--dir", str(tmp_path), "codigos", "3"]) == 1
    assert len(pr.read_rows(tmp_path / "codigos.csv")) == 18


def test_import_counts_and_summary_suppresses_small_groups(tmp_path):
    pr.main(["--dir", str(tmp_path), "iniciar"])
    report = {
        "format": "oralia-study-report/v1",
        "counts": {"completed_attempts": 2},
        "turns": [{"local_sources": [{"filename": "a"}]}, {"local_sources": [], "internet_sources": []}],
    }
    file = tmp_path / "r.json"
    file.write_text(json.dumps(report), encoding="utf-8")
    assert pr.main(["--dir", str(tmp_path), "importar", "P-AAAA", str(file)]) == 0
    row = pr.read_rows(tmp_path / "sesiones.csv")[0]
    assert row["preguntas_enviadas"] == "2" and row["consultas_a_fuentes"] == "1"
    assert "no se muestran desgloses" in pr.summary(tmp_path)


def test_summary_aggregates_with_five_sessions(tmp_path):
    rows = [
        {
            "codigo_participante": f"P-{i}",
            "inicio": "10:00",
            "fin": "10:30",
            "completada": "si" if i < 4 else "no",
            "preguntas_enviadas": "6",
        }
        for i in range(5)
    ]
    pr.write_rows(tmp_path / "sesiones.csv", pr.SESSION_FIELDS, rows)
    text = pr.summary(tmp_path)
    assert "Completadas: 4 (80 %)" in text and "Duración media: 30.0" in text


def test_anonymize_requires_confirmation(tmp_path):
    pr.main(["--dir", str(tmp_path), "codigos", "2"])
    assert pr.main(["--dir", str(tmp_path), "anonimizar"]) == 1
    assert (tmp_path / "codigos.csv").exists()
    assert pr.main(["--dir", str(tmp_path), "anonimizar", "--confirmar"]) == 0
    assert not (tmp_path / "codigos.csv").exists()
