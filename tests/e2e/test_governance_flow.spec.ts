import { readFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { test, expect } from "./local_auth";

test.use({ administrative: false });

test("local governance: real login, immutable successor, consented review, two exports, deletion and logout", async ({
  page,
  request,
}) => {
  const name = `Gobierno ${randomUUID()}`;
  const participant = `pilot-${randomUUID()}`;
  expect(
    (
      await request.get("http://127.0.0.1:8005/api/v1/governance/sessions")
    ).status(),
  ).toBe(401);
  await page.goto("/gobierno");
  await page
    .getByLabel("Credencial local")
    .fill("fictional-e2e-installation-secret-005");
  await page.getByLabel("Credencial local").press("Enter");
  await expect(
    page.getByRole("heading", { name: "Nueva configuración", exact: true }),
  ).toBeVisible();
  await page.getByLabel("Nombre de actividad", { exact: true }).fill(name);
  await page.getByLabel("Límite de turnos", { exact: true }).fill("2");
  await page
    .getByLabel("Código seudónimo destinatario de la política")
    .fill(participant);
  await page.getByLabel("Permitir elección de conservación").press("Space");
  await page
    .getByRole("button", { name: "Preparar política explícita para revisar" })
    .press("Enter");
  await page
    .getByLabel("He revisado los permisos de salida de esta versión")
    .press("Space");
  const configured = page.waitForResponse(
    (r) =>
      r.url().endsWith("/governance/activities") &&
      r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Guardar borrador", exact: true })
    .press("Enter");
  const createdResponse = await configured;
  expect(createdResponse.status(), await createdResponse.text()).toBe(201);
  const activity = await createdResponse.json();
  const firstArticle = page.getByRole("article", {
    name: `Actividad ${name} versión 1`,
    exact: true,
  });
  await firstArticle.getByRole("button", { name: "Activar versión" }).press("Enter");
  await expect(firstArticle).toContainText("active");
  await page.goto("/defensa");
  await page.getByLabel("Código seudónimo", { exact: true }).fill(participant);
  await page.getByLabel("Actividad", { exact: true }).fill(activity.id);
  const opened = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Iniciar defensa" }).press("Enter");
  const session = await (await opened).json();
  await expect(page.locator(".system")).toHaveCount(1);
  await page.getByLabel("Conservar transcripción", { exact: true }).press("Space");
  await page.getByLabel("Conservar resumen", { exact: true }).press("Space");
  await page
    .getByLabel("Tu respuesta", { exact: true })
    .fill("Una explicación ficticia de la decisión principal.");
  await page.getByRole("button", { name: "Enviar", exact: true }).press("Enter");
  await expect(page.getByRole("status")).toContainText("closed_limit_reached");
  await page.goto("/gobierno");
  await page
    .getByRole("button", {
      name: `Revisar sesión ${session.session_id}`,
      exact: true,
    })
    .press("Enter");
  await expect(
    page.getByRole("region", { name: "Revisión consentida" }),
  ).toContainText("Una explicación ficticia");
  await page
    .getByLabel(`Sesión ${session.session_id}`, { exact: false })
    .press("Space");
  await page.getByLabel("Incluir texto libre autorizado").press("Space");
  await expect(
    page.getByRole("button", { name: "Exportar JSON", exact: true }),
  ).toBeDisabled();
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
    const file = await (await pending).path();
    const text = await readFile(file!, "utf8");
    expect(text).toContain("Una explicación ficticia");
    expect(text).not.toContain(participant);
    expect(text).not.toContain(session.session_id);
    expect(text).not.toContain(session.access_token);
    expect(text).not.toContain("fictional-e2e-installation-secret-005");
  }
  await firstArticle
    .getByRole("button", { name: "Editar como nueva versión" })
    .press("Enter");
  await page.getByLabel("Límite de turnos", { exact: true }).fill("3");
  await page
    .getByLabel("He revisado los permisos de salida de esta versión")
    .press("Space");
  const duplicated = page.waitForResponse(
    (r) =>
      r.url().endsWith(`/governance/activities/${activity.id}/duplicate`) &&
      r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Crear versión sucesora", exact: true })
    .press("Enter");
  expect((await duplicated).status()).toBe(201);
  const successor = page.getByRole("article", {
    name: `Actividad ${name} versión 2`,
    exact: true,
  });
  await successor.getByRole("button", { name: "Activar versión" }).press("Enter");
  await expect(successor).toContainText("active");
  await expect(firstArticle).toContainText("retired");
  const previous = await page.request.get(
    `http://127.0.0.1:8005/api/v1/governance/sessions/${session.session_id}`,
  );
  expect((await previous.json()).configuration.version).toBe(1);
  const retiredStart = await request.post(
    "http://127.0.0.1:8005/api/v1/sessions",
    {
      data: {
        participant_code: "another-pilot",
        activity_configuration_id: activity.id,
      },
    },
  );
  expect(retiredStart.status()).toBe(409);
  await page
    .getByLabel("Confirmo eliminar el contenido de esta sesión", {
      exact: true,
    })
    .press("Space");
  const deleteReviewed = page.getByRole("button", { name: "Eliminar sesión revisada" });
  await expect(deleteReviewed).toBeEnabled();
  const deleted = page.waitForResponse(
    r => r.url().endsWith(`/api/v1/sessions/${session.session_id}/content`)
      && r.request().method() === "DELETE",
  );
  await deleteReviewed.press("Enter");
  expect((await deleted).status()).toBe(200);
  await expect(page.getByRole("status")).toContainText(
    "Eliminación confirmada",
  );
  expect(
    (
      await page.request.get(
        `http://127.0.0.1:8005/api/v1/governance/sessions/${session.session_id}`,
      )
    ).status(),
  ).toBe(404);
  expect(
    (
      await page.request.post(
        "http://127.0.0.1:8005/api/v1/governance/exports",
        { data: { session_ids: [session.session_id] } },
      )
    ).status(),
  ).toBe(409);
  const logout = page.getByRole("button", { name: "Cerrar acceso docente" });
  await expect(logout).toBeEnabled();
  const loggedOut = page.waitForResponse(
    r => r.url().endsWith("/api/v1/auth/logout") && r.request().method() === "POST",
  );
  await logout.press("Enter");
  expect((await loggedOut).status()).toBe(200);
  await expect(page.getByLabel("Credencial local")).toBeVisible();
  expect(
    (
      await page.request.get("http://127.0.0.1:8005/api/v1/governance/sessions")
    ).status(),
  ).toBe(401);
});
