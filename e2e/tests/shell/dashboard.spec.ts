import { expect, loginFresh, test } from "../../support/fixtures";
import { bookList, DM1, loadChapter, markSlides, progressOf } from "../../support/shell";

/* Home page: overall progress and section cards: three bars (slides, questions, exercises) and chapter squares. */

/** Percentage as in the app: rounded to the nearest integer. */
const pct = (done: number, all: number) => (all === 0 ? 0 : Math.floor((done * 100 + Math.floor(all / 2)) / all));

/** A card bar row by its label ("Слайды", "Вопросы", "Упражнения"). */
const barOf = (c: import("@playwright/test").Locator, label: string) => c.locator(".dash-bar").filter({ has: c.page().locator(".dash-bar-label", { hasText: label }) });

const card = (page: import("@playwright/test").Page, title: string) => page.locator(".dash-card").filter({ has: page.locator(".dash-title", { hasText: title }) });

/** «1 урок», «2 урока», «5 уроков», «21 урок» (Russian plural forms). */
function lessonWord(n: number): string {
  const [n10, n100] = [n % 10, n % 100];
  if (n10 === 1 && n100 !== 11) return "урок";
  if (n10 >= 2 && n10 <= 4 && (n100 < 12 || n100 > 14)) return "урока";
  return "уроков";
}

test("section cards: one per book, with a title, lesson count and slide count", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  await expect(page.locator(".dash-card")).toHaveCount(books.length);
  await expect(page.locator(".dash-title")).toHaveText(books.map((b) => b.title));
  for (const [i, b] of books.entries()) {
    const c = page.locator(".dash-card").nth(i);
    await expect(c.locator(".dash-meta")).toHaveText(`${b.lessons_count} ${lessonWord(b.lessons_count)}`);
    await expect(c.locator(".dash-bar-label")).toHaveText(["Слайды", "Вопросы", "Упражнения"]);
    await expect(barOf(c, "Слайды").locator(".dash-bar-num")).toHaveText(`0/${b.parts_count}`);
  }
  await expect(page.locator(".dash-head h2")).toHaveText("Прогресс");
  await expect(page.locator(".dash-sub")).toHaveText("Разделы");
  guard.assertClean();
});

test("a new user has zero progress: overall, per section and bars", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  const slides = books.reduce((n, b) => n + b.parts_count, 0);
  await page.goto("/");
  // total = slides + questions + exercises: at least as many slides as in the books
  // question and exercise counters arrive in separate requests: wait until the total stops being "slides only"
  await expect.poll(async () => Number(/^0% · 0 из (\d+)$/.exec((await page.locator(".dash-all").textContent()) ?? "")?.[1] ?? 0)).toBeGreaterThan(slides);
  for (const w of await page.locator(".pr-bar i").evaluateAll((els) => els.map((e) => (e as HTMLElement).style.width))) {
    expect(w).toBe("0%");
  }
});

test("clicking the card header opens the section", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  await card(page, "Дискретная математика").locator(".dash-card-head").click();
  await expect(page).toHaveURL(/\/book\/12$/);
  await expect(page.locator(".topics-sec").first()).toBeVisible();
});

test("server progress: viewed slides are visible on the home page and counted per book", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const other = await loadChapter(request, { book: 13, num: 1 });
  await markSlides(request, token, 12, DM1.num, [0, 1, 2, 3]);
  await markSlides(request, token, 13, 1, [0, 5]);
  const books = await bookList(request);
  const dm = books.find((b) => b.id === 12)!;
  const py = books.find((b) => b.id === 13)!;
  expect(ch.lessons.length).toBeGreaterThan(4);
  expect(other.lessons.length).toBeGreaterThan(5);

  await page.goto("/");
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`4/${dm.parts_count}`);
  await expect(barOf(card(page, "Python как первый язык"), "Слайды").locator(".dash-bar-num")).toHaveText(`2/${py.parts_count}`);
  await expect(page.locator(".dash-all")).toHaveText(/^\d+% · 6 из \d+$/);
  const width = await barOf(card(page, "Дискретная математика"), "Слайды").locator(".pr-bar i").evaluate((e) => (e as HTMLElement).style.width);
  expect(width).toBe(`${pct(4, dm.parts_count)}%`);
  // other sections are untouched
  await expect(barOf(card(page, "Алгоритмы и структуры данных"), "Слайды").locator(".dash-bar-num")).toHaveText(/^0\//);
});

test("viewing chapter slides through the interface increases the home page counters", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const books = await bookList(request);
  const dm = books.find((b) => b.id === 12)!;

  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  // the open chapter has already counted the first slide; page through two more with the dots
  await page.locator(".slide-dot").nth(1).click();
  await page.locator(".slide-dot").nth(2).click();
  await expect(page.locator(".slide-panel-num")).toHaveText(`03 / ${ch.lessons.length}`);
  await expect.poll(async () => (await progressOf(request, token)).slides[`12:${DM1.num}`]).toEqual([0, 1, 2]);

  await page.locator(".logo").click();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`3/${dm.parts_count}`);
  await expect(page.locator(".dash-all")).toHaveText(/^\d+% · 3 из \d+$/);

  // viewing the same slides again does not increase the counter
  await page.locator(".dash-card-head", { hasText: "Дискретная математика" }).click();
  await page.locator(".topic-card").first().click();
  await page.locator(".slide-dot").nth(2).click();
  await page.locator(".slide-dot").nth(0).click();
  await page.locator(".logo").click();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`3/${dm.parts_count}`);
});

test("counters are stored on the server: after a reload and a new sign-in the progress is the same", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  await markSlides(request, token, 12, DM1.num, [0, 1]);
  const dm = (await bookList(request)).find((b) => b.id === 12)!;
  await page.goto("/");
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`2/${dm.parts_count}`);
  await page.reload();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`2/${dm.parts_count}`);
});

test("clicking the logo returns to the home page from any page", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/book/12");
  await page.locator(".logo").click();
  await expect(page).toHaveURL(/\/$/);
  await expect(page.locator(".dash-grid")).toBeVisible();
});

// Dashboard specification (AGENTS.md, home page progress dashboard): three bars (slides, questions, exercises) and chapter squares.
test("a section card has \"Вопросы\" and \"Упражнения\" bars", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  const c = page.locator(".dash-card").first();
  await expect(c.locator(".dash-bar-label")).toHaveText(["Слайды", "Вопросы", "Упражнения"]);
});

test("a section card has chapter squares, a click opens the chapter", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  const c = page.locator(".dash-card").filter({ has: page.locator(".dash-title", { hasText: "Дискретная математика" }) });
  // card header + one square for each of the 10 chapters
  await expect(c.locator("button")).toHaveCount(1 + 10);
  await c.locator("button").nth(1).click();
  await expect(page).toHaveURL(/\/book\/12\/chapter\/\d+/);
});

// Defect: for chapter 0 (Python chapter 0; Unix chapter 0) slide views are not saved: POST /api/progress/slides answers 422
// ("chapter: from 1 to 1000", `backend/src/progress.rs`, `check_range`), the client swallows the error silently, so the counter resets after a reload.
test("viewing slides of chapter 0 is saved on the server", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, { book: 13, num: 0 });
  await page.goto(`/book/13/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  await page.locator(".slide-dot").nth(1).click();
  await expect.poll(async () => (await progressOf(request, token)).slides["13:0"]).toEqual([0, 1]);
});
