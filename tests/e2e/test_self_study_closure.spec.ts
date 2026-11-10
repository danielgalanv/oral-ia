import { expect, test } from "./local_auth";
import type { APIRequestContext, Page } from "@playwright/test";
import { readFile } from "node:fs/promises";
import { createHash, randomUUID } from "node:crypto";
import path from "node:path";

const API = "http://127.0.0.1:8005/api/v1";
const COURSE_ID = "30000000-0000-0000-0000-000000000001";
const RETENTION_POLICY_ID = "30000000-0000-0000-0000-000000000002";

function outputPolicy(participantCode: string) {
  return {
    schema_version: 1,
    policy_id: `e2e-policy-${randomUUID()}`,
    policy_version: 1,
    allowed_recipients: [participantCode],
    allowed_disclosures: [
      { category: "texto", provenance: "activity_material", recipient: participantCode },
    ],
    allowed_scopes: {
      topics: ["activity"],
      purposes: ["material_response", "missing_information", "conversation_recovery"],
      actions: ["respond", "acknowledge_missing_info", "clarify"],
    },
    general_knowledge_allowed: false,
    allowed_templates: [
      ["material-fragment-response", 1],
      ["material-fragment-response-2", 1],
      ["material-fragment-response-3", 1],
      ["self-study-missing-info", 1],
      ["self-study-incoherence", 1],
    ],
    allowed_operational_messages: [],
  };
}

async function createActivity(
  request: APIRequestContext,
  participantCode: string,
  maxTurns: number,
) {
  const created = await request.post(`${API}/activities`, {
    data: {
      course_id: COURSE_ID,
      name: `Autoestudio E2E ${randomUUID()}`,
      subject: "Demo",
      objective: "Validar cierre y resumen",
      mode: "self_study",
      language: "es",
      max_turns: maxTurns,
      max_duration_seconds: 900,
      retention_policy_id: RETENTION_POLICY_ID,
      general_knowledge_allowed: false,
      output_authorization_policy: outputPolicy(participantCode),
    },
  });
  expect(created.ok(), await created.text()).toBeTruthy();
  const activity = await created.json();

  for (let attempt = 0; attempt < 20; attempt += 1) {
    if ((await request.get(`${API}/activities/${activity.id}`)).ok()) break;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }

  const configured = await request.post(`${API}/tecnica/activities/${activity.id}/self-study-config`, {
    data: {
      enabled_modes: ["doubt_resolution"],
      summary_authorized: true,
      practice_reveals_solution: false,
      retention_authorized: false,
    },
  });
  expect(configured.ok(), await configured.text()).toBeTruthy();

  const sample = await readFile(path.resolve(__dirname, "../fixtures/materials/sample.docx"));
  let uploaded = await request.post(`${API}/materials/documents`, {
    multipart: {
      course_id: COURSE_ID,
      activity_configuration_ids: activity.id,
      file: {
        name: `sample-${createHash("sha1").update(activity.id).digest("hex")}.docx`,
        mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        buffer: Buffer.concat([sample, Buffer.from(activity.id)]),
      },
    },
  });
  if (uploaded.status() === 409) {
    const conflict = await uploaded.json();
    uploaded = await request.post(
      `${API}/materials/documents/${conflict.conflict_token}/duplicate-resolution`,
      { data: { resolution: "proceed_new" } },
    );
  }
  expect(uploaded.ok(), await uploaded.text()).toBeTruthy();
  const document = await uploaded.json();
  for (let attempt = 0; attempt < 20; attempt += 1) {
    if ((await request.get(`${API}/materials/documents/${document.id}`)).ok()) break;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  const activated = await request.post(`${API}/materials/documents/${document.id}/activate`);
  expect(activated.ok(), await activated.text()).toBeTruthy();
  return activity.id as string;
}

async function startThroughUi(page: Page, participantCode: string, activityId: string) {
  await page.goto("/autoestudio");
  await page.getByLabel("Código de participante (seudónimo)").fill(participantCode);
  await page.getByLabel("Identificador de actividad").fill(activityId);
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByText(/sistema automático/)).toBeVisible();
}

async function submitCoveredTurn(page: Page, expectVisibleResponse = true) {
  await page.getByLabel("Tu mensaje").fill("¿Qué contiene el documento de prueba?");
  await page.getByRole("button", { name: "Enviar" }).click();
  if (expectVisibleResponse) await expect(page.locator(".turn-log .system")).toBeVisible();
}

test("voluntary self-study closure displays its summary once and disables input", async ({
  page,
  request,
}) => {
  const participant = `e2e-voluntary-${randomUUID()}`;
  const activityId = await createActivity(request, participant, 5);
  await startThroughUi(page, participant, activityId);
  await submitCoveredTurn(page);

  await page.getByRole("button", { name: "Finalizar sesión" }).click();
  await expect(page.getByRole("status")).toContainText("closed_voluntary");
  await expect(page.getByRole("heading", { name: "Resumen de estudio" })).toBeVisible();
  await expect(page.getByLabel("Tu mensaje")).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Resumen de estudio" })).toHaveCount(1);
});

test("automatic limit closure uses the turn response and disables further input", async ({
  page,
  request,
}) => {
  const participant = `e2e-limit-${randomUUID()}`;
  const activityId = await createActivity(request, participant, 1);
  await startThroughUi(page, participant, activityId);
  await submitCoveredTurn(page, false);

  await expect(page.getByRole("status")).toContainText("closed_limit_reached");
  await expect(page.getByRole("heading", { name: "Resumen de estudio" })).toBeVisible();
  await expect(page.getByLabel("Tu mensaje")).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Finalizar sesión" })).toHaveCount(0);
});
