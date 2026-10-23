import { expect, loginViaApi, test } from "../support/fixtures";

test("вход демо-пользователем открывает дашборд с разделами", async ({ page, request, guard }) => {
  await loginViaApi(page, request);
  await page.goto("/");
  await expect(page.getByText("Дискретная математика").first()).toBeVisible();
  await expect(page.locator(".topic-card, .dash-card, .aside").first()).toBeVisible();
  guard.assertClean();
});
