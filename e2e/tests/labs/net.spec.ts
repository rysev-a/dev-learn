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

/* Лаборатория «Компьютерные сети» (книга 15): симулятор сети в браузере, цели считает движок в wasm, решение перепроверяет сервер. */

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

// --- помощники интерфейса -------------------------------------------------------------------------------

const escapeRe = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const goalRows = (page: Page) => page.locator(".nl-goals li");
const links = (page: Page) => page.locator(".nl-board .nl-link");
const cableButton = (page: Page) => page.getByRole("button", { name: /^Кабель/ });
const zoomPct = (page: Page) => page.locator(".lab-board-wrap .lab-zoom .pct");

/** Устройство на поле по имени (точное совпадение с названием). */
const device = (page: Page, name: string) => page.locator(".nl-board .nl-dev").filter({ has: page.locator(".nl-name", { hasText: new RegExp(`^${escapeRe(name)}$`) }) });

const nameOf = (t: LabTaskData, id: string) => {
  const d = specOf(t).start.devices.find((x) => x.id === id);
  if (!d) throw new Error(`нет устройства ${id}`);
  return d.name;
};

async function center(page: Page, name: string) {
  const l = device(page, name).locator("rect").first();
  await l.scrollIntoViewIfNeeded();
  const b = await l.boundingBox();
  if (!b) throw new Error(`нет рамки у «${name}»`);
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
}

async function setCable(page: Page, on: boolean) {
  // кнопки «Кабель» нет там, где инструмент закрыт: режим кабеля и так выключен
  if ((await cableButton(page).count()) === 0) {
    if (on) throw new Error("инструмент «Кабель» закрыт");
    return;
  }
  const active = (await cableButton(page).innerText()).includes("выберите");
  if (active !== on) await cableButton(page).click();
}

/** Команда в мини-терминале выбранного (кликом) устройства; возвращает вывод команды. */
async function terminal(page: Page, name: string, line: string, { clears = false } = {}) {
  await setCable(page, false);
  await device(page, name).click();
  await expect(page.locator(".nl-panel-head h4")).toHaveText(name);
  await page.getByRole("button", { name: "Терминал", exact: true }).click();
  const out = page.locator(".nl-term-out");
  const before = await out.locator("div.cmd").count();
  await page.getByLabel("Командная строка").fill(line);
  await page.keyboard.press("Enter");
  // `clear` стирает историю, остальные команды добавляют строку
  await expect(out.locator("div.cmd")).toHaveCount(clears ? 0 : before + 1);
  return out.innerText();
}

/** Кабель между устройствами двумя кликами (режим «Кабель»). */
async function cableByClicks(page: Page, a: string, b: string) {
  await setCable(page, true);
  await device(page, a).click();
  await device(page, b).click();
}

/** Кабель протяжкой от одного устройства к другому. */
async function cableByDrag(page: Page, a: string, b: string) {
  await setCable(page, true);
  const [from, to] = [await center(page, a), await center(page, b)];
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move((from.x + to.x) / 2, (from.y + to.y) / 2, { steps: 4 });
  await page.mouse.move(to.x, to.y, { steps: 6 });
  await page.mouse.up();
}

/** Воспроизводит эталонное решение упражнения действиями в интерфейсе: кабели и команды терминала. */
async function replay(page: Page, task: LabTaskData) {
  for (const s of specOf(task).solution) {
    if (s.op === "cable") await cableByClicks(page, nameOf(task, s.a!), nameOf(task, s.b!));
    else if (s.op === "cmd") await terminal(page, nameOf(task, s.dev!), s.line!);
    else throw new Error(`шаг ${s.op} не воспроизводится в интерфейсе`);
  }
}

async function expectAllGoalsDone(page: Page, total: number) {
  await expect(goalRows(page)).toHaveCount(total);
  await expect(page.locator(".nl-goals li.ok")).toHaveCount(total);
  await expect(page.locator(".nl-goals li.bad")).toHaveCount(0);
  await expect(page.locator(".nl-goals .lab-alert.ok .lab-alert-title")).toHaveText("Все цели выполнены");
}

// --- 1. эталон: действия в интерфейсе → сервер → тот же черновик у другого ученика -----------------------------

