import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, controlClock, DM1, loadChapter, mmss, progressOf, seconds, stored, words, type ChapterDto } from "../../support/shell";

/* The "voice-over without sound" player: paragraphs are read on a virtual clock (14 characters per second, at least three seconds). The page clock
   is stopped and advances only via `page.clock.runFor`, so tests never wait real minutes. */

const num = (page: Page) => page.locator(".slide-panel-num");
const clockText = (page: Page) => page.locator(".s-time-mono");
const play = (page: Page) => page.locator(".slide-panel-head .slide-btn:not(.slide-skip)");
const back = (page: Page) => page.getByRole("button", { name: /^Назад:/ });
const forward = (page: Page) => page.getByRole("button", { name: /^Вперёд:/ });
const voice = (page: Page) => page.locator(".voice-pop-text");
const dot = (page: Page, i: number) => page.locator(".slide-dot").nth(i);
/**
 * Click a slide dot. The page clock is stopped, and a manual slide choice goes into the URL (`?slide=`) via a router timer,
 * so after the click we let the clock advance a fraction of a second.
 */
const pick = async (page: Page, i: number) => {
  await dot(page, i).click();
  await page.clock.runFor(100);
};
const pageNum = (ch: ChapterDto, n: number) => `${String(n).padStart(2, "0")} / ${String(ch.lessons.length).padStart(2, "0")}`;

/** Seconds from the `m:ss` left part of "position / length". */
async function position(page: Page): Promise<number> {
  const text = (await clockText(page).innerText()).split("/")[0]!.trim();
  const [m, s] = text.split(":").map(Number) as [number, number];
  return m * 60 + s;
}

/** Index of the highlighted ("being read") word in the voice-over window; -1 if no word is highlighted. */
const nowWord = (page: Page) => page.locator(".voice-pop-text span").evaluateAll((els) => els.findIndex((e) => e.classList.contains("now")));

