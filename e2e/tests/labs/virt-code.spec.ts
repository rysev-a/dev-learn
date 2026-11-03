import { request as pwRequest, type APIRequestContext, type Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { FakeWorker, PORT, chapterPath, dockerReady, realWorkerRequested, startRealWorker, unique, type RealWorker } from "../../support/learning";
import { labChapters, labFile } from "../../support/labs";

/* Python tasks over the oVirt board (book 17): the boards of the tests beside the results (level 2) and the `fix(board)` tasks whose repaired boards are judged
   by the model (level 3). The queue is driven by a fake worker (the test prints the boards a correct solution would print); with E2E_WORKER=1 the references
   are run in the real sandbox. */

test.use({ viewport: { width: 1400, height: 1500 } });

interface Board {
  nodes: { id: string; kind: string; name: string; params?: Record<string, unknown>; x?: number; y?: number }[];
  edges: { from: string; to: string }[];
}
interface Check {
  pack: string;
  scenario: string;
}

// The reference solutions of the three fix tasks (also the ones checked in the real sandbox).
const REFERENCES: Record<string, string> = {
  "ovb20-wire-hosts": "def fix(board):\n    kind = {n[\"id\"]: n[\"kind\"] for n in board[\"nodes\"]}\n    edges = [(e[\"from\"], e[\"to\"]) for e in board[\"edges\"]]\n    dcs = [i for i, k in kind.items() if k == \"data_center\"]\n    add = []\n\n    def link(a, b):\n        if (a, b) not in edges:\n            edges.append((a, b))\n            add.append([a, b])\n\n    # a domain that no data center has goes to the only data center\n    for d in [i for i, k in kind.items() if k == \"storage_domain\"]:\n        if not any(b == d and kind[a] == \"data_center\" for a, b in edges) and len(dcs) == 1:\n            link(dcs[0], d)\n    for dc in dcs:\n        domains = [b for a, b in edges if a == dc and kind[b] == \"storage_domain\"]\n        for cl in [b for a, b in edges if a == dc and kind[b] == \"cluster\"]:\n            networks = [a for a, b in edges if b == cl and kind[a] == \"network\"]\n            for host in [b for a, b in edges if a == cl and kind[b] == \"host\"]:\n                for x in networks + domains:\n                    link(x, host)\n    return {\"add\": add, \"remove\": []}\n",
  "ovb21-spread-networks": "def fix(board):\n    kind = {n[\"id\"]: n[\"kind\"] for n in board[\"nodes\"]}\n    edges = [(e[\"from\"], e[\"to\"]) for e in board[\"edges\"]]\n    add = []\n\n    def link(a, b):\n        if (a, b) not in edges:\n            edges.append((a, b))\n            add.append([a, b])\n\n    for dc in [i for i, k in kind.items() if k == \"data_center\"]:\n        networks = [b for a, b in edges if a == dc and kind[b] == \"network\"]\n        for cl in [b for a, b in edges if a == dc and kind[b] == \"cluster\"]:\n            for net in networks:\n                link(net, cl)\n                for host in [b for a, b in edges if a == cl and kind[b] == \"host\"]:\n                    link(net, host)\n    return {\"add\": add, \"remove\": []}\n",
  "ovb25-heal": "def fix(board):\n    kind = {n[\"id\"]: n[\"kind\"] for n in board[\"nodes\"]}\n    role = {n[\"id\"]: n.get(\"params\", {}).get(\"role\", \"vm\") for n in board[\"nodes\"] if n[\"kind\"] == \"network\"}\n    edges = [(e[\"from\"], e[\"to\"]) for e in board[\"edges\"]]\n    ids = list(kind)\n    dcs = [i for i in ids if kind[i] == \"data_center\"]\n    engines = [i for i in ids if kind[i] == \"engine\"]\n    add = []\n\n    def link(a, b):\n        if (a, b) not in edges:\n            edges.append((a, b))\n            add.append([a, b])\n\n    # the engine sits in every management network\n    for net in [i for i in ids if kind[i] == \"network\" and role[i] == \"management\"]:\n        for engine in engines:\n            link(engine, net)\n    # a domain that no data center has goes to the only data center\n    for d in [i for i in ids if kind[i] == \"storage_domain\"]:\n        if not any(b == d and kind[a] == \"data_center\" for a, b in edges) and len(dcs) == 1:\n            link(dcs[0], d)\n    for dc in dcs:\n        clusters = [b for a, b in edges if a == dc and kind[b] == \"cluster\"]\n        # a network that no cluster has goes to every cluster of its data center\n        for net in [b for a, b in edges if a == dc and kind[b] == \"network\"]:\n            if not any(b == net for a, b in edges if kind[a] == \"network\") and not any(a == net and kind[b] == \"cluster\" for a, b in edges):\n                for cl in clusters:\n                    link(net, cl)\n        domains = [b for a, b in edges if a == dc and kind[b] == \"storage_domain\"]\n        for cl in clusters:\n            networks = [a for a, b in edges if b == cl and kind[a] == \"network\"]\n            for host in [b for a, b in edges if a == cl and kind[b] == \"host\"]:\n                for x in networks + domains:\n                    link(x, host)\n    return {\"add\": add, \"remove\": []}\n"
};

const FIX_TASKS = [
  { id: "ovb20-wire-hosts", chapter: 20 },
  { id: "ovb21-spread-networks", chapter: 21 },
  { id: "ovb25-heal", chapter: 25 },
];

/** Opens a code task of the book 17 (not a lab: no lab data to look up). */
async function openTask(page: Page, request: APIRequestContext, _kind: string, chapter: number, id: string): Promise<void> {
  await page.goto(`${await chapterPath(request, 17, chapter, "exercises")}?task=${id}`);
  await expect(page.locator(".pr-main")).toBeVisible();
}

const editor = (page: Page) => page.locator("textarea.rs-input");
const check = (page: Page) => page.locator(".ex-row button.quiz-btn").first();
const picTabs = (page: Page) => page.locator(".vl-pic .vl-tab-mark").locator("xpath=..");

/** The reference board of a scenario, the way the driver prints it (no positions). */
function printed(pack: string, scenario: string): string {
  for (const ch of labChapters("virt")) {
    const task = labFile("virt", ch).tasks.find((t) => t.id === pack);
    if (task) {
      const board = (task.spec as { solution: Record<string, Board> }).solution[scenario]!;
      return JSON.stringify({ nodes: board.nodes.map(({ x, y, ...n }) => n), edges: board.edges });
    }
  }
  throw new Error(`no pack ${pack}`);
}

test.describe("level 2: the board of the test beside the results", () => {
  test("every test has a board; after a run the first failing test is shown", async ({ page, request, guard }) => {
    await loginFresh(page, request, "board-tests");
    const worker = new FakeWorker(request);
    await worker.ping();
    await openTask(page, request, "virt", 21, "ovb21-host-status");
    await expect(page.locator(".vl-pic")).toBeVisible();
    const tests = await picTabs(page).count();
    expect(tests).toBeGreaterThanOrEqual(5);
    await expect(page.locator(".vl-pic-svg .vl-topo-node").first()).toBeVisible();
    // statuses are drawn by the model from the links of the test board
    await expect(page.locator(".vl-pic-svg .vl-topo-status .vl-chip").first()).toBeVisible();

    await editor(page).fill(`def host_statuses(board):\n    return {}\n${unique()}\n`);
    await check(page).click();
    const job = await worker.claim();
    expect(job).not.toBeNull();
    const results = Array.from({ length: tests }, (_, i) => ({ ok: i !== 2, args: "[...]", expected: "{}", got: "{}" }));
    await worker.complete(job!, { status: "ok", results, stdout: "" });
    await expect(picTabs(page).nth(2)).toHaveClass(/\bon\b/);
    await expect(picTabs(page).nth(0)).toHaveClass(/\bok\b/);
    await expect(picTabs(page).nth(2)).not.toHaveClass(/\bok\b/);
    guard.assertClean();
  });
});

test.describe("level 3: the code repairs the board, the model judges it", () => {
  for (const task of FIX_TASKS) {
    test(`${task.id}: the boards come back repaired, the goals are checked by the model`, async ({ page, request, guard }) => {
      test.setTimeout(120_000);
      await loginFresh(page, request, "board-fix");
      const worker = new FakeWorker(request);
      await worker.ping();
      await openTask(page, request, "virt", task.chapter, task.id);
      await expect(page.locator(".vl-pic")).toBeVisible();
      const n = await picTabs(page).count();
      expect(n).toBe(4);
      // before a run: the starting board of the first scenario, some goal is open
      await expect(page.locator(".vl-pic .vl-goals li:not(.ok)").first()).toBeVisible();

      // the first run prints the boards untouched: nothing is solved
      await editor(page).fill(`def fix(board):\n    return {"add": [], "remove": []}\n${unique()}\n`);
      await check(page).click();
      const job = await worker.claim();
      expect(job, "the job reached the worker").not.toBeNull();
      const checks = job!.task.board_check as Check[];
      expect(checks.length).toBe(4);

      await worker.complete(job!, { status: "ok", results: [{ ok: false, got: "", expected: "", error: "TypeError: not a board" }], stdout: "" });
      await expect(page.locator(".pr-badge.bad")).toBeVisible();

      // the second run prints the reference boards: every scenario is solved
      await editor(page).fill(`def fix(board):\n    return {"add": [], "remove": []}\n# second ${unique()}\n`);
      await check(page).click();
      const job2 = await worker.claim();
      expect(job2).not.toBeNull();
      await worker.complete(job2!, { status: "ok", results: [{ ok: false, got: checks.map((c) => printed(c.pack, c.scenario)).join("\n") + "\n", expected: "", error: null }], stdout: "" });
      await expect(page.locator(".pr-badge.ok")).toBeVisible();
      await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(4);
      await page.getByRole("button", { name: /После вашей починки|After your fix/ }).click();
      await expect(page.locator(".vl-pic .vl-goals li:not(.ok)")).toHaveCount(0);
      await expect(page.locator(".vl-pic-svg .vl-topo-edge.path").first()).toBeVisible(); // links the code added
      guard.assertClean();
    });
  }
});

// ==================================================================================================
// Real sandbox: E2E_WORKER=1, Docker and the python:3.13-slim image
// ==================================================================================================

test.describe("level 3 in the real sandbox", () => {
  test.describe.configure({ mode: "serial", timeout: 240_000 });
  test.skip(!realWorkerRequested, "E2E_WORKER=1 is not set: the real check is disabled");
  test.skip(realWorkerRequested && !dockerReady(), "Docker is unavailable or the python:3.13-slim image is missing");

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

  for (const task of FIX_TASKS) {
    test(`${task.id}: the reference solution runs in the sandbox and solves all four boards`, async ({ page, request, guard }) => {
      await loginFresh(page, request, "board-real");
      await openTask(page, request, "virt", task.chapter, task.id);
      await editor(page).fill(`${REFERENCES[task.id]}\n${unique()}\n`);
      await check(page).click();
      await expect(page.locator(".pr-badge.ok")).toBeVisible({ timeout: 150_000 });
      await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(4);
      guard.assertClean();
    });

    test(`${task.id}: the starter solves nothing`, async ({ page, request, guard }) => {
      await loginFresh(page, request, "board-real-starter");
      await openTask(page, request, "virt", task.chapter, task.id);
      await check(page).click();
      await expect(page.locator(".vl-pic .vl-tab").first()).toBeVisible();
      await expect(page.locator(".pr-res")).toBeVisible({ timeout: 150_000 });
      await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(0);
      await expect(page.locator(".pr-badge.ok")).toHaveCount(0);
      guard.assertClean();
    });
  }
});
