import { expect, test } from "./local_auth";

test("/defensa is reachable and blocked null output creates no bubble", async ({
  page,
}) => {
  let turnCalls = 0;
  await page.route("**/defense-sessions/session-1/settings", (route) =>
    route.fulfill({
      json: {
        voice_input_allowed: false,
        voice_output_allowed: false,
        transcript_retention_authorized: false,
      },
    }),
  );
  await page.route("**/api/v1/sessions", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        session_id: "session-1",
        status: "active",
        activity_snapshot: {},
        ai_disclosure: "Interacción con IA",
      }),
    });
  });
  await page.route(
    "**/api/v1/defense-sessions/session-1/defense-turns",
    async (route) => {
      turnCalls += 1;
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          turn_id: `turn-${turnCalls}`,
          dialogue_action: turnCalls === 1 ? "ask" : "finish",
          dialogue_purpose: turnCalls === 1 ? "initial_question" : null,
          output_text:
            turnCalls === 1 ? "Explica tu decisión principal." : null,
          state_version: null,
          sources: [],
          general_knowledge_used: false,
          blocked: turnCalls !== 1,
          speech: null,
        }),
      });
    },
  );

  await page.goto("/defensa");
  await expect(
    page.getByRole("heading", { name: "ORAL-IA — Defensa oral" }),
  ).toBeVisible();
  await page.getByLabel("Código seudónimo").fill("participant-a");
  await page.getByLabel("Actividad").fill("activity-a");
  await page.getByRole("button", { name: "Iniciar defensa" }).click();
  await page.getByLabel("Tu respuesta").fill("respuesta privada");
  await page.getByRole("button", { name: "Enviar" }).click();
  await expect(page.getByRole("status")).toContainText("closed_error_safe");
  // Terminal ephemeral closure clears prior transcript; null output never creates a bubble.
  await expect(page.locator(".system")).toHaveCount(0);
  await expect(page.locator("audio")).toHaveCount(0);
});

test("defense exposes keyboard pause, pace and repeat controls", async ({
  page,
}) => {
  await page.route("**/api/v1/sessions", (route) =>
    route.fulfill({
      json: {
        session_id: "controls",
        ai_disclosure: "Interacción con IA",
        activity: {
          name: "Defensa",
          objective: "Explicar",
          max_turns: 5,
          max_duration_seconds: 600,
        },
      },
    }),
  );
  await page.route("**/defense-sessions/controls/settings", (route) =>
    route.fulfill({
      json: {
        voice_input_allowed: false,
        voice_output_allowed: false,
        transcript_retention_authorized: true,
      },
    }),
  );
  await page.route("**/defense-sessions/controls/defense-turns", (route) =>
    route.fulfill({
      json: {
        turn_id: "turn",
        dialogue_action: "ask",
        output_text: "Explica la separación.",
        sources: [],
        speech: null,
      },
    }),
  );
  await page.goto("/defensa");
  await page.getByLabel("Código seudónimo").fill("participant");
  await page.getByLabel("Actividad", { exact: true }).fill("activity");
  await page.getByRole("button", { name: "Iniciar defensa" }).click();
  await page.getByRole("button", { name: "Pausar" }).click();
  await expect(page.getByLabel("Tu respuesta")).toBeDisabled();
  await page.getByRole("button", { name: "Reanudar" }).click();
  await expect(page.getByLabel("Tu respuesta")).toBeEnabled();
  await expect(page.getByLabel("Ritmo de voz")).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Repetir pregunta" }),
  ).toBeVisible();
  await expect(page.getByLabel("Conservar transcripción")).toBeVisible();
});

