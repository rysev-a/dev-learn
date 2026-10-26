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

/* Практика с кодом: список и выбор упражнений, редактор, черновик, подсказка, очередь проверки, результаты, история попыток,
   виджет «База данных» у SQL-задач. Очередью управляет подставной воркер (без Docker); настоящая песочница — при E2E_WORKER=1. */

const PY = { book: 13, num: 0 }; // 6 упражнений: stdout и func
const SQL = { book: 9, num: 1 }; // 41 SQL-упражнение на учебной базе «магазин»

const pyTasks = codeTasks(PY.book, PY.num);
const sqlTasks = codeTasks(SQL.book, SQL.num);

// --- локаторы и действия ------------------------------------------------------------------------

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

/** Подменить текст решения: уникальный комментарий исключает попадание в кэш результатов. */
async function typeCode(page: Page, code: string): Promise<string> {
  const full = `${code}\n${unique()}\n`;
  await editor(page).fill(full);
  return full;
}

/** Ждёт, пока черновик уйдёт на сервер. */
async function savedDraft(page: Page, action: () => Promise<void>): Promise<void> {
  const sent = page.waitForResponse((r) => r.request().method() === "PUT" && r.url().includes("/draft"));
  await action();
  expect((await sent).status()).toBe(204);
}

/** Один круг проверки подставным воркером: ждёт появления задания и возвращает результат. */
async function serve(worker: FakeWorker, answer: Parameters<FakeWorker["complete"]>[1]) {
  const job = await worker.claim();
  expect(job, "задание дошло до воркера").not.toBeNull();
  await worker.complete(job!, answer);
  return job!;
}

const STARTER_OF = (t: CodeTask) => t.starter;

// ==================================================================================================
// Интерфейс практики (проверка кода не нужна)
// ==================================================================================================

test.describe("список и выбор упражнений", () => {
  test("список со статусами, шапка, условие и заготовка первого упражнения", async ({ page, request, guard }) => {
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
    await expect(page.locator(".pr-hist")).toHaveCount(0); // попыток ещё не было
    await expect(page.locator(".sx")).toHaveCount(0); // виджет базы данных только у SQL-задач
    guard.assertClean();
  });

  test("выбор упражнения: адрес ?task=, заголовок, условие, заготовка; прямая ссылка; неизвестный id — первое", async ({ page, request, guard }) => {
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
    // выбор заменяет запись в истории браузера: «Назад» уходит со страницы практики, а не по задачам
    // прямая ссылка на упражнение
    const last = pyTasks[pyTasks.length - 1]!;
    await open(page, request, PY, last.id);
    await expect(page.locator(".pr-head h3")).toHaveText(`${pyTasks.length}. ${last.title}`);
    await expect(items(page).last()).toHaveClass(/\bon\b/);
    // неизвестный id → первое
    await open(page, request, PY, "нет-такого");
    await expect(page.locator(".pr-head h3")).toHaveText(`1. ${pyTasks[0]!.title}`);
    guard.assertClean();
  });

  test("при открытии и при смене упражнения фокус в редакторе, курсор в конце", async ({ page, request }) => {
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

  test("подсказка: показать и скрыть, у каждого упражнения своя", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const toggle = page.getByRole("button", { name: /подсказку$|^Подсказка$/ });
    await expect(toggle).toHaveText("Подсказка");
    await toggle.click();
    await expect(toggle).toHaveText("Скрыть подсказку");
    await expect(page.locator(".pr-main .ex-hint")).toHaveText(pyTasks[0]!.hint);
    await items(page).nth(1).click();
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[1]!.title);
    await expect(page.locator(".pr-main .ex-hint")).toHaveCount(0); // у второго подсказка закрыта
    await expect(page.getByRole("button", { name: "Подсказка", exact: true })).toBeVisible();
    await items(page).first().click();
    await expect(page.locator(".pr-main .ex-hint")).toHaveText(pyTasks[0]!.hint); // первая осталась открытой
    await page.getByRole("button", { name: "Скрыть подсказку" }).click();
    await expect(page.locator(".pr-main .ex-hint")).toHaveCount(0);
  });
});

