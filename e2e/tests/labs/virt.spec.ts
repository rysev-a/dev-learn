import type { Locator, Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { labTask, listItem, openTask, progressLabel, putSolved, statusOf, expectStatusOk } from "../../support/labs";

/* Лаборатория «Виртуализация» (книга 17): шесть симуляторов. Решение — JSON `{id цели: данные}`, которое строит сам интерфейс;
   у этих упражнений в данных нет эталона, поэтому решаются действиями в интерфейсе, а присланное решение затем
   воспроизводится другим учеником через API (серверная перепроверка моделью). */

test.use({ viewport: { width: 1400, height: 1500 } });

/** Симулятор → глава и id упражнения. */
const SIM = {
  hv: [2, "virt-sim-hv"],
  ept: [4, "virt-sim-ept"],
  virtq: [6, "virt-sim-virtqueue"],
  qcow2: [9, "virt-sim-qcow2"],
  migration: [10, "virt-sim-migration"],
  numa: [11, "virt-sim-numa"],
} as const;
type Sim = keyof typeof SIM;

// --- помощники --------------------------------------------------------------------------------------------

const goalItems = (page: Page) => page.locator(".vl-goals li");
const tabs = (page: Page) => page.locator(".vl-tab");
const badge = (page: Page) => page.locator(".pr-head .pr-badge");

async function open(page: Page, request: Parameters<typeof openTask>[1], sim: Sim) {
  const [chapter, id] = SIM[sim];
  await openTask(page, request, "virt", chapter, id);
  await expect(page.locator(".vl")).toBeVisible();
}

/** Решение, которое интерфейс отправит на сервер (перехватывается запрос, ответ сервера не подменяется). */
function solutionRequest(page: Page, sim: Sim) {
  const [, id] = SIM[sim];
  return page.waitForRequest((r) => r.url().endsWith(`/${id}/solved`) && r.method() === "PUT");
}
const solutionOf = (r: { postData(): string | null }) => (JSON.parse(r.postData() ?? "{}") as { solution: string }).solution;

/** Все цели упражнения выполнены в интерфейсе и записаны на сервере. */
async function expectSolved(page: Page, request: Parameters<typeof openTask>[1], token: string, sim: Sim) {
  const [chapter, id] = SIM[sim];
  const task = labTask("virt", chapter, id);
  await expect(badge(page)).toHaveText("выполнено");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expect(progressLabel(page)).toHaveText(/^Решено 1 из \d+$/);
  await expectStatusOk(request, token, "virt", chapter, id);
}

/**
 * Решение, присланное интерфейсом, принимает сервер и у другого ученика: после этого страница открывается решённой.
 * Затем решение портится `spoil` — сервер обязан отказать с причиной, содержащей `reason`.
 */
async function replayForAnotherUser(page: Page, request: Parameters<typeof openTask>[1], sim: Sim, solution: string, spoil: (s: Record<string, unknown>) => void, reason: RegExp) {
  const [chapter, id] = SIM[sim];
  const other = await loginFresh(page, request, `virt-${sim}`);
  const bad = JSON.parse(solution) as Record<string, unknown>;
  spoil(bad);
  const refused = await putSolved(request, other.token, "virt", chapter, id, JSON.stringify(bad));
  expect(refused.status, `испорченное решение ${sim}`).toBe(422);
  expect(refused.detail).toMatch(reason);
  expect(await statusOf(request, other.token, "virt", chapter, id)).toBeUndefined();

  expect((await putSolved(request, other.token, "virt", chapter, id, solution)).status).toBe(204);
  expect(await statusOf(request, other.token, "virt", chapter, id)).toBe("ok");
  await page.goto("about:blank");
  await openTask(page, request, "virt", chapter, id);
  await expect(badge(page)).toHaveText("выполнено");
  // решённое упражнение показывает все цели достигнутыми
  const marks = page.locator(".vl-goals li.ok, .vl-tab.ok");
  expect(await marks.count()).toBeGreaterThan(0);
  await expect(page.locator(".vl-goals li:not(.ok), .vl-tab:not(.ok)")).toHaveCount(0);
}

// --- 0. исходное состояние -----------------------------------------------------------------------------------

test.describe("исходное состояние не засчитывается", () => {
  for (const sim of Object.keys(SIM) as Sim[]) {
    test(`${sim}: цели не достигнуты, на сервере решения нет`, async ({ page, request, guard }) => {
      const [chapter, id] = SIM[sim];
      const { token } = await loginFresh(page, request, `virt-${sim}`);
      await open(page, request, sim);
      await expect(badge(page)).toHaveText("не решено");
      await expect(page.locator(".vl-tab.ok, .vl-goals li.ok")).toHaveCount(0);
      if (sim === "hv" || sim === "migration") await expect(tabs(page)).toHaveCount(3);
      else if (sim === "numa") await expect(tabs(page)).toHaveCount(2);
      else await expect(goalItems(page)).toHaveCount(sim === "ept" ? 4 : 3);
      await expect(page.locator(".pr-list .pr-item.ok")).toHaveCount(0);
      await page.waitForLoadState("networkidle");
      expect(await statusOf(request, token, "virt", chapter, id)).toBeUndefined();
      // пустое решение сервер отклоняет с причиной
      const empty = await putSolved(request, token, "virt", chapter, id, "{}");
      expect(empty.status).toBe(422);
      expect(empty.detail).toContain("цель не достигнута");
      guard.assertClean();
    });
  }
});

// --- 1. мини-гипервизор (глава 2) ----------------------------------------------------------------------------------

/** Верная имитация на ловушке: по заголовку ловушки и виртуальному флагу IF гостя. */
function correctOption(title: string, vif: string): string {
  const num = (re: RegExp) => re.exec(title)?.[1] ?? "";
  if (title.startsWith("CLI")) return "виртуальный флаг vif ← 0";
  if (title.startsWith("STI")) return "vif ← 1 и доставить очередь";
  if (title.startsWith("MOV CR3,")) return `виртуальный vcr3 ← ${num(/MOV CR3, (-?\d+)/)}`;
  if (title.startsWith("MOV acc, CR3")) return "acc ← виртуальный vcr3";
  if (title.startsWith("HLT")) return "остановить виртуальный процессор гостя";
  if (title.startsWith("внешнее прерывание")) return vif === "1" ? "доставить гостю сейчас" : "поставить в очередь";
  if (title.startsWith("POPF")) return `vif ← ${num(/POPF (-?\d+)/)}`;
  throw new Error(`неизвестная ловушка: ${title}`);
}

/** Значение строки таблицы «гость видит». */
const guestCell = (page: Page, name: string) => page.locator(".vl-stat tr", { has: page.locator("td", { hasText: name }) }).locator("td").nth(1);

/** Проходит текущую программу верными вариантами до сообщения «Программа выполнена». */
async function runHvProgram(page: Page) {
  const done = page.locator(".vl-yes", { hasText: "Программа выполнена верно" });
  for (let i = 0; i < 40 && !(await done.isVisible()); i++) {
    const trap = page.locator(".vl-trap-t");
    if (await trap.isVisible()) {
      const title = (await trap.innerText()).replace(/^⚡ Ловушка: /, "");
      const vif = await guestCell(page, "vif").innerText();
      await page.locator(".vl-opt", { hasText: new RegExp(`^${correctOption(title, vif).replace(/[()+*?.|\\^$[\]]/g, "\\$&")}$`) }).click();
    } else {
      await page.getByRole("button", { name: "Шаг", exact: true }).click();
    }
  }
  await expect(done).toBeVisible();
}

test.describe("hv: мини-гипервизор", () => {
  test("три программы проходятся верными имитациями; решение с записью действий принимает сервер", async ({ page, request, guard }) => {
    const [chapter, id] = SIM.hv;
    const { token } = await loginFresh(page, request, "virt-hv");
    await open(page, request, "hv");
    const sent = solutionRequest(page, "hv");

    // программа 1: «Шаг» недоступен на ловушке, неверный вариант объясняется
    await expect(tabs(page).nth(0)).toHaveClass(/\bon\b/);
    await page.getByRole("button", { name: "Шаг", exact: true }).click(); // ADD 3
    await expect(page.locator(".vl-trap-t")).toContainText("CLI");
    await expect(page.getByRole("button", { name: "Шаг", exact: true })).toBeDisabled();
    await page.locator(".vl-opt", { hasText: "выполнить CLI на настоящем процессоре" }).click();
    await expect(page.locator(".vl-no")).toContainText("Нет:");
    await expect(page.locator(".vl-trap-t")).toContainText("CLI");
    await runHvProgram(page);
    await expect(tabs(page).nth(0)).toHaveClass(/\bok\b/);
    await expect(guestCell(page, "vcr3")).toHaveText("4096");
    await expect(page.locator(".vl-log li").first()).toBeVisible();

    // программа 2: прерывания ждут в очереди, пока гость не разрешит
    await tabs(page).nth(1).click();
    await runHvProgram(page);
    await expect(tabs(page).nth(1)).toHaveClass(/\bok\b/);
    await expect(guestCell(page, "доставлено")).toHaveText("1, 2");

    // программа 3: без трансляции POPF «тихая» — программа не проходится; с трансляцией проходится
    await tabs(page).nth(2).click();
    for (let i = 0; i < 20 && !(await page.locator(".vl-no", { hasText: "неверный результат" }).isVisible()); i++) {
      if (await page.locator(".vl-trap-t").isVisible()) {
        const title = (await page.locator(".vl-trap-t").innerText()).replace(/^⚡ Ловушка: /, "");
        await page.locator(".vl-opt", { hasText: new RegExp(`^${correctOption(title, "1").replace(/[()+*?.|\\^$[\]]/g, "\\$&")}$`) }).click();
      } else {
        await page.getByRole("button", { name: "Шаг", exact: true }).click();
      }
    }
    await expect(page.locator(".vl-no", { hasText: "неверный результат" })).toBeVisible();
    await expect(tabs(page).nth(2)).not.toHaveClass(/\bok\b/);
    expect(await statusOf(request, token, "virt", chapter, id)).toBeUndefined();
    await page.getByRole("button", { name: "Сначала" }).click();
    await expect(page.locator(".vl-no")).toHaveCount(0);
    const translate = page.getByLabel("двоичная трансляция", { exact: false });
    await translate.check();
    await runHvProgram(page);
    // трансляцию нельзя менять после запуска
    await expect(translate).toBeDisabled();
    await expect(page.locator(".vl-tab.ok")).toHaveCount(3);

    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "hv");
    const parsed = JSON.parse(solution) as Record<string, { translate: boolean; trace: unknown[] }>;
    expect(Object.keys(parsed).sort()).toEqual(["base", "irq", "popf"]);
    expect(parsed.popf!.translate).toBe(true);
    expect(parsed.base!.trace.length).toBeGreaterThan(5);
    guard.assertClean();

    // та же запись действий у другого ученика: принята; подделка (число ошибок, трансляция) — нет
    await replayForAnotherUser(page, request, "hv", solution, (s) => {
      (s.base as { mistakes: number }).mistakes += 5;
    }, /число ошибок не совпадает/);
    await replayForAnotherUser(page, request, "hv", solution, (s) => {
      (s.popf as { trace: unknown[] }).trace = [];
    }, /popf/);
  });
});

