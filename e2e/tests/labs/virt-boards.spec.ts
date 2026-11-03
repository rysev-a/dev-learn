import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { clone, expectStatusOk, labChapters, labFile, openTask, putDraft, putSolved, statusOf } from "../../support/labs";

/* Every oVirt topology board exercise of the book 17 (all packs found in `backend/data/labs/virt`): the reference boards stored as a draft solve it and the server
   replays them, a spoiled board is refused, and the reference of the first and the last scenario is rebuilt in the interface with clicks. */

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
interface Pack {
  chapter: number;
  id: string;
  title: string;
  scenarios: Scenario[];
  solution: Record<string, Board>;
}

/** All board exercises of the data files. */
function packs(): Pack[] {
  const out: Pack[] = [];
  for (const chapter of labChapters("virt")) {
    for (const t of labFile("virt", chapter).tasks) {
      const spec = t.spec as { sim?: string; scenarios?: Scenario[]; solution?: Record<string, Board> };
      if (spec.sim === "ovirt_topo") out.push({ chapter, id: t.id, title: t.title, scenarios: spec.scenarios!, solution: spec.solution! });
    }
  }
  return out;
}

const PACKS = packs();
const tabs = (page: Page) => page.locator(".vl-tab");
const edgeKey = (e: { from: string; to: string }) => `${e.from}>${e.to}`;

test("the board exercises are all found", () => {
  expect(PACKS.length).toBeGreaterThanOrEqual(11);
  for (const p of PACKS) expect(p.scenarios.length, p.id).toBeGreaterThanOrEqual(4);
});

for (const pack of PACKS) {
  test.describe(pack.id, () => {
    test("the initial state is not accepted", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "boards");
      await openTask(page, request, "virt", pack.chapter, pack.id);
      await expect(page.locator(".vl-topo")).toBeVisible();
      await expect(tabs(page)).toHaveCount(pack.scenarios.length);
      await expect(page.locator(".vl-tab.ok")).toHaveCount(0);
      const empty = await putSolved(request, token, "virt", pack.chapter, pack.id, "{}");
      expect(empty.status).toBe(422);
      expect(await statusOf(request, token, "virt", pack.chapter, pack.id)).toBeUndefined();
      guard.assertClean();
    });

    test("the reference boards solve it; the server replays them and refuses a spoiled board", async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "boards");
      await putDraft(request, token, "virt", pack.chapter, pack.id, JSON.stringify(pack.solution));
      const sent = page.waitForRequest((r) => r.url().endsWith(`/${pack.id}/solved`) && r.method() === "PUT");
      await openTask(page, request, "virt", pack.chapter, pack.id);
      await expect(page.locator(".vl-tab.ok")).toHaveCount(pack.scenarios.length);
      const solution = JSON.parse((JSON.parse((await sent).postData() ?? "{}") as { solution: string }).solution) as Record<string, Board>;
      await expectStatusOk(request, token, "virt", pack.chapter, pack.id);
      expect(Object.keys(solution).sort()).toEqual(pack.scenarios.map((s) => s.id).sort());
      guard.assertClean();

      // another student: the key link of a scenario removed — refused; the original — accepted
      const other = await loginFresh(page, request, "boards-other");
      const spoiled = clone(solution);
      const sc = pack.scenarios.find((s) => solution[s.id]!.edges.some((e) => !s.start.edges.some((x) => edgeKey(x) === edgeKey(e))))!;
      const added = solution[sc.id]!.edges.filter((e) => !sc.start.edges.some((x) => edgeKey(x) === edgeKey(e)));
      spoiled[sc.id]!.edges = spoiled[sc.id]!.edges.filter((e) => edgeKey(e) !== edgeKey(added[added.length - 1]!));
      const refused = await putSolved(request, other.token, "virt", pack.chapter, pack.id, JSON.stringify(spoiled));
      expect(refused.status, `spoiled ${sc.id}`).toBe(422);
      expect(refused.detail).toContain(sc.id);
      expect((await putSolved(request, other.token, "virt", pack.chapter, pack.id, JSON.stringify(solution))).status).toBe(204);
    });

    // the first and the last scenario are rebuilt by hand: from the starting board to the reference with clicks
    for (const which of ["first", "last"] as const) {
      test(`the ${which} scenario is rebuilt in the interface`, async ({ page, request, guard }) => {
        test.setTimeout(240_000);
        const index = which === "first" ? 0 : pack.scenarios.length - 1;
        const sc = pack.scenarios[index]!;
        await loginFresh(page, request, "boards");
        await openTask(page, request, "virt", pack.chapter, pack.id);
        await tabs(page).nth(index).click();
        await expect(page.locator(".vl-topo-node")).toHaveCount(sc.start.nodes.length);
        await expect(tabs(page).nth(index)).not.toHaveClass(/\bok\b/);
        await replay(page, sc.start, pack.solution[sc.id]!);
        await expect(tabs(page).nth(index)).toHaveClass(/\bok\b/);
        await expect(page.locator(".vl-goals li:not(.ok)")).toHaveCount(0);
        guard.assertClean();
      });
    }
  });
}

