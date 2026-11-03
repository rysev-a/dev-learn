import { expect, loginViaApi, test } from "../../support/fixtures";
import { DM1, loadChapter } from "../../support/shell";
import { ADMIN, clearRecords } from "../../support/records";

/* Recording through the interface with the browser's fake microphone: every "Record" is a new take, the first one stays the voice-over. */

test.use({ launchOptions: { args: ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"] }, permissions: ["microphone"] });

test("every Record makes a new take", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await page.goto(`/book/12/chapter/${ch.id}`);
  const status = page.locator(".slide-rec-status");
  for (const n of [1, 2]) {
    await page.locator(".slide-rec").click(); // start
    await expect(page.locator(".slide-rec.on")).toBeVisible();
    await page.waitForTimeout(1500);
    await page.locator(".slide-rec").click(); // stop
    await expect(status).toContainText(`${n}.wav`, { timeout: 20_000 });
  }
  await page.locator(".slide-rec-menu").click();
  await expect(page.locator(".rd-row")).toHaveCount(2);
  await expect(page.locator(".rd-row").nth(0)).toHaveClass(/on/); // the first stays the voice-over
  await clearRecords(request, token, ch.num);
});
