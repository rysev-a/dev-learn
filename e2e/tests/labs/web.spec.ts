import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { expectStatusOk, labFile, labTask, listItem, openTask, putSolved, statusOf } from "../../support/labs";

/* Лаборатория «HTML и CSS» (книга 11): редактор, предпросмотр в iframe, условия на странице и перепроверка решения на сервере.
   Упражнения — глава 18 «CSS для программиста» (стили и селекторы). */

test.use({ viewport: { width: 1400, height: 1400 } });

const CH = 18;
const goals = (page: Page) => page.locator(".lab-web .vl-goals li");
const editor = (page: Page) => page.locator(".lab-web textarea").first();
const badge = (page: Page) => page.locator(".pr-head .pr-badge");
const frame = (page: Page) => page.frameLocator("iframe.web-frame");

async function typeCode(page: Page, code: string) {
  await editor(page).fill(code);
}

test("стили: условия оживают по мере набора, решённое принимает сервер", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-css");
  const task = labTask("web", CH, "w18-css-color");
  await openTask(page, request, "web", CH, task.id);
  await expect(page.locator(".lab-web")).toBeVisible();
  const total = (task.spec.checks as unknown[]).length;
  expect(total).toBeGreaterThanOrEqual(3);
  // на пустом редакторе зелёным может быть только «CSS без ошибок»
  expect(await page.locator(".lab-web .vl-goals li.ok").count()).toBeLessThan(total);
  await expect(badge(page)).not.toHaveText("выполнено");

  // половина решения: заголовок покрашен, абзац — нет
  await typeCode(page, ".title { color: #c0392b; }");
  await expect(goals(page).filter({ hasText: ".title" })).toHaveClass(/ok/);
  await expect(goals(page).filter({ hasText: ".lead" })).not.toHaveClass(/ok/);
  await expect(badge(page)).not.toHaveText("выполнено");
  expect(await statusOf(request, token, "web", CH, task.id)).toBeUndefined();

  // предпросмотр действительно применил стили
  await expect(frame(page).locator(".title")).toHaveCSS("color", "rgb(192, 57, 43)");

  await typeCode(page, (task.spec.reference as { css: string }).css);
  await expect(page.locator(".lab-web .vl-goals li.ok")).toHaveCount(total);
  await expect(badge(page)).toHaveText("выполнено");
  await expect(listItem(page, task.title).locator(".pr-mark")).toHaveText("✓");
  await expectStatusOk(request, token, "web", CH, task.id);
});

test("селектор: выбранные элементы обводятся, лишние называются по именам", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-sel");
  const task = labTask("web", CH, "w18-sel-descendant");
  await openTask(page, request, "web", CH, task.id);

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
  await expectStatusOk(request, token, "web", CH, task.id);
});

test("специфичность: селектор слишком тяжёлый — условие красное", async ({ page, request }) => {
  await loginFresh(page, request, "web-spec");
  const task = labTask("web", CH, "w18-sel-low-spec");
  await openTask(page, request, "web", CH, task.id);
  await typeCode(page, "#page .note");
  await expect(goals(page).filter({ hasText: "Специфичность" })).not.toHaveClass(/ok/);
  await expect(goals(page).filter({ hasText: "Специфичность" })).toContainText("(1, 1, 0)");
  await typeCode(page, ".note");
  await expect(badge(page)).toHaveText("выполнено");
});

test("кнопки ширины меняют окно предпросмотра, «Начать заново» возвращает заготовку", async ({ page, request }) => {
  await loginFresh(page, request, "web-width");
  const task = labTask("web", CH, "w18-css-specificity");
  await openTask(page, request, "web", CH, task.id);
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

test("сервер отказывает неверному и пустому решению с причиной, эталон принимает", async ({ page, request }) => {
  const { token } = await loginFresh(page, request, "web-api");
  const task = labTask("web", CH, "w18-css-flex-row");
  const bad = await putSolved(request, token, "web", CH, task.id, JSON.stringify({ html: "", css: ".bar { display: block; }" }));
  expect(bad.status).toBe(422);
  expect(bad.detail).toContain("display");
  const empty = await putSolved(request, token, "web", CH, task.id, JSON.stringify({ html: "", css: "" }));
  expect(empty.status).toBe(422);
  const broken = await putSolved(request, token, "web", CH, task.id, "это не JSON");
  expect(broken.status).toBe(422);
  const good = await putSolved(request, token, "web", CH, task.id, JSON.stringify({ html: "", css: (task.spec.reference as { css: string }).css }));
  expect(good.status).toBe(204);
  expect(await statusOf(request, token, "web", CH, task.id)).toBe("ok");
});

test("клиенту не уходит эталон", async ({ page, request }) => {
  await loginFresh(page, request, "web-ref");
  const task = labTask("web", CH, "w18-css-flex-row");
  const res = await request.get(`/api/labs/11/${CH}`);
  expect(res.ok()).toBeTruthy();
  const body = (await res.json()) as { tasks: { id: string; spec: Record<string, unknown> }[] };
  const mine = body.tasks.find((t) => t.id === task.id)!;
  expect(mine.spec["reference"]).toBeUndefined();
  expect(JSON.stringify(body)).not.toContain("justify-content: space-between; align-items: center; gap: 16px");
});

// --- раздел «HTML и разметка» (главы 13–15): эталон каждого упражнения вводится руками и принимается сервером ----------------

for (const chapter of [13, 14, 15]) {
  test(`HTML, глава ${chapter}: эталон каждого упражнения решает его в интерфейсе`, async ({ page, request }) => {
    test.setTimeout(600_000);
    const { token } = await loginFresh(page, request, `web-html-${chapter}`);
    const tasks = labFile("web", chapter).tasks;
    expect(tasks.length).toBeGreaterThanOrEqual(15);
    for (const task of tasks) {
      await openTask(page, request, "web", chapter, task.id);
      // заготовка не решает задачу
      await expect(badge(page), `${task.id}: заготовка`).not.toHaveText("выполнено");
      const ref = (task.spec.reference as { html: string }).html;
      await typeCode(page, ref);
      await expect(badge(page), `${task.id}: эталон`).toHaveText("выполнено");
      await expectStatusOk(request, token, "web", chapter, task.id);
    }
  });
}

test("HTML: вырезанный скрипт не работает в предпросмотре, разметка видна", async ({ page, request }) => {
  await loginFresh(page, request, "web-html-preview");
  await openTask(page, request, "web", 13, "w13-skeleton");
  await typeCode(page, "<!doctype html><html lang=ru><head><title>Т</title></head><body><h1 id=x>Привет</h1><script>document.title='x'</script></body></html>");
  await expect(frame(page).locator("#x")).toHaveText("Привет");
});
