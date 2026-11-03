import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { clone, expectStatusOk, labBooks, labChapters, labFile, openTask, putDraft, putSolved, statusOf } from "../../support/labs";

/* Every board exercise of the virtualization labs (all packs found in `backend/data/labs/virt`: the oVirt topology boards of the book 17 and the LVM boards of the book 19):
   the reference boards stored as a draft solve it and the server replays them, a spoiled board is refused, and the reference of the first and the last scenario is
   rebuilt in the interface with clicks. The two boards share the model of the data (`{nodes, edges}`) and the DOM contract, under the prefixes `vl-topo`, `vl-lvm` and `vl-net`. */

test.use({ viewport: { width: 1400, height: 1500 } });

interface BoardNode {
  id: string;
  kind: string;
  name: string;
  params?: Record<string, unknown>;
}
interface Board {
  nodes: BoardNode[];
  edges: { from: string; to: string }[];
}
interface Scenario {
  id: string;
  start: Board;
  goals: unknown[];
}
/** The simulators that are boards and the prefix of the CSS classes of each. */
const BOARDS: Record<string, string> = { ovirt_topo: "vl-topo", lvm_board: "vl-lvm", net_board: "vl-net" };

interface Pack {
  book: number;
  prefix: string;
  chapter: number;
  id: string;
  title: string;
  scenarios: Scenario[];
  solution: Record<string, Board>;
}

/** All board exercises of the data files. */
function packs(): Pack[] {
  const out: Pack[] = [];
  for (const book of labBooks("virt")) {
    for (const chapter of labChapters("virt", book)) {
      for (const t of labFile("virt", chapter, book).tasks) {
        const spec = t.spec as { sim?: string; scenarios?: Scenario[]; solution?: Record<string, Board> };
        const prefix = spec.sim ? BOARDS[spec.sim] : undefined;
        if (prefix) out.push({ book, prefix, chapter, id: t.id, title: t.title, scenarios: spec.scenarios!, solution: spec.solution! });
      }
    }
  }
  return out;
}

const PACKS = packs();
const tabs = (page: Page) => page.locator(".vl-tab");
const edgeKey = (e: { from: string; to: string }) => `${e.from}>${e.to}`;

test("the board exercises are all found", () => {
  expect(PACKS.filter((p) => p.prefix === "vl-topo").length).toBeGreaterThanOrEqual(11);
  expect(PACKS.filter((p) => p.prefix === "vl-lvm").length).toBeGreaterThanOrEqual(3);
  expect(PACKS.filter((p) => p.prefix === "vl-net").length).toBeGreaterThanOrEqual(3);
  for (const p of PACKS) expect(p.scenarios.length, p.id).toBeGreaterThanOrEqual(4);
});

for (const pack of PACKS) {
  test.describe(pack.id, () => {
    test("the initial state is not accepted", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "boards");
      await openTask(page, request, "virt", pack.chapter, pack.id, pack.book);
      await expect(page.locator(`.${pack.prefix}`).first()).toBeVisible();
      await expect(tabs(page)).toHaveCount(pack.scenarios.length);
      await expect(page.locator(".vl-tab.ok")).toHaveCount(0);
      const empty = await putSolved(request, token, "virt", pack.chapter, pack.id, "{}", pack.book);
      expect(empty.status).toBe(422);
      expect(await statusOf(request, token, "virt", pack.chapter, pack.id, pack.book)).toBeUndefined();
      guard.assertClean();
    });

    test("the reference boards solve it; the server replays them and refuses a spoiled board", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "boards");
      await putDraft(request, token, "virt", pack.chapter, pack.id, JSON.stringify(pack.solution), pack.book);
      const sent = page.waitForRequest((r) => r.url().endsWith(`/${pack.id}/solved`) && r.method() === "PUT");
      await openTask(page, request, "virt", pack.chapter, pack.id, pack.book);
      await expect(page.locator(".vl-tab.ok")).toHaveCount(pack.scenarios.length);
      const solution = JSON.parse((JSON.parse((await sent).postData() ?? "{}") as { solution: string }).solution) as Record<string, Board>;
      await expectStatusOk(request, token, "virt", pack.chapter, pack.id, pack.book);
      expect(Object.keys(solution).sort()).toEqual(pack.scenarios.map((s) => s.id).sort());
      guard.assertClean();

      // another student: the key link of a scenario removed — refused; the original — accepted
      const other = await loginFresh(page, request, "boards-other");
      const spoiled = clone(solution);
      const sc = pack.scenarios.find((s) => solution[s.id]!.edges.some((e) => !s.start.edges.some((x) => edgeKey(x) === edgeKey(e))))!;
      const added = solution[sc.id]!.edges.filter((e) => !sc.start.edges.some((x) => edgeKey(x) === edgeKey(e)));
      spoiled[sc.id]!.edges = spoiled[sc.id]!.edges.filter((e) => edgeKey(e) !== edgeKey(added[added.length - 1]!));
      const refused = await putSolved(request, other.token, "virt", pack.chapter, pack.id, JSON.stringify(spoiled), pack.book);
      expect(refused.status, `spoiled ${sc.id}`).toBe(422);
      expect(refused.detail).toContain(sc.id);
      expect((await putSolved(request, other.token, "virt", pack.chapter, pack.id, JSON.stringify(solution), pack.book)).status).toBe(204);
    });

    // the first and the last scenario are rebuilt by hand: from the starting board to the reference with clicks
    for (const which of ["first", "last"] as const) {
      test(`the ${which} scenario is rebuilt in the interface`, async ({ page, request, guard }) => {
        test.setTimeout(240_000);
        const index = which === "first" ? 0 : pack.scenarios.length - 1;
        const sc = pack.scenarios[index]!;
        await loginFresh(page, request, "boards");
        await openTask(page, request, "virt", pack.chapter, pack.id, pack.book);
        await tabs(page).nth(index).click();
        await expect(page.locator(`.${pack.prefix}-node`)).toHaveCount(sc.start.nodes.length);
        await expect(tabs(page).nth(index)).not.toHaveClass(/\bok\b/);
        await replay(page, pack.prefix, sc.start, pack.solution[sc.id]!);
        await expect(tabs(page).nth(index)).toHaveClass(/\bok\b/);
        await expect(page.locator(".vl-goals li:not(.ok)")).toHaveCount(0);
        guard.assertClean();
      });
    }
  });
}

