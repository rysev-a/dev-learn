import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, controlClock, courseOf, DM1, loadChapter, type ChapterDto } from "../../support/shell";

/* Полноэкранный режим главы: оболочка `.slide-fs` (дерево, шапка с вкладками, содержимое), состояние в адресе `?fs=1`. */

const fsRoot = (page: Page) => page.locator(".slide-fs");
const items = (page: Page) => fsRoot(page).locator(".fst-slide");
const onItem = (page: Page) => fsRoot(page).locator(".fst-slide.on");
const head = (page: Page) => fsRoot(page).locator(".slide-fs-head");
const search = (page: Page) => new URL(page.url()).search;

/** Открывает главу сразу в полном экране и ждёт, пока вкладка положит пункты в дерево. */
async function openFs(page: Page, ch: ChapterDto, query = "") {
  await page.goto(`/book/12/chapter/${ch.id}?fs=1${query}`);
  await expect(fsRoot(page)).toBeVisible();
  await expect(items(page)).toHaveCount(ch.lessons.length);
}

const pageNum = (ch: ChapterDto, n: number) => `${String(n).padStart(2, "0")} / ${String(ch.lessons.length).padStart(2, "0")}`;

test("кнопка «Весь экран» открывает оболочку: адрес ?fs=1, нативный полный экран, дерево и шапка", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.locator(".slide-panel")).toBeVisible();
  await expect(fsRoot(page)).toHaveCount(0);
  await page.locator(".ch-expand").click();
  await expect(fsRoot(page)).toBeVisible();
  await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${ch.id}\\?fs=1$`));
  await expect.poll(() => page.evaluate(() => document.fullscreenElement?.tagName ?? null)).toBe("HTML");
  await expect(fsRoot(page).locator(".slide-fs-toc")).toBeVisible();
  await expect(head(page).locator(".slide-fs-caption")).toHaveText(`Урок ${ch.num}. ${ch.title}`);
  await expect(head(page).getByRole("button", { name: "Свернуть" })).toBeVisible();
  // в полном экране кнопки «Весь экран» нет
  await expect(fsRoot(page).locator(".ch-expand")).toHaveCount(0);
  assertCleanBut404(guard);
});

test("заход по адресу ?fs=1 сразу показывает оболочку со вкладками", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await openFs(page, ch);
  await expect(fsRoot(page).locator(".ch-tab")).toHaveCount(3);
  await expect(fsRoot(page).locator(".ch-tab.on")).toHaveText("Теория");
  // ссылки вкладок сохраняют ?fs=1
  const base = `/book/12/chapter/${ch.id}`;
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Теория" })).toHaveAttribute("href", `${base}?fs=1`);
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Вопросы" })).toHaveAttribute("href", `${base}/questions?fs=1`);
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Практика" })).toHaveAttribute("href", `${base}/exercises?fs=1`);
});

test.describe("дерево разделов и глав", () => {
  test("разделы книги; раздел текущей главы раскрыт, остальные свёрнуты; текущая глава отмечена", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const heads = fsRoot(page).locator(".fst-sec-head");
    await expect(heads).toHaveCount(course.length);
    await expect(heads).toHaveText(course.map((s) => new RegExp(s.title, "i")));
    await expect(heads.nth(0)).toHaveAttribute("aria-expanded", "true");
    for (let i = 1; i < course.length; i++) await expect(heads.nth(i)).toHaveAttribute("aria-expanded", "false");
    // главы раскрытого раздела видны, текущая отмечена
    const first = course[0]!.chapters;
    const sec0 = fsRoot(page).locator(".fst-sec").nth(0);
    await expect(sec0.locator(".slide-fs-toc-item")).toHaveCount(first.length);
    await expect(sec0.locator(".slide-fs-toc-item.on")).toHaveCount(1);
    await expect(sec0.locator(".slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(ch.title);
    // у свёрнутого раздела главы скрыты
    await expect(fsRoot(page).locator(".fst-sec").nth(1).locator(".slide-fs-toc-item").first()).toBeHidden();
  });

  test("заголовок раздела раскрывает и сворачивает его главы", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const second = fsRoot(page).locator(".fst-sec").nth(1);
    const secHead = second.locator(".fst-sec-head");
    await secHead.click();
    await expect(secHead).toHaveAttribute("aria-expanded", "true");
    await expect(second.locator(".slide-fs-toc-item")).toHaveCount(course[1]!.chapters.length);
    await expect(second.locator(".slide-fs-toc-item").first()).toBeVisible();
    await secHead.click();
    await expect(secHead).toHaveAttribute("aria-expanded", "false");
    await expect(second.locator(".slide-fs-toc-item").first()).toBeHidden();
  });

  test("под текущей главой — пункты слайдов с названиями, текущий слайд отмечен", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await expect(items(page)).toHaveCount(ch.lessons.length);
    await expect(onItem(page)).toHaveCount(1);
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("01");
    for (const name of await items(page).locator(".fst-slide-name").allInnerTexts()) expect(name.trim()).not.toBe("");
    // пункты лежат в дереве под своей главой
    await expect(fsRoot(page).locator(".fst-sec").nth(0).locator(".fst-slide")).toHaveCount(ch.lessons.length);
  });

  test("клик по пункту слайда показывает его: номер, ?slide= в адресе, отметка", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await items(page).nth(4).click();
    await expect(head(page).locator(".slide-panel-num")).toHaveText(pageNum(ch, 5));
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("05");
    await expect.poll(() => search(page)).toBe("?fs=1&slide=4");
    await expect(page.locator(".slide-fs-stage .s-title")).toBeVisible();
  });

  test("клик по другой главе открывает её теорию в полном экране", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const [c1, c2] = course[0]!.chapters;
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await fsRoot(page).locator(".slide-fs-toc-item", { hasText: c2!.title }).click();
    await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${c2!.id}\\?fs=1$`));
    await expect(fsRoot(page)).toBeVisible();
    await expect(head(page).locator(".slide-fs-caption")).toHaveText(`Урок ${c2!.num}. ${c2!.title}`);
    await expect(fsRoot(page).locator(".slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(c2!.title);
    await expect(fsRoot(page).locator(".ch-tab.on")).toHaveText("Теория");
    await expect(items(page)).toHaveCount(c2!.parts_count);
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("01");
    expect(c1!.id).toBe(ch.id);
  });

  test("переход к другой главе из вкладки «Вопросы» открывает «Теорию»", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const c2 = course[0]!.chapters[1]!;
    const ch = await loadChapter(request, DM1);
    await page.goto(`/book/12/chapter/${ch.id}/questions?fs=1`);
    await expect(fsRoot(page).locator(".ch-tab.on")).toContainText("Вопросы");
    await fsRoot(page).locator(".slide-fs-toc-item", { hasText: c2.title }).click();
    await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${c2.id}\\?fs=1$`));
    await expect(fsRoot(page).locator(".ch-tab.on")).toHaveText("Теория");
  });

  test("раскрытые разделы переживают переход к другой главе", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const c2 = course[0]!.chapters[1]!;
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const third = fsRoot(page).locator(".fst-sec").nth(2).locator(".fst-sec-head");
    await third.click();
    await expect(third).toHaveAttribute("aria-expanded", "true");
    await fsRoot(page).locator(".slide-fs-toc-item", { hasText: c2.title }).click();
    await expect(page).toHaveURL(new RegExp(`/chapter/${c2.id}\\?fs=1$`));
    await expect(fsRoot(page).locator(".fst-sec").nth(2).locator(".fst-sec-head")).toHaveAttribute("aria-expanded", "true");
    await expect(fsRoot(page).locator(".fst-sec").nth(0).locator(".fst-sec-head")).toHaveAttribute("aria-expanded", "true");
  });

  test("переход в главу другого раздела раскрывает её раздел", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const target = course[1]!.chapters[0]!;
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await fsRoot(page).locator(".fst-sec").nth(1).locator(".fst-sec-head").click();
    await fsRoot(page).locator(".slide-fs-toc-item", { hasText: target.title }).click();
    await expect(page).toHaveURL(new RegExp(`/chapter/${target.id}\\?fs=1$`));
    await expect(fsRoot(page).locator(".fst-sec").nth(1).locator(".fst-sec-head")).toHaveAttribute("aria-expanded", "true");
    await expect(fsRoot(page).locator(".fst-sec").nth(1).locator(".slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(target.title);
  });
});

test.describe("вкладки в полном экране", () => {
  test("переключение вкладок сохраняет ?fs=1 и оболочку; пункты дерева — вопросы", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const base = `/book/12/chapter/${ch.id}`;
    const tab = (name: string) => fsRoot(page).locator(".ch-tab", { hasText: name });

    await tab("Вопросы").click();
    await expect(page).toHaveURL(new RegExp(`${base}/questions\\?fs=1$`));
    await expect(fsRoot(page)).toBeVisible();
    await expect(tab("Вопросы")).toHaveClass(/\bon\b/);
    await expect(items(page)).toHaveCount(5); // по пункту на вопрос
    await expect(fsRoot(page).locator(".quiz-q")).toHaveCount(5);

    await tab("Практика").click();
    await expect(page).toHaveURL(new RegExp(`${base}/exercises\\?fs=1$`));
    await expect(fsRoot(page)).toBeVisible();
    await expect(tab("Практика")).toHaveClass(/\bon\b/);

    await tab("Теория").click();
    await expect(page).toHaveURL(new RegExp(`${base}\\?fs=1$`));
    await expect(items(page)).toHaveCount(ch.lessons.length);
    assertCleanBut404(guard);
  });

  test("в шапке вкладки «Теория» — номер слайда, время и «Играть»", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await expect(head(page).locator(".slide-panel-num")).toHaveText(pageNum(ch, 1));
    await expect(head(page).locator(".s-time-mono")).toContainText("0:00 / ");
    await expect(head(page).getByRole("button", { name: "Играть" })).toBeVisible();
    // на других вкладках этих кнопок в шапке нет
    await fsRoot(page).locator(".ch-tab", { hasText: "Вопросы" }).click();
    await expect(head(page).locator(".slide-panel-num")).toHaveCount(0);
  });
});

test.describe("листание стрелками", () => {
  test("→ и ↓ вперёд, ← и ↑ назад, на краях главы стоим", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const num = head(page).locator(".slide-panel-num");
    await page.keyboard.press("ArrowLeft");
    await expect(num).toHaveText(pageNum(ch, 1)); // раньше первого не идём
    await page.keyboard.press("ArrowRight");
    await expect(num).toHaveText(pageNum(ch, 2));
    await page.keyboard.press("ArrowDown");
    await expect(num).toHaveText(pageNum(ch, 3));
    await page.keyboard.press("ArrowLeft");
    await expect(num).toHaveText(pageNum(ch, 2));
    await page.keyboard.press("ArrowUp");
    await expect(num).toHaveText(pageNum(ch, 1));
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("01");

    // до конца и дальше конца
    // каждое нажатие ждёт применения прежнего: адрес меняется асинхронно, и нажатия «без пауз» схлопываются
    for (let i = 1; i < ch.lessons.length; i++) {
      await page.keyboard.press("ArrowRight");
      await expect(num).toHaveText(pageNum(ch, i + 1));
    }
    await expect(num).toHaveText(pageNum(ch, ch.lessons.length));
    await page.keyboard.press("ArrowRight");
    await expect(num).toHaveText(pageNum(ch, ch.lessons.length));
    await expect(onItem(page)).toHaveCount(1);
  });

  test("стрелки в обычном режиме страницы слайды не листают", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(page.locator(".slide-panel")).toBeVisible();
    await page.keyboard.press("ArrowRight");
    await expect(page.locator(".slide-panel-num")).toHaveText(pageNum(ch, 1));
  });
});

test.describe("выход из полного экрана", () => {
  test("«Свернуть» закрывает оболочку и убирает ?fs=1, слайд и вкладка остаются", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await items(page).nth(3).click();
    await head(page).getByRole("button", { name: "Свернуть" }).click();
    await expect(fsRoot(page)).toHaveCount(0);
    await expect.poll(() => search(page)).toBe("?slide=3");
    await expect(page.locator(".slide-panel-num")).toHaveText(pageNum(ch, 4));
    await expect(page.locator(".ch-expand")).toBeVisible();
    await expect.poll(() => page.evaluate(() => document.fullscreenElement?.tagName ?? null)).toBeNull();
  });

  test("Esc закрывает оболочку; вкладка «Вопросы» остаётся открытой", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.goto(`/book/12/chapter/${ch.id}/questions?fs=1`);
    await expect(fsRoot(page)).toBeVisible();
    await expect(fsRoot(page).locator(".quiz-q")).toHaveCount(5);
    await page.keyboard.press("Escape");
    await expect(fsRoot(page)).toHaveCount(0);
    await expect(page).toHaveURL(new RegExp(`/book/12/chapter/${ch.id}/questions$`));
    await expect(page.locator(".ch-tab.on")).toContainText("Вопросы");
    await expect(page.locator(".quiz-q")).toHaveCount(5);
  });

  test("после выхода можно войти в полный экран снова", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await page.locator(".ch-expand").click();
    await expect(fsRoot(page)).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(fsRoot(page)).toHaveCount(0);
    await page.locator(".ch-expand").click();
    await expect(fsRoot(page)).toBeVisible();
    await expect(page).toHaveURL(/\?fs=1$/);
  });

  test("перезагрузка в полном экране возвращает в него же, на тот же слайд", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await items(page).nth(6).click();
    await expect.poll(() => search(page)).toBe("?fs=1&slide=6");
    await page.reload();
    await expect(fsRoot(page)).toBeVisible();
    await expect(head(page).locator(".slide-panel-num")).toHaveText(pageNum(ch, 7));
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("07");
  });
});

test("в полном экране плеер читает по виртуальным часам, окно «За кадром» стоит по центру области оболочки", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await controlClock(page);
  await openFs(page, ch);
  const pop = page.locator(".voice-pop");
  await expect(pop).toBeVisible();
  await expect(pop.locator(".voice-pop-tag")).toHaveText("За кадром");
  // центр окна совпадает с центром колонки `.slide-fs-main`
  const main = (await fsRoot(page).locator(".slide-fs-main").boundingBox())!;
  const box = (await pop.boundingBox())!;
  expect(Math.abs(box.x + box.width / 2 - (main.x + main.width / 2))).toBeLessThan(4);

  await head(page).getByRole("button", { name: "Играть" }).click();
  await expect(head(page).getByRole("button", { name: "Пауза" })).toBeVisible();
  await page.clock.runFor(1000);
  await expect(head(page).locator(".s-time-mono")).toContainText("0:01 / ");
  await expect(pop.locator(".now")).toHaveCount(1);
  await head(page).getByRole("button", { name: "Пауза" }).click();
  await expect(head(page).getByRole("button", { name: "Играть" })).toBeVisible();
});
