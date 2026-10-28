import type { Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import { answerQuiz, controlClock, drafts, DM1, loadChapter, markSlides, progressOf, saveDraft, stored, taskIds } from "../../support/shell";

/* The /settings page: appearance lives in the browser's localStorage and applies at once; progress and account live on the server. */

const sw = (page: Page, name: string) => page.getByRole("switch", { name });
const openSettings = async (page: Page) => {
  await page.goto("/settings");
  await expect(page.locator(".set-card")).toBeVisible();
};

/** Progress to be reset: slides and a quiz answer in book 12, a code draft in book 13. */
async function seedProgress(page: Page, request: import("@playwright/test").APIRequestContext, token: string) {
  const ids = await taskIds(request, 13, 1);
  await markSlides(request, token, 12, DM1.num, [0, 1, 2]);
  await answerQuiz(request, token, 12, DM1.num, 0, 0);
  await saveDraft(request, token, 13, 1, ids[0]!, "print('draft')");
  return ids[0]!;
}

test("settings page: groups and rows", async ({ page, request, guard }) => {
  await loginFresh(page, request);
  await openSettings(page);
  await expect(page.locator(".set-card h2")).toHaveText("Настройки");
  await expect(page.locator(".set-group")).toHaveText(["Аккаунт", "Внешний вид", "Слайды", "Упражнения", "Диаграммы", "Прогресс"]);
  await expect(page.getByRole("switch")).toHaveCount(6);
  for (const name of ["Светлая тема", "Свёрнутое меню разделов", "Автопроигрывание анимаций", "Автопереход к следующему упражнению", "Автосвязывание в «Архитектуре компьютера»", "Автосвязывание в «Системном дизайне»"]) {
    await expect(sw(page, name)).toBeVisible();
  }
  await expect(page.locator(".topbar .btn-icon.on")).toHaveAttribute("title", "Настройки");
  guard.assertClean();
});

test("defaults: dark theme, menu expanded, animations on, auto-advance off, auto-wiring on", async ({ page, request }) => {
  await loginFresh(page, request);
  await openSettings(page);
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "true");
  await expect(sw(page, "Автопереход к следующему упражнению")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Автосвязывание в «Архитектуре компьютера»")).toHaveAttribute("aria-checked", "true");
  await expect(sw(page, "Автосвязывание в «Системном дизайне»")).toHaveAttribute("aria-checked", "true");
  // storage holds only the deviation from the default
  for (const key of ["cs-core-aside-collapsed", "cs-core-anim-auto", "cs-core-auto-next", "cs-core-autowire-lab", "cs-core-autowire-sd"]) {
    expect(await stored(page, key), key).toBeNull();
  }
});

test.describe("theme", () => {
  test("the light theme switch: data-theme, cs-core-theme, header button", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    const html = page.locator("html");
    await sw(page, "Светлая тема").click();
    await expect(html).toHaveAttribute("data-theme", "light");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "cs-core-theme")).toBe("light");
    await expect(page.getByRole("button", { name: "Переключить тему" })).toHaveAttribute("title", "Тёмная тема");

    await sw(page, "Светлая тема").click();
    await expect(html).toHaveAttribute("data-theme", "dark");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "cs-core-theme")).toBe("dark");
    await expect(page.getByRole("button", { name: "Переключить тему" })).toHaveAttribute("title", "Светлая тема");
  });

  test("the header theme button and the page switch stay in sync", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "true");
  });

  test("the theme changes page colours and survives a reload", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    const bg = () => page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const dark = await bg();
    await sw(page, "Светлая тема").click();
    await expect.poll(bg).not.toBe(dark);
    const light = await bg();
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "true");
    expect(await bg()).toBe(light);
  });
});

