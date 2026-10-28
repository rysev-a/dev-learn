import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bearer, chapters, expect, loginFresh, test, type ChapterRef } from "./fixtures";
import type { APIRequestContext, Page } from "@playwright/test";

/* Book chapter walk: one chapter — one test. The chapter list is taken statically from the slide files in `backend/data/slides`,
   the chapter id and its data (slides, number of questions and exercises) come from the API at run time. */

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const data = path.join(root, "backend", "data");

/** Numbers of the book's chapters that have a slide file `<book:02>-<chapter:02>.json`. */
export function slideChapters(book: number): number[] {
  const prefix = `${String(book).padStart(2, "0")}-`;
  return fs
    .readdirSync(path.join(data, "slides"))
    .filter((f) => f.startsWith(prefix) && f.endsWith(".json"))
    .map((f) => Number(f.slice(prefix.length, -".json".length)))
    .sort((a, b) => a - b);
}

/** Books from `sql/books.sql`: id → short name and title. */
export function bookMeta(): Map<number, { slug: string; title: string }> {
  const sql = fs.readFileSync(path.join(data, "sql", "books.sql"), "utf8");
  const out = new Map<number, { slug: string; title: string }>();
  for (const m of sql.matchAll(/^\s*\((\d+),\s*'([^']+)',\s*'([^']+)'/gm)) out.set(Number(m[1]), { slug: m[2]!, title: m[3]! });
  return out;
}

/** Chapter titles from the textbooks (`#CHAPTER N | Title`): for test names while the API is not yet available. */
function textbookTitles(book: number): Map<number, string> {
  const out = new Map<number, string>();
  const base = path.join(data, "textbook");
  const dir = fs.readdirSync(base).find((d) => d.startsWith(`${book}-`));
  if (!dir) return out;
  for (const f of fs.readdirSync(path.join(base, dir))) {
    if (!f.endsWith(".md")) continue;
    const text = fs.readFileSync(path.join(base, dir, f), "utf8");
    for (const m of text.matchAll(/^#CHAPTER\s+(\d+)\s*\|\s*(.+)$/gm)) out.set(Number(m[1]), m[2]!.trim());
  }
  return out;
}

// --- API data ------------------------------------------------------------------------------------------------------------

interface SceneBlock {
  t: "scene";
  labels: string[];
  captions: string[];
}
interface SlideData {
  title: string;
  main: string;
  body: ({ t: string } | SceneBlock)[];
}
interface ChapterSlides {
  rubric: string;
  slides: SlideData[];
}
type Counts = Record<string, Record<string, number>>;

const chapterCache = new Map<number, ChapterRef[]>();
async function chaptersOf(request: APIRequestContext, book: number): Promise<ChapterRef[]> {
  let list = chapterCache.get(book);
  if (!list) {
    list = await chapters(request, book);
    chapterCache.set(book, list);
  }
  return list;
}

async function getJson<T>(request: APIRequestContext, url: string, headers?: Record<string, string>): Promise<T> {
  const res = await request.get(url, headers ? { headers } : {});
  expect(res.ok(), `${url}: ${res.status()}`).toBeTruthy();
  return res.json() as Promise<T>;
}

const countOf = (counts: Counts, book: number, num: number): number => counts[String(book)]?.[String(num)] ?? 0;

// --- console guard --------------------------------------------------------------------------------------------------------

/**
 * Like `watchConsole` from fixtures, but without noise from expected 404s: the chapter tabs request `/api/exercises/<book>/<chapter>`,
 * and a 404 means "no code exercises" — the browser logs it to the console as an error, although it is a normal app response.
 */
function watchChapterConsole(page: Page, ignore500 = false) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() !== "error" || /ResizeObserver loop|Blocked script execution in 'about:srcdoc'/.test(m.text())) return;
    const exercises = /\/api\/exercises\/\d+\/\d+$/.test(m.location().url);
    const expected = exercises && (/status of 404/.test(m.text()) || (ignore500 && /status of 500/.test(m.text())));
    if (!expected) errors.push(`console.error: ${m.text().slice(0, 300)} @${m.location().url}`);
  });
  return errors;
}

// --- tab checks ------------------------------------------------------------------------------------------------------

const two = (n: number) => String(n).padStart(2, "0");