// --- 2. EPT / теневые таблицы (глава 4) -------------------------------------------------------------------------------

test.describe("ept: трансляция адресов", () => {
  test("перебор режимов и размеров страниц достигает всех целей; запуск показывает цену обхода", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-ept");
    await open(page, request, "ept");
    const sent = solutionRequest(page, "ept");
    const [mode, guest, host, workload] = [page.locator(".vl-segbtn"), page.locator(".vl-field select").nth(0), page.locator(".vl-field select").nth(1), page.locator(".vl-field select").nth(2)];

    // формула и сетка обхода зависят от режима и размеров
    await mode.filter({ hasText: "EPT" }).click();
    await expect(page.locator(".pr-res-time")).toHaveText("(4+1)×(4+1)−1");
    await expect(page.locator(".vl-grid2 i")).toHaveCount(25);
    await guest.selectOption("2M");
    await host.selectOption("2M");
    await expect(page.locator(".pr-res-time")).toHaveText("(3+1)×(3+1)−1");
    await mode.filter({ hasText: "теневые" }).click();
    await expect(page.locator(".pr-res-time")).toContainText("уровн");
    await expect(page.locator(".vl-final")).toHaveCount(0);

    // «Один промах TLB» в EPT на страницах 2 МиБ — первая цель (≤ 15 обращений)
    await mode.filter({ hasText: "EPT" }).click();
    await workload.selectOption({ index: 0 });
    await page.getByRole("button", { name: "Запустить нагрузку" }).click();
    await expect(page.locator(".vl-final")).toContainText("цена одного промаха");
    await expect(page.locator(".vl-final tr", { hasText: "цена одного промаха" })).toContainText("15 обращ.");
    await expect(goalItems(page).first()).toHaveClass(/\bok\b/);
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);

    // остальные цели — перебором: для каждой нагрузки все режимы и размеры страниц
    const count = await workload.locator("option").count();
    for (let w = 1; w < count; w++) {
      await workload.selectOption({ index: w });
      for (const m of ["теневые", "EPT"]) {
        await mode.filter({ hasText: m }).click();
        for (const g of ["4K", "2M", "1G"]) {
          for (const h of ["4K", "2M", "1G"]) {
            await guest.selectOption(g);
            await host.selectOption(h);
            await page.getByRole("button", { name: "Запустить нагрузку" }).click();
          }
        }
      }
    }
    await expect(page.locator(".vl-goals li.ok")).toHaveCount(4);
    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "ept");
    const parsed = JSON.parse(solution) as Record<string, { mode: string; workload: string }>;
    expect(Object.keys(parsed).sort()).toEqual(["fork", "random", "scan", "walk"]);
    expect(parsed.walk!.workload).toBe("one");
    guard.assertClean();

    // сервер заново запускает модель: настройки, при которых цель недостижима, отклоняются
    await replayForAnotherUser(page, request, "ept", solution, (s) => {
      const walk = s.walk as { mode: string; guest: string; host: string };
      walk.mode = "shadow";
      walk.guest = "4K";
      walk.host = "4K";
    }, /walk|цель не достигается/);
  });
});