test.describe("редактор кода", () => {
  test("ввод, подсветка Python и Tab: отступ вместо смены фокуса", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-parity");
    // у заготовки с def подсвечены ключевые слова, у комментария — приглушённый цвет
    await editor(page).fill("# заметка\ndef f(n):\n    return 1\n");
    const shade = page.locator(".rs-shade");
    await expect(shade.locator(".rs-line")).toHaveCount(4);
    await expect(shade.locator("span", { hasText: /^def$/ })).toHaveAttribute("style", /color: var\(--s-/);
    await expect(shade.locator("span", { hasText: /^return$/ })).toHaveAttribute("style", /color: var\(--s-/);
    await expect(shade.locator("span", { hasText: "# заметка" })).toHaveAttribute("style", /--s-muted/);
    // Tab в конце строки: четыре пробела, фокус остаётся
    await editor(page).fill("ab");
    await editor(page).press("Tab");
    await expect(editor(page)).toHaveValue("ab    ");
    await expect(editor(page)).toBeFocused();
    // Tab в начале: отступ слева, текст не теряется
    await editor(page).press("Home");
    await editor(page).press("Tab");
    await expect(editor(page)).toHaveValue("    ab    ");
    // Shift+Tab не вставляет отступ (уводит фокус как обычно)
    await editor(page).press("Shift+Tab");
    await expect(editor(page)).toHaveValue("    ab    ");
    guard.assertClean();
  });

  test("поле растёт с числом строк, длинные строки не ломают разметку", async ({ page, request }) => {
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

  test("подсветка SQL и Rust выбирается по режиму задачи", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL);
    await expect(editor(page)).toHaveValue(sqlTasks[0]!.starter);
    await editor(page).fill("SELECT name FROM customers WHERE id > 1;");
    await expect(page.locator(".rs-shade span", { hasText: /^SELECT$/ })).toHaveAttribute("style", /color: var\(--s-/);
    await expect(page.locator(".rs-shade span", { hasText: /^WHERE$/ })).toHaveAttribute("style", /color: var\(--s-/);
  });
});

test.describe("черновик", () => {
  test("набранный код уходит на сервер и возвращается после перезагрузки", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await open(page, request);
    const code = "year = 1991\nprint(year)\n";
    await savedDraft(page, () => editor(page).fill(code));
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string>; status: Record<string, string> };
    expect(state.drafts[pyTasks[0]!.id]).toBe(code);
    expect(state.status).toEqual({});
    await page.reload();
    await expect(editor(page)).toHaveValue(code);
    // другие упражнения остались с заготовками
    await items(page).nth(1).click();
    await expect(editor(page)).toHaveValue(pyTasks[1]!.starter);
  });

  test("у каждого упражнения свой черновик, переключение его не теряет", async ({ page, request }) => {
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

  test("уход со страницы сохраняет черновик сразу, без паузы", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const sent = page.waitForResponse((r) => r.request().method() === "PUT" && r.url().includes("/draft"));
    await editor(page).fill("quick = 1\n");
    // не ждём паузы: переходим на теорию — страница практики размонтируется и сбрасывает черновик
    await page.locator(".ch-tab", { hasText: "Теория" }).click();
    expect((await sent).status()).toBe(204);
    await page.goBack();
    await expect(editor(page)).toHaveValue("quick = 1\n");
  });

  test("«Сбросить» возвращает заготовку и сохраняет её как черновик", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await open(page, request);
    const t = pyTasks[0]!;
    await savedDraft(page, () => editor(page).fill("print('чужой код')\n"));
    await savedDraft(page, () => page.getByRole("button", { name: "Сбросить" }).click());
    await expect(editor(page)).toHaveValue(t.starter);
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string> };
    expect(state.drafts[t.id]).toBe(t.starter);
    await page.reload();
    await expect(editor(page)).toHaveValue(t.starter);
  });
});

