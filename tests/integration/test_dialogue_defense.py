"""Public defense controls preserve the pending reviewed question without answers."""

from tests.dialogue.api_fixture import checked, prepare_guided


def test_historical_defense_help_repeat_rephrase_does_not_reveal_solution(app_client):
    fixture = prepare_guided(app_client, mode="oral_defense")
    sid = fixture["session"]["session_id"]
    endpoint = f"/api/v1/defense-sessions/{sid}/defense-turns"
    initial = checked(app_client.post(endpoint, json={"text": ""}))
    outputs = []
    for text in [
        "a los 99 grados",
        "no sé justificarlo",
        "y ahora?",
        "puedes repetir?",
        "no entiendo, dilo de otra forma",
    ]:
        result = checked(app_client.post(endpoint, json={"text": text}))
        assert result["output_text"] and not result["blocked"], result
        assert "100" not in result["output_text"]
        assert all(not source.get("fragment_text") for source in result["sources"])
        outputs.append(result)
    assert outputs[3]["output_text"] == initial["output_text"]
    assert outputs[4]["output_text"] != outputs[3]["output_text"]
    assert outputs[1]["dialogue_status"]["support_step"] >= 1
    assert (
        checked(
            app_client.post(
                f"/api/v1/defense-sessions/{sid}/defense-end", json={"retain": False, "scope": []}
            )
        )["status"]
        == "closed_voluntary"
    )
