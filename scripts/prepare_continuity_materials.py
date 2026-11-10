"""Create a new review-pending successor, preserving every prior package byte."""

import hashlib
import json
from pathlib import Path


def prepare(parent, output):
    parent = Path(parent).resolve()
    output = Path(output).resolve()
    if output.exists() or output.is_relative_to(parent):
        raise ValueError("Use a new separate successor")
    manifest = json.loads((parent / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Parent source mismatch")
    output.mkdir()
    for path in parent.iterdir():
        if path.is_file() and path.name != "manifest.json":
            (output / path.name).write_bytes(path.read_bytes())
    specifics = {
        "evaporacion": [
            (
                "¿Estás explicando un cambio de estado o una transformación de la "
                "sustancia? ¿Qué distingue ambas ideas en tu razonamiento?"
            ),
            "¿Qué observación de la tela respalda tu explicación y qué condición necesitas precisar?",
            "¿Cómo conectarías tu argumento con la pregunta original sin suponer un resultado no observado?",
        ],
        "validacion": [
            (
                "¿Cómo distingues comprobar el formato de comprobar la regla del c"
                "aso al justificar tu respuesta?"
            ),
            (
                "¿Qué condición necesita cumplirse antes de solicitar la siguiente"
                " operación, y cómo la justificarías?"
            ),
            "¿Qué parte de tu argumento procede de la regla del caso y qué parte estás suponiendo?",
        ],
        "media": [
            (
                "¿Cómo distingues los intentos realizados de las observaciones dis"
                "ponibles al justificar el divisor?"
            ),
            "¿Qué representa el total y qué representa cada término del reparto que propones?",
            "¿Qué condición necesitas comprobar para que tu cálculo responda a la pregunta original?",
        ],
    }
    for domain in ["agua", "programa", "datos"]:
        path = output / f"{domain}-units.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        practice = []
        for objective in pack["objectives"]:
            topic = objective["topic_ref"]
            question = next(u for u in pack["units"] if u["key"] == f"{domain}-{topic}-question")
            texts = specifics.get(
                topic,
                [
                    (
                        f"En tu respuesta a «{question['reviewed_content']}», "
                        "¿qué puedes justificar con el material?"
                    ),
                    f"Para el tema {topic}, ¿qué condición has supuesto y cómo afecta a tu explicación?",
                    (
                        f"En {topic}, ¿qué parte de tu argumento necesitarías aclarar "
                        "para responder a la pregunta inicial?"
                    ),
                ],
            )
            refs = []
            for i, text in enumerate(texts, 1):
                key = f"{domain}-{topic}-question-continuity-{i}"
                refs.append(key)
                pack["units"].append(
                    {
                        "key": key,
                        "kind": "question",
                        "topic_ref": topic,
                        "subgoal_ref": topic,
                        "reviewed_content": text,
                        "reveal_policy": "question",
                        "source_key": f"{domain}-practice-support",
                        "integration_source": "practice_support",
                        "derived_from": [question["key"]],
                        "relations_by_key": {},
                    }
                )
                practice.append(f"## Seguimiento de {topic}, {i}\n\n{text}\n")
            question["relations_by_key"]["rephrases"] = refs
        additions = []
        if domain == "programa":
            additions = [
                (
                    "validacion",
                    "causal-order",
                    "explanation",
                    (
                        "Validar antes de pedir guardar evita que el programa persista una"
                        " cantidad que incumple las reglas del caso. Primero se comprueban"
                        " formato y rango. Solo cuando la validación acepta los datos se s"
                        "olicita guardarlos. Un fallo de escritura es otro problema: una c"
                        "antidad puede ser válida aunque el archivo no pueda escribirse."
                    ),
                )
            ]
        if domain == "datos":
            additions = [
                (
                    "media",
                    "causal-count",
                    "explanation",
                    (
                        "En esta práctica hay seis intentos y cinco duraciones medidas. El"
                        " intento sin medida no aporta un cero ni otra duración conocida. "
                        "El divisor de la media cuenta observaciones válidas, no intentos:"
                        " en la serie A se divide el total de treinta segundos entre cinco"
                        " valores medidos."
                    ),
                ),
                (
                    "media",
                    "count-fact",
                    "fact",
                    (
                        "El divisor usa cinco observaciones válidas de la serie A. El sext"
                        "o intento sigue sin una duración conocida y queda fuera del repar"
                        "to. El número de intentos y el número de medidas disponibles son "
                        "conceptos distintos."
                    ),
                ),
            ]
        supports = []
        for topic, suffix, kind, text in additions:
            key = f"{domain}-{topic}-{suffix}"
            pack["units"].append(
                {
                    "key": key,
                    "kind": kind,
                    "topic_ref": topic,
                    "subgoal_ref": topic,
                    "reviewed_content": text,
                    "reveal_policy": "study_only",
                    "source_key": f"{domain}-integration-support",
                    "integration_source": "support",
                    "relations_by_key": {},
                    "derived_from": [f"{domain}-{topic}-process"],
                }
            )
            base = next(u for u in pack["units"] if u["key"] == f"{domain}-{topic}-explanation")
            base["relations_by_key"].setdefault("next", []).append(key)
            supports.append(f"## Continuidad {topic}, {suffix}\n\n{text}\n")
        pack["version"] = 4
        pack["integration_status"] = "proposal_human_review_pending; continuity successor"
        path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name, texts in [(f"{domain}-preguntas-apoyo.md", practice), (f"{domain}-apoyos.md", supports)]:
            with (output / name).open("a", encoding="utf-8") as f:
                f.write("\n\n# Continuidad propuesta, revisión humana pendiente\n\n" + "\n".join(texts))
    revision = json.loads((output / "revision.json").read_text(encoding="utf-8"))
    revision["continuity_parent_manifest_sha256"] = hashlib.sha256(
        (parent / "manifest.json").read_bytes()
    ).hexdigest()
    revision["continuity_status"] = "proposal; not human approved"
    (output / "revision.json").write_text(
        json.dumps(revision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output / "manifest.json").write_text(
        json.dumps(
            {
                "status": "human_review_pending",
                "parent_manifest_sha256": revision["continuity_parent_manifest_sha256"],
                "sha256": files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return files


def extend_atoms(parent, output):
    """Separate two reviewed-source purposes; keep all parent evidence immutable."""
    parent, output = Path(parent).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(parent):
        raise ValueError("Use a new separate successor")
    original = json.loads((parent / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in original["sha256"].items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Parent source mismatch")
    output.mkdir()
    for path in parent.iterdir():
        if path.is_file() and path.name != "manifest.json":
            (output / path.name).write_bytes(path.read_bytes())
    additions = [
        (
            "agua",
            "evaporacion",
            "molecular-fact",
            "fact",
            "La molécula sigue siendo agua; el cambio de estado no separa hidrógeno y oxígeno.",
        ),
        (
            "programa",
            "validacion",
            "functional-definition",
            "explanation",
            "Validar es comprobar que un dato cumple las reglas del caso antes de utilizarlo. "
            "En Registro Local se comprueba el formato admitido y el rango de la cantidad. "
            "Guardar escribe el registro; validar decide si la cantidad satisface esas reglas.",
        ),
    ]
    for domain, topic, suffix, kind, content in additions:
        path = output / f"{domain}-units.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        base = next(u for u in pack["units"] if u["key"] == f"{domain}-{topic}-explanation")
        key = f"{domain}-{topic}-{suffix}"
        unit = {
            "key": key,
            "kind": kind,
            "topic_ref": topic,
            "subgoal_ref": topic,
            "reviewed_content": content,
            "reveal_policy": "study_only",
            "source_key": base["source_key"],
            "relations_by_key": {},
            "derived_from": [base["key"]],
        }
        if domain == "programa":
            unit.update(source_key="programa-integration-support", integration_source="support")
            base["relations_by_key"]["didactic_definition"].insert(0, key)
            with (output / "programa-apoyos.md").open("a", encoding="utf-8") as handle:
                handle.write(
                    "\n\n## Definición funcional propuesta, revisión humana pendiente\n\n" + content + "\n"
                )
        else:
            base["relations_by_key"].setdefault("next", []).append(key)
        pack["units"].append(unit)
        pack["version"] = 5
        path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    revision_path = output / "revision.json"
    revision = json.loads(revision_path.read_text(encoding="utf-8"))
    parent_hash = hashlib.sha256((parent / "manifest.json").read_bytes()).hexdigest()
    revision["atomic_parent_manifest_sha256"] = parent_hash
    revision["atomic_status"] = "proposal; human review pending"
    revision_path.write_text(json.dumps(revision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output / "manifest.json").write_text(
        json.dumps(
            {"status": "human_review_pending", "parent_manifest_sha256": parent_hash, "sha256": files},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return files


def extend_contextual(parent, output):
    """Add explicit decimal material in a new proposal, never overwrite a package."""
    parent, output = Path(parent).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(parent):
        raise ValueError("Use a new separate successor")
    manifest = json.loads((parent / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Parent source mismatch")
    output.mkdir()
    for path in parent.iterdir():
        if path.is_file() and path.name != "manifest.json":
            (output / path.name).write_bytes(path.read_bytes())
    path = output / "programa-units.json"
    pack = json.loads(path.read_text(encoding="utf-8"))
    base = next(u for u in pack["units"] if u["key"] == "programa-validacion-explanation")
    proposals = [
        (
            "decimal-fact",
            "fact",
            (
                "Una entrada con separador decimal no cumple el formato de cantida"
                "d entera de Registro Local. Comprobar que una cantidad es menor q"
                "ue mil no sustituye la comprobación previa de sus caracteres."
            ),
        ),
        (
            "decimal-process",
            "explanation",
            (
                "Para una entrada con separador decimal, primero comprueba que el "
                "texto no esté vacío. Después revisa sus caracteres. La coma no es"
                " uno de los dígitos admitidos, por lo que se rechaza el formato e"
                "n ese paso. No se convierte a entero, no se comprueba el rango y "
                "no se pide guardar."
            ),
        ),
    ]
    for suffix, kind, content in proposals:
        key = "programa-validacion-" + suffix
        pack["units"].append(
            {
                "key": key,
                "kind": kind,
                "topic_ref": "validacion",
                "subgoal_ref": "validacion",
                "reviewed_content": content,
                "reveal_policy": "study_only",
                "source_key": "programa-integration-support",
                "integration_source": "support",
                "relations_by_key": {},
            }
        )
        base["relations_by_key"].setdefault("next", []).append(key)
        with (output / "programa-apoyos.md").open("a", encoding="utf-8") as f:
            f.write("\n\n## Decimal propuesto, revisión humana pendiente\n\n" + content + "\n")
    pack["version"] = 6
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    parent_hash = hashlib.sha256((parent / "manifest.json").read_bytes()).hexdigest()
    revision_path = output / "revision.json"
    revision = json.loads(revision_path.read_text(encoding="utf-8"))
    revision["contextual_parent_manifest_sha256"] = parent_hash
    revision["contextual_status"] = "proposal; human review pending"
    revision_path.write_text(json.dumps(revision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output / "manifest.json").write_text(
        json.dumps(
            {"status": "human_review_pending", "parent_manifest_sha256": parent_hash, "sha256": files},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return files


def extend_sequence(parent, output):
    """Publish a separate review-pending proposal of explicit object relations."""
    parent, output = Path(parent).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(parent):
        raise ValueError("Use a new separate successor")
    manifest = json.loads((parent / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Parent source mismatch")
    output.mkdir()
    for path in parent.iterdir():
        if path.is_file() and path.name != "manifest.json":
            (output / path.name).write_bytes(path.read_bytes())
    for domain in ["programa", "datos"]:
        path = output / f"{domain}-units.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        by_key = {u["key"]: u for u in pack["units"]}
        topic = "validacion" if domain == "programa" else "media"
        base = by_key[f"{domain}-{topic}-explanation"]
        support_texts = []

        def add(
            suffix,
            kind="explanation",
            *,
            copied=None,
            content=None,
            domain=domain,
            topic=topic,
            by_key=by_key,
            support_texts=support_texts,
            pack=pack,
        ):
            key = f"{domain}-{topic}-{suffix}"
            if copied:
                unit = {**by_key[copied], "derived_from": [copied]}
            else:
                unit = {
                    "source_key": f"{domain}-integration-support",
                    "integration_source": "support",
                    "reviewed_content": content,
                }
                support_texts.append(content)
            unit.update(
                key=key,
                kind=kind,
                topic_ref=topic,
                subgoal_ref=topic,
                reveal_policy="study_only",
                relations_by_key={},
            )
            pack["units"].append(unit)
            by_key[key] = unit
            return unit

        if domain == "programa":
            acceptance = add(
                "acceptance-boundary",
                "comparison",
                content=(
                    "Introducir una cantidad solo aporta el texto de entrada. Para "
                    "aceptarla se comprueba el formato y después el rango del caso. "
                    "Haber podido escribir el texto no demuestra que cumpla ambas "
                    "comprobaciones."
                ),
            )
            definition = by_key[base["relations_by_key"]["didactic_definition"][0]]
            definition["relations_by_key"].setdefault("comparisons", []).append(acceptance["key"])
            bridge = add("storage-boundary", "comparison", copied="programa-almacenamiento-alternative")
            cause = add("storage-failure", copied="programa-almacenamiento-cause")
            process = add("storage-report-process", copied="programa-almacenamiento-process")
            base["relations_by_key"]["comparisons"].insert(0, bridge["key"])
            bridge["relations_by_key"].update(next=[cause["key"]], rephrases=[cause["key"]])
            cause["relations_by_key"].update(next=[process["key"]], rephrases=[process["key"]])
        else:
            cause = add("missing-zero-cause", copied="datos-ausentes-cause")
            alternative = add(
                "missing-zero-alternative",
                content=(
                    "Una casilla sin duración conocida no indica que el proceso "
                    "durase cero segundos. Sabemos cuántas veces se intentó y cuántas "
                    "duraciones se midieron; no conocemos la duración de la casilla "
                    "vacía. Mantenerla como ausente deja visible esa diferencia."
                ),
            )
            process = add("missing-zero-process", copied="datos-ausentes-process")
            definition = add(
                "rephrased-definition",
                content=(
                    "La media puede entenderse como un reparto uniforme del total de "
                    "duración entre las observaciones válidas. No cuenta intentos "
                    "sin medida como si aportaran una duración. La suma responde "
                    "cuánto tiempo se acumuló; la media expresa el total por "
                    "observación válida."
                ),
            )
            by_key["datos-media-definition"]["relations_by_key"]["rephrases"] = [definition["key"]]
            for key in ["datos-media-causal-count", "datos-media-count-fact"]:
                by_key[key]["relations_by_key"].update(
                    didactic_cause=[cause["key"]], didactic_process=[process["key"]]
                )
            cause["relations_by_key"].update(
                rephrases=[alternative["key"]], didactic_process=[process["key"]]
            )
            alternative["relations_by_key"].update(
                rephrases=[process["key"]], didactic_process=[process["key"]]
            )
        pack["version"] = 7
        pack["sequence_status"] = "proposal; human review pending"
        path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with (output / f"{domain}-apoyos.md").open("a", encoding="utf-8") as f:
            f.write(
                "\n\n# Continuaciones propuestas, revisión humana pendiente\n\n"
                + "\n\n".join(support_texts)
                + "\n"
            )
    parent_hash = hashlib.sha256((parent / "manifest.json").read_bytes()).hexdigest()
    path = output / "revision.json"
    revision = json.loads(path.read_text(encoding="utf-8"))
    revision["sequence_parent_manifest_sha256"] = parent_hash
    revision["sequence_status"] = "proposal; human review pending"
    path.write_text(json.dumps(revision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output / "manifest.json").write_text(
        json.dumps(
            {"status": "human_review_pending", "parent_manifest_sha256": parent_hash, "sha256": files},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return files


def fix_source_aliases(parent, output):
    """Preserve the actual supplementary provenance of derived teaching units."""
    parent, output = Path(parent).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(parent):
        raise ValueError("Use a new separate successor")
    manifest = json.loads((parent / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Parent source mismatch")
    output.mkdir()
    for path in parent.iterdir():
        if path.is_file() and path.name != "manifest.json":
            (output / path.name).write_bytes(path.read_bytes())
    path = output / "revision.json"
    revision = json.loads(path.read_text(encoding="utf-8"))
    repairs = []
    for stream, config in revision["streams"].items():
        pack = json.loads((output / (config["domain"] + "-units.json")).read_text(encoding="utf-8"))
        missing = set(config["primary_missing_unit_keys"])
        for _ in range(len(pack["units"])):
            changed = False
            for unit in pack["units"]:
                if unit["key"] in missing or unit.get("integration_source"):
                    continue
                parents = [key for key in unit.get("derived_from", []) if key in missing]
                if parents:
                    missing.add(unit["key"])
                    repairs.append(
                        {
                            "stream": stream,
                            "key": unit["key"],
                            "derived_from": parents,
                            "source_role": "supplement",
                        }
                    )
                    changed = True
            if not changed:
                break
        config["primary_missing_unit_keys"] = sorted(missing)
        support = any(
            u.get("integration_source") == "support" and u["kind"] not in {"question", "hint"}
            for u in pack["units"]
        )
        config["main_format_alone_complete"] = not missing and not support
        revision["domains"][config["domain"]]["technical_units_with_support"] = len(pack["units"])
    parent_hash = hashlib.sha256((parent / "manifest.json").read_bytes()).hexdigest()
    revision["source_alias_parent_manifest_sha256"] = parent_hash
    revision["source_alias_repairs"] = repairs
    revision["source_alias_status"] = "proposal; human review pending; literal API witnesses required"
    path.write_text(json.dumps(revision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
    (output / "manifest.json").write_text(
        json.dumps(
            {"status": "human_review_pending", "parent_manifest_sha256": parent_hash, "sha256": files},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode", choices=["continuity", "atoms", "contextual", "sequence", "aliases"], default="continuity"
    )
    parser.add_argument("--parent", default="materiales/docente/integracion-controlada-20261020-v3")
    parser.add_argument("--output", default="materiales/docente/integracion-controlada-20261020-v4")
    arguments = parser.parse_args()
    operation = {
        "atoms": extend_atoms,
        "contextual": extend_contextual,
        "sequence": extend_sequence,
        "aliases": fix_source_aliases,
        "continuity": prepare,
    }[arguments.mode]
    result = operation(arguments.parent, arguments.output)
    print("New successor files:", len(result))
