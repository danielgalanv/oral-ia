"""Render already captured synthetic chat turns; never infer or authorize."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Readable display transcript from frozen lab receipts")
    parser.add_argument("--packet", type=Path, required=True)
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        parser.error("Packet directory missing")
    files = sorted(packet.glob("*-0-A.json")) + sorted(packet.glob("*-0-documental.json"))
    files += sorted(packet.glob("*-0-pedagogica.json"))
    if not files:
        parser.error("No first-repetition A/B/C files found")
    lines = [
        "# Diálogos sintéticos realmente mostrados",
        "",
        "Solo laboratorio. Los raw, solicitudes completas y eventos permanecen en los JSON originales. "
        "Un aviso operativo no es una respuesta docente; ninguna candidata está autorizada.",
        "",
    ]
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        lines += [f"## {data['case']} — {data['variant']}", ""]
        for index, row in enumerate(data["turns"], 1):
            provider = row.get("provider", {})
            params = provider.get("parameters", {})
            kind = row.get("display_kind", "candidate" if row.get("displayed_text") else "none")
            seconds = round(row["elapsed_seconds"], 2) if "elapsed_seconds" in row else "sin dato"
            lines += [
                f"### Turno {index}: {row['stage']}",
                "",
                "**Entrada ficticia:** " + row.get("input", "[no ejecutado]"),
                "",
                "**Texto mostrado:**",
                "",
                row.get("displayed_text") or "[No se mostró texto]",
                "",
                "**Estado técnico:** "
                + ", ".join(
                    [
                        f"tipo={kind}",
                        f"error={row.get('error', 'ninguno')}",
                        f"fin={provider.get('finish_reason', 'sin dato')}",
                        f"tokens_entrada={params.get('input_tokens', 'sin dato')}",
                        f"tokens_salida={params.get('output_tokens', 'sin dato')}",
                        f"segundos={seconds}",
                    ]
                ),
                "",
                "**Páginas recuperadas:** " + (", ".join(row.get("retrieved_source_ids", [])) or "ninguna"),
                "",
            ]
    (packet / "dialogues-readable.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