// --- driving the board -------------------------------------------------------------------------------------------------------------------------

const node = (id: string) => `.vl-topo-node[data-id="${id}"]`;
const edgeSel = (e: { from: string; to: string }) => `.vl-topo-edge[data-from="${e.from}"][data-to="${e.to}"]`;

async function link(page: Page, from: string, to: string) {
  await page.locator(`.vl-topo-pin.out[data-node="${from}"]`).click({ force: true });
  await page.locator(`.vl-topo-pin.in[data-node="${to}"]`).click({ force: true });
}

/** Turn the starting board into the reference with the interface: delete links, add objects, set parameters, add links. */
async function replay(page: Page, start: Board, ref: Board) {
  const refEdges = new Set(ref.edges.map(edgeKey));
  const startEdges = new Set(start.edges.map(edgeKey));
  // 1. links the reference does not have
  for (const e of start.edges.filter((e) => !refEdges.has(edgeKey(e)))) {
    if ((await page.locator(edgeSel(e)).count()) === 0) continue; // already dropped together with another one
    await page.locator(`${edgeSel(e)} .hit`).dispatchEvent("click");
    await page.locator(".vl-topo-delete").click();
    await expect(page.locator(edgeSel(e))).toHaveCount(0);
  }
  // 2. objects the reference has and the start has not (identifiers are chosen by the interface: map them)
  const ids = new Map<string, string>(start.nodes.map((n) => [n.id, n.id]));
  for (const n of ref.nodes.filter((n) => !ids.has(n.id))) {
    const known = new Set([...ids.values()]);
    await page.locator(`.vl-topo-add[data-kind="${n.kind}"]`).click();
    const now = await page.locator(`.vl-topo-node[data-kind="${n.kind}"]`).evaluateAll((els) => els.map((e) => (e as HTMLElement).dataset.id!));
    const fresh = now.filter((id) => !known.has(id));
    expect(fresh.length, `a new ${n.kind}`).toBe(1);
    ids.set(n.id, fresh[0]!);
  }
  // 3. parameters of the reference (new objects start with the defaults, the start ones with theirs)
  const startNodes = new Map(start.nodes.map((n) => [n.id, n]));
  for (const n of ref.nodes) {
    const before = startNodes.get(n.id)?.params ?? {};
    const want = n.params ?? {};
    for (const [key, value] of Object.entries(want)) {
      if (JSON.stringify(before[key]) === JSON.stringify(value) && startNodes.has(n.id)) continue;
      await page.locator(node(ids.get(n.id)!)).locator(".vl-topo-name").click({ force: true });
      const inspector = page.locator(".vl-topo-inspector");
      if (typeof value === "boolean") {
        const box = inspector.locator("label", { hasText: /./ }).locator(`input[type=checkbox]`).first();
        await (value ? box.check() : box.uncheck());
      } else {
        const selects = inspector.locator("select");
        const count = await selects.count();
        let done = false;
        for (let i = 0; i < count && !done; i++) {
          const options = await selects.nth(i).locator("option").evaluateAll((os) => os.map((o) => (o as HTMLOptionElement).value));
          if (options.includes(String(value))) {
            await selects.nth(i).selectOption(String(value));
            done = true;
          }
        }
        expect(done, `a control for ${key}=${String(value)}`).toBeTruthy();
      }
    }
  }
  // 4. links of the reference that are not on the board. The order of the reference is not always the order the rules allow (a network is assigned to a host only
  //    after the host is in the cluster): refused links wait for the next pass
  let pending = ref.edges.map((e) => ({ from: ids.get(e.from)!, to: ids.get(e.to)! }));
  for (let pass = 0; pass < 5 && pending.length > 0; pass++) {
    const still: typeof pending = [];
    for (const e of pending) {
      if ((await page.locator(edgeSel(e)).count()) > 0) continue;
      await link(page, e.from, e.to);
      if ((await page.locator(edgeSel(e)).count()) === 0) still.push(e);
    }
    pending = still;
  }
  expect(pending, "links that the board refused in every pass").toEqual([]);
  void startEdges;
}
