import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { expectStatusOk, labFile, labTask, listItem, openTask, putSolved, statusOf } from "../../support/labs";

/* HTML and CSS lab (book 11): editor, iframe preview, on-page conditions and server-side re-check of the solution.
   Chapters 13-15 are HTML, 16-21 are CSS (selectors, cascade, box model, flexbox, grid, responsiveness). */

test.use({ viewport: { width: 1400, height: 1400 } });

const goals = (page: Page) => page.locator(".lab-web .vl-goals li");
const editor = (page: Page) => page.locator(".lab-web textarea").first();
const badge = (page: Page) => page.locator(".pr-head .pr-badge");
const frame = (page: Page) => page.frameLocator("iframe.web-frame");

async function typeCode(page: Page, code: string) {
  await editor(page).fill(code);
}

test("styles: conditions come alive as you type, the server accepts the solved state", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-css");
  const task = labTask("web", 17, "w17-color-size");
  await openTask(page, request, "web", 17, task.id);
  await expect(page.locator(".lab-web")).toBeVisible();
  const total = (task.spec.checks as unknown[]).length;
  expect(total).toBeGreaterThanOrEqual(3);
  // on an empty editor only "CSS без ошибок" can be green
  expect(await page.locator(".lab-web .vl-goals li.ok").count()).toBeLessThan(total);
  await expect(badge(page)).not.toHaveText("выполнено");

  // half a solution: the heading is colored, the paragraph is not
  await typeCode(page, ".title { color: #c0392b; }");
  await expect(goals(page).filter({ hasText: ".title" })).toHaveClass(/ok/);
  await expect(goals(page).filter({ hasText: ".lead" })).not.toHaveClass(/ok/);
  await expect(badge(page)).not.toHaveText("выполнено");
  expect(await statusOf(request, token, "web", 17, task.id)).toBeUndefined();

  // the preview really applied the styles
  await expect(frame(page).locator(".title")).toHaveCSS("color", "rgb(192, 57, 43)");

  await typeCode(page, (task.spec.reference as { css: string }).css);
  await expect(page.locator(".lab-web .vl-goals li.ok")).toHaveCount(total);
  await expect(badge(page)).toHaveText("выполнено");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expectStatusOk(request, token, "web", 17, task.id);
});

test("selector: selected elements are outlined, extra ones are named", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-sel");
  const task = labTask("web", 16, "w16-sel-descendant");
  await openTask(page, request, "web", 16, task.id);

  await typeCode(page, "p");
  await expect(goals(page).filter({ hasText: "Выбирает ровно" })).toContainText("лишние: #out");
  await expect(frame(page).locator("#out")).toHaveCSS("outline-style", "solid");
  await expect(badge(page)).not.toHaveText("выполнено");

  await typeCode(page, "p[");
  await expect(goals(page).first()).not.toHaveClass(/ok/);
  await expect(goals(page).first()).toContainText("не разобран");

  await typeCode(page, ".article p");
  await expect(goals(page).filter({ hasText: "Выбирает ровно" })).toHaveClass(/ok/);
  await expect(frame(page).locator("#p1")).toHaveCSS("outline-style", "solid");
  await expect(frame(page).locator("#out")).not.toHaveCSS("outline-style", "solid");
  await expect(badge(page)).toHaveText("выполнено");
  await expectStatusOk(request, token, "web", 16, task.id);
});

test("specificity: the selector is too heavy, so the condition is red", async ({ page, request }) => {
  await loginFresh(page, request, "web-spec");
  const task = labTask("web", 16, "w16-sel-low-spec");
  await openTask(page, request, "web", 16, task.id);
  await typeCode(page, "#page .note");
  await expect(goals(page).filter({ hasText: "Специфичность" })).not.toHaveClass(/ok/);
  await expect(goals(page).filter({ hasText: "Специфичность" })).toContainText("(1, 1, 0)");
  await typeCode(page, ".note");
  await expect(badge(page)).toHaveText("выполнено");
});

