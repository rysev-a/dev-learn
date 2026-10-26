import type { Page } from "@playwright/test";
import { bearer, expect, loginFresh, test } from "../../support/fixtures";
import { answerQuiz, controlClock, drafts, DM1, loadChapter, markSlides, progressOf, saveDraft, stored, taskIds } from "../../support/shell";

/* Страница /settings: внешний вид — в localStorage браузера и применяется сразу, прогресс и аккаунт — на сервере. */

const sw = (page: Page, name: string) => page.getByRole("switch", { name });
const openSettings = async (page: Page) => {
  await page.goto("/settings");
  await expect(page.locator(".set-card")).toBeVisible();
};

/** Прогресс «для сброса»: слайды и ответ квиза в книге 12, черновик кода в книге 13. */
async function seedProgress(page: Page, request: import("@playwright/test").APIRequestContext, token: string) {
  const ids = await taskIds(request, 13, 1);
  await markSlides(request, token, 12, DM1.num, [0, 1, 2]);
  await answerQuiz(request, token, 12, DM1.num, 0, 0);
  await saveDraft(request, token, 13, 1, ids[0]!, "print('draft')");
  return ids[0]!;
}

test("страница настроек: группы и строки", async ({ page, request, guard }) => {
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

test("значения по умолчанию: тёмная тема, меню развёрнуто, анимации включены, автопереход выключен, автосвязывание включено", async ({ page, request }) => {
  await loginFresh(page, request);
  await openSettings(page);
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "true");
  await expect(sw(page, "Автопереход к следующему упражнению")).toHaveAttribute("aria-checked", "false");
  await expect(sw(page, "Автосвязывание в «Архитектуре компьютера»")).toHaveAttribute("aria-checked", "true");
  await expect(sw(page, "Автосвязывание в «Системном дизайне»")).toHaveAttribute("aria-checked", "true");
  // в хранилище лежит только отклонение от умолчания
  for (const key of ["say-aside-collapsed", "say-anim-auto", "say-auto-next", "say-autowire-lab", "say-autowire-sd"]) {
    expect(await stored(page, key), key).toBeNull();
  }
});

test.describe("тема", () => {
  test("переключатель «Светлая тема»: data-theme, say-theme, кнопка в шапке", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    const html = page.locator("html");
    await sw(page, "Светлая тема").click();
    await expect(html).toHaveAttribute("data-theme", "light");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "say-theme")).toBe("light");
    await expect(page.getByRole("button", { name: "Переключить тему" })).toHaveAttribute("title", "Тёмная тема");

    await sw(page, "Светлая тема").click();
    await expect(html).toHaveAttribute("data-theme", "dark");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "say-theme")).toBe("dark");
    await expect(page.getByRole("button", { name: "Переключить тему" })).toHaveAttribute("title", "Светлая тема");
  });

  test("кнопка темы в шапке и переключатель на странице синхронны", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    await expect(sw(page, "Светлая тема")).toHaveAttribute("aria-checked", "true");
  });

  test("тема меняет цвета страницы и переживает перезагрузку", async ({ page, request }) => {
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

test.describe("свёрнутое меню", () => {
  test("переключатель сворачивает меню разделов и пишет say-aside-collapsed", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await sw(page, "Свёрнутое меню разделов").click();
    await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
    await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "say-aside-collapsed")).toBe("1");
    await page.reload();
    await expect(page.locator(".sidebar")).toHaveClass(/collapsed/);
    await expect(sw(page, "Свёрнутое меню разделов")).toHaveAttribute("aria-checked", "true");
    await sw(page, "Свёрнутое меню разделов").click();
    await expect(page.locator(".sidebar")).not.toHaveClass(/collapsed/);
    expect(await stored(page, "say-aside-collapsed")).toBeNull();
  });
});

