import type { Browser, Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import {
  chapterState,
  expectStatusOk,
  labChapters,
  labTask,
  labTasks,
  listItem,
  openTask,
  progressLabel,
  putDraft,
  putSolved,
  statusOf,
  type LabTaskData,
} from "../../support/labs";

/* Computer Networks lab (book 15): a network simulator in the browser, goals are computed by the wasm engine, the server re-checks the solution. */

test.use({ viewport: { width: 1500, height: 1300 } });

interface Device {
  id: string;
  name: string;
}
interface Step {
  op: "cable" | "cmd" | "unlink" | "drop";
  a?: string;
  b?: string;
  dev?: string;
  line?: string;
}
interface NetSpecData {
  start: { devices: Device[]; links: unknown[] };
  goals: { text: string }[];
  solution: Step[];
  tools: Record<string, boolean>;
}
const specOf = (t: LabTaskData) => t.spec as unknown as NetSpecData;

// --- UI helpers -------------------------------------------------------------------------------

const escapeRe = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const goalRows = (page: Page) => page.locator(".nl-goals li");
const links = (page: Page) => page.locator(".nl-board .nl-link");
const cableButton = (page: Page) => page.getByRole("button", { name: /^Кабель/ });
const zoomPct = (page: Page) => page.locator(".lab-board-wrap .lab-zoom .pct");

/** A device on the field by name (exact match with the title). */
const device = (page: Page, name: string) => page.locator(".nl-board .nl-dev").filter({ has: page.locator(".nl-name", { hasText: new RegExp(`^${escapeRe(name)}$`) }) });

const nameOf = (t: LabTaskData, id: string) => {
  const d = specOf(t).start.devices.find((x) => x.id === id);
  if (!d) throw new Error(`no device ${id}`);
  return d.name;
};

async function center(page: Page, name: string) {
  const l = device(page, name).locator("rect").first();
  await l.scrollIntoViewIfNeeded();
  const b = await l.boundingBox();
  if (!b) throw new Error(`no bounding box for "${name}"`);
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
}

async function setCable(page: Page, on: boolean) {
  // the Cable button is absent where the tool is locked: cable mode is off anyway
  if ((await cableButton(page).count()) === 0) {
    if (on) throw new Error("the Cable tool is locked");
    return;
  }
  const active = (await cableButton(page).innerText()).includes("выберите");
  if (active !== on) await cableButton(page).click();
}

/** A command in the mini terminal of the (clicked) selected device; returns the command output. */
async function terminal(page: Page, name: string, line: string, { clears = false } = {}) {
  await setCable(page, false);
  await device(page, name).click();
  await expect(page.locator(".nl-panel-head h4")).toHaveText(name);
  await page.getByRole("button", { name: "Терминал", exact: true }).click();
  const out = page.locator(".nl-term-out");
  const before = await out.locator("div.cmd").count();
  await page.getByLabel("Командная строка").fill(line);
  await page.keyboard.press("Enter");
  // `clear` wipes the history, other commands add a line
  await expect(out.locator("div.cmd")).toHaveCount(clears ? 0 : before + 1);
  return out.innerText();
}

/** A cable between devices with two clicks (Cable mode). */
async function cableByClicks(page: Page, a: string, b: string) {
  await setCable(page, true);
  await device(page, a).click();
  await device(page, b).click();
}

/** A cable dragged from one device to another. */
async function cableByDrag(page: Page, a: string, b: string) {
  await setCable(page, true);
  const [from, to] = [await center(page, a), await center(page, b)];
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move((from.x + to.x) / 2, (from.y + to.y) / 2, { steps: 4 });
  await page.mouse.move(to.x, to.y, { steps: 6 });
  await page.mouse.up();
}

/** Replays the exercise reference solution with UI actions: cables and terminal commands. */
async function replay(page: Page, task: LabTaskData) {
  for (const s of specOf(task).solution) {
    if (s.op === "cable") await cableByClicks(page, nameOf(task, s.a!), nameOf(task, s.b!));
    else if (s.op === "cmd") await terminal(page, nameOf(task, s.dev!), s.line!);
    else throw new Error(`step ${s.op} cannot be replayed in the UI`);
  }
}

async function expectAllGoalsDone(page: Page, total: number) {
  await expect(goalRows(page)).toHaveCount(total);
  await expect(page.locator(".nl-goals li.ok")).toHaveCount(total);
  await expect(page.locator(".nl-goals li.bad")).toHaveCount(0);
  await expect(page.locator(".nl-goals .lab-alert.ok .lab-alert-title")).toHaveText("Все цели выполнены");
}

// --- 1. reference: UI actions → server → the same draft for another student -----------------------------

/** Exercises of different chapters and tools: cable, NAT, firewall, TCP window, DNS, HTTP, TLS, load balancer, SSH. */
const PIPELINE: [number, string, string][] = [
  [1, "n1-cable", "cable"],
  [1, "n1-switch", "cables to a switch"],
  [4, "n4-nat", "NAT"],
  [6, "n6-fw", "firewall"],
  [8, "n8-window", "TCP receive window"],
  [10, "n10-record", "DNS"],
  [11, "n11-404", "HTTP"],
  [13, "n13-expired", "TLS"],
  [17, "n17-pool", "load balancer"],
  [18, "n18-keys", "SSH"],
];

test.describe("a reference replayed in the UI is accepted, and its draft is accepted for other students too", () => {
  for (const [chapter, id, what] of PIPELINE) {
    test(`chapter ${chapter}: ${id} (${what})`, async ({ page, request, browser, guard }) => {
      const task = labTask("net", chapter, id);
      const total = specOf(task).goals.length;
      const { token } = await loginFresh(page, request, "net");
      await openTask(page, request, "net", chapter, id);
      await expect(goalRows(page)).toHaveCount(total);
      // before the first edit the goals are numbered, no verdict yet
      await expect(page.locator(".nl-goals .lab-alert")).toHaveCount(0);
      await expect(page.locator(".nl-goals li .nl-gmark").first()).toHaveText("1");

      await replay(page, task);

      await expectAllGoalsDone(page, total);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
      await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
      await expect(progressLabel(page)).toHaveText(`Решено 1 из ${labTasks("net", chapter).length}`);
      await expectStatusOk(request, token, "net", chapter, id);
      const draft = (await chapterState(request, token, "net", chapter)).drafts[id];
      expect(draft, "the solution is saved as a draft").toBeTruthy();

      // the draft → engine → server pipeline: the same draft opens as solved for another student
      await expectDraftSolves(browser, request, task, chapter, draft!);
      guard.assertClean();
    });
  }
});

/** A new student gets the draft through the API and opens the exercise — the UI accepts it by itself. */
async function expectDraftSolves(browser: Browser, request: Parameters<typeof loginFresh>[1], task: LabTaskData, chapter: number, draft: string) {
  const context = await browser.newContext({ viewport: { width: 1500, height: 1300 }, locale: "ru-RU" });
  try {
    const page = await context.newPage();
    const { token } = await loginFresh(page, request, "net-b");
    await putDraft(request, token, "net", chapter, task.id, draft);
    await openTask(page, request, "net", chapter, task.id);
    await expectAllGoalsDone(page, specOf(task).goals.length);
    await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
    await expectStatusOk(request, token, "net", chapter, task.id);
  } finally {
    await context.close();
  }
}

// --- 2. the initial state is not accepted ---------------------------------------------------------------------

test.describe("the initial network is not accepted", () => {
  for (const chapter of labChapters("net")) {
    const task = labTasks("net", chapter)[0]!;
    test(`chapter ${chapter}: ${task.id}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "net");
      await openTask(page, request, "net", chapter, task.id);
      await expect(goalRows(page)).toHaveCount(specOf(task).goals.length);
      await expect(page.locator(".nl-goals .lab-alert")).toHaveCount(0);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
      await expect(page.locator(".pr-list .pr-item.ok")).toHaveCount(0);
      // Check without edits: at least one goal is not met
      await page.getByRole("button", { name: "Проверить" }).click();
      await expect(page.locator(".nl-goals li.bad").first()).toBeVisible();
      await expect(page.locator(".nl-goals .lab-alert.bad .lab-alert-title")).toHaveText("Пока не всё работает");
      await page.waitForLoadState("networkidle");
      expect(await statusOf(request, token, "net", chapter, task.id)).toBeUndefined();
      guard.assertClean();
    });
  }
});

// --- 3. server rejection ------------------------------------------------------------------------------------------

test("the server rejects the initial network, device substitution and invalid edits (422 with a reason)", async ({ page, request }) => {
  const [chapter, id] = [4, "n4-nat"];
  const task = labTask("net", chapter, id);
  const spec = specOf(task);
  const { token } = await loginFresh(page, request, "net");

  const start = await putSolved(request, token, "net", chapter, id, JSON.stringify(spec.start));
  expect(start.status).toBe(422);
  expect(start.detail).toContain("цель не выполнена");

  const junk = await putSolved(request, token, "net", chapter, id, "{not json");
  expect(junk.status).toBe(422);
  expect(junk.detail).not.toBe("");

  // cables cannot be changed in an exercise without the Cable tool
  const noCable = JSON.parse(JSON.stringify(spec.start)) as { links: unknown[] };
  noCable.links = noCable.links.slice(1);
  const cable = await putSolved(request, token, "net", chapter, id, JSON.stringify(noCable));
  expect(cable.status).toBe(422);
  expect(cable.detail).toContain("кабел");

  // device substituted: another name
  const renamed = JSON.parse(JSON.stringify(spec.start)) as { devices: { name: string }[] };
  renamed.devices[0]!.name = "Foreign device";
  const dev = await putSolved(request, token, "net", chapter, id, JSON.stringify(renamed));
  expect(dev.status).toBe(422);
  expect(dev.detail).toContain("подменено");

  // a locked device (the provider) cannot be changed
  const locked = JSON.parse(JSON.stringify(spec.start)) as { devices: { id: string; forward: boolean }[] };
  const isp = locked.devices.find((d) => d.id === "isp")!;
  isp.forward = !isp.forward;
  const closed = await putSolved(request, token, "net", chapter, id, JSON.stringify(locked));
  expect(closed.status).toBe(422);
  expect(closed.detail).toContain("закрыто");

  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
});

test("the UI shows the server rejection reason when the solution was tampered with", async ({ page, request, guard }) => {
  const [chapter, id] = [1, "n1-cable"];
  const task = labTask("net", chapter, id);
  const { token } = await loginFresh(page, request, "net");
  await page.route(`**/api/exercises/15/${chapter}/${id}/solved`, (route) =>
    route.continue({ postData: JSON.stringify({ solution: JSON.stringify(specOf(task).start) }) }),
  );
  await openTask(page, request, "net", chapter, id);
  const refused = page.waitForResponse((r) => r.url().endsWith(`/${id}/solved`) && r.request().method() === "PUT");
  await cableByClicks(page, "PC 1", "PC 2");
  expect((await refused).status()).toBe(422);
  const error = page.locator(".pr-main p.error");
  await expect(error).toContainText("Решение не принято");
  await expect(error).toContainText("цель не выполнена");
  await expect(page.locator(".nl-goals .lab-alert-title")).toHaveText("Все цели выполнены");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
  expect(guard.errors.filter((e) => !/422/.test(e))).toEqual([]);
});

// --- 4. real actions on the field -------------------------------------------------------------------------------

test.describe("actions on the field", () => {
  test("cable by drag, ping in the terminal, the log and the goal ▶ show the packet path", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await expect(links(page)).toHaveCount(0);
    await expect(page.locator(".nl-log .nl-none")).toBeVisible();

    await cableByDrag(page, "PC 1", "PC 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-board .nl-port").first()).toHaveText("eth0");
    await expect(page.locator(".nl-goals li.ok")).toHaveCount(1);

    const out = await terminal(page, "PC 1", "ping -c 2 192.168.0.2");
    expect(out).toContain("2 packets transmitted, 2 received, 0% packet loss");
    await expect(page.locator(".nl-log ol li").first()).toBeVisible();
    await expect(page.locator(".nl-log h4 small")).toContainText("ping -c 2 192.168.0.2");
    await expect(page.locator(".nl-caption")).toBeVisible();

    // ▶ on a goal: the packet path for the goal, the log is titled with the goal text
    await page.locator(".nl-goals li .nl-play").first().click();
    await expect(page.locator(".nl-log h4 small")).toContainText("PC 1 pings PC 2");
    await expect(page.locator(".nl-log ol li").first()).toBeVisible();

    // terminal command: help, an unknown command, clear
    expect(await terminal(page, "PC 1", "help")).not.toBe("");
    await terminal(page, "PC 1", "hostname");
    await terminal(page, "PC 1", "clear", { clears: true });

    await expectStatusOk(request, token, "net", chapter, id);
    guard.assertClean();
  });

  test("no free ports: an extra cable is rejected with a message, a cable is selected and deleted", async ({ page, request, guard }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 1, "n1-cable");
    await cableByClicks(page, "PC 1", "PC 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-notice")).toHaveCount(0);
    // each PC has one port — a second cable between them cannot be laid
    await cableByClicks(page, "PC 1", "PC 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-notice")).not.toHaveText("");
    // select a cable and delete it
    await page.locator(".nl-board .nl-link .hit").first().dispatchEvent("click");
    await expect(page.locator(".nl-link.on")).toHaveCount(1);
    await page.getByRole("button", { name: "Удалить кабель" }).click();
    await expect(links(page)).toHaveCount(0);
    await page.getByRole("button", { name: "Проверить" }).click();
    await expect(page.locator(".nl-goals li.bad")).toHaveCount(1);
    guard.assertClean();
  });

  test("a device is dragged, the position is saved as a draft", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    const dev = device(page, "PC 1");
    const before = await dev.getAttribute("transform");
    const c = await center(page, "PC 1");
    await page.mouse.move(c.x, c.y);
    await page.mouse.down();
    await page.mouse.move(c.x + 60, c.y + 40, { steps: 6 });
    await page.mouse.up();
    await expect(dev).not.toHaveAttribute("transform", before!);
    await expect(dev).toHaveClass(/\bon\b/);
    await expect(page.locator(".nl-panel-head h4")).toHaveText("PC 1");
    // the draft on the server contains the new position
    await expect.poll(async () => (await chapterState(request, token, "net", chapter)).drafts[id] ?? "").not.toBe("");
    const saved = (await chapterState(request, token, "net", chapter)).drafts[id]!;
    expect(saved).not.toBe(JSON.stringify(specOf(labTask("net", chapter, id)).start));
    guard.assertClean();
  });

  test("device form: the mask of PC 2 is changed in the field — n2-l3 is solved, the server accepts", async ({ page, request, guard }) => {
    const [chapter, id] = [2, "n2-l3"];
    const task = labTask("net", chapter, id);
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await device(page, "PC 2").click();
    await expect(page.locator(".nl-panel-head h4")).toHaveText("PC 2");
    await expect(page.getByLabel("IP eth0")).toHaveValue("192.168.0.200");
    const mask = page.getByLabel("Маска");
    await expect(mask).toHaveValue("25");
    await page.getByRole("button", { name: "Проверить" }).click();
    await expect(page.locator(".nl-goals li.bad").first()).toBeVisible();
    await mask.fill("24");
    await mask.press("Enter");
    await expectAllGoalsDone(page, specOf(task).goals.length);
    await expect(page.locator(".nl-goals .lab-alert-text")).toHaveText("Упражнение засчитано.");
    await expectStatusOk(request, token, "net", chapter, id);
    await expect(page.getByRole("button", { name: "Дальше" })).toBeVisible();
    guard.assertClean();
  });

  test("device form: address and gateway are set in the fields (n4-plan: four PCs)", async ({ page, request, guard }) => {
    const [chapter, id] = [4, "n4-plan"];
    const task = labTask("net", chapter, id);
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    const plan: [string, string, string, string][] = [
      ["PC A1", "192.168.10.2", "26", "192.168.10.1"],
      ["PC A2", "192.168.10.3", "26", "192.168.10.1"],
      ["PC B1", "192.168.10.66", "27", "192.168.10.65"],
      ["PC B2", "192.168.10.67", "27", "192.168.10.65"],
    ];
    for (const [name, ip, prefix, gw] of plan) {
      await device(page, name).click();
      await expect(page.locator(".nl-panel-head h4")).toHaveText(name);
      // the address is committed on Enter, after which the field is recreated — the mask is entered separately
      await page.getByLabel("IP eth0").fill(ip);
      await page.getByLabel("IP eth0").press("Enter");
      await expect(page.getByLabel("IP eth0")).toHaveValue(ip);
      await page.getByLabel("Маска").fill(prefix);
      await page.getByLabel("Маска").press("Enter");
      const gateway = page.locator(".nl-field", { hasText: "Шлюз по умолчанию" }).locator("input");
      await gateway.fill(gw);
      await gateway.press("Enter");
      await expect(device(page, name).locator(".nl-ip")).toHaveText(`${ip}/${prefix}`);
      // focus leaves the field before switching devices (see the fixme about the panic when switching devices with focus in the gateway field)
      await page.locator(".nl-panel-head h4").click();
    }
    await expectAllGoalsDone(page, specOf(task).goals.length);
    await expectStatusOk(request, token, "net", chapter, id);
    guard.assertClean();
  });

  test("Check, Hint, Reset and the field zoom", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const task = labTask("net", chapter, id);
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await expect(page.locator(".nl-hint")).toHaveCount(0);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".nl-hint")).toHaveText(task.hint);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".nl-hint")).toHaveCount(0);

    // zoom: buttons and "100%"
    const zoom = page.locator(".lab-board-wrap .lab-zoom");
    await expect(zoomPct(page)).toHaveText("100%");
    await zoom.getByRole("button", { name: "+" }).click();
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeGreaterThan(100);
    await zoom.getByRole("button", { name: "−" }).click();
    await zoom.getByRole("button", { name: "−" }).click();
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeLessThan(100);
    await zoomPct(page).click();
    await expect(zoomPct(page)).toHaveText("100%");
    // Ctrl + wheel
    const b = (await page.locator(".nl-board").boundingBox())!;
    await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2);
    await page.keyboard.down("Control");
    await page.mouse.wheel(0, -300);
    await page.keyboard.up("Control");
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeGreaterThan(100);
    await zoomPct(page).click();

    // Reset restores the initial network, goals are numbered again
    await cableByClicks(page, "PC 1", "PC 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-goals li.ok")).toHaveCount(1);
    await page.getByRole("button", { name: "Сбросить" }).click();
    await expect(links(page)).toHaveCount(0);
    // the exercise is already solved, so goals are shown as marks; after a reset a goal is not met
    await expect(page.locator(".nl-goals li.bad")).toHaveCount(1);
    await expect(page.locator(".nl-goals .lab-alert.ok")).toHaveCount(0);
    guard.assertClean();
  });

  // APP DEFECT: a Rust panic. Steps: select a PC, enter a gateway and press Enter (focus stays in the field), click another
  // device. The gateway form is destroyed while the field's blur event calls its handler: "you tried to access a reactive value
  // which was defined at forms.rs:275 ... already been disposed", then "unreachable" in the console.
  test("switching devices with focus in the gateway field does not cause a panic", async ({ page, request, guard }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 4, "n4-plan");
    await device(page, "PC A1").click();
    const gateway = page.locator(".nl-field", { hasText: "Шлюз по умолчанию" }).locator("input");
    await gateway.fill("192.168.10.1");
    await gateway.press("Enter");
    await device(page, "PC A2").click();
    await expect(page.locator(".nl-panel-head h4")).toHaveText("PC A2");
    guard.assertClean();
  });

  // APP DEFECT: the address is committed when the field loses focus, after which the UI row is recreated —
  // and the mask typed next disappears (focus is lost, the field keeps /24). Steps: PC А1 → the "IP eth0" field,
  // type an address, Tab, type 26, Enter. Expected: the device has 192.168.10.2/26.
  test("Tab from the address field to the mask field keeps the typed mask", async ({ page, request }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 4, "n4-plan");
    await device(page, "PC A1").click();
    await page.getByLabel("IP eth0").click();
    await page.keyboard.type("192.168.10.2");
    await page.keyboard.press("Tab");
    await page.keyboard.type("26");
    await page.keyboard.press("Enter");
    await expect(device(page, "PC A1").locator(".nl-ip")).toHaveText("192.168.10.2/26");
  });
});

// --- 5. a hand-made solution --------------------------------------------------------------------------------------------

test("n1-cable is solved by hand: a cable dragged between the ports of two PCs, the server accepts", async ({ page, request, guard }) => {
  const [chapter, id] = [1, "n1-cable"];
  const task = labTask("net", chapter, id);
  const { token } = await loginFresh(page, request, "net");
  await openTask(page, request, "net", chapter, id);
  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
  await cableByDrag(page, "PC 1", "PC 2");
  await expectAllGoalsDone(page, specOf(task).goals.length);
  await expect(page.locator(".nl-goals .lab-alert-text")).toHaveText("Упражнение засчитано.");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expectStatusOk(request, token, "net", chapter, id);
  // Next — the next exercise of the chapter
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(labTasks("net", chapter)[1]!.title);
  guard.assertClean();
});
