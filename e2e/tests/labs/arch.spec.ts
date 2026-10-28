import type { Page } from "@playwright/test";
import {
  ARCH_CHAPTERS,
  centerOf,
  chapterState,
  circuitOf,
  clickCenter,
  emptyDrawing,
  expectCircuitSolved,
  listItem,
  openTask,
  playSteps,
  putDraft,
  putSolved,
  rejectionOf,
  solutionText,
  solveBefore,
  solveViaApi,
  statusOf,
  tasksOf,
  type CircuitSpec,
  type LabTask,
} from "../../support/arch";
import { expect, loginFresh, test } from "../../support/fixtures";

/* Circuit lab (book 14, chapters 6–14): gates and blocks. References come from the course data; student solutions are stored
   as drafts and composite blocks are unlocked by solved exercises, so the course order matters. */

const CIRCUIT_CHAPTERS = ARCH_CHAPTERS.filter((c) => c <= 14);
const ALL = process.env["E2E_ARCH_ALL"] === "1";

/** Which chapter exercises are checked in the UI: first, middle and last (all with E2E_ARCH_ALL=1; chapter 14 in full). */
function sample(chapter: number): LabTask<CircuitSpec>[] {
  const list = tasksOf(chapter) as LabTask<CircuitSpec>[];
  if (ALL || chapter === 14) return list;
  const picks = new Set([0, Math.floor(list.length / 2), list.length - 1]);
  return list.filter((_, i) => picks.has(i));
}

