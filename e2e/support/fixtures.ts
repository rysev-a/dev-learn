import { expect, test as base, type APIRequestContext, type Page } from "@playwright/test";

/* Общие приспособления e2e: вход демо-пользователем, номера глав → адреса, охрана консоли браузера. */

export const STUDENT = { email: "student@mail.com", password: "student" };

/** Вход через API: токен кладётся в localStorage ещё до загрузки приложения (как после обычного входа). */
export async function loginViaApi(page: Page, request: APIRequestContext, who = STUDENT): Promise<string> {
  const res = await request.post("/api/auth/login", { data: { login: who.email, email: who.email, password: who.password } });
  expect(res.ok(), `вход ${who.email}: ${res.status()}`).toBeTruthy();
  const { token } = (await res.json()) as { token: string };
  await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("say-token", t); }, token);
  return token;
}

let counter = 0;

/**
 * Новый пользователь с чистым прогрессом (регистрация + вход через API): тесты не делят прогресс и не мешают друг другу.
 * Адрес уникален в рамках запуска.
 */
export async function loginFresh(page: Page, request: APIRequestContext, prefix = "e2e"): Promise<{ email: string; token: string }> {
  // готовый стек ограничивает регистрации (429): входим одним заданным пользователем (`E2E_USER`/`E2E_PASSWORD`) и стираем его прогресс
  if (process.env.E2E_USER) {
    const email = process.env.E2E_USER;
    const res = await request.post("/api/auth/login", { data: { login: email, email, password: process.env.E2E_PASSWORD ?? "" } });
    expect(res.ok(), `вход ${email}`).toBeTruthy();
    const { token } = (await res.json()) as { token: string };
    const reset = await request.delete("/api/progress?scope=all", { headers: { Authorization: `Bearer ${token}` } });
    expect(reset.ok(), "сброс прогресса").toBeTruthy();
    await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("say-token", t); }, token);
    return { email, token };
  }
  const email = `${prefix}-${Date.now().toString(36)}-${counter++}@e2e.test`;
  const password = "correct-horse-1";
  const signup = await request.post("/api/auth/signup", { data: { email, password, name: "E2E" } });
  expect(signup.status(), `регистрация ${email}`).toBe(201);
  const res = await request.post("/api/auth/login", { data: { login: email, email, password } });
  expect(res.ok(), `вход ${email}`).toBeTruthy();
  const { token } = (await res.json()) as { token: string };
  await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("say-token", t); }, token);
  return { email, token };
}

/** Заголовок авторизации для прямых вызовов API из теста. */
export const bearer = (token: string) => ({ Authorization: `Bearer ${token}` });

export interface Book {
  id: number;
  title: string;
  slug: string | null;
}
export interface ChapterRef {
  num: number;
  id: number;
  title: string;
}

export async function books(request: APIRequestContext): Promise<Book[]> {
  return (await request.get("/api/books")).json();
}

/** Главы книги по порядку: номер в книге и внутренний id (в адресе страницы — id). */
export async function chapters(request: APIRequestContext, book: number): Promise<ChapterRef[]> {
  const course = (await (await request.get(`/api/books/${book}/course`)).json()) as { chapters: ChapterRef[] }[];
  return course.flatMap((s) => s.chapters).sort((a, b) => a.num - b.num);
}

export async function chapterId(request: APIRequestContext, book: number, num: number): Promise<number> {
  const found = (await chapters(request, book)).find((c) => c.num === num);
  if (!found) throw new Error(`нет главы ${book}:${num}`);
  return found.id;
}

/** Ошибки страницы, которые не считаем сбоем (шум браузера). */
/** Шум, не относящийся к приложению: `ResizeObserver`; init-скрипт Playwright, который песочница предпросмотра (iframe без allow-scripts) не выполняет. */
const NOISE = [/ResizeObserver loop/, /Blocked script execution in 'about:srcdoc'/];

/**
 * Охрана консоли: любое необработанное исключение страницы или `console.error` (паника Rust, неверный ответ API) — провал теста.
 * Вызывается в тесте до перехода на страницу; `assertClean()` — в конце проверки.
 */
export function watchConsole(page: Page) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() === "error" && !NOISE.some((r) => r.test(m.text()))) errors.push(`console.error: ${m.text().slice(0, 300)}`);
  });
  return {
    errors,
    assertClean: () => expect(errors, "ошибки в консоли браузера").toEqual([]),
  };
}

export const test = base.extend<{ guard: ReturnType<typeof watchConsole> }>({
  guard: async ({ page }, use) => {
    const guard = watchConsole(page);
    await use(guard);
  },
});

export { expect };
