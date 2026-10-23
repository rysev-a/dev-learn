import type { APIRequestContext, Page } from "@playwright/test";
import { bearer, chapters, expect } from "./fixtures";

/* Помощники тестов оболочки: прогресс через API, абзацы главы, часы плеера, чтение localStorage. */

/** Малые главы для проверок: книга 12 («Дискретная математика»), глава 1 — слайды, вопросы, ответы; книга 13 («Python»), глава 0 — ещё и код-задачи. */
export const DM1 = { book: 12, num: 1 } as const;
export const PY0 = { book: 13, num: 0 } as const;

export interface ProgressDto {
  slides: Record<string, number[]>;
  quiz: Record<string, (number | null)[]>;
  quizRight: Record<string, number>;
  answers: Record<string, Record<string, string>>;
  code: Record<string, Record<string, string>>;
}

export interface BookDto {
  id: number;
  title: string;
  lessons_count: number;
  parts_count: number;
}
export interface SectionDto {
  id: number;
  title: string;
  chapters: { id: number; num: number; title: string; parts_count: number }[];
}
export interface LessonDto {
  ord: number;
  text: string;
}
export interface ChapterDto {
  id: number;
  num: number;
  title: string;
  section: string;
  lessons: LessonDto[];
}

export async function bookList(request: APIRequestContext): Promise<BookDto[]> {
  return (await request.get("/api/books")).json();
}

export async function courseOf(request: APIRequestContext, book: number): Promise<SectionDto[]> {
  return (await request.get(`/api/books/${book}/course`)).json();
}

export async function chapterDto(request: APIRequestContext, id: number): Promise<ChapterDto> {
  return (await request.get(`/api/chapters/${id}`)).json();
}

/** Глава целиком: внутренний id, номер и абзацы озвучки. */
export async function loadChapter(request: APIRequestContext, ref: { book: number; num: number }): Promise<ChapterDto> {
  const found = (await chapters(request, ref.book)).find((c) => c.num === ref.num);
  if (!found) throw new Error(`нет главы ${ref.book}:${ref.num}`);
  return chapterDto(request, found.id);
}

export async function progressOf(request: APIRequestContext, token: string): Promise<ProgressDto> {
  const res = await request.get("/api/progress", { headers: bearer(token) });
  expect(res.ok(), `прогресс: ${res.status()}`).toBeTruthy();
  return res.json();
}

/** Отметить слайды главы просмотренными (как это делает вкладка «Теория»). */
export async function markSlides(request: APIRequestContext, token: string, book: number, chapter: number, slides: number[]): Promise<void> {
  for (const slide of slides) {
    const res = await request.post("/api/progress/slides", { headers: bearer(token), data: { book, chapter, slide } });
    expect(res.status(), `слайд ${slide}`).toBe(204);
  }
}

/** Ответить на вопрос квиза (выбор записывается один раз). */
export async function answerQuiz(request: APIRequestContext, token: string, book: number, chapter: number, question: number, pick: number): Promise<void> {
  const res = await request.post(`/api/quizzes/${book}/${chapter}/answer`, { headers: bearer(token), data: { question, pick } });
  expect(res.ok(), `ответ на вопрос ${question}: ${res.status()}`).toBeTruthy();
}

/** Идентификаторы код-задач главы. */
export async function taskIds(request: APIRequestContext, book: number, chapter: number): Promise<string[]> {
  const res = await request.get(`/api/exercises/${book}/${chapter}`);
  expect(res.ok(), `задачи ${book}:${chapter}`).toBeTruthy();
  return ((await res.json()) as { tasks: { id: string }[] }).tasks.map((t) => t.id);
}

export async function saveDraft(request: APIRequestContext, token: string, book: number, chapter: number, task: string, code: string): Promise<void> {
  const res = await request.put(`/api/exercises/${book}/${chapter}/${task}/draft`, { headers: bearer(token), data: { code } });
  expect(res.status(), `черновик ${task}`).toBe(204);
}

/** Черновики кода главы на сервере: id задачи → код. */
export async function drafts(request: APIRequestContext, token: string, book: number, chapter: number): Promise<Record<string, string>> {
  const res = await request.get(`/api/exercises/${book}/${chapter}/state`, { headers: bearer(token) });
  expect(res.ok(), `состояние практики: ${res.status()}`).toBeTruthy();
  const state = (await res.json()) as { drafts?: Record<string, string> };
  return state.drafts ?? {};
}

/** Значение ключа `localStorage` страницы. */
export function stored(page: Page, key: string): Promise<string | null> {
  return page.evaluate((k) => window.localStorage.getItem(k), key);
}

/** Секунды абзаца на виртуальных часах плеера: 14 символов в секунду, не меньше трёх. */
export function seconds(text: string): number {
  return Math.max([...text].length / 14, 3);
}

/** `м:сс`, как в плеере. */
export function mmss(secs: number): string {
  const s = Math.round(Math.max(0, secs));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Текст так, как его показывает окно «За кадром»: слова через пробел. */
export function words(text: string): string {
  return text.split(/\s+/).filter(Boolean).join(" ");
}

/**
 * Часы страницы под управлением теста: фальшивые и остановленные с самого начала (вызывать до `goto`);
 * время идёт только по `page.clock.runFor`, поэтому чтение абзацев детерминировано и не ждёт минут.
 */
export async function controlClock(page: Page): Promise<void> {
  await page.clock.install({ time: new Date("2026-03-01T10:00:00") });
  await page.clock.pauseAt(new Date("2026-03-01T10:00:01"));
}

/**
 * Охрана консоли без «Failed to load resource … 404»: у главы без код-задач (например, у «Дискретной математики») вкладки
 * запрашивают `/api/exercises/<книга>/<глава>`, а сервер отвечает 404 — это ожидаемый ответ «задач нет», но браузер пишет его в консоль.
 */
export function assertCleanBut404(guard: { errors: string[] }): void {
  expect(guard.errors.filter((e) => !/status of 404/.test(e)), "ошибки в консоли браузера (кроме 404 «задач нет»)").toEqual([]);
}