/** Snapshot of the shown slide (collected in the page with a single call so the walk is not limited by the number of browser round trips). */
interface Snap {
  num: string;
  rubric: string;
  count: string;
  title: string;
  mainLabel: string;
  mainText: string;
  bodyKids: number;
  stages: { chips: string[] }[];
  errors: number;
}

/** Waits in the page until the condition yields a value; on timeout reports what exactly was awaited. */
async function until<T, A>(page: Page, what: string, fn: (arg: A) => T | null | false, arg: A): Promise<T> {
  try {
    const handle = await page.waitForFunction(fn as (a: unknown) => unknown, arg, { timeout: 10_000 });
    return (await handle.jsonValue()) as T;
  } catch (e) {
    throw new Error(`timed out waiting for: ${what}\n${(e as Error).message.split("\n")[0]}`);
  }
}

/** The Theory tab: every slide point by point, every step for diagrams. */
async function walkTheory(page: Page, deck: ChapterSlides) {
  const count = deck.slides.length;
  await expect(page.locator(".slide-dot")).toHaveCount(count);
  for (let i = 0; i < count; i++) {
    const slide = deck.slides[i]!;
    const at = `slide ${i + 1}/${count} "${slide.title}"`;
    if (i > 0) await page.locator(".slide-dot").nth(i).click();

    // slide i is shown: the number in the panel and in the rubric match
    const snap = await until<Snap, string>(
      page,
      `${at}: slide shown`,
      (want) => {
        const num = document.querySelector(".slide-panel-num")?.textContent ?? "";
        const frame = document.querySelector(".slide-stage .slide");
        const spans = frame?.querySelectorAll(".s-rubric > span");
        if (!frame || !spans || spans.length < 2 || num !== want.split("|")[0] || spans[1]!.textContent !== want.split("|")[1]) return null;
        const text = (sel: string) => (frame.querySelector(sel)?.textContent ?? "").replace(/\s+/g, " ").trim();
        return {
          num,
          rubric: (spans[0]!.textContent ?? "").trim(),
          count: spans[1]!.textContent ?? "",
          title: text(".s-title"),
          mainLabel: text(".s-main-label"),
          mainText: text(".s-main-text"),
          bodyKids: frame.querySelectorAll(".s-body > *").length,
          stages: [...frame.querySelectorAll(".a-stage")].map((st) => ({ chips: [...st.querySelectorAll(".a-chip")].map((c) => (c.textContent ?? "").trim()) })),
          errors: document.querySelectorAll(".error").length,
        };
      },
      `${two(i + 1)} / ${two(count)}|${two(i + 1)} / ${count}`,
    );
    const norm = (t: string) => t.replace(/\s+/g, " ").trim();
    expect(snap.rubric, `${at}: rubric`).toBe(norm(deck.rubric));
    expect(snap.title, `${at}: title`).toBe(norm(slide.title));
    expect(snap.mainLabel, `${at}: MAIN label`).toBe("ГЛАВНОЕ");
    expect(norm(slide.main), `${at}: MAIN is empty in the data`).not.toBe("");
    expect(snap.mainText, `${at}: MAIN text`).toBe(norm(slide.main));
    expect(snap.bodyKids, `${at}: empty slide body`).toBeGreaterThan(0);
    expect(snap.errors, `${at}: error block`).toBe(0);

    const scenes = slide.body.filter((b): b is SceneBlock => b.t === "scene");
    expect(snap.stages.length, `${at}: number of diagrams`).toBe(scenes.length);
    for (let s = 0; s < scenes.length; s++) {
      const scene = scenes[s]!;
      expect(snap.stages[s]!.chips, `${at}: step buttons`).toEqual(scene.labels.map(norm));
      for (let k = 0; k < scene.labels.length; k++) {
        const step = `${at}, step ${k + 1} "${scene.labels[k]}"`;
        await page.locator(".slide-stage .a-stage").nth(s).locator(".a-chip").nth(k).click();
        const got = await until<{ note: string; svg: number; errors: number }, [number, number]>(
          page,
          `${step}: button enabled`,
          ([si, ki]) => {
            const st = document.querySelectorAll(".slide-stage .a-stage")[si!];
            if (!st) return null;
            const on = [...st.querySelectorAll(".a-chip")].findIndex((c) => c.classList.contains("on"));
            if (on !== ki) return null;
            return {
              note: (st.querySelector(".a-result-note")?.textContent ?? "").replace(/\s+/g, " ").trim(),
              svg: st.querySelectorAll(".a-svg > :not(defs)").length,
              errors: document.querySelectorAll(".error").length,
            };
          },
          [s, k],
        );
        expect(scene.captions[k]!.trim(), `${step}: caption is empty in the data`).not.toBe("");
        expect(got.note, `${step}: caption`).toBe(norm(scene.captions[k]!));
        // canvas: besides the arrow definitions the SVG has shapes
        expect(got.svg, `${step}: diagram SVG is empty`).toBeGreaterThan(0);
        expect(got.errors, `${step}: error block`).toBe(0);
      }
    }
  }
}

