import { expect, loginFresh, test } from "../../support/fixtures";
import { loadChapter, DM1, stored } from "../../support/shell";

/* Two interface languages: English text is the translation key, Russian lives in the dictionary; a switch in the header; the content of a translated
   book ("Дискретная математика") comes from the server in the request language, other books stay Russian with an "RU" tag. */

const KEY = "cs-core-lang";

test("the browser language picks the interface language, a saved choice takes priority", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Разделы"); // the test browser's locale is ru-RU
  await expect(page.locator("html")).toHaveAttribute("lang", "ru");

  await page.evaluate((k) => window.localStorage.setItem(k, "en"), KEY);
  await page.reload();
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Sections");
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await expect(page.getByTitle("Settings")).toBeVisible();
});

test("the EN / RU switch remembers the language and reloads the page", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.goto("/");
  const switcher = page.locator(".topbar .lang-switch");
  await expect(switcher.locator(".lang-btn.on")).toHaveText("RU");
  await switcher.getByRole("button", { name: "EN" }).click();
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Sections");
  expect(await stored(page, KEY)).toBe("en");
  await expect(switcher.locator(".lang-btn.on")).toHaveText("EN");

  await switcher.getByRole("button", { name: "RU" }).click();
  await expect(page.locator(".sidebar .aside-head .s-label")).toHaveText("Разделы");
  expect(await stored(page, KEY)).toBe("ru");
});

test("translated books are fully English, without the \"RU\" tag", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "en"), KEY);
  await page.goto("/");

  const menu = page.locator(".sidebar .menu .slide-fs-toc-item");
  const dm = menu.filter({ hasText: "Discrete Mathematics" });
  await expect(dm).toHaveCount(1);
  await expect(dm.locator(".lang-tag")).toHaveCount(0); // it exists in English, so there is no tag
  const py = menu.filter({ hasText: "Python as a First Language" });
  await expect(py.locator(".lang-tag")).toHaveCount(0);
  await expect(menu.locator(".lang-tag")).toHaveCount(0); // all course books exist in English

  // section and chapter of a translated book
  await dm.click();
  await expect(page.locator(".lang-note")).toHaveCount(0);
  await expect(page.locator(".topics-title").first()).toHaveText("The language of mathematics");
  const ch = await loadChapter(request, DM1);
  await page.goto(`/book/12/chapter/${ch.id}`);
  await expect(page.getByRole("heading", { name: /^Lesson 1\. Sets: the language of mathematics$/ })).toBeVisible();
  await expect(page.locator(".ch-tabs, .chapter-tabs, .tabs").getByText("Theory").first()).toBeVisible();
  await expect(page.locator(".voice-pop-text")).toContainText("Discrete mathematics. Chapter 1.");

  // questions and exercises are in English too
  await page.goto(`/book/12/chapter/${ch.id}/questions`);
  await expect(page.locator(".quiz-head h3")).toHaveText("Quiz: sets");
  await expect(page.locator(".quiz").getByText("How does a set differ from a list?")).toBeVisible();

});

test("the \"Python\" book is English: text, slides, questions and task statements", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "en"), KEY);
  const ch = await loadChapter(request, { book: 13, num: 5 });
  await page.goto(`/book/13/chapter/${ch.id}`);
  await expect(page.locator(".voice-pop-text")).toContainText("Python as a first language. Chapter 5.");
  await expect(page.locator(".np-card, .slide-title, h2").first()).toBeVisible();

  await page.goto(`/book/13/chapter/${ch.id}/questions`);
  await expect(page.locator(".quiz-head h3")).not.toHaveText(/[А-Яа-я]/);

  await page.goto(`/book/13/chapter/${ch.id}/exercises`);
  const statement = page.locator(".pr-statement").first();
  await expect(statement).toBeVisible();
  await expect(statement).not.toContainText(/Напишите|Дан список|Допишите/);
});

test("labs are English: interface, statements and node names", async ({ page, request }) => {
  await loginFresh(page, request);
  await page.addInitScript((k) => window.localStorage.setItem(k, "en"), KEY);
  for (const [book, num] of [[18, 1], [14, 6], [15, 1], [17, 2]] as const) {
    const ch = await loadChapter(request, { book, num });
    await page.goto(`/book/${book}/chapter/${ch.id}/exercises`);
    await expect(page.locator(".pr-statement").first()).toBeVisible();
    // everything the lab itself draws is English: strip statements, exercise titles and scenario data (node names, goals)
    const russian = await page.evaluate(() => {
      const root = document.querySelector(".pr-main") ?? document.body;
      const bits: string[] = [];
      root.querySelectorAll("button, label, th, h3, h4, summary, [title], [aria-label], [placeholder]").forEach((e) => {
        if (e.closest(".pr-statement, .pr-item, .pr-head, svg, textarea, .cm-editor")) return;
        bits.push(e.getAttribute("title") ?? "", e.getAttribute("aria-label") ?? "", e.getAttribute("placeholder") ?? "");
        if (e.children.length === 0) bits.push(e.textContent ?? "");
      });
      return bits.filter((t) => /[А-Яа-яЁё]{3}/.test(t)).slice(0, 8);
    });
    expect(russian, `chapter ${book}:${num}`).toEqual([]);
    await expect(page.locator(".pr-statement").first()).not.toContainText(/[А-Яа-яЁё]{3}/);
  }
});
