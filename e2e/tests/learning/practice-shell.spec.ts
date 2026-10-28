import type { APIRequestContext, Locator, Page } from "@playwright/test";
import { bearer, chapters, expect, loginFresh, test } from "../../support/fixtures";
import { FakeWorker, chapterPath, codeTasks, failing, passing, presetSetting, unique, type CodeTask, type WorkerResult } from "../../support/learning";

/* Shared practice shell: "Решено N из M" progress, exercise order, "Дальше →" transitions and auto-advance, items in fullscreen,
   exercise reset from settings. A fake worker performs the check; solutions are seeded directly through the API. */

const PY = { book: 13, num: 0 };
const SQL = { book: 9, num: 1 };
const pyTasks = codeTasks(PY.book, PY.num);
const sqlTasks = codeTasks(SQL.book, SQL.num);

const items = (page: Page): Locator => page.locator(".pr-item");
const editor = (page: Page): Locator => page.locator("textarea.rs-input");
const mainBtn = (page: Page): Locator => page.locator(".ex-row button.quiz-btn").first();
const label = (page: Page): Locator => page.locator(".pr-top-label").first();

async function open(page: Page, request: APIRequestContext, query = "", target = PY): Promise<void> {
  await page.goto(`${await chapterPath(request, target.book, target.num, "exercises")}${query}`);
  await expect(page.locator(".pr-main")).toBeVisible();
}

/** Submits a solution through the API and answers for the worker: this sets an exercise status without using the interface. */
async function seed(request: APIRequestContext, token: string, worker: FakeWorker, t: CodeTask, answer: WorkerResult, target = PY): Promise<void> {
  await worker.ping();
  const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: target.book, chapter: target.num, task: t.id, code: `print(1)\n${unique()}\n` } });
  expect(res.status(), await res.text()).toBe(202);
  const job = await worker.claim();
  expect(job?.task.id).toBe(t.id);
  await worker.complete(job!, answer);
}

/** The worker's answer to what the interface sent. */
async function serve(worker: FakeWorker, answer: WorkerResult): Promise<void> {
  const job = await worker.claim();
  expect(job, "the job reached the worker").not.toBeNull();
  await worker.complete(job!, answer);
}

test.describe("progress and order", () => {
  test("\"Решено N из M\", the bar, the tab badge and the marks follow the server statuses", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await seed(request, token, worker, pyTasks[0]!, passing("1991\n"));
    await seed(request, token, worker, pyTasks[1]!, passing("int\n"));
    await seed(request, token, worker, pyTasks[2]!, failing("even", "odd"));
    await seed(request, token, worker, pyTasks[3]!, passing("1\n"));
    await open(page, request);
    const total = pyTasks.length;
    await expect(label(page)).toHaveText(`Решено 3 из ${total}`);
    await expect(page.locator(".pr-bar")).toHaveAttribute("aria-valuemax", String(total));
    await expect(page.locator(".pr-bar i")).toHaveAttribute("style", new RegExp(`width: ${Math.floor((3 * 100) / total)}%`));
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`3/${total}`);
    const marks = await items(page).locator(".pr-mark").allTextContents();
    expect(marks).toEqual(["✓", "✓", "✗", "✓", "5", "6"]);
    await expect(page.locator(".pr-item.ok")).toHaveCount(3);
    await expect(page.locator(".pr-item.bad")).toHaveCount(1);
    // an opened failed exercise shows "не пройдено", an unsolved one shows "не решено"
    await items(page).nth(2).click();
    await expect(page.locator(".pr-badge")).toHaveText("не пройдено");
    await items(page).nth(4).click();
    await expect(page.locator(".pr-badge")).toHaveText("не решено");
    guard.assertClean();
  });

  test("exercises go in chapter order (SQL: 41 exercises), titles and numbers match the data", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, "", SQL);
    await expect(items(page)).toHaveCount(sqlTasks.length);
    expect(await items(page).locator(".pr-name").allTextContents()).toEqual(sqlTasks.map((t) => t.title));
    expect(await items(page).locator(".pr-mark").allTextContents()).toEqual(sqlTasks.map((_, i) => String(i + 1)));
    await expect(label(page)).toHaveText(`Решено 0 из ${sqlTasks.length}`);
    // selecting the last exercise
    await items(page).last().click();
    await expect(page.locator(".pr-head h3")).toHaveText(`${sqlTasks.length}. ${sqlTasks[sqlTasks.length - 1]!.title}`);
  });
});