async function open(page: Page, ch: ChapterDto, query = "") {
  await page.goto(`/book/12/chapter/${ch.id}${query}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(voice(page)).toBeVisible();
}

const setup = async (page: Page, request: import("@playwright/test").APIRequestContext) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const durs = ch.lessons.map((l) => seconds(l.text));
  await controlClock(page);
  return { ch, durs, total: durs.reduce((a, b) => a + b, 0) };
};

test("initial state: first slide, time 0:00 of the chapter length, Play, no words highlighted", async ({ page, request, guard }) => {
  const { ch, total } = await setup(page, request);
  await open(page, ch);
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await expect(clockText(page)).toHaveText(`0:00 / ${mmss(total)}`);
  await expect(play(page)).toHaveText("Играть");
  await expect(play(page)).toHaveAttribute("title", "Играть");
  await expect(dot(page, 0)).toHaveClass(/\bon\b/);
  await expect(page.locator(".voice-pop-text .now, .voice-pop-text .past")).toHaveCount(0);
  assertCleanBut404(guard);
});

test("Play starts reading: Pause shown, time runs, words are highlighted in order", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(1000);
  await expect(clockText(page)).toContainText("0:01 / ");
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1);
  const wordCount = await page.locator(".voice-pop-text span").count();
  const early = await nowWord(page);
  expect(early).toBeGreaterThanOrEqual(0);
  await page.clock.runFor(10_000);
  const later = await nowWord(page);
  expect(later).toBeGreaterThan(early);
  // words before the current one are read, after it are pending
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(later);
  await expect(page.locator(".voice-pop-text .next")).toHaveCount(wordCount - later - 1);
});

test("slides advance on their own: at the end of a paragraph, the next slide and its text", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(durs[0]! * 1000 - 3000);
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await page.clock.runFor(4000);
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await expect(voice(page)).toHaveText(words(ch.lessons[1]!.text));
  await expect(dot(page, 1)).toHaveClass(/\bon\b/);
  await expect(dot(page, 0)).not.toHaveClass(/\bon\b/);
  // position in the chapter is the sum of the finished paragraph and the time inside the new one
  const pos = await position(page);
  expect(pos).toBeGreaterThanOrEqual(Math.floor(durs[0]!));
  expect(pos).toBeLessThanOrEqual(Math.ceil(durs[0]! + 2));
  await expect(play(page)).toHaveText("Пауза");
  // and on: another paragraph
  await page.clock.runFor(durs[1]! * 1000);
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect(voice(page)).toHaveText(words(ch.lessons[2]!.text));
});

test("Pause stops reading, Play resumes ignoring the paused time", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(5000);
  await play(page).click();
  await expect(play(page)).toHaveText("Играть");
  const t = await position(page);
  const w = await nowWord(page);
  expect(t).toBeGreaterThanOrEqual(4);
  await page.clock.runFor(120_000);
  await expect(num(page)).toHaveText(pageNum(ch, 1)); // the slide does not change
  expect(await position(page)).toBe(t);
  expect(await nowWord(page)).toBe(w);
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1); // reading stays in place
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(1000);
  const after = await position(page);
  expect(after - t).toBeGreaterThanOrEqual(0);
  expect(after - t).toBeLessThanOrEqual(3); // not the 120 seconds of pause
  await expect(num(page)).toHaveText(pageNum(ch, 1));
});

test("clicking a slide while the player is stopped shows the slide and does not start reading", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  await open(page, ch);
  await pick(page, 4);
  await expect(num(page)).toHaveText(pageNum(ch, 5));
  await expect(voice(page)).toHaveText(words(ch.lessons[4]!.text));
  await expect(play(page)).toHaveText("Играть");
  await expect(dot(page, 4)).toHaveClass(/\bon\b/);
  const before = durs.slice(0, 4).reduce((a, b) => a + b, 0);
  await expect(clockText(page)).toContainText(`${mmss(before)} / `);
  await page.clock.runFor(60_000);
  await expect(num(page)).toHaveText(pageNum(ch, 5)); // does not turn pages by itself
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
});

test("Play after a manual choice starts reading from the chosen slide", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  await open(page, ch);
  await pick(page, 4);
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(1000);
  await expect(num(page)).toHaveText(pageNum(ch, 5));
  await expect(voice(page)).toHaveText(words(ch.lessons[4]!.text));
  const before = durs.slice(0, 4).reduce((a, b) => a + b, 0);
  const pos = await position(page);
  expect(pos).toBeGreaterThanOrEqual(Math.floor(before));
  expect(pos).toBeLessThanOrEqual(Math.ceil(before + 3));
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1);
});

test("clicking a slide during reading starts reading from the start of its paragraph", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(8000);
  const wordsBefore = await nowWord(page);
  expect(wordsBefore).toBeGreaterThan(3);
  await pick(page, 8);
  await expect(num(page)).toHaveText(pageNum(ch, 9));
  await expect(voice(page)).toHaveText(words(ch.lessons[8]!.text));
  await expect(play(page)).toHaveText("Пауза");
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(0); // reading goes from the first word
  const start = durs.slice(0, 8).reduce((a, b) => a + b, 0);
  expect(await position(page)).toBeGreaterThanOrEqual(Math.floor(start));
  expect(await position(page)).toBeLessThanOrEqual(Math.ceil(start + 1));
  await page.clock.runFor(durs[8]! * 1000 + 1000);
  await expect(num(page)).toHaveText(pageNum(ch, 10));
});

test("clicking the current slide while paused resumes reading", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(3000);
  await play(page).click();
  await expect(play(page)).toHaveText("Играть");
  const t = await position(page);
  await pick(page, 0);
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(1000);
  expect(await position(page)).toBeGreaterThanOrEqual(t); // from the paused position, not from the start
  await expect(num(page)).toHaveText(pageNum(ch, 1));
});

test("the voice-over window shows the current slide's paragraph on any slide of the chapter", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await expect(page.locator(".voice-pop")).toHaveCount(1);
  await expect(page.locator(".voice-pop")).toHaveAttribute("role", "region");
  await expect(page.locator(".voice-pop .voice-pop-tag")).toHaveText("За кадром");
  for (const i of [0, 1, 6, ch.lessons.length - 1, 3]) {
    await pick(page, i);
    await expect(num(page)).toHaveText(pageNum(ch, i + 1));
    await expect(voice(page)).toHaveText(words(ch.lessons[i]!.text));
    await expect(page.locator(".voice-pop")).toHaveCount(1);
  }
});

test("the voice-over window is pinned to the bottom edge and centred on the chapter column", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  const pop = (await page.locator(".voice-pop").boundingBox())!;
  const content = (await page.locator(".content").boundingBox())!;
  const viewport = page.viewportSize()!;
  expect(Math.abs(pop.x + pop.width / 2 - (content.x + content.width / 2))).toBeLessThan(4);
  expect(viewport.height - (pop.y + pop.height)).toBeLessThan(40);
  // the full window height is available to the player and page margins
  const varPx = await page.evaluate(() => parseFloat(document.documentElement.style.getPropertyValue("--voice-h")));
  expect(Math.abs(varPx - pop.height)).toBeLessThan(2);
});

test("voice-over window height: double-clicking the handle restores the default, dragging is remembered", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await page.addInitScript(() => window.localStorage.setItem("cs-core-voice-h", "100"));
  await open(page, ch);
  await expect(voice(page)).toHaveAttribute("style", /max-height: min\(100px, 70vh\)/);
  const grip = page.locator(".voice-pop-grip");
  await grip.dblclick();
  await expect(voice(page)).not.toHaveAttribute("style", /max-height/);
  expect(await stored(page, "cs-core-voice-h")).toBeNull();

  const g = (await grip.boundingBox())!;
  await page.mouse.move(g.x + g.width / 2, g.y + g.height / 2);
  await page.mouse.down();
  await page.mouse.move(g.x + g.width / 2, g.y - 60, { steps: 4 });
  await page.mouse.up();
  const saved = await stored(page, "cs-core-voice-h");
  expect(saved).not.toBeNull();
  expect(Number(saved)).toBeGreaterThan(0);
});

test("?slide= URL: a manual choice goes into the URL, reload returns to the same slide", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  expect(new URL(page.url()).searchParams.get("slide")).toBeNull();
  await pick(page, 3);
  await expect.poll(() => new URL(page.url()).searchParams.get("slide")).toBe("3");
  await page.reload();
  await expect(num(page)).toHaveText(pageNum(ch, 4));
  await expect(dot(page, 3)).toHaveClass(/\bon\b/);
  await expect(voice(page)).toHaveText(words(ch.lessons[3]!.text));
  await expect(play(page)).toHaveText("Играть");
});

test("?slide= URL: opening by link, out-of-range and garbage values", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch, "?slide=5");
  await expect(num(page)).toHaveText(pageNum(ch, 6));
  await expect(voice(page)).toHaveText(words(ch.lessons[5]!.text));
  await open(page, ch, "?slide=999");
  await expect(num(page)).toHaveText(pageNum(ch, ch.lessons.length));
  await open(page, ch, "?slide=abc");
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await open(page, ch, "?slide=0");
  await expect(num(page)).toHaveText(pageNum(ch, 1));
});

test("leaving the page stops reading: after returning, Play and 0:00", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(4000);
  await expect(play(page)).toHaveText("Пауза");
  await page.locator(".logo").click();
  await expect(page.locator(".dash-grid")).toBeVisible();
  await page.goBack();
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(play(page)).toHaveText("Играть");
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await expect(clockText(page)).toContainText("0:00 / ");
});

test("navigating in the left sections menu stops reading", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(2000);
  await page.locator(".sidebar .slide-fs-toc-item").nth(1).click(); // another section
  await expect(page).toHaveURL(/\/book\/13$/);
  await page.goBack(); // same app tab, no reload: the player must not keep playing in the background
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(play(page)).toHaveText("Играть");
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
});

test("reading the last paragraph ends with a stop: Play, no words highlighted", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  const last = ch.lessons.length - 1;
  await open(page, ch, `?slide=${last}`);
  await play(page).click();
  await expect(num(page)).toHaveText(pageNum(ch, last + 1));
  await page.clock.runFor(durs[last]! * 1000 + 2000);
  await expect(play(page)).toHaveText("Играть");
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
  // the player can be started again
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
});

test("slides read by the player count towards progress", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const durs = ch.lessons.map((l) => seconds(l.text));
  await controlClock(page);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor((durs[0]! + durs[1]!) * 1000 + 1500);
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect.poll(async () => (await progressOf(request, token)).slides[`12:${DM1.num}`]).toEqual([0, 1, 2]);
});

test("the voice-over window appears only on the theory tab", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
  await expect(page.locator(".quiz-q").first()).toBeVisible();
  await expect(page.locator(".voice-pop")).toHaveCount(0);
  await page.locator(".ch-tab", { hasText: "Теория" }).click();
  await expect(page.locator(".voice-pop")).toBeVisible();
  await expect(voice(page)).toHaveText(words(ch.lessons[0]!.text));
});

test("switching tabs during reading stops the player", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(2000);
  await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
  await expect(page.locator(".quiz-q").first()).toBeVisible();
  await page.locator(".ch-tab", { hasText: "Теория" }).click();
  await expect(play(page)).toHaveText("Играть");
});

test("the chapter slider rewinds: the slide, the time and the text follow, a paused player stays paused", async ({ page, request }) => {
  const { ch, durs, total } = await setup(page, request);
  await open(page, ch);
  const seek = page.locator(".slide-seek");
  await expect(seek).toHaveAttribute("max", String(total));
  const target = Math.ceil(durs[0]! + durs[1]!) + 2;
  await seek.fill(String(target));
  await expect(num(page)).toHaveText(pageNum(ch, 3)); // the third paragraph
  await expect(voice(page)).toHaveText(words(ch.lessons[2]!.text));
  await expect(play(page)).toHaveText("Пауза"); // a stopped player starts from the chosen place
  expect(await position(page)).toBeGreaterThanOrEqual(Math.floor(target));
  expect(await position(page)).toBeLessThanOrEqual(Math.ceil(target + 1));
  // back to the start while paused: stays paused
  await play(page).click();
  await expect(play(page)).toHaveText("Играть");
  await seek.fill("0");
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await expect(play(page)).toHaveText("Играть");
  await page.clock.runFor(5000);
  await expect(clockText(page)).toContainText("0:00 / ");
});

test("volume: the slider and the mute button, the level is remembered", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  const range = page.locator(".slide-vol-range");
  await expect(range).toHaveValue("1");
  await range.fill("0.4");
  await expect.poll(() => stored(page, "cs-core-volume")).toBe("0.4");
  await page.locator(".slide-vol-btn").click(); // mute
  await expect(range).toHaveValue("0");
  await page.locator(".slide-vol-btn").click(); // back to the previous level
  await expect(range).toHaveValue("0.4");
  await page.reload();
  await expect(page.locator(".slide-vol-range")).toHaveValue("0.4");
});

test("Back and Forward on a stopped player turn the slides: back from the start goes to the previous slide", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await expect(play(page)).toHaveText("Играть");
  await forward(page).click();
  await page.clock.runFor(100); // a manual choice goes into the URL via a router timer
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await forward(page).click();
  await page.clock.runFor(100); // a manual choice goes into the URL via a router timer
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect(play(page)).toHaveText("Играть"); // nothing starts by itself
  await back(page).click();
  await page.clock.runFor(100);
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await back(page).click();
  await page.clock.runFor(100);
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await back(page).click();
  await page.clock.runFor(100); // the first slide has no previous one
  await expect(num(page)).toHaveText(pageNum(ch, 1));
  await pick(page, ch.lessons.length - 1);
  await expect(forward(page)).toBeDisabled();
});

test("Back during reading: to the start of the slide, and when already at the start - to the previous slide", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await pick(page, 2);
  await play(page).click();
  await page.clock.runFor(6000);
  expect(await nowWord(page)).toBeGreaterThan(2);
  await back(page).click(); // far from the start: the same slide from its start
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(0);
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(500);
  await back(page).click(); // at the start: the previous slide
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await expect(play(page)).toHaveText("Пауза");
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(0);
  await forward(page).click();
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect(play(page)).toHaveText("Пауза"); // reading goes on
  await page.clock.runFor(1000);
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1);
});

test("Forward on a paused player moves to the next slide and stays paused", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(2000);
  await play(page).click(); // pause
  await expect(play(page)).toHaveText("Играть");
  await forward(page).click();
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await expect(play(page)).toHaveText("Играть");
  await page.clock.runFor(5000);
  await expect(num(page)).toHaveText(pageNum(ch, 2));
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(0); // a pause does not read
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(2000);
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1);
});