test.describe("collapsed menu", () => {
  test("the switch collapses the sections menu and writes cs-core-aside-collapsed", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await sw(page, "Свёрнутое меню разделов").click();
    await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
    await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "cs-core-aside-collapsed")).toBe("1");
    await page.reload();
    await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
    await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "true");
    await sw(page, "Свёрнутое меню разделов").click();
    await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
    expect(await stored(page, "cs-core-aside-collapsed")).toBeNull();
  });
});

test.describe("animation autoplay", () => {
  const chips = (page: Page) => page.locator(".slide-stage .a-chip");
  const current = (page: Page) => chips(page).evaluateAll((els) => els.findIndex((e) => e.classList.contains("on")));

  test("the toggle writes cs-core-anim-auto=0 and restores the default", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await sw(page, "Автопроигрывание анимаций").click();
    await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "cs-core-anim-auto")).toBe("0");
    await page.reload();
    await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "false");
    await sw(page, "Автопроигрывание анимаций").click();
    expect(await stored(page, "cs-core-anim-auto")).toBeNull();
  });

  test("on: the scene starts at the first step and walks through steps on a timer", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await controlClock(page);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(chips(page).first()).toBeVisible();
    const n = await chips(page).count();
    expect(n).toBeGreaterThan(1);
    expect(await current(page)).toBe(0);
    await page.clock.runFor(60_000);
    await expect.poll(() => current(page)).toBe(n - 1); // reached the final state
  });

  test("off: the scene shows the final state at once and does not move, steps are switched manually", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.addInitScript(() => window.localStorage.setItem("cs-core-anim-auto", "0"));
    await controlClock(page);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(chips(page).first()).toBeVisible();
    const n = await chips(page).count();
    expect(await current(page)).toBe(n - 1);
    await page.clock.runFor(30_000);
    expect(await current(page)).toBe(n - 1);
    // manual step selection works
    await chips(page).first().click();
    expect(await current(page)).toBe(0);
    await page.clock.runFor(30_000);
    expect(await current(page)).toBe(0);
  });
});

test.describe("exercises and diagrams", () => {
  test("auto-advance: off by default, writes cs-core-auto-next=1 when turned on", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    const row = sw(page, "Автопереход к следующему упражнению");
    await expect(row).toHaveAttribute("aria-checked", "false");
    await row.click();
    await expect(row).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "cs-core-auto-next")).toBe("1");
    await page.reload();
    await expect(row).toHaveAttribute("aria-checked", "true");
    await row.click();
    await expect(row).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "cs-core-auto-next")).toBeNull();
  });

  for (const [name, key] of [
    ["Автосвязывание в «Архитектуре компьютера»", "cs-core-autowire-lab"],
    ["Автосвязывание в «Системном дизайне»", "cs-core-autowire-sd"],
  ] as const) {
    test(`${name}: on by default, when off it is stored as "0" in ${key}`, async ({ page, request }) => {
      await loginFresh(page, request);
      await openSettings(page);
      const row = sw(page, name);
      await expect(row).toHaveAttribute("aria-checked", "true");
      await row.click();
      await expect(row).toHaveAttribute("aria-checked", "false");
      expect(await stored(page, key)).toBe("0");
      // the two settings are independent
      const other = key === "cs-core-autowire-lab" ? "cs-core-autowire-sd" : "cs-core-autowire-lab";
      expect(await stored(page, other)).toBeNull();
      await page.reload();
      await expect(sw(page, name)).toHaveAttribute("aria-checked", "false");
      await sw(page, name).click();
      await expect(sw(page, name)).toHaveAttribute("aria-checked", "true");
      expect(await stored(page, key)).toBeNull();
    });
  }
});

test.describe("account", () => {
  test("name and email are shown, Sign out returns to the login form", async ({ page, request }) => {
    test.skip(!!process.env.E2E_USER, "in prebuilt-stack mode we sign in as a given user: the name is not E2E");
    const { email, token } = await loginFresh(page, request);
    await openSettings(page);
    const row = page.locator(".set-row").filter({ has: page.getByRole("button", { name: "Выйти" }) });
    await expect(row).toContainText("E2E");
    await expect(row).toContainText(email);
    await row.getByRole("button", { name: "Выйти" }).click();
    await expect(page.locator(".auth-card")).toBeVisible();
    expect(await stored(page, "cs-core-token")).toBeNull();
    expect((await request.get("/api/progress", { headers: bearer(token) })).status()).toBe(401);
  });
});

