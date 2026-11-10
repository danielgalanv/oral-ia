"""Assemble the opt-in v2 documentary package from reviewed, immutable sources."""

import copy
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

import pdfplumber
from review_requirements_block import OLD, OUT, dump, sha

NEW = OLD.parent / "paquete-v2"
TEACHER = Path(
    "C:/Users/<usuario>/OneDrive - Universidad Politécnica de Madrid/Docencia/"
    "Ingeniería del software/22-23/Traspis"
)
SUPPLEMENTS = {
    "docente-procesos": ("3 - Procesos.pdf", "procesos", list(range(37, 42))),
    "docente-agil": ("4 - Agil.pdf", "agil", [25, 26, 27]),
    "docente-modelos": ("7 - Modelos.pdf", "modelos", list(range(35, 40))),
    "docente-testing": ("12 - Testing.pdf", "testing", [55, 56]),
}
FIGURES = {8, 9, 18, 27, 29, 44, 45, 50, 55, 66, 70, 81, 84}
ADMIN = {1, 2, 6, 26, 48, 51, 71, 77, 85}
NASA = [64, 66, 70, 71, 140, 142, 143, 144, 145]


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def copy_asset(source, relative):
    target = NEW / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(source, target)
    if sha(source) != sha(target):
        raise ValueError("Asset changed")
    return relative


def reviewed_preview(row, key):
    relative = f"qa/v2/{key}-{row['page']}.png"
    row["preview"] = copy_asset(OUT / "renders" / key / f"{row['page']}.png", relative)


def available(row, reason="Texto/listas contrastados contra página renderizada completa"):
    row.update(
        status="disponible",
        qa_state="revisado_textual_visual",
        reason=reason + "; revisión técnica, aceptación docente pendiente",
    )


def blocked(row, state, reason):
    row.update(status="cuarentena", qa_state=state, reason=reason)


