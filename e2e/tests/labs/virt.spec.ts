import type { Locator, Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { labTask, listItem, openTask, progressLabel, putSolved, statusOf, expectStatusOk } from "../../support/labs";

/* Virtualization lab (book 17): six simulators (the three oVirt ones are not covered yet). A solution is JSON `{goal id: data}` built by the interface itself;
   these exercises have no reference in the data, so they are solved by actions in the interface, and the submitted solution is then
   replayed by another student through the API (server-side re-check by the model). */

test.use({ viewport: { width: 1400, height: 1500 } });

/** Simulator -> chapter and exercise id. */
const SIM = {
  hv: [2, "virt-sim-hv"],
  ept: [4, "virt-sim-ept"],
  virtq: [6, "virt-sim-virtqueue"],
  qcow2: [9, "virt-sim-qcow2"],
  migration: [10, "virt-sim-migration"],
  numa: [11, "virt-sim-numa"],
} as const;
type Sim = keyof typeof SIM;

// --- helpers --------------------------------------------------------------------------------------------

const goalItems = (page: Page) => page.locator(".vl-goals li");
const tabs = (page: Page) => page.locator(".vl-tab");
const badge = (page: Page) => page.locator(".pr-head .pr-badge");

async function open(page: Page, request: Parameters<typeof openTask>[1], sim: Sim) {
  const [chapter, id] = SIM[sim];
  await openTask(page, request, "virt", chapter, id);
  await expect(page.locator(".vl")).toBeVisible();
}

/** The solution the interface will send to the server (the request is intercepted, the server response is not replaced). */
function solutionRequest(page: Page, sim: Sim) {
  const [, id] = SIM[sim];
  return page.waitForRequest((r) => r.url().endsWith(`/${id}/solved`) && r.method() === "PUT");
}
const solutionOf = (r: { postData(): string | null }) => (JSON.parse(r.postData() ?? "{}") as { solution: string }).solution;

/** All exercise goals are met in the interface and recorded on the server. */
async function expectSolved(page: Page, request: Parameters<typeof openTask>[1], token: string, sim: Sim) {
  const [chapter, id] = SIM[sim];
  const task = labTask("virt", chapter, id);
  await expect(badge(page)).toHaveText("выполнено");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expect(progressLabel(page)).toHaveText(/^Решено 1 из \d+$/);
  await expectStatusOk(request, token, "virt", chapter, id);
}

/**
 * The solution submitted by the interface is also accepted by the server for another student: after that the page opens as solved.
 * Then the solution is corrupted by `spoil`; the server must refuse with a reason containing `reason`.
 */
async function replayForAnotherUser(page: Page, request: Parameters<typeof openTask>[1], sim: Sim, solution: string, spoil: (s: Record<string, unknown>) => void, reason: RegExp) {
  const [chapter, id] = SIM[sim];
  const other = await loginFresh(page, request, `virt-${sim}`);
  const bad = JSON.parse(solution) as Record<string, unknown>;
  spoil(bad);
  const refused = await putSolved(request, other.token, "virt", chapter, id, JSON.stringify(bad));
  expect(refused.status, `corrupted solution ${sim}`).toBe(422);
  expect(refused.detail).toMatch(reason);
  expect(await statusOf(request, other.token, "virt", chapter, id)).toBeUndefined();

  expect((await putSolved(request, other.token, "virt", chapter, id, solution)).status).toBe(204);
  expect(await statusOf(request, other.token, "virt", chapter, id)).toBe("ok");
  await page.goto("about:blank");
  await openTask(page, request, "virt", chapter, id);
  await expect(badge(page)).toHaveText("выполнено");
  // a solved exercise shows all goals as met
  const marks = page.locator(".vl-goals li.ok, .vl-tab.ok");
  expect(await marks.count()).toBeGreaterThan(0);
  await expect(page.locator(".vl-goals li:not(.ok), .vl-tab:not(.ok)")).toHaveCount(0);
}

// --- 0. initial state -----------------------------------------------------------------------------------

test.describe("the initial state is not accepted", () => {
  for (const sim of Object.keys(SIM) as Sim[]) {
    test(`${sim}: goals are not met, no solution on the server`, async ({ page, request, guard }) => {
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
      // the server rejects an empty solution with a reason
      const empty = await putSolved(request, token, "virt", chapter, id, "{}");
      expect(empty.status).toBe(422);
      expect(empty.detail).toContain("цель не достигнута");
      guard.assertClean();
    });
  }
});

// --- 1. mini hypervisor (chapter 2) ----------------------------------------------------------------------------------

/** Correct emulation for a trap: by the trap title and the guest's virtual IF flag. */
function correctOption(title: string, vif: string): string {
  const num = (re: RegExp) => re.exec(title)?.[1] ?? "";
  if (title.startsWith("CLI")) return "виртуальный флаг vif ← 0";
  if (title.startsWith("STI")) return "vif ← 1 и доставить очередь";
  if (title.startsWith("MOV CR3,")) return `виртуальный vcr3 ← ${num(/MOV CR3, (-?\d+)/)}`;
  if (title.startsWith("MOV acc, CR3")) return "acc ← виртуальный vcr3";
  if (title.startsWith("HLT")) return "остановить виртуальный процессор гостя";
  if (title.startsWith("внешнее прерывание")) return vif === "1" ? "доставить гостю сейчас" : "поставить в очередь";
  if (title.startsWith("POPF")) return `vif ← ${num(/POPF (-?\d+)/)}`;
  throw new Error(`unknown trap: ${title}`);
}

/** Value of a row in the "guest sees" table. */
const guestCell = (page: Page, name: string) => page.locator(".vl-stat tr", { has: page.locator("td", { hasText: name }) }).locator("td").nth(1);

/** Runs the current program with correct options until the "Программа выполнена" message. */
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

test.describe("hv: mini hypervisor", () => {
  test("three programs pass with correct emulations; the server accepts the solution with its action log", async ({ page, request, guard }) => {
    const [chapter, id] = SIM.hv;
    const { token } = await loginFresh(page, request, "virt-hv");
    await open(page, request, "hv");
    const sent = solutionRequest(page, "hv");

    // program 1: "Шаг" is unavailable on a trap, a wrong option is explained
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

    // program 2: interrupts wait in the queue until the guest allows them
    await tabs(page).nth(1).click();
    await runHvProgram(page);
    await expect(tabs(page).nth(1)).toHaveClass(/\bok\b/);
    await expect(guestCell(page, "доставлено")).toHaveText("1, 2");

    // program 3: without translation POPF is silent and the program fails; with translation it passes
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
    // translation cannot be changed after the start
    await expect(translate).toBeDisabled();
    await expect(page.locator(".vl-tab.ok")).toHaveCount(3);

    const solution = solutionOf(await sent);
    await expectSolved(page, request, token, "hv");
    const parsed = JSON.parse(solution) as Record<string, { translate: boolean; trace: unknown[] }>;
    expect(Object.keys(parsed).sort()).toEqual(["base", "irq", "popf"]);
    expect(parsed.popf!.translate).toBe(true);
    expect(parsed.base!.trace.length).toBeGreaterThan(5);
    guard.assertClean();

    // the same action log for another student: accepted; a forgery (error count, translation) is not
    await replayForAnotherUser(page, request, "hv", solution, (s) => {
      (s.base as { mistakes: number }).mistakes += 5;
    }, /число ошибок не совпадает/);
    await replayForAnotherUser(page, request, "hv", solution, (s) => {
      (s.popf as { trace: unknown[] }).trace = [];
    }, /popf/);
  });
});

// --- 2. EPT / shadow tables (chapter 4) -------------------------------------------------------------------------------

test.describe("ept: address translation", () => {
  test("trying modes and page sizes reaches all goals; a run shows the walk cost", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-ept");
    await open(page, request, "ept");
    const sent = solutionRequest(page, "ept");
    const [mode, guest, host, workload] = [page.locator(".vl-segbtn"), page.locator(".vl-field select").nth(0), page.locator(".vl-field select").nth(1), page.locator(".vl-field select").nth(2)];

    // the formula and the walk grid depend on the mode and sizes
    await mode.filter({ hasText: "EPT" }).click();
    await expect(page.locator(".pr-res-time")).toHaveText("(4+1)×(4+1)−1");
    await expect(page.locator(".vl-grid2 i")).toHaveCount(25);
    await guest.selectOption("2M");
    await host.selectOption("2M");
    await expect(page.locator(".pr-res-time")).toHaveText("(3+1)×(3+1)−1");
    await mode.filter({ hasText: "теневые" }).click();
    await expect(page.locator(".pr-res-time")).toContainText("уровн");
    await expect(page.locator(".vl-final")).toHaveCount(0);

    // "one TLB miss" in EPT on 2 MiB pages is the first goal (<= 15 accesses)
    await mode.filter({ hasText: "EPT" }).click();
    await workload.selectOption({ index: 0 });
    await page.getByRole("button", { name: "Запустить нагрузку" }).click();
    await expect(page.locator(".vl-final")).toContainText("цена одного промаха");
    await expect(page.locator(".vl-final tr", { hasText: "цена одного промаха" })).toContainText("15 обращ.");
    await expect(goalItems(page).first()).toHaveClass(/\bok\b/);
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);

    // the remaining goals by brute force: for each workload, all modes and page sizes
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

    // the server reruns the model: settings that make the goal unreachable are rejected
    await replayForAnotherUser(page, request, "ept", solution, (s) => {
      const walk = s.walk as { mode: string; guest: string; host: string };
      walk.mode = "shadow";
      walk.guest = "4K";
      walk.host = "4K";
    }, /walk|цель не достигается/);
  });
});

