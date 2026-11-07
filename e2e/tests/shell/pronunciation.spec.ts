import { expect, loginViaApi, test } from "../../support/fixtures";
import { DM1, loadChapter } from "../../support/shell";
import { ADMIN, clearRecords, record } from "../../support/records";

/* The pronunciation check of a take in the "Recordings of this slide" window: the scores, the text with the weak words marked and the list of what to work on.
   The speech service is never called for real (the e2e backend points at a dead address): the result comes from a canned reply, and the failure path
   shows the server's message. */

const RESULT = {
  at: 1730000000,
  pron: 78.4,
  accuracy: 74.0,
  fluency: 91.0,
  completeness: 88.0,
  prosody: 66.0,
  words: [
    { word: "Think", accuracy: 41.0, error: "Mispronunciation", pause: "None", phonemes: [{ phoneme: "θ", accuracy: 12.0 }, { phoneme: "ɪ", accuracy: 95.0 }] },
    { word: "about", accuracy: 99.0, error: "None", pause: "None", phonemes: [] },
    { word: "sets", accuracy: 85.0, error: "None", pause: "UnexpectedBreak", phonemes: [] },
    { word: "carefully", accuracy: 0.0, error: "Omission", pause: "None", phonemes: [] },
  ],
};

async function openRecordings(page: import("@playwright/test").Page, id: number) {
  await page.goto(`/book/12/chapter/${id}`);
  await page.locator(".slide-rec-menu").click();
  await expect(page.locator(".rd.open")).toBeVisible();
  await expect(page.locator(".rd-row")).toHaveCount(1);
}

test("a check shows the scores, the marked text and what to work on", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru");
  await page.route(`**/api/records/12/${ch.num}/0/1/assess*`, (route) => route.fulfill({ json: RESULT }));
  await openRecordings(page, ch.id);

  await page.locator(".rd-check").click();
  const detail = page.locator(".rd-detail");
  await expect(detail).toBeVisible();
  await expect(page.locator(".rd-check .rd-score")).toHaveText("78");
  await expect(page.locator(".rd-metric")).toHaveCount(5);
  await expect(page.locator(".rd-metric").first().locator("dd")).toHaveText("78");
  await expect(page.locator(".rd-metric dd.mid").first()).toBeVisible();

  // the text keeps the words in order; the bad ones are marked, the skipped one is struck through
  await expect(detail.locator(".rd-text")).toHaveText("Think about sets carefully");
  await expect(detail.locator(".rd-w.low")).toHaveText(["Think"]);
  await expect(detail.locator(".rd-w.skip")).toHaveText(["carefully"]);

  // what to work on: the words below 80 or with a fault, with their weak sounds; a good word without a fault is not listed
  const weak = detail.locator(".rd-weak");
  await expect(weak).toHaveCount(3);
  await expect(weak.nth(0)).toContainText("Think");
  await expect(weak.nth(0)).toContainText("/θ/ 12");
  await expect(weak.nth(0).locator(".rd-tag")).toHaveCount(1);
  await expect(weak.nth(1)).toContainText("sets");
  await expect(weak.nth(2)).toContainText("carefully");
  await expect(weak.nth(2).locator(".rd-weak-score")).toHaveCount(0);

  // the score button folds and unfolds the result; "check again" is inside it
  await page.locator(".rd-check").click();
  await expect(detail).toHaveCount(0);
  await page.locator(".rd-check").click();
  await expect(detail.locator(".rd-again")).toBeVisible();
  await clearRecords(request, token, ch.num);
});

test("a failed check shows the server's message", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru");
  await openRecordings(page, ch.id);

  await page.locator(".rd-check").click();
  await expect(page.locator(".rd-note.error")).toContainText("Сервис проверки произношения не ответил");
  await expect(page.locator(".rd-detail")).toHaveCount(0);
  await expect(page.locator(".rd-check")).toBeEnabled(); // it can be tried again
  await clearRecords(request, token, ch.num);
});