test("width buttons resize the preview window, \"Начать заново\" restores the starter", async ({ page, request }) => {
  await loginFresh(page, request, "web-width");
  const task = labTask("web", 16, "w16-css-specificity");
  await openTask(page, request, "web", 16, task.id);
  const iframe = page.locator("iframe.web-frame");
  await page.getByRole("button", { name: "360" }).click();
  await expect(iframe).toHaveCSS("width", "360px");
  await page.getByRole("button", { name: "768" }).click();
  await expect(iframe).toHaveCSS("width", "768px");

  await typeCode(page, "#card .text.text { color: blue; }");
  await expect(badge(page)).toHaveText("выполнено");
  await page.getByRole("button", { name: "Начать заново" }).click();
  await expect(editor(page)).toHaveValue(String((task.spec as { starter_css: string }).starter_css));
});

test("the server refuses wrong and empty solutions with a reason and accepts the reference", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-api");
  const task = labTask("web", 19, "w19-bar");
  const bad = await putSolved(request, token, "web", 19, task.id, JSON.stringify({ html: "", css: ".bar { display: block; }" }));
  expect(bad.status).toBe(422);
  expect(bad.detail).toContain("display");
  const empty = await putSolved(request, token, "web", 19, task.id, JSON.stringify({ html: "", css: "" }));
  expect(empty.status).toBe(422);
  const broken = await putSolved(request, token, "web", 19, task.id, "this is not JSON");
  expect(broken.status).toBe(422);
  const good = await putSolved(request, token, "web", 19, task.id, JSON.stringify({ html: "", css: (task.spec.reference as { css: string }).css }));
  expect(good.status).toBe(204);
  expect(await statusOf(request, token, "web", 19, task.id)).toBe("ok");
});

test("the reference is not sent to the client", async ({ page, request }) => {
  await loginFresh(page, request, "web-ref");
  const task = labTask("web", 19, "w19-bar");
  const res = await request.get("/api/labs/11/19");
  expect(res.ok()).toBeTruthy();
  const body = (await res.json()) as { tasks: { id: string; spec: Record<string, unknown> }[] };
  const mine = body.tasks.find((t) => t.id === task.id)!;
  expect(mine.spec["reference"]).toBeUndefined();
  expect(JSON.stringify(body)).not.toContain("justify-content: space-between; align-items: center; gap: 16px");
});

// --- chapters 13-21: the reference of each exercise is typed by hand and accepted by the server ----------------------------------------------

/** What to type into the editor: HTML, CSS or a selector. */
function referenceText(spec: Record<string, unknown>): string {
  const r = spec["reference"] as { html: string; css: string; selector: string };
  return spec["kind"] === "html" ? r.html : spec["kind"] === "selector" ? r.selector : r.css;
}

for (const chapter of [13, 14, 15, 16, 17, 18, 19, 20, 21]) {
  test(`chapter ${chapter}: each exercise's reference solves it in the interface`, async ({ page, request }) => {
    test.setTimeout(900_000);
    const { token } = await loginFresh(page, request, `web-all-${chapter}`);
    const tasks = labFile("web", chapter).tasks;
    expect(tasks.length).toBeGreaterThanOrEqual(15);
    for (const task of tasks) {
      await openTask(page, request, "web", chapter, task.id);
      // the starter does not solve the task
      await expect(badge(page), `${task.id}: starter`).not.toHaveText("выполнено");
      await typeCode(page, referenceText(task.spec));
      await expect(badge(page), `${task.id}: reference`).toHaveText("выполнено");
      await expectStatusOk(request, token, "web", chapter, task.id);
    }
  });
}

test("HTML: the stripped script does not run in the preview, the markup is visible", async ({ page, request }) => {
  await loginFresh(page, request, "web-html-preview");
  await openTask(page, request, "web", 13, "w13-skeleton");
  await typeCode(page, "<!doctype html><html lang=ru><head><title>Т</title></head><body><h1 id=x>Привет</h1><script>document.title='x'</script></body></html>");
  await expect(frame(page).locator("#x")).toHaveText("Привет");
});
