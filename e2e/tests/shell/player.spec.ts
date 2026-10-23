import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, controlClock, DM1, loadChapter, mmss, progressOf, seconds, stored, words, type ChapterDto } from "../../support/shell";

/* Плеер «озвучки без звука»: абзацы читаются по виртуальным часам (14 символов в секунду, не меньше трёх секунд). Часы страницы
   остановлены и идут только по `page.clock.runFor`, поэтому тесты не ждут настоящих минут. */

const num = (page: Page) => page.locator(".slide-panel-num");
const clockText = (page: Page) => page.locator(".s-time-mono");
const play = (page: Page) => page.locator(".slide-panel-head .slide-btn");
const voice = (page: Page) => page.locator(".voice-pop-text");
const dot = (page: Page, i: number) => page.locator(".slide-dot").nth(i);
/**
 * Клик по точке слайда. Часы страницы остановлены, а ручной выбор слайда уходит в адрес (`?slide=`) через таймер роутера,
 * поэтому после клика даём часам тронуться на долю секунды.
 */
const pick = async (page: Page, i: number) => {
  await dot(page, i).click();
  await page.clock.runFor(100);
};
const pageNum = (ch: ChapterDto, n: number) => `${String(n).padStart(2, "0")} / ${String(ch.lessons.length).padStart(2, "0")}`;

/** Секунды из `м:сс` левой части «позиция / длина». */
async function position(page: Page): Promise<number> {
  const text = (await clockText(page).innerText()).split("/")[0]!.trim();
  const [m, s] = text.split(":").map(Number) as [number, number];
  return m * 60 + s;
}

/** Номер подсвеченного («читаемого») слова в окне «За кадром»; -1, если слова не подсвечены. */
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

