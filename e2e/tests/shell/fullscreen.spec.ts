import type { Page } from "@playwright/test";
import { expect, loginFresh, test } from "../../support/fixtures";
import { assertCleanBut404, controlClock, courseOf, DM1, loadChapter, type ChapterDto } from "../../support/shell";

/* Chapter fullscreen mode: the `.slide-fs` shell (tree, header with tabs, content), state in the `?fs=1` address. */

const fsRoot = (page: Page) => page.locator(".slide-fs");
const items = (page: Page) => fsRoot(page).locator(".fst-slide");
const onItem = (page: Page) => fsRoot(page).locator(".fst-slide.on");
const head = (page: Page) => fsRoot(page).locator(".slide-fs-head");
const search = (page: Page) => new URL(page.url()).search;

/** Opens a chapter straight in fullscreen and waits until the tab puts its items into the tree. */
async function openFs(page: Page, ch: ChapterDto, query = "") {
  await page.goto(`/book/12/chapter/${ch.id}?fs=1${query}`);
  await expect(fsRoot(page)).toBeVisible();
  await expect(items(page)).toHaveCount(ch.lessons.length);
}

const pageNum = (ch: ChapterDto, n: number) => `${String(n).padStart(2, "0")} / ${String(ch.lessons.length).padStart(2, "0")}`;

test("the \"Весь экран\" button opens the shell: ?fs=1 address, native fullscreen, tree and header", async ({ page, request, guard }) => {
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
  // there is no "Весь экран" button in fullscreen
  await expect(fsRoot(page).locator(".ch-expand")).toHaveCount(0);
  assertCleanBut404(guard);
});

test("visiting the ?fs=1 address shows the shell with tabs at once", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await openFs(page, ch);
  await expect(fsRoot(page).locator(".ch-tab")).toHaveCount(3);
  await expect(fsRoot(page).locator(".ch-tab.on")).toHaveText("Теория");
  // tab links keep ?fs=1
  const base = `/book/12/chapter/${ch.id}`;
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Теория" })).toHaveAttribute("href", `${base}?fs=1`);
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Вопросы" })).toHaveAttribute("href", `${base}/questions?fs=1`);
  await expect(fsRoot(page).locator(".ch-tab", { hasText: "Практика" })).toHaveAttribute("href", `${base}/exercises?fs=1`);
});

