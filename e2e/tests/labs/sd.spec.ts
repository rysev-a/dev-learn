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

/* System Design lab (book 18): a service diagram on the field, wasm computation and server re-verification of the solution. */

// the diagram field is small in height: the page must fit it entirely so the mouse hits the ports
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

// --- UI helpers -------------------------------------------------------------------------

const goalsList = (page: Page) => page.locator(".sd-goals li");
const nodes = (page: Page) => page.locator(".sd-node:not(.ghost)");
const kindNode = (page: Page, kind: string) => page.locator(`.sd-node.${kind}:not(.ghost)`);
const edges = (page: Page) => page.locator(".sd-board .sd-edge");
const zoomPct = (page: Page) => page.locator(".sd-viewport .lab-zoom .pct");
const metric = (page: Page, name: string) => page.locator(".sd-metrics dl > div", { has: page.locator("dt", { hasText: name }) }).locator("dd");

async function box(l: Locator) {
  await l.scrollIntoViewIfNeeded();
  const b = await l.boundingBox();
  if (!b) throw new Error("the element has no bounding box");
  return b;
}

/** A component port: the input at the left edge of the frame, the output at the right one, at mid height. */
async function port(node: Locator, side: "in" | "out") {
  const b = await box(node.locator("rect").first());
  return { x: side === "out" ? b.x + b.width : b.x, y: b.y + b.height / 2 };
}

async function center(l: Locator) {
  const b = await box(l);
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
}

/** A single mouse press (without movement). */
async function clickAt(page: Page, p: { x: number; y: number }) {
  await page.mouse.move(p.x, p.y);
  await page.mouse.down();
  await page.mouse.up();
}

/** Mouse drag from one point to another. */
async function dragTo(page: Page, from: { x: number; y: number }, to: { x: number; y: number }) {
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move((from.x + to.x) / 2, (from.y + to.y) / 2, { steps: 4 });
  await page.mouse.move(to.x, to.y, { steps: 6 });
  await page.mouse.up();
}

/** A parameter card field by its label. */
const field = (page: Page, label: string) => page.locator(".sd-float .sd-field", { has: page.locator("span", { hasText: new RegExp(`^${label.replace(/[()]/g, "\\$&")}$`) }) });

/** All goals are met: no ✗, the summary banner is in place. */
async function expectAllGoalsDone(page: Page, total: number) {
  await expect(goalsList(page)).toHaveCount(total);
  await expect(page.locator(".sd-goals li.bad")).toHaveCount(0);
  await expect(page.locator(".sd-goals li.ok")).toHaveCount(total);
  await expect(page.locator(".sd-goals .lab-alert.ok .lab-alert-title")).toHaveText("Все цели выполнены");
}

// --- 1. reference from the data → draft → UI → server ----------------------------------------------

/** Exercises for checking the pipeline: one from different chapters, including final projects and exams. */
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

test.describe("a reference from the data file, put in as a draft, is accepted", () => {
  for (const [chapter, id] of PIPELINE) {
    test(`chapter ${chapter}: ${id}`, async ({ page, request, guard }) => {
      const task = labTask("sd", chapter, id);
      const { token } = await loginFresh(page, request, "sd");
      await putDraft(request, token, "sd", chapter, id, JSON.stringify(reference(task)));

      await openTask(page, request, "sd", chapter, id);
      await expectAllGoalsDone(page, (task.spec.goals as unknown[]).length);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
      await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
      await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
      await expect(progressLabel(page)).toHaveText(`Решено 1 из ${labTasks("sd", chapter).length}`);
      // the server accepted the solution on its own: the UI sent it as soon as the goals were met
      await expectStatusOk(request, token, "sd", chapter, id);

      // after a reload the solution is already recorded: the banner says it was already solved
      await page.reload();
      await expect(page.locator(".sd-goals .lab-alert-text")).toHaveText("Упражнение уже было решено.");
      guard.assertClean();
    });
  }
});

