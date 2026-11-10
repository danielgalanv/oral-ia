import { defineConfig } from "@playwright/test";
import { randomUUID } from "node:crypto";

process.env.ORALIA_DEMO_TEST_SECRET ??= randomUUID() + randomUUID();

// E2E tests run against isolated local API and Vite processes owned by this suite.
export default defineConfig({
  testDir: ".",
  globalSetup: "./preservation_guard.ts",
  // All browser flows share the API's process-wide single active-session lock.
  workers: 1,
  timeout: 30_000,
  use: {
    baseURL: "http://127.0.0.1:5175",
    trace: "on-first-retry",
  },
  webServer: [
    {
      command: "uv run --offline --no-sync python tests/e2e/run_demo.py",
      cwd: "../..",
      env: { ORALIA_DEMO_TEST_SECRET: process.env.ORALIA_DEMO_TEST_SECRET },
      url: "http://127.0.0.1:8015/demo-ready",
      reuseExistingServer: false,
      timeout: 90_000,
    },
    {
      command: "uv run --no-sync python tests/e2e/run_self_study_api.py",
      cwd: "../..",
      url: "http://127.0.0.1:8005/health",
      reuseExistingServer: false,
      timeout: 30_000,
    },
    {
      command: "pnpm.cmd --dir apps/web run dev",
      env: {
        ORALIA_E2E_WEB_PORT: "5175",
        ORALIA_E2E_API_URL: "http://127.0.0.1:8005",
      },
      cwd: "../..",
      url: "http://127.0.0.1:5175",
      reuseExistingServer: false,
      timeout: 30_000,
    },
  ],
});