// --- 3. очередь virtio (глава 6) ------------------------------------------------------------------------------------------

test.describe("virtq: очередь virtio", () => {
  test("пачки, переполнение и подавление оповещений; запись действий воспроизводит сервер", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-virtq");
    await open(page, request, "virtq");
    const sent = solutionRequest(page, "virtq");
    const press = (name: string) => page.getByRole("button", { name, exact: true }).click();
    const row = (name: string) => page.locator(".vl-stat tr", { has: page.locator("td", { hasText: name }) }).locator("td").nth(1);

    await expect(page.locator(".pr-res-time")).toHaveText("свободно 8 из 8");
    await press("Устройство: обработать 1");
    await expect(page.locator(".vl-final")).toContainText("Устройство спит");
    // две пачки по 3 без подавления: шесть буферов не больше чем двумя оповещениями
    await press("Гость: положить пачку из 3");
    await expect(page.locator(".pr-res-time")).toHaveText("свободно 5 из 8");
    await expect(page.locator(".vl-desc i.avail")).toHaveCount(3);
    await press("Гость: положить пачку из 3");
    await expect(row("оповещений")).toHaveText(/^[12]$/);
    await expect(goalItems(page).nth(0)).toHaveClass(/\bok\b/);
    // третья пачка не помещается: переполнение
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);
    await press("Гость: положить пачку из 3");
    await expect(page.locator(".vl-final")).toContainText("очередь переполнена");
    await expect(goalItems(page).nth(1)).toHaveClass(/\bok\b/);

    // обработка устройством и сбор готовых освобождают дескрипторы
    await press("Устройство: обработать 1");
    await expect(page.locator(".vl-desc i.used")).toHaveCount(1);
    await press("Гость: забрать готовые");
    await expect(page.locator(".vl-desc i.used")).toHaveCount(0);

    // сброс, подавление и десять буферов двумя оповещениями
    await press("Сбросить");
    await expect(page.locator(".pr-res-time")).toHaveText("свободно 8 из 8");
    const suppress = page.getByLabel("подавление оповещений", { exact: false });
    await suppress.check();
    await expect(goalItems(page).nth(2)).not.toHaveClass(/\bok\b/);
    for (let round = 0; round < 2; round++) {
      await press("Гость: положить пачку из 3");
      await press("Гость: положить пачку из 3");
      for (let i = 0; i < 6; i++) await press("Устройство: обработать 1");
      await press("Гость: забрать готовые");
    }
    await expect(page.locator(".vl-goals li.ok")).toHaveCount(3);
    await expect(row("оповещений")).toHaveText("2");
    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "virtq");
    const parsed = JSON.parse(solution) as Record<string, { trace: { op: string }[] }>;
    expect(Object.keys(parsed).sort()).toEqual(["batch", "overflow", "suppress"]);
    expect(parsed.suppress!.trace.some((a) => a.op === "suppress")).toBe(true);
    guard.assertClean();

    await replayForAnotherUser(page, request, "virtq", solution, (s) => {
      (s.suppress as { trace: unknown[] }).trace = [{ op: "post", n: 1 }];
    }, /suppress/);
  });
});

