import { test, expect } from "./local_auth";

// Escenario A (quickstart.md): sesión válida de extremo a extremo — inicio, un turno,
// finalización voluntaria, y verificación en el área técnica de que todo quedó
// registrado. The Playwright configuration owns the isolated local services.

test("Escenario A — sesión completa de participante", async ({
  page,
  request,
}) => {
  const seedResponse = await request.post(
    "http://127.0.0.1:8005/api/v1/activities",
    {
      data: {
        course_id: "30000000-0000-0000-0000-000000000001",
        name: "Actividad E2E",
        subject: "Demo",
        objective: "Probar el flujo end-to-end",
        mode: "texto",
        language: "es",
        max_turns: 10,
        max_duration_seconds: 900,
        retention_policy_id: "30000000-0000-0000-0000-000000000002",
        output_authorization_policy: {
          schema_version: 1,
          policy_id: "e2e-core",
          policy_version: 1,
          allowed_recipients: ["part-e2e001"],
          allowed_disclosures: [
            {
              category: "public_activity",
              provenance: "trusted_template",
              recipient: "part-e2e001",
            },
          ],
          allowed_scopes: {
            topics: ["activity"],
            purposes: ["acknowledge_turn"],
            actions: ["continue"],
          },
          general_knowledge_allowed: false,
          allowed_templates: [["sc007-acknowledgement", 1]],
          allowed_operational_messages: [],
        },
      },
    },
  );
  expect(seedResponse.ok(), await seedResponse.text()).toBeTruthy();
  const activity = await seedResponse.json();

  await page.goto("/participante");
  await page
    .getByLabel("Código de participante (seudónimo)")
    .fill("part-e2e001");
  await page.getByLabel("Identificador de actividad").fill(activity.id);
  const started = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/v1/sessions") &&
      response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  const session = await (await started).json();
  try {
    await expect(page.getByRole("status")).toContainText("sistema automático");

    await page.getByLabel("Tu mensaje").fill("Hola, esto es una prueba");
    const submitted = page.waitForResponse(
      response => response.url().endsWith(`/api/v1/sessions/${session.session_id}/turns`)
        && response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Enviar" }).click();
    const actual = await submitted;
    expect(actual.status()).toBe(200);
    expect((await actual.json()).output_text).toBeTruthy();
    await expect(page.locator(".turn-log .system")).toBeVisible();

    const ended = page.waitForResponse(
      response => response.url().endsWith(`/api/v1/sessions/${session.session_id}/end`)
        && response.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Finalizar sesión" }).click();
    expect((await ended).status()).toBe(200);
    await expect(page.getByRole("status")).toContainText("finalizado");

    await page.goto("/tecnica");
    const listed = page.waitForResponse(
      response => response.url().endsWith("/api/v1/sessions")
        && response.request().method() === "GET",
    );
    await page.getByRole("button", { name: "Sesiones" }).click();
    expect((await listed).status()).toBe(200);
    await expect(
      page.getByRole("button", {
        name: `${session.session_id.slice(0, 8)} — closed_voluntary — 1 turnos`,
        exact: true,
      }),
    ).toBeVisible();
  } finally {
    await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, {
      data: { confirm: true, reason: "abandoned" },
    }).catch(() => {});
  }
});