/** Упражнения разных глав и инструментов: кабель, NAT, файрвол, окно TCP, DNS, HTTP, TLS, балансировщик, SSH. */
const PIPELINE: [number, string, string][] = [
  [1, "n1-cable", "кабель"],
  [1, "n1-switch", "кабели к коммутатору"],
  [4, "n4-nat", "NAT"],
  [6, "n6-fw", "файрвол"],
  [8, "n8-window", "окно приёма TCP"],
  [10, "n10-record", "DNS"],
  [11, "n11-404", "HTTP"],
  [13, "n13-expired", "TLS"],
  [17, "n17-pool", "балансировщик"],
  [18, "n18-keys", "SSH"],
];

test.describe("эталон, воспроизведённый в интерфейсе, засчитывается, а его черновик — и другим ученикам", () => {
  for (const [chapter, id, what] of PIPELINE) {
    test(`глава ${chapter}: ${id} (${what})`, async ({ page, request, browser, guard }) => {
      const task = labTask("net", chapter, id);
      const total = specOf(task).goals.length;
      const { token } = await loginFresh(page, request, "net");
      await openTask(page, request, "net", chapter, id);
      await expect(goalRows(page)).toHaveCount(total);
      // до первой правки цели пронумерованы, итога нет
      await expect(page.locator(".nl-goals .lab-alert")).toHaveCount(0);
      await expect(page.locator(".nl-goals li .nl-gmark").first()).toHaveText("1");

      await replay(page, task);

      await expectAllGoalsDone(page, total);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
      await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
      await expect(progressLabel(page)).toHaveText(`Решено 1 из ${labTasks("net", chapter).length}`);
      await expectStatusOk(request, token, "net", chapter, id);
      const draft = (await chapterState(request, token, "net", chapter)).drafts[id];
      expect(draft, "решение сохранено черновиком").toBeTruthy();

      // конвейер «черновик → движок → сервер»: тот же черновик у другого ученика открывается решённым
      await expectDraftSolves(browser, request, task, chapter, draft!);
      guard.assertClean();
    });
  }
});

/** Новый ученик получает черновик через API, открывает упражнение — интерфейс сам засчитывает его. */
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

// --- 2. исходное состояние не засчитывается ---------------------------------------------------------------------

