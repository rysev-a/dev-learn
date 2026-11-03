import type { APIRequestContext, Page } from "@playwright/test";
import { expect, loginViaApi, test } from "../../support/fixtures";
import { ADMIN, clearRecords, record } from "../../support/records";
import { assertCleanBut404, DM1, loadChapter } from "../../support/shell";

/* Slide recordings (author tool, administrators only): every Record is a new take, a set of takes per language, the burger next to "Play" opens
   a window where the take that voices the slide is chosen and takes are deleted. Takes are mostly put on the server through the API;
   one test records through the interface with the browser's fake microphone. */

const durations = async (request: APIRequestContext, id: number, lang: "ru" | "en") => {
  const res = await request.get(`/api/chapters/${id}?lang=${lang}`);
  return ((await res.json()) as { lessons: { dur: number }[] }).lessons.slice(0, 3).map((l) => l.dur);
};

const burger = (page: Page) => page.locator(".slide-rec-menu");
const dialog = (page: Page) => page.locator(".rd.open");
const rows = (page: Page) => page.locator(".rd-row");

test("the burger opens the window with the takes: the first is chosen, another can be chosen and deleted", async ({ page, request, guard }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru", 1);
  await record(request, token, ch.num, 0, "ru", 2);
  await record(request, token, ch.num, 1, "en", 1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-rec")).toBeVisible();
  await expect(dialog(page)).toHaveCount(0);

  // by default the first take voices the slide
  expect(await durations(request, ch.id, "ru")).toEqual([1, 0, 0]);
  await burger(page).click();
  await expect(dialog(page)).toBeVisible();
  await expect(rows(page)).toHaveCount(2);
  await expect(rows(page).nth(0)).toHaveClass(/on/);
  await expect(rows(page).nth(1)).not.toHaveClass(/on/);
  await expect(rows(page).nth(0).locator(".rd-meta")).toContainText("0:01");
  await expect(rows(page).nth(1).locator(".rd-meta")).toContainText("0:02");

  // choosing the second one
  await rows(page).nth(1).locator(".rd-pick").click();
  await expect(rows(page).nth(1)).toHaveClass(/on/);
  await expect(rows(page).nth(0)).not.toHaveClass(/on/);
  expect(await durations(request, ch.id, "ru")).toEqual([2, 0, 0]);

  // the window shows the shown slide: another slide has no takes in this language
  await page.keyboard.press("Escape");
  await expect(dialog(page)).toHaveCount(0);
  await page.locator(".slide-dot").nth(1).click();
  await burger(page).click();
  await expect(page.locator(".rd-note")).toContainText("Записей пока нет");
  await page.locator(".rd-backdrop").click({ position: { x: 5, y: 5 } });
  await expect(dialog(page)).toHaveCount(0);
  await page.locator(".slide-dot").nth(0).click();

  // cancelling the confirmation keeps the take; deleting the chosen one makes the first voice the slide
  await burger(page).click();
  page.once("dialog", (d) => void d.dismiss());
  await rows(page).nth(1).locator(".rd-del").click();
  await expect(rows(page)).toHaveCount(2);
  page.once("dialog", (d) => void d.accept());
  await rows(page).nth(1).locator(".rd-del").click();
  await expect(rows(page)).toHaveCount(1);
  await expect(rows(page).nth(0)).toHaveClass(/on/);
  expect(await durations(request, ch.id, "ru")).toEqual([1, 0, 0]);
  expect(await durations(request, ch.id, "en"), "the English take is untouched").toEqual([0, 1, 0]);

  // deleting the last take: the slide is silent again
  page.once("dialog", (d) => void d.accept());
  await rows(page).nth(0).locator(".rd-del").click();
  await expect(page.locator(".rd-note")).toContainText("Записей пока нет");
  expect(await durations(request, ch.id, "ru")).toEqual([0, 0, 0]);
  await clearRecords(request, token, ch.num);
  assertCleanBut404(guard);
});

test("the English interface has its own takes", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru");
  await record(request, token, ch.num, 1, "en");
  await page.addInitScript(() => window.localStorage.setItem("cs-core-lang", "en"));
  await page.goto(`/book/12/chapter/${ch.id}`);
  await burger(page).click();
  await expect(page.locator(".rd-note")).toContainText("No recordings yet"); // slide 1 has only a Russian take
  await page.keyboard.press("Escape");
  await page.locator(".slide-dot").nth(1).click();
  await burger(page).click();
  await expect(rows(page)).toHaveCount(1);
  page.once("dialog", (d) => void d.accept());
  await rows(page).nth(0).locator(".rd-del").click();
  await expect(page.locator(".rd-note")).toContainText("No recordings yet");
  expect(await durations(request, ch.id, "en")).toEqual([0, 0, 0]);
  expect(await durations(request, ch.id, "ru"), "the Russian take is untouched").toEqual([1, 0, 0]);
  await clearRecords(request, token, ch.num);
});

test("a student does not see the record button and the burger", async ({ page, request }) => {
  await loginViaApi(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel-head")).toBeVisible();
  await expect(page.locator(".slide-rec")).toHaveCount(0);
  await expect(burger(page)).toHaveCount(0);
});
