import { expect, loginFresh, test, books, chapters } from "../../support/fixtures";

/* Exercise data (code, SQL, labs) is English only in both interface languages: in Russian mode only the
   title, statement and hint are Russian; in English mode the practice page has no Cyrillic at all. */

const CYR = /[А-Яа-яЁё]/;
const EXERCISE_BOOKS = [7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18];

type Task = { id: string; title?: string; statement?: string; hint?: string; [k: string]: unknown };

function strip(task: Task): unknown {
  const { title, statement, hint, ...rest } = task; // eslint-disable-line @typescript-eslint/no-unused-vars
  return rest;
}

test("the exercises API has no Cyrillic: English everywhere, Russian only in the title, statement and hint", async ({ request }) => {
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
  expect(checked, "responses checked").toBeGreaterThan(100);
  expect(bad, bad.slice(0, 20).join("\n")).toEqual([]);
});

test("practice page in English: not a single Russian letter in the exercise area", async ({ page, request }) => {
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
