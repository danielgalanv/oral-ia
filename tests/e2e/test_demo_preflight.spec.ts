import { test, expect } from "@playwright/test";

test.use({ baseURL: "http://127.0.0.1:5185", trace: "off" });

test("demo: destinatario incorrecto no bloquea una entrada corregida y muestra un mensaje legible", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: "Área docente", exact: true }).press("Enter");
  const article = page.getByRole("article", { name: "Actividad Demo: autoestudio del agua versión 1", exact: true });
  await article.getByRole("link", { name: "Abrir actividad de autoestudio" }).press("Enter");
  const code = page.getByLabel("Código de participante (seudónimo)", { exact: true });
  await code.fill("synthetic-not-allowed");
  const rejected = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
  await page.getByRole("button", { name: "Iniciar", exact: false }).press("Enter");
  const denied = await rejected;
  expect(denied.status()).toBe(409);
  expect((await denied.json()).detail.code).toBe("recipient_not_allowed");
  await expect(page.getByRole("alert")).toContainText("no es destinatario");
  await expect(page.getByRole("alert")).not.toContainText("[object Object]");
  await code.fill("demo-007");
  const accepted = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
  await page.getByRole("button", { name: "Iniciar", exact: false }).press("Enter");
  expect((await accepted).status()).toBe(201);
  await page.getByRole("button", { name: "Finalizar", exact: false }).press("Enter");
  await expect(page.getByRole("status").first()).toContainText("closed");
});
