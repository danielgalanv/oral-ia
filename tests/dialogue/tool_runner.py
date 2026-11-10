"""Public synthetic tool conversations with real calls and non-replacing spies.

The frozen narratives are mapped to explicit UI/API operations. Text alone never
authorizes teacher tools. Tokens stay in memory and never enter the report.
"""

import copy
import hashlib
import json
import re
from pathlib import Path
from uuid import uuid4

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided
from tests.dialogue.tool_oracles import ExpectedOperation, Observation, verify_operation

FOLDER = Path(__file__).parent / "fixtures/tools"


def cases(partition):
    frozen = json.loads((FOLDER / "freeze.json").read_text(encoding="utf-8"))["sha256"]
    result = []
    for path in sorted(FOLDER.glob("S*.json")):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == frozen[path.name]
        item = json.loads(path.read_text(encoding="utf-8"))
        if item["partition"] == partition:
            result.append(item)
    return result


def run_tools(client, case, monkeypatch):
    from oralia.application.services import guided_dialogue_service as guided
    from oralia.application.services import reviewed_unit_renderer as renderer
    from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    events = []
    actor = ["teacher"]
    original_units = guided.current_units
    original_render = renderer.render_plan
    original_choose = guided.choose
    original_patch = guided.update_context
    original_interpret = StudyIntentInterpreterAgent.execute
    original_disclosure = SolutionNonDisclosureVerifierAgent.execute

    def units(db, activity):
        result = original_units(db, activity)
        events.append(
            {
                "operation": "retrieve",
                "actor": actor[0],
                "arguments": {"activity_id": activity.id},
                "result_count": len(result),
            }
        )
        events.append(
            {
                "operation": "teaching_unit_resolve",
                "actor": actor[0],
                "arguments": {"activity_id": activity.id},
                "resolution": "current scoped catalog",
                "result_count": len(result),
            }
        )
        return result

    def render(db, session, plan):
        result = original_render(db, session, plan)
        events.append(
            {
                "operation": "teaching_unit_resolve",
                "actor": actor[0],
                "arguments": {"session_id": session.id, "unit_ids": [str(ref) for ref in plan.unit_refs]},
                "observed": True,
            }
        )
        return result

    def choose(*args, **kwargs):
        result = original_choose(*args, **kwargs)
        selected = next((unit for unit in args[0] if unit.id == result.unit_id), None)
        if selected and selected.kind == "hint":
            events.append(
                {
                    "operation": "hint_select",
                    "actor": actor[0],
                    "arguments": {"unit_id": selected.id, "goal": selected.subgoal_ref},
                    "observed": True,
                }
            )
        return result

    def patch(*args, **kwargs):
        result = original_patch(*args, **kwargs)
        events.append(
            {
                "operation": "context_patch",
                "actor": actor[0],
                "arguments": {"session_id": args[1], "base_version": args[2]},
                "applied": result.applied,
            }
        )
        return result

    async def interpret(agent, request, token):
        result = await original_interpret(agent, request, token)
        events.append(
            {
                "operation": "interpret",
                "actor": actor[0],
                "arguments": {"session_id": str(request.session_id)},
                "status": result.status,
            }
        )
        return result

    async def disclosure(agent, request, token):
        result = await original_disclosure(agent, request, token)
        events.append(
            {
                "operation": "non_disclosure",
                "actor": actor[0],
                "arguments": {"session_id": str(request.session_id)},
                "status": result.status,
                "verdict": (result.output or {}).get("verdict"),
            }
        )
        return result

    monkeypatch.setattr(guided, "current_units", units)
    monkeypatch.setattr(renderer, "render_plan", render)
    monkeypatch.setattr(guided, "choose", choose)
    monkeypatch.setattr(guided, "update_context", patch)
    monkeypatch.setattr(StudyIntentInterpreterAgent, "execute", interpret)
    monkeypatch.setattr(SolutionNonDisclosureVerifierAgent, "execute", disclosure)
    prepared = prepare_guided(client, domain=case["domain"], mode=case["mode"])
    events.clear()  # Do not count preparation as a participant tool invocation.
    sid = prepared["session"]["session_id"]
    aid = prepared["activity"]["id"]
    study = case["mode"] == "self_study"
    family = case["family"]
    names = client.app.state.local_access.cookie_names
    teacher_token = client.cookies.get(names[0])
    owner_token = client.cookies.get(names[1])
    choice = {"retain": bool(case["consent_scope"]), "scope": case["consent_scope"]}
    if case["fault"] == "missing_consent_scope":
        choice = {"retain": False, "scope": []}
    observations = []
    failures = []

    def state():
        with client.__db_sessionmaker__() as db:
            row = db.get(models.Session, sid)
            preference = db.get(models.SessionPrivacyPreference, sid)
            consent = (
                db.query(models.ConsentRecord).filter_by(session_id=sid, decision="retain").one_or_none()
            )
            context = db.get(models.CognitiveState, sid)
            return {
                "turn_count": row.turn_count,
                "session_status": row.status,
                "receipt_count": db.query(models.TurnRequestReceipt).filter_by(session_id=sid).count(),
                "preference_scope": sorted(preference.scope) if preference and preference.retain else [],
                "consent_scope": sorted(consent.scope) if consent else [],
                "context_present": bool(context and context.dialogue_context),
            }

    def request(
        operation,
        method,
        path,
        *,
        role="participant",
        body=None,
        expected_status=200,
        expected_state=None,
        response_properties=None,
    ):
        saved = copy.copy(client.cookies)
        client.cookies.clear()
        token = teacher_token if role == "teacher" else owner_token
        grant = client.app.state.local_access.resolve(token)
        assert grant is not None and grant.role == role
        client.cookies.set(names[0] if role == "teacher" else names[1], token)
        actor[0] = grant.role
        before = state()
        expected = ExpectedOperation(
            operation=operation,
            actor=role,
            arguments={"method": method, "path": path, "body": body},
            expected_status=expected_status,
            expected_state=expected_state if expected_state is not None else before,
            response_properties=response_properties or {},
        )
        try:
            response = (
                client.request(method, path, json=body) if body is not None else client.request(method, path)
            )
        finally:
            client.cookies = saved
        try:
            data = response.json()
        except ValueError:
            data = {"non_json": True}
        if isinstance(data, dict):
            data = {key: value for key, value in data.items() if key not in {"access_token", "secret"}}
        observed = Observation(
            operation=operation,
            actor=grant.role,
            arguments={
                "method": response.request.method,
                "path": response.request.url.path,
                "body": json.loads(response.request.content) if response.request.content else None,
            },
            status=response.status_code,
            state=state(),
            response=data,
            observed=True,
        )
        errors = verify_operation(expected, observed)
        observations.append(
            {"expected": expected.model_dump(), "observed": observed.model_dump(), "errors": errors}
        )
        failures.extend({"operation": operation, "error": error} for error in errors)
        events.append({"operation": operation, "actor": grant.role, "status": response.status_code})
        return response, data

    def endpoint():
        return (
            f"/api/v1/sessions/{sid}/study-turns"
            if study
            else f"/api/v1/defense-sessions/{sid}/defense-turns"
        )

    def turn(text, request_id=None, expected_status=200, *, terminal=None):
        before = state()
        terminal = (
            text.strip().casefold() in {"terminar", "terminar la sesión"} if terminal is None else terminal
        )
        target = {
            **before,
            "turn_count": before["turn_count"] + 1,
            "session_status": "closed_voluntary" if terminal else "active",
            "receipt_count": (
                before["receipt_count"] + 1 if not terminal or "transcript" in choice["scope"] else 0
            ),
            "preference_scope": sorted(choice["scope"]) if terminal else before["preference_scope"],
            "consent_scope": sorted(choice["scope"]) if terminal else before["consent_scope"],
            "context_present": not terminal or "transcript" in choice["scope"],
        }
        return request(
            "dialogue",
            "POST",
            endpoint(),
            body={"text": text, "client_request_id": request_id or str(uuid4()), "closure_consent": choice},
            expected_state=target if expected_status == 200 else before,
            expected_status=expected_status,
        )

    request(
        "privacy_choice",
        "POST",
        f"/api/v1/sessions/{sid}/privacy",
        body=choice,
        expected_state={**state(), "preference_scope": sorted(choice["scope"])},
    )
    if case["fault"] == "injected_provider_timeout":
        from oralia.application.services.reviewed_unit_renderer import ReviewedUnitGenerationAdapter

        actual_provider = ReviewedUnitGenerationAdapter.render
        injected = [False]

        def timeout_once(adapter, request):
            if not injected[0]:
                injected[0] = True
                events.append(
                    {"operation": "fault_injection", "fault": "synthetic_provider_timeout", "observed": True}
                )
                raise TimeoutError("synthetic controlled provider timeout")
            return actual_provider(adapter, request)

        monkeypatch.setattr(ReviewedUnitGenerationAdapter, "render", timeout_once)
    if not study:
        turn("")
    if case["fault"] == "retrieval_empty":
        request(
            "retire_source",
            "POST",
            f"/api/v1/materials/documents/{prepared['document']['id']}/deactivate",
            role="teacher",
        )
    if case["fault"] == "unit_retired":
        unit_id = next(value for key, value in prepared["units"].items() if key.endswith("-explanation"))
        request("retire_unit", "POST", f"/api/v1/governance/teaching-units/{unit_id}/retire", role="teacher")
    if family == "S05" and case["fault"] == "wrong_recipient_or_owner":
        # Two real grants with the SAME pseudo-code still represent distinct
        # sessions. The older owner must not acquire or close the new active one.
        end = f"/api/v1/sessions/{sid}/study-end"
        request(
            "harness_old_owner_close",
            "POST",
            end,
            body={"retain": False, "scope": []},
            expected_state={
                **state(),
                "session_status": "closed_voluntary",
                "receipt_count": 0,
                "preference_scope": [],
                "consent_scope": [],
                "context_present": False,
            },
        )
        _, created = request(
            "harness_foreign_start",
            "POST",
            "/api/v1/sessions",
            body={"participant_code": "synthetic-010", "activity_configuration_id": aid},
            expected_status=201,
        )
        sid = created["session_id"]
        choice = {"retain": False, "scope": []}

    last_request = None
    last_payload = {}
    late_delete = family == "S07" and case["fault"] == "late_response_after_delete"
    delete_index = 3 if late_delete else 4
    new_session_index = 6 if late_delete else 5
    for index, step in enumerate(case["steps"]):
        if family == "S05" and case["fault"] == "wrong_recipient_or_owner":
            if index in {0, 1}:
                request(
                    "session_preflight",
                    "POST",
                    "/api/v1/sessions",
                    body={
                        "participant_code": "not-authorized" if index == 0 else "synthetic-010",
                        "activity_configuration_id": aid,
                    },
                    expected_status=409,
                )
            elif index == 2:
                request(
                    "owner_discovery",
                    "GET",
                    "/api/v1/auth/owned-session",
                    response_properties={"session": None},
                )
            elif index in {3, 4}:
                request("owner_resume", "GET", f"/api/v1/sessions/{sid}/resume", expected_status=403)
            else:
                request(
                    "foreign_close_denied",
                    "POST",
                    f"/api/v1/governance/sessions/{sid}/close",
                    body={"confirm": True, "reason": "abandoned"},
                    expected_status=403,
                )
            continue
        if family == "S05" and index == 3:
            request("owner_resume", "GET", f"/api/v1/sessions/{sid}/resume")
            continue
        if family == "S06" and index >= 4:
            negative = case["fault"] == "missing_consent_scope"
            if index == 4:
                request(
                    "review",
                    "GET",
                    f"/api/v1/governance/sessions/{sid}",
                    role="participant" if negative else "teacher",
                    expected_status=403 if negative else 200,
                )
            else:
                request(
                    "export",
                    "POST",
                    "/api/v1/governance/exports",
                    role="participant" if negative else "teacher",
                    body={"session_ids": [sid], "format": "json"},
                    expected_status=403 if negative else 200,
                )
                if negative:
                    request(
                        "export_without_scope",
                        "POST",
                        "/api/v1/governance/exports",
                        role="teacher",
                        body={"session_ids": [sid], "format": "json"},
                        expected_status=409,
                    )
            continue
        if family == "S07" and index == delete_index:
            before = state()
            request(
                "delete_content",
                "DELETE",
                f"/api/v1/sessions/{sid}/content",
                body={"confirm": True},
                expected_state={
                    **before,
                    "receipt_count": 0,
                    "preference_scope": [],
                    "consent_scope": [],
                    "context_present": False,
                },
            )
            request(
                "deleted_receipt",
                "GET",
                f"/api/v1/sessions/{sid}/requests/{last_request}",
                expected_status=404,
            )
            continue
        if late_delete and index == 4:
            request("late_replay_after_delete", "POST", endpoint(), body=last_payload, expected_status=409)
            continue
        if late_delete and index == 5:
            request(
                "export_deleted_denied",
                "POST",
                "/api/v1/governance/exports",
                role="teacher",
                body={"session_ids": [sid], "format": "json"},
                expected_status=409,
            )
            continue
        if family == "S07" and index == new_session_index:
            created_response, data = request(
                "new_session",
                "POST",
                "/api/v1/sessions",
                body={"participant_code": "synthetic-010", "activity_configuration_id": aid},
                expected_status=201,
            )
            sid = data["session_id"]
            # Public creation issues its grant normally. Resolve the token from the
            # returned Set-Cookie, never copy a pseudo-code into an auth field.
            with client.__db_sessionmaker__() as db:
                row = db.get(models.Session, sid)
                context = db.get(models.CognitiveState, sid)
                assert row.turn_count == 0 and row.status == "active"
                assert context is None or context.dialogue_context is None
            # request() restores the previous jar, so use the real response cookie.
            owner_token = created_response.cookies.get(names[1])
            assert owner_token and client.app.state.local_access.resolve(owner_token).session_id == sid
            choice = {"retain": False, "scope": []}  # Never inherit the previous session's consent.
            continue
        if family == "S08" and index in {3, 4, 5} and last_request is not None:
            if index == 3:
                request("reconcile", "POST", endpoint(), body=last_payload)
            elif index == 4:
                request(
                    "payload_conflict",
                    "POST",
                    endpoint(),
                    body={**last_payload, "text": "different synthetic payload"},
                    expected_status=409,
                )
            else:
                request(
                    "request_receipt",
                    "GET",
                    f"/api/v1/sessions/{sid}/requests/{last_request}",
                    response_properties={"status": "completed"},
                )
            continue
        if state()["session_status"] != "active":
            failures.append(
                {
                    "operation": "dialogue",
                    "error": "narrative_requires_explicit_closed_session_operation",
                    "step": index,
                }
            )
            continue
        last_request = str(uuid4())
        last_payload = {"text": step["input"], "client_request_id": last_request, "closure_consent": choice}
        # The original S03-D includes a study-mode command during a defense.
        # The contract requires a refusal with unchanged state, not enabling it.
        disabled_mode = (
            family == "S03"
            and not study
            and bool(
                re.search(
                    r"\b(repasemos|practicar|explicación guiada|exposición)\b", step["input"].casefold()
                )
            )
        )
        _, result = turn(
            step["input"],
            last_request,
            expected_status=409 if disabled_mode else 200,
            terminal=step.get("expected_terminal"),
        )
        if family == "S01":
            valid_sources = all(
                item.get("document_id") == prepared["document"]["id"]
                and item.get("document_version") == prepared["document"]["version"]
                for item in result.get("sources", [])
            )
            events.append(
                {
                    "operation": "sources",
                    "actor": "participant",
                    "valid_current_references": valid_sources,
                    "count": len(result.get("sources", [])),
                }
            )
            if not valid_sources:
                failures.append({"operation": "sources", "error": "invented_or_wrong_version"})
    if family == "S05":
        request(
            "session_preflight",
            "POST",
            "/api/v1/sessions",
            body={"participant_code": "not-authorized", "activity_configuration_id": aid},
            expected_status=409,
        )
    if family == "S08" and case["fault"] == "injected_provider_timeout" and not injected[0]:
        failures.append({"operation": "fault_injection", "error": "provider_timeout_not_exercised"})
    required = set(case["expected_properties"]["operations"])
    for event in events:
        arguments = event.get("arguments", {})
        if "activity_id" in arguments and arguments["activity_id"] != aid:
            failures.append({"operation": event["operation"], "error": "foreign_activity_argument"})
        if "unit_ids" in arguments and not set(arguments["unit_ids"]) <= set(prepared["units"].values()):
            failures.append({"operation": event["operation"], "error": "foreign_unit_argument"})
        if event["operation"] == "context_patch" and not event.get("applied"):
            failures.append({"operation": "context_patch", "error": "unapplied_patch"})
    missing = required - {event["operation"] for event in events}
    failures.extend(
        {"operation": name, "error": "required_operation_not_observed"} for name in sorted(missing)
    )
    if state()["session_status"] == "active":
        target = {
            **state(),
            "session_status": "closed_teacher_confirmed",
            "receipt_count": state()["receipt_count"] if "transcript" in choice["scope"] else 0,
            "preference_scope": sorted(choice["scope"]),
            "consent_scope": sorted(choice["scope"]),
            "context_present": state()["context_present"] and "transcript" in choice["scope"],
        }
        request(
            "harness_cleanup",
            "POST",
            f"/api/v1/governance/sessions/{sid}/close",
            role="teacher",
            body={"confirm": True, "reason": "abandoned"},
            expected_state=target,
        )
    return {
        "case_id": case["case_id"],
        "family": family,
        "partition": case["partition"],
        "domain": case["domain"],
        "mode": case["mode"],
        "seed": case["seed"],
        "profile": "guided_controlled",
        "fault_requested": case["fault"],
        "operations": events,
        "observations": observations,
        "failures": failures,
        "passed": not failures,
        "human_validation": "not_evaluated",
    }