test.describe("tree of sections and chapters", () => {
  test("book sections; the section of the current chapter is expanded, the rest are collapsed; the current chapter is marked", async ({ page, request }) => {
    await loginFresh(page, request);
    const course = await courseOf(request, 12);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const heads = fsRoot(page).locator(".fst-sec-head");
    await expect(heads).toHaveCount(course.length);
    await expect(heads).toHaveText(course.map((s) => new RegExp(s.title, "i")));
    await expect(heads.nth(0)).toHaveAttribute("aria-expanded", "true");
    for (let i = 1; i < course.length; i++) await expect(heads.nth(i)).toHaveAttribute("aria-expanded", "false");
    // chapters of the expanded section are visible, the current one is marked
    const first = course[0]!.chapters;
    const sec0 = fsRoot(page).locator(".fst-sec").nth(0);
    await expect(sec0.locator(".slide-fs-toc-item")).toHaveCount(first.length);
    await expect(sec0.locator(".slide-fs-toc-item.on")).toHaveCount(1);
    await expect(sec0.locator(".slide-fs-toc-item.on .slide-fs-toc-name")).toHaveText(ch.title);
    // chapters of a collapsed section are hidden
    await expect(fsRoot(page).locator(".fst-sec").nth(1).locator(".slide-fs-toc-item").first()).toBeHidden();
  });

  test("a section heading expands and collapses its chapters", async ({ page, request }) => {
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

  test("under the current chapter there are slide items with titles, the current slide is marked", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await expect(items(page)).toHaveCount(ch.lessons.length);
    await expect(onItem(page)).toHaveCount(1);
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("01");
    for (const name of await items(page).locator(".fst-slide-name").allInnerTexts()) expect(name.trim()).not.toBe("");
    // items sit in the tree under their chapter
    await expect(fsRoot(page).locator(".fst-sec").nth(0).locator(".fst-slide")).toHaveCount(ch.lessons.length);
  });

  test("clicking a slide item shows it: number, ?slide= in the address, mark", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await items(page).nth(4).click();
    await expect(head(page).locator(".slide-panel-num")).toHaveText(pageNum(ch, 5));
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("05");
    await expect.poll(() => search(page)).toBe("?fs=1&slide=4");
    await expect(page.locator(".slide-fs-stage .s-title")).toBeVisible();
  });

  test("clicking another chapter opens its theory in fullscreen", async ({ page, request }) => {
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

  test("going to another chapter from the \"Вопросы\" tab opens \"Теория\"", async ({ page, request }) => {
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

  test("expanded sections survive moving to another chapter", async ({ page, request }) => {
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

  test("going to a chapter of another section expands that section", async ({ page, request }) => {
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

test.describe("tabs in fullscreen", () => {
  test("switching tabs keeps ?fs=1 and the shell; tree items are questions", async ({ page, request, guard }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const base = `/book/12/chapter/${ch.id}`;
    const tab = (name: string) => fsRoot(page).locator(".ch-tab", { hasText: name });

    await tab("Вопросы").click();
    await expect(page).toHaveURL(new RegExp(`${base}/questions\\?fs=1$`));
    await expect(fsRoot(page)).toBeVisible();
    await expect(tab("Вопросы")).toHaveClass(/\bon\b/);
    await expect(items(page)).toHaveCount(5); // one item per question
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

  test("the \"Теория\" tab header has the slide number, time and \"Играть\"", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    await expect(head(page).locator(".slide-panel-num")).toHaveText(pageNum(ch, 1));
    await expect(head(page).locator(".s-time-mono")).toContainText("0:00 / ");
    await expect(head(page).getByRole("button", { name: "Играть" })).toBeVisible();
    // on other tabs the header has no such buttons
    await fsRoot(page).locator(".ch-tab", { hasText: "Вопросы" }).click();
    await expect(head(page).locator(".slide-panel-num")).toHaveCount(0);
  });
});

test.describe("arrow-key paging", () => {
  test("right and down go forward, left and up go back, at chapter edges we stay", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await openFs(page, ch);
    const num = head(page).locator(".slide-panel-num");
    await page.keyboard.press("ArrowLeft");
    await expect(num).toHaveText(pageNum(ch, 1)); // we do not go before the first one
    await page.keyboard.press("ArrowRight");
    await expect(num).toHaveText(pageNum(ch, 2));
    await page.keyboard.press("ArrowDown");
    await expect(num).toHaveText(pageNum(ch, 3));
    await page.keyboard.press("ArrowLeft");
    await expect(num).toHaveText(pageNum(ch, 2));
    await page.keyboard.press("ArrowUp");
    await expect(num).toHaveText(pageNum(ch, 1));
    await expect(onItem(page).locator(".fst-slide-num")).toHaveText("01");

    // to the end and beyond
    // each press waits for the previous one to apply: the address changes asynchronously and presses without pauses collapse
    for (let i = 1; i < ch.lessons.length; i++) {
      await page.keyboard.press("ArrowRight");
      await expect(num).toHaveText(pageNum(ch, i + 1));
    }
    await expect(num).toHaveText(pageNum(ch, ch.lessons.length));
    await page.keyboard.press("ArrowRight");
    await expect(num).toHaveText(pageNum(ch, ch.lessons.length));
    await expect(onItem(page)).toHaveCount(1);
  });

  test("arrows do not page slides in the normal page mode", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(page.locator(".slide-panel")).toBeVisible();
    await page.keyboard.press("ArrowRight");
    await expect(page.locator(".slide-panel-num")).toHaveText(pageNum(ch, 1));
  });
});

test.describe("leaving fullscreen", () => {
  test("\"Свернуть\" closes the shell and removes ?fs=1, the slide and tab stay", async ({ page, request }) => {
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

  test("Esc closes the shell; the \"Вопросы\" tab stays open", async ({ page, request }) => {
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

  test("after leaving, fullscreen can be entered again", async ({ page, request }) => {
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

  test("a reload in fullscreen returns to it, on the same slide", async ({ page, request }) => {
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

test("in fullscreen the player reads by virtual clock, the \"За кадром\" window is centered in the shell area", async ({ page, request }) => {
  await loginFresh(page, request);
  const ch = await loadChapter(request, DM1);
  await controlClock(page);
  await openFs(page, ch);
  const pop = page.locator(".voice-pop");
  await expect(pop).toBeVisible();
  await expect(pop.locator(".voice-pop-tag")).toHaveText("За кадром");
  // the window center matches the center of the `.slide-fs-main` column
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