test.describe("progress reset", () => {
  test("Reset exercise progress: declining the confirmation deletes nothing", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    const task = await seedProgress(page, request, token);
    await openSettings(page);
    let message = "";
    page.once("dialog", (d) => {
      message = d.message();
      void d.dismiss();
    });
    await page.getByRole("button", { name: "Сбросить", exact: true }).click();
    await expect.poll(() => message).toBe("Удалить решения, черновики и историю попыток во всех упражнениях?");
    await expect(page.locator(".set-done")).toHaveCount(0);
    expect((await drafts(request, token, 13, 1))[task]).toBe("print('draft')");
  });

  test("Reset exercise progress: drafts removed, slides and questions intact", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await seedProgress(page, request, token);
    await openSettings(page);
    page.once("dialog", (d) => void d.accept());
    await page.getByRole("button", { name: "Сбросить", exact: true }).click();
    await expect(page.locator(".set-done")).toHaveText("Готово.");
    await expect(page.locator(".set-done")).toHaveCount(1);
    expect(await drafts(request, token, 13, 1)).toEqual({});
    const p = await progressOf(request, token);
    expect(p.slides[`12:${DM1.num}`]).toEqual([0, 1, 2]);
    expect(p.quiz[`12:${DM1.num}`]?.[0]).toBe(0);
  });

  test("Reset all progress: confirmation, everything zeroed on the server and on the home page", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await seedProgress(page, request, token);
    await page.goto("/");
    await expect(page.locator(".dash-all")).not.toContainText("0% · 0 из"); // three viewed slides are visible
    await page.getByRole("button", { name: "Настройки" }).click();
    await expect(page.locator(".set-card")).toBeVisible();
    let message = "";
    page.once("dialog", (d) => {
      message = d.message();
      void d.accept();
    });
    await page.getByRole("button", { name: "Сбросить всё" }).click();
    await expect.poll(() => message).toBe("Обнулить весь прогресс: слайды, вопросы и упражнения?");
    await expect(page.locator(".set-done")).toHaveText("Готово.");

    const p = await progressOf(request, token);
    expect(p.slides).toEqual({});
    expect(p.quiz).toEqual({});
    expect(p.answers).toEqual({});
    expect(p.code).toEqual({});
    expect(await drafts(request, token, 13, 1)).toEqual({});

    // the dashboard is clean at once, without a reload
    await page.locator(".logo").click();
    await expect(page.locator(".dash-all")).toContainText("0% · 0 из");
    await expect(page.locator(".dash-bar-num").first()).toHaveText(/^0\//);
  });

  test("Reset all progress: declining the confirmation keeps progress", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await seedProgress(page, request, token);
    await openSettings(page);
    let seen = false;
    page.once("dialog", (d) => {
      seen = true;
      void d.dismiss();
    });
    await page.getByRole("button", { name: "Сбросить всё" }).click();
    await expect.poll(() => seen).toBe(true);
    await expect(page.locator(".set-done")).toHaveCount(0);
    const p = await progressOf(request, token);
    expect(p.slides[`12:${DM1.num}`]).toEqual([0, 1, 2]);
  });

  test("reset does not touch another user's progress", async ({ page, request, browser }) => {
    test.skip(!!process.env.E2E_USER, "in prebuilt-stack mode there is no second user (registration is restricted)");
    const mine = await loginFresh(page, request);
    await seedProgress(page, request, mine.token);
    // a second user with their own progress
    const ctx = await browser.newContext();
    const otherPage = await ctx.newPage();
    const other = await loginFresh(otherPage, ctx.request, "other");
    await markSlides(ctx.request, other.token, 12, DM1.num, [0, 1]);
    await openSettings(page);
    page.once("dialog", (d) => void d.accept());
    await page.getByRole("button", { name: "Сбросить всё" }).click();
    await expect(page.locator(".set-done")).toBeVisible();
    expect((await progressOf(request, other.token)).slides[`12:${DM1.num}`]).toEqual([0, 1]);
    await ctx.close();
  });
});