test.describe("shell labels", () => {
  // The right-hand label of the progress bar is hard-coded as "python · docker", for SQL chapters (sql mode, SQLite sandbox) and for Rust/C/JS alike.
  test("the label to the right of the bar does not say Python for SQL exercises", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, "", SQL);
    await expect(page.locator(".pr-top-label").last()).not.toContainText("python");
  });
});

test.describe("\"Дальше →\" and auto-advance", () => {
  test("auto-advance is off by default: after solving we stay on the exercise", async ({ page, request }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await editor(page).fill(`year = 1991\nprint(year)\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    const url = page.url();
    await page.waitForTimeout(2000); // auto-advance, if it were on, would fire after a second
    expect(page.url()).toBe(url);
    await expect(mainBtn(page)).toHaveText("Дальше →");
  });

  test("auto-advance is on: the next exercise opens after a second", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await presetSetting(page, "cs-core-auto-next", "1");
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await editor(page).fill(`year = 1991\nprint(year)\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[1]!.id}$`), { timeout: 5000 });
    await expect(page.locator(".pr-head h3")).toHaveText(`2. ${pyTasks[1]!.title}`);
    await expect(editor(page)).toBeFocused();
    await expect(items(page).first()).toHaveClass(/\bok\b/);
    guard.assertClean();
  });

  test("auto-advance does not move on if the student already picked another exercise", async ({ page, request }) => {
    await loginFresh(page, request);
    await presetSetting(page, "cs-core-auto-next", "1");
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await editor(page).fill(`year = 1991\nprint(year)\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    await items(page).nth(4).click(); // without waiting for the second
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[4]!.id}$`));
    await page.waitForTimeout(2000);
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[4]!.id}$`));
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[4]!.title);
  });

  test("the \"Автопереход\" setting toggles and is written to localStorage", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.goto("/settings");
    const toggle = page.getByRole("switch", { name: "Автопереход к следующему упражнению" });
    await expect(toggle).toHaveAttribute("aria-checked", "false");
    const stored = () => page.evaluate(() => window.localStorage.getItem("cs-core-auto-next"));
    expect(await stored()).toBeNull();
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-checked", "true");
    expect(await stored()).toBe("1");
    await page.reload();
    await expect(toggle).toHaveAttribute("aria-checked", "true");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-checked", "false");
    expect(await stored()).toBeNull();
  });

  // The settings promise: "after the last one, the first exercise of the next chapter" (same in AGENTS.md). In the Leptos frontend
  // `go_next` does nothing on the last exercise, and the "Дальше →" button does not appear there at all (`go_mode` requires idx + 1 < total).
  test("after solving the last exercise, \"Дальше →\" leads to the first exercise of the next chapter with tasks", async ({ page, request }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const last = pyTasks[pyTasks.length - 1]!;
    await open(page, request, `?task=${last.id}`);
    await editor(page).fill(`class A:\n    pass\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("ok\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await mainBtn(page).click();
    const next = (await chapters(request, PY.book)).find((c) => c.num === PY.num + 1)!;
    await expect(page).toHaveURL(new RegExp(`/book/${PY.book}/chapter/${next.id}/exercises`));
  });
});

test.describe("fullscreen", () => {
  test("the left tree lists exercises with statuses; a pick keeps ?fs=1; checking works and updates the icon", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await seed(request, token, worker, pyTasks[0]!, passing("1991\n"));
    await seed(request, token, worker, pyTasks[1]!, failing("int\n", "str\n"));
    await open(page, request, "?fs=1");
    await expect(page.locator(".slide-fs")).toBeVisible();
    const tree = page.locator(".slide-fs-toc .fst-slide");
    await expect(tree).toHaveCount(pyTasks.length);
    expect(await tree.locator(".fst-slide-name").allTextContents()).toEqual(pyTasks.map((t) => t.title));
    await expect(tree.nth(0)).toHaveClass(/\bok\b/);
    await expect(tree.nth(0).locator(".fst-slide-num")).toHaveText("✓");
    await expect(tree.nth(1)).toHaveClass(/\bbad\b/);
    await expect(tree.nth(1).locator(".fst-slide-num")).toHaveText("✗");
    await expect(tree.nth(2).locator(".fst-slide-num")).toHaveText("03");
    await expect(tree.nth(0)).toHaveClass(/\bon\b/); // the current exercise is marked
    // a pick in the tree: the address keeps fs=1 and adds task
    await tree.nth(2).click();
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[2]!.id}`));
    await expect(page).toHaveURL(/fs=1/);
    await expect(page.locator(".slide-fs")).toBeVisible();
    await expect(page.locator(".pr-head h3")).toHaveText(`3. ${pyTasks[2]!.title}`);
    await expect(tree.nth(2)).toHaveClass(/\bon\b/);
    await expect(tree.nth(0)).not.toHaveClass(/\bon\b/);
    // checking right in fullscreen: the item icon changes to a check mark
    await page.getByRole("button", { name: "Сбросить" }).click(); // preparation: starter -> own solution
    await editor(page).fill(`def parity(n):\n    return 'x'\n${unique()}\n`);
    await editor(page).press("Control+Enter");
    await serve(worker, passing(""));
    await expect(tree.nth(2)).toHaveClass(/\bok\b/);
    await expect(tree.nth(2).locator(".fst-slide-num")).toHaveText("✓");
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 2 из ${pyTasks.length}`);
    // "Свернуть" returns the normal view, the selected exercise stays
    await page.locator(".slide-fs .slide-btn", { hasText: "Свернуть" }).click();
    await expect(page.locator(".slide-fs")).toHaveCount(0);
    await expect(page.locator(".pr-head h3")).toHaveText(`3. ${pyTasks[2]!.title}`);
    guard.assertClean();
  });
});

test.describe("exercise reset in settings", () => {
  test("\"Сбросить прогресс упражнений\" erases statuses, drafts and history; declining the confirmation touches nothing", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await seed(request, token, worker, pyTasks[0]!, passing("1991\n"));
    await seed(request, token, worker, pyTasks[1]!, failing("int\n", "str\n"));
    const stateUrl = `/api/exercises/${PY.book}/${PY.num}/state`;
    const state = async () => (await (await request.get(stateUrl, { headers: bearer(token) })).json()) as { status: Record<string, string>; drafts: Record<string, string> };
    expect(Object.keys((await state()).status)).toHaveLength(2);

    await page.goto("/settings");
    const row = page.locator(".set-row", { hasText: "Сбросить прогресс упражнений" });
    // decline
    page.once("dialog", (d) => void d.dismiss());
    await row.getByRole("button", { name: "Сбросить", exact: true }).click();
    expect(Object.keys((await state()).status)).toHaveLength(2);
    // accept
    page.once("dialog", (d) => void d.accept());
    await row.getByRole("button", { name: "Сбросить", exact: true }).click();
    await expect.poll(async () => Object.keys((await state()).status).length).toBe(0);
    expect((await state()).drafts).toEqual({});
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: unknown[] };
    expect(attempts.attempts).toEqual([]);
    // practice is clean again
    await open(page, request);
    await expect(label(page)).toHaveText(`Решено 0 из ${pyTasks.length}`);
    await expect(page.locator(".pr-item.ok, .pr-item.bad")).toHaveCount(0);
    await expect(page.locator(".pr-hist")).toHaveCount(0);
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`0/${pyTasks.length}`);
  });
});

test.describe("chapter tabs", () => {
  // The "Теория" link points to the chapter address without a subpath and is considered current by prefix: it always has aria-current="page", even when
  // the "Вопросы" or "Практика" tab is open (a screen reader announces two current pages).
  test("aria-current=page only on the open tab", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const current = page.locator(".ch-tabs a[aria-current='page']");
    await expect(current).toHaveCount(1);
    await expect(current).toContainText("Практика");
  });

  test("switching tabs keeps the selected exercise in the practice tab address", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, `?task=${pyTasks[3]!.id}`);
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[3]!.title);
    await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
    await expect(page.locator(".quiz")).toBeVisible();
    await page.locator(".ch-tab", { hasText: "Практика" }).click();
    await expect(page.locator(".pr-main")).toBeVisible();
    // the tab opens from the first exercise (the pick lives in the address), the draft is not lost
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[0]!.title);
  });
});
