import { expect, loginFresh, test } from "../../support/fixtures";
import { bookList, loadChapter, DM1, stored } from "../../support/shell";

/* Left sections menu: book list, current-book highlight, collapsing into an icon column (`cs-core-aside-collapsed`). */

const KEY = "cs-core-aside-collapsed";

test("book list: in API order, with numbers and titles", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const items = page.locator(".sidebar .menu .slide-fs-toc-item");
  await expect(items).toHaveCount(books.length);
  await expect(items.locator(".slide-fs-toc-name")).toHaveText(books.map((b) => b.title));
  await expect(items.locator(".slide-fs-toc-num")).toHaveText(books.map((_, i) => String(i + 1).padStart(2, "0")));
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Разделы");
  // by default the menu is expanded and there is no storage key
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  expect(await stored(page, KEY)).toBeNull();
  guard.assertClean();
});

test("the menu is visible on the home page, in a section, in a chapter and in settings", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  for (const path of ["/", "/book/12", `/book/12/chapter/${ch.id}`, "/settings"]) {
    await page.goto(path);
    await expect(page.locator(".sidebar .menu .slide-fs-toc-item").first(), path).toBeVisible();
  }
});

test("clicking a book opens its page and highlights the item", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const items = page.locator(".sidebar .menu .slide-fs-toc-item");
  await expect(items.locator(".on")).toHaveCount(0); // nothing is highlighted on the home page
  await expect(page.locator(".sidebar .slide-fs-toc-item.on")).toHaveCount(0);

  const dm = books.findIndex((b) => b.id === 12);
  await items.nth(dm).click();
  await expect(page).toHaveURL(/\/book\/12$/);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on")).toHaveCount(1);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(books[dm]!.title);

  const py = books.findIndex((b) => b.id === 13);
  await items.nth(py).click();
  await expect(page).toHaveURL(/\/book\/13$/);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on")).toHaveCount(1);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(books[py]!.title);
});

test("the highlight stays on the book while its chapter is open and goes away on the settings page", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText("Дискретная математика");
  await page.goto("/settings");
  await expect(page.locator(".set-card")).toBeVisible();
  await expect(page.locator(".sidebar .slide-fs-toc-item.on")).toHaveCount(0);
});

test("the sections menu does not lead to nonexistent books: each item opens its own section", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  for (const [i, b] of books.entries()) {
    await page.locator(".sidebar .menu .slide-fs-toc-item").nth(i).click();
    await expect(page).toHaveURL(new RegExp(`/book/${b.id}$`));
    await expect(page.locator(".lessons-menu .s-label").first()).toHaveText(b.title);
  }
});

test("collapsing: an icon column instead of titles, state in localStorage", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const toggle = page.locator(".aside-toggle");
  await expect(toggle).toHaveAttribute("title", "Свернуть меню");
  await toggle.click();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  await expect(page.locator(".sidebar .slide-fs-toc-item")).toHaveCount(0);
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveCount(0); // the "Разделы" label is hidden
  await expect(toggle).toHaveAttribute("title", "Развернуть меню");
  expect(await stored(page, KEY)).toBe("1");
  // the icon is the first letter of the title, the tooltip is the title
  await expect(page.locator(".aside-icon").first()).toHaveAttribute("title", books[0]!.title);
  await expect(page.locator(".aside-icon").first()).toHaveText(books[0]!.title.slice(0, 1).toUpperCase());

  // the width changes smoothly: wait for the transition to end
  const width = async () => (await page.locator(".sidebar").boundingBox())!.width;
  await expect.poll(width).toBeLessThan(100);
  await toggle.click();
  await expect.poll(width).toBeGreaterThan(200);
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  await expect(page.locator(".sidebar .slide-fs-toc-item")).toHaveCount(books.length);
  expect(await stored(page, KEY)).toBeNull();
});

test("the collapsed state survives a reload and navigation between pages", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  await page.locator(".aside-toggle").click();
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  await page.reload();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  expect(await stored(page, KEY)).toBe("1");

  await page.locator(".aside-icon").nth(0).click(); // in-app navigation does not expand the menu
  await expect(page).toHaveURL(/\/book\/\d+$/);
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await page.getByRole("button", { name: "Настройки" }).click();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
});

test("in the collapsed menu an icon opens the book and is highlighted", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "1"), KEY);
  await page.goto("/");
  await expect(page.locator(".aside-icon.on")).toHaveCount(0);
  const dm = books.find((b) => b.id === 12)!;
  await page.locator(`.aside-icon[title="${dm.title}"]`).click();
  await expect(page).toHaveURL(/\/book\/12$/);
  await expect(page.locator(".aside-icon.on")).toHaveCount(1);
  await expect(page.locator(".aside-icon.on")).toHaveAttribute("title", dm.title);
});

test("an old explicit \"0\" in the setting means the menu is expanded", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "0"), KEY);
  await page.goto("/");
  await expect(page.locator(".sidebar .slide-fs-toc-item").first()).toBeVisible();
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
});

test("the menu state is shared with the settings page", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/settings");
  const sw = page.getByRole("switch", { name: "Свёрнутое меню разделов" });
  await expect(sw).toHaveAttribute("aria-checked", "false");
  await page.locator(".aside-toggle").click(); // button above the menu
  await expect(sw).toHaveAttribute("aria-checked", "true");
  await sw.click(); // switch on the page
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  await expect(sw).toHaveAttribute("aria-checked", "false");
});
