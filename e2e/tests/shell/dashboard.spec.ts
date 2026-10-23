import { expect, loginFresh, test } from "../../support/fixtures";
import { bookList, DM1, loadChapter, markSlides, progressOf } from "../../support/shell";

/* Главная: общий прогресс и карточки разделов: три полосы (слайды, вопросы, упражнения) и квадратики глав. */

/** Процент как в приложении: округление к ближайшему целому. */
const pct = (done: number, all: number) => (all === 0 ? 0 : Math.floor((done * 100 + Math.floor(all / 2)) / all));

/** Строка полосы карточки по подписи («Слайды», «Вопросы», «Упражнения»). */
const barOf = (c: import("@playwright/test").Locator, label: string) => c.locator(".dash-bar").filter({ has: c.page().locator(".dash-bar-label", { hasText: label }) });

const card = (page: import("@playwright/test").Page, title: string) => page.locator(".dash-card").filter({ has: page.locator(".dash-title", { hasText: title }) });

test("карточки разделов: по одной на книгу, с названием, числом уроков и слайдов", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  await expect(page.locator(".dash-card")).toHaveCount(books.length);
  await expect(page.locator(".dash-title")).toHaveText(books.map((b) => b.title));
  for (const [i, b] of books.entries()) {
    const c = page.locator(".dash-card").nth(i);
    await expect(c.locator(".dash-meta")).toHaveText(`${b.lessons_count} уроков`);
    await expect(c.locator(".dash-bar-label")).toHaveText(["Слайды", "Вопросы", "Упражнения"]);
    await expect(barOf(c, "Слайды").locator(".dash-bar-num")).toHaveText(`0/${b.parts_count}`);
  }
  await expect(page.locator(".dash-head h2")).toHaveText("Прогресс");
  await expect(page.locator(".dash-sub")).toHaveText("Разделы");
  guard.assertClean();
});

test("у нового пользователя прогресс нулевой: общий, по разделам и полосы", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  const slides = books.reduce((n, b) => n + b.parts_count, 0);
  await page.goto("/");
  // всего = слайды + вопросы + упражнения: слайдов не меньше, чем в книгах
  // счётчики вопросов и упражнений приходят отдельными запросами — ждём, пока итог перестанет быть «одни слайды»
  await expect.poll(async () => Number(/^0% · 0 из (\d+)$/.exec((await page.locator(".dash-all").textContent()) ?? "")?.[1] ?? 0)).toBeGreaterThan(slides);
  for (const w of await page.locator(".pr-bar i").evaluateAll((els) => els.map((e) => (e as HTMLElement).style.width))) {
    expect(w).toBe("0%");
  }
});

test("клик по шапке карточки открывает раздел", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  await card(page, "Дискретная математика").locator(".dash-card-head").click();
  await expect(page).toHaveURL(/\/book\/12$/);
  await expect(page.locator(".topics-sec").first()).toBeVisible();
});

test("прогресс с сервера: просмотренные слайды видны на главной и считаются по книгам", async ({ page, request }) => {
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
  // остальные разделы не тронуты
  await expect(barOf(card(page, "Алгоритмы и структуры данных"), "Слайды").locator(".dash-bar-num")).toHaveText(/^0\//);
});

test("просмотр слайдов главы через интерфейс увеличивает счётчики на главной", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const books = await bookList(request);
  const dm = books.find((b) => b.id === 12)!;

  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  // открытая глава уже засчитала первый слайд; листаем точками ещё два
  await page.locator(".slide-dot").nth(1).click();
  await page.locator(".slide-dot").nth(2).click();
  await expect(page.locator(".slide-panel-num")).toHaveText(`03 / ${ch.lessons.length}`);
  await expect.poll(async () => (await progressOf(request, token)).slides[`12:${DM1.num}`]).toEqual([0, 1, 2]);

  await page.locator(".logo").click();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`3/${dm.parts_count}`);
  await expect(page.locator(".dash-all")).toHaveText(/^\d+% · 3 из \d+$/);

  // повторный просмотр тех же слайдов счётчик не увеличивает
  await page.locator(".dash-card-head", { hasText: "Дискретная математика" }).click();
  await page.locator(".topic-card").first().click();
  await page.locator(".slide-dot").nth(2).click();
  await page.locator(".slide-dot").nth(0).click();
  await page.locator(".logo").click();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`3/${dm.parts_count}`);
});

test("счётчики хранятся на сервере: после перезагрузки и нового входа прогресс тот же", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  await markSlides(request, token, 12, DM1.num, [0, 1]);
  const dm = (await bookList(request)).find((b) => b.id === 12)!;
  await page.goto("/");
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`2/${dm.parts_count}`);
  await page.reload();
  await expect(barOf(card(page, "Дискретная математика"), "Слайды").locator(".dash-bar-num")).toHaveText(`2/${dm.parts_count}`);
});

test("клик по логотипу возвращает на главную с любой страницы", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/book/12");
  await page.locator(".logo").click();
  await expect(page).toHaveURL(/\/$/);
  await expect(page.locator(".dash-grid")).toBeVisible();
});

// Спецификация дашборда (AGENTS.md, «Главная: дашборд прогресса»): три полосы — слайды, вопросы, упражнения — и квадратики глав.
test("на карточке раздела есть полосы «Вопросы» и «Упражнения»", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  const c = page.locator(".dash-card").first();
  await expect(c.locator(".dash-bar-label")).toHaveText(["Слайды", "Вопросы", "Упражнения"]);
});

test("на карточке раздела есть квадратики глав, клик открывает главу", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  const c = page.locator(".dash-card").filter({ has: page.locator(".dash-title", { hasText: "Дискретная математика" }) });
  // шапка карточки + по одному квадратику на каждую из 10 глав
  await expect(c.locator("button")).toHaveCount(1 + 10);
  await c.locator("button").nth(1).click();
  await expect(page).toHaveURL(/\/book\/12\/chapter\/\d+/);
});

// Дефект: у главы 0 (Python, глава 0; Unix, глава 0) просмотры слайдов не сохраняются: POST /api/progress/slides отвечает 422
// («chapter: от 1 до 1000», `backend-rs/src/progress.rs`, `check_range`), клиент ошибку молча глотает — после перезагрузки счётчик обнуляется.
test("просмотр слайдов главы 0 сохраняется на сервере", async ({ page, request }) => {
  const { token } = await loginFresh(page, request);
  const ch = await loadChapter(request, { book: 13, num: 0 });
  await page.goto(`/book/13/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  await page.locator(".slide-dot").nth(1).click();
  await expect.poll(async () => (await progressOf(request, token)).slides["13:0"]).toEqual([0, 1]);
});