test.describe("API упражнений", () => {
  test("список задач без тестов и эталонов, статистика по главам, чужие данные закрыты", async ({ page, request }) => {
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
    // состояние, черновик, попытки и запуск — только для вошедшего
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/state`)).status()).toBe(401);
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/draft`, { data: { code: "x" } })).status()).toBe(401);
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`)).status()).toBe(401);
    expect((await request.post("/api/exercises/run", { data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "print(1)" } })).status()).toBe(401);
    expect((await request.get("/api/exercises/run/abc")).status()).toBe(401);
    // воркерский API закрыт токеном
    expect((await request.post("/internal/worker/ping", { data: { name: "x", lanes: ["light"] } })).status()).toBe(401);
    expect((await request.post("/internal/worker/ping", { headers: { Authorization: "Bearer nope" }, data: { name: "x", lanes: ["light"] } })).status()).toBe(401);
    const { token } = await loginFresh(page, request);
    const h = bearer(token);
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/нет-такой/draft`, { headers: h, data: { code: "x" } })).status()).toBe(404);
    expect((await request.get(`/api/exercises/${PY.book}/${PY.num}/нет-такой/attempts`, { headers: h })).status()).toBe(404);
    expect((await request.post("/api/exercises/run", { headers: h, data: { book: PY.book, chapter: PY.num, task: "нет-такой", code: "print(1)" } })).status()).toBe(404);
    expect((await request.get("/api/exercises/run/нет-такого", { headers: h })).status()).toBe(404);
    // упражнение-лаборатория в песочнице не проверяется, решённым его вручную не объявить
    expect((await request.put(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/solved`, { headers: h, data: { solution: "x" } })).status()).toBe(404);
  });
});

// ==================================================================================================
// Проверка без воркера: очередь недоступна. Идёт первой — позже подставные воркеры оставляют сервер «живым» на 30 секунд.
// ==================================================================================================

test.describe("проверка без воркера", () => {
  test("статус проверки: воркеров нет, очередь пуста", async ({ request }) => {
    await waitNoWorkers(request);
    const status = await (await request.get("/api/exercises/runner/status")).json();
    expect(status).toEqual({ queued: 0, running: 0, workers: 0, available: false });
  });

  test("Ctrl+Enter и кнопка: сообщение о недоступности, статус и история не меняются, код остаётся", async ({ page, request }) => {
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
    // ничего не засчитано и не записано
    await expect(badge(page)).toHaveText("не решено");
    await expect(items(page).first().locator(".pr-mark")).toHaveText("1");
    await expect(page.locator(".pr-hist")).toHaveCount(0);
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(mainBtn(page)).toBeEnabled();
    await expect(editor(page)).toHaveValue(code);
    // кнопка делает то же самое
    await mainBtn(page).click();
    await expect.poll(() => posts.length).toBe(2);
    await expect(unavailable).toContainText("временно недоступна");
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: unknown[] };
    expect(attempts.attempts).toEqual([]);
    guard.assertClean();
  });

  test("окно о перегрузке: ссылка на репозиторий и инструкцию, закрытие, не навязывается повторно", async ({ page, request }) => {
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
    await expect(notice.getByRole("link", { name: "Как запустить у себя" })).toHaveAttribute("href", /github\.com\/rysev-a\/dev-learn#/);
    await expect(notice.getByRole("link", { name: "Репозиторий" })).toHaveAttribute("href", "https://github.com/rysev-a/dev-learn");
    // закрыли — следующий отказ в ближайшую минуту окно не возвращает, сообщение в результатах остаётся
    await notice.getByRole("button", { name: "Закрыть" }).click();
    await expect(notice).toHaveCount(0);
    await mainBtn(page).click();
    await expect(result(page).locator(".cx-error")).toContainText("временно недоступна");
    await expect(notice).toHaveCount(0);
    guard.assertClean();
  });

  test("пустой код не уходит в очередь: сервер отвечает сообщением", async ({ page, request }) => {
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

  test("слишком длинное решение отклоняется", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "x".repeat(20_001) } });
    expect(res.status()).toBe(422);
  });
});

// ==================================================================================================
// Виджет «База данных» у SQL-задач
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
  expect(key, "у SQL-задачи есть набор данных").toBeTruthy();
  return body.datasets[key!]!;
}

test.describe("SQL: виджет «База данных»", () => {
  const tableBox = (page: Page, name: string) => page.locator(".sx-tbl", { has: page.locator(".sx-name", { hasText: new RegExp(`^${name}$`) }) });
  const transform = (loc: Locator) => loc.getAttribute("transform");

  test("ERD: таблицы со столбцами и связями, подпись с числом таблиц", async ({ page, request, guard }) => {
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

  test("вкладка «Данные»: таблица на вкладку, строки и столбцы как на сервере", async ({ page, request }) => {
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
    // NULL показан отдельно от пустой строки (у клиентов есть без e-mail и без города)
    await tabs.first().click();
    await expect(page.locator(".sx-grid .sx-null").first()).toHaveText("NULL");
  });

  test("клик по таблице на диаграмме открывает её данные; перетаскивание сдвигает, но данные не открывает", async ({ page, request }) => {
    await loginFresh(page, request);
    const data = await datasetOf(request);
    await open(page, request, SQL);
    const target = data.tables[1]!;
    const box = tableBox(page, target.name);
    const before = await transform(box);
    // перетаскивание: таблица смещается, вид остаётся ERD
    const rect = (await box.locator(".sx-frame").boundingBox())!;
    const [x, y] = [rect.x + rect.width / 2, rect.y + 12];
    await page.mouse.move(x, y);
    await page.mouse.down();
    await page.mouse.move(x + 40, y + 60, { steps: 6 });
    await page.mouse.up();
    const moved = await transform(box);
    expect(moved).not.toBe(before);
    await expect(page.locator(".sx-seg button.on")).toHaveText("ERD");
    // «расставить заново» возвращает раскладку
    await page.getByRole("button", { name: "расставить заново" }).click();
    expect(await transform(box)).toBe(before);
    // клик без сдвига: вкладка «Данные» этой таблицы
    await box.locator(".sx-frame").click();
    await expect(page.locator(".sx-seg button.on")).toHaveText("Данные");
    await expect(page.locator(".sx-tab.on")).toContainText(target.name);
  });

  test("наведение подсвечивает связанные таблицы", async ({ page, request }) => {
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

  test("свернуть и вид помнятся между перезагрузками", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, SQL);
    await page.locator(".sx-seg button", { hasText: "Данные" }).click();
    await page.reload();
    await expect(page.locator(".sx-seg button.on")).toHaveText("Данные"); // вид запомнен
    await page.locator(".sx-fold").click();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(".sx-data, .sx-erd")).toHaveCount(0);
    await page.reload();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(".sx-data, .sx-erd")).toHaveCount(0);
    // выбор вида при свёрнутом виджете разворачивает его
    await page.locator(".sx-seg button", { hasText: "ERD" }).click();
    await expect(page.locator(".sx-fold")).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator(".sx-erd")).toBeVisible();
  });

  test("виджет есть у каждой SQL-задачи главы и пропадает у задач без базы", async ({ page, request }) => {
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
// Очередь и результаты: подставной воркер
// ==================================================================================================

test.describe("очередь и результаты (подставной воркер)", () => {
  test("«в очереди» → «выполняется» → не пройдено: тест с ожидаемым и полученным, история, статус ✗", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const t = pyTasks[2]!; // intro-parity, func
    await open(page, request, PY, t.id);
    const code = await typeCode(page, "def parity(n):\n    return 'чётное'");
    await mainBtn(page).click();
    // заявка в очереди: кнопка и панель результата сообщают об этом, кнопка недоступна
    await expect(mainBtn(page)).toHaveText("В очереди…");
    await expect(mainBtn(page)).toBeDisabled();
    await expect(result(page)).toContainText("В очереди…");
    const status = await (await request.get("/api/exercises/runner/status")).json();
    expect(status).toMatchObject({ queued: 1, available: true });
    // воркер забрал задание: решение и задача дошли без искажений
    const job = await worker.claim();
    expect(job!.task.id).toBe(t.id);
    expect(job!.code).toBe(code);
    await expect(result(page)).toContainText("Выполняется в песочнице…");
    await expect(mainBtn(page)).toHaveText("Проверяю…");
    await worker.complete(job!, {
      status: "ok",
      results: [
        { ok: true, args: "[4]", expected: "чётное", got: "чётное" },
        { ok: false, args: "[7]", expected: "нечётное", got: "чётное" },
      ],
      stdout: "",
    });
    // результат
    await expect(result(page).locator(".pr-res-sum")).toHaveText("1 из 2");
    await expect(result(page).locator(".pr-res-sum")).toHaveClass(/\bbad\b/);
    await expect(result(page).locator(".pr-test")).toHaveCount(2);
    await expect(result(page).locator(".pr-test.ok")).toContainText("тест 1");
    await expect(result(page).locator(".pr-test.ok")).toContainText("вызов [4]");
    const bad = result(page).locator(".pr-test.bad");
    await expect(bad).toContainText("тест 2");
    await expect(bad).toContainText("вызов [7]");
    await expect(bad.locator(".pr-diff > div").nth(0)).toContainText("нечётное"); // ожидалось
    await expect(bad.locator(".pr-diff > div").nth(0).locator(".s-label")).toHaveText("ожидалось");
    await expect(bad.locator(".pr-diff > div").nth(1).locator(".s-label")).toHaveText("получено");
    await expect(bad.locator(".pr-diff > div").nth(1).locator("pre")).toHaveText("чётное");
    await expect(result(page)).toContainText("программа ничего не вывела");
    // статус «не пройдено», кнопка снова «Проверить»
    await expect(badge(page)).toHaveText("не пройдено");
    await expect(badge(page)).toHaveClass(/\bbad\b/);
    await expect(items(page).nth(2)).toHaveClass(/\bbad\b/);
    await expect(items(page).nth(2).locator(".pr-mark")).toHaveText("✗");
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 0 из ${pyTasks.length}`);
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(mainBtn(page)).toBeEnabled();
    // история: одна неудачная попытка с этим кодом
    await expect(history(page)).toHaveCount(1);
    await expect(history(page).first()).toHaveClass(/\bbad\b/);
    await expect(history(page).first().locator(".pr-hist-n")).toHaveText("#1");
    await expect(history(page).first().locator(".pr-hist-mark")).toHaveText("✗");
    await expect(history(page).first().locator(".pr-hist-score")).toHaveText("1/2");
    await expect(history(page).first().locator(".pr-hist-code")).toHaveText("def parity(n):");
    await expect(history(page).first()).toHaveClass(/\bon\b/);
    await expect(page.locator(".pr-hist .pr-res-time")).toHaveText("1");
    // и на сервере
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { status: Record<string, string> };
    expect(state.status[t.id]).toBe("bad");
    guard.assertClean();
  });

  test("решено: ✓, «выполнено», «Решено 1 из N», «Дальше →»; правка кода возвращает «Проверить»", async ({ page, request, guard }) => {
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
    // принятое решение: вместо «Проверить» — «Дальше →» и «Проверить ещё раз»
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await expect(page.getByRole("button", { name: "Проверить ещё раз" })).toBeVisible();
    await expect(history(page)).toHaveCount(1);
    await expect(history(page).first()).toHaveClass(/\bok\b/);
    await expect(history(page).first().locator(".pr-hist-mark")).toHaveText("✓");
    // правка принятого решения: «Проверить», зелёная рамка уходит; статус «выполнено» остаётся
    await editor(page).press("End");
    await editor(page).pressSequentially(" ");
    await expect(mainBtn(page)).toHaveText("Проверить");
    await expect(page.locator(".rs-editor")).not.toHaveClass(/\bright\b/);
    await expect(badge(page)).toHaveText("выполнено");
    // вернули прежний текст — снова «Дальше →»
    await editor(page).fill(code);
    await expect(mainBtn(page)).toHaveText("Дальше →");
    // сервер: статус, попытка с кодом
    const state = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { status: Record<string, string> };
    expect(state.status[t.id]).toBe("ok");
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${t.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: { code: string; status: string; passed: number; total: number }[] };
    expect(attempts.attempts).toHaveLength(1);
    expect(attempts.attempts[0]).toMatchObject({ code, status: "ok", passed: 1, total: 1 });
    guard.assertClean();
  });

  test("решённое остаётся решённым: после перезагрузки статусы, счётчики, черновик и история на месте; провал решённое не отменяет", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    const t = pyTasks[0]!;
    await open(page, request);
    const good = await typeCode(page, "year = 1991\nprint(year)");
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(badge(page)).toHaveText("выполнено");
    // новая неудачная попытка статус не откатывает
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
    // черновик (последний набранный код) уже на сервере
    await expect
      .poll(async () => ((await (await request.get(`/api/exercises/${PY.book}/${PY.num}/state`, { headers: bearer(token) })).json()) as { drafts: Record<string, string> }).drafts[t.id])
      .toBe(worse);
    // перезагрузка
    await page.reload();
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 1 из ${pyTasks.length}`);
    await expect(items(page).first()).toHaveClass(/\bok\b/);
    await expect(badge(page)).toHaveText("выполнено");
    await expect(editor(page)).toHaveValue(worse); // черновик — последний набранный код
    await expect(history(page)).toHaveCount(2);
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`1/${pyTasks.length}`);
    // клик по принятой попытке возвращает её код в редактор и включает «Дальше →»
    await history(page).nth(1).click();
    await expect(editor(page)).toHaveValue(good);
    await expect(history(page).nth(1)).toHaveClass(/\bon\b/);
    await expect(history(page).nth(0)).not.toHaveClass(/\bon\b/);
    await expect(mainBtn(page)).toHaveText("Дальше →");
    // …а на неудачную — обратно
    await history(page).nth(0).click();
    await expect(editor(page)).toHaveValue(worse);
    await expect(mainBtn(page)).toHaveText("Проверить");
    guard.assertClean();
  });

  test("очередь: место «перед вами N», одна проверка на пользователя, порядок выдачи воркеру", async ({ page, request, browser }) => {
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
    // повторная постановка того же пользователя, пока проверка идёт, отклоняется
    const dup = await request.post("/api/exercises/run", { headers: bearer(tokenA), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code: "print(3)" } });
    expect(dup.status()).toBe(429);
    expect(await dup.text()).toContain("Предыдущая проверка ещё идёт");
    // повторные нажатия не ставят вторую заявку: кнопка заблокирована
    await expect(mainBtn(page)).toBeDisabled();
    await editor(page).press("Control+Enter");
    // второй пользователь — следом за первым
    await mainBtn(pageB).click();
    await expect(result(pageB)).toContainText("В очереди (перед вами 1)…");
    const queued = await (await request.get("/api/exercises/runner/status")).json();
    expect(queued).toMatchObject({ queued: 2, running: 0 });
    // воркер получает заявки по порядку постановки
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
    // у каждого свой результат, статус и история
    await expect(badge(pageB)).toHaveText("не пройдено");
    await expect(badge(page)).toHaveText("выполнено");
    await other.close();
  });

  test("результат из кэша: то же решение другого пользователя принимается сразу, не дожидаясь воркера", async ({ page, request, browser }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    const code = await typeCode(page, "year = 1991\nprint(year)");
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(badge(page)).toHaveText("выполнено");
    // другой пользователь присылает точно такой код: ответ готов сразу, воркер не нужен
    const other = await browser.newContext();
    const { token } = await loginFresh(await other.newPage(), other.request);
    const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: PY.book, chapter: PY.num, task: pyTasks[0]!.id, code } });
    expect(res.status()).toBe(202);
    expect(await res.json()).toMatchObject({ state: "done", solved: true, passed: 1, total: 1 });
    expect(await (await request.get("/api/exercises/runner/status")).json()).toMatchObject({ queued: 0, running: 0 });
    await other.close();
    // тот же код с другой задачей кэш не берёт: ключ — задача и код
    const { token: t2 } = await loginFresh(page, request);
    const other2 = await request.post("/api/exercises/run", { headers: bearer(t2), data: { book: PY.book, chapter: PY.num, task: pyTasks[1]!.id, code } });
    expect(other2.status()).toBe(202);
    expect(await other2.json()).toMatchObject({ state: "queued" });
    const job = await worker.claim();
    await worker.complete(job!, failing("int\n", "1991\n")); // освобождаем очередь
  });

  test("результаты разных видов: ошибка выполнения, лимит времени, вывод программы", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request, PY, "intro-loop");
    // ошибка до запуска тестов: traceback в логах, тестов нет
    await typeCode(page, "for i in range(3)\n    print(i)");
    await mainBtn(page).click();
    await serve(worker, { status: "error", results: [], stdout: "", stderr: "SyntaxError: expected ':'" });
    await expect(result(page)).toContainText("Тесты не запускались");
    await expect(result(page).locator(".cx-error")).toHaveText("SyntaxError: expected ':'");
    await expect(result(page).locator(".pr-res-sum")).toHaveCount(0);
    await expect(badge(page)).toHaveText("не пройдено");
    // лимит времени
    await typeCode(page, "while True:\n    pass");
    await mainBtn(page).click();
    await serve(worker, { status: "timeout", results: [], stdout: "", stderr: "" });
    await expect(result(page)).toContainText("Проверка не уложилась в лимит времени");
    await expect(result(page)).not.toContainText("Тесты не запускались");
    // вывод программы (режим stdout): виден в логах, расхождение — «ожидалось/получено»
    await typeCode(page, "for i in range(1, 4):\n    print(i)");
    await mainBtn(page).click();
    await serve(worker, { status: "ok", results: [{ ok: false, expected: "1\n2\n3\n4\n5\n", got: "1\n2\n3\n" }], stdout: "1\n2\n3\n" });
    await expect(result(page).locator(".pr-log")).toHaveText("1\n2\n3");
    await expect(result(page).locator(".pr-test.bad .pr-diff pre").first()).toHaveText("1\n2\n3\n4\n5\n");
    await expect(result(page).locator(".pr-test.bad .pr-diff pre").nth(1)).toHaveText("1\n2\n3\n");
    await expect(history(page)).toHaveCount(3);
    guard.assertClean();
  });

  test("SQL: неверный результат показан двумя таблицами с подсветкой различий", async ({ page, request, guard }) => {
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
          got_rows: [[1, "Анна"], [2, "Борис"], [9, "Лишний"]],
          got_total: 3,
          exp_cols: ["id", "name"],
          exp_rows: [[1, "Анна"], [2, "Борис"], [3, "Вера"]],
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
    // совпавшие строки без подсветки, лишняя у ученика и недостающая у эталона отмечены
    await expect(diff.locator(".sd-side.got .sd-ok")).toHaveCount(2);
    await expect(diff.locator(".sd-side.exp .sd-ok")).toHaveCount(2);
    await expect(diff.locator(".sd-side.got tr.sd-diff, .sd-side.got tr.sd-extra")).toHaveCount(1);
    await expect(diff.locator(".sd-side.exp tr.sd-diff, .sd-side.exp tr.sd-missing")).toHaveCount(1);
    await expect(diff.locator(".sd-side.got td.extra").first()).toContainText(/Лишний|9/);
    await expect(diff.locator(".sd-side.exp td.missing").first()).toContainText(/Вера|3/);
    await expect(diff.locator(".sd-legend")).toContainText("лишнее или неверное значение у вас");
    await expect(badge(page)).toHaveText("не пройдено");
    guard.assertClean();
  });

  test("после решения Ctrl+Enter открывает следующее упражнение (и по кнопке «Дальше →»)", async ({ page, request }) => {
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
    // решаем второе и уходим по кнопке
    await typeCode(page, 'print(type(5).__name__)');
    await mainBtn(page).click();
    await serve(worker, passing("int\n"));
    await expect(mainBtn(page)).toHaveText("Дальше →");
    await mainBtn(page).click();
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[2]!.id}$`));
  });
});

