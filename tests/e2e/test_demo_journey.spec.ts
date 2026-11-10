import { test, expect } from "@playwright/test";
import { readFile } from "node:fs/promises";

test.use({ baseURL: "http://127.0.0.1:5185", trace: "off" });

test("demo: portada, apertura autorizada, fuentes reales, conservación, exportación, borrado y alternativa efímera", async ({
  page,
}) => {
  test.setTimeout(60_000);
  const externalRequests: string[] = [];
  await page.route("**/*", async (route) => {
    const host = new URL(route.request().url()).hostname;
    if (!["127.0.0.1", "localhost"].includes(host)) {
      externalRequests.push(host);
      await route.abort();
    } else await route.continue();
  });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Demostración con datos ficticios" }),
  ).toBeVisible();
  await page
    .getByRole("link", { name: "Área docente", exact: true })
    .press("Enter");
  await expect(page.getByLabel("Credencial local")).toHaveCount(0);
  const article = page.getByRole("article", {
    name: "Actividad Demo: autoestudio del agua versión 1",
    exact: true,
  });
  await expect(article).toBeVisible();
  await page
    .getByText("Materiales disponibles y estado", { exact: true })
    .press("Enter");
  await expect(
    page.getByText("agua-demo.docx", { exact: false }),
  ).toBeVisible();
  await article
    .getByRole("link", { name: "Abrir actividad de autoestudio" })
    .press("Enter");
  await expect(
    page.getByLabel("Identificador de actividad", { exact: true }),
  ).not.toHaveValue("");
  await page
    .getByLabel("Código de participante (seudónimo)", { exact: true })
    .fill("demo-007");
  const started = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Iniciar", exact: false })
    .press("Enter");
  const session = await (await started).json();
  await page
    .getByLabel("Conservar transcripción de esta sesión", { exact: true })
    .press("Space");
  await page
    .getByLabel("Conservar resumen de esta sesión", { exact: true })
    .press("Space");
  await page
    .getByLabel("Tu mensaje", { exact: true })
    .fill("¿A qué temperatura hierve el agua?");
  await page
    .getByRole("button", { name: "Enviar", exact: true })
    .press("Enter");
  await expect(page.locator(".system")).toContainText("100");
  await expect(
    page.getByText("Fuentes", { exact: false }).first(),
  ).toBeVisible();
  await page.getByText("Fuentes", { exact: true }).press("Enter");
  await expect(page.locator(".sources-panel")).toContainText("100");
  await page
    .getByRole("button", { name: "Finalizar", exact: false })
    .press("Enter");
  await expect(page.getByRole("status").first()).toContainText("closed");
  await page.getByRole("link", { name: "Volver al inicio" }).press("Enter");
  await page
    .getByRole("link", { name: "Área docente", exact: true })
    .press("Enter");
  await page
    .getByRole("button", {
      name: `Revisar sesión ${session.session_id}`,
      exact: true,
    })
    .press("Enter");
  await expect(
    page.getByRole("region", { name: "Revisión consentida" }),
  ).toContainText("100");
  await page
    .getByLabel(`Sesión ${session.session_id}`, { exact: false })
    .press("Space");
  await page.getByLabel("Incluir texto libre autorizado").press("Space");
  await page
    .getByLabel(
      "He revisado el texto libre de todas las sesiones seleccionadas",
    )
    .press("Space");
  for (const format of ["JSON", "Markdown"]) {
    const pending = page.waitForEvent("download");
    await page
      .getByRole("button", { name: `Exportar ${format}`, exact: true })
      .press("Enter");
    const download = await pending;
    const content = await readFile((await download.path())!, "utf8");
    expect(content).toContain("100");
    expect(content).not.toContain("demo-007");
    expect(content).not.toContain(process.env.ORALIA_DEMO_TEST_SECRET!);
  }
  await page
    .getByLabel("Confirmo eliminar el contenido de esta sesión", {
      exact: true,
    })
    .press("Space");
  await page
    .getByRole("button", { name: "Eliminar sesión revisada" })
    .press("Enter");
  await expect(page.getByRole("status")).toContainText(
    "Eliminación confirmada",
  );
  expect(
    (
      await page.request.get(
        `/api/v1/governance/sessions/${session.session_id}`,
      )
    ).status(),
  ).toBe(404);
  expect(
    (
      await page.request.post("/api/v1/governance/exports", {
        data: { session_ids: [session.session_id] },
      })
    ).status(),
  ).toBe(409);
  const defense = page.getByRole("article", {
    name: "Actividad Demo: defensa del agua versión 1",
    exact: true,
  });
  await defense
    .getByRole("link", { name: "Abrir actividad de defensa" })
    .press("Enter");
  await page.getByLabel("Código seudónimo", { exact: true }).fill("demo-007");
  const opened = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Iniciar defensa" }).press("Enter");
  const ephemeral = await (await opened).json();
  await expect(page.locator(".system")).toContainText("agua");
  await page
    .getByLabel("Tu respuesta", { exact: true })
    .fill("El agua hierve a 100 grados.");
  const answered = page.waitForResponse(
    (r) => r.url().endsWith(`/defense-sessions/${ephemeral.session_id}/defense-turns`)
      && r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Enviar", exact: true })
    .press("Enter");
  expect((await answered).status()).toBe(200);
  await expect(page.getByRole("button", { name: "Finalizar sesión", exact: true })).toBeEnabled();
  await page
    .getByRole("button", { name: "Finalizar", exact: false })
    .press("Enter");
  const closedEphemeral = page.waitForResponse(
    (r) => r.url().endsWith(`/defense-sessions/${ephemeral.session_id}/defense-end`)
      && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Confirmar cierre de sesión", exact: true }).press("Enter");
  const closure = await closedEphemeral;
  expect(closure.status()).toBe(200);
  expect((await closure.json()).status).toBe("closed_voluntary");
  expect(
    (
      await page.request.get(
        `/api/v1/governance/sessions/${ephemeral.session_id}`,
      )
    ).status(),
  ).toBe(404);
  expect(externalRequests).toEqual([]);
});
