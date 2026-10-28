import { request as pwRequest, type APIRequestContext, type Locator, type Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import {
  FakeWorker,
  PORT,
  chapterPath,
  codeTasks,
  dockerReady,
  failing,
  learningGuard,
  passing,
  realWorkerRequested,
  startRealWorker,
  unique,
  waitNoWorkers,
  type CodeTask,
  type RealWorker,
} from "../../support/learning";

/* Code practice: exercise list and selection, editor, draft, hint, check queue, results, attempt history,
   the "База данных" widget for SQL tasks. The queue is driven by a fake worker (no Docker); the real sandbox runs with E2E_WORKER=1. */

const PY = { book: 13, num: 0 }; // 6 exercises: stdout and func
const SQL = { book: 9, num: 1 }; // 41 SQL exercises on the "shop" training database

const pyTasks = codeTasks(PY.book, PY.num);
const sqlTasks = codeTasks(SQL.book, SQL.num);

// --- locators and actions ------------------------------------------------------------------------

const items = (page: Page): Locator => page.locator(".pr-item");
const editor = (page: Page): Locator => page.locator("textarea.rs-input");
const mainBtn = (page: Page): Locator => page.locator(".ex-row button.quiz-btn").first();
const badge = (page: Page): Locator => page.locator(".pr-badge");
const result = (page: Page): Locator => page.locator(".pr-res");
const history = (page: Page): Locator => page.locator(".pr-hist-item");

async function open(page: Page, request: APIRequestContext, target = PY, task?: string): Promise<void> {
  const url = await chapterPath(request, target.book, target.num, "exercises");
  await page.goto(task ? `${url}?task=${task}` : url);
  await expect(page.locator(".pr-main")).toBeVisible();
}

/** Replace the solution text: a unique comment avoids hitting the result cache. */
async function typeCode(page: Page, code: string): Promise<string> {
  const full = `${code}\n${unique()}\n`;
  await editor(page).fill(full);
  return full;
}

/** Waits until the draft is sent to the server. */
async function savedDraft(page: Page, action: () => Promise<void>): Promise<void> {
  const sent = page.waitForResponse((r) => r.request().method() === "PUT" && r.url().includes("/draft"));
  await action();
  expect((await sent).status()).toBe(204);
}

/** One check round by the fake worker: waits for the job to appear and returns the result. */
async function serve(worker: FakeWorker, answer: Parameters<FakeWorker["complete"]>[1]) {
  const job = await worker.claim();
  expect(job, "the job reached the worker").not.toBeNull();
  await worker.complete(job!, answer);
  return job!;
}

const STARTER_OF = (t: CodeTask) => t.starter;

// ==================================================================================================
// Practice interface (no code checking needed)
// ==================================================================================================

test.describe("exercise list and selection", () => {
  test("list with statuses, header, statement and starter of the first exercise", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await open(page, request);
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 0 из ${pyTasks.length}`);
    await expect(page.locator(".pr-bar")).toHaveAttribute("aria-valuemax", String(pyTasks.length));
    await expect(page.locator(".pr-bar i")).toHaveAttribute("style", /width: 0%/);
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`0/${pyTasks.length}`);
    await expect(items(page)).toHaveCount(pyTasks.length);
    for (const [i, t] of pyTasks.entries()) {
      await expect(items(page).nth(i).locator(".pr-mark")).toHaveText(String(i + 1));
      await expect(items(page).nth(i).locator(".pr-name")).toHaveText(t.title);
    }
    await expect(items(page).first()).toHaveClass(/\bon\b/);
    await expect(items(page).locator(".on")).toHaveCount(0);
    await expect(page.locator(".pr-item.ok, .pr-item.bad")).toHaveCount(0);
    const first = pyTasks[0]!;
    await expect(page.locator(".pr-head h3")).toHaveText(`1. ${first.title}`);
    await expect(badge(page)).toHaveText("не решено");
    await expect(page.locator(".pr-statement")).toHaveText(first.statement);
    await expect(editor(page)).toHaveValue(STARTER_OF(first));
    await expect(result(page)).toContainText("Нажмите «Проверить»");
    await expect(page.locator(".pr-hist")).toHaveCount(0); // no attempts yet
    await expect(page.locator(".sx")).toHaveCount(0); // the database widget exists only for SQL tasks
    guard.assertClean();
  });

  test("exercise selection: ?task= address, title, statement, starter; direct link; unknown id falls back to the first", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await open(page, request);
    const t = pyTasks[2]!;
    await items(page).nth(2).click();
    await expect(page).toHaveURL(new RegExp(`/exercises\\?task=${t.id}$`));
    await expect(items(page).nth(2)).toHaveClass(/\bon\b/);
    await expect(items(page).first()).not.toHaveClass(/\bon\b/);
    await expect(page.locator(".pr-head h3")).toHaveText(`3. ${t.title}`);
    await expect(page.locator(".pr-statement")).toHaveText(t.statement);
    await expect(editor(page)).toHaveValue(STARTER_OF(t));
    // selection replaces the browser history entry: Back leaves the practice page instead of walking through tasks
    // direct link to an exercise
    const last = pyTasks[pyTasks.length - 1]!;
    await open(page, request, PY, last.id);
    await expect(page.locator(".pr-head h3")).toHaveText(`${pyTasks.length}. ${last.title}`);
    await expect(items(page).last()).toHaveClass(/\bon\b/);
    // unknown id -> the first one
    await open(page, request, PY, "no-such-id");
    await expect(page.locator(".pr-head h3")).toHaveText(`1. ${pyTasks[0]!.title}`);
    guard.assertClean();
  });

  test("on opening and on switching exercises the editor has focus and the cursor is at the end", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    await expect(editor(page)).toBeFocused();
    const caretAtEnd = () => editor(page).evaluate((el: HTMLTextAreaElement) => el.selectionStart === el.value.length && el.selectionEnd === el.value.length);
    expect(await caretAtEnd()).toBe(true);
    await items(page).nth(3).click();
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[3]!.title);
    await expect(editor(page)).toBeFocused();
    expect(await caretAtEnd()).toBe(true);
  });

  test("hint: show and hide, each exercise has its own", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const toggle = page.getByRole("button", { name: /подсказку$|^Подсказка$/ });
    await expect(toggle).toHaveText("Подсказка");
    await toggle.click();
    await expect(toggle).toHaveText("Скрыть подсказку");
    await expect(page.locator(".pr-main .ex-hint")).toHaveText(pyTasks[0]!.hint);
    await items(page).nth(1).click();
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[1]!.title);
    await expect(page.locator(".pr-main .ex-hint")).toHaveCount(0); // the second one has its hint closed
    await expect(page.getByRole("button", { name: "Подсказка", exact: true })).toBeVisible();
    await items(page).first().click();
    await expect(page.locator(".pr-main .ex-hint")).toHaveText(pyTasks[0]!.hint); // the first one stayed open
    await page.getByRole("button", { name: "Скрыть подсказку" }).click();
    await expect(page.locator(".pr-main .ex-hint")).toHaveCount(0);
  });
});

test.describe("code editor", () => {
  test("input, Python highlighting and Tab: indent instead of changing focus", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-parity");
    // in a starter with def the keywords are highlighted, a comment gets the muted color
    await editor(page).fill("# note\ndef f(n):\n    return 1\n");
    const shade = page.locator(".rs-shade");
    await expect(shade.locator(".rs-line")).toHaveCount(4);
    await expect(shade.locator("span", { hasText: /^def$/ })).toHaveAttribute("style", /color: var\(--(s|syn)-/);
    await expect(shade.locator("span", { hasText: /^return$/ })).toHaveAttribute("style", /color: var\(--(s|syn)-/);
    await expect(shade.locator("span", { hasText: "# note" })).toHaveAttribute("style", /--s-muted/);
    // Tab at the end of a line: four spaces, focus stays
    await editor(page).fill("ab");
    await editor(page).press("Tab");
    await expect(editor(page)).toHaveValue("ab    ");
    await expect(editor(page)).toBeFocused();
    // Tab at the start: indent on the left, text is not lost
    await editor(page).press("Home");
    await editor(page).press("Tab");
    await expect(editor(page)).toHaveValue("    ab    ");
    // Shift+Tab inserts no indent (moves focus as usual)
    await editor(page).press("Shift+Tab");
    await expect(editor(page)).toHaveValue("    ab    ");
    guard.assertClean();
  });

  test("the field grows with the line count, long lines do not break the layout", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const rows = async () => Number(await editor(page).getAttribute("rows"));
    expect(await rows()).toBe(6);
    await editor(page).fill(Array.from({ length: 15 }, (_, i) => `x${i} = ${i}`).join("\n"));
    await expect.poll(rows).toBe(15);
    await editor(page).fill("y = " + "1 + ".repeat(120) + "1");
    await expect(page.locator(".rs-shade .rs-line")).toHaveCount(1);
    expect(await rows()).toBe(6);
  });

  test("SQL and Rust highlighting is chosen by the task mode", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL);
    await expect(editor(page)).toHaveValue(sqlTasks[0]!.starter);
    await editor(page).fill("SELECT name FROM customers WHERE id > 1;");
    await expect(page.locator(".rs-shade span", { hasText: /^SELECT$/ })).toHaveAttribute("style", /color: var\(--(s|syn)-/);
    await expect(page.locator(".rs-shade span", { hasText: /^WHERE$/ })).toHaveAttribute("style", /color: var\(--(s|syn)-/);
  });
});

test.describe("draft", () => {
  test("typed code is sent to the server and returns after a reload", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await open(page, request);
    const code = "year = 1991\nprint(year)\n";
    await savedDraft(page, () => editor(page).fill(code));
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string>; status: Record<string, string> };
    expect(state.drafts[pyTasks[0]!.id]).toBe(code);
    expect(state.status).toEqual({});
    await page.reload();
    await expect(editor(page)).toHaveValue(code);
    // other exercises kept their starters
    await items(page).nth(1).click();
    await expect(editor(page)).toHaveValue(pyTasks[1]!.starter);
  });

  test("each exercise has its own draft, switching does not lose it", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    await editor(page).fill("one = 1\n");
    await items(page).nth(1).click();
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[1]!.title);
    await expect(editor(page)).toHaveValue(pyTasks[1]!.starter);
    await savedDraft(page, () => editor(page).fill("two = 2\n"));
    await items(page).first().click();
    await expect(editor(page)).toHaveValue("one = 1\n");
    await items(page).nth(1).click();
    await expect(editor(page)).toHaveValue("two = 2\n");
  });

  test("leaving the page saves the draft immediately, without a pause", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const sent = page.waitForResponse((r) => r.request().method() === "PUT" && r.url().includes("/draft"));
    await editor(page).fill("quick = 1\n");
    // no waiting: switch to theory; the practice page unmounts and flushes the draft
    await page.locator(".ch-tab", { hasText: "Теория" }).click();
    expect((await sent).status()).toBe(204);
    await page.goBack();
    await expect(editor(page)).toHaveValue("quick = 1\n");
  });

  test("\"Сбросить\" restores the starter and saves it as the draft", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await open(page, request);
    const t = pyTasks[0]!;
    await savedDraft(page, () => editor(page).fill("print('foreign code')\n"));
    await savedDraft(page, () => page.getByRole("button", { name: "Сбросить" }).click());
    await expect(editor(page)).toHaveValue(t.starter);
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string> };
    expect(state.drafts[t.id]).toBe(t.starter);
    await page.reload();
    await expect(editor(page)).toHaveValue(t.starter);
  });
});

test.describe("exercises API", () => {
  test("task list without tests and references, per-chapter stats, other users' data closed", async ({ page, request }) => {
    const raw = await (await request.get(`/api/exercises/${PY.book}/${PY.num}`)).text();
    const body = JSON.parse(raw) as { tasks: Record<string, unknown>[] };
    expect(body.tasks.map((t) => t.id)).toEqual(pyTasks.map((t) => t.id));
    for (const t of body.tasks) {
      expect(Object.keys(t).sort()).toEqual(expect.arrayContaining(["hint", "id", "mode", "starter", "statement", "title"]));
      expect(t).not.toHaveProperty("tests");
      expect(t).not.toHaveProperty("expected");
      expect(t).not.toHaveProperty("spec");
      expect(t).not.toHaveProperty("driver");
    }
    const counts = (await (await request.get("/api/exercises")).json()) as Record<string, Record<string, number>>;
    expect(counts[String(PY.book)]?.[String(PY.num)]).toBe(pyTasks.length);
    expect((await request.get("/api/exercises/13/9999")).status()).toBe(404);
    // state, draft, attempts and run are for signed-in users only
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/state`)).status()).toBe(401);
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/draft`, { data: { code: "x" } })).status()).toBe(401);
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`)).status()).toBe(401);
    expect((await request.post("/api/exercises/run", { data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "print(1)" } })).status()).toBe(401);
    expect((await request.get("/api/exercises/run/abc")).status()).toBe(401);
    // the worker API is closed by a token
    expect((await request.post("/internal/worker/ping", { data: { name: "x", lanes: ["light"] } })).status()).toBe(401);
    expect((await request.post("/internal/worker/ping", { headers: { Authorization: "Bearer nope" }, data: { name: "x", lanes: ["light"] } })).status()).toBe(401);
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/no-such-task/draft`, { headers: h, data: { code: "x" } })).status()).toBe(404);
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/no-such-task/attempts`, { headers: h })).status()).toBe(404);
    expect((await request.post("/api/exercises/run", { headers: h, data: { book: PY.book, chapter: PY.num, task: "no-such-task", code: "print(1)" } })).status()).toBe(404);
    expect((await request.get("/api/exercises/run/no-such-id", { headers: h })).status()).toBe(404);
    // a lab exercise is not checked in the sandbox and cannot be declared solved by hand
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/solved`, { headers: h, data: { solution: "x" } })).status()).toBe(404);
  });
});

// ==================================================================================================
// Check without a worker: the queue is unavailable. Runs first, because later fake workers keep the server "alive" for 30 seconds.
// ==================================================================================================

test.describe("check without a worker", () => {
  test("check status: no workers, empty queue", async ({ request }) => {
    await waitNoWorkers(request);
    const status = await (await request.get("/api/exercises/runner/status")).json();
    expect(status).toEqual({ queued: 0, running: 0, workers: 0, available: false });
  });

  test("Ctrl+Enter and the button: an unavailable message, status and history unchanged, the code stays", async ({ page, request }) => {
    const guard = learningGuard(page);
    await waitNoWorkers(request);
    const { token } = await loginFresh(page, request);
    await open(page, request);
    const code = await typeCode(page, "print(1991)");
    const posts: number[] = [];
    page.on("response", (r) => {
      if (r.request().method() === "POST" && r.url().endsWith("/api/exercises/run")) posts.push(r.status());
    });
    await editor(page).press("Control+Enter");
    const unavailable = result(page).locator(".cx-error");
    await expect(unavailable).toContainText("Проверка кода временно недоступна");
    await expect(result(page)).toContainText("Тесты не запускались");
    await expect(result(page).locator(".pr-res-sum")).toHaveCount(0);
    expect(posts).toEqual([503]);
    // nothing counted or recorded
    await expect(badge(page)).toHaveText("не решено");
    await expect(items(page).first().locator(".pr-mark")).toHaveText("1");
    await expect(page.locator(".pr-hist")).toHaveCount(0);
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(mainBtn(page)).toBeEnabled();
    await expect(editor(page)).toHaveValue(code);
    // the button does the same
    await mainBtn(page).click();
    await expect.poll(() => posts.length).toBe(2);
    await expect(unavailable).toContainText("временно недоступна");
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: unknown[] };
    expect(attempts.attempts).toEqual([]);
    guard.assertClean();
  });

  test("overload notice: service under development, closing, not imposed again", async ({ page, request }) => {
    const guard = learningGuard(page);
    await waitNoWorkers(request);
    await loginFresh(page, request);
    await open(page, request);
    await typeCode(page, "print(1991)");
    const notice = page.locator(".overload");
    await expect(notice).toHaveCount(0);
    await mainBtn(page).click();
    await expect(notice).toBeVisible();
    await expect(notice).toContainText("Проверка кода сейчас недоступна");
    await expect(notice).toContainText("в стадии развития");
    await expect(notice).toContainText("не выдерживает большую нагрузку");
    await expect(notice.getByRole("link")).toHaveCount(0);
    // closed: the next refusal within a minute does not bring the notice back, the message in results stays
    await notice.getByRole("button", { name: "Понятно" }).click();
    await expect(notice).toHaveCount(0);
    await mainBtn(page).click();
    await expect(result(page).locator(".cx-error")).toContainText("временно недоступна");
    await expect(notice).toHaveCount(0);
    guard.assertClean();
  });

  test("empty code does not enter the queue: the server answers with a message", async ({ page, request }) => {
    const guard = learningGuard(page);
    await waitNoWorkers(request);
    await loginFresh(page, request);
    await open(page, request);
    await editor(page).fill("   \n");
    await editor(page).press("Control+Enter");
    await expect(result(page).locator(".cx-error")).toContainText("Пустой код");
    await expect(page.locator(".pr-hist")).toHaveCount(0);
    guard.assertClean();
  });

  test("a too long solution is rejected", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "x".repeat(20_001) } });
    expect(res.status()).toBe(422);
  });
});

// ==================================================================================================
// The "База данных" widget for SQL tasks
// ==================================================================================================

interface Col {
  name: string;
  pk?: boolean;
  fk?: unknown;
}
interface Table {
  name: string;
  total: number;
  columns: Col[];
  rows: unknown[][];
}
interface Dataset {
  tables: Table[];
  relations: unknown[];
}

async function datasetOf(request: APIRequestContext, target = SQL): Promise<Dataset> {
  const body = (await (await request.get(`/api/exercises/${target.book}/${target.num}`)).json()) as { tasks: { dataset?: string }[]; datasets: Record<string, Dataset> };
  const key = body.tasks.find((t) => t.dataset)?.dataset;
  expect(key, "an SQL task has a dataset").toBeTruthy();
  return body.datasets[key!]!;
}

test.describe("SQL: the \"База данных\" widget", () => {
  const tableBox = (page: Page, name: string) => page.locator(".sx-tbl", { has: page.locator(".sx-name", { hasText: new RegExp(`^${name}$`) }) });
  const transform = (loc: Locator) => loc.getAttribute("transform");

  test("ERD: tables with columns and relations, caption with the table count", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const data = await datasetOf(request);
    await open(page, request, SQL);
    await expect(page.locator(".pr-statement")).toHaveText(sqlTasks[0]!.statement);
    const widget = page.locator(".sx");
    await expect(widget).toBeVisible();
    await expect(widget.locator(".sx-fold")).toContainText("База данных");
    await expect(widget.locator(".sx-fold em")).toHaveText(new RegExp(`^${data.tables.length} (таблица|таблицы|таблиц)`));
    await expect(widget.locator(".sx-seg button.on")).toHaveText("ERD");
    await expect(widget.locator("svg[aria-label='ERD-диаграмма учебной базы']")).toBeVisible();
    await expect(widget.locator(".sx-tbl")).toHaveCount(data.tables.length);
    await expect(widget.locator(".sx-rel")).toHaveCount(data.relations.length);
    for (const t of data.tables) {
      const box = tableBox(page, t.name);
      await expect(box).toHaveCount(1);
      await expect(box.locator(".sx-count")).toHaveText(String(t.total));
      await expect(box.locator(".sx-col")).toHaveText(t.columns.map((c) => c.name));
      await expect(box.locator(".sx-key", { hasText: "PK" })).toHaveCount(t.columns.filter((c) => c.pk).length);
      await expect(box.locator(".sx-key", { hasText: "FK" })).toHaveCount(t.columns.filter((c) => c.fk && !c.pk).length);
    }
    await expect(widget.locator(".sx-erd-foot")).toContainText("PK — первичный ключ");
    guard.assertClean();
  });

  test("\"Данные\" tab: one table per tab, rows and columns as on the server", async ({ page, request }) => {
    await loginFresh(page, request);
    const data = await datasetOf(request);
    await open(page, request, SQL);
    await page.locator(".sx-seg button", { hasText: "Данные" }).click();
    await expect(page.locator(".sx-seg button.on")).toHaveText("Данные");
    const tabs = page.locator(".sx-tab");
    await expect(tabs).toHaveCount(data.tables.length);
    for (const [i, t] of data.tables.entries()) {
      await expect(tabs.nth(i)).toContainText(t.name);
      await expect(tabs.nth(i).locator("em")).toHaveText(String(t.total));
      await tabs.nth(i).click();
      await expect(tabs.nth(i)).toHaveClass(/\bon\b/);
      await expect(tabs.nth(i)).toHaveAttribute("aria-selected", "true");
      await expect(page.locator(".sx-grid thead th")).toHaveCount(t.columns.length);
      await expect(page.locator(".sx-grid tbody tr")).toHaveCount(Math.max(1, t.rows.length));
      await expect(page.locator(".sx-grid thead th").first()).toContainText(t.columns[0]!.name);
      if (t.total > t.rows.length) await expect(page.locator(".sx-more")).toContainText(`из ${t.total}`);
    }
    // NULL is shown separately from an empty string (some customers have no e-mail and no city)
    await tabs.first().click();
    await expect(page.locator(".sx-grid .sx-null").first()).toHaveText("NULL");
  });

  test("clicking a table on the diagram opens its data; dragging moves it but does not open the data", async ({ page, request }) => {
    await loginFresh(page, request);
    const data = await datasetOf(request);
    await open(page, request, SQL);
    const target = data.tables[1]!;
    const box = tableBox(page, target.name);
    const before = await transform(box);
    // dragging: the table moves, the view stays ERD
    const rect = (await box.locator(".sx-frame").boundingBox())!;
    const [x, y] = [rect.x + rect.width / 2, rect.y + 12];
    await page.mouse.move(x, y);
    await page.mouse.down();
    await page.mouse.move(x + 40, y + 60, { steps: 6 });
    await page.mouse.up();
    const moved = await transform(box);
    expect(moved).not.toBe(before);
    await expect(page.locator(".sx-seg button.on")).toHaveText("ERD");
    // "расставить заново" restores the layout
    await page.getByRole("button", { name: "расставить заново" }).click();
    expect(await transform(box)).toBe(before);
    // click without moving: the "Данные" tab of this table
    await box.locator(".sx-frame").click();
    await expect(page.locator(".sx-seg button.on")).toHaveText("Данные");
    await expect(page.locator(".sx-tab.on")).toContainText(target.name);
  });

  test("hovering highlights related tables", async ({ page, request }) => {
    await loginFresh(page, request);
    const data = await datasetOf(request);
    await open(page, request, SQL);
    const orders = tableBox(page, "orders");
    await expect(orders).toHaveCount(1);
    await orders.locator(".sx-frame").hover();
    await expect(orders).toHaveClass(/\bon\b/);
    await expect(page.locator(".sx-tbl.linked").first()).toBeVisible();
    await expect(page.locator(".sx-rel.on").first()).toBeVisible();
    await page.locator(".pr-statement").hover();
    await expect(page.locator(".sx-tbl.on, .sx-tbl.linked")).toHaveCount(0);
    expect(data.relations.length).toBeGreaterThan(0);
  });

  test("collapsed state and view are remembered across reloads", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL);
    await page.locator(".sx-seg button", { hasText: "Данные" }).click();
    await page.reload();
    await expect(page.locator(".sx-seg button.on")).toHaveText("Данные"); // view is remembered
    await page.locator(".sx-fold").click();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(".sx-data, .sx-erd")).toHaveCount(0);
    await page.reload();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(".sx-data, .sx-erd")).toHaveCount(0);
    // choosing a view while the widget is collapsed expands it
    await page.locator(".sx-seg button", { hasText: "ERD" }).click();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator(".sx-erd")).toBeVisible();
  });

  test("the widget exists for every SQL task of the chapter and disappears for tasks without a database", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL, sqlTasks[9]!.id);
    await expect(page.locator(".sx")).toBeVisible();
    await open(page, request, SQL, sqlTasks[sqlTasks.length - 1]!.id);
    await expect(page.locator(".sx")).toBeVisible();
    await open(page, request, PY);
    await expect(page.locator(".sx")).toHaveCount(0);
  });
});

// ==================================================================================================
// Queue and results: fake worker
// ==================================================================================================

test.describe("queue and results (fake worker)", () => {
  test("\"в очереди\" -> \"выполняется\" -> failed: a test with expected and received, history, status cross", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const t = pyTasks[2]!; // intro-parity, func
    await open(page, request, PY, t.id);
    const code = await typeCode(page, "def parity(n):\n    return 'even'");
    await mainBtn(page).click();
    // the request is queued: the button and the result panel say so, the button is disabled
    await expect(mainBtn(page)).toHaveText("В очереди…");
    await expect(mainBtn(page)).toBeDisabled();
    await expect(result(page)).toContainText("В очереди…");
    const status = await (await request.get("/api/exercises/runner/status")).json();
    expect(status).toMatchObject({ queued: 1, available: true });
    // the worker took the job: the solution and the task arrived undistorted
    const job = await worker.claim();
    expect(job!.task.id).toBe(t.id);
    expect(job!.code).toBe(code);
    await expect(result(page)).toContainText("Выполняется в песочнице…");
    await expect(mainBtn(page)).toHaveText("Проверяю…");
    await worker.complete(job!, {
      status: "ok",
      results: [
        { ok: true, args: "[4]", expected: "even", got: "even" },
        { ok: false, args: "[7]", expected: "odd", got: "even" },
      ],
      stdout: "",
    });
    // result
    await expect(result(page).locator(".pr-res-sum")).toHaveText("1 из 2");
    await expect(result(page).locator(".pr-res-sum")).toHaveClass(/\bbad\b/);
    await expect(result(page).locator(".pr-test")).toHaveCount(2);
    await expect(result(page).locator(".pr-test.ok")).toContainText("тест 1");
    await expect(result(page).locator(".pr-test.ok")).toContainText("вызов [4]");
    const bad = result(page).locator(".pr-test.bad");
    await expect(bad).toContainText("тест 2");
    await expect(bad).toContainText("вызов [7]");
    await expect(bad.locator(".pr-diff > div").nth(0)).toContainText("odd"); // expected
    await expect(bad.locator(".pr-diff > div").nth(0).locator(".s-label")).toHaveText("ожидалось");
    await expect(bad.locator(".pr-diff > div").nth(1).locator(".s-label")).toHaveText("получено");
    await expect(bad.locator(".pr-diff > div").nth(1).locator("pre")).toHaveText("even");
    await expect(result(page)).toContainText("программа ничего не вывела");
    // status "не пройдено", the button is "Проверить" again
    await expect(badge(page)).toHaveText("не пройдено");
    await expect(badge(page)).toHaveClass(/\bbad\b/);
    await expect(items(page).nth(2)).toHaveClass(/\bbad\b/);
    await expect(items(page).nth(2).locator(".pr-mark")).toHaveText("✗");
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 0 из ${pyTasks.length}`);
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(mainBtn(page)).toBeEnabled();
    // history: one failed attempt with this code
    await expect(history(page)).toHaveCount(1);
    await expect(history(page).first()).toHaveClass(/\bbad\b/);
    await expect(history(page).first().locator(".pr-hist-n")).toHaveText("#1");
    await expect(history(page).first().locator(".pr-hist-mark")).toHaveText("✗");
    await expect(history(page).first().locator(".pr-hist-score")).toHaveText("1/2");
    await expect(history(page).first().locator(".pr-hist-code")).toHaveText("def parity(n):");
    await expect(history(page).first()).toHaveClass(/\bon\b/);
    await expect(page.locator(".pr-hist .pr-res-time")).toHaveText("1");
    // and on the server
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { status: Record<string, string> };
    expect(state.status[t.id]).toBe("bad");
    guard.assertClean();
  });

  test("solved: check mark, \"выполнено\", \"Решено 1 из N\", \"Дальше →\"; editing the code brings back \"Проверить\"", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const t = pyTasks[0]!;
    await open(page, request);
    const code = await typeCode(page, "year = 1991\nprint(year)");
    await editor(page).press("Control+Enter");
    await serve(worker, passing("1991\n"));
    await expect(badge(page)).toHaveText("выполнено");
    await expect(badge(page)).toHaveClass(/\bok\b/);
    await expect(result(page).locator(".pr-res-sum")).toHaveText("1 из 1");
    await expect(result(page).locator(".pr-res-sum")).toHaveClass(/\bok\b/);
    await expect(result(page).locator(".pr-log")).toHaveText("1991");
    await expect(items(page).first()).toHaveClass(/\bok\b/);
    await expect(items(page).first().locator(".pr-mark")).toHaveText("✓");
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 1 из ${pyTasks.length}`);
    await expect(page.locator(".pr-bar i")).toHaveAttribute("style", new RegExp(`width: ${Math.floor(100 / pyTasks.length)}%`));
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`1/${pyTasks.length}`);
    await expect(page.locator(".rs-editor")).toHaveClass(/\bright\b/);
    // accepted solution: "Дальше →" and "Проверить ещё раз" instead of "Проверить"
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await expect(page.getByRole("button", { name: "Проверить ещё раз" })).toBeVisible();
    await expect(history(page)).toHaveCount(1);
    await expect(history(page).first()).toHaveClass(/\bok\b/);
    await expect(history(page).first().locator(".pr-hist-mark")).toHaveText("✓");
    // editing an accepted solution: "Проверить", the green frame goes away; the "выполнено" status stays
    await editor(page).press("End");
    await editor(page).pressSequentially(" ");
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(page.locator(".rs-editor")).not.toHaveClass(/\bright\b/);
    await expect(badge(page)).toHaveText("выполнено");
    // restored the old text: "Дальше →" again
    await editor(page).fill(code);
    await expect(mainBtn(page)).toHaveText("Дальше →");
    // server: status, attempt with the code
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { status: Record<string, string> };
    expect(state.status[t.id]).toBe("ok");
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${t.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: { code: string; status: string; passed: number; total: number }[] };
    expect(attempts.attempts).toHaveLength(1);
    expect(attempts.attempts[0]).toMatchObject({ code, status: "ok", passed: 1, total: 1 });
    guard.assertClean();
  });

  test("solved stays solved: after a reload statuses, counters, draft and history are in place; a failure does not undo it", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const t = pyTasks[0]!;
    await open(page, request);
    const good = await typeCode(page, "year = 1991\nprint(year)");
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(badge(page)).toHaveText("выполнено");
    // a new failed attempt does not roll the status back
    const worse = await typeCode(page, "print(1990)");
    await mainBtn(page).click();
    await serve(worker, failing("1991\n", "1990\n"));
    await expect(result(page).locator(".pr-res-sum")).toHaveText("0 из 1");
    await expect(badge(page)).toHaveText("выполнено");
    await expect(items(page).first().locator(".pr-mark")).toHaveText("✓");
    await expect(history(page)).toHaveCount(2);
    await expect(history(page).nth(0).locator(".pr-hist-n")).toHaveText("#2");
    await expect(history(page).nth(0).locator(".pr-hist-mark")).toHaveText("✗");
    await expect(history(page).nth(1).locator(".pr-hist-mark")).toHaveText("✓");
    // the draft (the last typed code) is already on the server
    await expect
      .poll(async () => ((await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string> }).drafts[t.id])
      .toBe(worse);
    // reload
    await page.reload();
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 1 из ${pyTasks.length}`);
    await expect(items(page).first()).toHaveClass(/\bok\b/);
    await expect(badge(page)).toHaveText("выполнено");
    await expect(editor(page)).toHaveValue(worse); // the draft is the last typed code
    await expect(history(page)).toHaveCount(2);
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`1/${pyTasks.length}`);
    // a click on an accepted attempt returns its code to the editor and enables "Дальше →"
    await history(page).nth(1).click();
    await expect(editor(page)).toHaveValue(good);
    await expect(history(page).nth(1)).toHaveClass(/\bon\b/);
    await expect(history(page).nth(0)).not.toHaveClass(/\bon\b/);
    await expect(mainBtn(page)).toHaveText("Дальше →");
    // ...and a click on the failed one goes back
    await history(page).nth(0).click();
    await expect(editor(page)).toHaveValue(worse);
    await expect(mainBtn(page)).toHaveText("Проверить");
    guard.assertClean();
  });

  test("queue: position \"перед вами N\", one check per user, order of handing out to the worker", async ({ page, request, browser }) => {
    const tokenA = (await loginFresh(page, request)).token;
    const other = await browser.newContext();
    const pageB = await other.newPage();
    await loginFresh(pageB, other.request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await open(pageB, request);
    const codeA = await typeCode(page, "print(1)");
    const codeB = await typeCode(pageB, "print(2)");
    await mainBtn(page).click();
    await expect(result(page)).toContainText("В очереди…");
    // a repeated submission by the same user while a check is running is rejected
    const dup = await request.post("/api/exercises/run", { headers: bearer(tokenA), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "print(3)" } });
    expect(dup.status()).toBe(429);
    expect(await dup.text()).toContain("The previous check is still running");
    // repeated clicks do not queue a second request: the button is disabled
    await expect(mainBtn(page)).toBeDisabled();
    await editor(page).press("Control+Enter");
    // the second user goes right after the first
    await mainBtn(pageB).click();
    await expect(result(pageB)).toContainText("В очереди (перед вами 1)…");
    const queued = await (await request.get("/api/exercises/runner/status")).json();
    expect(queued).toMatchObject({ queued: 2, running: 0 });
    // the worker receives requests in submission order
    const first = await worker.claim();
    expect(first!.code).toBe(codeA);
    await expect(result(page)).toContainText("Выполняется в песочнице…");
    await expect(result(pageB)).toContainText("В очереди…");
    await expect(result(pageB)).not.toContainText("перед вами");
    await worker.complete(first!, passing("1\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    const second = await worker.claim();
    expect(second!.code).toBe(codeB);
    await worker.complete(second!, failing("1991\n", "2\n"));
    await expect(pageB.locator(".pr-res-sum")).toHaveText("0 из 1");
    // each has own result, status and history
    await expect(badge(pageB)).toHaveText("не пройдено");
    await expect(badge(page)).toHaveText("выполнено");
    await other.close();
  });

  test("cached result: the same solution from another user is accepted at once, without waiting for the worker", async ({ page, request, browser }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    const code = await typeCode(page, "year = 1991\nprint(year)");
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(badge(page)).toHaveText("выполнено");
    // another user submits exactly the same code: the answer is ready at once, no worker needed
    const other = await browser.newContext();
    const { token } = await loginFresh(await other.newPage(), other.request);
    const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code } });
    expect(res.status()).toBe(202);
    expect(await res.json()).toMatchObject({ state: "done", solved: true, passed: 1, total: 1 });
    expect(await (await request.get("/api/exercises/runner/status")).json()).toMatchObject({ queued: 0, running: 0 });
    await other.close();
    // the same code with another task misses the cache: the key is task plus code
    const { token: t2 } = await loginFresh(page, request);
    const other2 = await request.post("/api/exercises/run", { headers: bearer(t2), data: { book: PY.book, chapter: PY.num, task: pyTasks[1]!.id, code } });
    expect(other2.status()).toBe(202);
    expect(await other2.json()).toMatchObject({ state: "queued" });
    const job = await worker.claim();
    await worker.complete(job!, failing("int\n", "1991\n")); // free the queue
  });

  test("results of different kinds: runtime error, time limit, program output", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request, PY, "intro-loop");
    // error before the tests run: traceback in the logs, no tests
    await typeCode(page, "for i in range(3)\n    print(i)");
    await mainBtn(page).click();
    await serve(worker, { status: "error", results: [], stdout: "", stderr: "SyntaxError: expected ':'" });
    await expect(result(page)).toContainText("Тесты не запускались");
    await expect(result(page).locator(".cx-error")).toHaveText("SyntaxError: expected ':'");
    await expect(result(page).locator(".pr-res-sum")).toHaveCount(0);
    await expect(badge(page)).toHaveText("не пройдено");
    // time limit
    await typeCode(page, "while True:\n    pass");
    await mainBtn(page).click();
    await serve(worker, { status: "timeout", results: [], stdout: "", stderr: "" });
    await expect(result(page)).toContainText("Проверка не уложилась в лимит времени");
    await expect(result(page)).not.toContainText("Тесты не запускались");
    // program output (stdout mode): visible in the logs, a mismatch shows "ожидалось/получено"
    await typeCode(page, "for i in range(1, 4):\n    print(i)");
    await mainBtn(page).click();
    await serve(worker, { status: "ok", results: [{ ok: false, expected: "1\n2\n3\n4\n5\n", got: "1\n2\n3\n" }], stdout: "1\n2\n3\n" });
    await expect(result(page).locator(".pr-log")).toHaveText("1\n2\n3");
    await expect(result(page).locator(".pr-test.bad .pr-diff pre").first()).toHaveText("1\n2\n3\n4\n5\n");
    await expect(result(page).locator(".pr-test.bad .pr-diff pre").nth(1)).toHaveText("1\n2\n3\n");
    await expect(history(page)).toHaveCount(3);
    guard.assertClean();
  });

  test("SQL: a wrong result is shown as two tables with highlighted differences", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request, SQL);
    await typeCode(page, "SELECT id, name FROM customers");
    await mainBtn(page).click();
    await serve(worker, {
      status: "ok",
      results: [
        {
          ok: false,
          kind: "rows",
          ordered: false,
          got_cols: ["id", "name"],
          got_rows: [[1, "Anna"], [2, "Boris"], [9, "Extra"]],
          got_total: 3,
          exp_cols: ["id", "name"],
          exp_rows: [[1, "Anna"], [2, "Boris"], [3, "Vera"]],
          exp_total: 3,
        },
      ],
      stdout: "",
    });
    const diff = result(page).locator(".sd");
    await expect(diff).toBeVisible();
    await expect(diff.locator(".sd-side")).toHaveCount(2);
    await expect(diff.locator(".sd-side.got .sd-count")).toHaveText("3 строки");
    await expect(diff.locator(".sd-side.exp .sd-count")).toHaveText("3 строки");
    // matching rows are not highlighted; the extra row of the student and the missing row of the reference are marked
    await expect(diff.locator(".sd-side.got .sd-ok")).toHaveCount(2);
    await expect(diff.locator(".sd-side.exp .sd-ok")).toHaveCount(2);
    await expect(diff.locator(".sd-side.got tr.sd-diff, .sd-side.got tr.sd-extra")).toHaveCount(1);
    await expect(diff.locator(".sd-side.exp tr.sd-diff, .sd-side.exp tr.sd-missing")).toHaveCount(1);
    await expect(diff.locator(".sd-side.got td.extra").first()).toContainText(/Extra|9/);
    await expect(diff.locator(".sd-side.exp td.missing").first()).toContainText(/Vera|3/);
    await expect(diff.locator(".sd-legend")).toContainText("лишнее или неверное значение у вас");
    await expect(badge(page)).toHaveText("не пройдено");
    guard.assertClean();
  });

  test("after solving, Ctrl+Enter opens the next exercise (and so does the \"Дальше →\" button)", async ({ page, request }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await typeCode(page, "year = 1991\nprint(year)");
    await editor(page).press("Control+Enter");
    await serve(worker, passing("1991\n"));
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await editor(page).press("Control+Enter");
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[1]!.id}$`));
    await expect(page.locator(".pr-head h3")).toHaveText(`2. ${pyTasks[1]!.title}`);
    await expect(editor(page)).toBeFocused();
    // solve the second one and leave by the button
    await typeCode(page, 'print(type(5).__name__)');
    await mainBtn(page).click();
    await serve(worker, passing("int\n"));
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await mainBtn(page).click();
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[2]!.id}$`));
  });
});

