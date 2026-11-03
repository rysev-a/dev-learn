import { request as pwRequest, type APIRequestContext, type Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { FakeWorker, PORT, chapterPath, dockerReady, realWorkerRequested, startRealWorker, unique, type RealWorker } from "../../support/learning";
import { labFile } from "../../support/labs";

/* Python tasks over the LVM board (chapter 16) and the Linux network board (chapter 12) of the book 19: the boards of the tests beside the results (level 2) and the
   `fix(board)` tasks whose repaired boards are judged by the model (level 3). The queue is driven by a fake worker (the test prints the boards a correct solution
   would print); with E2E_WORKER=1 the references are run in the real sandbox. The same checks for the oVirt book are in `virt-code.spec.ts`. */

test.use({ viewport: { width: 1400, height: 1500 } });

const BOOK = 19;

interface Board {
  nodes: { id: string; kind: string; name: string; params?: Record<string, unknown>; x?: number; y?: number }[];
  edges: { from: string; to: string }[];
}
interface Check {
  pack: string;
  scenario: string;
}

// The reference solutions of the tasks (also the ones checked in the real sandbox).
const REFERENCES: Record<string, string> = {
  "lvb16-vg-free": "def vg_free(board):\n    nodes = {n[\"id\"]: n for n in board[\"nodes\"]}\n    edges = board[\"edges\"]\n\n    def num(n, key, default):\n        return int(n.get(\"params\", {}).get(key, default))\n\n    def parents(node_id, kind):\n        return [e[\"from\"] for e in edges if e[\"to\"] == node_id and nodes[e[\"from\"]][\"kind\"] == kind]\n\n    pe = {n[\"id\"]: num(n, \"pe\", 4) for n in board[\"nodes\"] if n[\"kind\"] == \"vg\"}\n    total = {g: 0 for g in pe}\n    for n in board[\"nodes\"]:\n        if n[\"kind\"] != \"pv\":\n            continue\n        groups = [e[\"to\"] for e in edges if e[\"from\"] == n[\"id\"] and nodes[e[\"to\"]][\"kind\"] == \"vg\"]\n        disks = parents(n[\"id\"], \"disk\")\n        if groups and disks:\n            total[groups[0]] += (num(nodes[disks[0]], \"size\", 100) * 1024 - 1) // pe[groups[0]]\n    used = {g: 0 for g in pe}\n\n    def take(group, want):\n        if want <= total[group] - used[group]:\n            used[group] += want\n\n    def ext(mib, group):\n        return -(-mib // pe[group])\n\n    for n in board[\"nodes\"]:\n        if n[\"kind\"] == \"lv\":\n            groups = parents(n[\"id\"], \"vg\")\n            if groups:\n                take(groups[0], ext(num(n, \"size\", 10) * 1024, groups[0]) * num(n, \"mirror\", 1))\n        elif n[\"kind\"] == \"thin_pool\":\n            groups = parents(n[\"id\"], \"vg\")\n            if groups:\n                take(groups[0], ext(num(n, \"size\", 50) * 1024, groups[0]) + ext(num(n, \"meta\", 128), groups[0]))\n        elif n[\"kind\"] == \"snapshot\":\n            origins = parents(n[\"id\"], \"lv\")\n            groups = parents(origins[0], \"vg\") if origins else []\n            if groups:\n                take(groups[0], ext(num(n, \"size\", 5) * 1024, groups[0]))\n    return {g: [total[g], total[g] - used[g]] for g in pe}\n",
  "lvb16-fs-status": "def fs_status(board):\n    nodes = {n[\"id\"]: n for n in board[\"nodes\"]}\n    edges = board[\"edges\"]\n\n    def size(n, default):\n        return int(n.get(\"params\", {}).get(\"size\", default))\n\n    result = {}\n    for fs in board[\"nodes\"]:\n        if fs[\"kind\"] != \"fs\":\n            continue\n        volumes = [nodes[e[\"from\"]] for e in edges if e[\"to\"] == fs[\"id\"] and nodes[e[\"from\"]][\"kind\"] in (\"lv\", \"thin_lv\")]\n        if not volumes:\n            result[fs[\"id\"]] = \"detached\"\n            continue\n        volume = volumes[0]\n        parent = \"vg\" if volume[\"kind\"] == \"lv\" else \"thin_pool\"\n        if not any(e[\"to\"] == volume[\"id\"] and nodes[e[\"from\"]][\"kind\"] == parent for e in edges):\n            result[fs[\"id\"]] = \"volume_down\"\n            continue\n        fs_gib = size(fs, 10)\n        volume_gib = size(volume, 10 if volume[\"kind\"] == \"lv\" else 50)\n        if fs_gib < volume_gib:\n            result[fs[\"id\"]] = \"not_grown\"\n        elif fs_gib > volume_gib:\n            result[fs[\"id\"]] = \"too_big\"\n        else:\n            result[fs[\"id\"]] = \"ok\"\n    return result\n",
  "lvb16-snapshot-status": "def snapshot_status(board, changed_gib):\n    nodes = {n[\"id\"]: n for n in board[\"nodes\"]}\n    edges = board[\"edges\"]\n\n    def num(n, key, default):\n        return int(n.get(\"params\", {}).get(key, default))\n\n    result = {}\n    for snap in board[\"nodes\"]:\n        if snap[\"kind\"] != \"snapshot\":\n            continue\n        origins = [nodes[e[\"from\"]] for e in edges if e[\"to\"] == snap[\"id\"] and nodes[e[\"from\"]][\"kind\"] in (\"lv\", \"thin_lv\")]\n        if not origins:\n            result[snap[\"id\"]] = \"orphan\"\n            continue\n        origin = origins[0]\n        if origin[\"kind\"] == \"thin_lv\":\n            result[snap[\"id\"]] = \"valid\"\n            continue\n        groups = [nodes[e[\"from\"]] for e in edges if e[\"to\"] == origin[\"id\"] and nodes[e[\"from\"]][\"kind\"] == \"vg\"]\n        pe = num(groups[0], \"pe\", 4) if groups else 4\n        cow_mib = -(-num(snap, \"size\", 5) * 1024 // pe) * pe\n        changed = min(changed_gib, num(origin, \"size\", 10))\n        result[snap[\"id\"]] = \"invalid\" if changed * 1024 > cow_mib else \"valid\"\n    return result\n",
  "lvb16-wire-stack": "def fix(board):\n    nodes = board[\"nodes\"]\n    kind = {n[\"id\"]: n[\"kind\"] for n in nodes}\n    linked = {(e[\"from\"], e[\"to\"]) for e in board[\"edges\"]}\n    add = []\n\n    def ids(k):\n        return [n[\"id\"] for n in nodes if n[\"kind\"] == k]\n\n    def only(k):\n        found = ids(k)\n        return found[0] if len(found) == 1 else None\n\n    # 1. loose disks and PVs without a disk, in the order of the board\n    loose_disks = [d for d in ids(\"disk\") if not any((d, p) in linked for p in ids(\"pv\"))]\n    loose_pvs = [p for p in ids(\"pv\") if not any((d, p) in linked for d in ids(\"disk\"))]\n    add += [[d, p] for d, p in zip(loose_disks, loose_pvs)]\n    group = only(\"vg\")\n    if group:\n        # 2. PVs, 3. volumes and pools\n        for p in ids(\"pv\"):\n            if (p, group) not in linked:\n                add.append([p, group])\n        for i in ids(\"lv\") + ids(\"thin_pool\"):\n            if (group, i) not in linked:\n                add.append([group, i])\n    # 4. thin volumes\n    pool = only(\"thin_pool\")\n    if pool:\n        for t in ids(\"thin_lv\"):\n            if (pool, t) not in linked:\n                add.append([pool, t])\n    # 5. snapshots by name\n    names = {n[\"name\"]: n[\"id\"] for n in nodes if n[\"kind\"] in (\"lv\", \"thin_lv\")}\n    for n in nodes:\n        if n[\"kind\"] == \"snapshot\" and not any((v, n[\"id\"]) in linked for v in names.values()):\n            origin = names.get(n[\"name\"][:-5]) if n[\"name\"].endswith(\"-snap\") else None\n            if origin:\n                add.append([origin, n[\"id\"]])\n    return {\"add\": add, \"remove\": []}\n",
  "nb12-addresses": "def addresses(board):\n    third = {\"a\": 1, \"b\": 2, \"c\": 3}\n    interfaces = (\"eth\", \"veth\", \"bridge\", \"bond\", \"vlan\", \"vm\")\n    count = {}\n    result = {}\n    for n in board[\"nodes\"]:\n        params = n.get(\"params\", {})\n        if n[\"kind\"] == \"external\":\n            result[n[\"id\"]] = \"10.0.%d.254\" % third[params.get(\"net\", \"a\")]\n        elif n[\"kind\"] in interfaces:\n            net = params.get(\"net\", \"none\")\n            if net != \"none\":\n                count[net] = count.get(net, 0) + 1\n                result[n[\"id\"]] = \"10.0.%d.%d\" % (third[net], count[net])\n    return result\n",
  "nb12-link-states": "def link_states(board):\n    nodes = {n[\"id\"]: n for n in board[\"nodes\"]}\n    edges = board[\"edges\"]\n    interfaces = (\"eth\", \"veth\", \"bridge\", \"bond\", \"vlan\", \"vm\")\n\n    def sources(node_id, kinds):\n        return [nodes[e[\"from\"]] for e in edges if e[\"to\"] == node_id and nodes[e[\"from\"]][\"kind\"] in kinds]\n\n    def targets(node_id, kinds):\n        return [nodes[e[\"to\"]] for e in edges if e[\"from\"] == node_id and nodes[e[\"to\"]][\"kind\"] in kinds]\n\n    def is_up(n):\n        return n.get(\"params\", {}).get(\"up\", True)\n\n    def state(n):\n        if n[\"kind\"] != \"vm\" and not sources(n[\"id\"], (\"netns\",)):\n            return \"no_carrier\"\n        if not is_up(n):\n            return \"down\"\n        kind = n[\"kind\"]\n        if kind == \"eth\":\n            return \"up\" if targets(n[\"id\"], (\"external\",)) else \"no_carrier\"\n        if kind == \"veth\":\n            peers = [m for m in board[\"nodes\"] if m[\"kind\"] == \"veth\" and m[\"id\"] != n[\"id\"] and (\n                (n[\"id\"], m[\"id\"]) in {(e[\"from\"], e[\"to\"]) for e in edges} or (m[\"id\"], n[\"id\"]) in {(e[\"from\"], e[\"to\"]) for e in edges})]\n            if peers and is_up(peers[0]) and sources(peers[0][\"id\"], (\"netns\",)):\n                return \"up\"\n            return \"no_carrier\"\n        if kind == \"bond\":\n            live = [s for s in sources(n[\"id\"], (\"eth\",)) if state(s) == \"up\"]\n            if not live:\n                return \"no_carrier\"\n            if n.get(\"params\", {}).get(\"mode\", \"active-backup\") == \"802.3ad\":\n                switches = {t[\"id\"] for s in live for t in targets(s[\"id\"], (\"external\",))}\n                if len(switches) > 1:\n                    return \"no_carrier\"\n            return \"up\"\n        if kind == \"vlan\":\n            parents = sources(n[\"id\"], (\"eth\", \"bond\"))\n            return \"up\" if parents and state(parents[0]) == \"up\" else \"no_carrier\"\n        if kind == \"bridge\":\n            ports = sources(n[\"id\"], (\"eth\", \"veth\", \"bond\", \"vlan\", \"vm\"))\n            return \"up\" if any(is_up(p) and state(p) == \"up\" for p in ports) else \"no_carrier\"\n        bridges = targets(n[\"id\"], (\"bridge\",))\n        return \"up\" if bridges and is_up(bridges[0]) else \"no_carrier\"\n\n    return {n[\"id\"]: state(n) for n in board[\"nodes\"] if n[\"kind\"] in interfaces}\n",
  "nb12-bridge-vlans": "def bridge_vlans(board):\n    nodes = {n[\"id\"]: n for n in board[\"nodes\"]}\n    ports = (\"eth\", \"veth\", \"bond\", \"vlan\", \"vm\")\n    result = {}\n    for bridge in board[\"nodes\"]:\n        if bridge[\"kind\"] != \"bridge\":\n            continue\n        groups = {}\n        for e in board[\"edges\"]:\n            port = nodes[e[\"from\"]]\n            if e[\"to\"] == bridge[\"id\"] and port[\"kind\"] in ports:\n                tag = port.get(\"params\", {}).get(\"access_vlan\", \"0\")\n                groups.setdefault(tag, []).append(port[\"id\"])\n        result[bridge[\"id\"]] = {tag: sorted(ids) for tag, ids in groups.items()}\n    return result\n",
  "nb12-wire-network": "def fix(board):\n    nodes = board[\"nodes\"]\n    linked = {(e[\"from\"], e[\"to\"]) for e in board[\"edges\"]}\n    add = []\n\n    def ids(*kinds):\n        return [n[\"id\"] for n in nodes if n[\"kind\"] in kinds]\n\n    def only(kind):\n        found = ids(kind)\n        return found[0] if len(found) == 1 else None\n\n    by_name = {n[\"name\"]: n[\"id\"] for n in nodes if n[\"kind\"] == \"netns\"}\n    # 1 and 2: where the interfaces live\n    for n in nodes:\n        home = None\n        if n[\"kind\"] in (\"eth\", \"bridge\", \"bond\", \"vlan\"):\n            home = by_name.get(\"host\")\n        elif n[\"kind\"] == \"veth\" and \"-\" in n[\"name\"]:\n            home = by_name.get(n[\"name\"].split(\"-\", 1)[1])\n        if home and (home, n[\"id\"]) not in linked:\n            add.append([home, n[\"id\"]])\n    # 3: veth pairs, the host end first\n    ends = {}\n    for n in nodes:\n        if n[\"kind\"] == \"veth\" and \"-\" in n[\"name\"]:\n            ends.setdefault(n[\"name\"].split(\"-\", 1)[0], []).append(n)\n    for pair in ends.values():\n        if len(pair) == 2:\n            a, b = sorted(pair, key=lambda n: not n[\"name\"].endswith(\"-host\"))\n            if (a[\"id\"], b[\"id\"]) not in linked and (b[\"id\"], a[\"id\"]) not in linked:\n                add.append([a[\"id\"], b[\"id\"]])\n    bridge = only(\"bridge\")\n    bond = only(\"bond\")\n    if bridge:\n        # 4 and 6: ports and taps\n        for n in nodes:\n            wanted = (n[\"kind\"] == \"veth\" and n[\"name\"].endswith(\"-host\")) or n[\"kind\"] in (\"bond\", \"vm\")\n            if wanted and (n[\"id\"], bridge) not in linked:\n                add.append([n[\"id\"], bridge])\n    if bond:\n        # 5: slaves\n        for e in ids(\"eth\"):\n            if (e, bond) not in linked:\n                add.append([e, bond])\n    return {\"add\": add, \"remove\": []}\n",
};

/** Level 2: the answer is data; `p` is the CSS prefix of the board (`vl-lvm`, `vl-net`). */
const DATA_TASKS = [
  { id: "lvb16-vg-free", chapter: 16, p: "lvm", fn: "vg_free", args: "board" },
  { id: "lvb16-fs-status", chapter: 16, p: "lvm", fn: "fs_status", args: "board" },
  { id: "lvb16-snapshot-status", chapter: 16, p: "lvm", fn: "snapshot_status", args: "board, changed_gib" },
  { id: "nb12-addresses", chapter: 12, p: "net", fn: "addresses", args: "board" },
  { id: "nb12-link-states", chapter: 12, p: "net", fn: "link_states", args: "board" },
  { id: "nb12-bridge-vlans", chapter: 12, p: "net", fn: "bridge_vlans", args: "board" },
];

/** Level 3: the code repairs the board. The scenarios of the fix packs are boards of real packs with links taken away; the reference is the board of the source. */
const FIX_TASKS = [
  {
    id: "lvb16-wire-stack",
    chapter: 16,
    p: "lvm",
    sources: {
      "loose-disk": ["virt-sim-lvm-grow", "build"],
      "vm-group": ["virt-sim-lvm-resilience", "vm-disks"],
      "thin-stack": ["virt-sim-lvm-snapshots", "thin-snapshot"],
      "cow-origin": ["virt-sim-lvm-snapshots", "cow-size"],
    } as Record<string, [string, string]>,
  },
  {
    id: "nb12-wire-network",
    chapter: 12,
    p: "net",
    sources: {
      "veth-pair": ["virt-sim-net-bridge", "two-namespaces"],
      container: ["virt-sim-net-nat", "build"],
      "bond-slaves": ["virt-sim-net-bond", "build-bond"],
      "vm-on-bond": ["virt-sim-net-bond", "bond-bridge"],
    } as Record<string, [string, string]>,
  },
];

/** Opens a code task of the book 19. */
async function openTask(page: Page, request: APIRequestContext, chapter: number, id: string): Promise<void> {
  await page.goto(`${await chapterPath(request, BOOK, chapter, "exercises")}?task=${id}`);
  await expect(page.locator(".pr-main")).toBeVisible();
}

const editor = (page: Page) => page.locator("textarea.rs-input");
const check = (page: Page) => page.locator(".ex-row button.quiz-btn").first();
const picTabs = (page: Page) => page.locator(".vl-pic .vl-tab-mark").locator("xpath=..");

/** The reference board of a scenario of a real pack (the lab data file keeps the solution), the way the driver prints it (no positions). */
function printed(source: [string, string]): string {
  const [pack, scenario] = source;
  for (const ch of [10, 11, 12, 16, 20]) {
    let file;
    try {
      file = labFile("virt", ch, BOOK);
    } catch {
      continue;
    }
    const task = file.tasks.find((t) => t.id === pack);
    if (task) {
      const board = (task.spec as { solution: Record<string, Board> }).solution[scenario]!;
      return JSON.stringify({ nodes: board.nodes.map(({ x, y, ...n }) => n), edges: board.edges });
    }
  }
  throw new Error(`no pack ${pack}`);
}

test.describe("level 2: the board of the test beside the results", () => {
  for (const task of DATA_TASKS) {
    test(`${task.id}: every test has a board; after a run the first failing test is shown`, async ({ page, request, guard }) => {
      await loginFresh(page, request, "board19-tests");
      const worker = new FakeWorker(request);
      await worker.ping();
      await openTask(page, request, task.chapter, task.id);
      await expect(page.locator(".vl-pic")).toBeVisible();
      const tests = await picTabs(page).count();
      expect(tests).toBeGreaterThanOrEqual(4);
      await expect(page.locator(`.vl-pic-svg .vl-${task.p}-node`).first()).toBeVisible();
      // statuses are drawn by the model from the links of the test board
      await expect(page.locator(`.vl-pic-svg .vl-${task.p}-status .vl-chip`).first()).toBeVisible();

      await editor(page).fill(`def ${task.fn}(${task.args}):\n    return {}\n${unique()}\n`);
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
  }
});

test.describe("level 3: the code repairs the board, the model judges it", () => {
  for (const task of FIX_TASKS) {
    test(`${task.id}: the boards come back repaired, the goals are checked by the model`, async ({ page, request, guard }) => {
      test.setTimeout(120_000);
      await loginFresh(page, request, "board19-fix");
      const worker = new FakeWorker(request);
      await worker.ping();
      await openTask(page, request, task.chapter, task.id);
      await expect(page.locator(".vl-pic")).toBeVisible();
      const n = await picTabs(page).count();
      expect(n).toBe(4);
      // before a run: the starting board of the first scenario, some goal is open
      await expect(page.locator(".vl-pic .vl-goals li:not(.ok)").first()).toBeVisible();
      await expect(page.locator(`.vl-pic-svg .vl-${task.p}-node`).first()).toBeVisible();

      // the first run prints nothing useful: nothing is solved
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
      const lines = checks.map((c) => printed(task.sources[c.scenario]!)).join("\n") + "\n";
      await worker.complete(job2!, { status: "ok", results: [{ ok: false, got: lines, expected: "", error: null }], stdout: "" });
      await expect(page.locator(".pr-badge.ok")).toBeVisible();
      await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(4);
      await page.getByRole("button", { name: /После вашей починки|After your fix/ }).click();
      await expect(page.locator(".vl-pic .vl-goals li:not(.ok)")).toHaveCount(0);
      await expect(page.locator(`.vl-pic-svg .vl-${task.p}-edge.path`).first()).toBeVisible(); // links the code added
      guard.assertClean();
    });
  }
});

// ==================================================================================================
// Real sandbox: E2E_WORKER=1, Docker and the python:3.13-slim image
// ==================================================================================================

test.describe("board tasks of the book 19 in the real sandbox", () => {
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

  for (const task of [...DATA_TASKS, ...FIX_TASKS]) {
    test(`${task.id}: the reference solution runs in the sandbox and passes`, async ({ page, request, guard }) => {
      await loginFresh(page, request, "board19-real");
      await openTask(page, request, task.chapter, task.id);
      await editor(page).fill(`${REFERENCES[task.id]}\n${unique()}\n`);
      await check(page).click();
      await expect(page.locator(".pr-badge.ok")).toBeVisible({ timeout: 150_000 });
      await expect(page.locator(".vl-pic .vl-tab").first()).toBeVisible();
      if ("sources" in task) await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(4);
      guard.assertClean();
    });
  }

  for (const task of FIX_TASKS) {
    test(`${task.id}: the starter solves nothing`, async ({ page, request, guard }) => {
      await loginFresh(page, request, "board19-real-starter");
      await openTask(page, request, task.chapter, task.id);
      await check(page).click();
      await expect(page.locator(".vl-pic .vl-tab").first()).toBeVisible();
      await expect(page.locator(".pr-res")).toBeVisible({ timeout: 150_000 });
      await expect(page.locator(".vl-pic .vl-tab.ok")).toHaveCount(0);
      await expect(page.locator(".pr-badge.ok")).toHaveCount(0);
      guard.assertClean();
    });
  }
});