test.describe("colour themes", () => {
  const card = (page: Page, name: string) => page.getByRole("button", { name: new RegExp(`^${name}`) });
  const html = (page: Page) => page.locator("html");
  const cssVar = (page: Page, name: string) => page.evaluate((n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim(), name);

  test("cards: seven dark and five light, Dark selected by default", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await expect(page.locator(".palette-group").nth(0).locator(".palette-card")).toHaveCount(7);
    await expect(page.locator(".palette-group").nth(1).locator(".palette-card")).toHaveCount(5);
    await expect(card(page, "Тёмная")).toHaveAttribute("aria-pressed", "true");
    await expect(card(page, "Светлая")).toHaveAttribute("aria-pressed", "false");
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
  });

  test("choosing a theme paints the page and editor and is remembered; dark and light are stored separately", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Dracula").click();
    await expect(html(page)).toHaveAttribute("data-theme", "dark");
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    expect(await stored(page, "cs-core-palette-dark")).toBe("dracula");
    expect(await cssVar(page, "--bg")).toBe("#282a36");
    await expect(page.locator("body")).toHaveCSS("background-color", "rgb(40, 42, 54)");
    await expect(card(page, "Dracula")).toHaveAttribute("aria-pressed", "true");

    // choosing a light theme switches the mode; the dark choice stays remembered
    await card(page, "GitHub Light").click();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");
    expect(await stored(page, "cs-core-theme")).toBe("light");
    expect(await stored(page, "cs-core-palette-light")).toBe("github-light");
    expect(await stored(page, "cs-core-palette-dark")).toBe("dracula");
    await expect(card(page, "Dracula")).toHaveAttribute("aria-pressed", "false");

    // the header button returns to dark mode with the same theme
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html(page)).toHaveAttribute("data-theme", "dark");
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");

    // after a reload the theme is in place (even before the app starts: a script in index.html sets it)
    await page.reload();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");
    await expect(page.locator(".set-card")).toBeVisible();
    await expect(card(page, "GitHub Light")).toHaveAttribute("aria-pressed", "true");
  });

  test("the default theme removes the attribute and clears the entry", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Nord").click();
    await expect(html(page)).toHaveAttribute("data-palette", "nord");
    await card(page, "Тёмная").click();
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
    expect(await stored(page, "cs-core-palette-dark")).toBeNull();
    expect(await cssVar(page, "--bg")).toBe("#0f1115");
  });

  test("an unknown value in storage is ignored", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.addInitScript(() => window.localStorage.setItem("cs-core-palette-dark", "no-such-theme"));
    await openSettings(page);
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
    await expect(card(page, "Тёмная")).toHaveAttribute("aria-pressed", "true");
  });

  test("a card shows its own theme regardless of the current one: background and code colours", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    // light mode is on now, yet the Dracula card is still dark; the keyword in the code sample is pink, as in Dracula
    await sw(page, "Светлая тема").click();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    const dracula = card(page, "Dracula");
    await expect(dracula).toHaveCSS("background-color", "rgb(40, 42, 54)");
    await expect(dracula.locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(255, 121, 198)");
    await expect(card(page, "One Light")).toHaveCSS("background-color", "rgb(250, 250, 250)");
  });

  test("default theme cards do not inherit the active theme's code colours", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Dracula").click();
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    // the Light card keeps the original blue keyword, not Dracula's pink
    await expect(card(page, "Светлая").locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(47, 107, 176)");
    await expect(card(page, "Тёмная").locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(130, 184, 232)");
  });
});
