import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bearer, chapters, expect, loginFresh, test, type ChapterRef } from "./fixtures";
import type { APIRequestContext, Page } from "@playwright/test";

/* Обход глав книги: по одной главе — один test. Список глав берётся статически из файлов слайдов `backend/data/slides`,
   id главы и её данные (слайды, число вопросов и упражнений) — из API при выполнении. */

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const data = path.join(root, "backend", "data");

/** Номера глав книги, у которых есть файл слайдов `<книга:02>-<глава:02>.json`. */
export function slideChapters(book: number): number[] {
  const prefix = `${String(book).padStart(2, "0")}-`;
  return fs
    .readdirSync(path.join(data, "slides"))
    .filter((f) => f.startsWith(prefix) && f.endsWith(".json"))
    .map((f) => Number(f.slice(prefix.length, -".json".length)))
    .sort((a, b) => a - b);
}

/** Книги из `sql/books.sql`: id → короткое имя и название. */
export function bookMeta(): Map<number, { slug: string; title: string }> {
  const sql = fs.readFileSync(path.join(data, "sql", "books.sql"), "utf8");
  const out = new Map<number, { slug: string; title: string }>();
  for (const m of sql.matchAll(/^\s*\((\d+),\s*'([^']+)',\s*'([^']+)'/gm)) out.set(Number(m[1]), { slug: m[2]!, title: m[3]! });
  return out;
}

/** Названия глав из учебников (`#CHAPTER N | Название`): для имён тестов, пока API ещё недоступен. */
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

// --- данные API ------------------------------------------------------------------------------------------------------------

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

// --- охрана консоли --------------------------------------------------------------------------------------------------------

/**
 * Как `watchConsole` из fixtures, но без шума от ожидаемых 404: вкладки главы спрашивают `/api/exercises/<книга>/<глава>`,
 * и ответ 404 означает «код-упражнений нет» — браузер пишет его в консоль как error, хотя это штатный ответ приложения.
 */
function watchChapterConsole(page: Page, ignore500 = false) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() !== "error" || /ResizeObserver loop/.test(m.text())) return;
    const exercises = /\/api\/exercises\/\d+\/\d+$/.test(m.location().url);
    const expected = exercises && (/status of 404/.test(m.text()) || (ignore500 && /status of 500/.test(m.text())));
    if (!expected) errors.push(`console.error: ${m.text().slice(0, 300)} @${m.location().url}`);
  });
  return errors;
}

// --- проверки вкладок ------------------------------------------------------------------------------------------------------

const two = (n: number) => String(n).padStart(2, "0");

/** Снимок показанного слайда (собирается в странице одним вызовом, чтобы обход не упирался в число обращений к браузеру). */
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

/** Ждёт в странице, пока условие даст значение; при тайм-ауте сообщает, что именно ждали. */
async function until<T, A>(page: Page, what: string, fn: (arg: A) => T | null | false, arg: A): Promise<T> {
  try {
    const handle = await page.waitForFunction(fn as (a: unknown) => unknown, arg, { timeout: 10_000 });
    return (await handle.jsonValue()) as T;
  } catch (e) {
    throw new Error(`не дождались: ${what}\n${(e as Error).message.split("\n")[0]}`);
  }
}

