"""Plan pending draft inputs for the existing teacher API, without writing or publishing.

Binding IDs requires a separate authenticated preparation and current DB source
checks. This helper supplies no authority, reviewed flag, session or T090 receipt.
"""

from oralia.application.services.teaching_unit_service import TeachingUnitInput


def draft_graph(packet):
    if packet["human_review"] != "pending" or packet["participant_publication"] is not False:
        raise ValueError("only pending, unpublished draft packets are supported")
    graph = {}
    declared_relations = packet.get("relations", [])
    registered = {
        r[key]
        for r in declared_relations
        for key in ["definition_ref", "rephrase_ref", "example_ref", "question_ref"]
    }
    for goal in packet["goals"]:
        units = [u for u in packet["units"] if u["goal"] == goal["id"]]
        roles = {u["role"]: u for u in units}
        if len(roles) != len(units):
            raise ValueError("duplicate role within goal")
        required = {
            "definition",
            "cause",
            "process",
            "rephrase",
            "example",
            "comparison",
            "question",
            "hint1",
            "hint2",
            "hint3",
            "correction",
        }
        if not required <= set(roles) or any(
            u["id"] not in registered for u in units if u["role"] not in required
        ):
            raise ValueError("draft goal has incomplete roles")
        for unit in units:
            if unit["review_status"] != "pending" or unit["id"] in graph:
                raise ValueError("draft status or identity invalid")
            relations = {}
            if unit["role"] == "question":
                relations = {"hints": [roles[f"hint{i}"]["id"] for i in range(1, 4)]}
                feedback = unit.get("feedback_ref")
                if feedback is not None:
                    related = next(
                        (
                            u
                            for u in units
                            if u["id"] == feedback and u["role"] in {"comparison", "correction"}
                        ),
                        None,
                    )
                    if related is None:
                        raise ValueError("question feedback outside goal")
                    relations["comparisons"] = [feedback]
            elif unit["role"] == "definition":
                relations = {
                    name: [roles[role]["id"]]
                    for name, role in {
                        "didactic_cause": "cause",
                        "didactic_process": "process",
                        "rephrases": "rephrase",
                        "examples": "example",
                        "comparisons": "comparison",
                        "next": "question",
                    }.items()
                }
            for relation in declared_relations:
                if unit["id"] == relation["definition_ref"]:
                    secondary = next(
                        u
                        for u in packet["units"]
                        if u["goal"] == relation["secondary_goal"] and u["role"] == "definition"
                    )
                    relations_for_unit = {
                        "comparisons": [secondary["id"]],
                        "rephrases": [relation["rephrase_ref"]],
                        "examples": [relation["example_ref"]],
                    }
                    for name, refs in relations_for_unit.items():
                        if unit["id"] in refs:
                            raise ValueError("self-referential teaching relation")
                        relations[name] = refs
            graph[unit["id"]] = {"unit": unit, "relations_by_key": relations}
    if len(graph) != len(packet["units"]):
        raise ValueError("unit outside known goal")
    return graph


def next_draft_input(graph, created_ids, course_id, activity_id, source_bindings):
    """Return the next dependency-ready input; caller records IDs from API responses.

    No API call or publication happens here. Missing bindings fail before a first
    request can be built; normal teacher service must still revalidate every input.
    """
    needed = {ref["source_id"] for item in graph.values() for ref in item["unit"]["source_refs"]}
    if needed - set(source_bindings):
        raise ValueError("missing source binding")
    if set(created_ids) - set(graph):
        raise ValueError("unknown created draft key")
    remaining = [(key, item) for key, item in graph.items() if key not in created_ids]
    if not remaining:
        return None
    for key, item in remaining:
        relations = item["relations_by_key"]
        if any(ref not in created_ids for refs in relations.values() for ref in refs):
            continue
        unit = item["unit"]
        refs = []
        for source in unit["source_refs"]:
            ref = source_bindings[source["source_id"]]
            if ref not in refs:
                refs.append(ref)
        data = TeachingUnitInput(
            course_id=course_id,
            kind=unit["kind"],
            topic_ref=unit["goal"],
            subgoal_ref=unit["goal"],
            reviewed_content=unit["draft_content"],
            source_refs=refs,
            activity_refs=[activity_id],
            reveal_policy=unit["reveal_policy"],
            relations={name: [created_ids[ref] for ref in keys] for name, keys in relations.items()},
        )
        return key, data
    raise ValueError("cyclic or unresolved draft relations")
