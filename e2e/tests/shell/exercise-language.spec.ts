import { expect, loginFresh, test, books, chapters } from "../../support/fixtures";

/* Данные упражнений (код, SQL, лаборатории) — только английские в обоих языках интерфейса: в русском режиме по-русски только
   название, условие и подсказка; в английском режиме на странице практики нет кириллицы вообще. */

const CYR = /[А-Яа-яЁё]/;
const EXERCISE_BOOKS = [7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18];

type Task = { id: string; title?: string; statement?: string; hint?: string; [k: string]: unknown };

function strip(task: Task): unknown {
  const { title, statement, hint, ...rest } = task; // eslint-disable-line @typescript-eslint/no-unused-vars
  return rest;
}

test("в API упражнений нет кириллицы: английский — нигде, русский — только в названии, условии и подсказке", async ({ request }) => {
  test.setTimeout(600_000);
  const bad: string[] = [];
  let checked = 0;
  for (const b of await books(request)) {
    if (!EXERCISE_BOOKS.includes(b.id)) continue;
    for (const ch of await chapters(request, b.id)) {
      for (const [kind, url] of [["tasks", `/api/exercises/${b.id}/${ch.num}`], ["labs", `/api/labs/${b.id}/${ch.num}`]] as const) {
        for (const lang of ["en", "ru"] as const) {
          const res = await request.get(url, { headers: { "Accept-Language": lang } });
          if (!res.ok()) continue;
          const body = (await res.json()) as unknown;
          const tasks: Task[] = Array.isArray(body) ? (body as Task[]) : (((body as { tasks?: Task[] }).tasks ?? []) as Task[]);
          const whole = lang === "en" ? JSON.stringify(body) : JSON.stringify(tasks.map(strip)) + JSON.stringify(Array.isArray(body) ? {} : { ...(body as object), tasks: undefined });
          checked++;
          const m = whole.match(/.{0,40}[А-Яа-яЁё]+.{0,20}/);
          if (m && CYR.test(whole)) bad.push(`${lang} ${kind} ${b.id}/${ch.num}: …${m[0]}…`);
        }
      }
    }
  }
  expect(checked, "проверено ответов").toBeGreaterThan(100);
  expect(bad, bad.slice(0, 20).join("\n")).toEqual([]);
});

test("страница практики по-английски: ни одной русской буквы в области упражнения", async ({ page, request }) => {
  test.setTimeout(900_000);
  await loginFresh(page, request);
  await page.addInitScript(() => window.localStorage.setItem("cs-core-lang", "en"));
  const bad: string[] = [];
  for (const b of await books(request)) {
    if (!EXERCISE_BOOKS.includes(b.id)) continue;
    for (const ch of await chapters(request, b.id)) {
      const has = await request.get(`/api/exercises/${b.id}/${ch.num}`);
      const lab = await request.get(`/api/labs/${b.id}/${ch.num}`);
      if (!has.ok() && !lab.ok()) continue;
      await page.goto(`/book/${b.id}/chapter/${ch.id}/exercises`);
      await page.locator(".pr-statement, .pr-main").first().waitFor({ timeout: 20_000 }).catch(() => undefined);
      const text = await page.evaluate(() => {
        const root = document.querySelector(".pr-main, .practice, main") ?? document.body;
        return (root as HTMLElement).innerText;
      });
      const m = text.match(/.{0,40}[А-Яа-яЁё]+.{0,20}/);
      if (m) bad.push(`${b.id}/${ch.num}: …${m[0].replace(/\n/g, " ")}…`);
    }
  }
  expect(bad, bad.slice(0, 20).join("\n")).toEqual([]);
});