test.describe("circuits: the reference from a draft is accepted by the UI", () => {
  test.setTimeout(240_000);
  for (const chapter of CIRCUIT_CHAPTERS) {
    test(`chapter ${chapter}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "arch");
      const targets = new Set(sample(chapter).map((t) => t.id));
      await solveBefore(request, token, chapter, tasksOf(chapter)[0]!.id);
      for (const task of tasksOf(chapter) as LabTask<CircuitSpec>[]) {
        if (!targets.has(task.id)) {
          await solveViaApi(request, token, chapter, task.id); // for course order: blocks are assembled from solved ones
          continue;
        }
        await test.step(`${task.id}: ${task.title}`, async () => {
          expect(await statusOf(request, token, chapter, task.id), "not solved before opening").not.toBe("ok");
          await putDraft(request, token, chapter, task.id, solutionText(task));
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "steps") {
            await expect(page.locator(".lab-steps .lab-step")).toHaveCount(task.spec.steps.length);
            await playSteps(page, task.spec);
          } else {
            await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          }
          await expectCircuitSolved(page, request, token, chapter, task);
          // a solved exercise survives a reload: the circuit is back, status ✓
          await page.reload();
          await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
        });
      }
      guard.assertClean();
    });
  }
});

/* ——— initial, empty and incomplete solution ——— */

/** A solution without the last wire/bus: the circuit is almost ready but does not work. */
function withoutLastWire(task: LabTask<CircuitSpec>): string {
  const sol = JSON.parse(solutionText(task)) as { wires?: unknown[]; bus_wires?: unknown[] };
  const key = task.spec.build === "gates" ? "wires" : "bus_wires";
  const list = sol[key] ?? [];
  return JSON.stringify({ ...sol, [key]: list.slice(0, -1) });
}

test("circuits: an empty board and an incomplete circuit do not solve the exercise (first and last in every chapter)", async ({ page, request, guard }) => {
  test.setTimeout(240_000);
  const { token } = await loginFresh(page, request, "arch-neg");
  for (const chapter of CIRCUIT_CHAPTERS) {
    const list = tasksOf(chapter) as LabTask<CircuitSpec>[];
    await solveBefore(request, token, chapter, list[0]!.id);
    for (const task of list) {
      const edge = task === list[0] || task === list[list.length - 1];
      if (edge) {
        await test.step(`${chapter}/${task.id}: empty board, then incomplete circuit`, async () => {
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "steps") await expect(page.locator(".lab-card-head .lab-badge", { hasText: `Шаг 1 / ${task.spec.steps.length}` })).toBeVisible();
          else await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          await expect(page.locator(".lab-alert")).toHaveCount(0);
          await expect(listItem(page, task.title)).not.toHaveClass(/\bok\b/);
          await expect(page.locator(".pr-head .pr-badge")).not.toHaveText("выполнено");

          // a circuit without the last wire: the UI does not accept it (neither empty nor almost ready — the server received nothing)
          await putDraft(request, token, chapter, task.id, withoutLastWire(task));
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "table") await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          await expect(page.locator(".lab-alert")).toHaveCount(0);
          await expect(page.locator(".lab-card-head .lab-badge.ok")).toHaveCount(0);
          expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
          // and the server rejects the same solution with a reason
          const res = await putSolved(request, token, chapter, task.id, withoutLastWire(task));
          expect(res.status()).toBe(422);
          expect((await rejectionOf(res)).length).toBeGreaterThan(5);
        });
      }
      await solveViaApi(request, token, chapter, task.id);
    }
  }
  guard.assertClean();
});

/* ——— server: rejections and course order ——— */

test("server: references of all chapter 6–14 exercises are accepted in course order, an empty circuit is rejected with a reason", async ({ page, request }) => {
  test.setTimeout(120_000);
  const { token } = await loginFresh(page, request, "arch-api");
  let count = 0;
  for (const chapter of CIRCUIT_CHAPTERS) {
    for (const task of tasksOf(chapter) as LabTask<CircuitSpec>[]) {
      const empty = await putSolved(request, token, chapter, task.id, emptyDrawing(task.spec.build));
      expect(empty.status(), `${chapter}/${task.id}: empty circuit`).toBe(422);
      const reason = await rejectionOf(empty);
      expect(reason.length, `${chapter}/${task.id}: rejection reason`).toBeGreaterThan(5);
      if (task.spec.mode === "table") expect(reason).toMatch(/Схема совпала с целью в 0 строках из \d+/);
      else expect(reason).toMatch(/^Шаг \d+ из \d+ не пройден/);
      expect(await statusOf(request, token, chapter, task.id), "after a rejection the status is not \"solved\"").not.toBe("ok");
      await solveViaApi(request, token, chapter, task.id);
      expect(await statusOf(request, token, chapter, task.id)).toBe("ok");
      count++;
    }
  }
  expect(count).toBe(95); // chapters 6–14; 8 more are Mini-8 assembly in chapter 15
});

test("server: invalid solutions are rejected with a clear reason", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "arch-bad");
  const bad = async (chapter: number, id: string, body: string) => {
    const res = await putSolved(request, token, chapter, id, body);
    expect(res.status(), `${chapter}/${id}: ${body.slice(0, 40)}`).toBe(422);
    return rejectionOf(res);
  };
  expect(await bad(6, "not", "это не JSON")).toMatch(/^не JSON/);
  expect(await bad(6, "not", "")).toMatch(/^не JSON/);
  // wrong solution shape: gates expect {gates, wires}, blocks expect {instances, bus_wires}
  expect(await bad(6, "not", emptyDrawing("blocks"))).toMatch(/Ожидалась схема из вентилей/);
  await solveBefore(request, token, 14, "decode-bus");
  expect(await bad(14, "decode-bus", emptyDrawing("gates"))).toMatch(/Ожидалась схема из блоков/);
  // an element outside the exercise palette
  const and = JSON.stringify({ gates: [{ id: "g", type: "AND", x: 1, y: 1 }], wires: [] });
  expect(await bad(6, "not", and)).toBe("Элемент AND недоступен в этом упражнении");
  // a solution of another exercise: OR instead of AND
  expect(await bad(6, "and", solutionText(circuitOf(6, "or")))).toBe("Элемент OR недоступен в этом упражнении");
  // someone else's exercise and a request without a token
  expect((await putSolved(request, token, 6, "nope", "{}")).status()).toBe(404);
  const anonymous = await request.put("/api/exercises/14/6/not/solved", { data: { solution: "{}" } });
  expect(anonymous.status()).toBe(401);
});

// Composite elements (XOR, XNOR, NAND, DFF) are locked in the UI until the student builds them; the server does not check this:
// a solution with a locked XNOR is accepted directly through the API. The test is strict — it is marked fixme until the defect is fixed.
test("server: a solution with a locked composite element (XNOR before XOR is built) is rejected", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "arch-lock");
  const xnor = {
    gates: [{ id: "g_x", type: "XNOR", x: 150, y: 12 }],
    wires: [
      { id: "w1", from: { node: "A", pin: "out" }, to: { node: "g_x", pin: "in0" } },
      { id: "w2", from: { node: "B", pin: "out" }, to: { node: "g_x", pin: "in1" } },
      { id: "w3", from: { node: "g_x", pin: "out" }, to: { node: "Q", pin: "in0" } },
    ],
  };
  const res = await putSolved(request, token, 6, "equals", JSON.stringify(xnor));
  expect(res.status(), "XNOR is unlocked only by a solved Exclusive OR").toBe(422);
});

/* ——— gate board: by hand ——— */

/** Auto-wiring is off (setting `cs-core-autowire-lab`): wires are placed by hand only. */
async function noAutowire(page: Page) {
  await page.addInitScript(() => window.localStorage.setItem("cs-core-autowire-lab", "0"));
}

/** Dragging a wire from pin to pin. */
async function dragWire(page: Page, from: ReturnType<Page["locator"]>, to: ReturnType<Page["locator"]>) {
  const a = await centerOf(from);
  const b = await centerOf(to);
  await page.mouse.move(a.x, a.y);
  await page.mouse.down();
  await page.mouse.move(b.x, b.y, { steps: 6 });
  await expect(page.locator(".wire-preview.ok")).toHaveCount(1); // the wire is dragged and "sees" a suitable pin
  await page.mouse.up();
  await expect(page.locator(".wire-preview")).toHaveCount(0);
}

/** Click on a pin, then on another: the wire "sticks" to the cursor. */
async function clickWire(page: Page, from: ReturnType<Page["locator"]>, to: ReturnType<Page["locator"]>) {
  await clickCenter(page, from);
  await expect(page.locator(".wire-preview")).toHaveCount(1);
  await clickCenter(page, to);
  await expect(page.locator(".wire-preview")).toHaveCount(0);
}

test("board: an inverter is built by hand — palette, wires by drag and by clicks, deletion, toggle, the server accepts", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-hand");
  await noAutowire(page);
  const task = circuitOf(6, "not");
  await openTask(page, request, 6, task.id);

  // palette: the exercise's allowed elements (NOT, NOR); while the board is empty the circuit does not work
  const palette = page.getByRole("toolbar", { name: /^Элементы/ });
  await expect(palette.getByRole("button")).toHaveCount(2);
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".lab-tt .bad-mark, .lab-tt .na-mark").first()).toBeVisible();

  // add a NOT element by clicking the palette
  await palette.getByRole("button", { name: "Добавить элемент NOT, НЕ" }).click();
  await expect(page.locator(".gate")).toHaveCount(1);
  const inA = page.locator(".input-node .pin-hit").first();
  const outY = page.locator(".out-node .pin-hit").first();
  const gateIn = page.locator(".gate .pin-hit").nth(0);
  const gateOut = page.locator(".gate .pin-hit").nth(1);

  // a wire by dragging: A → NOT input; clicking the wire deletes it
  await dragWire(page, inA, gateIn);
  await expect(page.locator(".wire")).toHaveCount(1);
  await page.locator(".wire-hit").first().click({ force: true });
  await expect(page.locator(".wire")).toHaveCount(0);

  // the same wire by two clicks on pins; NOT output → output Y by dragging
  await clickWire(page, inA, gateIn);
  await expect(page.locator(".wire")).toHaveCount(1);
  await expect(page.locator(".pr-item.on")).not.toHaveClass(/\bok\b/);
  await dragWire(page, gateOut, outY);
  await expect(page.locator(".wire")).toHaveCount(2);

  // the circuit works: the table matched, success banner, exercise solved, the server accepted
  await expect(page.locator(".lab-tt tbody tr .ok-mark")).toHaveCount(2);
  const solvedTask = { ...task, title: task.title };
  await expectCircuitSolved(page, request, token, 6, solvedTask);

  // toggle: A = 1 → output Y = 0, the table row with A = 1 is highlighted
  const chip = page.locator(".input-node .node-chip-text");
  const outChip = page.locator(".out-node .node-chip-text");
  await expect(chip).toHaveText("0");
  await expect(outChip).toHaveText("1");
  await expect(page.locator(".lab-tt tbody tr.current")).toHaveCount(1);
  await clickCenter(page, page.locator(".input-node .node-click"));
  await expect(chip).toHaveText("1");
  await expect(outChip).toHaveText("0");
  await expect(page.locator(".lab-tt tbody tr").nth(1)).toHaveClass(/current/);
  await clickCenter(page, page.locator(".input-node .node-click"));
  await expect(outChip).toHaveText("1");

  // the solution is saved as a draft and comes back after a reload
  const state = await chapterState(request, token, 6);
  const draft = JSON.parse(state.drafts["not"] ?? "{}") as { gates: { type: string }[]; wires: unknown[] };
  expect(draft.gates.map((g) => g.type)).toEqual(["NOT"]);
  expect(draft.wires).toHaveLength(2);
  await page.reload();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).toHaveCount(2);
  guard.assertClean();
});

test("board: an element is dragged from the palette onto the field, moves, and is deleted together with its wires", async ({ page, request, guard }) => {
  await loginFresh(page, request, "arch-drag");
  await noAutowire(page);
  await openTask(page, request, 6, "and");
  const button = page.getByRole("button", { name: "Добавить элемент AND, И" });
  const svg = page.locator(".lab-board-svg");
  const from = await centerOf(button);
  const box = (await svg.boundingBox())!;
  // drag from the palette onto the field: a "ghost" under the cursor, the element lands where released
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.5, { steps: 8 });
  await expect(page.locator(".lab-ghost")).toHaveCount(1);
  await page.mouse.up();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".lab-ghost")).toHaveCount(0);
  const before = await page.locator(".gate").getAttribute("transform");

  // move the element by its body
  const body = await centerOf(page.locator(".gate .gate-body"));
  await page.mouse.move(body.x, body.y);
  await page.mouse.down();
  await page.mouse.move(body.x + 90, body.y + 50, { steps: 5 });
  await page.mouse.up();
  const after = await page.locator(".gate").getAttribute("transform");
  expect(after).not.toBe(before);

  // wires to the element, then delete the element — the wires go with it
  await dragWire(page, page.locator(".input-node .pin-hit").nth(0), page.locator(".gate .pin-hit").nth(0));
  await dragWire(page, page.locator(".input-node .pin-hit").nth(1), page.locator(".gate .pin-hit").nth(1));
  await expect(page.locator(".wire")).toHaveCount(2);
  await clickCenter(page, page.locator(".gate .gate-del circle"));
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".wire")).toHaveCount(0);

  // only an output can be connected to an input: output to output is refused, and a note below the board explains why
  await page.getByRole("button", { name: "Добавить элемент AND, И" }).click();
  await clickWire(page, page.locator(".input-node .pin-hit").nth(0), page.locator(".gate .pin-hit").nth(2));
  await expect(page.locator(".lab-flash")).toContainText("Соединять нужно выход элемента со входом другого");
  await expect(page.locator(".wire")).toHaveCount(0);
  guard.assertClean();
});

test("board: auto-wiring suggests links with dashes and places them on release; the setting turns it off", async ({ page, request, guard }) => {
  await loginFresh(page, request, "arch-auto");
  await openTask(page, request, 6, "and"); // the setting is on by default
  const button = page.getByRole("button", { name: "Добавить элемент AND, И" });
  const box = (await page.locator(".lab-board-svg").boundingBox())!;
  const k = box.width / 880; // board units per pixel
  const from = await centerOf(button);
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move(box.x + 300 * k, box.y + 190 * k, { steps: 8 });
  await expect(page.locator(".wire-auto")).not.toHaveCount(0); // suggested links are dashed
  await page.mouse.up();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).not.toHaveCount(0); // and placed
  await expect(page.locator(".wire-auto")).toHaveCount(0);

  // turn auto-wiring off in the settings → the element lands without wires
  await page.evaluate(() => window.localStorage.setItem("cs-core-autowire-lab", "0"));
  await openTask(page, request, 6, "and");
  await page.getByRole("button", { name: "Добавить элемент AND, И" }).click();
  const from2 = await centerOf(page.getByRole("button", { name: "Добавить элемент AND, И" }));
  await page.mouse.move(from2.x, from2.y);
  await page.mouse.down();
  await page.mouse.move(box.x + 300 * k, box.y + 190 * k, { steps: 8 });
  await expect(page.locator(".wire-auto")).toHaveCount(0);
  await page.mouse.up();
  await expect(page.locator(".wire")).toHaveCount(0);
  guard.assertClean();
});

test("board: pan, zoom (buttons and Ctrl + wheel), reset and board height", async ({ page, request, guard }) => {
  await loginFresh(page, request, "arch-zoom");
  await openTask(page, request, 6, "and");
  const svg = page.locator(".lab-board-svg");
  const view = async () => ((await svg.getAttribute("viewBox")) ?? "").split(" ").map(Number) as [number, number, number, number];
  const pct = page.locator(".lab-zoom .pct");
  const [, , w0] = await view();
  await expect(pct).toHaveText("100%");

  await page.getByRole("button", { name: "+", exact: true }).click();
  await expect(pct).toHaveText("125%");
  expect((await view())[2]).toBeCloseTo(w0 / 1.25, 0);
  await page.getByRole("button", { name: "−", exact: true }).click();
  await page.getByRole("button", { name: "−", exact: true }).click();
  await expect(pct).toHaveText("80%");
  expect((await view())[2]).toBeCloseTo(w0 / 0.8, 0);
  await pct.click(); // reset zoom
  await expect(pct).toHaveText("100%");

  // pan by dragging the background
  const [x0, y0] = await view();
  const box = (await svg.boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width / 2 + 60, box.y + box.height / 2 + 40, { steps: 4 });
  await page.mouse.up();
  const [x1, y1] = await view();
  expect([x1, y1]).not.toEqual([x0, y0]);

  // Ctrl + wheel zooms around the cursor
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.keyboard.down("Control");
  await page.mouse.wheel(0, -300);
  await page.keyboard.up("Control");
  await expect(pct).not.toHaveText("100%");

  // "⌖" returns the board to its place and 100 % zoom
  await page.getByRole("button", { name: "⌖" }).click();
  await expect(pct).toHaveText("100%");
  expect(await view()).toEqual([0, 0, w0, (await view())[3]]);

  // height grip: the down/up arrows change the field height, a double click restores the default
  const grip = page.getByRole("separator", { name: /Высота доски/ });
  const h0 = (await svg.boundingBox())!.height;
  await grip.focus();
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");
  await expect.poll(async () => (await svg.boundingBox())!.height).toBeGreaterThan(h0 + 30);
  await grip.dblclick();
  await expect.poll(async () => Math.round((await svg.boundingBox())!.height)).toBe(Math.round(h0));
  guard.assertClean();
});

test("board: a locked composite element shows a hint on what to build; after solving Exclusive OR it unlocks", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-lock-ui");
  await openTask(page, request, 6, "equals");
  const xnor = page.getByRole("button", { name: /Добавить элемент XNOR/ });
  await expect(xnor.locator(".lab-pal-lock")).toBeVisible();
  await expect(xnor).toHaveAttribute("title", "Соберите «Исключающее ИЛИ» (практика «Простые схемы»)");
  // click on a locked one: a message under the board and an expanded hint with a lock mark; the element does not appear
  await xnor.dispatchEvent("pointerdown");
  await expect(page.locator(".lab-flash")).toContainText("и элемент откроется");
  await expect(page.locator(".ex-hint")).toContainText("🔒 Соберите «Исключающее ИЛИ»");
  await expect(page.locator(".gate")).toHaveCount(0);
  // the hint button collapses the text
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  await solveBefore(request, token, 6, "equals"); // "xor" and all previous ones are solved
  await openTask(page, request, 6, "equals");
  await expect(page.getByRole("button", { name: /Добавить элемент XNOR/ }).locator(".lab-pal-lock")).toHaveCount(0);
  await page.getByRole("button", { name: /Добавить элемент XNOR/ }).click();
  await expect(page.locator(".gate")).toHaveCount(1);
  guard.assertClean();
});

test("board: exercise hint; Clear erases the circuit and the draft", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-clear");
  const task = circuitOf(6, "and");
  // an incomplete circuit (without the last wire): the exercise is not solved, it can be erased
  await putDraft(request, token, 6, task.id, withoutLastWire(task));
  await openTask(page, request, 6, task.id);
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).toHaveCount(2);

  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText(task.hint.slice(0, 30));
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  // Clear — an empty board, no matches in the table
  await page.getByRole("button", { name: "Очистить" }).first().click();
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".wire")).toHaveCount(0);
  await expect(page.locator(".lab-alert")).toHaveCount(0);
  await expect(page.locator(".lab-tt tbody tr .ok-mark")).toHaveCount(0);
  // an exercise not solved on the server: the clean board is saved as a draft
  await expect
    .poll(async () => (JSON.parse((await chapterState(request, token, 6)).drafts["and"] ?? "{}") as { gates?: unknown[] }).gates?.length)
    .toBe(0);
  expect(await statusOf(request, token, 6, "and")).not.toBe("ok");
  guard.assertClean();
});

/* ——— scenarios and clock ——— */

test("scenario: clock generator (single tick and auto), edge counter, timing diagram", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-clock");
  await solveBefore(request, token, 10, "dff");
  const task = circuitOf(10, "dff");
  await putDraft(request, token, 10, task.id, solutionText(task));
  await openTask(page, request, 10, task.id);
  const clock = page.getByRole("group", { name: "Тактовый генератор" });
  await expect(clock.locator(".lab-edges")).toHaveText("тактов: 0");
  const one = clock.getByRole("button", { name: "Такт ▸" });
  await one.click();
  await expect(clock.locator(".lab-edges")).toHaveText("тактов: 1");
  await expect(one).toBeDisabled(); // the pulse is still going: CLK is high
  await expect(one).toBeEnabled(); // it went low

  // the timing diagram grows by columns, Clear erases it
  const wave = page.locator(".lab-wave");
  await expect(wave.locator(".wave-grid")).not.toHaveCount(0);
  await expect(wave.locator(".wave-row")).not.toHaveCount(0);
  await page.locator(".lab-card", { has: wave }).getByRole("button", { name: "Очистить" }).click();
  await expect(wave.locator(".wave-grid")).toHaveCount(0);

  // auto generator: 4 Hz, edges accumulate, pause stops it
  await clock.getByRole("combobox", { name: "Частота генератора" }).selectOption("4");
  const auto = clock.getByRole("button", { name: /Авто/ });
  await auto.click();
  await expect(clock.getByRole("button", { name: /Пауза/ })).toBeVisible();
  await expect.poll(async () => Number(((await clock.locator(".lab-edges").textContent()) ?? "").replace(/\D/g, ""))).toBeGreaterThanOrEqual(4);
  await clock.getByRole("button", { name: /Пауза/ }).click();
  await expect(auto).toBeVisible();
  const frozen = await clock.locator(".lab-edges").textContent();
  await expect(clock.locator(".lab-edges")).toHaveText(frozen ?? "");
  guard.assertClean();
});

test("scenario: steps are marked as they are done, output values are highlighted", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-steps");
  await solveBefore(request, token, 8, "sr-nor");
  const task = circuitOf(8, "sr-nor");
  await putDraft(request, token, 8, task.id, solutionText(task));
  await openTask(page, request, 8, task.id);
  const steps = page.locator(".lab-step");
  await expect(steps).toHaveCount(4);
  await expect(steps.nth(0)).toHaveClass(/active/);
  await expect(page.locator(".lab-card-head .lab-badge", { hasText: "Шаг 1 / 4" })).toBeVisible();
  // toggles are labelled as in the statement (R, S), the first step requires S = 1
  await expect(page.locator(".input-node .node-label")).toHaveText(["R", "S"]);
  await clickCenter(page, page.locator(".input-node").nth(1).locator(".node-click"));
  await expect(steps.nth(0)).toHaveClass(/done/);
  await expect(steps.nth(0).locator(".lab-step-no")).toHaveText("✓");
  await expect(steps.nth(1)).toHaveClass(/active/);
  await expect(page.locator(".lab-card-head .lab-badge", { hasText: "Шаг 2 / 4" })).toBeVisible();
  await expect(page.locator(".lab-alert")).toHaveCount(0); // the scenario is not finished yet
  guard.assertClean();
});

/* ——— blocks (chapter 14) ——— */

test("blocks: locked blocks with a hint, adding, deleting with the × button, Clear", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-blocks");
  await openTask(page, request, 14, "decode-bus");
  const items = page.locator(".lab-block-item");
  await expect(items).toHaveCount(2);
  await expect(items.first()).toHaveClass(/locked/);
  await items.first().click();
  await expect(page.locator(".lab-flash")).toContainText("Решите «ПЗУ с программой»");
  await expect(page.locator(".lab-flash")).toContainText("и блок откроется");
  await expect(page.locator(".bbox:not(.top)")).toHaveCount(0);

  await solveBefore(request, token, 14, "decode-bus");
  await openTask(page, request, 14, "decode-bus");
  await expect(items.first()).not.toHaveClass(/locked/);
  await items.nth(0).click();
  await items.nth(1).click();
  await expect(page.locator(".bbox:not(.top) .bbox-title")).toHaveText(["ROM with a program", "Instruction decoder"]);

  // remove one block from the board with the × button
  await page.locator(".bbox:not(.top)").nth(1).locator(".bbtn.del").click();
  await expect(page.locator(".bbox:not(.top) .bbox-title")).toHaveText(["ROM with a program"]);

  // Clear removes the blocks from the board
  await page.getByRole("button", { name: "Очистить" }).first().click();
  await expect(page.locator(".bbox:not(.top)")).toHaveCount(0);
  guard.assertClean();
});

// The magnifier button (look inside) on a block does nothing: `CircuitLab` does not pass `on_inspect` to `BlockBoard`, and `inspect_path`
// never becomes non-empty, so `Inspector` is unreachable. The test is strict — marked fixme until fixed.
test("blocks: the magnifier on a block opens the circuit inside the block (view only) with Back", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "arch-inspect");
  await solveBefore(request, token, 14, "decode-bus");
  await openTask(page, request, 14, "decode-bus");
  await page.locator(".lab-block-item").first().click();
  await page.locator(".bbtn.inspect").first().click();
  await expect(page.locator(".lab-inspector")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Где вы находитесь" })).toContainText("ROM with a program");
});