// --- 4. слои qcow2 (глава 9) ---------------------------------------------------------------------------------------------------

test.describe("qcow2: слои образа", () => {
  test("снимки, глубокое чтение, слияние и откат; запись действий воспроизводит сервер", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-qcow2");
    await open(page, request, "qcow2");
    const sent = solutionRequest(page, "qcow2");
    const press = (name: string) => page.getByRole("button", { name, exact: true }).click();
    const cluster = (n: number) => page.locator(".vl-seg .vl-segbtn", { hasText: new RegExp(`^${n}$`) });
    const layers = page.locator(".vl-layers .vl-layer");

    await expect(page.locator(".pr-res-time")).toHaveText("1 сл.");
    await expect(layers).toHaveCount(1);
    await press("Откатить верхний слой");
    await expect(page.locator(".vl-final")).toContainText("Откат невозможен");

    // три снимка → цепочка из четырёх слоёв; чтение кластера из базы проходит все слои
    for (let i = 0; i < 3; i++) await press("Снимок");
    await expect(page.locator(".pr-res-time")).toHaveText("4 сл.");
    await expect(layers).toHaveCount(4);
    await cluster(0).click();
    await press("Прочитать");
    await expect(page.locator(".vl-final")).toContainText("обращений к таблицам: 4");
    await expect(goalItems(page).nth(0)).toHaveClass(/\bok\b/);

    // слияние дважды: цепочка сокращается до двух слоёв
    await press("Слить верхний слой");
    await expect(layers).toHaveCount(3);
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);
    await press("Слить верхний слой");
    await expect(layers).toHaveCount(2);
    await expect(goalItems(page).nth(1)).toHaveClass(/\bok\b/);

    // откат: запись в верхний слой, откат слоя, чтение — старые данные вернулись
    await page.locator(".vl-field select").selectOption("F");
    await press("Записать");
    await expect(page.locator(".vl-final")).toContainText("копирование при записи");
    await press("Откатить верхний слой");
    await expect(page.locator(".vl-final")).toContainText("Откат: верхний слой с записями отброшен");
    await expect(goalItems(page).nth(2)).not.toHaveClass(/\bok\b/);
    await press("Прочитать");
    await expect(page.locator(".vl-final")).toContainText("Кластер 0 = «A»");
    await expect(page.locator(".vl-goals li.ok")).toHaveCount(3);

    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "qcow2");
    const parsed = JSON.parse(solution) as Record<string, { trace: { op: string }[] }>;
    expect(Object.keys(parsed).sort()).toEqual(["deep", "rollback", "squash"]);
    guard.assertClean();

    await replayForAnotherUser(page, request, "qcow2", solution, (s) => {
      (s.squash as { trace: unknown[] }).trace = [{ op: "snapshot" }];
    }, /squash/);
  });
});