def main():
    NEW.mkdir(exist_ok=True)
    old = json.loads((OLD / "manifest-v1.1.json").read_text(encoding="utf-8"))
    manifest = copy.deepcopy(old)
    manifest.update(
        package_id="oralia-requisitos-20261027-v2",
        scope=(
            "Bloque docente de requisitos: revisión integral de principales, "
            "complementos seleccionados y huecos explícitos. Solo consulta "
            "documental, sin tutor ni índice."
        ),
        predecessor={"path": "../paquete-v1/manifest-v1.1.json", "sha256": sha(OLD / "manifest-v1.1.json")},
    )
    all_rows = {}
    for doc in manifest["documents"]:
        key = doc["id"]
        copy_asset(OLD / doc["original"], doc["original"])
        rows = json.loads((OLD / doc["extraction"]).read_text(encoding="utf-8"))
        for row in rows:
            row["previous_status"] = row["status"]
            row["qa_state"] = "revisado_previo" if row["status"] == "disponible" else "no_revisado"
            if row.get("preview"):
                copy_asset(OLD / row["preview"], row["preview"])
            if key in {"docente-requisitos", "docente-procedimiento"}:
                reviewed_preview(row, "requisitos" if key.endswith("requisitos") else "procedimiento")
                number = row["page"]
                available(row)
                if key == "docente-requisitos":
                    if number in ADMIN:
                        blocked(
                            row,
                            "portada_indice_separador",
                            "Revisada: portada, índice o separador; sin contenido académico adicional",
                        )
                    elif number in FIGURES:
                        blocked(
                            row,
                            "fallo_extraccion",
                            (
                                "Figura/imagen contrastada visualmente; extracción omite cuerpo o "
                                "relaciones. Original y render consultables; no evidencia textual "
                                "completa. No se excluye el tema"
                            ),
                        )
                    elif number == 32:
                        with pdfplumber.open(OLD / doc["original"]) as pdf:
                            p = pdf.pages[31]
                            row["text"] = (
                                row["section"]
                                + "\n"
                                + "\n".join(
                                    p.crop(box).extract_text() or ""
                                    for box in [
                                        (0, 95, p.width / 2, p.height - 38),
                                        (p.width / 2, 95, p.width, p.height - 38),
                                    ]
                                )
                            )
                        row["derivation"] = (
                            "Lectura por columna izquierda completa y después derecha; cotejo del "
                            "esquema; raw_text preservado, sin traducción"
                        )
                    elif number == 36:
                        with pdfplumber.open(OLD / doc["original"]) as pdf:
                            table = pdf.pages[35].extract_tables()[0]
                        row["tables"] = table
                        row["text"] = (
                            row["section"]
                            + "\n"
                            + "\n".join(
                                " | ".join((c or "").replace("\n", " ") for c in line) for line in table
                            )
                        )
                        row["derivation"] = (
                            "Tabla nativa por celdas contrastada contra original; raw_text "
                            "preservado; sin traducción"
                        )
                else:
                    if number == 1:
                        blocked(
                            row,
                            "portada_indice_separador",
                            "Revisada: portada sin contenido académico adicional",
                        )
                    elif number == 3:
                        blocked(
                            row,
                            "fallo_extraccion",
                            (
                                "Diagrama de actividad revisado visualmente; extractor solo obtiene el "
                                "pie. Sin texto completo: no habilitado como evidencia; "
                                "original/render disponibles"
                            ),
                        )
                    elif number in {13, 14}:
                        available(
                            row,
                            (
                                "Fidelidad al original comprobada: aparente inversión título/cuerpo "
                                "presente en PDF. Leer ambas páginas juntas, sin reasignar títulos: "
                                "p13 cuerpo trazabilidad; p14 cuerpo problemas"
                            ),
                        )
                        row["context_required"] = ["docente-procedimiento:13", "docente-procedimiento:14"]
            elif key == "nasa-seh":
                if row["page"] in NASA:
                    reviewed_preview(row, "nasa")
                    with pdfplumber.open(OLD / doc["original"]) as pdf:
                        p = pdf.pages[row["page"] - 1]
                        top = 356 if row["page"] == 70 else 60
                        columns = [
                            p.crop((x, top, x + p.width / 2, p.height - 40)).extract_text() or ""
                            for x in [0, p.width / 2]
                        ]
                        if row["page"] == 70:
                            columns.insert(0, p.crop((0, 60, p.width, 350)).extract_text() or "")
                        elif row["page"] == 66:
                            columns = [
                                p.crop((x, 60, x + p.width / 2, 440)).extract_text() or ""
                                for x in [0, p.width / 2]
                            ]
                            columns.append(p.crop((0, 460, p.width, 690)).extract_text() or "")
                        elif row["page"] == 140:
                            columns = [
                                p.crop((p.width / 2, 220, p.width, 515)).extract_text() or "",
                                p.crop((0, 530, p.width, 675)).extract_text() or "",
                            ]
                    text = "\n\n".join(columns)
                    if row["page"] == 140:
                        text = text[text.index("6.2 Requirements Management") :]
                        # The definition callout concerns requirements traceability; retain it.
                    elif row["page"] == 145:
                        text = text.split("6.3 Interface Management")[0]
                    row.update(
                        text=text,
                        section=(
                            "NASA §4.2 Technical Requirements Definition"
                            if row["page"] < 100
                            else "NASA §6.2 Requirements Management"
                        ),
                        printed_page=row["page"] - 10,
                    )
                    row["derivation"] = (
                        "Lectura por columnas; recuadros de ancho completo separados en "
                        "PDF66/70/140; fragmento de §6.2 en páginas límite140/145; raw_text "
                        "preservado. Sin traducción; leer páginas contiguas para continuaciones"
                    )
                    available(row)
                elif row["status"] != "disponible":
                    state = (
                        "fallo_extraccion"
                        if row["page"] in {65, 67, 68, 69, 141, 212, 214}
                        else "fuera_subconjunto_complementario"
                    )
                    blocked(
                        row,
                        state,
                        (
                            (
                                "Complemento seleccionado: §4.2 (texto), §6.2 y apéndices C–E. Otras "
                                "páginas no habilitadas; no revisión integral del manual. "
                                "Figuras/tablas65/67/68/212/214 requieren representación textual fiel"
                            )
                            if state != "fallo_extraccion"
                            else (
                                "Contraste visual realizado; diagrama/tabla no conservado fielmente en "
                                "texto. Mantener cuarentena textual; consultar original/render"
                            )
                        ),
                    )
                    if row["page"] in {65, 67, 68, 69, 141, 212, 214}:
                        reviewed_preview(row, "nasa")
            elif key == "sommerville" and row["status"] != "disponible":
                blocked(
                    row,
                    "no_revisado_complementario",
                    (
                        "Capítulo oficial disponible íntegro; complemento textual acotado a12 "
                        "diapositivas previamente contrastadas. El bloque docente se revisa "
                        "íntegro por separado. Equivalencias candidatas no son aceptación ni "
                        "evidencia independiente"
                    ),
                )
            elif key == "nasa-swe055" and row["status"] != "disponible":
                blocked(
                    row,
                    "fallo_extraccion",
                    (
                        "Captura íntegra preservada; extracción de sección amplia duplica "
                        "listas y no resuelve iconos/tablas. No usar como texto acreditado; "
                        "§4.1.7 se conserva en unidad core"
                    ),
                )
            row["text_sha256"] = digest(row["text"])
        all_rows[key] = rows

    for key, (filename, preview_key, selected) in SUPPLEMENTS.items():
        original = f"originales/{filename}"
        copy_asset(TEACHER / filename, original)
        with pdfplumber.open(TEACHER / filename) as pdf:
            rows = []
            for index, p in enumerate(pdf.pages, 1):
                raw = p.extract_text() or ""
                row = dict(
                    id=f"{key}:{index}",
                    page=index,
                    section=raw.splitlines()[0] if raw else "Sin texto extraído",
                    raw_text=raw,
                    text=raw,
                    source_sha256=sha(TEACHER / filename),
                    text_sha256=digest(raw),
                    derivation="Extracción nativa pdfplumber; sin traducción",
                )
                blocked(
                    row,
                    "fuera_subconjunto",
                    (
                        "Documento adyacente: solo sección relacionada con requisitos "
                        "seleccionada; resto no define el alcance del bloque ni se incorpora "
                        "al tutor"
                    ),
                )
                if index in selected:
                    reviewed_preview(row, preview_key)
                    available(row)
                    if (key, index) in {
                        ("docente-procesos", 39),
                        ("docente-agil", 26),
                        ("docente-agil", 27),
                        ("docente-modelos", 37),
                        ("docente-modelos", 39),
                    }:
                        blocked(
                            row,
                            "fallo_extraccion",
                            (
                                "Figura/tarjeta revisada visualmente; texto/relaciones omitidos en "
                                "extracción. Original/render consultables, cuarentena textual "
                                "conservada"
                            ),
                        )
                    if (key, index) == ("docente-modelos", 38):
                        table = p.extract_tables()[0]
                        row["tables"] = table
                        row["text"] = (
                            row["section"]
                            + "\n"
                            + "\n".join(
                                " | ".join((c or "").replace("\n", " ") for c in line) for line in table
                            )
                        )
                        row["text_sha256"] = digest(row["text"])
                        row["derivation"] = "Tabla por celdas cotejada visualmente; raw_text preservado"
                rows.append(row)
        all_rows[key] = rows
        manifest["documents"].append(
            dict(
                id=key,
                filename=filename,
                original=original,
                author="Docencia UPM; adaptación de Ian Sommerville",
                edition=(
                    "Curso22-23, material con atribución a capítulos Sommerville; "
                    "sin nueva edición inferida"
                ),
                domain="software; complemento del bloque requisitos",
                sha256=sha(TEACHER / filename),
                origin=str(TEACHER / filename),
                access_date="2026-10-27",
                teacher_acceptance="pendiente",
                conditions=old["documents"][0]["conditions"],
                extracted_pages=len(rows),
            )
        )

    for doc in manifest["documents"]:
        rows = all_rows[doc["id"]]
        for row in rows:
            if row.get("preview"):
                row["preview_sha256"] = sha(NEW / row["preview"])
        doc["extraction"] = f"revisado/{doc['id']}.json"
        dump(NEW / doc["extraction"], rows)
        doc.update(
            extracted_units=len(rows),
            available=sum(r["status"] == "disponible" for r in rows),
            quarantine=sum(r["status"] != "disponible" for r in rows),
            extraction_sha256=sha(NEW / doc["extraction"]),
            status=(
                "revision_tecnica_integral_con_huecos"
                if doc["id"] in {"docente-requisitos", "docente-procedimiento"}
                else "complemento_seleccionado"
            ),
            qa_states=dict(Counter(r["qa_state"] for r in rows)),
        )

    def refs(key, nums):
        return [
            f"{key}:{n}"
            for n in nums
            if any(r["page"] == n and r["status"] == "disponible" for r in all_rows[key])
        ]

    definitions = [
        (
            "Definición, necesidades, abstracción y destinatarios",
            [3, 4, 5, 7],
            [2, 4, 5],
            [],
            "Figuras8/9 sin texto completo; no limitan definición ni niveles",
            refs("sommerville", [3, 6]),
        ),
        (
            "Tipos, niveles, dominio e integración",
            list(range(10, 20)) + [23, 24, 25],
            [6, 8],
            [],
            (
                "Figura18 sin relaciones textuales; dominio en Procedimiento8 tiene "
                "acepción tecnológica más estrecha"
            ),
            refs("sommerville", [15, 19, 23]) + refs("nasa-seh", [64, 66]),
        ),
        (
            "Calidad, metas, métricas y comprobabilidad",
            [13, 14, 20, 21, 22, 39, 40],
            [10, 11],
            [],
            "Métricas son ejemplos de la fuente; no umbrales universales",
            refs("nasa-seh", [207, 208, 210]) + refs("sommerville", [55]),
        ),
        (
            "SRS: estructura, lectores, variabilidad y estándares",
            list(range(27, 37)),
            [6, 7, 8],
            [],
            (
                "27 miniatura SRS y29 gráfico lectores en cuarentena; 31/32 son "
                "material docente sobre29148, no se incorpora la norma completa ni se "
                "acredita vigencia normativa"
            ),
            [],
        ),
        (
            "Especificación natural, estructurada, tabular y diseño",
            list(range(35, 48)),
            [6, 8, 9],
            [],
            (
                "44/45 formulario no extraído fielmente;42/43 explican técnica y47 "
                "aporta tabla completa; no sustituir el ejemplo médico por guía clínica"
            ),
            [],
        ),
        (
            "Proceso iterativo y visión general",
            [49, 52, 54, 56],
            [2, 4, 5, 6, 7, 9],
            [],
            "Diagramas50/55 yProcedimiento3 en cuarentena textual",
            refs("nasa-seh", [64]),
        ),
        (
            "Obtención, stakeholders, análisis, priorización y negociación",
            list(range(52, 62)),
            [4, 5, 9],
            [],
            "Entrevistas no agotan técnicas; priorización/negociación expresas en54/56",
            refs("sommerville", [63, 69]) + refs("nasa-seh", [64, 66]),
        ),
        (
            "Escenarios, casos de uso y modelos",
            [62, 63, 64, 65, 66],
            [4, 5, 6, 8, 9],
            refs("docente-modelos", [35, 36, 38]),
            "Figura66 yModelos37/39 sin representación textual íntegra; tabla38 contrastada",
            [],
        ),
        (
            "Etnografía y prototipado",
            [67, 68, 69, 70, 74],
            [12],
            refs("docente-procesos", [37, 38, 40, 41]),
            "Diagramas70 yProcesos39 en cuarentena; prototipos desechables según fuente/contexto",
            [],
        ),
        (
            "Agilidad e historias de usuario",
            [28, 87],
            [],
            refs("docente-agil", [25]),
            "Tarjetas26/27 de Ágil en cuarentena textual; no se incorpora bloque ágil completo",
            [],
        ),
        (
            "Validación, verificación, revisiones y pruebas derivadas",
            list(range(72, 77)),
            [10, 11, 12],
            refs("docente-testing", [55, 56]),
            (
                "Distinguir validación de requisitos y producto; tablas NASA D-1/E-1 "
                "no disponibles como texto"
            ),
            refs("nasa-seh", [70, 71, 208, 211, 213])
            + ["nasa-swe055:1-core"]
            + refs("sommerville", [72, 73, 76]),
        ),
        (
            "Gestión, evolución, cambio, problemas y trazabilidad",
            list(range(78, 85)),
            [11, 13, 14],
            [],
            "Procedimiento13/14 fieles con inversión aparente documentada; figuras81/84 no extraídas",
            refs("nasa-seh", [140, 142, 143, 144, 145, 209]) + refs("sommerville", [82]),
        ),
    ]
    coverage = []
    manifest["concepts"] = []
    old_refs = {
        r["id"]
        for d in old["documents"]
        for r in json.loads((OLD / d["extraction"]).read_text(encoding="utf-8"))
        if r["status"] == "disponible"
    }
    for label, req, proc, additional, limits, external in definitions:
        passages = (
            refs("docente-requisitos", req) + refs("docente-procedimiento", proc) + additional + external
        )
        manifest["concepts"].append(dict(label=label, passages=passages, limits=limits))
        coverage.append(
            dict(
                subtopic=label,
                before=[r for r in passages if r in old_refs],
                after=passages,
                before_by_source=dict(Counter(r.split(":")[0] for r in passages if r in old_refs)),
                after_by_source=dict(Counter(r.split(":")[0] for r in passages)),
                limits=limits,
                status="cobertura_documental_con_huecos_explicitos",
                acceptance="pendiente",
            )
        )
    manifest["concepts"].append(
        dict(
            label="INCOSE — no incorporada",
            passages=[],
            limits=(
                "Summary Sheet gratuita: permiso de reproducción con atribución "
                "comprobado en recurso oficial; descarga local403. Alternativa oficial "
                "Requirements—Why Bother también403. Sin original local, no cobertura "
                "de esta familia"
            ),
        )
    )
    manifest["limitations"] = [
        (
            "Revisión técnica integral de103 páginas principales; no todas "
            "habilitadas: portada/separador y extracción incompleta se distinguen "
            "en motivo yqa_state. Cuarentena no significa fuera del curso. "
            "Disponible solo texto/listas/tablas fieles; figuras omitidas siguen "
            "en cuarentena aunque visualmente revisadas."
        ),
        (
            "Sommerville:12 diapositivas complementarias previamente contrastadas, "
            "no88 revisadas en esta entrega;48 equivalencias candidatas con "
            "adaptación no suman fuentes independientes."
        ),
        (
            "NASA:9 páginas textuales de§4.2/§6.2 añadidas a6 previas; no manual "
            "entero. Figuras65/67/68 ytablas212/214 requieren extracción fiel; se "
            "pueden abrir original yrender. SWE-055 solo§4.1.7 habilitado; "
            "secciones amplias con duplicación/iconos no acreditadas."
        ),
        (
            "INCOSE no incorporada por403 local en resumen gratuito yalternativa "
            "pública oficial; no se elude tienda ni Members-Only. Permiso del "
            "resumen sí permite reproducción/derivadas con atribución ycopyright "
            "completo; no confundir bloqueo técnico con prohibición legal."
        ),
        (
            "Sin índice, fingerprint efectivo, fragmentación por tokenizer, "
            "recuperación semántica, generación, examen, evaluación o voz. T077 y "
            "gates permanecen pendientes/cerrados; no hay cambio al catálogo "
            "habitual."
        ),
        (
            "Idiomas originales sin traducción. Textos revisados derivados "
            "identificados, extracciones iniciales yoriginales intactos. Uso "
            "docente local; paquete completo no autorizado para redistribución "
            "pública."
        ),
    ]
    manifest["discrepancies"][0] = (
        "Procedimiento13: título Registrar problemas, cuerpo trazabilidad;14: "
        "título Registrar trazabilidad, cuerpo problemas. Contraste integral "
        "confirma fidelidad al original. Se habilita lectura documental "
        "literal con advertencia ycontexto conjunto; sin intercambiar títulos "
        "ni aprobar doctrina."
    )
    manifest["discrepancies"].append(
        "Procedimiento8 clasifica dominio como restricciones normalmente "
        "tecnológicas; Requisitos23 vincula dominio al entorno operativo "
        "ypermite requisitos funcionales/no funcionales. Conservar taxonomías "
        "yprocedencias."
    )
    manifest["available"] = sum(d["available"] for d in manifest["documents"])
    manifest["quarantine"] = sum(d["quarantine"] for d in manifest["documents"])
    dump(NEW / "manifest-v2.json", manifest)
    dump(NEW / "coverage-v2.json", coverage)
    dump(
        NEW / "qa/review-v2.json",
        [
            {
                "passage": r["id"],
                "status": r["status"],
                "qa_state": r["qa_state"],
                "reason": r["reason"],
                "preview": r.get("preview"),
            }
            for rows in all_rows.values()
            for r in rows
        ],
    )
    dump(
        NEW / "equivalencias-v1-referencia.json",
        {
            "path": "../paquete-v1/equivalencias.json",
            "sha256": sha(OLD / "equivalencias.json"),
            "decision": "48 candidatos preservados; no nuevas evidencias independientes",
        },
    )
    print([(d["id"], d["available"], d["qa_states"]) for d in manifest["documents"]])


if __name__ == "__main__":
    main()