test("the reference is accepted when opened from another chapter exercise (the ✓ list only for the solved one)", async ({ page, request, guard }) => {
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

// --- 2. the initial state is not accepted ----------------------------------------------------------

test.describe("the initial diagram is not accepted", () => {
  // the first exercise of every chapter: goals not met, no solution on the server
  for (const chapter of labChapters("sd")) {
    const task = labTasks("sd", chapter)[0]!;
    test(`chapter ${chapter}: ${task.id}`, async ({ page, request, guard }) => {
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

test("a draft with an incomplete diagram is not accepted; a corrupted draft opens the initial diagram", async ({ page, request, guard }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  // the reference diagram without a database: the goals do not match
  const broken = clone(solutionOf(task));
  broken.nodes = broken.nodes.filter((n) => n.kind !== "db");
  broken.edges = broken.edges.filter((e) => e.to !== "db");
  await putDraft(request, token, "sd", chapter, id, JSON.stringify(broken));
  await openTask(page, request, "sd", chapter, id);
  await expect(kindNode(page, "app")).toHaveCount(1);
  await expect(kindNode(page, "db")).toHaveCount(0);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
  await expect(page.locator(".sd-goals .lab-alert")).toHaveCount(0);

  await putDraft(request, token, "sd", chapter, id, "{not json");
  await page.reload();
  await expect(nodes(page)).toHaveCount(startOf(task).nodes.length);
  await expect(page.locator(".sd-goals li.bad").first()).toBeVisible();
  await page.waitForLoadState("networkidle");
  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  guard.assertClean();
});

// --- 3. server rejection ------------------------------------------------------------------------------------

test("the server rejects the initial diagram and garbage with a reason (422)", async ({ page, request }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");

  const start = await putSolved(request, token, "sd", chapter, id, JSON.stringify(startOf(task)));
  expect(start.status).toBe(422);
  expect(start.detail).toContain("цель не выполнена");
  expect(start.detail).toContain("80%");

  const junk = await putSolved(request, token, "sd", chapter, id, "not json");
  expect(junk.status).toBe(422);
  expect(junk.detail).toContain("неверный JSON");

  // a diagram with a parameter outside the reference substituted, and a component absent from the exercise palette
  const forged = clone(solutionOf(task));
  forged.nodes.find((n) => n.kind === "app")!.params.size = "XXL";
  const bad = await putSolved(request, token, "sd", chapter, id, JSON.stringify(forged));
  expect(bad.status).toBe(422);
  expect(bad.detail).not.toBe("");

  const outside = clone(solutionOf(task));
  outside.nodes.push({ id: "cache1", kind: "cache", name: "Cache", params: {} });
  const out = await putSolved(request, token, "sd", chapter, id, JSON.stringify(outside));
  expect(out.status).toBe(422);

  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  // the reference is accepted (204), and so is a repeated submission
  expect((await putSolved(request, token, "sd", chapter, id, JSON.stringify(reference(task)))).status).toBe(204);
  expect(await statusOf(request, token, "sd", chapter, id)).toBe("ok");
});

test("the UI shows the server rejection reason when the solution was tampered with", async ({ page, request, guard }) => {
  const [chapter, id] = [2, "sd02-vertical"];
  const task = labTask("sd", chapter, id);
  const { token } = await loginFresh(page, request, "sd");
  await putDraft(request, token, "sd", chapter, id, JSON.stringify(reference(task)));
  // the solution the client will send is replaced by the initial diagram — as if the UI made a computation mistake
  await page.route("**/api/exercises/18/2/sd02-vertical/solved", async (route) => {
    await route.continue({ postData: JSON.stringify({ solution: JSON.stringify(startOf(task)) }) });
  });
  const refused = page.waitForResponse((r) => r.url().endsWith("/sd02-vertical/solved") && r.request().method() === "PUT");
  await openTask(page, request, "sd", chapter, id);
  expect((await refused).status()).toBe(422);
  const error = page.locator(".pr-main p.error");
  await expect(error).toContainText("Решение не принято");
  await expect(error).toContainText("цель не выполнена");
  // the UI considers the goals met, but the server recorded nothing
  await expect(page.locator(".sd-goals .lab-alert-title")).toHaveText("Все цели выполнены");
  await expect(page.locator(".sd-goals .lab-alert-text")).toHaveText("Проверяю решение на сервере…");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
  expect(await statusOf(request, token, "sd", chapter, id)).toBeUndefined();
  // the console guard lets 422 through: a resource load error is a normal server response, not a page failure
  expect(guard.errors.filter((e) => !/422/.test(e))).toEqual([]);
});

// --- 4. real actions on the field ---------------------------------------------------------------------

test.describe("actions on the field", () => {
  const OPEN: [number, string] = [2, "sd02-vertical"];

  async function setup(page: Page, request: Parameters<typeof openTask>[1], who = "sd") {
    const user = await loginFresh(page, request, who);
    await openTask(page, request, "sd", OPEN[0], OPEN[1]);
    await expect(nodes(page)).toHaveCount(3);
    return user;
  }

  test("palette: a click adds a component, the card shows its parameters, × closes it", async ({ page, request, guard }) => {
    const { token } = await setup(page, request);
    await expect(page.locator(".sd-float")).toHaveCount(0);
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(4);
    await expect(page.locator(".sd-node.on")).toHaveClass(/\bdb\b/);
    await expect(page.locator(".sd-float h4")).toHaveText("База данных 2");
    await expect(field(page, "Реплики на шард").locator("input")).toHaveValue("0");
    await page.getByRole("button", { name: "Закрыть" }).click();
    await expect(page.locator(".sd-float")).toHaveCount(0);
    // the new diagram is saved as a draft on the server
    await expect
      .poll(async () => {
        const raw = (await chapterState(request, token, "sd", OPEN[0])).drafts[OPEN[1]];
        return raw ? (JSON.parse(raw) as SdState).nodes.length : 0;
      })
      .toBe(4);
    guard.assertClean();
  });

  test("dragging from the palette puts the component where the button was released", async ({ page, request, guard }) => {
    await setup(page, request);
    const svg = await box(page.locator(".sd-board"));
    // an empty place of the field — the lower part
    const drop = { x: svg.x + svg.width * 0.5, y: svg.y + svg.height * 0.85 };
    const from = await center(page.getByRole("button", { name: "+ Сервер приложения" }));
    await page.mouse.move(from.x, from.y);
    await page.mouse.down();
    await page.mouse.move(drop.x, drop.y, { steps: 8 });
    // while dragging, a ghost of the component is visible under the cursor
    await expect(page.locator(".sd-node.ghost")).toHaveCount(1);
    await page.mouse.up();
    await expect(page.locator(".sd-node.ghost")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(4);
    const added = page.locator(".sd-node.on");
    await expect(added).toHaveClass(/\bapp\b/);
    const c = await center(added.locator("rect").first());
    expect(Math.abs(c.x - drop.x)).toBeLessThan(40);
    expect(Math.abs(c.y - drop.y)).toBeLessThan(40);
    // released outside the field — the component is not added
    await page.mouse.move(from.x, from.y);
    await page.mouse.down();
    await page.mouse.move(from.x + 5, svg.y - 120, { steps: 5 });
    await page.mouse.up();
    await expect(nodes(page)).toHaveCount(4);
    guard.assertClean();
  });

  test("a link by two clicks on ports and by dragging; the field rejects an invalid link with a reason", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(edges(page)).toHaveCount(2);
    const app = kindNode(page, "app");

    // by two clicks: the server output → the new database input
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(4);
    await page.getByRole("button", { name: "Закрыть" }).click();
    const db2 = page.locator(".sd-node.db").nth(1);
    await clickAt(page, await port(app, "out"));
    await clickAt(page, await port(db2, "in"));
    await expect(edges(page)).toHaveCount(3);

    // by dragging: one more component, a wire from its input to the server output (input to output also works)
    await page.getByRole("button", { name: "+ База данных" }).click();
    await expect(nodes(page)).toHaveCount(5);
    await page.getByRole("button", { name: "Закрыть" }).click();
    const db3 = page.locator(".sd-node.db").nth(2);
    await dragTo(page, await port(app, "out"), await center(db3.locator("rect").first()));
    await expect(edges(page)).toHaveCount(4);

    // invalid: users have no input
    await dragTo(page, await port(app, "out"), await center(kindNode(page, "clients").locator("rect").first()));
    await expect(edges(page)).toHaveCount(4);
    await expect(page.locator(".sd-notice")).not.toHaveText("");
    guard.assertClean();
  });

  test("a link and a component are selected and deleted with the Delete button and the Delete key", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(page.getByRole("button", { name: "Удалить" })).toBeDisabled();
    // link: selected → a hint under the field → deleted
    await page.locator(".sd-edge .hit").first().dispatchEvent("click");
    await expect(page.locator(".sd-edge.on")).toHaveCount(1);
    await expect(page.locator(".sd-boardcard .sd-hint")).toContainText("выбрана");
    await page.getByRole("button", { name: "Удалить" }).click();
    await expect(edges(page)).toHaveCount(1);

    // component: selected by a click, deleted together with its links; users cannot be deleted
    await clickAt(page, await center(kindNode(page, "clients").locator("rect").first()));
    await expect(page.getByRole("button", { name: "Удалить" })).toBeDisabled();
    await clickAt(page, await center(kindNode(page, "db").locator("rect").first()));
    await expect(page.locator(".sd-float h4")).toHaveText("Database");
    await page.keyboard.press("Delete");
    await expect(kindNode(page, "db")).toHaveCount(0);
    await expect(edges(page)).toHaveCount(0);
    await expect(page.locator(".sd-float")).toHaveCount(0);
    guard.assertClean();
  });

  test("changing a parameter in the card recomputes goals and metrics; a failure and Disable change the metrics", async ({ page, request, guard }) => {
    await setup(page, request);
    await expect(metric(page, "Успешных ответов")).toHaveText("30.0%");
    await clickAt(page, await center(kindNode(page, "app").locator("rect").first()));
    await expect(page.locator(".sd-float h4")).toHaveText("App server");
    await expect(page.locator(".sd-float .sd-load")).toContainText("Нагрузка:");
    await field(page, "Размер").locator("select").selectOption("L");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    await expect(kindNode(page, "app").locator(".sd-sub")).toContainText("L");

    // zone failure: with the one-zone placement the diagram does not survive it
    const heading = page.locator(".sd-metrics h4");
    await expect(heading).not.toContainText("·");
    await page.locator(".sd-fail select").selectOption("zone");
    await expect(heading).toContainText("отказ зоны доступности");
    await expect(metric(page, "Успешных ответов")).not.toHaveText(/^100(\.0+)?%$/);
    await page.locator(".sd-fail select").selectOption("");
    await expect(heading).not.toContainText("·");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    // component kind failure: the list contains the kinds present on the diagram
    await expect(page.locator(".sd-fail select option")).toContainText(["отказ региона", "выкладка новой версии", "падает сервер приложения"]);
    await page.locator(".sd-fail select").selectOption("app");
    await expect(heading).toContainText("падает сервер приложения");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^0(\.0+)?%$/);
    await page.locator(".sd-fail select").selectOption("");

    // disable a component by hand
    await field(page, "Отключить (проверить отказ)").locator("input").check();
    await expect(page.locator(".sd-node.app")).toHaveClass(/\bdown\b/);
    await expect(kindNode(page, "app").locator(".sd-sub")).toHaveText("отключён");
    await expect(metric(page, "Успешных ответов")).toHaveText(/^0(\.0+)?%$/);
    await field(page, "Отключить (проверить отказ)").locator("input").uncheck();
    await expect(metric(page, "Успешных ответов")).toHaveText(/^100(\.0+)?%$/);
    guard.assertClean();
  });

  test("hint, the ? help, full screen and Esc", async ({ page, request, guard }) => {
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
    // in full screen the same goals and metrics are next to the field, and there is no height grip
    await expect(page.locator(".sd.fs .sd-goals li").first()).toBeVisible();
    await expect(page.locator(".sd.fs .sd-metrics")).toBeVisible();
    await expect(page.locator(".sd.fs .sd-resize")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(3);
    await page.keyboard.press("Escape");
    await expect(page.locator(".sd.fs")).toHaveCount(0);
    await expect(nodes(page)).toHaveCount(3);
    // and with the Collapse button
    await page.getByRole("button", { name: "На весь экран", exact: true }).click();
    await expect(page.locator(".sd.fs")).toBeVisible();
    await page.getByRole("button", { name: "Свернуть", exact: true }).click();
    await expect(page.locator(".sd.fs")).toHaveCount(0);
    guard.assertClean();
  });

  test("zoom: buttons, Ctrl+wheel, \"100%\" and fit; panning the empty space", async ({ page, request, guard }) => {
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
    // Ctrl + wheel over the field
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
    // fit: appeared after the view changed, returns the diagram into the window (zoom as on opening)
    await zoom.getByRole("button", { name: "⌖" }).click();
    await expect(zoomPct(page)).toHaveText(`${fit}%`);
    await expect(zoom.getByRole("button", { name: "⌖" })).toHaveCount(0);

    // pan: drag the empty place of the field
    const v0 = await vb();
    const box0 = await box(page.locator(".sd-board"));
    await dragTo(page, { x: box0.x + 60, y: box0.y + 40 }, { x: box0.x + 160, y: box0.y + 90 });
    expect(await vb()).not.toBe(v0);
    await expect(zoom.getByRole("button", { name: "⌖" })).toBeVisible();
    guard.assertClean();
  });

  test("the grip changes the field height, a double click restores it; the height is remembered", async ({ page, request, guard }) => {
    await setup(page, request);
    const viewport = page.locator(".sd-viewport");
    const h0 = (await box(viewport)).height;
    const grip = await center(page.locator(".sd-resize"));
    await dragTo(page, grip, { x: grip.x, y: grip.y + 120 });
    await expect(viewport).toHaveClass(/\bsized\b/);
    await expect.poll(async () => (await box(viewport)).height).toBeGreaterThan(h0 + 80);
    expect(await page.evaluate(() => window.localStorage.getItem("cs-core-sd-board-h"))).not.toBeNull();
    // the chosen height survives a reload
    await page.reload();
    await expect(viewport).toHaveClass(/\bsized\b/);
    await page.locator(".sd-resize").dblclick();
    await expect(viewport).not.toHaveClass(/\bsized\b/);
    await expect.poll(async () => Math.abs((await box(viewport)).height - h0)).toBeLessThan(2);
    expect(await page.evaluate(() => window.localStorage.getItem("cs-core-sd-board-h"))).toBeNull();
    guard.assertClean();
  });

  test("Reset restores the initial diagram and goals, and the draft on the server too", async ({ page, request, guard }) => {
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

  test("component count limit: an extra one is not added, the field explains why", async ({ page, request, guard }) => {
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

// --- 5. a hand-made solution -----------------------------------------------------------------------------------

test("sd02-vertical is solved by hand: server size L — goals ✓, the server accepts", async ({ page, request, guard }) => {
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
  // the saved solution is a diagram with an L server
  const saved = JSON.parse((await chapterState(request, token, "sd", chapter)).drafts[id]!) as SdState;
  expect(saved.nodes.find((n) => n.kind === "app")?.params.size).toBe("L");

  // Next leads to the next exercise of the chapter
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(labTasks("sd", chapter)[1]!.title);
  guard.assertClean();
});

test("sd01-wire is solved by hand: two links — one by dragging, the other by two clicks on ports", async ({ page, request, guard }) => {
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
