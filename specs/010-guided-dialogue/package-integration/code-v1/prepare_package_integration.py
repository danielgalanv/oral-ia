"""Create an immutable, explicitly pending integration overlay; never publish or mutate source."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import unicodedata
from pathlib import Path
from oralia.domain.materials.segmenter import segment_blocks
from oralia.infrastructure.documents.extractor import get_extractor, mime_type_for_filename

STREAMS={"agua-docx":("agua","01-agua-dossier.docx"),"programa-docx":("programa","02-programa-caso.docx"),"programa-pptx":("programa","03-programa-presentacion.pptx"),"datos-pdf":("datos","04-datos-practica.pdf")}

def normal(text):return " ".join(unicodedata.normalize("NFC",text).split())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare(original:Path, output:Path):
    original=original.resolve();output=output.resolve()
    if output.exists() or output.is_relative_to(original):raise ValueError("Output must be new and outside the original package")
    manifest=json.loads((original/"manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path=(original/item["path"]).resolve()
        if not path.is_relative_to(original) or digest(path)!=item["sha256"]:raise ValueError("Original manifest mismatch")
    output.mkdir(parents=True)
    report={"schema_version":1,"status":"proposal_human_review_pending","parent":str(original),"parent_manifest_sha256":digest(original/"manifest.json"),"domains":{},"streams":{}}
    for domain in ["agua","programa","datos"]:
        pack=json.loads((original/f"{domain}-unidades.json").read_text(encoding="utf-8"));pack=copy.deepcopy(pack)
        support=[]
        for objective in pack["objectives"]:
            topic=objective["topic_ref"];prefix=f"{domain}-{topic}"
            by={u["key"]:u for u in pack["units"]}
            process=by[prefix+"-process"];comparison=by[prefix+"-comparison"];cause=by[prefix+"-cause"]
            examples=[by[prefix+"-example-1"],by[prefix+"-example-2"]]
            refs=list(process["relations_by_key"].get("rephrases",[]))
            for number,components in [(2,[comparison,process,examples[0]]),(3,[cause,process,examples[1]])]:
                text=" ".join(u["reviewed_content"] for u in components)
                if len(text)>3000:raise ValueError("Support composition exceeds published bound")
                key=prefix+f"-process-support-{number}"
                unit={"key":key,"kind":"explanation","topic_ref":topic,"subgoal_ref":topic,"reviewed_content":text,"reveal_policy":"study_only","source_key":f"{domain}-integration-support","relations_by_key":{},"integration_source":"support","derived_from":[u["key"] for u in components]}
                pack["units"].append(unit);support.append(f"## Apoyo {topic}, estrategia {number}\n\n{text}\n");refs.append(key)
            process["relations_by_key"]["rephrases"]=refs
        pack["integration_status"]="technical_test_publication_only; human_review_pending";pack["version"]=2
        (output/f"{domain}-units.json").write_text(json.dumps(pack,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (output/f"{domain}-apoyos.md").write_text(f"# Apoyos propuestos de {domain}\n\nDerivados de las unidades originales. Revisión docente pendiente.\n\n"+"\n".join(support),encoding="utf-8")
        report["domains"][domain]={"original_units":70,"technical_units_with_support":len(pack["units"]),"support_variants_added":len(support),"original_unit_file_sha256":digest(original/f"{domain}-unidades.json")}
    for stream,(domain,filename) in STREAMS.items():
        pack=json.loads((output/f"{domain}-units.json").read_text(encoding="utf-8"));primary=original/"para-cargar"/filename
        fragments=segment_blocks(get_extractor(mime_type_for_filename(filename)).extract(str(primary)))
        missing=[];paragraphs=[];seen=set()
        for u in pack["units"]:
            if u["kind"] in {"question","hint"} or u.get("integration_source")=="support":continue
            if not any(normal(u["reviewed_content"]) in normal(f.text) for f in fragments):
                missing.append(u["key"])
                if u["reviewed_content"] not in seen:
                    paragraphs.append(f"## Ampliación de {u['topic_ref']}\n\n{u['reviewed_content']}\n");seen.add(u["reviewed_content"])
        supplement=None
        if paragraphs:
            supplement=stream+"-ampliacion.md";(output/supplement).write_text("# Ampliación textual propuesta\n\nContenido de las unidades originales que no se vincula literalmente al formato principal. No atribuirlo al archivo principal; revisión docente pendiente.\n\n"+"\n".join(paragraphs),encoding="utf-8")
        report["streams"][stream]={"domain":domain,"primary":str(primary),"primary_sha256":digest(primary),"practice":str(original/f"{domain}-preguntas.md"),"practice_sha256":digest(original/f"{domain}-preguntas.md"),"support":domain+"-apoyos.md","supplement":supplement,"primary_missing_unit_keys":missing,"main_format_alone_complete":not missing,"program_formats_combined":False}
    (output/"revision.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    files={p.name:digest(p) for p in output.iterdir() if p.is_file()}
    (output/"manifest.json").write_text(json.dumps({"status":"human_review_pending","parent_manifest_sha256":report["parent_manifest_sha256"],"sha256":files},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--original",type=Path,required=True);parser.add_argument("--output",type=Path,required=True);args=parser.parse_args();result=prepare(args.original,args.output);print(json.dumps({"output":str(args.output),"streams":{k:len(v["primary_missing_unit_keys"]) for k,v in result["streams"].items()}},ensure_ascii=False))