// --- 5. живая миграция (глава 10) ------------------------------------------------------------------------------------------------

test.describe("migration: живая миграция", () => {
  /** Запускает миграцию с параметрами и ждёт вердикта по цели сценария. */
  async function migrate(page: Page, opts: { downtime: number; autoConverge?: boolean; hybridAfter?: number }) {
    await page.locator("input[type=range]").fill(String(opts.downtime));
    const checks = page.locator(".vl-check input[type=checkbox]");
    await checks.nth(0).setChecked(!!opts.autoConverge);
    await checks.nth(2).setChecked(opts.hybridAfter !== undefined);
    if (opts.hybridAfter !== undefined) await page.locator(".vl-check select").selectOption(String(opts.hybridAfter));
    await page.getByRole("button", { name: "Запустить миграцию" }).click();
  }
  const verdict = (page: Page) => page.locator(".vl-final, .vl-card").getByText(/Цель сценария/);

  test("три сценария: параметры подбираются, достижение цели проверяет сервер", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-migration");
    await open(page, request, "migration");
    const sent = solutionRequest(page, "migration");

    // спокойный гость: параметры по умолчанию (простой 300 мс) цели не достигают, с 80 мс — достигают
    await migrate(page, { downtime: 300 });
    await expect(page.locator(".vl-rounds li").first()).toBeVisible();
    await expect(verdict(page)).toContainText("не достигнута");
    await expect(tabs(page).nth(0)).not.toHaveClass(/\bok\b/);
    await migrate(page, { downtime: 80 });
    await expect(verdict(page)).toContainText("достигнута");
    await expect(verdict(page)).not.toContainText("не достигнута");
    await expect(tabs(page).nth(0)).toHaveClass(/\bok\b/);

    // активный гость: нужно притормозить vCPU (auto-converge)
    await tabs(page).nth(1).click();
    await migrate(page, { downtime: 300 });
    await expect(verdict(page)).toContainText("не достигнута");
    await migrate(page, { downtime: 300, autoConverge: true });
    await expect(tabs(page).nth(1)).toHaveClass(/\bok\b/);

    // очень активный: гибрид с переходом на post-copy
    await tabs(page).nth(2).click();
    await migrate(page, { downtime: 80, hybridAfter: 1 });
    await expect(page.locator(".vl-tab.ok")).toHaveCount(3);

    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "migration");
    const parsed = JSON.parse(solution) as Record<string, { downtimeMs: number }>;
    expect(Object.keys(parsed).sort()).toEqual(["busy", "calm", "wild"]);
    expect(parsed.calm!.downtimeMs).toBe(80);
    guard.assertClean();

    await replayForAnotherUser(page, request, "migration", solution, (s) => {
      (s.calm as { downtimeMs: number }).downtimeMs = 1000;
    }, /calm/);
  });
});

