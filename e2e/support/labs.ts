import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, type APIRequestContext, type Page } from "@playwright/test";
import { bearer, chapterId } from "./fixtures";

/* e2e helpers for the labs (books 15, 17, 18): reference solutions are read from the backend data files, not duplicated in tests;
   an exercise is opened by chapter number and id, state is checked both through the UI and the API. */

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DATA = path.join(root, "backend", "data", "labs");

export type LabKind = "sd" | "net" | "virt" | "web";

/** Course book for each lab kind. */
export const BOOK: Record<LabKind, number> = { sd: 18, net: 15, virt: 17, web: 11 };

export interface LabTaskData {
  id: string;
  title: string;
  statement: string;
  hint: string;
  /** exercise scenario together with the reference (`solution`) */
  spec: Record<string, unknown>;
}

interface LabFile {
  book: number;
  chapter: number;
  lab: string;
  tasks: LabTaskData[];
}

const cache = new Map<string, LabFile>();

/** Chapter data file: `backend/data/labs/<kind>/<book>-<chapter:02>.json` (`book` — the default book of the kind unless given: the virtualization labs of the book 19 live beside those of the book 17). */
export function labFile(kind: LabKind, chapter: number, book: number = BOOK[kind]): LabFile {
  const name = `${book}-${String(chapter).padStart(2, "0")}.json`;
  const file = path.join(DATA, kind, name);
  let found = cache.get(file);
  if (!found) {
    found = JSON.parse(fs.readFileSync(file, "utf8")) as LabFile;
    cache.set(file, found);
  }
  return found;
}

/** Chapter numbers that have data files of the book (the default book of the kind unless given), ascending. */
export function labChapters(kind: LabKind, book: number = BOOK[kind]): number[] {
  return fs
    .readdirSync(path.join(DATA, kind))
    .filter((f) => f.startsWith(`${book}-`))
    .map((f) => Number(/-(\d+)\.json$/.exec(f)?.[1]))
    .filter((n) => Number.isFinite(n))
    .sort((a, b) => a - b);
}

/** Books that have data files of the kind, ascending. */
export function labBooks(kind: LabKind): number[] {
  const books = new Set(
    fs
      .readdirSync(path.join(DATA, kind))
      .map((f) => Number(/^(\d+)-\d+\.json$/.exec(f)?.[1]))
      .filter((n) => Number.isFinite(n)),
  );
  return [...books].sort((a, b) => a - b);
}

/** Exercise by chapter number and id. */
export function labTask(kind: LabKind, chapter: number, id: string, book: number = BOOK[kind]): LabTaskData {
  const t = labFile(kind, chapter, book).tasks.find((x) => x.id === id);
  if (!t) throw new Error(`no exercise ${kind} ${chapter}:${id}`);
  return t;
}

/** All chapter exercises in course order. */
export function labTasks(kind: LabKind, chapter: number, book: number = BOOK[kind]): LabTaskData[] {
  return labFile(kind, chapter, book).tasks;
}

/** Exercise reference as a JSON object (`spec.solution`); an error for labs without a reference in the data. */
export function reference(task: LabTaskData): unknown {
  if (task.spec.solution === undefined) throw new Error(`${task.id} has no reference in the data`);
  return task.spec.solution;
}

const url = (book: number, chapter: number, task: string, tail = "") => `/api/exercises/${book}/${chapter}/${task}${tail}`;

/** Exercise draft through the API — the way the UI itself saves it. */
export async function putDraft(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, code: string, book: number = BOOK[kind]): Promise<void> {
  const res = await request.put(url(book, chapter, id, "/draft"), { headers: bearer(token), data: { code } });
  expect(res.status(), `draft ${id}`).toBe(204);
}

/** Solution submitted for server verification (the whole response: status and body). */
export async function putSolved(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, solution: string, book: number = BOOK[kind]) {
  const res = await request.put(url(book, chapter, id, "/solved"), { headers: bearer(token), data: { solution } });
  const text = await res.text();
  let detail = "";
  try {
    detail = (JSON.parse(text) as { detail?: string }).detail ?? "";
  } catch {
    /* empty body (204) */
  }
  return { status: res.status(), detail };
}

export interface ChapterState {
  status: Record<string, string>;
  drafts: Record<string, string>;
}

export async function chapterState(request: APIRequestContext, token: string, kind: LabKind, chapter: number, book: number = BOOK[kind]): Promise<ChapterState> {
  const res = await request.get(`/api/exercises/${book}/${chapter}/state`, { headers: bearer(token) });
  expect(res.ok(), "chapter state").toBeTruthy();
  return (await res.json()) as ChapterState;
}

/** Waits until the server records status `ok` for the exercise (the UI submits the solution itself, and not immediately). */
export async function expectStatusOk(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, book: number = BOOK[kind]): Promise<void> {
  await expect.poll(async () => (await chapterState(request, token, kind, chapter, book)).status[id], { message: `status ${id} on the server`, timeout: 15_000 }).toBe("ok");
}

/** Exercise status on the server right now (`undefined` — no solution). */
export async function statusOf(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, book: number = BOOK[kind]): Promise<string | undefined> {
  return (await chapterState(request, token, kind, chapter, book)).status[id];
}

/** Opens the chapter practice on the needed exercise; waits for the exercise itself to appear on the page. */
export async function openTask(page: Page, request: APIRequestContext, kind: LabKind, chapter: number, id: string, book: number = BOOK[kind]): Promise<void> {
  const cid = await chapterId(request, book, chapter);
  await page.goto(`/book/${book}/chapter/${cid}/exercises?task=${id}`);
  await expect(page.locator(".pr-main .pr-head h3")).toContainText(labTask(kind, chapter, id, book).title);
}

/** Exercise row in the list strip. */
export const listItem = (page: Page, title: string) => page.locator(".pr-list .pr-item", { hasText: title });

/** The "Solved N of M" caption above the exercise list. */
export const progressLabel = (page: Page) => page.locator(".pr-top .pr-top-label").first();

/** Deep copy of a JSON value. */
export function clone<T>(v: T): T {
  return JSON.parse(JSON.stringify(v)) as T;
}