test("исходное состояние: первый слайд, время 0:00 из длины главы, «Играть», слова не подсвечены", async ({ page, request, guard }) => {
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

test("«Играть» запускает чтение: «Пауза», время идёт, слова подсвечиваются по порядку", async ({ page, request }) => {
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
  // слова до читаемого — прочитанные, после — ожидающие
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(later);
  await expect(page.locator(".voice-pop-text .next")).toHaveCount(wordCount - later - 1);
});

test("слайды сменяются сами: по концу абзаца — следующий слайд и его текст", async ({ page, request }) => {
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
  // позиция в главе — сумма прочитанного абзаца и времени внутри нового
  const pos = await position(page);
  expect(pos).toBeGreaterThanOrEqual(Math.floor(durs[0]!));
  expect(pos).toBeLessThanOrEqual(Math.ceil(durs[0]! + 2));
  await expect(play(page)).toHaveText("Пауза");
  // и дальше: ещё абзац
  await page.clock.runFor(durs[1]! * 1000);
  await expect(num(page)).toHaveText(pageNum(ch, 3));
  await expect(voice(page)).toHaveText(words(ch.lessons[2]!.text));
});

test("«Пауза» останавливает чтение, «Играть» продолжает без учёта времени паузы", async ({ page, request }) => {
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
  await expect(num(page)).toHaveText(pageNum(ch, 1)); // слайд не меняется
  expect(await position(page)).toBe(t);
  expect(await nowWord(page)).toBe(w);
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(1); // чтение «на месте»
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
  await page.clock.runFor(1000);
  const after = await position(page);
  expect(after - t).toBeGreaterThanOrEqual(0);
  expect(after - t).toBeLessThanOrEqual(3); // а не 120 секунд паузы
  await expect(num(page)).toHaveText(pageNum(ch, 1));
});

test("клик по слайду при остановленном плеере показывает слайд и не запускает чтение", async ({ page, request }) => {
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
  await expect(num(page)).toHaveText(pageNum(ch, 5)); // сам не листается
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
});

test("«Играть» после ручного выбора начинает чтение с выбранного слайда", async ({ page, request }) => {
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

test("клик по слайду во время чтения начинает чтение с него «с начала абзаца»", async ({ page, request }) => {
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
  await expect(page.locator(".voice-pop-text .past")).toHaveCount(0); // чтение идёт с первого слова
  const start = durs.slice(0, 8).reduce((a, b) => a + b, 0);
  expect(await position(page)).toBeGreaterThanOrEqual(Math.floor(start));
  expect(await position(page)).toBeLessThanOrEqual(Math.ceil(start + 1));
  await page.clock.runFor(durs[8]! * 1000 + 1000);
  await expect(num(page)).toHaveText(pageNum(ch, 10));
});

test("клик по текущему слайду на паузе возобновляет чтение", async ({ page, request }) => {
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
  expect(await position(page)).toBeGreaterThanOrEqual(t); // с места паузы, не с начала
  await expect(num(page)).toHaveText(pageNum(ch, 1));
});

test("окно «За кадром» показывает абзац текущего слайда на любом слайде главы", async ({ page, request }) => {
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

test("окно «За кадром» закреплено у нижнего края и стоит по центру колонки главы", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  const pop = (await page.locator(".voice-pop").boundingBox())!;
  const content = (await page.locator(".content").boundingBox())!;
  const viewport = page.viewportSize()!;
  expect(Math.abs(pop.x + pop.width / 2 - (content.x + content.width / 2))).toBeLessThan(4);
  expect(viewport.height - (pop.y + pop.height)).toBeLessThan(40);
  // полная высота окна доступна плееру и полям страницы
  const varPx = await page.evaluate(() => parseFloat(document.documentElement.style.getPropertyValue("--voice-h")));
  expect(Math.abs(varPx - pop.height)).toBeLessThan(2);
});

test("высота окна «За кадром»: двойной клик по «лапке» возвращает по умолчанию, перетаскивание запоминает", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await page.addInitScript(() => window.localStorage.setItem("say-voice-h", "100"));
  await open(page, ch);
  await expect(voice(page)).toHaveAttribute("style", /max-height: min\(100px, 70vh\)/);
  const grip = page.locator(".voice-pop-grip");
  await grip.dblclick();
  await expect(voice(page)).not.toHaveAttribute("style", /max-height/);
  expect(await stored(page, "say-voice-h")).toBeNull();

  const g = (await grip.boundingBox())!;
  await page.mouse.move(g.x + g.width / 2, g.y + g.height / 2);
  await page.mouse.down();
  await page.mouse.move(g.x + g.width / 2, g.y - 60, { steps: 4 });
  await page.mouse.up();
  const saved = await stored(page, "say-voice-h");
  expect(saved).not.toBeNull();
  expect(Number(saved)).toBeGreaterThan(0);
});

test("адрес ?slide=: ручной выбор попадает в адрес, перезагрузка возвращает на тот же слайд", async ({ page, request }) => {
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

test("адрес ?slide=: заход по ссылке, выход за границы и мусор в значении", async ({ page, request }) => {
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

test("при уходе со страницы чтение останавливается: после возвращения — «Играть» и 0:00", async ({ page, request }) => {
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

test("переход в левом меню разделов останавливает чтение", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(2000);
  await page.locator(".sidebar .slide-fs-toc-item").nth(1).click(); // другой раздел
  await expect(page).toHaveURL(/\/book\/13$/);
  await page.goBack(); // та же вкладка приложения, без перезагрузки: плеер не должен «доиграть» в фоне
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(play(page)).toHaveText("Играть");
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
});

test("чтение последнего абзаца заканчивается остановкой: «Играть», слова не подсвечены", async ({ page, request }) => {
  const { ch, durs } = await setup(page, request);
  const last = ch.lessons.length - 1;
  await open(page, ch, `?slide=${last}`);
  await play(page).click();
  await expect(num(page)).toHaveText(pageNum(ch, last + 1));
  await page.clock.runFor(durs[last]! * 1000 + 2000);
  await expect(play(page)).toHaveText("Играть");
  await expect(page.locator(".voice-pop-text .now")).toHaveCount(0);
  // проигрыватель можно запустить снова
  await play(page).click();
  await expect(play(page)).toHaveText("Пауза");
});

test("слайды, прочитанные плеером, попадают в прогресс", async ({ page, request }) => {
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

test("окно «За кадром» только на вкладке теории", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
  await expect(page.locator(".quiz-q").first()).toBeVisible();
  await expect(page.locator(".voice-pop")).toHaveCount(0);
  await page.locator(".ch-tab", { hasText: "Теория" }).click();
  await expect(page.locator(".voice-pop")).toBeVisible();
  await expect(voice(page)).toHaveText(words(ch.lessons[0]!.text));
});

test("смена вкладки во время чтения останавливает плеер", async ({ page, request }) => {
  const { ch } = await setup(page, request);
  await open(page, ch);
  await play(page).click();
  await page.clock.runFor(2000);
  await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
  await expect(page.locator(".quiz-q").first()).toBeVisible();
  await page.locator(".ch-tab", { hasText: "Теория" }).click();
  await expect(play(page)).toHaveText("Играть");
});
