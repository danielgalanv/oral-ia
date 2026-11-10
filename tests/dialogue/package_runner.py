"""Full uncut synthetic conversations via the owned public API; no favorable outputs."""

from __future__ import annotations

import json

from oralia.domain.dialogue.interpretation import normalized
from oralia.infrastructure.db import models
from tests.dialogue.package_fixture import start_package_session


def run_conversation(client, prepared, case, target):
    if target.exists():
        raise ValueError("Use a new output directory; preserve every first result")
    session = start_package_session(client, prepared, case["mode"])
    sid = session["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    report = {
        "case": case,
        "session_id": sid,
        "observations": [],
        "violations": [],
        "human_review": "pending",
        "audio_real": False,
        "teaching_material_review": "proposal_only",
    }
    target.parent.mkdir(parents=True, exist_ok=True)

    def save():
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def require(condition, message, step):
        if not condition:
            report["violations"].append({"step": step, "criterion": message})

    supports = []
    pending = None
    closed = False
    confirmed_privacy = False
    try:
        for step, text in enumerate(case["steps"], 1):
            response = client.post(endpoint, json={"text": text})
            body = response.json()
            status = body.get("dialogue_status", {})
            refs = status.get("rendered_unit_ids", [])
            observation = {
                "step": step,
                "input": text,
                "http_status": response.status_code,
                "response": body,
                "selected_units": [prepared["published"].get(ref) for ref in refs],
                "source_witnesses": [
                    prepared["witnesses"][key] for key, ref in prepared["units"].items() if ref in refs
                ],
            }
            report["observations"].append(observation)
            save()
            require(response.status_code == 200, "HTTP request accepted without bypass", step)
            if response.status_code != 200:
                report["outcome"] = "http_failed"
                break
            output = body.get("output_text") or ""
            require(bool(output), "understandable published output", step)
            value = normalized(text)
            with client.__db_sessionmaker__() as db:
                row = db.get(models.Session, sid)
                state = db.get(models.CognitiveState, sid)
                context = state.dialogue_context if state and state.dialogue_context else {}
                pref = db.get(models.SessionPrivacyPreference, sid)
                observation["state"] = {
                    "status": row.status,
                    "turn_count": row.turn_count,
                    "current_topic": context.get("current_topic_ref"),
                    "pending_topic": context.get("pending_topic_ref"),
                    "pending_question_unit_id": context.get("pending_question_unit_id"),
                    "support_step": context.get("support_step"),
                    "privacy": {"retain": bool(pref and pref.retain), "scope": pref.scope if pref else []},
                }
                if refs:
                    require(
                        all(ref in prepared["published"] for ref in refs),
                        "owned teaching unit reference",
                        step,
                    )
                    require(
                        status.get("grounding_verdict") == "fundamentada"
                        and status.get("coherence_verdict") == "approved",
                        "independent academic verification",
                        step,
                    )
                    for ref in refs:
                        unit = db.get(models.TeachingUnit, ref)
                        for source in unit.source_refs:
                            fragment = db.get(models.MaterialFragment, source["fragment_id"])
                            document = db.get(models.MaterialDocument, source["document_id"])
                            require(
                                fragment is not None
                                and document.status == "active"
                                and document.retired_at is None
                                and fragment.document_id == document.id
                                and fragment.document_version == source["document_version"],
                                "current real source binding",
                                step,
                            )
                    if case["mode"] == "oral_defense":
                        require(
                            all(prepared["published"][ref]["kind"] in {"question", "hint"} for ref in refs),
                            "protected defense never emits study answer",
                            step,
                        )
                        require(
                            status.get("non_disclosure_verdict") == "approved",
                            "independent non-disclosure approval",
                            step,
                        )
                if case["mode"] == "oral_defense" and not closed:
                    current = context.get("pending_question_unit_id")
                    if value == "confirmo":
                        pending = current
                    elif pending and current:
                        require(current == pending, "pending question preserved until confirmed change", step)
                    if current and not pending:
                        pending = current
            if value.startswith(("hola", "buenas tardes")):
                require("hola" in normalized(output), "respond to greeting", step)
            if case["mode"] == "self_study":
                if value in {
                    "no lo entiendo",
                    "explicalo de otra forma",
                    "sigo sin entenderlo",
                    "necesito otra explicacion",
                }:
                    supports.append(output)
                    require(bool(refs), "a reviewed support, not a generic alert", step)
                if "precio" in value or "otros planetas" in value:
                    require(
                        not refs
                        and any(word in normalized(output) for word in ["fuentes", "material", "disponible"]),
                        "outside-source request gets honest limit",
                        step,
                    )
                if any(
                    value.startswith(prefix)
                    for prefix in [
                        "que significa",
                        "¿que significa",
                        "¿por que ocurre",
                        "¿como sucede",
                        "¿cual es la definicion",
                        "define ",
                    ]
                ):
                    require(bool(refs), "answer academic purpose with reviewed content", step)
            if "de donde" in value:
                require(
                    "sección" in output
                    and all(d["id"] not in output for d in prepared["documents"].values()),
                    "spoken provenance rather than UUID/screen",
                    step,
                )
            if value.startswith("confirmo ") and "conservar" in value:
                confirmed_privacy = True
                view = client.get(f"/api/v1/sessions/{sid}/privacy").json()
                require(view["retain"] == case["retain"], "confirmed retention has real state", step)
            if value == "confirmo cerrar":
                closed = True
                require(
                    body.get("session_status") == "closed_voluntary" and confirmed_privacy,
                    "confirmed closure after explicit conservation",
                    step,
                )
            if value == "revisar intervencion 1":
                if any(o["input"].startswith("confirmo eliminar") for o in report["observations"]):
                    require("No hay una transcripción" in output, "deleted content never resurrected", step)
                else:
                    require(
                        ("Registro histórico propio" in output) == case["retain"],
                        "closed review matches actual retention",
                        step,
                    )
            if value.startswith("confirmo eliminar"):
                require(body.get("deleted") is True, "explicit erasure has real effect", step)
                transcript = client.get(f"/api/v1/sessions/{sid}/transcript").json()
                require(
                    not transcript["turns"] and not transcript["transcripts"], "real transcript erased", step
                )
            save()
        if case["mode"] == "self_study":
            require(
                len(supports) == 3 and len(set(supports)) == 3, "three distinct contextual explanations", 0
            )
        require(len(report["observations"]) == len(case["steps"]), "complete uncut conversation", 0)
        report["outcome"] = "passed" if not report["violations"] else "failed"
        save()
        return report
    finally:
        client.post(f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"})
