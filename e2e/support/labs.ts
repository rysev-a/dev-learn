import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, type APIRequestContext, type Page } from "@playwright/test";
import { bearer, chapterId } from "./fixtures";

/* Помощники e2e для лабораторий (книги 15, 17, 18): эталоны читаются из файлов данных бэкенда, а не дублируются в тестах;
   упражнение открывается по номеру главы и id, состояние проверяется и по интерфейсу, и по API. */

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DATA = path.join(root, "backend", "data", "labs");

export type LabKind = "sd" | "net" | "virt";

/** Книга курса для каждого вида лаборатории. */
export const BOOK: Record<LabKind, number> = { sd: 18, net: 15, virt: 17 };

export interface LabTaskData {
  id: string;
  title: string;
  statement: string;
  hint: string;
  /** сценарий упражнения вместе с эталоном (`solution`) */
  spec: Record<string, unknown>;
}

interface LabFile {
  book: number;
  chapter: number;
  lab: string;
  tasks: LabTaskData[];
}

const cache = new Map<string, LabFile>();

/** Файл данных главы: `backend/data/labs/<вид>/<книга>-<глава:02>.json`. */
export function labFile(kind: LabKind, chapter: number): LabFile {
  const name = `${BOOK[kind]}-${String(chapter).padStart(2, "0")}.json`;
  const file = path.join(DATA, kind, name);
  let found = cache.get(file);
  if (!found) {
    found = JSON.parse(fs.readFileSync(file, "utf8")) as LabFile;
    cache.set(file, found);
  }
  return found;
}

/** Номера глав, для которых есть файлы данных, по возрастанию. */
export function labChapters(kind: LabKind): number[] {
  return fs
    .readdirSync(path.join(DATA, kind))
    .map((f) => Number(/-(\d+)\.json$/.exec(f)?.[1]))
    .filter((n) => Number.isFinite(n))
    .sort((a, b) => a - b);
}

/** Упражнение по номеру главы и id. */
export function labTask(kind: LabKind, chapter: number, id: string): LabTaskData {
  const t = labFile(kind, chapter).tasks.find((x) => x.id === id);
  if (!t) throw new Error(`нет упражнения ${kind} ${chapter}:${id}`);
  return t;
}

/** Все упражнения главы в порядке курса. */
export function labTasks(kind: LabKind, chapter: number): LabTaskData[] {
  return labFile(kind, chapter).tasks;
}

/** Эталон упражнения как JSON-объект (`spec.solution`); для лабораторий без эталона в данных — ошибка. */
export function reference(task: LabTaskData): unknown {
  if (task.spec.solution === undefined) throw new Error(`у ${task.id} нет эталона в данных`);
  return task.spec.solution;
}

const url = (book: number, chapter: number, task: string, tail = "") => `/api/exercises/${book}/${chapter}/${task}${tail}`;

/** Черновик упражнения через API — так его сохраняет сам интерфейс. */
export async function putDraft(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, code: string): Promise<void> {
  const res = await request.put(url(BOOK[kind], chapter, id, "/draft"), { headers: bearer(token), data: { code } });
  expect(res.status(), `черновик ${id}`).toBe(204);
}

/** Решение на проверку сервером (ответ целиком: статус и тело). */
export async function putSolved(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string, solution: string) {
  const res = await request.put(url(BOOK[kind], chapter, id, "/solved"), { headers: bearer(token), data: { solution } });
  const text = await res.text();
  let detail = "";
  try {
    detail = (JSON.parse(text) as { detail?: string }).detail ?? "";
  } catch {
    /* тело пустое (204) */
  }
  return { status: res.status(), detail };
}

export interface ChapterState {
  status: Record<string, string>;
  drafts: Record<string, string>;
}

export async function chapterState(request: APIRequestContext, token: string, kind: LabKind, chapter: number): Promise<ChapterState> {
  const res = await request.get(`/api/exercises/${BOOK[kind]}/${chapter}/state`, { headers: bearer(token) });
  expect(res.ok(), "состояние главы").toBeTruthy();
  return (await res.json()) as ChapterState;
}

/** Ждёт, пока сервер запишет упражнению статус `ok` (интерфейс отправляет решение сам и не сразу). */
export async function expectStatusOk(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string): Promise<void> {
  await expect.poll(async () => (await chapterState(request, token, kind, chapter)).status[id], { message: `статус ${id} на сервере`, timeout: 15_000 }).toBe("ok");
}

/** Статус упражнения на сервере прямо сейчас (`undefined` — решения нет). */
export async function statusOf(request: APIRequestContext, token: string, kind: LabKind, chapter: number, id: string): Promise<string | undefined> {
  return (await chapterState(request, token, kind, chapter)).status[id];
}

/** Открывает практику главы на нужном упражнении; ждёт, пока на странице появится само упражнение. */
export async function openTask(page: Page, request: APIRequestContext, kind: LabKind, chapter: number, id: string): Promise<void> {
  const cid = await chapterId(request, BOOK[kind], chapter);
  await page.goto(`/book/${BOOK[kind]}/chapter/${cid}/exercises?task=${id}`);
  await expect(page.locator(".pr-main .pr-head h3")).toContainText(labTask(kind, chapter, id).title);
}

/** Строка упражнения в полосе списка. */
export const listItem = (page: Page, title: string) => page.locator(".pr-list .pr-item", { hasText: title });

/** Подпись «Решено N из M» над списком упражнений. */
export const progressLabel = (page: Page) => page.locator(".pr-top .pr-top-label").first();

/** Глубокая копия JSON-значения. */
export function clone<T>(v: T): T {
  return JSON.parse(JSON.stringify(v)) as T;
}
