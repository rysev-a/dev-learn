import { expect, test as base, type APIRequestContext, type Page } from "@playwright/test";

/* Shared e2e helpers: demo user login, chapter numbers → URLs, browser console guard. */

export const STUDENT = { email: "student@mail.com", password: "student" };

/** Login through the API: the token is put into localStorage before the app loads (as after a regular login). */
export async function loginViaApi(page: Page, request: APIRequestContext, who = STUDENT): Promise<string> {
  const res = await request.post("/api/auth/login", { data: { login: who.email, email: who.email, password: who.password } });
  expect(res.ok(), `login ${who.email}: ${res.status()}`).toBeTruthy();
  const { token } = (await res.json()) as { token: string };
  await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("cs-core-token", t); }, token);
  return token;
}

let counter = 0;

/**
 * A new user with clean progress (sign-up + login through the API): tests do not share progress and do not interfere with each other.
 * The address is unique within a run.
 */
export async function loginFresh(page: Page, request: APIRequestContext, prefix = "e2e"): Promise<{ email: string; token: string }> {
  // a ready-made stack limits sign-ups (429): log in as one given user (`E2E_USER`/`E2E_PASSWORD`) and erase its progress
  if (process.env.E2E_USER) {
    const email = process.env.E2E_USER;
    const res = await request.post("/api/auth/login", { data: { login: email, email, password: process.env.E2E_PASSWORD ?? "" } });
    expect(res.ok(), `login ${email}`).toBeTruthy();
    const { token } = (await res.json()) as { token: string };
    const reset = await request.delete("/api/progress?scope=all", { headers: { Authorization: `Bearer ${token}` } });
    expect(reset.ok(), "progress reset").toBeTruthy();
    await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("cs-core-token", t); }, token);
    return { email, token };
  }
  const email = `${prefix}-${Date.now().toString(36)}-${counter++}@e2e.test`;
  const password = "correct-horse-1";
  const signup = await request.post("/api/auth/signup", { data: { email, password, name: "E2E" } });
  expect(signup.status(), `sign-up ${email}`).toBe(201);
  const res = await request.post("/api/auth/login", { data: { login: email, email, password } });
  expect(res.ok(), `login ${email}`).toBeTruthy();
  const { token } = (await res.json()) as { token: string };
  await page.addInitScript((t) => { if (window === window.top) window.localStorage.setItem("cs-core-token", t); }, token);
  return { email, token };
}

/** Authorization header for direct API calls from a test. */
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

/** Book chapters in order: number within the book and internal id (the page URL uses the id). */
export async function chapters(request: APIRequestContext, book: number): Promise<ChapterRef[]> {
  const course = (await (await request.get(`/api/books/${book}/course`)).json()) as { chapters: ChapterRef[] }[];
  return course.flatMap((s) => s.chapters).sort((a, b) => a.num - b.num);
}

export async function chapterId(request: APIRequestContext, book: number, num: number): Promise<number> {
  const found = (await chapters(request, book)).find((c) => c.num === num);
  if (!found) throw new Error(`no chapter ${book}:${num}`);
  return found.id;
}

/** Noise unrelated to the app: `ResizeObserver`; the Playwright init script, which the preview sandbox (iframe without allow-scripts) does not run. */
const NOISE = [/ResizeObserver loop/, /Blocked script execution in 'about:srcdoc'/];

/**
 * Console guard: any unhandled page exception or `console.error` (a Rust panic, a bad API response) fails the test.
 * Called in the test before navigating to the page; `assertClean()` at the end of the check.
 */
export function watchConsole(page: Page) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() === "error" && !NOISE.some((r) => r.test(m.text()))) errors.push(`console.error: ${m.text().slice(0, 300)}`);
  });
  return {
    errors,
    assertClean: () => expect(errors, "browser console errors").toEqual([]),
  };
}

export const test = base.extend<{ guard: ReturnType<typeof watchConsole> }>({
  guard: async ({ page }, use) => {
    const guard = watchConsole(page);
    await use(guard);
  },
});

export { expect };
