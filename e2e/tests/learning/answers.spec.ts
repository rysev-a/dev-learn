import type { Locator, Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import { answerTasks, answerTitle, chapterPath, firstAnswer, learningGuard, progressOf } from "../../support/learning";

/* Exercises with typed answers (discrete math, book 12): statements and hints come without answers, the server checks. */

const BOOK = 12;
const CHAPTERS = [1, 2, 3];
const NOTE = "Пока неверно — попробуй ещё раз или загляни в подсказку.";
const WRONG = "gibberish-e2e";

const row = (page: Page, i: number): Locator => page.locator(".quiz-q").nth(i);
const input = (page: Page, i: number): Locator => row(page, i).locator("input.ex-input");
const checkBtn = (page: Page, i: number): Locator => row(page, i).locator(".ex-row button.quiz-btn");
const counter = (page: Page): Locator => page.locator(".quiz-lang");

/** Input + "Проверить". */
async function submit(page: Page, i: number, value: string) {
  await input(page, i).fill(value);
  await checkBtn(page, i).click();
}

/** Setup: solve a task directly through the API. */
async function solveViaApi(request: Parameters<typeof chapterPath>[0], token: string, num: number, task: number, value: string) {
  const res = await request.post(`/api/answers/${BOOK}/${num}/check`, { headers: bearer(token), data: { task, value } });
  expect(res.ok()).toBeTruthy();
  expect(await res.json()).toEqual({ ok: true });
}

for (const num of CHAPTERS) {
  test.describe(`discrete math, chapter ${num}`, () => {
    const tasks = answerTasks(BOOK, num);
    const title = answerTitle(BOOK, num);

    test("statements, inputs and hints without answers", async ({ page, request }) => {
      const guard = learningGuard(page);
      await loginFresh(page, request);
      await page.goto(await chapterPath(request, BOOK, num, "exercises"));
      await expect(page.locator(".quiz-head h3")).toHaveText(title);
      await expect(counter(page)).toHaveText("упражнения");
      await expect(page.locator(".quiz-q")).toHaveCount(tasks.length);
      for (const [i, t] of tasks.entries()) {
        await expect(row(page, i).locator(".quiz-q-text")).toHaveText(`${i + 1}. ${t.q}`);
        await expect(input(page, i)).toHaveAttribute("placeholder", "Ответ");
        await expect(input(page, i)).toBeEnabled();
        await expect(input(page, i)).toHaveValue("");
        await expect(checkBtn(page, i)).toHaveText("Проверить");
        await expect(row(page, i).locator(".ex-hint")).toHaveCount(0); // hint is hidden
      }
      await expect(page.getByRole("button", { name: "Начать заново" })).toHaveCount(0);
      await expect(page.locator(".quiz-result")).toHaveCount(0);
      guard.assertClean();
    });

    test("wrong input gives a message, an edit clears it, a correct one shows \"решено\"", async ({ page, request }) => {
      const guard = learningGuard(page);
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, BOOK, num, "exercises"));
      const t = tasks[0]!;
      await submit(page, 0, WRONG);
      await expect(row(page, 0).locator(".ex-note")).toHaveText(NOTE);
      await expect(input(page, 0)).toHaveClass(/\bwrong\b/);
      await expect(input(page, 0)).toBeEnabled();
      await expect(counter(page)).toHaveText("упражнения");
      expect((await progressOf(request, token)).answers[`${BOOK}:${num}`] ?? {}).toEqual({});
      // a new edit clears the "wrong" state
      await input(page, 0).press("End");
      await input(page, 0).pressSequentially("1");
      await expect(row(page, 0).locator(".ex-note")).toHaveCount(0);
      await expect(input(page, 0)).not.toHaveClass(/\bwrong\b/);
      // correct answer
      await submit(page, 0, firstAnswer(t));
      await expect(input(page, 0)).toHaveClass(/\bright\b/);
      await expect(input(page, 0)).toBeDisabled();
      await expect(checkBtn(page, 0)).toHaveText("✓");
      await expect(checkBtn(page, 0)).toBeDisabled();
      await expect(row(page, 0).locator(".ex-note")).toHaveCount(0);
      await expect(counter(page)).toHaveText(`упражнения · решено 1/${tasks.length}`);
      await expect(page.getByRole("button", { name: "Начать заново" })).toBeVisible();
      // other tasks are unaffected
      await expect(input(page, 1)).toBeEnabled();
      expect((await progressOf(request, token)).answers[`${BOOK}:${num}`]).toEqual({ "0": firstAnswer(t) });
      guard.assertClean();
    });

    test("solved state survives a reload, \"Начать заново\" also clears it on the server", async ({ page, request }) => {
      const guard = learningGuard(page);
      const { token } = await loginFresh(page, request);
      const url = await chapterPath(request, BOOK, num, "exercises");
      await page.goto(url);
      await submit(page, 0, firstAnswer(tasks[0]!));
      await submit(page, 1, firstAnswer(tasks[1]!));
      await submit(page, 2, WRONG); // a wrong attempt is not saved
      await expect(counter(page)).toHaveText(`упражнения · решено 2/${tasks.length}`);
      await page.reload();
      await expect(counter(page)).toHaveText(`упражнения · решено 2/${tasks.length}`);
      for (const i of [0, 1]) {
        await expect(input(page, i)).toHaveValue(firstAnswer(tasks[i]!));
        await expect(input(page, i)).toBeDisabled();
        await expect(input(page, i)).toHaveClass(/\bright\b/);
        await expect(checkBtn(page, i)).toHaveText("✓");
      }
      await expect(input(page, 2)).toHaveValue("");
      await expect(input(page, 2)).toBeEnabled();

      await page.getByRole("button", { name: "Начать заново" }).click();
      await expect(counter(page)).toHaveText("упражнения");
      for (const i of [0, 1]) {
        await expect(input(page, i)).toHaveValue("");
        await expect(input(page, i)).toBeEnabled();
        await expect(input(page, i)).not.toHaveClass(/\bright\b/);
        await expect(checkBtn(page, i)).toHaveText("Проверить");
      }
      await expect(page.getByRole("button", { name: "Начать заново" })).toHaveCount(0);
      await expect.poll(async () => (await progressOf(request, token)).answers[`${BOOK}:${num}`] ?? {}).toEqual({});
      await page.reload();
      await expect(counter(page)).toHaveText("упражнения");
      await expect(input(page, 0)).toBeEnabled();
      // after a reset it can be solved again
      await submit(page, 0, firstAnswer(tasks[0]!));
      await expect(counter(page)).toHaveText(`упражнения · решено 1/${tasks.length}`);
      guard.assertClean();
    });

    test("all tasks solved: summary line", async ({ page, request }) => {
      const guard = learningGuard(page);
      const { token } = await loginFresh(page, request);
      await page.goto(await chapterPath(request, BOOK, num, "exercises"));
      for (const [i, t] of tasks.entries()) {
        await expect(page.locator(".quiz-result")).toHaveCount(0);
        await submit(page, i, firstAnswer(t));
        await expect(input(page, i)).toBeDisabled();
      }
      await expect(counter(page)).toHaveText(`упражнения · решено ${tasks.length}/${tasks.length}`);
      await expect(page.locator(".quiz-result")).toHaveClass(/\bok\b/);
      await expect(page.locator(".quiz-result")).toContainText(`✓ Все задачи решены: ${tasks.length}/${tasks.length}`);
      expect(Object.keys((await progressOf(request, token)).answers[`${BOOK}:${num}`] ?? {})).toHaveLength(tasks.length);
      guard.assertClean();
    });
  });
}

