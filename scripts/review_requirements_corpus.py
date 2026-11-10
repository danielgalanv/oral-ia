"""Encode the bounded page review; retain the first extraction unchanged."""

import copy
import importlib.metadata
import json
import re
from difflib import SequenceMatcher

import pdfplumber
from prepare_requirements_corpus import PACKAGE, ROOT, digest, write_new


def normalized(text):
    lines = [
        line for line in text.splitlines() if not re.fullmatch(r"\d+|30/10/2014|Chapter 4.*", line.strip())
    ]
    return " ".join(re.findall(r"[a-z]+", " ".join(lines).lower()))


def main():
    initial = json.loads((PACKAGE / "manifest-initial.json").read_text(encoding="utf-8"))
    reviewed = PACKAGE / "revisado"
    reviewed.mkdir(exist_ok=True)
    selected = {
        "docente-requisitos": [3, 7, 10, 20, 21, 22, 33, 34, 39, 47, 52, 53, 56, 60, 72, 73, 74, 76, 82, 83],
        "docente-procedimiento": [2, 10, 11, 12],
        "nasa-seh": [207, 208, 209, 210, 211, 213],
        "sommerville": [3, 6, 15, 19, 23, 55, 63, 69, 72, 73, 76, 82],
        "nasa-swe055": [],
    }
    origins = {
        "nasa-seh": "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf",
        "nasa-swe055": "https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695440/SWE-055+-+Requirements+Validation",
        "sommerville": (
            "https://software-engineering-book.com/slides/ → enlace del autor a "
            "slides.zip → slides/Ch4 Req Eng.pptx"
        ),
    }
    all_rows = {}
    qa = []
    for doc in initial["documents"]:
        key = doc["id"]
        rows = json.loads((PACKAGE / doc["extraction"]).read_text(encoding="utf-8"))
        prefix = {
            "docente-requisitos": "docente",
            "docente-procedimiento": "procedimiento",
            "nasa-seh": "nasa",
            "sommerville": "sommerville",
        }.get(key)
        for row in rows:
            n = row["page"]
            preview = PACKAGE / "qa" / f"{prefix}-{n}.png"
            if preview.is_file():
                row["preview"] = preview.relative_to(PACKAGE).as_posix()
            if n in selected[key]:
                row["status"] = "disponible"
                row["reason"] = (
                    "Contraste técnico de texto/listas o tabla con página renderizada; "
                    "sin aceptación docente inferida"
                )
                if not preview.is_file():
                    raise ValueError("Missing reviewed page preview")
                qa.append(
                    dict(
                        passage=row["id"],
                        preview=row["preview"],
                        review="texto y orden contrastados visualmente; no certifica doctrina o eficacia",
                    )
                )
            if key == "docente-requisitos" and n in [22, 33, 34, 47]:
                with pdfplumber.open(PACKAGE / doc["original"]) as pdf:
                    table = pdf.pages[n - 1].extract_tables()[0]
                row["tables"] = table
                row["text"] = (
                    row["section"]
                    + "\n"
                    + "\n".join(
                        " | ".join((cell or "").replace("\n", " ") for cell in line) for line in table
                    )
                )
                row["derivation"] = (
                    "tabla nativa extraída por celdas y contrastada visualmente; raw_text"
                    " preservado; sin traducción"
                )
            if key == "nasa-seh":
                row["printed_page"] = n - 10 if n >= 11 else None
                if n in [207, 211, 213]:
                    with pdfplumber.open(PACKAGE / doc["original"]) as pdf:
                        page = pdf.pages[n - 1]
                        columns = [
                            page.crop(b).extract_text() or ""
                            for b in [
                                (0, 155, page.width / 2, page.height - 32),
                                (page.width / 2, 155, page.width, page.height - 32),
                            ]
                        ]
                    heading = {
                        207: "Appendix C: How to Write a Good Requirement—Checklist",
                        211: "Appendix D: Requirements Verification Matrix",
                        213: "Appendix E: Creating the Validation Plan with a Validation Requirements Matrix",
                    }[n]
                    row["text"] = heading + "\n" + "\n\n".join(columns)
                    row["section"] = heading
                if n in selected[key]:
                    row["text"] = row["text"].replace("\x86", "□")
                    row["reason"] += (
                        "; lectura izquierda→derecha; continuaciones C.3 207→208, Consistency"
                        " 208→209 y Reliability 209→210; consultar páginas contiguas"
                    )
                elif n == 212:
                    row["reason"] = (
                        "Tabla D-1 girada: texto/columnas no fieles. Consultable en original;"
                        " no usar extracción como evidencia"
                    )
                elif n == 214:
                    row["reason"] = (
                        "Tabla E-1: extracción y celdas no revisadas; original renderizado disponible"
                    )
                else:
                    row["reason"] = (
                        "Fuera del subconjunto revisado C–E de este incremento; no acredita "
                        "exclusión académica"
                    )
            if key == "docente-procedimiento" and n in [13, 14]:
                row["reason"] = (
                    "Aparente inversión título/cuerpo entre páginas 13 y 14; requiere "
                    "decisión docente. Original intacto"
                )
            if key == "sommerville" and n == 60:
                row["reason"] = (
                    "Especificación en imagen: extractor recupera título/pie pero omite "
                    "el cuerpo. Sin OCR por alcance"
                )
            row["text_sha256"] = digest(row["text"].encode())
        if key == "nasa-swe055":
            # One bounded exact passage, avoiding visual applicability icons and nested duplicates.
            raw = rows[0]
            core = copy.deepcopy(raw)
            core.update(
                id="nasa-swe055:1-core",
                section="1. Requirements — solo §4.1.7",
                text=(
                    "4.1.7 The project manager shall perform requirements validation to "
                    "ensure that the software will perform as intended in the customer "
                    "environment."
                ),
                status="disponible",
                reason=(
                    "Párrafo exacto contrastado con HTML oficial y captura local; tabla "
                    "de aplicabilidad excluida"
                ),
                derivation="pasaje literal acotado del HTML; no traducción",
            )
            core["text_sha256"] = digest(core["text"].encode())
            rows.append(core)
            for row in rows[:-1]:
                row["reason"] = (
                    "Sección no revisada íntegramente; iconos de aplicabilidad omitidos o"
                    " duplicación de listas anidadas en primera extracción. Solo §4.1.7 "
                    "está disponible"
                )
            qa.append(
                dict(
                    passage=core["id"],
                    review=(
                        "Comparado con main-content HTML y encabezado1/4.1.7 de URL oficial; "
                        "no se atribuye revisión al resto"
                    ),
                )
            )
        all_rows[key] = rows
        doc["origin"] = (
            origins.get(
                key,
                str(
                    next(
                        x
                        for x in json.loads(
                            (ROOT / "materiales/docente/asignatura-real-20261021/inventario.json").read_text(
                                encoding="utf-8"
                            )
                        )
                        if x["relative"] == doc["filename"]
                    )["path"]
                ),
            )
            if key.startswith("docente")
            else origins[key]
        )
        doc["conditions"] = (
            (
                "Copia local para consulta docente autorizada por el usuario; "
                "conserva atribuciones y derechos de terceros; sin licencia abierta "
                "ni redistribución pública acreditada"
            )
            if key.startswith("docente")
            else (
                (
                    "NTRS 20170001761: Distribution Public; Public Use Permitted. "
                    "Conservar atribución; no implica aval NASA ni licencia de todos los "
                    "elementos de terceros"
                )
                if key == "nasa-seh"
                else (
                    (
                        "Página pública oficial NASA, captura local para consulta; sin "
                        "licencia específica identificada en la página; no redistribución "
                        "pública del paquete"
                    )
                    if key == "nasa-swe055"
                    else (
                        "Descarga ofrecida explícitamente por el autor para presentaciones "
                        "SE10. Uso local docente; conservar atribución. No consta licencia "
                        "abierta ni autorización de redistribución pública; sin acceso a "
                        "soluciones/quizzes restringidos"
                    )
                )
            )
        )
        doc["available"] = sum(r["status"] == "disponible" for r in rows)
        doc["quarantine"] = len(rows) - doc["available"]
        doc["extraction"] = f"revisado/{key}.json"

    equivalences = []
    teacher = all_rows["docente-requisitos"]
    for som in all_rows["sommerville"]:
        a = normalized(som["raw_text"])
        candidates = [(SequenceMatcher(None, a, normalized(t["raw_text"])).ratio(), t) for t in teacher]
        score, match = max(candidates, key=lambda v: v[0])
        if score >= 0.9:
            equivalences.append(
                dict(
                    a=som["id"],
                    canonical=match["id"],
                    ratio=round(score, 5),
                    decision=(
                        "pasaje equivalente candidato por texto normalizado; no cobertura "
                        "independiente; originales/versiones separados"
                    ),
                )
            )
            som["equivalent_to"] = match["id"]
    for doc in initial["documents"]:
        write_new(PACKAGE / doc["extraction"], all_rows[doc["id"]])
        doc["extraction_sha256"] = digest((PACKAGE / doc["extraction"]).read_bytes())
    concepts = [
        (
            "Necesidades y requisitos",
            ["docente-requisitos:3", "docente-procedimiento:2", "sommerville:3"],
            "La diapositiva oficial y la adaptación solapan; no suman evidencia independiente",
        ),
        (
            "Tipos funcionales/no funcionales y niveles",
            [
                "docente-requisitos:7",
                "docente-requisitos:10",
                "sommerville:6",
                "sommerville:15",
                "sommerville:19",
            ],
            "Clasificaciones de software; no universalizar a toda ingeniería de sistemas",
        ),
        (
            "Calidad, especificación y comprobabilidad",
            [
                "docente-procedimiento:10",
                "docente-procedimiento:11",
                "docente-requisitos:20",
                "docente-requisitos:21",
                "docente-requisitos:22",
                "docente-requisitos:33",
                "docente-requisitos:34",
                "docente-requisitos:39",
                "nasa-seh:207",
                "nasa-seh:208",
                "nasa-seh:210",
            ],
            "NASA C.1–C.4 es guía de sistemas; tablas normalizadas con raw_text conservado",
        ),
        (
            "Obtención, análisis y negociación",
            [
                "docente-requisitos:52",
                "docente-requisitos:53",
                "docente-requisitos:56",
                "docente-requisitos:60",
            ],
            "Cobertura inicial de entrevistas y actividades; diagramas no revisados en cuarentena",
        ),
        (
            "Validación y verificación",
            [
                "docente-procedimiento:12",
                "docente-requisitos:72",
                "docente-requisitos:73",
                "docente-requisitos:74",
                "nasa-seh:208",
                "nasa-seh:211",
                "nasa-seh:213",
                "nasa-swe055:1-core",
            ],
            (
                "Distinguir calidad del documento, validación de requisitos y "
                "validación del producto; NASA software y sistemas separados"
            ),
        ),
        (
            "Gestión, cambio y trazabilidad",
            [
                "docente-requisitos:76",
                "docente-requisitos:82",
                "docente-requisitos:83",
                "nasa-seh:209",
                "sommerville:82",
            ],
            "Procedimiento13–14 está en cuarentena por inversión aparente",
        ),
        (
            "INCOSE",
            [],
            (
                "No incorporada: GtWR4 de tienda y webinar168 solo miembros; no se "
                "usan PDF directos indexados para eludir condiciones"
            ),
        ),
    ]
    initial.update(
        scope="Consulta docente parcial sin vectores; no tutor ni corpus completo de la asignatura",
        date="2026-10-27",
        concepts=[dict(label=a, passages=b, limits=c) for a, b, c in concepts],
        limitations=[
            (
                "INCOSE no incorporada. GtWR v4 (1 July 2023) se ofrece en tienda; "
                "webinar168 (25 October 2023) está etiquetado Members-Only. Descarga "
                "de página con 403 registrada. Sin compra/login ni búsqueda de copias"
                " alternativas."
            ),
            (
                "Originales íntegros disponibles; solo los pasajes marcados "
                "disponibles fueron contrastados en este incremento. Cuarentena no "
                "significa fuera del curso."
            ),
            (
                "Sin OCR ni extracción fiable de imágenes/diagramas no revisados. "
                "NASA tablaD-1 PDF212 y Sommerville diapositiva60 no son evidencia "
                "textual disponible."
            ),
            (
                "Sin índice semántico: T077 identidad efectiva y segmentación por "
                "tokenizer siguen pendientes. Búsqueda literal por documento y mapa "
                "manual, sin simular relevancia."
            ),
            (
                "Sin traducción doctrinal: textos en idioma original. Normalización "
                "mecánica de tablas/columnas etiquetada; no cambia el original."
            ),
        ],
        discrepancies=[
            (
                "Procedimiento13 dice Registrar problemas pero su cuerpo describe "
                "trazabilidad;14 dice Registrar trazabilidad pero describe problemas."
                " Se conservan ambos y quedan en cuarentena."
            ),
            (
                "Requisitos72/73 agrupa controles de calidad bajo validation; "
                "Procedimiento10/11 los llama verificar calidad y12 validar "
                "necesidades. No imponer una equivalencia terminológica única."
            ),
            (
                "NASA SEH C recomienda formulación positiva; Requisitos10 admite "
                "especificar lo que no debe hacer el sistema. Diferencia contextual, "
                "no corrección automática de una fuente por otra."
            ),
            (
                "NASA SEH C.1 usa should como goal; Sommerville55 lo usa para "
                "desirable requirements. Conservar la fuerza modal y contexto de cada"
                " fuente, sin traducir ambos como obligación."
            ),
            (
                "El manual NASA es guía de sistemas, no directiva de software; "
                "SWE-055 sí trata software NASA bajo NPR7150.2D. Ninguno impone por "
                "sí mismo obligaciones a la asignatura."
            ),
            (
                "La adaptación docente89 páginas reordena/añade contenido respecto al"
                " capítulo oficial88 diapositivas. Comparación de contenido "
                "registrada; fechas2014/SE10, no atribuirlas a una edición posterior."
            ),
            (
                "No se puede comparar doctrina de INCOSE sin contenido autorizado "
                "adquirido; la familia sigue ausente."
            ),
        ],
        tools={p: importlib.metadata.version(p) for p in ["pdfplumber", "python-pptx", "lxml", "pypdfium2"]},
        review="asistente: revisión técnica de extracción, no aprobación docente",
        available=sum(d["available"] for d in initial["documents"]),
        quarantine=sum(d["quarantine"] for d in initial["documents"]),
    )
    write_new(PACKAGE / "equivalencias.json", equivalences)
    write_new(PACKAGE / "qa/review.json", qa)
    write_new(PACKAGE / "manifest.json", initial)
    print([(d["id"], d["available"], d["quarantine"]) for d in initial["documents"]])
    print("Equivalences", len(equivalences))


if __name__ == "__main__":
    main()
