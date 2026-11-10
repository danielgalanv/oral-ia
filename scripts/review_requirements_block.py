"""Prepare CPU render evidence for the whole requirements block (no activation)."""

import hashlib
import json
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "materiales/docente/piloto-requisitos/paquete-v1"
OUT = ROOT / "docs/audits/2026-10-27-requirements-block"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def render(source, key, numbers):
    folder = OUT / "renders" / key
    folder.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(source)
    images = []
    for number in numbers:
        target = folder / f"{number}.png"
        if not target.exists():
            pdf[number - 1].render(scale=1.5).to_pil().convert("RGB").save(target)
        images.append((number, target))
    for start in range(0, len(images), 6):
        canvas = Image.new("RGB", (1800, 2100), "#dddddd")
        draw = ImageDraw.Draw(canvas)
        for index, (number, target) in enumerate(images[start : start + 6]):
            im = Image.open(target)
            im.thumbnail((885, 650))
            x, y = (index % 2) * 900, (index // 2) * 700
            canvas.paste(im, (x, y + 28))
            draw.text((x + 8, y + 5), f"{key} PDF {number}", fill="black")
        canvas.save(folder / f"sheet-{start + 1}.jpg")
    pdf.close()


def main():
    manifest = json.loads((OLD / "manifest-v1.1.json").read_text(encoding="utf-8"))
    tracked = [*OLD.rglob("*")]
    dump(OUT / "preserved-before.json", {str(p.relative_to(ROOT)): sha(p) for p in tracked if p.is_file()})
    for key, name, count in [
        ("requisitos", "5 - Requisitos.pdf", 89),
        ("procedimiento", "6 - Procedimiento requisitos.pdf", 14),
    ]:
        render(OLD / "originales" / name, key, range(1, count + 1))
    # Relevant sections located from the actual NASA table of contents, then refined after reading.
    with pdfplumber.open(OLD / "originales/nasa-handbook.pdf") as pdf:
        headings = [{"page": i + 1, "text": p.extract_text() or ""} for i, p in enumerate(pdf.pages)]
    dump(OUT / "nasa-locator.json", headings)
    for doc in manifest["documents"]:
        if doc["id"].startswith("docente"):
            rows = json.loads((OLD / doc["extraction"]).read_text(encoding="utf-8"))
            (OUT / f"{doc['id']}-full.txt").write_text(
                "\n\n".join(f"PAGE {r['page']}\n{r['text']}" for r in rows), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
