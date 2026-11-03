import { expect, loginViaApi, test } from "../../support/fixtures";
import { DM1, loadChapter } from "../../support/shell";
import { ADMIN, clearRecords, record } from "../../support/records";

/* Recording through the interface with the browser's fake microphone: every "Record" is a new take, the first one stays the voice-over; the recording lasts
   as long as the slide is shown (its reading time), not as long as an earlier take, and a countdown pop-up is shown at the top right. */

test.use({ launchOptions: { args: ["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"] }, permissions: ["microphone"] });

test("every Record makes a new take", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru", 1); // an earlier one-second take: the new recording must not end after a second
  await page.goto(`/book/12/chapter/${ch.id}`);
  const status = page.locator(".slide-rec-status");
  for (const n of [2, 3]) {
    await page.locator(".slide-rec").click(); // start
    await expect(page.locator(".slide-rec.on")).toBeVisible();
    const timer = page.locator(".rec-timer");
    await expect(timer).toBeVisible();
    const box = (await timer.boundingBox())!;
    const view = page.viewportSize()!;
    expect(box.x + box.width / 2, "at the right").toBeGreaterThan(view.width / 2);
    expect(box.y, "at the top").toBeLessThan(160);
    const left = async () => {
      const [m, sec] = (await timer.locator(".rec-timer-time").innerText()).split(":").map(Number) as [number, number];
      return m * 60 + sec;
    };
    const before = await left();
    await page.waitForTimeout(2500);
    await expect(page.locator(".slide-rec.on"), "still recording after the earlier take's length").toBeVisible();
    expect(await left(), "the countdown goes down").toBeLessThan(before);
    await page.locator(".slide-rec").click(); // stop
    await expect(timer).toHaveCount(0);
    await expect(status).toContainText(`/${n}.wav`, { timeout: 20_000 });
  }
  await page.locator(".slide-rec-menu").click();
  await expect(page.locator(".rd-row")).toHaveCount(3);
  await expect(page.locator(".rd-row").nth(0)).toHaveClass(/on/); // the first stays the voice-over
  await clearRecords(request, token, ch.num);
});
