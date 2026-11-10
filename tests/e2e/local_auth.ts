import { test as base, expect } from "@playwright/test";

// Fictitious install credential, passed through the real login route. No production bypass.
export const test = base.extend<{ administrative: boolean; localLogin: void }>({
  administrative: [true, { option: true }],
  localLogin: [
    async ({ context, request, administrative }, use) => {
      if (administrative) {
        for (const client of [context.request, request]) {
          const response = await client.post(
            "http://127.0.0.1:8005/api/v1/auth/login",
            {
              data: { secret: "fictional-e2e-installation-secret-005" },
            },
          );
          expect(response.status()).toBe(200);
        }
      }
      await use();
    },
    { auto: true },
  ],
});
export { expect };
