import { bearer, expect, STUDENT, test } from "../../support/fixtures";
import { stored } from "../../support/shell";
import type { Page } from "@playwright/test";

/* Вход и регистрация: без входа приложение закрыто, токен живёт в localStorage (`say-token`), выход его стирает. */

let counter = 0;
const newEmail = () => `auth-${Date.now().toString(36)}-${counter++}@e2e.test`;

async function fillForm(page: Page, email: string, password: string, name?: string) {
  await page.locator("input[type=email]").fill(email);
  if (name !== undefined) await page.locator(".auth-field", { hasText: "Имя" }).locator("input").fill(name);
  await page.locator("input[type=password]").fill(password);
}

const submit = (page: Page) => page.locator(".auth-submit");
const tab = (page: Page, name: string) => page.locator(".auth-tab", { hasText: name });

test.describe("без входа", () => {
  for (const path of ["/", "/book/12", "/settings", "/book/12/chapter/151"]) {
    test(`приложение закрыто: ${path} показывает форму входа`, async ({ page, guard }) => {
      await page.goto(path);
      await expect(page.locator(".auth-card")).toBeVisible();
      await expect(page.locator(".topbar")).toHaveCount(0);
      await expect(page.locator(".sidebar")).toHaveCount(0);
      await expect(page.locator(".content")).toHaveCount(0);
      expect(await stored(page, "say-token")).toBeNull();
      guard.assertClean();
    });
  }

  test("запросы без токена к прогрессу отклоняются", async ({ request }) => {
    expect((await request.get("/api/progress")).status()).toBe(401);
  });

  test("форма: вкладки «Вход» и «Регистрация», поля и кнопки", async ({ page, guard }) => {
    await page.goto("/");
    await expect(page.locator(".auth-logo")).toHaveText("CS.Core");
    await expect(tab(page, "Вход")).toHaveAttribute("aria-selected", "true");
    await expect(tab(page, "Регистрация")).toHaveAttribute("aria-selected", "false");
    await expect(page.locator(".auth-field span")).toHaveText(["Email", "Пароль (не короче 8 символов)"]);
    await expect(submit(page)).toHaveText("Войти");

    await tab(page, "Регистрация").click();
    await expect(tab(page, "Регистрация")).toHaveAttribute("aria-selected", "true");
    await expect(tab(page, "Вход")).toHaveAttribute("aria-selected", "false");
    await expect(page.locator(".auth-field span")).toHaveText(["Email", "Имя", "Пароль (не короче 8 символов)"]);
    await expect(submit(page)).toHaveText("Зарегистрироваться");

    await tab(page, "Вход").click();
    await expect(page.locator(".auth-field")).toHaveCount(2);
    guard.assertClean();
  });

  test("поля email и пароль обязательны: пустая форма не отправляется", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, "", "");
    let calls = 0;
    page.on("request", (r) => r.url().includes("/api/auth/login") && calls++);
    await submit(page).click();
    await expect(page.locator(".auth-card")).toBeVisible();
    expect(calls).toBe(0);
    expect(await page.locator("input[type=email]").evaluate((el: HTMLInputElement) => el.validity.valueMissing)).toBe(true);
  });

  test("тема переключается и на форме входа", async ({ page }) => {
    await page.goto("/");
    const html = page.locator("html");
    await expect(html).toHaveAttribute("data-theme", "dark");
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html).toHaveAttribute("data-theme", "light");
    expect(await stored(page, "say-theme")).toBe("light");
  });
});