// --- 6. размещение по узлам NUMA (глава 11) ------------------------------------------------------------------------------------------

test.describe("numa: размещение машин", () => {
  const rows = (page: Page) => page.locator(".vl-vms tbody tr");
  const place = (row: Locator, what: "cpu" | "mem", node: string) => row.locator("select").nth(what === "cpu" ? 0 : 1).selectOption(node);

  test("размещение принимается только при выполнении цели; сервер оценивает его заново", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-numa");
    await open(page, request, "numa");
    const sent = solutionRequest(page, "numa");
    const accept = () => page.getByRole("button", { name: "Принять размещение" }).click();

    // сценарий 1: по умолчанию машины не размещены как надо — «Принять» отклоняется с причиной
    await expect(rows(page)).toHaveCount(4);
    await accept();
    await expect(page.locator(".vl-no")).not.toHaveText("");
    await expect(tabs(page).nth(0)).not.toHaveClass(/\bok\b/);
    // A и B — на узел 0, C и D — на узел 1 (и процессоры, и память)
    for (const [i, node] of [[0, "0"], [1, "0"], [2, "1"], [3, "1"]] as const) {
      await place(rows(page).nth(i), "cpu", node);
      await place(rows(page).nth(i), "mem", node);
    }
    await expect(page.locator(".vl-stat tr", { hasText: "средняя доля удалённых" })).toContainText("0%");
    await accept();
    await expect(page.locator(".vl-yes")).toContainText("Принято");
    await expect(tabs(page).nth(0)).toHaveClass(/\bok\b/);

    // сценарий 2: большая машина растянута, нужна виртуальная NUMA (без неё доля удалённых больше 20%)
    await tabs(page).nth(1).click();
    await expect(rows(page)).toHaveCount(3);
    await place(rows(page).nth(0), "cpu", "wide");
    await place(rows(page).nth(0), "mem", "wide");
    await place(rows(page).nth(1), "cpu", "0");
    await place(rows(page).nth(1), "mem", "0");
    await place(rows(page).nth(2), "cpu", "1");
    await place(rows(page).nth(2), "mem", "1");
    await accept();
    await expect(page.locator(".vl-no")).toContainText("больше допустимых");
    await expect(tabs(page).nth(1)).not.toHaveClass(/\bok\b/);
    await page.getByLabel("виртуальная топология NUMA", { exact: false }).check();
    await accept();
    await expect(page.locator(".vl-yes")).toContainText("Принято");
    await expect(page.locator(".vl-tab.ok")).toHaveCount(2);

    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "numa");
    const parsed = JSON.parse(solution) as Record<string, Record<string, { vnuma: boolean }>>;
    expect(Object.keys(parsed).sort()).toEqual(["small", "wide"]);
    expect(parsed.wide!.E!.vnuma).toBe(true);
    guard.assertClean();

    // без виртуальной NUMA размещение второго сценария сервер не принимает
    await replayForAnotherUser(page, request, "numa", solution, (s) => {
      for (const p of Object.values(s.wide as Record<string, { vnuma: boolean }>)) p.vnuma = false;
    }, /wide.*удалённых/);
  });

  test("размещение, не помещающееся в узлы, отклоняется с объяснением", async ({ page, request, guard }) => {
    await loginFresh(page, request, "virt-numa");
    await open(page, request, "numa");
    for (let i = 0; i < 4; i++) {
      await place(rows(page).nth(i), "cpu", "0");
      await place(rows(page).nth(i), "mem", "0");
    }
    await page.getByRole("button", { name: "Принять размещение" }).click();
    await expect(page.locator(".vl-no")).toContainText("не помещается");
    await expect(page.locator(".vl-vms")).toBeVisible();
    guard.assertClean();
  });
});

