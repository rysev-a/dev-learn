import type { Locator, Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import { answerQuiz, chapterPath, progressOf, quizQuestions } from "../../support/learning";

/* "Вопросы" tab (theory quiz): only the server knows the answers, each question is answered once, progress lives in the account. */

// small chapters from different books: system design (lab) and Python (code), 5 questions each
const CASES = [
  { book: 18, num: 1 },
  { book: 13, num: 1 },
] as const;

const wrongOf = (answer: number, options: number) => (answer + 1) % options;
const question = (page: Page, i: number): Locator => page.locator(".quiz-q").nth(i);
const option = (page: Page, q: number, o: number): Locator => question(page, q).locator(".quiz-opt").nth(o);

for (const { book, num } of CASES) {
  test.describe(`quiz of book ${book}, chapter ${num}`, () => {
    const truth = quizQuestions(book, num);

    test("questions are shown without answers and explanations", async ({ page, request, guard }) => {
      await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await expect(page.locator(".quiz-q")).toHaveCount(truth.length);
      for (const [i, t] of truth.entries()) {
        await expect(question(page, i).locator(".quiz-q-text")).toHaveText(`${i + 1}. ${t.q}`);
        await expect(question(page, i).locator(".quiz-opt")).toHaveText(t.options);
      }
      // before a pick nothing is highlighted, there are no explanations, buttons are enabled
      await expect(page.locator(".quiz-opt.right, .quiz-opt.wrong")).toHaveCount(0);
      await expect(page.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(page.locator(".quiz-opt:disabled")).toHaveCount(0);
      await expect(page.locator(".quiz-lang")).toHaveText("теория");
      await expect(page.getByRole("button", { name: "Пройти ещё раз" })).toHaveCount(0);
      await expect(page.locator(".quiz-result")).toHaveCount(0);
      guard.assertClean();
    });

    test("the server does not reveal the correct option before a pick", async ({ page, request }) => {
      const { token } = await loginFresh(page, request);
      // both a direct request and what the page actually received
      const seen = page.waitForResponse((r) => new RegExp(`/api/quizzes/${book}/${num}$`).test(r.url()) && r.request().method() === "GET");
      await page.goto(await chapterPath(request, book, num, "questions"));
      const pageBody = await (await seen).text();
      const direct = await request.get(`/api/quizzes/${book}/${num}`, { headers: bearer(token) });
      expect(direct.ok()).toBeTruthy();
      for (const raw of [pageBody, await direct.text()]) {
        const body = JSON.parse(raw) as { questions: Record<string, unknown>[]; reveal: unknown[] };
        expect(body.questions).toHaveLength(truth.length);
        for (const q of body.questions) expect(Object.keys(q).sort(), "a question has only text and options").toEqual(["options", "q"]);
        expect(body.reveal, "nothing is revealed").toEqual(truth.map(() => null));
        expect(raw, "the response has neither explanations nor an answer field").not.toMatch(/"answer"|"expl"/);
        for (const t of truth) expect(raw).not.toContain(t.expl);
      }
    });

    test("correct pick: check mark, explanation, counter, the server remembered it", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, book, num, "questions"));
      const t = truth[0]!;
      await option(page, 0, t.answer).click();
      await expect(option(page, 0, t.answer)).toHaveClass(/\bright\b/);
      await expect(page.locator(".quiz-opt.wrong")).toHaveCount(0);
      await expect(question(page, 0).locator(".quiz-q-expl")).toHaveText(t.expl);
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 1/1");
      // other questions are unaffected
      await expect(page.locator(".quiz-q-expl")).toHaveCount(1);
      // an answered question is closed for another pick
      await expect(question(page, 0).locator(".quiz-opt:disabled")).toHaveCount(t.options.length);
      await expect(question(page, 1).locator(".quiz-opt:disabled")).toHaveCount(0);
      const progress = await progressOf(request, token);
      expect(progress.quizRight[`${book}:${num}`]).toBe(1);
      expect(progress.quiz[`${book}:${num}`]?.[0]).toBe(t.answer);
      guard.assertClean();
    });

    test("wrong pick: cross on it, the correct one highlighted, explanation", async ({ page, request, guard }) => {
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

    test("a question is answered once: a repeated pick changes nothing", async ({ page, request }) => {
      const { token } = await loginFresh(page, request);
      const t = truth[2]!;
      const wrong = wrongOf(t.answer, t.options.length);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await option(page, 2, wrong).click();
      await expect(option(page, 2, wrong)).toHaveClass(/\bwrong\b/);
      // click on the correct option of an already closed question: the button is disabled and a direct request returns the first pick
      await expect(option(page, 2, t.answer)).toBeDisabled();
      await option(page, 2, t.answer).click({ force: true });
      await expect(option(page, 2, wrong)).toHaveClass(/\bwrong\b/);
      await expect(page.locator(".quiz-lang")).toHaveText("теория · 0/1");
      const again = await answerQuiz(request, token, book, num, 2, t.answer);
      expect(again.pick, "the server keeps the first pick").toBe(wrong);
      expect((await progressOf(request, token)).quiz[`${book}:${num}`]?.[2]).toBe(wrong);
    });

    test("progress survives a reload: marks, explanations, counter", async ({ page, request, guard }) => {
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
      // after a reload the question is still closed, and reveal contains answers only for answered questions
      await expect(question(page, 0).locator(".quiz-opt:disabled")).toHaveCount(a.options.length);
      guard.assertClean();
    });

    test("summary after the last question: all correct shows \"Отлично\", mistakes show \"Результат\"", async ({ page, request, guard }) => {
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
      // again, this time everything is correct
      await page.getByRole("button", { name: "Пройти ещё раз" }).click();
      await expect(page.locator(".quiz-result")).toHaveCount(0);
      for (const [i, t] of truth.entries()) await option(page, i, t.answer).click();
      await expect(page.locator(".quiz-result")).toHaveClass(/\bok\b/);
      await expect(page.locator(".quiz-result")).toContainText(`✓ Отлично: ${total}/${total}`);
      guard.assertClean();
    });

    test("\"Пройти ещё раз\" also clears the answers on the server", async ({ page, request, guard }) => {
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
      // the server is cleared too: empty after a reload and answering again is possible
      await expect.poll(async () => (await progressOf(request, token)).quiz[`${book}:${num}`] ?? []).toEqual([]);
      await page.reload();
      await expect(page.locator(".quiz-q-expl")).toHaveCount(0);
      await expect(page.locator(".quiz-lang")).toHaveText("теория");
      await option(page, 0, wrongOf(truth[0]!.answer, truth[0]!.options.length)).click();
      await expect(option(page, 0, truth[0]!.answer)).toHaveClass(/\bright\b/);
      guard.assertClean();
    });

    test("tab and badge: the question count does not change with answers, another user sees a clean state", async ({ page, request, browser }) => {
      const { token } = await loginFresh(page, request);
      for (const [i, t] of truth.entries()) await answerQuiz(request, token, book, num, i, t.answer);
      await page.goto(await chapterPath(request, book, num, "questions"));
      await expect(page.locator(".ch-tab", { hasText: "Вопросы" }).locator(".ch-tab-badge")).toHaveText(String(truth.length));
      await expect(page.locator(".quiz-lang")).toHaveText(`теория · ${truth.length}/${truth.length}`);
      await expect(page.locator(".quiz-result")).toContainText(`✓ Отлично: ${truth.length}/${truth.length}`);
      // progress is personal: a new user sees the same chapter without marks
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

test.describe("quiz API: server-side checks", () => {
  const { book, num } = CASES[0];
  const truth = quizQuestions(book, num);

  test("without sign-in questions and answers are closed, invalid requests are rejected", async ({ page, request }) => {
    expect((await request.get(`/api/quizzes/${book}/${num}`)).status()).toBe(401);
    expect((await request.post(`/api/quizzes/${book}/${num}/answer`, { data: { question: 0, pick: 0 } })).status()).toBe(401);
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    const post = (question: number, pick: number) => request.post(`/api/quizzes/${book}/${num}/answer`, { headers: h, data: { question, pick } });
    expect((await post(truth.length, 0)).status(), "no question with this number").toBe(404);
    expect((await post(0, 50)).status(), "no option with this number").toBe(422);
    expect((await post(-1, 0)).status(), "question number out of range").toBe(422);
    expect((await request.get("/api/quizzes/18/999", { headers: h })).status(), "the chapter has no quiz").toBe(404);
    // rejected requests wrote nothing
    expect((await progressOf(request, token)).quiz[`${book}:${num}`] ?? []).toEqual([]);
  });

  test("an answer returns the correct option, the explanation and the number of correct ones", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const [a, b] = [truth[0]!, truth[1]!];
    const first = await answerQuiz(request, token, book, num, 0, a.answer);
    expect(first).toEqual({ pick: a.answer, answer: a.answer, expl: a.expl, right: 1 });
    const second = await answerQuiz(request, token, book, num, 1, wrongOf(b.answer, b.options.length));
    expect(second).toMatchObject({ pick: wrongOf(b.answer, b.options.length), answer: b.answer, expl: b.expl, right: 1 });
    // after answers, GET reveals the answer only for answered questions
    const got = (await (await request.get(`/api/quizzes/${book}/${num}`, { headers: bearer(token) })).json()) as { reveal: ({ answer: number; expl: string } | null)[] };
    expect(got.reveal[0]).toEqual({ answer: a.answer, expl: a.expl });
    expect(got.reveal[1]).toEqual({ answer: b.answer, expl: b.expl });
    expect(got.reveal.slice(2).every((r) => r === null)).toBe(true);
  });
});

test.describe("quiz in fullscreen mode", () => {
  const { book, num } = CASES[0];
  const truth = quizQuestions(book, num);

  test("the tree has \"Вопрос N\" items: number -> check or cross after an answer, a click leads to the question", async ({ page, request, guard }) => {
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
    // an answer in fullscreen updates the icon
    await option(page, 3, truth[3]!.answer).click();
    await expect(items.nth(3)).toHaveClass(/\bok\b/);
    guard.assertClean();
  });
});

test.describe("dashboard", () => {
  // AGENTS.md says the home page shows overall progress over slides, questions and exercises, with three bars per section. The Leptos dashboard shows only slides.
  test("the dashboard shows the number of correct quiz answers", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const truth = quizQuestions(18, 1);
    for (const [i, t] of truth.entries()) await answerQuiz(request, token, 18, 1, i, t.answer);
    await page.goto("/");
    const card = page.locator(".dash-card", { hasText: "Системный дизайн" });
    await expect(card.getByText("Вопросы")).toBeVisible();
    await expect(card.getByText(new RegExp(`^${truth.length}/`))).toBeVisible();
  });
});