test.describe("вход", () => {
  test("неверный пароль: сообщение об ошибке, форма остаётся, токена нет", async ({ page, guard }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, "wrong-password-1");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".auth-error")).not.toHaveText("");
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "say-token")).toBeNull();
    // кнопка снова доступна, повторная попытка возможна
    await expect(submit(page)).toBeEnabled();
    await expect(submit(page)).toHaveText("Войти");
    // ошибка 401 от входа — ожидаемый сетевой отклик, не сбой приложения
    expect(guard.errors.filter((e) => !/401|Unauthorized|Failed to load resource/i.test(e))).toEqual([]);
  });

  test("неизвестный email: сообщение об ошибке", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, newEmail(), "correct-horse-1");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    expect(await stored(page, "say-token")).toBeNull();
  });

  test("ошибка пропадает при переключении вкладки и после успешного входа", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, "wrong-password-1");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await tab(page, "Регистрация").click();
    await expect(page.locator(".auth-error")).toHaveCount(0);
    await tab(page, "Вход").click();
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
  });

  test("демо-пользователь входит: шапка, меню и дашборд, токен в localStorage", async ({ page, request, guard }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".sidebar")).toBeVisible();
    await expect(page.locator(".dash-card").first()).toBeVisible();
    await expect(page.locator(".auth-card")).toHaveCount(0);
    await expect(page.locator(".user-chip")).toHaveAttribute("title", STUDENT.email);

    // токен из хранилища принимается сервером
    const token = await stored(page, "say-token");
    expect(token).toBeTruthy();
    const res = await request.get("/api/progress", { headers: bearer(token as string) });
    expect(res.status()).toBe(200);
    guard.assertClean();
  });

  test("Enter в поле пароля отправляет форму", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await page.locator("input[type=password]").press("Enter");
    await expect(page.locator(".topbar")).toBeVisible();
  });

  test("вход остаётся на запрошенной странице", async ({ page }) => {
    await page.goto("/book/12");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topics-sec").first()).toBeVisible();
    expect(new URL(page.url()).pathname).toBe("/book/12");
  });

  test("быстрые кнопки «войти как …» (только в dev-сборке)", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator(".auth-card")).toBeVisible();
    const quick = page.getByRole("button", { name: "войти как programmer" });
    test.skip((await quick.count()) === 0, "в релизной сборке быстрых кнопок нет");
    await quick.click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".user-chip")).toHaveAttribute("title", "programmer@mail.com");
  });

  test("сессия сохраняется после перезагрузки страницы", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    const token = await stored(page, "say-token");
    await page.reload();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".auth-card")).toHaveCount(0);
    expect(await stored(page, "say-token")).toBe(token);
    // и на другой странице тоже
    await page.goto("/settings");
    await expect(page.locator(".set-card")).toBeVisible();
  });

  test("недействительный токен в хранилище: форма входа и токен стёрт", async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem("say-token", "not-a-real-token"));
    await page.goto("/");
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect.poll(() => stored(page, "say-token")).toBeNull();
  });
});

test.describe("регистрация", () => {
  test("новый пользователь регистрируется и сразу входит", async ({ page, request, guard }) => {
    const email = newEmail();
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, email, "correct-horse-1", "Новичок");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".user-chip")).toContainText("Новичок");
    await expect(page.locator(".user-chip")).toHaveAttribute("title", email);
    const token = await stored(page, "say-token");
    expect(token).toBeTruthy();
    expect((await request.get("/api/progress", { headers: bearer(token as string) })).status()).toBe(200);
    // у нового пользователя чистый прогресс
    await expect(page.locator(".dash-all")).toContainText("0% · 0 из");
    guard.assertClean();
  });

  test("после регистрации можно войти заново тем же паролем", async ({ page }) => {
    const email = newEmail();
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, email, "correct-horse-1", "Повторный");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await page.locator("button[title='Выйти']").click();
    await expect(page.locator(".auth-card")).toBeVisible();
    await tab(page, "Вход").click();
    await fillForm(page, email, "correct-horse-1");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
  });

  test("занятый email: сообщение об ошибке, вход не выполняется", async ({ page }) => {
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, STUDENT.email, "correct-horse-1", "Двойник");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "say-token")).toBeNull();
  });

  test("короткий пароль отвергается", async ({ page }) => {
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, newEmail(), "short", "Коротыш");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
  });
});

test.describe("выход", () => {
  test("«Выйти» в шапке возвращает на форму входа, токен стёрт и отозван на сервере", async ({ page, request }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    const token = (await stored(page, "say-token")) as string;
    await page.locator("button[title='Выйти']").click();
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "say-token")).toBeNull();
    expect((await request.get("/api/progress", { headers: bearer(token) })).status()).toBe(401);
    // после перезагрузки сессии нет
    await page.reload();
    await expect(page.locator(".auth-card")).toBeVisible();
  });

  test("после выхода можно войти другим пользователем", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".user-chip")).toHaveAttribute("title", STUDENT.email);
    await page.locator("button[title='Выйти']").click();
    await expect(page.locator(".auth-card")).toBeVisible();
    await fillForm(page, "programmer@mail.com", "programmer");
    await submit(page).click();
    await expect(page.locator(".user-chip")).toHaveAttribute("title", "programmer@mail.com");
  });
});
