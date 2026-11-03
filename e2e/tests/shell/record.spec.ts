import type { APIRequestContext, Page } from "@playwright/test";
import { expect, loginViaApi, test } from "../../support/fixtures";
import { assertCleanBut404, DM1, loadChapter } from "../../support/shell";

/* Slide recordings (author tool, administrators only): one set per language, a delete button for the shown slide. The recordings are put
   on the server through the API (a real microphone is not available in the test browser). */

const ADMIN = { email: "programmer@mail.com", password: "programmer" };

/** One second of silence as a 16-bit mono WAV. */
function wav(): Buffer {
  const data = Buffer.alloc(16000);
  const head = Buffer.alloc(44);
  head.write("RIFF", 0);
  head.writeUInt32LE(36 + data.length, 4);
  head.write("WAVEfmt ", 8);
  head.writeUInt32LE(16, 16);
  head.writeUInt16LE(1, 20);
  head.writeUInt16LE(1, 22);
  head.writeUInt32LE(8000, 24);
  head.writeUInt32LE(16000, 28);
  head.writeUInt16LE(2, 32);
  head.writeUInt16LE(16, 34);
  head.write("data", 36);
  head.writeUInt32LE(data.length, 40);
  return Buffer.concat([head, data]);
}

async function record(request: APIRequestContext, token: string, chapter: number, slide: number, lang: "ru" | "en") {
  const res = await request.post(`/api/records/12/${chapter}/${slide}?lang=${lang}`, { headers: { Authorization: `Bearer ${token}`, "Content-Type": "audio/wav" }, data: wav() });
  expect(res.ok(), `record ${lang} ${slide}: ${res.status()}`).toBeTruthy();
}

const durations = async (request: APIRequestContext, id: number, lang: "ru" | "en") => {
  const res = await request.get(`/api/chapters/${id}?lang=${lang}`);
  return ((await res.json()) as { lessons: { dur: number }[] }).lessons.slice(0, 3).map((l) => l.dur);
};

const del = (page: Page) => page.locator(".slide-rec-del");

test("the delete button is shown for a slide with a recording and removes only the recording of the interface language", async ({ page, request, guard }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await record(request, token, ch.num, 0, "ru");
  await record(request, token, ch.num, 1, "en");
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-rec")).toBeVisible();

  // the Russian interface: slide 1 has a recording, slide 2 only has an English one
  await expect(del(page)).toBeVisible();
  await page.locator(".slide-dot").nth(1).click();
  await expect(del(page)).toHaveCount(0);
  await page.locator(".slide-dot").nth(0).click();

  // cancelling the confirmation keeps the recording
  page.once("dialog", (d) => void d.dismiss());
  await del(page).click();
  await expect(del(page)).toBeVisible();
  expect(await durations(request, ch.id, "ru")).toEqual([1, 0, 0]);

  page.once("dialog", (d) => void d.accept());
  await del(page).click();
  await expect(del(page)).toHaveCount(0);
  await expect(page.locator(".slide-rec-status")).toHaveText("Запись удалена");
  expect(await durations(request, ch.id, "ru")).toEqual([0, 0, 0]);
  expect(await durations(request, ch.id, "en"), "the English recording is untouched").toEqual([0, 1, 0]);
  assertCleanBut404(guard);

  // clean up the English one through the English interface
  await page.addInitScript(() => window.localStorage.setItem("cs-core-lang", "en"));
  await page.goto(`/book/12/chapter/${ch.id}`);
  await page.locator(".slide-dot").nth(1).click();
  await expect(del(page)).toBeVisible();
  page.once("dialog", (d) => void d.accept());
  await del(page).click();
  await expect(del(page)).toHaveCount(0);
  expect(await durations(request, ch.id, "en")).toEqual([0, 0, 0]);
});

test("a student does not see the record and delete buttons", async ({ page, request }) => {
  await loginViaApi(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel-head")).toBeVisible();
  await expect(page.locator(".slide-rec")).toHaveCount(0);
  await expect(del(page)).toHaveCount(0);
});
