import type { Locator, Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import { answerQuiz, chapterPath, progressOf, quizQuestions } from "../../support/learning";

/* Вкладка «Вопросы» (квиз на теорию): ответы знает только сервер, на вопрос отвечают один раз, прогресс живёт в кабинете. */

// небольшие главы из разных книг: системный дизайн (лаборатория) и Python (код), по 5 вопросов
const CASES = [
  { book: 18, num: 1 },
  { book: 13, num: 1 },
] as const;

const wrongOf = (answer: number, options: number) => (answer + 1) % options;
const question = (page: Page, i: number): Locator => page.locator(".quiz-q").nth(i);
const option = (page: Page, q: number, o: number): Locator => question(page, q).locator(".quiz-opt").nth(o);

for (const { book, num } of CASES) {
  test.describe(`квиз книги ${book}, глава ${num}`, () => {
    const truth = quizQuestions(book, num);

    test("вопросы показаны без ответов и пояснений", async ({ page, request, guard }) => {
      await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await expect(page.locator(".quiz-q")).toHaveCount(truth.length);
      for (const [i, t] of truth.entries()) {
        await expect(question(page, i).locator(".quiz-q-text")).toHaveText(`${i + 1}. ${t.q}`);
        await expect(question(page, i).locator(".quiz-opt")).toHaveText(t.options);
      }
      // до выбора ничего не подсвечено, пояснений нет, кнопки доступны
      await expect(page.locator(".quiz-opt.right, .quiz-opt.wrong")).toHaveCount(0);
      await expect(page.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(page.locator(".quiz-opt:disabled")).toHaveCount(0);
      await expect(page.locator(".quiz-lang")).toHaveText("теория");
      await expect(page.getByRole("button", { name: "Пройти ещё раз" })).toHaveCount(0);
      await expect(page.locator(".quiz-result")).toHaveCount(0);
      guard.assertClean();
    });

    test("сервер не раскрывает верный вариант до выбора", async ({ page, request }) => {
      const { token } = await loginFresh(page, request);
      // и прямой запрос, и то, что реально получила страница
      const seen = page.waitForResponse((r) => new RegExp(`/api/quizzes/${book}/${num}$`).test(r.url()) && r.request().method() === "GET");
      await page.goto(await chapterPath(request, book, num, "questions"));
      const pageBody = await (await seen).text();
      const direct = await request.get(`/api/quizzes/${book}/${num}`, { headers: bearer(token) });
      expect(direct.ok()).toBeTruthy();
      for (const raw of [pageBody, await direct.text()]) {
        const body = JSON.parse(raw) as { questions: Record<string, unknown>[]; reveal: unknown[] };
        expect(body.questions).toHaveLength(truth.length);
        for (const q of body.questions) expect(Object.keys(q).sort(), "у вопроса только текст и варианты").toEqual(["options", "q"]);
        expect(body.reveal, "ничего не раскрыто").toEqual(truth.map(() => null));
        expect(raw, "в ответе нет ни пояснений, ни поля answer").not.toMatch(/"answer"|"expl"/);
        for (const t of truth) expect(raw).not.toContain(t.expl);
      }
    });

    test("верный выбор: ✓, пояснение, счётчик, сервер запомнил", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      const t = truth[0]!;
      await option(page, 0, t.answer).click();
      await expect(option(page, 0, t.answer)).toHaveClass(/\bright\b/);
      await expect(page.locator(".quiz-opt.wrong")).toHaveCount(0);
      await expect(question(page, 0).locator(".quiz-q-expl")).toHaveText(t.expl);
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 1/1");
      // остальные вопросы не затронуты
      await expect(page.locator(".quiz-q-expl")).toHaveCount(1);
      // ответивший вопрос закрыт для повторного выбора
      await expect(question(page, 0).locator(".quiz-opt:disabled")).toHaveCount(t.options.length);
      await expect(question(page, 1).locator(".quiz-opt:disabled")).toHaveCount(0);
      const progress = await progressOf(request, token);
      expect(progress.quizRight[`${book}:${num}`]).toBe(1);
      expect(progress.quiz[`${book}:${num}`]?.[0]).toBe(t.answer);
      guard.assertClean();
    });

    test("неверный выбор: ✗ на нём, верный подсвечен, пояснение", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      const t = truth[1]!;
      const wrong = wrongOf(t.answer, t.options.length);
      await option(page, 1, wrong).click();
      await expect(option(page, 1, wrong)).toHaveClass(/\bwrong\b/);
      await expect(option(page, 1, t.answer)).toHaveClass(/\bright\b/);
      await expect(question(page, 1).locator(".quiz-opt.right, .quiz-opt.wrong")).toHaveCount(2);
      await expect(question(page, 1).locator(".quiz-q-expl")).toHaveText(t.expl);
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 0/1");
      const progress = await progressOf(request, token);
      expect(progress.quizRight[`${book}:${num}`] ?? 0).toBe(0);
      expect(progress.quiz[`${book}:${num}`]?.[1]).toBe(wrong);
      guard.assertClean();
    });

    test("на вопрос отвечают один раз: повторный выбор ничего не меняет", async ({ page, request }) => {
      const { token } = await loginFresh(page, request);
      const t = truth[2]!;
      const wrong = wrongOf(t.answer, t.options.length);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await option(page, 2, wrong).click();
      await expect(option(page, 2, wrong)).toHaveClass(/\bwrong\b/);
      // клик по верному варианту уже закрытого вопроса: кнопка заблокирована, а прямой запрос возвращает первый выбор
      await expect(option(page, 2, t.answer)).toBeDisabled();
      await option(page, 2, t.answer).click({ force: true });
      await expect(option(page, 2, wrong)).toHaveClass(/\bwrong\b/);
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 0/1");
      const again = await answerQuiz(request, token, book, num, 2, t.answer);
      expect(again.pick, "сервер оставляет первый выбор").toBe(wrong);
      expect((await progressOf(request, token)).quiz[`${book}:${num}`]?.[2]).toBe(wrong);
    });

    test("прогресс переживает перезагрузку: отметки, пояснения, счётчик", async ({ page, request, guard }) => {
      await loginFresh(page, request);
      const url = await chapterPath(request, book, num, "questions");
      await page.goto(url);
      const [a, b] = [truth[0]!, truth[1]!];
      await option(page, 0, a.answer).click();
      await option(page, 1, wrongOf(b.answer, b.options.length)).click();
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 1/2");
      await page.reload();
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 1/2");
      await expect(option(page, 0, a.answer)).toHaveClass(/\bright\b/);
      await expect(option(page, 1, b.answer)).toHaveClass(/\bright\b/);
      await expect(option(page, 1, wrongOf(b.answer, b.options.length))).toHaveClass(/\bwrong\b/);
      await expect(question(page, 0).locator(".quiz-q-expl")).toHaveText(a.expl);
      await expect(question(page, 1).locator(".quiz-q-expl")).toHaveText(b.expl);
      await expect(question(page, 2).locator(".quiz-opt:disabled")).toHaveCount(0);
      // после перезагрузки вопрос тоже закрыт, а ответы пришли в reveal только для отвеченных
      await expect(question(page, 0).locator(".quiz-opt:disabled")).toHaveCount(a.options.length);
      guard.assertClean();
    });

    test("итог после последнего вопроса: все верные — «Отлично», есть ошибки — «Результат»", async ({ page, request, guard }) => {
      await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      for (const [i, t] of truth.entries()) {
        await expect(page.locator(".quiz-result")).toHaveCount(0);
        await option(page, i, i === 0 ? wrongOf(t.answer, t.options.length) : t.answer).click();
        await expect(question(page, i).locator(".quiz-q-expl")).toBeVisible();
      }
      const total = truth.length;
      await expect(page.locator(".quiz-result")).toHaveClass(/\bfail\b/);
      await expect(page.locator(".quiz-result")).toContainText(`Результат: ${total - 1}/${total}`);
      await expect(page.locator(".quiz-lang")).toHaveText(`теория · ${total - 1}/${total}`);
      // заново, на этот раз всё верно
      await page.getByRole("button", { name: "Пройти ещё раз" }).click();
      await expect(page.locator(".quiz-result")).toHaveCount(0);
      for (const [i, t] of truth.entries()) await option(page, i, t.answer).click();
      await expect(page.locator(".quiz-result")).toHaveClass(/\bok\b/);
      await expect(page.locator(".quiz-result")).toContainText(`✓ Отлично: ${total}/${total}`);
      guard.assertClean();
    });

    test("«Пройти ещё раз» очищает ответы и на сервере", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await expect(page.getByRole("button", { name: "Пройти ещё раз" })).toHaveCount(0);
      await option(page, 0, truth[0]!.answer).click();
      await option(page, 1, wrongOf(truth[1]!.answer, truth[1]!.options.length)).click();
      await expect(page.locator(".quiz-q-expl")).toHaveCount(2);
      await page.getByRole("button", { name: "Пройти ещё раз" }).click();
      await expect(page.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(page.locator(".quiz-opt.right, .quiz-opt.wrong")).toHaveCount(0);
      await expect(page.locator(".quiz-opt:disabled")).toHaveCount(0);
      await expect(page.locator(".quiz-lang")).toHaveText("теория");
      await expect(page.getByRole("button", { name: "Пройти ещё раз" })).toHaveCount(0);
      // сервер тоже очищен: и после перезагрузки пусто, и можно ответить снова
      await expect.poll(async () => (await progressOf(request, token)).quiz[`${book}:${num}`] ?? []).toEqual([]);
      await page.reload();
      await expect(page.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(page.locator(".quiz-lang")).toHaveText("теория");
      await option(page, 0, wrongOf(truth[0]!.answer, truth[0]!.options.length)).click();
      await expect(option(page, 0, truth[0]!.answer)).toHaveClass(/\bright\b/);
      guard.assertClean();
    });

    test("вкладка и значок: число вопросов не меняется от ответов, у другого пользователя чисто", async ({ page, request, browser }) => {
      const { token } = await loginFresh(page, request);
      for (const [i, t] of truth.entries()) await answerQuiz(request, token, book, num, i, t.answer);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await expect(page.locator(".ch-tab", { hasText: "Вопросы" }).locator(".ch-tab-badge")).toHaveText(String(truth.length));
      await expect(page.locator(".quiz-lang")).toHaveText(`теория · ${truth.length}/${truth.length}`);
      await expect(page.locator(".quiz-result")).toContainText(`✓ Отлично: ${truth.length}/${truth.length}`);
      // прогресс личный: у нового пользователя та же глава без отметок
      const other = await browser.newContext();
      const otherPage = await other.newPage();
      await loginFresh(otherPage, other.request);
      await otherPage.goto(await chapterPath(request, book, num, "questions"));
      await expect(otherPage.locator(".quiz-q")).toHaveCount(truth.length);
      await expect(otherPage.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(otherPage.locator(".quiz-lang")).toHaveText("теория");
      await other.close();
    });
  });
}

test.describe("API квиза: проверки на сервере", () => {
  const { book, num } = CASES[0];
  const truth = quizQuestions(book, num);

  test("без входа вопросы и ответы закрыты, неверные запросы отклоняются", async ({ page, request }) => {
    expect((await request.get(`/api/quizzes/${book}/${num}`)).status()).toBe(401);
    expect((await request.post(`/api/quizzes/${book}/${num}/answer`, { data: { question: 0, pick: 0 } })).status()).toBe(401);
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    const post = (question: number, pick: number) => request.post(`/api/quizzes/${book}/${num}/answer`, { headers: h, data: { question, pick } });
    expect((await post(truth.length, 0)).status(), "вопроса с таким номером нет").toBe(404);
    expect((await post(0, 50)).status(), "варианта с таким номером нет").toBe(422);
    expect((await post(-1, 0)).status(), "номер вопроса вне диапазона").toBe(422);
    expect((await request.get("/api/quizzes/18/999", { headers: h })).status(), "у главы нет квиза").toBe(404);
    // отклонённые запросы ничего не записали
    expect((await progressOf(request, token)).quiz[`${book}:${num}`] ?? []).toEqual([]);
  });

  test("ответ даёт верный вариант, пояснение и число верных", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const [a, b] = [truth[0]!, truth[1]!];
    const first = await answerQuiz(request, token, book, num, 0, a.answer);
    expect(first).toEqual({ pick: a.answer, answer: a.answer, expl: a.expl, right: 1 });
    const second = await answerQuiz(request, token, book, num, 1, wrongOf(b.answer, b.options.length));
    expect(second).toMatchObject({ pick: wrongOf(b.answer, b.options.length), answer: b.answer, expl: b.expl, right: 1 });
    // после ответов GET раскрывает ответ только на отвеченные вопросы
    const got = (await (await request.get(`/api/quizzes/${book}/${num}`, { headers: bearer(token) })).json()) as { reveal: ({ answer: number; expl: string } | null)[] };
    expect(got.reveal[0]).toEqual({ answer: a.answer, expl: a.expl });
    expect(got.reveal[1]).toEqual({ answer: b.answer, expl: b.expl });
    expect(got.reveal.slice(2).every((r) => r === null)).toBe(true);
  });
});

test.describe("квиз в полноэкранном режиме", () => {
  const { book, num } = CASES[0];
  const truth = quizQuestions(book, num);

  test("в дереве пункты «Вопрос N»: номер → ✓ или ✗ после ответа, клик ведёт к вопросу", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    await answerQuiz(request, token, book, num, 0, truth[0]!.answer);
    await answerQuiz(request, token, book, num, 1, wrongOf(truth[1]!.answer, truth[1]!.options.length));
    await page.goto(`${await chapterPath(request, book, num, "questions")}?fs=1`);
    const items = page.locator(".slide-fs-toc .fst-slide");
    await expect(items).toHaveCount(truth.length);
    await expect(items.nth(0)).toHaveClass(/\bok\b/);
    await expect(items.nth(0).locator(".fst-slide-num")).toHaveText("✓");
    await expect(items.nth(1)).toHaveClass(/\bbad\b/);
    await expect(items.nth(1).locator(".fst-slide-num")).toHaveText("✗");
    await expect(items.nth(2).locator(".fst-slide-num")).toHaveText("03");
    await expect(items.nth(2).locator(".fst-slide-name")).toHaveText("Вопрос 3");
    // ответ в полном экране обновляет значок
    await option(page, 3, truth[3]!.answer).click();
    await expect(items.nth(3)).toHaveClass(/\bok\b/);
    guard.assertClean();
  });
});

test.describe("дашборд", () => {
  // В AGENTS.md главная — «общий прогресс по слайдам, вопросам и упражнениям, у каждого раздела три полосы». Leptos-дашборд показывает только слайды.
  test("дашборд показывает число верных ответов на вопросы", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const truth = quizQuestions(18, 1);
    for (const [i, t] of truth.entries()) await answerQuiz(request, token, 18, 1, i, t.answer);
    await page.goto("/");
    const card = page.locator(".dash-card", { hasText: "Системный дизайн" });
    await expect(card.getByText("Вопросы")).toBeVisible();
    await expect(card.getByText(new RegExp(`^${truth.length}/`))).toBeVisible();
  });
});
