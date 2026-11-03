import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, bookList, DM1, loadChapter } from "../../support/shell";

/* Narrow screen: the books list and the chapter list leave the page, the burger opens a drawer (books; the open book shows its chapters). */

test.use({ viewport: { width: 390, height: 800 } });

test("the side menus are hidden, the burger is shown and the drawer is closed", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".burger")).toBeVisible();
  await expect(page.locator(".sidebar")).toBeHidden();
  await expect(page.locator(".lessons-menu")).toBeHidden();
  await expect(page.locator(".mm-panel")).toBeHidden();
  assertCleanBut404(guard);
});

test("the burger opens the drawer with the current book expanded; a chapter opens and closes it", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await page.locator(".burger").click();
  await expect(page.locator(".mm-panel")).toBeVisible();
  await expect(page.locator(".mm-book")).toHaveCount(books.length);
  const chapters = page.locator(".mm-chapters .slide-fs-toc-item");
  await expect(chapters.first()).toBeVisible();
  await expect(page.locator(".mm-chapters .slide-fs-toc-item.on")).toHaveCount(1);

  await chapters.nth(1).click();
  await expect(page).toHaveURL(/\/book\/12\/chapter\/\d+$/);
  await expect(page).not.toHaveURL(new RegExp(`/chapter/${ch.id}$`));
  await expect(page.locator(".mm-panel")).toBeHidden();
});

test("another book expands on a tap, the backdrop and Escape close the drawer", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  await page.locator(".burger").click();
  await expect(page.locator(".mm-chapters")).toHaveCount(0);
  await page.locator(".mm-book-head").nth(1).click();
  await expect(page.locator(".mm-chapters .slide-fs-toc-item").first()).toBeVisible();
  await page.locator(".mm-book-head").nth(1).click();
  await expect(page.locator(".mm-chapters")).toHaveCount(0);

  await page.keyboard.press("Escape");
  await expect(page.locator(".mm-panel")).toBeHidden();
  await page.locator(".burger").click();
  await expect(page.locator(".mm-panel")).toBeVisible();
  await page.mouse.click(360, 400); // to the right of the panel: the backdrop
  await expect(page.locator(".mm-panel")).toBeHidden();
});
