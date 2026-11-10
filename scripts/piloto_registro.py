"""Registro de la clase piloto: códigos de participante, sesiones, cuestionarios e indicadores agregados.

Los datos viven en `piloto-privado/` (fuera de git). No guarda nombres salvo en `codigos.csv`, que
`anonimizar --confirmar` borra al cerrar el piloto. No puntúa ni infiere aprendizaje.

    python scripts/piloto_registro.py codigos 18
    python scripts/piloto_registro.py iniciar
    python scripts/piloto_registro.py importar P-XXX informe.json
    python scripts/piloto_registro.py resumen
    python scripts/piloto_registro.py anonimizar --confirmar
"""

import argparse
import csv
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIR = ROOT / "piloto-privado"
MIN_GROUP = 5
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

SESSION_FIELDS = [
    "codigo_participante",
    "fecha",
    "turno",
    "inicio",
    "fin",
    "duracion_minutos",
    "preguntas_enviadas",
    "aclaraciones_solicitadas",
    "consultas_a_fuentes",
    "cancelaciones",
    "completada",
    "minutos_revision_docente",
    "minutos_revision_manual_estimada",
    "observaciones_docentes",
]
LIKERT = [f"q{i}" for i in range(1, 11)]
QUESTION_FIELDS = (
    ["codigo_participante", "fecha", "turno"]
    + LIKERT
    + ["q11_preguntas", "q12_termino", "q13_incorrectas", "q14_alternativa", "comentarios"]
)


def read_rows(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def write_rows(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def new_code(existing):
    while True:
        code = "P-" + "".join(secrets.choice(ALPHABET) for _ in range(4))
        if code not in existing:
            return code


def cmd_codigos(directory, count):
    path = directory / "codigos.csv"
    if path.exists():
        print(f"Ya existe {path}; no se sobrescribe.")
        return 1
    codes = set()
    rows = []
    for _ in range(count):
        code = new_code(codes)
        codes.add(code)
        rows.append({"codigo_participante": code, "nombre": ""})
    write_rows(path, ["codigo_participante", "nombre"], rows)
    print(f"{count} códigos en {path}. Rellena el nombre a mano; el archivo está fuera de git.")
    return 0


def cmd_iniciar(directory):
    directory.mkdir(parents=True, exist_ok=True)
    for name, fields in (("sesiones.csv", SESSION_FIELDS), ("cuestionarios.csv", QUESTION_FIELDS)):
        path = directory / name
        if path.exists():
            print(f"Ya existe {path}")
        else:
            write_rows(path, fields, [])
            print(f"Creado {path}")
    return 0


def minutes_between(start, end):
    try:
        h1, m1 = (int(x) for x in start.split(":"))
        h2, m2 = (int(x) for x in end.split(":"))
    except ValueError:
        return None
    value = (h2 * 60 + m2) - (h1 * 60 + m1)
    return value if value >= 0 else None


def cmd_importar(directory, code, report_path):
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    if report.get("format") != "oralia-study-report/v1":
        print("El archivo no es una copia de sesión de ORALIA (oralia-study-report/v1).")
        return 1
    path = directory / "sesiones.csv"
    rows = read_rows(path)
    row = next((r for r in rows if r["codigo_participante"] == code), None)
    if row is None:
        row = {field: "" for field in SESSION_FIELDS}
        row["codigo_participante"] = code
        rows.append(row)
    turns = report.get("turns", [])
    row["preguntas_enviadas"] = str(report.get("counts", {}).get("completed_attempts", len(turns)))
    row["consultas_a_fuentes"] = str(
        sum(1 for t in turns if t.get("local_sources") or t.get("internet_sources"))
    )
    write_rows(path, SESSION_FIELDS, rows)
    questions, with_sources = row["preguntas_enviadas"], row["consultas_a_fuentes"]
    print(f"Importado para {code}: {questions} preguntas, {with_sources} con fuentes.")
    return 0


def numbers(rows, field):
    values = []
    for row in rows:
        try:
            values.append(float(str(row.get(field, "")).replace(",", ".")))
        except ValueError:
            pass
    return values


def mean(values):
    return sum(values) / len(values)


def summary(directory):
    sessions = read_rows(directory / "sesiones.csv")
    questionnaires = read_rows(directory / "cuestionarios.csv")
    lines = [f"Sesiones registradas: {len(sessions)}"]
    if len(sessions) < MIN_GROUP:
        lines.append(f"(menos de {MIN_GROUP} sesiones: no se muestran desgloses)")
    else:
        done = sum(1 for r in sessions if r.get("completada", "").strip().lower() in ("si", "sí"))
        completed = 100 * done / len(sessions)
        lines.append(f"Completadas: {done} ({completed:.0f} %). Abandono: {100 - completed:.0f} %")
        durations = numbers(sessions, "duracion_minutos")
        derived = [
            v
            for v in (
                minutes_between(r.get("inicio", ""), r.get("fin", ""))
                for r in sessions
                if not r.get("duracion_minutos")
            )
            if v is not None
        ]
        durations += derived
        if durations:
            lines.append(f"Duración media: {mean(durations):.1f} min ({len(durations)} sesiones con dato)")
        for field, label in (
            ("preguntas_enviadas", "Preguntas por sesión"),
            ("minutos_revision_docente", "Revisión docente (min por sesión)"),
            ("minutos_revision_manual_estimada", "Revisión manual equivalente estimada (min)"),
        ):
            values = numbers(sessions, field)
            if values:
                lines.append(f"{label}: media {mean(values):.1f} ({len(values)} con dato)")
    lines.append(f"Cuestionarios recibidos: {len(questionnaires)}")
    if len(questionnaires) < MIN_GROUP:
        lines.append(f"(menos de {MIN_GROUP} cuestionarios: no se muestran medias)")
    else:
        for field in LIKERT:
            values = numbers(questionnaires, field)
            if values:
                lines.append(f"{field}: media {mean(values):.2f} sobre 5 (n={len(values)})")
    return "\n".join(lines)


def cmd_anonimizar(directory, confirm):
    path = directory / "codigos.csv"
    if not path.exists():
        print("No hay tabla de códigos que borrar.")
        return 0
    if not confirm:
        print(f"Se borraría {path} (vínculo entre nombres y códigos). Repite con --confirmar para hacerlo.")
        return 1
    path.unlink()
    print("Tabla de códigos borrada: los datos restantes quedan anonimizados de forma irreversible.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("codigos")
    p.add_argument("count", type=int)
    sub.add_parser("iniciar")
    p = sub.add_parser("importar")
    p.add_argument("code")
    p.add_argument("report")
    sub.add_parser("resumen")
    p = sub.add_parser("anonimizar")
    p.add_argument("--confirmar", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "codigos":
        return cmd_codigos(args.dir, args.count)
    if args.command == "iniciar":
        return cmd_iniciar(args.dir)
    if args.command == "importar":
        return cmd_importar(args.dir, args.code, args.report)
    if args.command == "resumen":
        print(summary(args.dir))
        return 0
    return cmd_anonimizar(args.dir, args.confirmar)


if __name__ == "__main__":
    sys.exit(main())
