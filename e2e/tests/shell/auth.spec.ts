import { bearer, expect, STUDENT, test } from "../../support/fixtures";
import { stored } from "../../support/shell";
import type { Page } from "@playwright/test";

/* Sign-in and sign-up: without signing in the app is closed, the token lives in localStorage (`cs-core-token`), signing out erases it. */

let counter = 0;
const newEmail = () => `auth-${Date.now().toString(36)}-${counter++}@e2e.test`;

async function fillForm(page: Page, email: string, password: string, name?: string) {
  await page.locator("input[type=email]").fill(email);
  if (name !== undefined) await page.locator(".auth-field", { hasText: "Имя" }).locator("input").fill(name);
  await page.locator("input[type=password]").fill(password);
}

const submit = (page: Page) => page.locator(".auth-submit");
const tab = (page: Page, name: string) => page.locator(".auth-tab", { hasText: name });

test.describe("without sign-in", () => {
  for (const path of ["/", "/book/12", "/settings", "/book/12/chapter/151"]) {
    test(`the app is closed: ${path} shows the sign-in form`, async ({ page, guard }) => {
      await page.goto(path);
      await expect(page.locator(".auth-card")).toBeVisible();
      await expect(page.locator(".topbar")).toHaveCount(0);
      await expect(page.locator(".sidebar")).toHaveCount(0);
      await expect(page.locator(".content")).toHaveCount(0);
      expect(await stored(page, "cs-core-token")).toBeNull();
      guard.assertClean();
    });
  }

  test("progress requests without a token are rejected", async ({ request }) => {
    expect((await request.get("/api/progress")).status()).toBe(401);
  });

  test("form: \"Вход\" and \"Регистрация\" tabs, fields and buttons", async ({ page, guard }) => {
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

  test("email and password fields are required: an empty form is not submitted", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, "", "");
    let calls = 0;
    page.on("request", (r) => r.url().includes("/api/auth/login") && calls++);
    await submit(page).click();
    await expect(page.locator(".auth-card")).toBeVisible();
    expect(calls).toBe(0);
    expect(await page.locator("input[type=email]").evaluate((el: HTMLInputElement) => el.validity.valueMissing)).toBe(true);
  });

  test("the theme also switches on the sign-in form", async ({ page }) => {
    await page.goto("/");
    const html = page.locator("html");
    await expect(html).toHaveAttribute("data-theme", "dark");
    await page.getByRole("button", { name: "Переключить тему" }).click();
    await expect(html).toHaveAttribute("data-theme", "light");
    expect(await stored(page, "cs-core-theme")).toBe("light");
  });
});

test.describe("sign-in", () => {
  test("wrong password: an error message, the form stays, no token", async ({ page, guard }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, "wrong-password-1");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".auth-error")).not.toHaveText("");
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "cs-core-token")).toBeNull();
    // the button is available again, a retry is possible
    await expect(submit(page)).toBeEnabled();
    await expect(submit(page)).toHaveText("Войти");
    // a 401 from sign-in is an expected network response, not an app failure
    expect(guard.errors.filter((e) => !/401|Unauthorized|Failed to load resource/i.test(e))).toEqual([]);
  });

  test("unknown email: an error message", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, newEmail(), "correct-horse-1");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    expect(await stored(page, "cs-core-token")).toBeNull();
  });

  test("the error disappears on switching tabs and after a successful sign-in", async ({ page }) => {
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

  test("a demo user signs in: header, menu and dashboard, token in localStorage", async ({ page, request, guard }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".sidebar")).toBeVisible();
    await expect(page.locator(".dash-card").first()).toBeVisible();
    await expect(page.locator(".auth-card")).toHaveCount(0);
    await expect(page.locator(".user-chip")).toHaveAttribute("title", STUDENT.email);

    // the token from storage is accepted by the server
    const token = await stored(page, "cs-core-token");
    expect(token).toBeTruthy();
    const res = await request.get("/api/progress", { headers: bearer(token as string) });
    expect(res.status()).toBe(200);
    guard.assertClean();
  });

  test("Enter in the password field submits the form", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await page.locator("input[type=password]").press("Enter");
    await expect(page.locator(".topbar")).toBeVisible();
  });

  test("sign-in stays on the requested page", async ({ page }) => {
    await page.goto("/book/12");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topics-sec").first()).toBeVisible();
    expect(new URL(page.url()).pathname).toBe("/book/12");
  });

  test("quick \"войти как ...\" buttons (dev build only)", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator(".auth-card")).toBeVisible();
    const quick = page.getByRole("button", { name: "войти как programmer" });
    test.skip((await quick.count()) === 0, "there are no quick buttons in a release build");
    await quick.click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".user-chip")).toHaveAttribute("title", "programmer@mail.com");
  });

  test("the session persists after a page reload", async ({ page }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    const token = await stored(page, "cs-core-token");
    await page.reload();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".auth-card")).toHaveCount(0);
    expect(await stored(page, "cs-core-token")).toBe(token);
    // and on another page too
    await page.goto("/settings");
    await expect(page.locator(".set-card")).toBeVisible();
  });

  test("invalid token in storage: the sign-in form is shown and the token is erased", async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem("cs-core-token", "not-a-real-token"));
    await page.goto("/");
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect.poll(() => stored(page, "cs-core-token")).toBeNull();
  });
});

test.describe("sign-up", () => {
  test("a new user signs up and is signed in at once", async ({ page, request, guard }) => {
    const email = newEmail();
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, email, "correct-horse-1", "Newbie");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await expect(page.locator(".user-chip")).toContainText("Newbie");
    await expect(page.locator(".user-chip")).toHaveAttribute("title", email);
    const token = await stored(page, "cs-core-token");
    expect(token).toBeTruthy();
    expect((await request.get("/api/progress", { headers: bearer(token as string) })).status()).toBe(200);
    // a new user has clean progress
    await expect(page.locator(".dash-all")).toContainText("0% · 0 из");
    guard.assertClean();
  });

  test("after sign-up one can sign in again with the same password", async ({ page }) => {
    const email = newEmail();
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, email, "correct-horse-1", "Repeat");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    await page.locator("button[title='Выйти']").click();
    await expect(page.locator(".auth-card")).toBeVisible();
    await tab(page, "Вход").click();
    await fillForm(page, email, "correct-horse-1");
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
  });

  test("taken email: an error message, no sign-in", async ({ page }) => {
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, STUDENT.email, "correct-horse-1", "Twin");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "cs-core-token")).toBeNull();
  });

  test("a short password is rejected", async ({ page }) => {
    await page.goto("/");
    await tab(page, "Регистрация").click();
    await fillForm(page, newEmail(), "short", "Shorty");
    await submit(page).click();
    await expect(page.locator(".auth-error")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
  });
});

test.describe("sign-out", () => {
  test("\"Выйти\" in the header returns to the sign-in form, the token is erased and revoked on the server", async ({ page, request }) => {
    await page.goto("/");
    await fillForm(page, STUDENT.email, STUDENT.password);
    await submit(page).click();
    await expect(page.locator(".topbar")).toBeVisible();
    const token = (await stored(page, "cs-core-token")) as string;
    await page.locator("button[title='Выйти']").click();
    await expect(page.locator(".auth-card")).toBeVisible();
    await expect(page.locator(".topbar")).toHaveCount(0);
    expect(await stored(page, "cs-core-token")).toBeNull();
    expect((await request.get("/api/progress", { headers: bearer(token) })).status()).toBe(401);
    // there is no session after a reload
    await page.reload();
    await expect(page.locator(".auth-card")).toBeVisible();
  });

  test("after signing out one can sign in as another user", async ({ page }) => {
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
