import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, bookList, courseOf, DM1, loadChapter, PY0, type SectionDto } from "../../support/shell";

/* Страница книги: разделы и карточки глав, переход в главу, вкладки главы по содержимому и их адреса. */

test("страница книги: разделы и карточки глав как в API", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const course = await courseOf(request, 12);
  await page.goto("/book/12");
  await expect(page.locator(".topics-sec")).toHaveCount(course.length);
  await expect(page.locator(".topics-title")).toHaveText(course.map((s) => s.title));
  for (const [i, sec] of course.entries()) {
    const cards = page.locator(".topics-sec").nth(i).locator(".topic-card");
    await expect(cards).toHaveCount(sec.chapters.length);
    await expect(cards.locator(".topic-name")).toHaveText(sec.chapters.map((c) => c.title));
    await expect(cards.locator(".topic-num")).toHaveText(sec.chapters.map((c) => String(c.num).padStart(2, "0")));
    // число слайдов — из данных главы
    await expect(cards.locator(".topic-meta")).toHaveText(sec.chapters.map((c) => `${c.parts_count} слайдов`));
  }
  guard.assertClean();
});

test("число глав и слайдов в разделах сходится с карточкой книги", async ({ page, request }) => {
  await loginFresh(page, request);
  for (const b of await bookList(request)) {
    const course = await courseOf(request, b.id);
    expect(course.length, `разделов в «${b.title}»`).toBeGreaterThan(0);
    expect(course.flatMap((s) => s.chapters).length, `глав в «${b.title}»`).toBe(b.lessons_count);
    expect(course.flatMap((s) => s.chapters).reduce((n, c) => n + c.parts_count, 0), `слайдов в «${b.title}»`).toBe(b.parts_count);
  }
  await page.goto("/book/13");
  await expect(page.locator(".topic-card")).toHaveCount((await bookList(request)).find((b) => b.id === 13)!.lessons_count);
});

test("слева в разделе — меню уроков со всеми главами; клик открывает главу", async ({ page, request }) => {
  await loginFresh(page, request);
  const course = await courseOf(request, 12);
  const all = course.flatMap((s) => s.chapters);
  await page.goto("/book/12");
  const menu = page.locator(".lessons-menu");
  await expect(menu.locator(".s-label").first()).toHaveText("Дискретная математика");
  await expect(menu.locator(".lessons-sec")).toHaveText(course.map((s) => s.title));
  await expect(menu.locator(".slide-fs-toc-item")).toHaveCount(all.length);
  await expect(menu.locator(".slide-fs-toc-item.on")).toHaveCount(0);
  await menu.locator(".slide-fs-toc-item", { hasText: all[1]!.title }).click();
  await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${all[1]!.id}$`));
  await expect(page.locator("h2")).toHaveText(`Урок ${all[1]!.num}. ${all[1]!.title}`);
  // в главе тот же пункт меню подсвечен
  await expect(menu.locator(".slide-fs-toc-item.on")).toHaveCount(1);
  await expect(menu.locator(".slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(all[1]!.title);
});

test("клик по карточке главы открывает её теорию: заголовок, раздел, слайды", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto("/book/12");
  await page.locator(".topic-card", { hasText: ch.title }).first().click();
  await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${ch.id}$`));
  await expect(page.locator("h2")).toHaveText(`Урок ${ch.num}. ${ch.title}`);
  await expect(page.locator(".crumbs")).toHaveText(ch.section);
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(page.locator(".slide-panel-num")).toHaveText(`01 / ${ch.lessons.length}`);
  await expect(page.locator(".slide-dot")).toHaveCount(ch.lessons.length);
  assertCleanBut404(guard);
});

test("вкладки главы: Теория, Вопросы с числом вопросов, Практика со счётчиком задач", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, PY0);
  await page.goto(`/book/13/chapter/${ch.id}`);
  const tabs = page.locator(".ch-tab");
  await expect(tabs).toHaveCount(3);
  await expect(tabs.nth(0)).toHaveText("Теория");
  await expect(tabs.nth(1)).toContainText("Вопросы");
  await expect(tabs.nth(1).locator(".ch-tab-badge")).toHaveText("5");
  await expect(tabs.nth(2)).toContainText("Практика");
  await expect(tabs.nth(2).locator(".ch-tab-badge")).toHaveText("0/6"); // решено 0 из 6
});

