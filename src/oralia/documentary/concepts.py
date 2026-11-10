"""Prepare the authorised teacher package once; no GPU or conversational answers."""

import argparse
from pathlib import Path

from oralia.course_dialogue.prepared_concepts import prepare
from oralia.documentary.__main__ import CURRENT_PACKAGE, PACKAGES, confined, load_package
from oralia.infrastructure.generation.generation_port import EvidenceItem


def package_inputs(package=CURRENT_PACKAGE):
    root, manifest_name = PACKAGES[package]
    manifest, pages = load_package(root, manifest_name)
    evidence, locations, files = [], {}, {}
    for doc in manifest["documents"]:
        document_id = manifest["package_id"] + "/" + doc["id"]
        files[document_id] = confined(root, doc["original"])
        for p in pages[doc["id"]]:
            if p["status"] != "disponible":
                continue
            text = (
                f"Fuente: {doc['filename']}; página {p['page']}; {p['section']}\n"
                f"SHA256 original: {doc['sha256']}\n{p['text']}"
            )
            evidence.append(
                EvidenceItem(
                    fragment_id=p["id"],
                    document_id=document_id,
                    document_version=1 if package == "v1.1" else 2,
                    text=text,
                )
            )
            locations[p["id"]] = dict(
                document_title=doc["filename"],
                page=p["page"],
                topics=[c["label"] for c in manifest["concepts"] if p["id"] in c["passages"]],
            )
    return manifest, evidence, locations, files


def prepare_teacher_concepts(destination, *, package=CURRENT_PACKAGE):
    destination = Path(destination).resolve()
    root, _ = PACKAGES[package]
    if destination.is_relative_to(root.resolve()):
        raise ValueError("derived concepts must not be written inside original teacher package")
    manifest, evidence, locations, files = package_inputs(package)

    def revalidate():
        again, current, _, _ = package_inputs(package)
        if again != manifest or current != evidence:
            raise ValueError("teacher material changed during concept preparation")

    result = prepare(
        destination,
        evidence,
        files,
        corpus_id=manifest["package_id"],
        locations=locations,
        revalidate=revalidate,
    )
    return result


def main():
    parser = argparse.ArgumentParser(description="Preparar conceptos desde material autorizado, sin modelos")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--package", choices=PACKAGES, default="v2")
    args = parser.parse_args()
    result = prepare_teacher_concepts(args.output, package=args.package)
    pages = [p for d in result.documents.values() for p in d["pages"].values()]
    definitions = sum(bool(c["source_name"]) for p in pages for c in p["cards"])
    print(
        f"Catálogo preparado: {len(result.documents)} documentos, {len(pages)} pasajes, "
        f"{definitions} definiciones explícitas. Revisión semántica no inferida."
    )


if __name__ == "__main__":
    main()