test.describe("исходная сеть не засчитывается", () => {
  for (const chapter of labChapters("net")) {
    const task = labTasks("net", chapter)[0]!;
    test(`глава ${chapter}: ${task.id}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "net");
      await openTask(page, request, "net", chapter, task.id);
      await expect(goalRows(page)).toHaveCount(specOf(task).goals.length);
      await expect(page.locator(".nl-goals .lab-alert")).toHaveCount(0);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
      await expect(page.locator(".pr-list .pr-item.ok")).toHaveCount(0);
      // «Проверить» без правок: хотя бы одна цель не выполнена
      await page.getByRole("button", { name: "Проверить" }).click();
      await expect(page.locator(".nl-goals li.bad").first()).toBeVisible();
      await expect(page.locator(".nl-goals .lab-alert.bad .lab-alert-title")).toHaveText("Пока не всё работает");
      await page.waitForLoadState("networkidle");
      expect(await statusOf(request, token, "net", chapter, task.id)).toBeUndefined();
      guard.assertClean();
    });
  }
});

// --- 3. отказ сервера ------------------------------------------------------------------------------------------

test("сервер отклоняет исходную сеть, подмену устройств и недопустимые правки (422 с причиной)", async ({ page, request }) => {
  const [chapter, id] = [4, "n4-nat"];
  const task = labTask("net", chapter, id);
  const spec = specOf(task);
  const { token } = await loginFresh(page, request, "net");

  const start = await putSolved(request, token, "net", chapter, id, JSON.stringify(spec.start));
  expect(start.status).toBe(422);
  expect(start.detail).toContain("цель не выполнена");

  const junk = await putSolved(request, token, "net", chapter, id, "{не json");
  expect(junk.status).toBe(422);
  expect(junk.detail).not.toBe("");

  // кабели в упражнении без инструмента «Кабель» менять нельзя
  const noCable = JSON.parse(JSON.stringify(spec.start)) as { links: unknown[] };
  noCable.links = noCable.links.slice(1);
  const cable = await putSolved(request, token, "net", chapter, id, JSON.stringify(noCable));
  expect(cable.status).toBe(422);
  expect(cable.detail).toContain("кабел");

  // устройство подменено: другое название
  const renamed = JSON.parse(JSON.stringify(spec.start)) as { devices: { name: string }[] };
  renamed.devices[0]!.name = "Чужое устройство";
  const dev = await putSolved(request, token, "net", chapter, id, JSON.stringify(renamed));
  expect(dev.status).toBe(422);
  expect(dev.detail).toContain("подменено");

  // закрытое устройство (провайдер) менять нельзя
  const locked = JSON.parse(JSON.stringify(spec.start)) as { devices: { id: string; forward: boolean }[] };
  const isp = locked.devices.find((d) => d.id === "isp")!;
  isp.forward = !isp.forward;
  const closed = await putSolved(request, token, "net", chapter, id, JSON.stringify(locked));
  expect(closed.status).toBe(422);
  expect(closed.detail).toContain("закрыто");

  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
});

test("интерфейс показывает причину отказа сервера, если ему подменили решение", async ({ page, request, guard }) => {
  const [chapter, id] = [1, "n1-cable"];
  const task = labTask("net", chapter, id);
  const { token } = await loginFresh(page, request, "net");
  await page.route(`**/api/exercises/15/${chapter}/${id}/solved`, (route) =>
    route.continue({ postData: JSON.stringify({ solution: JSON.stringify(specOf(task).start) }) }),
  );
  await openTask(page, request, "net", chapter, id);
  const refused = page.waitForResponse((r) => r.url().endsWith(`/${id}/solved`) && r.request().method() === "PUT");
  await cableByClicks(page, "ПК 1", "ПК 2");
  expect((await refused).status()).toBe(422);
  const error = page.locator(".pr-main p.error");
  await expect(error).toContainText("Решение не принято");
  await expect(error).toContainText("цель не выполнена");
  await expect(page.locator(".nl-goals .lab-alert-title")).toHaveText("Все цели выполнены");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("не решено");
  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
  expect(guard.errors.filter((e) => !/422/.test(e))).toEqual([]);
});

// --- 4. реальные действия на поле -------------------------------------------------------------------------------

test.describe("действия на поле", () => {
  test("кабель протяжкой, ping в терминале, журнал и «▶» у цели показывают путь пакета", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await expect(links(page)).toHaveCount(0);
    await expect(page.locator(".nl-log .nl-none")).toBeVisible();

    await cableByDrag(page, "ПК 1", "ПК 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-board .nl-port").first()).toHaveText("eth0");
    await expect(page.locator(".nl-goals li.ok")).toHaveCount(1);

    const out = await terminal(page, "ПК 1", "ping -c 2 192.168.0.2");
    expect(out).toContain("2 packets transmitted, 2 received, 0% packet loss");
    await expect(page.locator(".nl-log ol li").first()).toBeVisible();
    await expect(page.locator(".nl-log h4 small")).toContainText("ping -c 2 192.168.0.2");
    await expect(page.locator(".nl-caption")).toBeVisible();

    // «▶» у цели: путь пакета по цели, журнал подписан текстом цели
    await page.locator(".nl-goals li .nl-play").first().click();
    await expect(page.locator(".nl-log h4 small")).toContainText("ПК 1 пингует ПК 2");
    await expect(page.locator(".nl-log ol li").first()).toBeVisible();

    // команда терминала: справка, неизвестная команда, clear
    expect(await terminal(page, "ПК 1", "help")).not.toBe("");
    await terminal(page, "ПК 1", "hostname");
    await terminal(page, "ПК 1", "clear", { clears: true });

    await expectStatusOk(request, token, "net", chapter, id);
    guard.assertClean();
  });

  test("свободных портов нет: лишний кабель отклоняется с сообщением, кабель выбирается и удаляется", async ({ page, request, guard }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 1, "n1-cable");
    await cableByClicks(page, "ПК 1", "ПК 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-notice")).toHaveCount(0);
    // у каждого ПК по одному порту — второй кабель между ними не проложить
    await cableByClicks(page, "ПК 1", "ПК 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-notice")).not.toHaveText("");
    // выбрать кабель и удалить
    await page.locator(".nl-board .nl-link .hit").first().dispatchEvent("click");
    await expect(page.locator(".nl-link.on")).toHaveCount(1);
    await page.getByRole("button", { name: "Удалить кабель" }).click();
    await expect(links(page)).toHaveCount(0);
    await page.getByRole("button", { name: "Проверить" }).click();
    await expect(page.locator(".nl-goals li.bad")).toHaveCount(1);
    guard.assertClean();
  });

  test("устройство перетаскивается, положение сохраняется черновиком", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    const dev = device(page, "ПК 1");
    const before = await dev.getAttribute("transform");
    const c = await center(page, "ПК 1");
    await page.mouse.move(c.x, c.y);
    await page.mouse.down();
    await page.mouse.move(c.x + 60, c.y + 40, { steps: 6 });
    await page.mouse.up();
    await expect(dev).not.toHaveAttribute("transform", before!);
    await expect(dev).toHaveClass(/\bon\b/);
    await expect(page.locator(".nl-panel-head h4")).toHaveText("ПК 1");
    // черновик на сервере содержит новое положение
    await expect.poll(async () => (await chapterState(request, token, "net", chapter)).drafts[id] ?? "").not.toBe("");
    const saved = (await chapterState(request, token, "net", chapter)).drafts[id]!;
    expect(saved).not.toBe(JSON.stringify(specOf(labTask("net", chapter, id)).start));
    guard.assertClean();
  });

  test("форма устройства: маска ПК 2 меняется в поле — n2-l3 решается, сервер принимает", async ({ page, request, guard }) => {
    const [chapter, id] = [2, "n2-l3"];
    const task = labTask("net", chapter, id);
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await device(page, "ПК 2").click();
    await expect(page.locator(".nl-panel-head h4")).toHaveText("ПК 2");
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

  test("форма устройства: адрес и шлюз задаются в полях (n4-plan: четыре ПК)", async ({ page, request, guard }) => {
    const [chapter, id] = [4, "n4-plan"];
    const task = labTask("net", chapter, id);
    const { token } = await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    const plan: [string, string, string, string][] = [
      ["ПК А1", "192.168.10.2", "26", "192.168.10.1"],
      ["ПК А2", "192.168.10.3", "26", "192.168.10.1"],
      ["ПК Б1", "192.168.10.66", "27", "192.168.10.65"],
      ["ПК Б2", "192.168.10.67", "27", "192.168.10.65"],
    ];
    for (const [name, ip, prefix, gw] of plan) {
      await device(page, name).click();
      await expect(page.locator(".nl-panel-head h4")).toHaveText(name);
      // адрес записывается по Enter, после него поле пересоздаётся — маска вводится отдельно
      await page.getByLabel("IP eth0").fill(ip);
      await page.getByLabel("IP eth0").press("Enter");
      await expect(page.getByLabel("IP eth0")).toHaveValue(ip);
      await page.getByLabel("Маска").fill(prefix);
      await page.getByLabel("Маска").press("Enter");
      const gateway = page.locator(".nl-field", { hasText: "Шлюз по умолчанию" }).locator("input");
      await gateway.fill(gw);
      await gateway.press("Enter");
      await expect(device(page, name).locator(".nl-ip")).toHaveText(`${ip}/${prefix}`);
      // фокус уходит из поля до смены устройства (см. fixme про панику при смене устройства с фокусом в поле шлюза)
      await page.locator(".nl-panel-head h4").click();
    }
    await expectAllGoalsDone(page, specOf(task).goals.length);
    await expectStatusOk(request, token, "net", chapter, id);
    guard.assertClean();
  });

  test("«Проверить», «Подсказка», «Сбросить» и масштаб поля", async ({ page, request, guard }) => {
    const [chapter, id] = [1, "n1-cable"];
    const task = labTask("net", chapter, id);
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", chapter, id);
    await expect(page.locator(".nl-hint")).toHaveCount(0);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".nl-hint")).toHaveText(task.hint);
    await page.getByRole("button", { name: "Подсказка" }).click();
    await expect(page.locator(".nl-hint")).toHaveCount(0);

    // масштаб: кнопки и «100%»
    const zoom = page.locator(".lab-board-wrap .lab-zoom");
    await expect(zoomPct(page)).toHaveText("100%");
    await zoom.getByRole("button", { name: "+" }).click();
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeGreaterThan(100);
    await zoom.getByRole("button", { name: "−" }).click();
    await zoom.getByRole("button", { name: "−" }).click();
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeLessThan(100);
    await zoomPct(page).click();
    await expect(zoomPct(page)).toHaveText("100%");
    // Ctrl + колесо
    const b = (await page.locator(".nl-board").boundingBox())!;
    await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2);
    await page.keyboard.down("Control");
    await page.mouse.wheel(0, -300);
    await page.keyboard.up("Control");
    await expect.poll(async () => Number((await zoomPct(page).innerText()).replace("%", ""))).toBeGreaterThan(100);
    await zoomPct(page).click();

    // «Сбросить» возвращает исходную сеть, цели снова пронумерованы
    await cableByClicks(page, "ПК 1", "ПК 2");
    await expect(links(page)).toHaveCount(1);
    await expect(page.locator(".nl-goals li.ok")).toHaveCount(1);
    await page.getByRole("button", { name: "Сбросить" }).click();
    await expect(links(page)).toHaveCount(0);
    // упражнение уже решено, поэтому цели показаны отметками; после сброса цель не выполнена
    await expect(page.locator(".nl-goals li.bad")).toHaveCount(1);
    await expect(page.locator(".nl-goals .lab-alert.ok")).toHaveCount(0);
    guard.assertClean();
  });

  // ДЕФЕКТ приложения: паника Rust. Шаги: выбрать ПК, ввести шлюз и нажать Enter (фокус остаётся в поле), кликнуть другое
  // устройство. Форма шлюза уничтожается, а событие blur поля вызывает её обработчик: «you tried to access a reactive value
  // which was defined at forms.rs:275 ... already been disposed», затем «unreachable» в консоли.
  test("смена устройства при фокусе в поле шлюза не вызывает панику", async ({ page, request, guard }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 4, "n4-plan");
    await device(page, "ПК А1").click();
    const gateway = page.locator(".nl-field", { hasText: "Шлюз по умолчанию" }).locator("input");
    await gateway.fill("192.168.10.1");
    await gateway.press("Enter");
    await device(page, "ПК А2").click();
    await expect(page.locator(".nl-panel-head h4")).toHaveText("ПК А2");
    guard.assertClean();
  });

  // ДЕФЕКТ приложения: адрес записывается при потере фокуса поля, после чего строка интерфейса пересоздаётся —
  // и набранная следом маска пропадает (фокус теряется, в поле остаётся /24). Шаги: ПК А1 → поле «IP eth0»,
  // набрать адрес, Tab, набрать 26, Enter. Ожидается: на устройстве 192.168.10.2/26.
  test("Tab из поля адреса в поле маски не теряет набранную маску", async ({ page, request }) => {
    await loginFresh(page, request, "net");
    await openTask(page, request, "net", 4, "n4-plan");
    await device(page, "ПК А1").click();
    await page.getByLabel("IP eth0").click();
    await page.keyboard.type("192.168.10.2");
    await page.keyboard.press("Tab");
    await page.keyboard.type("26");
    await page.keyboard.press("Enter");
    await expect(device(page, "ПК А1").locator(".nl-ip")).toHaveText("192.168.10.2/26");
  });
});

// --- 5. решение руками --------------------------------------------------------------------------------------------

test("n1-cable решается руками: кабель протяжкой между портами двух ПК, сервер принимает", async ({ page, request, guard }) => {
  const [chapter, id] = [1, "n1-cable"];
  const task = labTask("net", chapter, id);
  const { token } = await loginFresh(page, request, "net");
  await openTask(page, request, "net", chapter, id);
  expect(await statusOf(request, token, "net", chapter, id)).toBeUndefined();
  await cableByDrag(page, "ПК 1", "ПК 2");
  await expectAllGoalsDone(page, specOf(task).goals.length);
  await expect(page.locator(".nl-goals .lab-alert-text")).toHaveText("Упражнение засчитано.");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expectStatusOk(request, token, "net", chapter, id);
  // «Дальше» — следующее упражнение главы
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(labTasks("net", chapter)[1]!.title);
  guard.assertClean();
});