test.describe("answer input", () => {
  const num = 1;
  const tasks = answerTasks(BOOK, num);

  test("Enter in the field checks the answer; empty input sends nothing", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.goto(await chapterPath(request, BOOK, num, "exercises"));
    let checks = 0;
    page.on("request", (r) => {
      if (r.url().includes("/check")) checks++;
    });
    await input(page, 0).press("Enter");
    await checkBtn(page, 0).click();
    await input(page, 0).fill("   ");
    await input(page, 0).press("Enter");
    await expect(row(page, 0).locator(".ex-note")).toHaveCount(0);
    expect(checks, "empty input is not sent to the server").toBe(0);
    await input(page, 0).fill(firstAnswer(tasks[0]!));
    await input(page, 0).press("Enter");
    await expect(input(page, 0)).toHaveClass(/\bright\b/);
    expect(checks).toBe(1);
  });

  test("comparison ignores case and spaces, accepts a comma in numbers; alternative accepted answers", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.goto(await chapterPath(request, BOOK, num, "exercises"));
    // task 3 ("1022"): surrounding spaces, decimal notation
    await submit(page, 6, "  1022  ");
    await expect(input(page, 6)).toHaveClass(/\bright\b/);
    await submit(page, 5, "32,0");
    await expect(input(page, 5)).toHaveClass(/\bright\b/);
    // task 5: "да" is accepted in another case, as is the alternative "истинно"
    await submit(page, 4, "  ДА ");
    await expect(input(page, 4)).toHaveClass(/\bright\b/);
    await submit(page, 3, "6 pieces"); // extra text is not a number
    await expect(row(page, 3).locator(".ex-note")).toHaveText(NOTE);
    await submit(page, 2, "9.5"); // a close number is wrong
    await expect(row(page, 2).locator(".ex-note")).toHaveText(NOTE);
    // what the student typed is kept (edges trimmed)
    await expect(input(page, 4)).toHaveValue("  ДА ");
    const alt = answerTasks(BOOK, 2).find((t) => t.answers.length > 1)!;
    await page.goto(await chapterPath(request, BOOK, 2, "exercises"));
    const k = answerTasks(BOOK, 2).indexOf(alt);
    await submit(page, k, alt.answers[1]!);
    await expect(input(page, k)).toHaveClass(/\bright\b/);
  });

  test("hint: show and hide, it contains no answer", async ({ page, request }) => {
    const guard = learningGuard(page);
    await loginFresh(page, request);
    await page.goto(await chapterPath(request, BOOK, num, "exercises"));
    const t = tasks[2]!;
    const toggle = row(page, 2).locator(".ex-hint-row button");
    await expect(toggle).toHaveText("Подсказка");
    await toggle.click();
    await expect(toggle).toHaveText("Скрыть подсказку");
    await expect(row(page, 2).locator(".ex-hint")).toHaveText(t.hint);
    await expect(row(page, 1).locator(".ex-hint")).toHaveCount(0); // not opened for other tasks
    await toggle.click();
    await expect(toggle).toHaveText("Подсказка");
    await expect(row(page, 2).locator(".ex-hint")).toHaveCount(0);
    guard.assertClean();
  });

  test("the \"Практика\" tab of a chapter without code tasks opens the exercises, no count badge", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.goto(await chapterPath(request, BOOK, num, ""));
    await expect(page.locator(".ch-tab")).toHaveCount(3); // tabs appear as chapter data loads: wait for all of them so they do not shift under the cursor
    const tab = page.locator(".ch-tab", { hasText: "Практика" });
    await expect(tab).toBeVisible();
    await expect(tab.locator(".ch-tab-badge")).toHaveCount(0);
    await tab.click();
    await expect(page).toHaveURL(/\/exercises$/);
    await expect(page.locator(".quiz-q")).toHaveCount(tasks.length);
    await expect(page.locator(".pr")).toHaveCount(0); // there is no code-practice shell here
  });
});

