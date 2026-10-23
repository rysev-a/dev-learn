import type { APIRequestContext, Locator, Page } from "@playwright/test";
import { bearer, chapters, expect, loginFresh, test } from "../../support/fixtures";
import { FakeWorker, chapterPath, codeTasks, failing, passing, presetSetting, unique, type CodeTask, type WorkerResult } from "../../support/learning";

/* Общая оболочка практики: прогресс «Решено N из M», порядок упражнений, переходы «Дальше →» и автопереход, пункты в полном экране,
   сброс упражнений из настроек. Проверку выполняет подставной воркер; решения сидятся прямо через API. */

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

/** Отправляет решение через API и отвечает за воркера: так упражнению задаётся статус без работы в интерфейсе. */
async function seed(request: APIRequestContext, token: string, worker: FakeWorker, t: CodeTask, answer: WorkerResult, target = PY): Promise<void> {
  await worker.ping();
  const res = await request.post("/api/exercises/run", { headers: bearer(token), data: { book: target.book, chapter: target.num, task: t.id, code: `print(1)\n${unique()}\n` } });
  expect(res.status(), await res.text()).toBe(202);
  const job = await worker.claim();
  expect(job?.task.id).toBe(t.id);
  await worker.complete(job!, answer);
}

/** Ответ воркера на то, что прислали из интерфейса. */
async function serve(worker: FakeWorker, answer: WorkerResult): Promise<void> {
  const job = await worker.claim();
  expect(job, "задание дошло до воркера").not.toBeNull();
  await worker.complete(job!, answer);
}

test.describe("прогресс и порядок", () => {
  test("«Решено N из M», полоса, значок вкладки и отметки следуют статусам с сервера", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await seed(request, token, worker, pyTasks[0]!, passing("1991\n"));
    await seed(request, token, worker, pyTasks[1]!, passing("int\n"));
    await seed(request, token, worker, pyTasks[2]!, failing("чётное", "нечётное"));
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
    // у открытого провального упражнения «не пройдено», у нерешённого — «не решено»
    await items(page).nth(2).click();
    await expect(page.locator(".pr-badge")).toHaveText("не пройдено");
    await items(page).nth(4).click();
    await expect(page.locator(".pr-badge")).toHaveText("не решено");
    guard.assertClean();
  });

  test("упражнения идут в порядке главы (SQL: 41 упражнение), названия и номера совпадают с данными", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, "", SQL);
    await expect(items(page)).toHaveCount(sqlTasks.length);
    expect(await items(page).locator(".pr-name").allTextContents()).toEqual(sqlTasks.map((t) => t.title));
    expect(await items(page).locator(".pr-mark").allTextContents()).toEqual(sqlTasks.map((_, i) => String(i + 1)));
    await expect(label(page)).toHaveText(`Решено 0 из ${sqlTasks.length}`);
    // выбор последнего упражнения
    await items(page).last().click();
    await expect(page.locator(".pr-head h3")).toHaveText(`${sqlTasks.length}. ${sqlTasks[sqlTasks.length - 1]!.title}`);
  });
});

test.describe("подписи оболочки", () => {
  // Правая подпись полосы прогресса жёстко «python · docker» — и у SQL-глав (режим sql, песочница с SQLite), и у Rust/C/JS.
  test("подпись справа от полосы не называет Python у SQL-упражнений", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, "", SQL);
    await expect(page.locator(".pr-top-label").last()).not.toContainText("python");
  });
});