test.describe("автопроигрывание анимаций", () => {
  const chips = (page: Page) => page.locator(".slide-stage .a-chip");
  const current = (page: Page) => chips(page).evaluateAll((els) => els.findIndex((e) => e.classList.contains("on")));

  test("выключатель пишет say-anim-auto=0 и возвращает умолчание", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await sw(page, "Автопроигрывание анимаций").click();
    await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "say-anim-auto")).toBe("0");
    await page.reload();
    await expect(sw(page, "Автопроигрывание анимаций")).toHaveAttribute("aria-checked", "false");
    await sw(page, "Автопроигрывание анимаций").click();
    expect(await stored(page, "say-anim-auto")).toBeNull();
  });

  test("включено: схема начинает с первого шага и сама проходит шаги по таймеру", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await controlClock(page);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(chips(page).first()).toBeVisible();
    const n = await chips(page).count();
    expect(n).toBeGreaterThan(1);
    expect(await current(page)).toBe(0);
    await page.clock.runFor(60_000);
    await expect.poll(() => current(page)).toBe(n - 1); // дошла до итога
  });

  test("выключено: схема сразу показывает итог и не движется, шаги переключаются вручную", async ({ page, request }) => {
    await loginFresh(page, request);
    const ch = await loadChapter(request, DM1);
    await page.addInitScript(() => window.localStorage.setItem("say-anim-auto", "0"));
    await controlClock(page);
    await page.goto(`/book/12/chapter/${ch.id}`);
    await expect(chips(page).first()).toBeVisible();
    const n = await chips(page).count();
    expect(await current(page)).toBe(n - 1);
    await page.clock.runFor(30_000);
    expect(await current(page)).toBe(n - 1);
    // ручной выбор шага работает
    await chips(page).first().click();
    expect(await current(page)).toBe(0);
    await page.clock.runFor(30_000);
    expect(await current(page)).toBe(0);
  });
});

test.describe("упражнения и диаграммы", () => {
  test("автопереход: выключен по умолчанию, при включении пишет say-auto-next=1", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    const row = sw(page, "Автопереход к следующему упражнению");
    await expect(row).toHaveAttribute("aria-checked", "false");
    await row.click();
    await expect(row).toHaveAttribute("aria-checked", "true");
    expect(await stored(page, "say-auto-next")).toBe("1");
    await page.reload();
    await expect(row).toHaveAttribute("aria-checked", "true");
    await row.click();
    await expect(row).toHaveAttribute("aria-checked", "false");
    expect(await stored(page, "say-auto-next")).toBeNull();
  });

  for (const [name, key] of [
    ["Автосвязывание в «Архитектуре компьютера»", "say-autowire-lab"],
    ["Автосвязывание в «Системном дизайне»", "say-autowire-sd"],
  ] as const) {
    test(`${name}: включено по умолчанию, выключенное хранится как «0» в ${key}`, async ({ page, request }) => {
      await loginFresh(page, request);
      await openSettings(page);
      const row = sw(page, name);
      await expect(row).toHaveAttribute("aria-checked", "true");
      await row.click();
      await expect(row).toHaveAttribute("aria-checked", "false");
      expect(await stored(page, key)).toBe("0");
      // независимость двух настроек
      const other = key === "say-autowire-lab" ? "say-autowire-sd" : "say-autowire-lab";
      expect(await stored(page, other)).toBeNull();
      await page.reload();
      await expect(sw(page, name)).toHaveAttribute("aria-checked", "false");
      await sw(page, name).click();
      await expect(sw(page, name)).toHaveAttribute("aria-checked", "true");
      expect(await stored(page, key)).toBeNull();
    });
  }
});

test.describe("аккаунт", () => {
  test("показаны имя и email, «Выйти» возвращает на форму входа", async ({ page, request }) => {
    test.skip(!!process.env.E2E_USER, "в режиме готового стека входим заданным пользователем: имя не «E2E»");
    const { email, token } = await loginFresh(page, request);
    await openSettings(page);
    const row = page.locator(".set-row").filter({ has: page.getByRole("button", { name: "Выйти" }) });
    await expect(row).toContainText("E2E");
    await expect(row).toContainText(email);
    await row.getByRole("button", { name: "Выйти" }).click();
    await expect(page.locator(".auth-card")).toBeVisible();
    expect(await stored(page, "say-token")).toBeNull();
    expect((await request.get("/api/progress", { headers: bearer(token) })).status()).toBe(401);
  });
});

