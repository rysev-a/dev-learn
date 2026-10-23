import { expect, loginFresh, test } from "../../support/fixtures";
import { bookList, loadChapter, DM1, stored } from "../../support/shell";

/* Левое меню разделов: список книг, подсветка текущей, сворачивание в колонку иконок (`say-aside-collapsed`). */

const KEY = "say-aside-collapsed";

test("список книг: по порядку из API, с номерами и названиями", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const items = page.locator(".sidebar .menu .slide-fs-toc-item");
  await expect(items).toHaveCount(books.length);
  await expect(items.locator(".slide-fs-toc-name")).toHaveText(books.map((b) => b.title));
  await expect(items.locator(".slide-fs-toc-num")).toHaveText(books.map((_, i) => String(i + 1).padStart(2, "0")));
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Разделы");
  // по умолчанию меню развёрнуто и ключа в хранилище нет
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  expect(await stored(page, KEY)).toBeNull();
  guard.assertClean();
});

test("меню видно на главной, в разделе, в главе и в настройках", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  for (const path of ["/", "/book/12", `/book/12/chapter/${ch.id}`, "/settings"]) {
    await page.goto(path);
    await expect(page.locator(".sidebar .menu .slide-fs-toc-item").first(), path).toBeVisible();
  }
});

test("клик по книге открывает её страницу и подсвечивает пункт", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const items = page.locator(".sidebar .menu .slide-fs-toc-item");
  await expect(items.locator(".on")).toHaveCount(0); // на главной подсвеченных нет
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

test("подсветка остаётся на книге, пока открыта её глава, и уходит со страницы настроек", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".sidebar .slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText("Дискретная математика");
  await page.goto("/settings");
  await expect(page.locator(".set-card")).toBeVisible();
  await expect(page.locator(".sidebar .slide-fs-toc-item.on")).toHaveCount(0);
});

test("меню разделов не ведёт на несуществующие книги: каждый пункт открывает свой раздел", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  for (const [i, b] of books.entries()) {
    await page.locator(".sidebar .menu .slide-fs-toc-item").nth(i).click();
    await expect(page).toHaveURL(new RegExp(`/book/${b.id}$`));
    await expect(page.locator(".lessons-menu .s-label").first()).toHaveText(b.title);
  }
});

test("сворачивание: колонка иконок вместо названий, состояние в localStorage", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  const toggle = page.locator(".aside-toggle");
  await expect(toggle).toHaveAttribute("title", "Свернуть меню");
  await toggle.click();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  await expect(page.locator(".sidebar .slide-fs-toc-item")).toHaveCount(0);
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveCount(0); // подпись «Разделы» скрыта
  await expect(toggle).toHaveAttribute("title", "Развернуть меню");
  expect(await stored(page, KEY)).toBe("1");
  // иконка — первая буква названия, всплывающая подсказка — название
  await expect(page.locator(".aside-icon").first()).toHaveAttribute("title", books[0]!.title);
  await expect(page.locator(".aside-icon").first()).toHaveText(books[0]!.title.slice(0, 1).toUpperCase());

  // ширина меняется плавно: ждём конца перехода
  const width = async () => (await page.locator(".sidebar").boundingBox())!.width;
  await expect.poll(width).toBeLessThan(100);
  await toggle.click();
  await expect.poll(width).toBeGreaterThan(200);
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  await expect(page.locator(".sidebar .slide-fs-toc-item")).toHaveCount(books.length);
  expect(await stored(page, KEY)).toBeNull();
});

test("свёрнутое состояние переживает перезагрузку и переходы между страницами", async ({ page, request }) => {
  await loginFresh(page, request);
  const books = await bookList(request);
  await page.goto("/");
  await page.locator(".aside-toggle").click();
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  await page.reload();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await expect(page.locator(".aside-icon")).toHaveCount(books.length);
  expect(await stored(page, KEY)).toBe("1");

  await page.locator(".aside-icon").nth(0).click(); // переход внутри приложения не разворачивает меню
  await expect(page).toHaveURL(/\/book\/\d+$/);
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
  await page.getByRole("button", { name: "Настройки" }).click();
  await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
});

test("в свёрнутом меню иконка открывает книгу и подсвечивается", async ({ page, request }) => {
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

test("старое явное «0» в настройке — меню развёрнуто", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "0"), KEY);
  await page.goto("/");
  await expect(page.locator(".sidebar .slide-fs-toc-item").first()).toBeVisible();
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
});

test("состояние меню общее со страницей настроек", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/settings");
  const sw = page.getByRole("switch", { name: "Свёрнутое меню разделов" });
  await expect(sw).toHaveAttribute("aria-checked", "false");
  await page.locator(".aside-toggle").click(); // кнопка над меню
  await expect(sw).toHaveAttribute("aria-checked", "true");
  await sw.click(); // переключатель на странице
  await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
  await expect(sw).toHaveAttribute("aria-checked", "false");
});
