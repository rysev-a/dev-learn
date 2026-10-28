import { expect, loginViaApi, test } from "../support/fixtures";

test("signing in as the demo user opens the dashboard with sections", async ({ page, request, guard }) => {
  await loginViaApi(page, request);
  await page.goto("/");
  await expect(page.getByText("Дискретная математика").first()).toBeVisible();
  await expect(page.locator(".topic-card, .dash-card, .aside").first()).toBeVisible();
  guard.assertClean();
});