test.describe("сброс прогресса", () => {
  test("«Сбросить прогресс упражнений»: отказ в подтверждении ничего не удаляет", async ({ page, request }) => {
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

  test("«Сбросить прогресс упражнений»: черновики удалены, слайды и вопросы целы", async ({ page, request }) => {
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

  test("«Сбросить весь прогресс»: подтверждение, всё обнуляется на сервере и на главной", async ({ page, request }) => {
    const { token } = await loginFresh(page, request);
    await seedProgress(page, request, token);
    await page.goto("/");
    await expect(page.locator(".dash-all")).not.toContainText("0% · 0 из"); // три просмотренных слайда видны
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

    // дашборд сразу чистый, без перезагрузки
    await page.locator(".logo").click();
    await expect(page.locator(".dash-all")).toContainText("0% · 0 из");
    await expect(page.locator(".dash-bar-num").first()).toHaveText(/^0\//);
  });

  test("«Сбросить весь прогресс»: отказ в подтверждении оставляет прогресс", async ({ page, request }) => {
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

  test("сброс не трогает прогресс другого пользователя", async ({ page, request, browser }) => {
    test.skip(!!process.env.E2E_USER, "в режиме готового стека второго пользователя нет (регистрации ограничены)");
    const mine = await loginFresh(page, request);
    await seedProgress(page, request, mine.token);
    // второй пользователь с собственным прогрессом
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

test.describe("цветовые темы", () => {
  const card = (page: Page, name: string) => page.getByRole("button", { name: new RegExp(`^${name}`) });
  const html = (page: Page) => page.locator("html");
  const cssVar = (page: Page, name: string) => page.evaluate((n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim(), name);

  test("карточки: семь тёмных и пять светлых, по умолчанию выбрана «Тёмная»", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await expect(page.locator(".palette-group").nth(0).locator(".palette-card")).toHaveCount(7);
    await expect(page.locator(".palette-group").nth(1).locator(".palette-card")).toHaveCount(5);
    await expect(card(page, "Тёмная")).toHaveAttribute("aria-pressed", "true");
    await expect(card(page, "Светлая")).toHaveAttribute("aria-pressed", "false");
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
  });

  test("выбор темы красит страницу, редактор и запоминается; тёмная и светлая хранятся отдельно", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Dracula").click();
    await expect(html(page)).toHaveAttribute("data-theme", "dark");
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    expect(await stored(page, "say-palette-dark")).toBe("dracula");
    expect(await cssVar(page, "--bg")).toBe("#282a36");
    await expect(page.locator("body")).toHaveCSS("background-color", "rgb(40, 42, 54)");
    await expect(card(page, "Dracula")).toHaveAttribute("aria-pressed", "true");

    // выбор светлой темы переключает режим; тёмная остаётся запомненной
    await card(page, "GitHub Light").click();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");
    expect(await stored(page, "say-theme")).toBe("light");
    expect(await stored(page, "say-palette-light")).toBe("github-light");
    expect(await stored(page, "say-palette-dark")).toBe("dracula");
    await expect(card(page, "Dracula")).toHaveAttribute("aria-pressed", "false");

    // кнопка в шапке возвращает в тёмный режим с той же темой
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html(page)).toHaveAttribute("data-theme", "dark");
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");

    // после перезагрузки тема на месте (в том числе до запуска приложения: её ставит скрипт в index.html)
    await page.reload();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    await expect(html(page)).toHaveAttribute("data-palette", "github-light");
    await expect(page.locator(".set-card")).toBeVisible();
    await expect(card(page, "GitHub Light")).toHaveAttribute("aria-pressed", "true");
  });

  test("тема по умолчанию снимает атрибут и очищает запись", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Nord").click();
    await expect(html(page)).toHaveAttribute("data-palette", "nord");
    await card(page, "Тёмная").click();
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
    expect(await stored(page, "say-palette-dark")).toBeNull();
    expect(await cssVar(page, "--bg")).toBe("#0f1115");
  });

  test("неизвестное значение в хранилище игнорируется", async ({ page, request }) => {
    await loginFresh(page, request);
    await page.addInitScript(() => window.localStorage.setItem("say-palette-dark", "no-such-theme"));
    await openSettings(page);
    await expect(html(page)).not.toHaveAttribute("data-palette", /.+/);
    await expect(card(page, "Тёмная")).toHaveAttribute("aria-pressed", "true");
  });

  test("карточка показывает свою тему независимо от текущей: цвета фона и кода", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    // сейчас светлый режим, а карточка Dracula всё равно тёмная; ключевое слово в образце кода розовое, как в Dracula
    await sw(page, "Светлая тема").click();
    await expect(html(page)).toHaveAttribute("data-theme", "light");
    const dracula = card(page, "Dracula");
    await expect(dracula).toHaveCSS("background-color", "rgb(40, 42, 54)");
    await expect(dracula.locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(255, 121, 198)");
    await expect(card(page, "One Light")).toHaveCSS("background-color", "rgb(250, 250, 250)");
  });

  test("карточки тем по умолчанию не наследуют цвета кода активной темы", async ({ page, request }) => {
    await loginFresh(page, request);
    await openSettings(page);
    await card(page, "Dracula").click();
    await expect(html(page)).toHaveAttribute("data-palette", "dracula");
    // у «Светлой» ключевое слово прежнего синего, а не розовое из Dracula
    await expect(card(page, "Светлая").locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(47, 107, 176)");
    await expect(card(page, "Тёмная").locator(".palette-code span", { hasText: "def" }).first()).toHaveCSS("color", "rgb(130, 184, 232)");
  });
});