test("у главы с упражнениями на ввод ответа вкладка «Практика» без счётчика", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".ch-tab")).toHaveCount(3);
  await expect(page.locator(".ch-tab").nth(2)).toContainText("Практика");
  await expect(page.locator(".ch-tab").nth(2).locator(".ch-tab-badge")).toHaveCount(0);
});

test("набор вкладок определяется содержимым главы (по одной главе каждой книги)", async ({ page, request }) => {
  await loginFresh(page, request);
  const quizzes = (await (await request.get("/api/quizzes")).json()) as Record<string, Record<string, number>>;
  const answers = (await (await request.get("/api/answers")).json()) as Record<string, Record<string, number>>;
  const slides = (await (await request.get("/api/slides")).json()) as { book: number; chapter: number }[];
  for (const b of await bookList(request)) {
    const sec: SectionDto | undefined = (await courseOf(request, b.id))[0];
    const first = sec?.chapters[0];
    if (!first) throw new Error(`в книге ${b.id} нет глав`);
    const tasks = await request.get(`/api/exercises/${b.id}/${first.num}`);
    const taskCount = tasks.ok() ? ((await tasks.json()) as { tasks: unknown[] }).tasks.length : 0;
    const expected: string[] = [];
    if (slides.some((s) => s.book === b.id && s.chapter === first.num)) expected.push("Теория");
    if ((quizzes[String(b.id)]?.[String(first.num)] ?? 0) > 0) expected.push("Вопросы");
    if (taskCount > 0 || (answers[String(b.id)]?.[String(first.num)] ?? 0) > 0) expected.push("Практика");

    await page.goto(`/book/${b.id}/chapter/${first.id}`);
    await expect(page.locator("h2")).toContainText(`Урок ${first.num}.`);
    await expect(async () => {
      const names = (await page.locator(".ch-tab").allInnerTexts()).map((t) => t.split("\n")[0]);
      expect(names, `вкладки ${b.id}:${first.num}`).toEqual(expected);
    }).toPass();
  }
});

test("адреса вкладок: теория без суффикса, /questions, /exercises; активная подсвечена", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  const base = `/book/12/chapter/${ch.id}`;
  await page.goto(base);
  const tab = (name: string) => page.locator(".ch-tab", { hasText: name });
  await expect(tab("Теория")).toHaveClass(/\bon\b/);
  await expect(tab("Вопросы")).not.toHaveClass(/\bon\b/);
  await expect(tab("Теория")).toHaveAttribute("href", base);
  await expect(tab("Вопросы")).toHaveAttribute("href", `${base}/questions`);
  await expect(tab("Практика")).toHaveAttribute("href", `${base}/exercises`);

  await tab("Вопросы").click();
  await expect(page).toHaveURL(new RegExp(`${base}/questions$`));
  await expect(tab("Вопросы")).toHaveClass(/\bon\b/);
  await expect(tab("Теория")).not.toHaveClass(/\bon\b/);
  await expect(page.locator(".slide-panel")).toHaveCount(0);

  await tab("Практика").click();
  await expect(page).toHaveURL(new RegExp(`${base}/exercises$`));
  await expect(tab("Практика")).toHaveClass(/\bon\b/);

  await tab("Теория").click();
  await expect(page).toHaveURL(new RegExp(`${base}$`));
  await expect(page.locator(".slide-panel")).toBeVisible();
});

test("прямой заход на адрес вкладки открывает её; перезагрузка не сбрасывает вкладку", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  for (const [sub, name] of [["questions", "Вопросы"], ["exercises", "Практика"]] as const) {
    await page.goto(`/book/12/chapter/${ch.id}/${sub}`);
    await expect(page.locator(".ch-tab.on")).toContainText(name);
    await page.reload();
    await expect(page.locator(".ch-tab.on")).toContainText(name);
    expect(new URL(page.url()).pathname).toBe(`/book/12/chapter/${ch.id}/${sub}`);
  }
});

test("вкладка «Вопросы» показывает пять вопросов главы", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}/questions`);
  await expect(page.locator(".ch-tab.on")).toContainText("Вопросы");
  await expect(page.locator(".quiz-q")).toHaveCount(5);
  await expect(page.locator(".quiz-q-text").first()).toContainText("1.");
  await expect(page.locator(".quiz-lang")).toHaveText("теория");
});

test("несуществующая глава: «Урок не найден»; несуществующая страница: «Страница не найдена»", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/book/12/chapter/999999");
  await expect(page.locator(".content")).toContainText("Урок не найден");
  await page.goto("/no-such-page");
  await expect(page.locator(".content")).toContainText("Страница не найдена");
});