// --- driving the board -------------------------------------------------------------------------------------------------------------------------

const node = (prefix: string, id: string) => `.${prefix}-node[data-id="${id}"]`;
const edgeSel = (prefix: string, e: { from: string; to: string }) => `.${prefix}-edge[data-from="${e.from}"][data-to="${e.to}"]`;

async function link(page: Page, prefix: string, from: string, to: string) {
  await page.locator(`.${prefix}-pin.out[data-node="${from}"]`).click({ force: true });
  await page.locator(`.${prefix}-pin.in[data-node="${to}"]`).click({ force: true });
}

/** Turn the starting board into the reference with the interface: delete links, add objects, set parameters, add links. */
async function replay(page: Page, prefix: string, start: Board, ref: Board) {
  const refEdges = new Set(ref.edges.map(edgeKey));
  const startEdges = new Set(start.edges.map(edgeKey));
  // 0. objects the reference does not have (their links go with them)
  const refIds = new Set(ref.nodes.map((n) => n.id));
  for (const n of start.nodes.filter((n) => !refIds.has(n.id))) {
    await page.locator(node(prefix, n.id)).locator(`.${prefix}-name`).click({ force: true });
    await page.locator(`.${prefix}-delete`).click();
    await expect(page.locator(node(prefix, n.id))).toHaveCount(0);
  }
  // 1. links the reference does not have
  for (const e of start.edges.filter((e) => !refEdges.has(edgeKey(e)))) {
    if ((await page.locator(edgeSel(prefix, e)).count()) === 0) continue; // already dropped together with another one
    await page.locator(`${edgeSel(prefix, e)} .hit`).dispatchEvent("click");
    await page.locator(`.${prefix}-delete`).click();
    await expect(page.locator(edgeSel(prefix, e))).toHaveCount(0);
  }
  // 2. objects the reference has and the start has not (identifiers are chosen by the interface: map them)
  const ids = new Map<string, string>(start.nodes.map((n) => [n.id, n.id]));
  for (const n of ref.nodes.filter((n) => !ids.has(n.id))) {
    const known = new Set([...ids.values()]);
    await page.locator(`.${prefix}-add[data-kind="${n.kind}"]`).click();
    const now = await page.locator(`.${prefix}-node[data-kind="${n.kind}"]`).evaluateAll((els) => els.map((e) => (e as HTMLElement).dataset.id!));
    const fresh = now.filter((id) => !known.has(id));
    expect(fresh.length, `a new ${n.kind}`).toBe(1);
    ids.set(n.id, fresh[0]!);
  }
  // 3. parameters of the reference (new objects start with the defaults, the start ones with theirs). A control is found by the key of the parameter
  const startNodes = new Map(start.nodes.map((n) => [n.id, n]));
  for (const n of ref.nodes) {
    const before = startNodes.get(n.id)?.params ?? {};
    const want = n.params ?? {};
    for (const [key, value] of Object.entries(want)) {
      if (JSON.stringify(before[key]) === JSON.stringify(value) && startNodes.has(n.id)) continue;
      await page.locator(node(prefix, ids.get(n.id)!)).locator(`.${prefix}-name`).click({ force: true });
      const field = page.locator(`.${prefix}-inspector [data-param="${key}"]`);
      if (typeof value === "boolean") {
        const box = field.locator("input[type=checkbox]");
        await (value ? box.check() : box.uncheck());
      } else {
        await field.locator("select").selectOption(String(value));
      }
    }
  }
  // 3b. a parameter the start sets and the reference leaves unset is the default: the interface says which one it is
  for (const n of ref.nodes) {
    const before = startNodes.get(n.id)?.params ?? {};
    for (const key of Object.keys(before).filter((k) => !(k in (n.params ?? {})))) {
      const field = page.locator(`.${prefix}-inspector [data-param="${key}"]`);
      await page.locator(node(prefix, ids.get(n.id)!)).locator(`.${prefix}-name`).click({ force: true });
      const def = await field.getAttribute("data-default");
      if (def === null) continue;
      if (def === "true" || def === "false") await (def === "true" ? field.locator("input[type=checkbox]").check() : field.locator("input[type=checkbox]").uncheck());
      else await field.locator("select").selectOption(def);
    }
  }
  // 4. links of the reference that are not on the board. The order of the reference is not always the order the rules allow (a network is assigned to a host only
  //    after the host is in the cluster): refused links wait for the next pass
  let pending = ref.edges.map((e) => ({ from: ids.get(e.from)!, to: ids.get(e.to)! }));
  for (let pass = 0; pass < 5 && pending.length > 0; pass++) {
    const still: typeof pending = [];
    for (const e of pending) {
      if ((await page.locator(edgeSel(prefix, e)).count()) > 0) continue;
      await link(page, prefix, e.from, e.to);
      if ((await page.locator(edgeSel(prefix, e)).count()) === 0) still.push(e);
    }
    pending = still;
  }
  expect(pending, "links that the board refused in every pass").toEqual([]);
  void startEdges;
}