// --- 3. virtio queue (chapter 6) ------------------------------------------------------------------------------------------

test.describe("virtq: virtio queue", () => {
  test("batches, overflow and notification suppression; the server replays the action log", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-virtq");
    await open(page, request, "virtq");
    const sent = solutionRequest(page, "virtq");
    const press = (name: string) => page.getByRole("button", { name, exact: true }).click();
    const row = (name: string) => page.locator(".vl-stat tr", { has: page.locator("td", { hasText: name }) }).locator("td").nth(1);

    await expect(page.locator(".pr-res-time")).toHaveText("свободно 8 из 8");
    await press("Устройство: обработать 1");
    await expect(page.locator(".vl-final")).toContainText("Устройство спит");
    // two batches of 3 without suppression: six buffers with at most two notifications
    await press("Гость: положить пачку из 3");
    await expect(page.locator(".pr-res-time")).toHaveText("свободно 5 из 8");
    await expect(page.locator(".vl-desc i.avail")).toHaveCount(3);
    await press("Гость: положить пачку из 3");
    await expect(row("оповещений")).toHaveText(/^[12]$/);
    await expect(goalItems(page).nth(0)).toHaveClass(/\bok\b/);
    // the third batch does not fit: overflow
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);
    await press("Гость: положить пачку из 3");
    await expect(page.locator(".vl-final")).toContainText("очередь переполнена");
    await expect(goalItems(page).nth(1)).toHaveClass(/\bok\b/);

    // device processing and collecting completed buffers free the descriptors
    await press("Устройство: обработать 1");
    await expect(page.locator(".vl-desc i.used")).toHaveCount(1);
    await press("Гость: забрать готовые");
    await expect(page.locator(".vl-desc i.used")).toHaveCount(0);

    // reset, suppression and ten buffers with two notifications
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

// --- 4. qcow2 layers (chapter 9) ---------------------------------------------------------------------------------------------------

test.describe("qcow2: image layers", () => {
  test("snapshots, deep read, merge and rollback; the server replays the action log", async ({ page, request, guard }) => {
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

    // three snapshots -> a chain of four layers; reading a cluster from the base walks all layers
    for (let i = 0; i < 3; i++) await press("Снимок");
    await expect(page.locator(".pr-res-time")).toHaveText("4 сл.");
    await expect(layers).toHaveCount(4);
    await cluster(0).click();
    await press("Прочитать");
    await expect(page.locator(".vl-final")).toContainText("обращений к таблицам: 4");
    await expect(goalItems(page).nth(0)).toHaveClass(/\bok\b/);

    // merge twice: the chain shrinks to two layers
    await press("Слить верхний слой");
    await expect(layers).toHaveCount(3);
    await expect(goalItems(page).nth(1)).not.toHaveClass(/\bok\b/);
    await press("Слить верхний слой");
    await expect(layers).toHaveCount(2);
    await expect(goalItems(page).nth(1)).toHaveClass(/\bok\b/);

    // rollback: write to the top layer, roll the layer back, read; the old data is back
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

// --- 5. live migration (chapter 10) ------------------------------------------------------------------------------------------------

test.describe("migration: live migration", () => {
  /** Starts a migration with the parameters and waits for the verdict on the scenario goal. */
  async function migrate(page: Page, opts: { downtime: number; autoConverge?: boolean; hybridAfter?: number }) {
    await page.locator("input[type=range]").fill(String(opts.downtime));
    const checks = page.locator(".vl-check input[type=checkbox]");
    await checks.nth(0).setChecked(!!opts.autoConverge);
    await checks.nth(2).setChecked(opts.hybridAfter !== undefined);
    if (opts.hybridAfter !== undefined) await page.locator(".vl-check select").selectOption(String(opts.hybridAfter));
    await page.getByRole("button", { name: "Запустить миграцию" }).click();
  }
  const verdict = (page: Page) => page.locator(".vl-final, .vl-card").getByText(/Цель сценария/);

  test("three scenarios: parameters are tuned, the server checks that the goal is reached", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-migration");
    await open(page, request, "migration");
    const sent = solutionRequest(page, "migration");

    // calm guest: the default parameters (300 ms downtime) miss the goal, 80 ms reaches it
    await migrate(page, { downtime: 300 });
    await expect(page.locator(".vl-rounds li").first()).toBeVisible();
    await expect(verdict(page)).toContainText("не достигнута");
    await expect(tabs(page).nth(0)).not.toHaveClass(/\bok\b/);
    await migrate(page, { downtime: 80 });
    await expect(verdict(page)).toContainText("достигнута");
    await expect(verdict(page)).not.toContainText("не достигнута");
    await expect(tabs(page).nth(0)).toHaveClass(/\bok\b/);

    // active guest: the vCPU must be throttled (auto-converge)
    await tabs(page).nth(1).click();
    await migrate(page, { downtime: 300 });
    await expect(verdict(page)).toContainText("не достигнута");
    await migrate(page, { downtime: 300, autoConverge: true });
    await expect(tabs(page).nth(1)).toHaveClass(/\bok\b/);

    // very active guest: hybrid with a switch to post-copy
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

// --- 6. placement on NUMA nodes (chapter 11) ------------------------------------------------------------------------------------------

test.describe("numa: machine placement", () => {
  const rows = (page: Page) => page.locator(".vl-vms tbody tr");
  const place = (row: Locator, what: "cpu" | "mem", node: string) => row.locator("select").nth(what === "cpu" ? 0 : 1).selectOption(node);

  test("a placement is accepted only when the goal is met; the server evaluates it again", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "virt-numa");
    await open(page, request, "numa");
    const sent = solutionRequest(page, "numa");
    const accept = () => page.getByRole("button", { name: "Принять размещение" }).click();

    // scenario 1: by default the machines are not placed correctly; "Принять" is rejected with a reason
    await expect(rows(page)).toHaveCount(4);
    await accept();
    await expect(page.locator(".vl-no")).not.toHaveText("");
    await expect(tabs(page).nth(0)).not.toHaveClass(/\bok\b/);
    // A and B go to node 0, C and D to node 1 (both CPUs and memory)
    for (const [i, node] of [[0, "0"], [1, "0"], [2, "1"], [3, "1"]] as const) {
      await place(rows(page).nth(i), "cpu", node);
      await place(rows(page).nth(i), "mem", node);
    }
    await expect(page.locator(".vl-stat tr", { hasText: "средняя доля удалённых" })).toContainText("0%");
    await accept();
    await expect(page.locator(".vl-yes")).toContainText("Принято");
    await expect(tabs(page).nth(0)).toHaveClass(/\bok\b/);

    // scenario 2: the large machine is stretched and needs virtual NUMA (without it the remote share is above 20%)
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

    // without virtual NUMA the server does not accept the placement of the second scenario
    await replayForAnotherUser(page, request, "numa", solution, (s) => {
      for (const p of Object.values(s.wide as Record<string, { vnuma: boolean }>)) p.vnuma = false;
    }, /wide.*удалённых/);
  });

  test("a placement that does not fit the nodes is rejected with an explanation", async ({ page, request, guard }) => {
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

// --- server refusal interface ------------------------------------------------------------------------------------------------------

test("the interface shows the server's refusal reason when the solution was tampered with", async ({ page, request, guard }) => {
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