test("voice review, literal replay failure and retention preserve text continuity", async ({
  page,
}) => {
  await page.addInitScript(() => {
    const state = window as unknown as { urlRevocations: string[] };
    state.urlRevocations = [];
    const revoke = URL.revokeObjectURL.bind(URL);
    URL.revokeObjectURL = (url: string) => {
      state.urlRevocations.push(url);
      revoke(url);
    };
    const stream = { getTracks: () => [{ stop() {} }] };
    Object.defineProperty(navigator, "mediaDevices", {
      value: { getUserMedia: async () => stream },
    });
    class Recorder {
      state = "inactive";
      mimeType = "audio/webm";
      stream = stream;
      ondataavailable: ((event: { data: Blob }) => void) | null = null;
      onstop: (() => void) | null = null;
      start() {
        this.state = "recording";
      }
      stop() {
        this.state = "inactive";
        this.ondataavailable?.({ data: new Blob(["fixture"]) });
        this.onstop?.();
      }
    }
    Object.defineProperty(window, "MediaRecorder", { value: Recorder });
  });
  await page.route("**/api/v1/sessions", (route) =>
    route.fulfill({
      json: {
        session_id: "voice-ui",
        ai_disclosure: "Interacción con IA",
        activity: { max_turns: 10, max_duration_seconds: 900 },
      },
    }),
  );
  await page.route("**/defense-sessions/voice-ui/settings", (route) =>
    route.fulfill({
      json: {
        voice_input_allowed: true,
        voice_output_allowed: true,
        transcript_retention_authorized: true,
        low_confidence_threshold: 0.7,
      },
    }),
  );
  let turns = 0;
  await page.route("**/defense-sessions/voice-ui/defense-turns", (route) => {
    turns += 1;
    return route.fulfill({
      json: {
        turn_id: `turn-${turns}`,
        dialogue_action: "ask",
        output_text: "Explica la arquitectura.",
        speech: null,
      },
    });
  });
  await page.route("**/defense-turns/voice", (route) =>
    route.fulfill({
      json: {
        transcript_id: "transcript-ui",
        raw_text: "arquitectura incorrecta",
        low_confidence: true,
        overall_confidence: 0.65,
        segments: [
          {
            text: "arquitectura incorrecta",
            confidence: 0.65,
            start_ms: 0,
            end_ms: 100,
          },
        ],
      },
    }),
  );
  let confirmed = false;
  await page.route("**/defense-turns/voice/confirm", (route) => {
    expect(route.request().postDataJSON().corrected_text).toBe(
      "arquitectura corregida",
    );
    confirmed = true;
    return route.fulfill({
      json: {
        turn_id: "confirmed",
        dialogue_action: "ask",
        output_text: "Justifica la separación.",
        speech: {
          available: true,
          url: "/api/v1/voice-ui/speech",
          media_type: "audio/wav",
          text_sha256: "fixture",
        },
      },
    });
  });
  let speechCalls = 0;
  await page.route("**/voice-ui/speech", (route) => {
    speechCalls += 1;
    return speechCalls <= 2
      ? route.fulfill({
          contentType: "audio/wav",
          body: Buffer.from("RIFFfixture"),
        })
      : route.fulfill({ status: 503, json: { detail: "unavailable" } });
  });
  await page.route("**/defense-sessions/voice-ui/defense-transcript", (route) =>
    route.fulfill({
      json: {
        turns: [
          {
            turn_id: "confirmed",
            input_text: "arquitectura corregida",
            output_text: "Justifica la separación.",
          },
        ],
        transcripts: [
          {
            transcript_id: "t",
            raw_text: "arquitectura",
            corrections: ["arquitectura corregida"],
          },
        ],
      },
    }),
  );
  await page.route("**/defense-sessions/voice-ui/defense-end", (route) => {
    expect(route.request().postDataJSON()).toEqual({
      retain: true,
      scope: ["transcript"],
    });
    return route.fulfill({
      json: {
        session_id: "voice-ui",
        status: "closed_voluntary",
        defense_summary: { turn_count: 2 },
      },
    });
  });
  await page.goto("/defensa");
  await page.getByLabel("Código seudónimo").fill("participant");
  await page.getByLabel("Actividad", { exact: true }).fill("activity");
  await page.getByRole("button", { name: "Iniciar defensa" }).click();
  await expect(page.getByLabel("Tu respuesta")).toBeEnabled();
  await page.getByRole("button", { name: "Grabar respuesta" }).click();
  await page.getByRole("button", { name: "Detener grabación" }).click();
  await expect(page.locator(".low-confidence")).toContainText(
    "arquitectura incorrecta",
  );
  expect(turns).toBe(1);
  await page
    .getByLabel("Transcripción corregible")
    .fill("arquitectura corregida");
  await page.getByRole("button", { name: "Confirmar texto" }).click();
  await expect(
    page.getByText("Justifica la separación.", { exact: true }),
  ).toBeVisible();
  expect(confirmed).toBeTruthy();
  await page.getByRole("button", { name: "Reproducir voz" }).click();
  await expect(page.locator("audio")).toHaveAttribute("src", /^blob:/);
  const firstUrl = await page.locator("audio").getAttribute("src");
  await page.getByRole("button", { name: "Reproducir voz" }).click();
  await expect
    .poll(() =>
      page.evaluate(
        (url) =>
          (
            window as unknown as { urlRevocations: string[] }
          ).urlRevocations.includes(url!),
        firstUrl,
      ),
    )
    .toBe(true);
  await page.getByRole("button", { name: "Reproducir voz" }).click();
  await expect(page.getByRole("alert")).toContainText("texto sigue disponible");
  await expect(page.getByLabel("Tu respuesta")).toBeEnabled();
  await page.getByLabel("Conservar transcripción").check();
  await page.getByRole("button", { name: "Finalizar sesión" }).click();
  await expect(
    page.getByRole("region", { name: "Transcripción completa de la sesión" }),
  ).toContainText("Original de voz: arquitectura");
  await page
    .getByRole("button", { name: "Confirmar cierre de sesión" })
    .click();
  await expect(page.getByRole("status")).toContainText("closed_voluntary");
  await expect(page.getByLabel("Resumen descriptivo")).toContainText(
    "turn_count",
  );
});
