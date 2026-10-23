import type { Locator, Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import {
  chapterState,
  clone,
  expectStatusOk,
  labChapters,
  labTask,
  labTasks,
  listItem,
  openTask,
  progressLabel,
  putDraft,
  putSolved,
  reference,
  statusOf,
  type LabTaskData,
} from "../../support/labs";

/* Лаборатория «Системный дизайн» (книга 18): схема сервиса на поле, расчёт в wasm и перепроверка решения сервером. */

// поле схемы небольшое по высоте: страница должна вместить его целиком, чтобы мышь попадала в порты
test.use({ viewport: { width: 1500, height: 1600 } });

interface SdNode {
  id: string;
  kind: string;
  name: string;
  params: Record<string, unknown>;
}
interface SdState {
  nodes: SdNode[];
  edges: { from: string; to: string }[];
}
const startOf = (t: LabTaskData) => t.spec.start as SdState;
const solutionOf = (t: LabTaskData) => reference(t) as SdState;

// --- помощники интерфейса -------------------------------------------------------------------------

const goalsList = (page: Page) => page.locator(".sd-goals li");
const nodes = (page: Page) => page.locator(".sd-node:not(.ghost)");
const kindNode = (page: Page, kind: string) => page.locator(`.sd-node.${kind}:not(.ghost)`);
const edges = (page: Page) => page.locator(".sd-board .sd-edge");
const zoomPct = (page: Page) => page.locator(".sd-viewport .lab-zoom .pct");
const metric = (page: Page, name: string) => page.locator(".sd-metrics dl > div", { has: page.locator("dt", { hasText: name }) }).locator("dd");

async function box(l: Locator) {
  await l.scrollIntoViewIfNeeded();
  const b = await l.boundingBox();
  if (!b) throw new Error("у элемента нет рамки");
  return b;
}

/** Порт компонента: вход — у левого края рамки, выход — у правого, по середине высоты. */
async function port(node: Locator, side: "in" | "out") {
  const b = await box(node.locator("rect").first());
  return { x: side === "out" ? b.x + b.width : b.x, y: b.y + b.height / 2 };
}

async function center(l: Locator) {
  const b = await box(l);
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
}

/** Одиночное нажатие мышью (без сдвига). */
async function clickAt(page: Page, p: { x: number; y: number }) {
  await page.mouse.move(p.x, p.y);
  await page.mouse.down();
  await page.mouse.up();
}

/** Протяжка мышью из одной точки в другую. */
async function dragTo(page: Page, from: { x: number; y: number }, to: { x: number; y: number }) {
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move((from.x + to.x) / 2, (from.y + to.y) / 2, { steps: 4 });
  await page.mouse.move(to.x, to.y, { steps: 6 });
  await page.mouse.up();
}

/** Поле карточки параметров по подписи. */
const field = (page: Page, label: string) => page.locator(".sd-float .sd-field", { has: page.locator("span", { hasText: new RegExp(`^${label.replace(/[()]/g, "\\$&")}$`) }) });

/** Все цели выполнены: ни одной ✗, итоговая плашка на месте. */
async function expectAllGoalsDone(page: Page, total: number) {
  await expect(goalsList(page)).toHaveCount(total);
  await expect(page.locator(".sd-goals li.bad")).toHaveCount(0);
  await expect(page.locator(".sd-goals li.ok")).toHaveCount(total);
  await expect(page.locator(".sd-goals .lab-alert.ok .lab-alert-title")).toHaveText("Все цели выполнены");
}

// --- 1. эталон из данных → черновик → интерфейс → сервер ----------------------------------------------

/** Упражнения для проверки конвейера: по одному из разных глав, включая итоговые проекты и экзамены. */
const PIPELINE: [number, string][] = [
  [1, "sd01-fleet"],
  [2, "sd02-horizontal"],
  [3, "sd03-cache"],
  [4, "sd04-failover"],
  [5, "sd05-final"],
  [8, "sd08-spot"],
  [11, "sd11-ws-gateway"],
  [14, "sd14-slo-three"],
  [16, "sd16-bluegreen"],
  [18, "sd18-exam"],
  [21, "sd21-exam"],
  [24, "sd24-exam"],
];

test.describe("эталон из файла данных, положенный черновиком, засчитывается", () => {
  for (const [chapter, id] of PIPELINE) {
    test(`глава ${chapter}: ${id}`, async ({ page, request, guard }) => {
      const task = labTask("sd", chapter, id);
      const { token } = await loginFresh(page, request, "sd");
      await putDraft(request, token, "sd", chapter, id, JSON.stringify(reference(task)));

      await openTask(page, request, "sd", chapter, id);
      await expectAllGoalsDone(page, (task.spec.goals as unknown[]).length);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
      await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
      await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
      await expect(progressLabel(page)).toHaveText(`Решено 1 из ${labTasks("sd", chapter).length}`);
      // сервер принял решение самостоятельно: интерфейс отправил его, как только цели сошлись
      await expectStatusOk(request, token, "sd", chapter, id);

      // после перезагрузки решение уже записано: плашка говорит «уже было решено»
      await page.reload();
      await expect(page.locator(".sd-goals .lab-alert-text")).toHaveText("Упражнение уже было решено.");
      guard.assertClean();
    });
  }
});

test("эталон засчитывается и при открытии из другого упражнения главы (список ✓ только у решённого)", async ({ page, request, guard }) => {
  const chapter = 2;
  const list = labTasks("sd", chapter);
  const solved = list[1]!;
  const { token } = await loginFresh(page, request, "sd");
  await putDraft(request, token, "sd", chapter, solved.id, JSON.stringify(reference(solved)));
  await openTask(page, request, "sd", chapter, list[0]!.id);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
  await expect(page.locator(".pr-list .pr-item")).toHaveCount(list.length);
  await expect(page.locator(".pr-list .pr-item.ok")).toHaveCount(0);
  await listItem(page, solved.title).click();
  await expect(page.locator(".pr-head h3")).toContainText(solved.title);
  await expectAllGoalsDone(page, (solved.spec.goals as unknown[]).length);
  await expect(listItem(page, solved.title)).toHaveClass(/\bok\b/);
  await expect(listItem(page, list[0]!.title)).not.toHaveClass(/\bok\b/);
  await expectStatusOk(request, token, "sd", chapter, solved.id);
  guard.assertClean();
});

// --- 2. исходное состояние не засчитывается ----------------------------------------------------------

test.describe("исходная схема не засчитывается", () => {
  // первое упражнение каждой главы: цели не выполнены, решения на сервере нет
  for (const chapter of labChapters("sd")) {
    const task = labTasks("sd", chapter)[0]!;
    test(`глава ${chapter}: ${task.id}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "sd");
      await openTask(page, request, "sd", chapter, task.id);
      await expect(goalsList(page)).toHaveCount((task.spec.goals as unknown[]).length);
      await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
      await expect(page.locator(".sd-goals .lab-alert")).toHaveCount(0);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
      await expect(page.locator(".pr-list .pr-item.ok")).toHaveCount(0);
      await expect(progressLabel(page)).toHaveText(new RegExp(`^Решено 0 из ${labTasks("sd", chapter).length}$`));
      await page.waitForLoadState("networkidle");
      expect(await statusOf(request, token, "sd", chapter, task.id)).toBeUndefined();
      guard.assertClean();
    });
  }
});

test("черновик с неполной схемой не засчитывается; повреждённый черновик открывает исходную схему", async ({ page, request, guard }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  // схема эталона без базы данных: цели не сходятся
  const broken = clone(solutionOf(task));
  broken.nodes = broken.nodes.filter((n) => n.kind !== "db");
  broken.edges = broken.edges.filter((e) => e.to !== "db");
  await putDraft(request, token, "sd", chapter, id, JSON.stringify(broken));
  await openTask(page, request, "sd", chapter, id);
  await expect(kindNode(page, "app")).toHaveCount(1);
  await expect(kindNode(page, "db")).toHaveCount(0);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
  await expect(page.locator(".sd-goals .lab-alert")).toHaveCount(0);

  await putDraft(request, token, "sd", chapter, id, "{не json");
  await page.reload();
  await expect(nodes(page)).toHaveCount(startOf(task).nodes.length);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
  await page.waitForLoadState("networkidle");
  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  guard.assertClean();
});

// --- 3. отказ сервера ------------------------------------------------------------------------------------

test("сервер отклоняет исходную схему и мусор с причиной (422)", async ({ page, request }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");

  const start = await putSolved(request, token, "sd", chapter, id, JSON.stringify(startOf(task)));
  expect(start.status).toBe(422);
  expect(start.detail).toContain("цель не выполнена");
  expect(start.detail).toContain("80%");

  const junk = await putSolved(request, token, "sd", chapter, id, "не json");
  expect(junk.status).toBe(422);
  expect(junk.detail).toContain("неверный JSON");

  // схема, в которой подменён параметр вне справочника, и компонент, которого нет в палитре упражнения
  const forged = clone(solutionOf(task));
  forged.nodes.find((n) => n.kind === "app")!.params.size = "XXL";
  const bad = await putSolved(request, token, "sd", chapter, id, JSON.stringify(forged));
  expect(bad.status).toBe(422);
  expect(bad.detail).not.toBe("");

  const outside = clone(solutionOf(task));
  outside.nodes.push({ id: "cache1", kind: "cache", name: "Кэш", params: {} });
  const out = await putSolved(request, token, "sd", chapter, id, JSON.stringify(outside));
  expect(out.status).toBe(422);

  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  // эталон принимается (204), и повторная отправка тоже
  expect((await putSolved(request, token, "sd", chapter, id, JSON.stringify(reference(task)))).status).toBe(204);
  expect(await statusOf(request, token, "sd", chapter, id)).toBe("ok");
});

test("интерфейс показывает причину отказа сервера, если ему подменили решение", async ({ page, request, guard }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  await putDraft(request, token, "sd", chapter, id, JSON.stringify(reference(task)));
  // решение, которое клиент отправит, подменяется исходной схемой — как будто интерфейс ошибся в расчёте
  await page.route("**/api/exercises/18/2/sd02-vertical/solved", async (route) => {
    await route.continue({ postData: JSON.stringify({ solution: JSON.stringify(startOf(task)) }) });
  });
  const refused = page.waitForResponse((r) => r.url().endsWith("/sd02-vertical/solved") && r.request().method() === "PUT");
  await openTask(page, request, "sd", chapter, id);
  expect((await refused).status()).toBe(422);
  const error = page.locator(".pr-main p.error");
  await expect(error).toContainText("Решение не принято");
  await expect(error).toContainText("цель не выполнена");
  // интерфейс считает цели выполненными, но сервер ничего не записал
  await expect(page.locator(".sd-goals .lab-alert-title")).toHaveText("Все цели выполнены");
  await expect(page.locator(".sd-goals .lab-alert-text")).toHaveText("Проверяю решение на сервере…");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  // консоль охраняет 422: ошибка загрузки ресурса — штатный ответ сервера, а не сбой страницы
  expect(guard.errors.filter((e) => !/422/.test(e))).toEqual([]);
});

// --- 4. реальные действия на поле ---------------------------------------------------------------------

test.describe("действия на поле", () => {
  const OPEN: [number, string] = [2, "sd02-vertical"];

  async function setup(page: Page, request: Parameters<typeof openTask>[1], who = "sd") {
    const user = await loginFresh(page, request, who);
    await openTask(page, request, "sd", OPEN[0], OPEN[1]);
    await expect(nodes(page)).toHaveCount(3);
    return user;
  }

  test("палитра: клик добавляет компонент, карточка показывает его параметры, × закрывает", async ({ page, request, guard }) => {
    const { token } = await setup(page, request);
    await expect(page.locator(".sd-float")).toHaveCount(0);
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(4);
    await expect(page.locator(".sd-node.on")).toHaveClass(/\bdb\b/);
    await expect(page.locator(".sd-float h4")).toHaveText("База данных 2");
    await expect(field(page, "Реплики на шард").locator("input")).toHaveValue("0");
    await page.getByRole("button", { name: "Закрыть" }).click();
    await expect(page.locator(".sd-float")).toHaveCount(0);
    // новая схема сохранена черновиком на сервере
    await expect
      .poll(async () => {
        const raw = (await chapterState(request, token, "sd", OPEN[0])).drafts[OPEN[1]];
        return raw ? (JSON.parse(raw) as SdState).nodes.length : 0;
      })
      .toBe(4);
    guard.assertClean();
  });

  test("перетаскивание из палитры ставит компонент туда, где отпустили кнопку", async ({ page, request, guard }) => {
    await setup(page, request);
    const svg = await box(page.locator(".sd-board"));
    // пустое место поля — нижняя часть
    const drop = { x: svg.x + svg.width * 0.5, y: svg.y + svg.height * 0.85 };
    const from = await center(page.getByRole("button", { name: "+ Сервер приложения" }));
    await page.mouse.move(from.x, from.y);
    await page.mouse.down();
    await page.mouse.move(drop.x, drop.y, { steps: 8 });
    // пока тащим, под курсором виден «призрак» компонента
    await expect(page.locator(".sd-node.ghost")).toHaveCount(1);
    await page.mouse.up();
    await expect(page.locator(".sd-node.ghost")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(4);
    const added = page.locator(".sd-node.on");
    await expect(added).toHaveClass(/\bapp\b/);
    const c = await center(added.locator("rect").first());
    expect(Math.abs(c.x - drop.x)).toBeLessThan(40);
    expect(Math.abs(c.y - drop.y)).toBeLessThan(40);
    // отпустили вне поля — компонент не добавляется
    await page.mouse.move(from.x, from.y);
    await page.mouse.down();
    await page.mouse.move(from.x + 5, svg.y - 120, { steps: 5 });
    await page.mouse.up();
    await expect(nodes(page)).toHaveCount(4);
    guard.assertClean();
  });

  test("связь двумя кликами по портам и протяжкой; недопустимую связь поле отклоняет с причиной", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(edges(page)).toHaveCount(2);
    const app = kindNode(page, "app");

    // двумя кликами: выход сервера → вход новой базы данных
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(4);
    await page.getByRole("button", { name: "Закрыть" }).click();
    const db2 = page.locator(".sd-node.db").nth(1);
    await clickAt(page, await port(app, "out"));
    await clickAt(page, await port(db2, "in"));
    await expect(edges(page)).toHaveCount(3);

    // протяжкой: ещё один компонент, провод от его входа к выходу сервера (от входа к выходу тоже можно)
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(5);
    await page.getByRole("button", { name: "Закрыть" }).click();
    const db3 = page.locator(".sd-node.db").nth(2);
    await dragTo(page, await port(app, "out"), await center(db3.locator("rect").first()));
    await expect(edges(page)).toHaveCount(4);

    // недопустимо: у пользователей нет входа
    await dragTo(page, await port(app, "out"), await center(kindNode(page, "clients").locator("rect").first()));
    await expect(edges(page)).toHaveCount(4);
    await expect(page.locator(".sd-notice")).not.toHaveText("");
    guard.assertClean();
  });

  test("связь и компонент выбираются и удаляются кнопкой «Удалить» и клавишей Delete", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(page.getByRole("button", { name: "Удалить" })).toBeDisabled();
    // связь: выбрана → подсказка под полем → удалена
    await page.locator(".sd-edge .hit").first().dispatchEvent("click");
    await expect(page.locator(".sd-edge.on")).toHaveCount(1);
    await expect(page.locator(".sd-boardcard .sd-hint")).toContainText("выбрана");
    await page.getByRole("button", { name: "Удалить" }).click();
    await expect(edges(page)).toHaveCount(1);

    // компонент: выбран кликом, удаляется вместе со связями; пользователей удалять нельзя
    await clickAt(page, await center(kindNode(page, "clients").locator("rect").first()));
    await expect(page.getByRole("button", { name: "Удалить" })).toBeDisabled();
    await clickAt(page, await center(kindNode(page, "db").locator("rect").first()));
    await expect(page.locator(".sd-float h4")).toHaveText("База данных");
    await page.keyboard.press("Delete");
    await expect(kindNode(page, "db")).toHaveCount(0);
    await expect(edges(page)).toHaveCount(0);
    await expect(page.locator(".sd-float")).toHaveCount(0);
    guard.assertClean();
  });

  test("смена параметра в карточке пересчитывает цели и метрики; отказ и «Отключить» меняют метрики", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(metric(page, "Успешных ответов")).toHaveText("30.0%");
    await clickAt(page, await center(kindNode(page, "app").locator("rect").first()));
    await expect(page.locator(".sd-float h4")).toHaveText("Сервер приложения");
    await expect(page.locator(".sd-float .sd-load")).toContainText("Нагрузка:");
    await field(page, "Размер").locator("select").selectOption("L");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    await expect(kindNode(page, "app").locator(".sd-sub")).toContainText("L");

    // отказ зоны: при размещении «одна зона» схема не переживает его
    const heading = page.locator(".sd-metrics h4");
    await expect(heading).not.toContainText("·");
    await page.locator(".sd-fail select").selectOption("zone");
    await expect(heading).toContainText("отказ зоны доступности");
    await expect(metric(page, "Успешных ответов")).not.toHaveText(/^100(\.0+)?%$/);
    await page.locator(".sd-fail select").selectOption("");
    await expect(heading).not.toContainText("·");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    // отказ вида компонента: список содержит виды, которые есть на схеме
    await expect(page.locator(".sd-fail select option")).toContainText(["отказ региона", "выкладка новой версии", "падает сервер приложения"]);
    await page.locator(".sd-fail select").selectOption("app");
    await expect(heading).toContainText("падает сервер приложения");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^0(\.0+)?%$/);
    await page.locator(".sd-fail select").selectOption("");

    // «Отключить» компонент вручную
    await field(page, "Отключить (проверить отказ)").locator("input").check();
    await expect(page.locator(".sd-node.app")).toHaveClass(/\bdown\b/);
    await expect(kindNode(page, "app").locator(".sd-sub")).toHaveText("отключён");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^0(\.0+)?%$/);
    await field(page, "Отключить (проверить отказ)").locator("input").uncheck();
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    guard.assertClean();
  });

  test("подсказка, справка «?», «во весь экран» и Esc", async ({ page, request, guard }) => {
    await setup(page, request);
    const task = labTask("sd", OPEN[0], OPEN[1]);
    await expect(page.locator(".sd-boardcard > .sd-hint")).toHaveCount(0);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".sd-boardcard > .sd-hint")).toHaveText(task.hint);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".sd-boardcard > .sd-hint")).toHaveCount(0);

    const help = page.getByRole("button", { name: "Справка" });
    await expect(page.locator(".sd-help")).toHaveCount(0);
    await help.click();
    await expect(help).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator(".sd-help")).toContainText("Справочник чисел");
    await expect(page.locator(".sd-help li").first()).toBeVisible();
    await help.click();
    await expect(page.locator(".sd-help")).toHaveCount(0);

    await expect(page.locator(".sd.fs")).toHaveCount(0);
    await page.getByRole("button", { name: "На весь экран", exact: true }).click();
    await expect(page.locator(".sd.fs")).toBeVisible();
    // в полном экране рядом с полем те же цели и метрики, а «лапки» высоты нет
    await expect(page.locator(".sd.fs .sd-goals li").first()).toBeVisible();
    await expect(page.locator(".sd.fs .sd-metrics")).toBeVisible();
    await expect(page.locator(".sd.fs .sd-resize")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(3);
    await page.keyboard.press("Escape");
    await expect(page.locator(".sd.fs")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(3);
    // и кнопкой «Свернуть»
    await page.getByRole("button", { name: "На весь экран", exact: true }).click();
    await expect(page.locator(".sd.fs")).toBeVisible();
    await page.getByRole("button", { name: "Свернуть", exact: true }).click();
    await expect(page.locator(".sd.fs")).toHaveCount(0);
    guard.assertClean();
  });

  test("масштаб: кнопки, Ctrl+колесо, «100%» и «вписать»; сдвиг пустого места", async ({ page, request, guard }) => {
    await setup(page, request);
    const pct = async () => Number((await zoomPct(page).innerText()).replace("%", ""));
    const fit = await pct();
    const vb = () => page.locator(".sd-board").getAttribute("viewBox");
    const zoom = page.locator(".sd-viewport .lab-zoom");
    await expect(zoom.getByRole("button", { name: "⌖" })).toHaveCount(0);

    await zoom.getByRole("button", { name: "+" }).click();
    await expect.poll(pct).toBeGreaterThan(fit);
    await zoom.getByRole("button", { name: "−" }).click();
    await zoom.getByRole("button", { name: "−" }).click();
    await expect.poll(pct).toBeLessThan(fit);
    // Ctrl + колесо над полем
    const before = await pct();
    const c = await center(page.locator(".sd-board"));
    await page.mouse.move(c.x, c.y);
    await page.keyboard.down("Control");
    await page.mouse.wheel(0, -300);
    await page.keyboard.up("Control");
    await expect.poll(pct).toBeGreaterThan(before);
    // 100 %
    await zoomPct(page).click();
    await expect(zoomPct(page)).toHaveText("100%");
    // «вписать»: появилась после смены вида, возвращает схему в окно (масштаб как при открытии)
    await zoom.getByRole("button", { name: "⌖" }).click();
    await expect(zoomPct(page)).toHaveText(`${fit}%`);
    await expect(zoom.getByRole("button", { name: "⌖" })).toHaveCount(0);

    // сдвиг: тянем пустое место поля
    const v0 = await vb();
    const box0 = await box(page.locator(".sd-board"));
    await dragTo(page, { x: box0.x + 60, y: box0.y + 40 }, { x: box0.x + 160, y: box0.y + 90 });
    expect(await vb()).not.toBe(v0);
    await expect(zoom.getByRole("button", { name: "⌖" })).toBeVisible();
    guard.assertClean();
  });

  test("«лапка» меняет высоту поля, двойной клик возвращает; высота запоминается", async ({ page, request, guard }) => {
    await setup(page, request);
    const viewport = page.locator(".sd-viewport");
    const h0 = (await box(viewport)).height;
    const grip = await center(page.locator(".sd-resize"));
    await dragTo(page, grip, { x: grip.x, y: grip.y + 120 });
    await expect(viewport).toHaveClass(/\bsized\b/);
    await expect.poll(async () => (await box(viewport)).height).toBeGreaterThan(h0 + 80);
    expect(await page.evaluate(() => window.localStorage.getItem("say-sd-board-h"))).not.toBeNull();
    // выбранная высота переживает перезагрузку
    await page.reload();
    await expect(viewport).toHaveClass(/\bsized\b/);
    await page.locator(".sd-resize").dblclick();
    await expect(viewport).not.toHaveClass(/\bsized\b/);
    await expect.poll(async () => Math.abs((await box(viewport)).height - h0)).toBeLessThan(2);
    expect(await page.evaluate(() => window.localStorage.getItem("say-sd-board-h"))).toBeNull();
    guard.assertClean();
  });

  test("«Сбросить» возвращает исходную схему и цели, черновик на сервере тоже", async ({ page, request, guard }) => {
    const { token } = await setup(page, request);
    const task = labTask("sd", OPEN[0], OPEN[1]);
    await page.getByRole("button", { name: "+ Сервер приложения" }).click();
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(5);
    await clickAt(page, await center(kindNode(page, "app").first().locator("rect").first()));
    await field(page, "Размер").locator("select").selectOption("L");
    await expect(page.locator(".sd-goals li.bad")).toHaveCount(0);

    await page.getByRole("button", { name: "Сбросить" }).click();
    await expect(nodes(page)).toHaveCount(startOf(task).nodes.length);
    await expect(page.locator(".sd-float")).toHaveCount(0);
    await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
    await expect
      .poll(async () => {
        const raw = (await chapterState(request, token, "sd", OPEN[0])).drafts[OPEN[1]];
        return raw ? (JSON.parse(raw) as SdState).nodes.length : -1;
      })
      .toBe(startOf(task).nodes.length);
    guard.assertClean();
  });

  test("предел числа компонентов: лишний не добавляется, поле объясняет почему", async ({ page, request, guard }) => {
    await setup(page, request);
    const add = page.getByRole("button", { name: "+ Сервер приложения" });
    for (let i = 0; i < 40 && (await page.locator(".sd-notice").count()) === 0; i++) await add.click();
    await expect(page.locator(".sd-notice")).toContainText("На схеме не больше");
    const n = await nodes(page).count();
    await add.click();
    await expect(nodes(page)).toHaveCount(n);
    guard.assertClean();
  });
});

// --- 5. решение руками -----------------------------------------------------------------------------------

test("sd02-vertical решается руками: размер сервера L — цели ✓, сервер принимает", async ({ page, request, guard }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  await openTask(page, request, "sd", chapter, id);
  await expect(page.locator(".sd-goals li.bad")).toHaveCount(2);
  await expect(page.locator(".sd-goals li.ok")).toHaveCount(2);
  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();

  await clickAt(page, await center(kindNode(page, "app").locator("rect").first()));
  await field(page, "Размер").locator("select").selectOption("L");
  await expectAllGoalsDone(page, (task.spec.goals as unknown[]).length);
  await expect(page.locator(".sd-goals .lab-alert-text")).toHaveText("Упражнение засчитано.");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expect(page.getByRole("button", { name: "Дальше" })).toBeVisible();
  await expectStatusOk(request, token, "sd", chapter, id);
  // сохранённое решение — схема с сервером L
  const saved = JSON.parse((await chapterState(request, token, "sd", chapter)).drafts[id]!) as SdState;
  expect(saved.nodes.find((n) => n.kind === "app")?.params.size).toBe("L");

  // «Дальше» ведёт к следующему упражнению главы
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(labTasks("sd", chapter)[1]!.title);
  guard.assertClean();
});

test("sd01-wire решается руками: две связи — одна протяжкой, другая двумя кликами по портам", async ({ page, request, guard }) => {
  const [chapter, id] = [1, "sd01-wire"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  await openTask(page, request, "sd", chapter, id);
  await expect(nodes(page)).toHaveCount(3);
  await expect(edges(page)).toHaveCount(0);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();

  const [users, app, db] = [kindNode(page, "clients"), kindNode(page, "app"), kindNode(page, "db")];
  await dragTo(page, await port(users, "out"), await port(app, "in"));
  await expect(edges(page)).toHaveCount(1);
  await clickAt(page, await port(app, "out"));
  await clickAt(page, await port(db, "in"));
  await expect(edges(page)).toHaveCount(2);

  await expectAllGoalsDone(page, (task.spec.goals as unknown[]).length);
  await expectStatusOk(request, token, "sd", chapter, id);
  const saved = JSON.parse((await chapterState(request, token, "sd", chapter)).drafts[id]!) as SdState;
  expect(saved.edges).toEqual(expect.arrayContaining([{ from: "users", to: "app" }, { from: "app", to: "db" }]));
  guard.assertClean();
});