test.describe("«Дальше →» и автопереход", () => {
  test("автопереход выключен по умолчанию: после решения остаёмся на упражнении", async ({ page, request }) => {
    await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await editor(page).fill(`year = 1991\nprint(year)\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    const url = page.url();
    await page.waitForTimeout(2000); // автопереход, если бы он был, сработал бы через секунду
    expect(page.url()).toBe(url);
    await expect(mainBtn(page)).toHaveText("Дальше →");
  });

  test("автопереход включён: через секунду открывается следующее упражнение", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    await presetSetting(page, "say-auto-next", "1");
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

  test("автопереход не уводит, если ученик уже выбрал другое упражнение", async ({ page, request }) => {
    await loginFresh(page, request);
    await presetSetting(page, "say-auto-next", "1");
    const worker = new FakeWorker(request);
    await worker.ping();
    await open(page, request);
    await editor(page).fill(`year = 1991\nprint(year)\n${unique()}\n`);
    await mainBtn(page).click();
    await serve(worker, passing("1991\n"));
    await expect(page.locator(".pr-badge")).toHaveText("выполнено");
    await items(page).nth(4).click(); // не дожидаясь секунды
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[4]!.id}$`));
    await page.waitForTimeout(2000);
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[4]!.id}$`));
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[4]!.title);
  });

  test("настройка «Автопереход» переключается и пишется в localStorage", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.goto("/settings");
    const toggle = page.getByRole("switch", { name: "Автопереход к следующему упражнению" });
    await expect(toggle).toHaveAttribute("aria-checked", "false");
    const stored = () => page.evaluate(() => window.localStorage.getItem("say-auto-next"));
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

  // Настройки обещают: «после последнего — первое упражнение следующей главы» (так же в AGENTS.md). В Leptos-фронте
  // `go_next` на последнем упражнении ничего не делает, а кнопка «Дальше →» там вовсе не появляется (`go_mode` требует idx + 1 < total).
  test("после решения последнего упражнения «Дальше →» ведёт к первому упражнению следующей главы с задачами", async ({ page, request }) => {
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

test.describe("полный экран", () => {
  test("в дереве слева — упражнения со статусами; выбор сохраняет ?fs=1; проверка работает и обновляет значок", async ({ page, request, guard }) => {
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
    await expect(tree.nth(0)).toHaveClass(/\bon\b/); // текущее упражнение отмечено
    // выбор в дереве: адрес сохраняет fs=1 и добавляет task
    await tree.nth(2).click();
    await expect(page).toHaveURL(new RegExp(`task=${pyTasks[2]!.id}`));
    await expect(page).toHaveURL(/fs=1/);
    await expect(page.locator(".slide-fs")).toBeVisible();
    await expect(page.locator(".pr-head h3")).toHaveText(`3. ${pyTasks[2]!.title}`);
    await expect(tree.nth(2)).toHaveClass(/\bon\b/);
    await expect(tree.nth(0)).not.toHaveClass(/\bon\b/);
    // проверка прямо в полном экране: значок пункта меняется на ✓
    await page.getByRole("button", { name: "Сбросить" }).click(); // подготовка: заготовка → своё решение
    await editor(page).fill(`def parity(n):\n    return 'x'\n${unique()}\n`);
    await editor(page).press("Control+Enter");
    await serve(worker, passing(""));
    await expect(tree.nth(2)).toHaveClass(/\bok\b/);
    await expect(tree.nth(2).locator(".fst-slide-num")).toHaveText("✓");
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 2 из ${pyTasks.length}`);
    // «Свернуть» возвращает обычный вид, выбранное упражнение остаётся
    await page.locator(".slide-fs .slide-btn", { hasText: "Свернуть" }).click();
    await expect(page.locator(".slide-fs")).toHaveCount(0);
    await expect(page.locator(".pr-head h3")).toHaveText(`3. ${pyTasks[2]!.title}`);
    guard.assertClean();
  });
});

test.describe("сброс упражнений в настройках", () => {
  test("«Сбросить прогресс упражнений» стирает статусы, черновики и историю; отказ в подтверждении ничего не трогает", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const worker = new FakeWorker(request);
    await seed(request, token, worker, pyTasks[0]!, passing("1991\n"));
    await seed(request, token, worker, pyTasks[1]!, failing("int\n", "str\n"));
    const stateUrl = `/api/exercises/${PY.book}/${PY.num}/state`;
    const state = async () => (await (await request.get(stateUrl, { headers: bearer(token) })).json()) as { status: Record<string, string>; drafts: Record<string, string> };
    expect(Object.keys((await state()).status)).toHaveLength(2);

    await page.goto("/settings");
    const row = page.locator(".set-row", { hasText: "Сбросить прогресс упражнений" });
    // отказ
    page.once("dialog", (d) => void d.dismiss());
    await row.getByRole("button", { name: "Сбросить", exact: true }).click();
    expect(Object.keys((await state()).status)).toHaveLength(2);
    // согласие
    page.once("dialog", (d) => void d.accept());
    await row.getByRole("button", { name: "Сбросить", exact: true }).click();
    await expect.poll(async () => Object.keys((await state()).status).length).toBe(0);
    expect((await state()).drafts).toEqual({});
    const attempts = (await (await request.get(`/api/exercises/${PY.book}/${PY.num}/${pyTasks[0]!.id}/attempts`, { headers: bearer(token) })).json()) as { attempts: unknown[] };
    expect(attempts.attempts).toEqual([]);
    // практика снова чистая
    await open(page, request);
    await expect(label(page)).toHaveText(`Решено 0 из ${pyTasks.length}`);
    await expect(page.locator(".pr-item.ok, .pr-item.bad")).toHaveCount(0);
    await expect(page.locator(".pr-hist")).toHaveCount(0);
    await expect(page.locator(".ch-tab", { hasText: "Практика" }).locator(".ch-tab-badge")).toHaveText(`0/${pyTasks.length}`);
  });
});

test.describe("вкладки главы", () => {
  // Ссылка «Теория» ведёт на адрес главы без подпути и по префиксу считается «текущей»: у неё всегда aria-current="page", даже когда
  // открыта вкладка «Вопросы» или «Практика» (читалка экрана объявляет две текущие страницы).
  test("aria-current=page только у открытой вкладки", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request);
    const current = page.locator(".ch-tabs a[aria-current='page']");
    await expect(current).toHaveCount(1);
    await expect(current).toContainText("Практика");
  });

  test("переключение вкладок сохраняет выбранное упражнение в адресе вкладки практики", async ({ page, request }) => {
    await loginFresh(page, request);
    await open(page, request, `?task=${pyTasks[3]!.id}`);
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[3]!.title);
    await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
    await expect(page.locator(".quiz")).toBeVisible();
    await page.locator(".ch-tab", { hasText: "Практика" }).click();
    await expect(page.locator(".pr-main")).toBeVisible();
    // вкладка открывается с первого упражнения (выбор живёт в адресе), черновик при этом не теряется
    await expect(page.locator(".pr-head h3")).toContainText(pyTasks[0]!.title);
  });
});
