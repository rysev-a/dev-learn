import type { APIRequestContext, Page } from "@playwright/test";
import { bearer, chapters, expect } from "./fixtures";

/* Shell test helpers: progress through the API, chapter paragraphs, player clock, localStorage reads. */

/** Small chapters for checks: book 12 (Discrete Mathematics), chapter 1 — slides, questions, answers; book 13 (Python), chapter 0 — also code tasks. */
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

/** A whole chapter: internal id, number and voice-over paragraphs. */
export async function loadChapter(request: APIRequestContext, ref: { book: number; num: number }): Promise<ChapterDto> {
  const found = (await chapters(request, ref.book)).find((c) => c.num === ref.num);
  if (!found) throw new Error(`no chapter ${ref.book}:${ref.num}`);
  return chapterDto(request, found.id);
}

export async function progressOf(request: APIRequestContext, token: string): Promise<ProgressDto> {
  const res = await request.get("/api/progress", { headers: bearer(token) });
  expect(res.ok(), `progress: ${res.status()}`).toBeTruthy();
  return res.json();
}

/** Mark the chapter's slides as viewed (as the Theory tab does). */
export async function markSlides(request: APIRequestContext, token: string, book: number, chapter: number, slides: number[]): Promise<void> {
  for (const slide of slides) {
    const res = await request.post("/api/progress/slides", { headers: bearer(token), data: { book, chapter, slide } });
    expect(res.status(), `slide ${slide}`).toBe(204);
  }
}

/** Answer a quiz question (the pick is recorded once). */
export async function answerQuiz(request: APIRequestContext, token: string, book: number, chapter: number, question: number, pick: number): Promise<void> {
  const res = await request.post(`/api/quizzes/${book}/${chapter}/answer`, { headers: bearer(token), data: { question, pick } });
  expect(res.ok(), `answer to question ${question}: ${res.status()}`).toBeTruthy();
}

/** Ids of the chapter's code tasks. */
export async function taskIds(request: APIRequestContext, book: number, chapter: number): Promise<string[]> {
  const res = await request.get(`/api/exercises/${book}/${chapter}`);
  expect(res.ok(), `tasks ${book}:${chapter}`).toBeTruthy();
  return ((await res.json()) as { tasks: { id: string }[] }).tasks.map((t) => t.id);
}

export async function saveDraft(request: APIRequestContext, token: string, book: number, chapter: number, task: string, code: string): Promise<void> {
  const res = await request.put(`/api/exercises/${book}/${chapter}/${task}/draft`, { headers: bearer(token), data: { code } });
  expect(res.status(), `draft ${task}`).toBe(204);
}

/** Chapter code drafts on the server: task id → code. */
export async function drafts(request: APIRequestContext, token: string, book: number, chapter: number): Promise<Record<string, string>> {
  const res = await request.get(`/api/exercises/${book}/${chapter}/state`, { headers: bearer(token) });
  expect(res.ok(), `practice state: ${res.status()}`).toBeTruthy();
  const state = (await res.json()) as { drafts?: Record<string, string> };
  return state.drafts ?? {};
}

/** Value of a page's `localStorage` key. */
export function stored(page: Page, key: string): Promise<string | null> {
  return page.evaluate((k) => window.localStorage.getItem(k), key);
}

/** Paragraph seconds on the player's virtual clock: 14 characters per second, at least three. */
export function seconds(text: string): number {
  return Math.max([...text].length / 14, 3);
}

/** `m:ss`, as in the player. */
export function mmss(secs: number): string {
  const s = Math.round(Math.max(0, secs));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Text as the voice-over window shows it: words separated by spaces. */
export function words(text: string): string {
  return text.split(/\s+/).filter(Boolean).join(" ");
}

/**
 * Page clock controlled by the test: fake and stopped from the very start (call before `goto`);
 * time moves only through `page.clock.runFor`, so paragraph reading is deterministic and does not wait for minutes.
 */
export async function controlClock(page: Page): Promise<void> {
  await page.clock.install({ time: new Date("2026-03-01T10:00:00") });
  await page.clock.pauseAt(new Date("2026-03-01T10:00:01"));
}

/**
 * Console guard without "Failed to load resource … 404": for a chapter without code tasks (e.g. Discrete Mathematics) the tabs
 * request `/api/exercises/<book>/<chapter>` and the server answers 404 — the expected "no tasks" response, but the browser logs it to the console.
 */
export function assertCleanBut404(guard: { errors: string[] }): void {
  expect(guard.errors.filter((e) => !/status of 404/.test(e)), "browser console errors (except the 404 \"no tasks\")").toEqual([]);
}