/** The Questions tab: questions and options are shown, no answers (highlighting) before a pick. */
async function checkQuiz(page: Page, expected: number) {
  await expect(page).toHaveURL(/\/questions$/);
  const questions = page.locator(".quiz-q");
  await expect(questions).toHaveCount(expected);
  for (let q = 0; q < expected; q++) {
    await expect(questions.nth(q).locator(".quiz-q-text"), `question ${q + 1}`).not.toHaveText("");
    expect(await questions.nth(q).locator(".quiz-opt").count(), `question ${q + 1}: options`).toBeGreaterThanOrEqual(2);
  }
  await expect(page.locator(".quiz-opt.right, .quiz-opt.wrong"), "options are not highlighted before an answer").toHaveCount(0);
  await expect(page.locator(".error")).toHaveCount(0);
}

interface Task {
  id: string;
  title: string;
  mode: string;
  statement: string;
}

/** The Practice tab: a list of code/lab exercises or answer-entry tasks. No solutions here. */
async function checkPractice(page: Page, tasks: Task[], answers: number) {
  await expect(page).toHaveURL(/\/exercises(\?.*)?$/);
  if (tasks.length > 0) {
    await expect(page.locator(".pr-item")).toHaveCount(tasks.length);
    await expect(page.locator(".pr-item .pr-name")).toHaveText(tasks.map((t) => t.title));
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 0 из ${tasks.length}`);
    await expect(page.locator(".pr-head h3")).toHaveText(`1. ${tasks[0]!.title}`);
    await expect(page.locator(".pr-statement")).toHaveText(tasks[0]!.statement);
    if (tasks[0]!.mode === "lab") {
      // the exercise strip on top (`lab-pr`) exists only for chapters made of lab exercises alone; mixed ones (chapter 17:2 etc.) do not have it
      await expect(page.locator(".pr.lab-pr"), "lab layout").toHaveCount(tasks.every((t) => t.mode === "lab") ? 1 : 0);
      // besides the heading and the statement — the lab itself
      await expect.poll(() => page.locator(".pr-main > *").count(), "lab is not shown").toBeGreaterThan(2);
    } else {
      await expect(page.locator(".rs-input"), "code editor").toBeVisible();
    }
  } else {
    await expect(page.locator(".quiz-q")).toHaveCount(answers);
    await expect(page.locator(".quiz-q .quiz-q-text").first()).not.toHaveText("");
  }
  await expect(page.locator(".error")).toHaveCount(0);
}

/** Waits until the server records the chapter's viewed slides (zero-based numbers). */
async function expectSlideProgress(request: APIRequestContext, token: string, book: number, num: number, want: number[]) {
  await expect
    .poll(
      async () => {
        const p = await getJson<{ slides: Record<string, number[]> }>(request, "/api/progress", bearer(token));
        return p.slides[`${book}:${num}`] ?? [];
      },
      { message: "viewed-slide progress on the server", timeout: 10_000 },
    )
    .toEqual(want);
}

/**
 * Confirmed app defects (key — "book:chapter"). Such a chapter goes through the regular walk, but without the affected check;
 * the check itself stays strict in a separate test.fixme (see the end of bookSuite) and turns on when the defect is fixed.
 * - 9:26: `GET /api/exercises/9/26` answers 500 "FOREIGN KEY constraint failed" — chapter 26 of Databases (28 exercises)
 *   cannot open its practice (the page has no Practice tab).
 */
const KNOWN_DEFECTS: Record<string, { what: string }> = {};
const defectOf = (book: number, num: number) => KNOWN_DEFECTS[`${book}:${num}`];

// --- book test suite ----------------------------------------------------------------------------------------------------

/**
 * Book test suite: a separate test per chapter with slides (a failure is localised to the chapter).
 * Tests run one chapter at a time (workers = 1 in the config); a failing chapter does not cancel the next ones.
 */
export function bookSuite(bookId: number, slug: string) {
  const meta = bookMeta().get(bookId);
  if (!meta) throw new Error(`book ${bookId} not found in sql/books.sql`);
  if (meta.slug !== slug) throw new Error(`book ${bookId} has short name "${meta.slug}", not "${slug}"`);
  const titles = textbookTitles(bookId);
  const nums = slideChapters(bookId);
  if (nums.length === 0) throw new Error(`no slide files for book ${bookId}`);

  test.describe(`${meta.title} (book ${bookId})`, () => {
    for (const num of nums) {
      test(`"${meta.title}: chapter ${num} — ${titles.get(num) ?? "?"}"`, async ({ page, request }) => {
        const errors = watchChapterConsole(page, !!defectOf(bookId, num));
        const { token } = await loginFresh(page, request);

        // chapter data from the API
        const ref = (await chaptersOf(request, bookId)).find((c) => c.num === num);
        expect(ref, `chapter ${bookId}:${num} exists in the course`).toBeTruthy();
        const { id, title } = ref!;
        if (titles.has(num)) expect(title, "chapter title in the API and in the textbook").toBe(titles.get(num));
        const deck = await getJson<ChapterSlides>(request, `/api/slides/${bookId}/${num}`);
        const file = JSON.parse(fs.readFileSync(path.join(data, "slides", `${two(bookId)}-${two(num)}.json`), "utf8")) as ChapterSlides;
        expect(deck.slides.length, "number of slides in the API and in the data file").toBe(file.slides.length);
        expect(deck.slides.length).toBeGreaterThan(0);
        const quizzes = countOf(await getJson<Counts>(request, "/api/quizzes"), bookId, num);
        const answers = countOf(await getJson<Counts>(request, "/api/answers"), bookId, num);
        const codeRes = await request.get(`/api/exercises/${bookId}/${num}`);
        const tasks = codeRes.ok() ? ((await codeRes.json()) as { tasks: Task[] }).tasks : [];
        if (!codeRes.ok() && !defectOf(bookId, num)) expect(codeRes.status(), "no exercises — 404").toBe(404);
        const hasPractice = tasks.length > 0 || answers > 0;

        // chapter page
        await page.goto(`/book/${bookId}/chapter/${id}`);
        await expect(page.locator("h2")).toHaveText(`Урок ${num}. ${title}`);
        const tabNames = ["Теория", ...(quizzes > 0 ? ["Вопросы"] : []), ...(hasPractice ? ["Практика"] : [])];
        await expect(page.locator(".ch-tab")).toHaveCount(tabNames.length);
        for (const [i, name] of tabNames.entries()) await expect(page.locator(".ch-tab").nth(i)).toContainText(name);

        // theory
        await walkTheory(page, deck);

        // progress: all chapter slides viewed (zero-based numbers)
        await expectSlideProgress(request, token, bookId, num, deck.slides.map((_, i) => i));

        // questions and practice (if any)
        if (quizzes > 0) {
          await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
          await checkQuiz(page, quizzes);
        }
        if (hasPractice) {
          await page.locator(".ch-tab", { hasText: "Практика" }).click();
          await checkPractice(page, tasks, answers);
        }

        expect(errors, "browser console errors").toEqual([]);
      });
    }
    // strict checks of known defects: skipped (fixme) until the defect is fixed
    for (const num of nums) {
      const known = defectOf(bookId, num);
      if (!known) continue;
      test.fixme(`"${meta.title}: chapter ${num}" — ${known.what}`, async ({ page, request }) => {
        await loginFresh(page, request);
        const ref = (await chaptersOf(request, bookId)).find((c) => c.num === num)!;
        const tasks = (await getJson<{ tasks: Task[] }>(request, `/api/exercises/${bookId}/${num}`)).tasks;
        await page.goto(`/book/${bookId}/chapter/${ref.id}`);
        await page.locator(".ch-tab", { hasText: "Практика" }).click();
        await checkPractice(page, tasks, 0);
      });
    }
  });
}
