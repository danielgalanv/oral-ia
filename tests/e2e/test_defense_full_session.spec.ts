import { test, expect } from "./local_auth";
import { readFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import path from "node:path";
import { execFileSync } from "node:child_process";

for (const closeKind of ["voluntary", "turns", "duration"] as const) {
  test(`real HTTP defense ${closeKind}: selection before exact limit, full review, selective retention and purge`, async ({
    page,
    request,
  }) => {
    const participant = `def-${randomUUID()}`;
    const course = "30000000-0000-0000-0000-000000000001";
    const created = await request.post(
      "http://127.0.0.1:8005/api/v1/activities",
      {
        data: {
          course_id: course,
          name: "Defensa HTTP",
          subject: "Documento",
          objective: "Explicar el documento de prueba",
          mode: "oral_defense",
          language: "es",
          max_turns: closeKind === "turns" ? 2 : 10,
          max_duration_seconds: closeKind === "duration" ? 2 : 900,
          retention_policy_id: "30000000-0000-0000-0000-000000000002",
          output_authorization_policy: {
            schema_version: 1,
            policy_id: randomUUID(),
            policy_version: 1,
            allowed_recipients: [participant],
            allowed_disclosures: [
              {
                category: "generated_defense",
                provenance: "defense-agency",
                recipient: participant,
              },
              {
                category: "defense_summary",
                provenance: "persisted_session_facts",
                recipient: participant,
              },
            ],
            allowed_scopes: {
              topics: ["activity"],
              purposes: [
                "oral_defense",
                "missing_information",
                "clarify_response",
                "oral_defense_close",
                "oral_defense_summary",
              ],
              actions: [
                "ask",
                "clarify",
                "acknowledge_missing_info",
                "finish",
                "respond",
              ],
            },
            general_knowledge_allowed: false,
            allowed_templates: [
              "defense-initial-question",
              "defense-dynamic-output",
              "defense-missing-information",
              "defense-clarification",
              "defense-limit-close",
              "defense-summary",
            ].map((id) => [id, 1]),
            allowed_operational_messages: [],
          },
        },
      },
    );
    expect(created.ok(), await created.text()).toBeTruthy();
    const activity = await created.json();
    await expect
      .poll(async () =>
        (
          await request.get(
            `http://127.0.0.1:8005/api/v1/activities/${activity.id}`,
          )
        ).status(),
      )
      .toBe(200);
    const config = await request.post(
      `http://127.0.0.1:8005/api/v1/tecnica/activities/${activity.id}/defense-config`,
      {
        data: {
          initial_questions: ["Explica el documento de prueba."],
          summary_authorized: true,
          transcript_retention_authorized: true,
        },
      },
    );
    expect(config.status(), await config.text()).toBe(201);
    const sample = await readFile(
      path.resolve(__dirname, "../fixtures/materials/sample.docx"),
    );
    let uploaded = await request.post(
      "http://127.0.0.1:8005/api/v1/materials/documents",
      {
        multipart: {
          course_id: course,
          activity_configuration_ids: activity.id,
          file: {
            name: "defense.docx",
            mimeType:
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            buffer: Buffer.concat([sample, Buffer.from(activity.id)]),
          },
        },
      },
    );
    if (uploaded.status() === 409) {
      const conflict = await uploaded.json();
      uploaded = await request.post(
        `http://127.0.0.1:8005/api/v1/materials/documents/${conflict.conflict_token}/duplicate-resolution`,
        { data: { resolution: "proceed_new" } },
      );
    }
    expect(uploaded.ok(), await uploaded.text()).toBeTruthy();
    const document = await uploaded.json();
    await expect
      .poll(async () =>
        (
          await request.get(
            `http://127.0.0.1:8005/api/v1/materials/documents/${document.id}`,
          )
        ).status(),
      )
      .toBe(200);
    expect(
      (
        await request.post(
          `http://127.0.0.1:8005/api/v1/materials/documents/${document.id}/activate`,
        )
      ).ok(),
    ).toBeTruthy();
    await page.goto("/defensa");
    await page.getByLabel("Código seudónimo").fill(participant);
    await page.getByLabel("Actividad", { exact: true }).fill(activity.id);
    const startResponse = page.waitForResponse(
      (response) =>
        response.url().endsWith("/api/v1/sessions") &&
        response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Iniciar defensa" }).click();
    const session = await (await startResponse).json();
    await expect(
      page.getByText("Explica el documento de prueba.", { exact: true }),
    ).toBeVisible();
    const retainedScope = closeKind === "turns" ? "transcript" : "summary";
    await page
      .getByLabel(
        retainedScope === "transcript"
          ? "Conservar transcripción"
          : "Conservar resumen",
      )
      .check();
    await page
      .getByRole("button", { name: "Revisar transcripción completa" })
      .click();
    await expect(
      page.getByRole("region", { name: "Transcripción completa de la sesión" }),
    ).toContainText("Explica el documento de prueba.");
    if (closeKind === "duration") await page.waitForTimeout(2100);
    await page
      .getByLabel("Tu respuesta")
      .fill("Este parrafo contiene texto real de prueba para ORAL-IA.");
    const answered = page.waitForResponse(
      (response) =>
        response
          .url()
          .endsWith(`/defense-sessions/${session.session_id}/defense-turns`) &&
        response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Enviar" }).click();
    const answer = await (await answered).json();
    expect(answer.dialogue_action).toBe(
      closeKind === "voluntary" ? "ask" : "finish",
    );
    if (closeKind === "voluntary") {
      expect(answer.sources.length).toBeGreaterThan(0);
      await page.getByRole("button", { name: "Finalizar sesión" }).click();
      await expect(
        page.getByRole("region", {
          name: "Transcripción completa de la sesión",
        }),
      ).toContainText("Este parrafo contiene texto real");
      await page
        .getByRole("button", { name: "Confirmar cierre de sesión" })
        .click();
    }
    await expect(page.getByRole("status")).toContainText(
      closeKind === "voluntary" ? "closed_voluntary" : "closed_limit_reached",
    );
    await expect(page.getByLabel("Resumen descriptivo")).toContainText(
      "turn_count",
    );
    await expect(page.locator("audio")).toHaveCount(0);
    const retained = await (
      await page.request.get(
        `http://127.0.0.1:8005/api/v1/defense-sessions/${session.session_id}/defense-transcript`,
      )
    ).json();
    expect(retained.turns.length > 0).toBe(retainedScope === "transcript");
    const trace = await request.get(
      `http://127.0.0.1:8005/api/v1/tecnica/defense-sessions/${session.session_id}/defense-trace`,
    );
    expect(trace.ok()).toBeTruthy();
    const traceBody = await trace.text();
    expect(traceBody).toContain("consent_recorded");
    expect(traceBody.includes('"defense_session_summary"')).toBe(
      retainedScope === "summary",
    );
    expect(traceBody).toContain(retainedScope);
    const beforeDuplicate = traceBody;

    const duplicate = await page.request.post(
      `http://127.0.0.1:8005/api/v1/defense-sessions/${session.session_id}/defense-end`,
    );
    expect((await duplicate.json()).defense_summary).toBeNull();
    expect(
      await (
        await request.get(
          `http://127.0.0.1:8005/api/v1/tecnica/defense-sessions/${session.session_id}/defense-trace`,
        )
      ).text(),
    ).toBe(beforeDuplicate);
    // Only the isolated E2E database: advance expiry without production clocks or sleeps.
    execFileSync(
      "uv",
      [
        "run",
        "--no-sync",
        "python",
        "-c",
        "import sqlite3,sys; from datetime import datetime,timedelta,timezone; db=sqlite3.connect('file:.e2e_governance.db?mode=rw', uri=True); db.execute('UPDATE session SET ended_at=? WHERE id=?', ((datetime.now(timezone.utc)-timedelta(days=31)).replace(tzinfo=None).isoformat(sep=' '),sys.argv[1])); db.commit(); db.close()",
        session.session_id,
      ],
      { cwd: path.resolve(__dirname, "../..") },
    );
    const purge = await request.post(
      "http://127.0.0.1:8005/api/v1/tecnica/defense/purge-expired",
    );
    expect(purge.ok(), await purge.text()).toBeTruthy();
    expect((await purge.json()).sessions_with_rows_deleted).toBeGreaterThan(0);
    expect(
      await (
        await page.request.get(
          `http://127.0.0.1:8005/api/v1/defense-sessions/${session.session_id}/defense-transcript`,
        )
      ).json(),
    ).toEqual({ turns: [], transcripts: [] });
  });
}