test.describe("answers API: server-side check", () => {
  const num = 1;
  const tasks = answerTasks(BOOK, num);

  test("statements come without answers, a wrong answer does not reveal the right one", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    const set = await request.get(`/api/answers/${BOOK}/${num}`, { headers: h });
    expect(set.ok()).toBeTruthy();
    const raw = await set.text();
    const body = JSON.parse(raw) as { kind: string; title: string; tasks: Record<string, unknown>[]; solved: object };
    expect(body.kind).toBe("practice");
    expect(body.tasks).toHaveLength(tasks.length);
    for (const t of body.tasks) expect(Object.keys(t).sort()).toEqual(["hint", "q"]);
    expect(body.solved).toEqual({});
    expect(raw).not.toContain('"answers"');
    // the correct answer does not appear anywhere in the response to a wrong check
    const bad = await request.post(`/api/answers/${BOOK}/${num}/check`, { headers: h, data: { task: 0, value: WRONG } });
    expect(bad.ok()).toBeTruthy();
    expect(await bad.json()).toEqual({ ok: false });
    // correct: exactly {ok: true}, and afterwards GET returns the accepted value of this very user
    const good = await request.post(`/api/answers/${BOOK}/${num}/check`, { headers: h, data: { task: 0, value: " " + firstAnswer(tasks[0]!) + " " } });
    expect(await good.json()).toEqual({ ok: true });
    const after = (await (await request.get(`/api/answers/${BOOK}/${num}`, { headers: h })).json()) as { solved: Record<string, string> };
    expect(after.solved).toEqual({ "0": firstAnswer(tasks[0]!) });
    // chapter counters are open, they contain no answers
    const counts = (await (await request.get("/api/answers")).json()) as Record<string, Record<string, number>>;
    expect(counts[String(BOOK)]?.[String(num)]).toBe(tasks.length);
  });

  test("without sign-in and with invalid data the check is rejected", async ({ page, request }) => {
    expect((await request.get(`/api/answers/${BOOK}/${num}`)).status()).toBe(401);
    expect((await request.post(`/api/answers/${BOOK}/${num}/check`, { data: { task: 0, value: "1" } })).status()).toBe(401);
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    const check = (task: number, value: string) => request.post(`/api/answers/${BOOK}/${num}/check`, { headers: h, data: { task, value } });
    expect((await check(tasks.length, "1")).status(), "no task with this number").toBe(404);
    expect((await check(0, "1".repeat(201))).status(), "input too long").toBe(422);
    expect((await request.get(`/api/answers/${BOOK}/999`, { headers: h })).status(), "the chapter has no exercises").toBe(404);
    expect((await request.delete(`/api/answers?book=${BOOK}&chapter=-1`, { headers: h })).status(), "chapter out of range").toBe(422);
    expect((await progressOf(request, token)).answers[`${BOOK}:${num}`] ?? {}).toEqual({});
  });

  test("chapters do not share solved state; a reset affects only its own chapter", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    await solveViaApi(request, token, 1, 0, firstAnswer(tasks[0]!));
    await solveViaApi(request, token, 2, 0, firstAnswer(answerTasks(BOOK, 2)[0]!));
    const p = await progressOf(request, token);
    expect(Object.keys(p.answers)).toEqual(expect.arrayContaining([`${BOOK}:1`, `${BOOK}:2`]));
    expect((await request.delete(`/api/answers?book=${BOOK}&chapter=1`, { headers: h })).status()).toBe(204);
    const q = await progressOf(request, token);
    expect(q.answers[`${BOOK}:1`] ?? {}).toEqual({});
    expect(q.answers[`${BOOK}:2`]).toEqual({ "0": firstAnswer(answerTasks(BOOK, 2)[0]!) });
  });
});