// ==================================================================================================
// Real sandbox: E2E_WORKER=1, Docker and the python:3.13-slim image
// ==================================================================================================

test.describe("real check in the sandbox", () => {
  test.describe.configure({ mode: "serial", timeout: 180_000 });
  test.skip(!realWorkerRequested, "E2E_WORKER=1 is not set: the real check is disabled");
  test.skip(realWorkerRequested && !dockerReady(), "Docker is unavailable or the python:3.13-slim image is missing");

  let worker: RealWorker | undefined;
  test.beforeAll(async () => {
    const api = await pwRequest.newContext({ baseURL: `http://127.0.0.1:${PORT}` });
    try {
      worker = await startRealWorker(api);
    } finally {
      await api.dispose();
    }
  });
  test.afterAll(async () => {
    await worker?.stop();
  });

  const verdict = (page: Page, text: string) => expect(badge(page)).toHaveText(text, { timeout: 150_000 });

  test("Python, stdout mode: a correct solution is accepted, a wrong one shows expected and received", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-variable");
    await editor(page).fill("year = 1990\nprint(year)\n");
    await mainBtn(page).click();
    await verdict(page, "не пройдено");
    await expect(result(page).locator(".pr-test.bad")).toHaveCount(1);
    await expect(result(page).locator(".pr-test.bad .pr-diff pre").nth(1)).toContainText("1990");
    await editor(page).fill("year = 1991\nprint(year)\n");
    await mainBtn(page).click();
    await verdict(page, "выполнено");
    await expect(result(page).locator(".pr-res-sum")).toHaveText("1 из 1");
    await expect(result(page).locator(".pr-log")).toHaveText("1991");
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await expect(history(page)).toHaveCount(2);
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 1 из ${pyTasks.length}`);
    guard.assertClean();
  });

  test("Python, func mode: all tests pass for a correct solution; a wrong one fails with call arguments", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-parity");
    await editor(page).fill("def parity(n):\n    return 'чётное'\n");
    await mainBtn(page).click();
    await verdict(page, "не пройдено");
    await expect(result(page).locator(".pr-res-sum")).toHaveText("2 из 4");
    await expect(result(page).locator(".pr-test.bad")).toHaveCount(2);
    await expect(result(page).locator(".pr-test.bad").first()).toContainText("вызов [7]");
    await editor(page).fill("def parity(n):\n    return 'чётное' if n % 2 == 0 else 'нечётное'\n");
    await mainBtn(page).click();
    await verdict(page, "выполнено");
    await expect(result(page).locator(".pr-res-sum")).toHaveText("4 из 4");
  });

  test("an empty starter fails, an infinite loop hits the time limit", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-loop");
    await mainBtn(page).click(); // the starter is a single comment
    await verdict(page, "не пройдено");
    await expect(result(page).locator(".pr-test.bad")).toHaveCount(1);
    await editor(page).fill("while True:\n    pass\n");
    await mainBtn(page).click();
    await expect(result(page)).toContainText("Проверка не уложилась в лимит времени", { timeout: 150_000 });
  });

  test("SQL: a correct query is accepted, a foreign table gives two tables with differences", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL, "s01-01");
    await editor(page).fill("SELECT * FROM products;\n");
    await mainBtn(page).click();
    await verdict(page, "не пройдено");
    await expect(result(page).locator(".sd")).toBeVisible();
    await expect(result(page).locator(".sd-side")).toHaveCount(2);
    await editor(page).fill("SELECT * FROM customers;\n");
    await mainBtn(page).click();
    await verdict(page, "выполнено");
    await expect(result(page).locator(".pr-res-sum")).toHaveClass(/\bok\b/);
  });
});