/** Вкладка «Теория»: каждый слайд по точкам, у схем — каждый шаг. */
async function walkTheory(page: Page, deck: ChapterSlides) {
  const count = deck.slides.length;
  await expect(page.locator(".slide-dot")).toHaveCount(count);
  for (let i = 0; i < count; i++) {
    const slide = deck.slides[i]!;
    const at = `слайд ${i + 1}/${count} «${slide.title}»`;
    if (i > 0) await page.locator(".slide-dot").nth(i).click();

    // слайд i показан: номер в панели и в рубрике совпали
    const snap = await until<Snap, string>(
      page,
      `${at}: показ слайда`,
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
    expect(snap.rubric, `${at}: рубрика`).toBe(norm(deck.rubric));
    expect(snap.title, `${at}: заголовок`).toBe(norm(slide.title));
    expect(snap.mainLabel, `${at}: «ГЛАВНОЕ»`).toBe("ГЛАВНОЕ");
    expect(norm(slide.main), `${at}: «ГЛАВНОЕ» пусто в данных`).not.toBe("");
    expect(snap.mainText, `${at}: текст «ГЛАВНОЕ»`).toBe(norm(slide.main));
    expect(snap.bodyKids, `${at}: пустое тело слайда`).toBeGreaterThan(0);
    expect(snap.errors, `${at}: блок ошибки`).toBe(0);

    const scenes = slide.body.filter((b): b is SceneBlock => b.t === "scene");
    expect(snap.stages.length, `${at}: число схем`).toBe(scenes.length);
    for (let s = 0; s < scenes.length; s++) {
      const scene = scenes[s]!;
      expect(snap.stages[s]!.chips, `${at}: кнопки шагов`).toEqual(scene.labels.map(norm));
      for (let k = 0; k < scene.labels.length; k++) {
        const step = `${at}, шаг ${k + 1} «${scene.labels[k]}»`;
        await page.locator(".slide-stage .a-stage").nth(s).locator(".a-chip").nth(k).click();
        const got = await until<{ note: string; svg: number; errors: number }, [number, number]>(
          page,
          `${step}: кнопка включена`,
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
        expect(scene.captions[k]!.trim(), `${step}: подпись пуста в данных`).not.toBe("");
        expect(got.note, `${step}: подпись`).toBe(norm(scene.captions[k]!));
        // холст: кроме определений стрелок в SVG есть фигуры
        expect(got.svg, `${step}: SVG схемы пуст`).toBeGreaterThan(0);
        expect(got.errors, `${step}: блок ошибки`).toBe(0);
      }
    }
  }
}

/** Вкладка «Вопросы»: вопросы и варианты показаны, ответов (подсветки) до выбора нет. */
async function checkQuiz(page: Page, expected: number) {
  await expect(page).toHaveURL(/\/questions$/);
  const questions = page.locator(".quiz-q");
  await expect(questions).toHaveCount(expected);
  for (let q = 0; q < expected; q++) {
    await expect(questions.nth(q).locator(".quiz-q-text"), `вопрос ${q + 1}`).not.toHaveText("");
    expect(await questions.nth(q).locator(".quiz-opt").count(), `вопрос ${q + 1}: вариантов`).toBeGreaterThanOrEqual(2);
  }
  await expect(page.locator(".quiz-opt.right, .quiz-opt.wrong"), "до ответа варианты не подсвечены").toHaveCount(0);
  await expect(page.locator(".error")).toHaveCount(0);
}

interface Task {
  id: string;
  title: string;
  mode: string;
  statement: string;
}

/** Вкладка «Практика»: список упражнений с кодом/лабораторией или задачи с вводом ответа. Решений здесь нет. */
async function checkPractice(page: Page, tasks: Task[], answers: number) {
  await expect(page).toHaveURL(/\/exercises(\?.*)?$/);
  if (tasks.length > 0) {
    await expect(page.locator(".pr-item")).toHaveCount(tasks.length);
    await expect(page.locator(".pr-item .pr-name")).toHaveText(tasks.map((t) => t.title));
    await expect(page.locator(".pr-top-label").first()).toHaveText(`Решено 0 из ${tasks.length}`);
    await expect(page.locator(".pr-head h3")).toHaveText(`1. ${tasks[0]!.title}`);
    await expect(page.locator(".pr-statement")).toHaveText(tasks[0]!.statement);
    if (tasks[0]!.mode === "lab") {
      // полоса упражнений сверху (`lab-pr`) — только у глав из одних лабораторных упражнений; в смешанных (глава 17:2 и др.) её нет
      await expect(page.locator(".pr.lab-pr"), "раскладка лабораторий").toHaveCount(tasks.every((t) => t.mode === "lab") ? 1 : 0);
      // кроме заголовка и условия — сама лаборатория
      await expect.poll(() => page.locator(".pr-main > *").count(), "лаборатория не показана").toBeGreaterThan(2);
    } else {
      await expect(page.locator(".rs-input"), "редактор кода").toBeVisible();
    }
  } else {
    await expect(page.locator(".quiz-q")).toHaveCount(answers);
    await expect(page.locator(".quiz-q .quiz-q-text").first()).not.toHaveText("");
  }
  await expect(page.locator(".error")).toHaveCount(0);
}

/** Ждёт, пока сервер запишет просмотренные слайды главы (номера с нуля). */
async function expectSlideProgress(request: APIRequestContext, token: string, book: number, num: number, want: number[]) {
  await expect
    .poll(
      async () => {
        const p = await getJson<{ slides: Record<string, number[]> }>(request, "/api/progress", bearer(token));
        return p.slides[`${book}:${num}`] ?? [];
      },
      { message: "прогресс просмотренных слайдов на сервере", timeout: 10_000 },
    )
    .toEqual(want);
}

/**
 * Подтверждённые дефекты приложения (ключ — «книга:глава»). Такая глава проходит обычный обход, но без затронутой проверки;
 * сама проверка остаётся строгой в отдельном test.fixme (см. конец bookSuite) и включится, когда дефект исправят.
 * - 9:26: `GET /api/exercises/9/26` отвечает 500 «FOREIGN KEY constraint failed» — у главы 26 «Баз данных» (28 упражнений)
 *   не открывается практика (вкладки «Практика» на странице нет).
 */
const KNOWN_DEFECTS: Record<string, { what: string }> = {};
const defectOf = (book: number, num: number) => KNOWN_DEFECTS[`${book}:${num}`];

// --- набор тестов книги ----------------------------------------------------------------------------------------------------

/**
 * Набор тестов книги: на каждую главу со слайдами — отдельный test (провал локализуется до главы).
 * Тесты идут по одной главе за раз (workers = 1 в конфиге); падение одной главы не отменяет следующие.
 */
export function bookSuite(bookId: number, slug: string) {
  const meta = bookMeta().get(bookId);
  if (!meta) throw new Error(`книга ${bookId} не найдена в sql/books.sql`);
  if (meta.slug !== slug) throw new Error(`у книги ${bookId} короткое имя «${meta.slug}», а не «${slug}»`);
  const titles = textbookTitles(bookId);
  const nums = slideChapters(bookId);
  if (nums.length === 0) throw new Error(`нет файлов слайдов книги ${bookId}`);

  test.describe(`${meta.title} (книга ${bookId})`, () => {
    for (const num of nums) {
      test(`«${meta.title}: глава ${num} — ${titles.get(num) ?? "?"}»`, async ({ page, request }) => {
        const errors = watchChapterConsole(page, !!defectOf(bookId, num));
        const { token } = await loginFresh(page, request);

        // данные главы из API
        const ref = (await chaptersOf(request, bookId)).find((c) => c.num === num);
        expect(ref, `глава ${bookId}:${num} есть в курсе`).toBeTruthy();
        const { id, title } = ref!;
        if (titles.has(num)) expect(title, "название главы в API и в учебнике").toBe(titles.get(num));
        const deck = await getJson<ChapterSlides>(request, `/api/slides/${bookId}/${num}`);
        const file = JSON.parse(fs.readFileSync(path.join(data, "slides", `${two(bookId)}-${two(num)}.json`), "utf8")) as ChapterSlides;
        expect(deck.slides.length, "число слайдов в API и в файле данных").toBe(file.slides.length);
        expect(deck.slides.length).toBeGreaterThan(0);
        const quizzes = countOf(await getJson<Counts>(request, "/api/quizzes"), bookId, num);
        const answers = countOf(await getJson<Counts>(request, "/api/answers"), bookId, num);
        const codeRes = await request.get(`/api/exercises/${bookId}/${num}`);
        const tasks = codeRes.ok() ? ((await codeRes.json()) as { tasks: Task[] }).tasks : [];
        if (!codeRes.ok() && !defectOf(bookId, num)) expect(codeRes.status(), "упражнений нет — 404").toBe(404);
        const hasPractice = tasks.length > 0 || answers > 0;

        // страница главы
        await page.goto(`/book/${bookId}/chapter/${id}`);
        await expect(page.locator("h2")).toHaveText(`Урок ${num}. ${title}`);
        const tabNames = ["Теория", ...(quizzes > 0 ? ["Вопросы"] : []), ...(hasPractice ? ["Практика"] : [])];
        await expect(page.locator(".ch-tab")).toHaveCount(tabNames.length);
        for (const [i, name] of tabNames.entries()) await expect(page.locator(".ch-tab").nth(i)).toContainText(name);

        // теория
        await walkTheory(page, deck);

        // прогресс: просмотрены все слайды главы (номера с нуля)
        await expectSlideProgress(request, token, bookId, num, deck.slides.map((_, i) => i));

        // вопросы и практика (если есть)
        if (quizzes > 0) {
          await page.locator(".ch-tab", { hasText: "Вопросы" }).click();
          await checkQuiz(page, quizzes);
        }
        if (hasPractice) {
          await page.locator(".ch-tab", { hasText: "Практика" }).click();
          await checkPractice(page, tasks, answers);
        }

        expect(errors, "ошибки в консоли браузера").toEqual([]);
      });
    }
    // строгие проверки известных дефектов: пропущены (fixme), пока дефект не исправлен
    for (const num of nums) {
      const known = defectOf(bookId, num);
      if (!known) continue;
      test.fixme(`«${meta.title}: глава ${num}» — ${known.what}`, async ({ page, request }) => {
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