// ==================================================================================================
// Настоящая песочница: E2E_WORKER=1, Docker и образ python:3.13-slim
// ==================================================================================================

test.describe("настоящая проверка в песочнице", () => {
  test.describe.configure({ mode: "serial", timeout: 180_000 });
  test.skip(!realWorkerRequested, "E2E_WORKER=1 не задан: настоящая проверка выключена");
  test.skip(realWorkerRequested && !dockerReady(), "Docker недоступен или нет образа python:3.13-slim");

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

  test("Python, режим stdout: верное решение принято, неверное — с ожидаемым и полученным", async ({ page, request, guard }) => {
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

  test("Python, режим func: все тесты верного решения; у ошибочного — провалы с аргументами вызова", async ({ page, request }) => {
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

  test("пустая заготовка не проходит, бесконечный цикл упирается в лимит времени", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, PY, "intro-loop");
    await mainBtn(page).click(); // заготовка — один комментарий
    await verdict(page, "не пройдено");
    await expect(result(page).locator(".pr-test.bad")).toHaveCount(1);
    await editor(page).fill("while True:\n    pass\n");
    await mainBtn(page).click();
    await expect(result(page)).toContainText("Проверка не уложилась в лимит времени", { timeout: 150_000 });
  });

  test("SQL: верный запрос принят, чужая таблица — две таблицы с различиями", async ({ page, request }) => {
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