// --- интерфейс отказа сервера ------------------------------------------------------------------------------------------------------

test("интерфейс показывает причину отказа сервера, если решение подменили", async ({ page, request, guard }) => {
  const [chapter, id] = SIM.qcow2;
  const { token } = await loginFresh(page, request, "virt-qcow2");
  await page.route(`**/api/exercises/17/${chapter}/${id}/solved`, (route) => route.continue({ postData: JSON.stringify({ solution: JSON.stringify({ deep: { trace: [] } }) }) }));
  await open(page, request, "qcow2");
  const refused = page.waitForResponse((r) => r.url().endsWith(`/${id}/solved`) && r.request().method() === "PUT");
  const press = (name: string) => page.getByRole("button", { name, exact: true }).click();
  for (let i = 0; i < 3; i++) await press("Снимок");
  await press("Прочитать");
  await press("Слить верхний слой");
  await press("Слить верхний слой");
  await page.locator(".vl-field select").selectOption("F");
  await press("Записать");
  await press("Откатить верхний слой");
  await press("Прочитать");
  expect((await refused).status()).toBe(422);
  await expect(page.locator(".pr-main p.error")).toContainText("Решение не принято");
  await expect(page.locator(".pr-main p.error")).toContainText("цель не достигается");
  await expect(badge(page)).toHaveText("не решено");
  expect(await statusOf(request, token, "virt", chapter, id)).toBeUndefined();
  expect(guard.errors.filter((e) => !/422/.test(e))).toEqual([]);
});
