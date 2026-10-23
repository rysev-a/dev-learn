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

/* Лаборатория схем (книга 14, главы 6–14): вентили и блоки. Эталоны — из данных курса; решения ученика хранятся
   черновиками, а составные блоки открываются решёнными упражнениями, поэтому порядок курса важен. */

const CIRCUIT_CHAPTERS = ARCH_CHAPTERS.filter((c) => c <= 14);
const ALL = process.env["E2E_ARCH_ALL"] === "1";

/** Какие упражнения главы проверяются в интерфейсе: первое, среднее и последнее (все — при E2E_ARCH_ALL=1; главу 14 — целиком). */
function sample(chapter: number): LabTask<CircuitSpec>[] {
  const list = tasksOf(chapter) as LabTask<CircuitSpec>[];
  if (ALL || chapter === 14) return list;
  const picks = new Set([0, Math.floor(list.length / 2), list.length - 1]);
  return list.filter((_, i) => picks.has(i));
}

test.describe("схемы: эталон из черновика засчитывается интерфейсом", () => {
  test.setTimeout(240_000);
  for (const chapter of CIRCUIT_CHAPTERS) {
    test(`глава ${chapter}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "arch");
      const targets = new Set(sample(chapter).map((t) => t.id));
      await solveBefore(request, token, chapter, tasksOf(chapter)[0]!.id);
      for (const task of tasksOf(chapter) as LabTask<CircuitSpec>[]) {
        if (!targets.has(task.id)) {
          await solveViaApi(request, token, chapter, task.id); // для порядка курса: блоки собираются из решённого
          continue;
        }
        await test.step(`${task.id}: ${task.title}`, async () => {
          expect(await statusOf(request, token, chapter, task.id), "до открытия решения нет").not.toBe("ok");
          await putDraft(request, token, chapter, task.id, solutionText(task));
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "steps") {
            await expect(page.locator(".lab-steps .lab-step")).toHaveCount(task.spec.steps.length);
            await playSteps(page, task.spec);
          } else {
            await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          }
          await expectCircuitSolved(page, request, token, chapter, task);
          // решённое упражнение переживает перезагрузку: схема вернулась, статус ✓
          await page.reload();
          await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
        });
      }
      guard.assertClean();
    });
  }
});

/* ——— исходное, пустое и неполное решение ——— */

/** Решение без последнего провода/шины: схема почти готова, но не работает. */
function withoutLastWire(task: LabTask<CircuitSpec>): string {
  const sol = JSON.parse(solutionText(task)) as { wires?: unknown[]; bus_wires?: unknown[] };
  const key = task.spec.build === "gates" ? "wires" : "bus_wires";
  const list = sol[key] ?? [];
  return JSON.stringify({ ...sol, [key]: list.slice(0, -1) });
}

test("схемы: пустая доска и неполная схема не решают упражнение (первое и последнее в каждой главе)", async ({ page, request, guard }) => {
  test.setTimeout(240_000);
  const { token } = await loginFresh(page, request, "arch-neg");
  for (const chapter of CIRCUIT_CHAPTERS) {
    const list = tasksOf(chapter) as LabTask<CircuitSpec>[];
    await solveBefore(request, token, chapter, list[0]!.id);
    for (const task of list) {
      const edge = task === list[0] || task === list[list.length - 1];
      if (edge) {
        await test.step(`${chapter}/${task.id}: пустая доска, затем неполная схема`, async () => {
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "steps") await expect(page.locator(".lab-card-head .lab-badge", { hasText: `Шаг 1 / ${task.spec.steps.length}` })).toBeVisible();
          else await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          await expect(page.locator(".lab-alert")).toHaveCount(0);
          await expect(listItem(page, task.title)).not.toHaveClass(/\bok\b/);
          await expect(page.locator(".pr-head .pr-badge")).not.toHaveText("выполнено");

          // схема без последнего провода: интерфейс не засчитывает (ни пустая, ни почти готовая — сервер ничего не получил)
          await putDraft(request, token, chapter, task.id, withoutLastWire(task));
          await openTask(page, request, chapter, task.id);
          if (task.spec.mode === "table") await expect(page.locator(".lab-tt tbody tr")).toHaveCount(task.spec.target.length);
          await expect(page.locator(".lab-alert")).toHaveCount(0);
          await expect(page.locator(".lab-card-head .lab-badge.ok")).toHaveCount(0);
          expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
          // и сервер на то же решение отвечает отказом с причиной
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

/* ——— сервер: отказы и порядок курса ——— */

test("сервер: эталоны всех упражнений глав 6–14 принимаются в порядке курса, пустая схема отклоняется с причиной", async ({ page, request }) => {
  test.setTimeout(120_000);
  const { token } = await loginFresh(page, request, "arch-api");
  let count = 0;
  for (const chapter of CIRCUIT_CHAPTERS) {
    for (const task of tasksOf(chapter) as LabTask<CircuitSpec>[]) {
      const empty = await putSolved(request, token, chapter, task.id, emptyDrawing(task.spec.build));
      expect(empty.status(), `${chapter}/${task.id}: пустая схема`).toBe(422);
      const reason = await rejectionOf(empty);
      expect(reason.length, `${chapter}/${task.id}: причина отказа`).toBeGreaterThan(5);
      if (task.spec.mode === "table") expect(reason).toMatch(/Схема совпала с целью в 0 строках из \d+/);
      else expect(reason).toMatch(/^Шаг \d+ из \d+ не пройден/);
      expect(await statusOf(request, token, chapter, task.id), "после отказа статус не «выполнено»").not.toBe("ok");
      await solveViaApi(request, token, chapter, task.id);
      expect(await statusOf(request, token, chapter, task.id)).toBe("ok");
      count++;
    }
  }
  expect(count).toBe(95); // главы 6–14; ещё 8 — ассемблер Мини-8 в главе 15
});

test("сервер: некорректные решения отклоняются с понятной причиной", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "arch-bad");
  const bad = async (chapter: number, id: string, body: string) => {
    const res = await putSolved(request, token, chapter, id, body);
    expect(res.status(), `${chapter}/${id}: ${body.slice(0, 40)}`).toBe(422);
    return rejectionOf(res);
  };
  expect(await bad(6, "not", "это не JSON")).toMatch(/^не JSON/);
  expect(await bad(6, "not", "")).toMatch(/^не JSON/);
  // форма решения не та: для вентилей ждут {gates, wires}, для блоков — {instances, bus_wires}
  expect(await bad(6, "not", emptyDrawing("blocks"))).toMatch(/Ожидалась схема из вентилей/);
  await solveBefore(request, token, 14, "decode-bus");
  expect(await bad(14, "decode-bus", emptyDrawing("gates"))).toMatch(/Ожидалась схема из блоков/);
  // элемент вне палитры упражнения
  const and = JSON.stringify({ gates: [{ id: "g", type: "AND", x: 1, y: 1 }], wires: [] });
  expect(await bad(6, "not", and)).toBe("Элемент AND недоступен в этом упражнении");
  // решение другого упражнения: «ИЛИ» вместо «И»
  expect(await bad(6, "and", solutionText(circuitOf(6, "or")))).toBe("Элемент OR недоступен в этом упражнении");
  // чужое упражнение и вход без токена
  expect((await putSolved(request, token, 6, "nope", "{}")).status()).toBe(404);
  const anonymous = await request.put("/api/exercises/14/6/not/solved", { data: { solution: "{}" } });
  expect(anonymous.status()).toBe(401);
});

// Составные элементы (XOR, XNOR, NAND, DFF) в интерфейсе закрыты, пока ученик не соберёт их сам; сервер этого не проверяет:
// решение с закрытым XNOR принимается напрямую через API. Тест строгий — пока дефект не исправлен, он помечен fixme.
test("сервер: решение с закрытым составным элементом (XNOR до сборки XOR) отклоняется", async ({ page, request }) => {
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
  expect(res.status(), "XNOR открывается только решённым «Исключающим ИЛИ»").toBe(422);
});

/* ——— доска из вентилей: руками ——— */

/** Автосвязывание выключено (настройка `say-autowire-lab`): провода ставятся только руками. */
async function noAutowire(page: Page) {
  await page.addInitScript(() => window.localStorage.setItem("say-autowire-lab", "0"));
}

/** Протяжка провода от контакта к контакту. */
async function dragWire(page: Page, from: ReturnType<Page["locator"]>, to: ReturnType<Page["locator"]>) {
  const a = await centerOf(from);
  const b = await centerOf(to);
  await page.mouse.move(a.x, a.y);
  await page.mouse.down();
  await page.mouse.move(b.x, b.y, { steps: 6 });
  await expect(page.locator(".wire-preview.ok")).toHaveCount(1); // провод тянется и «видит» подходящий контакт
  await page.mouse.up();
  await expect(page.locator(".wire-preview")).toHaveCount(0);
}

/** Клик по контакту, затем по другому: провод «прилипает» к курсору. */
async function clickWire(page: Page, from: ReturnType<Page["locator"]>, to: ReturnType<Page["locator"]>) {
  await clickCenter(page, from);
  await expect(page.locator(".wire-preview")).toHaveCount(1);
  await clickCenter(page, to);
  await expect(page.locator(".wire-preview")).toHaveCount(0);
}

test("доска: инвертор собирается руками — палитра, провода протяжкой и кликами, удаление, тумблер, сервер принимает", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-hand");
  await noAutowire(page);
  const task = circuitOf(6, "not");
  await openTask(page, request, 6, task.id);

  // палитра: из допустимых элементов упражнения (НЕ, ИЛИ-НЕ); пока доска пуста — схема не работает
  const palette = page.getByRole("toolbar", { name: /^Элементы/ });
  await expect(palette.getByRole("button")).toHaveCount(2);
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".lab-tt .bad-mark, .lab-tt .na-mark").first()).toBeVisible();

  // добавляем элемент НЕ кликом по палитре
  await palette.getByRole("button", { name: "Добавить элемент NOT, НЕ" }).click();
  await expect(page.locator(".gate")).toHaveCount(1);
  const inA = page.locator(".input-node .pin-hit").first();
  const outY = page.locator(".out-node .pin-hit").first();
  const gateIn = page.locator(".gate .pin-hit").nth(0);
  const gateOut = page.locator(".gate .pin-hit").nth(1);

  // провод протяжкой: A → вход НЕ; клик по проводу его удаляет
  await dragWire(page, inA, gateIn);
  await expect(page.locator(".wire")).toHaveCount(1);
  await page.locator(".wire-hit").first().click({ force: true });
  await expect(page.locator(".wire")).toHaveCount(0);

  // тот же провод двумя кликами по контактам; выход НЕ → выход Y протяжкой
  await clickWire(page, inA, gateIn);
  await expect(page.locator(".wire")).toHaveCount(1);
  await expect(page.locator(".pr-item.on")).not.toHaveClass(/\bok\b/);
  await dragWire(page, gateOut, outY);
  await expect(page.locator(".wire")).toHaveCount(2);

  // схема работает: таблица совпала, плашка успеха, упражнение решено, сервер принял
  await expect(page.locator(".lab-tt tbody tr .ok-mark")).toHaveCount(2);
  const solvedTask = { ...task, title: task.title };
  await expectCircuitSolved(page, request, token, 6, solvedTask);

  // тумблер: A = 1 → выход Y = 0, подсвечена строка таблицы с A = 1
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

  // решение сохранено черновиком и вернётся после перезагрузки
  const state = await chapterState(request, token, 6);
  const draft = JSON.parse(state.drafts["not"] ?? "{}") as { gates: { type: string }[]; wires: unknown[] };
  expect(draft.gates.map((g) => g.type)).toEqual(["NOT"]);
  expect(draft.wires).toHaveLength(2);
  await page.reload();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).toHaveCount(2);
  guard.assertClean();
});

test("доска: элемент из палитры перетаскивается на поле, двигается, удаляется вместе с проводами", async ({ page, request, guard }) => {
  await loginFresh(page, request, "arch-drag");
  await noAutowire(page);
  await openTask(page, request, 6, "and");
  const button = page.getByRole("button", { name: "Добавить элемент AND, И" });
  const svg = page.locator(".lab-board-svg");
  const from = await centerOf(button);
  const box = (await svg.boundingBox())!;
  // тянем с палитры на поле: под курсором «призрак», элемент встаёт там, где отпустили
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.5, { steps: 8 });
  await expect(page.locator(".lab-ghost")).toHaveCount(1);
  await page.mouse.up();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".lab-ghost")).toHaveCount(0);
  const before = await page.locator(".gate").getAttribute("transform");

  // двигаем элемент за тело
  const body = await centerOf(page.locator(".gate .gate-body"));
  await page.mouse.move(body.x, body.y);
  await page.mouse.down();
  await page.mouse.move(body.x + 90, body.y + 50, { steps: 5 });
  await page.mouse.up();
  const after = await page.locator(".gate").getAttribute("transform");
  expect(after).not.toBe(before);

  // провода к элементу, затем удаляем элемент — провода уходят вместе с ним
  await dragWire(page, page.locator(".input-node .pin-hit").nth(0), page.locator(".gate .pin-hit").nth(0));
  await dragWire(page, page.locator(".input-node .pin-hit").nth(1), page.locator(".gate .pin-hit").nth(1));
  await expect(page.locator(".wire")).toHaveCount(2);
  await clickCenter(page, page.locator(".gate .gate-del circle"));
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".wire")).toHaveCount(0);

  // соединять можно только выход со входом: выход с выходом не соединяется, под доской объясняют почему
  await page.getByRole("button", { name: "Добавить элемент AND, И" }).click();
  await clickWire(page, page.locator(".input-node .pin-hit").nth(0), page.locator(".gate .pin-hit").nth(2));
  await expect(page.locator(".lab-flash")).toContainText("Соединять нужно выход элемента со входом другого");
  await expect(page.locator(".wire")).toHaveCount(0);
  guard.assertClean();
});

test("доска: автопроводка предлагает связи пунктиром и ставит их при отпускании; настройка её выключает", async ({ page, request, guard }) => {
  await loginFresh(page, request, "arch-auto");
  await openTask(page, request, 6, "and"); // настройка по умолчанию — включено
  const button = page.getByRole("button", { name: "Добавить элемент AND, И" });
  const box = (await page.locator(".lab-board-svg").boundingBox())!;
  const k = box.width / 880; // единиц доски в пикселе
  const from = await centerOf(button);
  await page.mouse.move(from.x, from.y);
  await page.mouse.down();
  await page.mouse.move(box.x + 300 * k, box.y + 190 * k, { steps: 8 });
  await expect(page.locator(".wire-auto")).not.toHaveCount(0); // предложенные связи — пунктиром
  await page.mouse.up();
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).not.toHaveCount(0); // и поставлены
  await expect(page.locator(".wire-auto")).toHaveCount(0);

  // выключаем автосвязывание в настройках → элемент встаёт без проводов
  await page.evaluate(() => window.localStorage.setItem("say-autowire-lab", "0"));
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

test("доска: сдвиг, масштаб (кнопки и Ctrl + колесо), возврат на место и высота доски", async ({ page, request, guard }) => {
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
  await pct.click(); // сброс масштаба
  await expect(pct).toHaveText("100%");

  // сдвиг перетаскиванием фона
  const [x0, y0] = await view();
  const box = (await svg.boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width / 2 + 60, box.y + box.height / 2 + 40, { steps: 4 });
  await page.mouse.up();
  const [x1, y1] = await view();
  expect([x1, y1]).not.toEqual([x0, y0]);

  // Ctrl + колесо — масштаб вокруг курсора
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.keyboard.down("Control");
  await page.mouse.wheel(0, -300);
  await page.keyboard.up("Control");
  await expect(pct).not.toHaveText("100%");

  // «⌖» возвращает доску на место и масштаб 100 %
  await page.getByRole("button", { name: "⌖" }).click();
  await expect(pct).toHaveText("100%");
  expect(await view()).toEqual([0, 0, w0, (await view())[3]]);

  // «лапка» высоты: стрелки вниз/вверх меняют высоту поля, двойной щелчок возвращает по умолчанию
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

test("доска: закрытый составной элемент — подсказка, что собрать; после решения «Исключающего ИЛИ» он открывается", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-lock-ui");
  await openTask(page, request, 6, "equals");
  const xnor = page.getByRole("button", { name: /Добавить элемент XNOR/ });
  await expect(xnor.locator(".lab-pal-lock")).toBeVisible();
  await expect(xnor).toHaveAttribute("title", "Соберите «Исключающее ИЛИ» (практика «Простые схемы»)");
  // клик по закрытому: сообщение под доской и раскрытая подсказка с пометкой замка; элемент не появляется
  await xnor.dispatchEvent("pointerdown");
  await expect(page.locator(".lab-flash")).toContainText("и элемент откроется");
  await expect(page.locator(".ex-hint")).toContainText("🔒 Соберите «Исключающее ИЛИ»");
  await expect(page.locator(".gate")).toHaveCount(0);
  // кнопка «Подсказка» сворачивает текст
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  await solveBefore(request, token, 6, "equals"); // решены «xor» и все предыдущие
  await openTask(page, request, 6, "equals");
  await expect(page.getByRole("button", { name: /Добавить элемент XNOR/ }).locator(".lab-pal-lock")).toHaveCount(0);
  await page.getByRole("button", { name: /Добавить элемент XNOR/ }).click();
  await expect(page.locator(".gate")).toHaveCount(1);
  guard.assertClean();
});

test("доска: подсказка упражнения, «Очистить» стирает схему и черновик", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-clear");
  const task = circuitOf(6, "and");
  // неполная схема (без последнего провода): упражнение не решено, её можно стереть
  await putDraft(request, token, 6, task.id, withoutLastWire(task));
  await openTask(page, request, 6, task.id);
  await expect(page.locator(".gate")).toHaveCount(1);
  await expect(page.locator(".wire")).toHaveCount(2);

  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText(task.hint.slice(0, 30));
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  // «Очистить» — пустая доска, в таблице ни одного совпадения
  await page.getByRole("button", { name: "Очистить" }).first().click();
  await expect(page.locator(".gate")).toHaveCount(0);
  await expect(page.locator(".wire")).toHaveCount(0);
  await expect(page.locator(".lab-alert")).toHaveCount(0);
  await expect(page.locator(".lab-tt tbody tr .ok-mark")).toHaveCount(0);
  // не решённое сервером упражнение: чистая доска сохраняется черновиком
  await expect
    .poll(async () => (JSON.parse((await chapterState(request, token, 6)).drafts["and"] ?? "{}") as { gates?: unknown[] }).gates?.length)
    .toBe(0);
  expect(await statusOf(request, token, 6, "and")).not.toBe("ok");
  guard.assertClean();
});

/* ——— сценарии и такт ——— */

test("сценарий: тактовый генератор (один такт и авто), счётчик фронтов, временная диаграмма", async ({ page, request, guard }) => {
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
  await expect(one).toBeDisabled(); // импульс ещё идёт: CLK поднят
  await expect(one).toBeEnabled(); // опустился

  // временная диаграмма пополняется столбцами, «Очистить» её стирает
  const wave = page.locator(".lab-wave");
  await expect(wave.locator(".wave-grid")).not.toHaveCount(0);
  await expect(wave.locator(".wave-row")).not.toHaveCount(0);
  await page.locator(".lab-card", { has: wave }).getByRole("button", { name: "Очистить" }).click();
  await expect(wave.locator(".wave-grid")).toHaveCount(0);

  // автогенератор: частота 4 Гц, фронты накапливаются, пауза останавливает
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

test("сценарий: шаги отмечаются по мере выполнения, значения выходов подсвечены", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "arch-steps");
  await solveBefore(request, token, 8, "sr-nor");
  const task = circuitOf(8, "sr-nor");
  await putDraft(request, token, 8, task.id, solutionText(task));
  await openTask(page, request, 8, task.id);
  const steps = page.locator(".lab-step");
  await expect(steps).toHaveCount(4);
  await expect(steps.nth(0)).toHaveClass(/active/);
  await expect(page.locator(".lab-card-head .lab-badge", { hasText: "Шаг 1 / 4" })).toBeVisible();
  // тумблеры подписаны как в условии (R, S), первый шаг требует S = 1
  await expect(page.locator(".input-node .node-label")).toHaveText(["R", "S"]);
  await clickCenter(page, page.locator(".input-node").nth(1).locator(".node-click"));
  await expect(steps.nth(0)).toHaveClass(/done/);
  await expect(steps.nth(0).locator(".lab-step-no")).toHaveText("✓");
  await expect(steps.nth(1)).toHaveClass(/active/);
  await expect(page.locator(".lab-card-head .lab-badge", { hasText: "Шаг 2 / 4" })).toBeVisible();
  await expect(page.locator(".lab-alert")).toHaveCount(0); // сценарий ещё не пройден
  guard.assertClean();
});

/* ——— блоки (глава 14) ——— */

test("блоки: закрытые блоки с подсказкой, добавление, удаление кнопкой ×, «Очистить»", async ({ page, request, guard }) => {
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
  await expect(page.locator(".bbox:not(.top) .bbox-title")).toHaveText(["ПЗУ с программой", "Декодер команд"]);

  // убрать один блок с доски кнопкой ×
  await page.locator(".bbox:not(.top)").nth(1).locator(".bbtn.del").click();
  await expect(page.locator(".bbox:not(.top) .bbox-title")).toHaveText(["ПЗУ с программой"]);

  // «Очистить» убирает блоки с доски
  await page.getByRole("button", { name: "Очистить" }).first().click();
  await expect(page.locator(".bbox:not(.top)")).toHaveCount(0);
  guard.assertClean();
});

// Кнопка-лупа «Заглянуть внутрь» на блоке ничего не делает: `CircuitLab` не передаёт `on_inspect` в `BlockBoard`, а `inspect_path`
// никогда не становится непустым, поэтому `Inspector` недостижим. Тест строгий — до исправления помечен fixme.
test("блоки: лупа на блоке открывает схему внутри блока (только просмотр) с «← Назад»", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "arch-inspect");
  await solveBefore(request, token, 14, "decode-bus");
  await openTask(page, request, 14, "decode-bus");
  await page.locator(".lab-block-item").first().click();
  await page.locator(".bbtn.inspect").first().click();
  await expect(page.locator(".lab-inspector")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Где вы находитесь" })).toContainText("ПЗУ с программой");
});
