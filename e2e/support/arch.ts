import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, type APIRequestContext, type APIResponse, type Locator, type Page } from "@playwright/test";
import { bearer, chapterId } from "./fixtures";

/* Лаборатории книги 14 (схемы, Мини-8, RISC-V): эталоны читаются из данных курса (backend/data/labs/arch),
   помощники API (черновики, решение, состояние) и открытие упражнения в практике главы. */

const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../backend/data/labs/arch");

export const BOOK = 14;
/** Главы со схемами и ассемблером Мини-8: 6–15; RISC-V: 16–17. */
export const ARCH_CHAPTERS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15] as const;
export const RISCV_CHAPTERS = [16, 17] as const;

export interface Step {
  inputs: Record<string, number>;
  expect: Record<string, number>;
  text: string;
  pulses: number | null;
}
export interface Solution {
  gates?: unknown[];
  wires?: unknown[];
  instances?: unknown[];
  bus_wires?: unknown[];
}
export interface CircuitSpec {
  kind: "circuit";
  section: string;
  mode: "table" | "steps";
  build: "gates" | "blocks";
  inputs: string[];
  labels: string[];
  outputs: string[];
  target: number[][];
  allowed: string[];
  steps: Step[];
  blocks: string[];
  clock: string | null;
  ticks: boolean;
  formula: string;
  solution: Solution;
}
export interface AsmSpec {
  kind: "asm";
  starter: string;
  solution: string;
  disk: string;
  expected: string;
  regions: { name: string; from: number; length: number }[];
}
export interface RiscvSpec {
  profile: "board" | "linux";
  starter: string;
  reference: string;
  data: string;
  max_steps: number;
  tests: unknown[];
}
export interface LabTask<S = CircuitSpec | AsmSpec | RiscvSpec> {
  id: string;
  title: string;
  statement: string;
  hint: string;
  spec: S;
}
interface LabFile {
  book: number;
  chapter: number;
  lab: "arch" | "riscv";
  tasks: LabTask[];
}

const cache = new Map<number, LabFile>();

/** Файл данных главы (14-NN.json). */
export function labFile(chapter: number): LabFile {
  let f = cache.get(chapter);
  if (!f) {
    f = JSON.parse(readFileSync(path.join(DIR, `14-${String(chapter).padStart(2, "0")}.json`), "utf8")) as LabFile;
    cache.set(chapter, f);
  }
  return f;
}

export const tasksOf = (chapter: number): LabTask[] => labFile(chapter).tasks;

export function taskOf(chapter: number, id: string): LabTask {
  const t = tasksOf(chapter).find((x) => x.id === id);
  if (!t) throw new Error(`нет упражнения 14:${chapter}/${id}`);
  return t;
}

export const circuitOf = (chapter: number, id: string): LabTask<CircuitSpec> => taskOf(chapter, id) as LabTask<CircuitSpec>;
export const asmOf = (chapter: number, id: string): LabTask<AsmSpec> => taskOf(chapter, id) as LabTask<AsmSpec>;
export const riscvOf = (chapter: number, id: string): LabTask<RiscvSpec> => taskOf(chapter, id) as LabTask<RiscvSpec>;

/** Эталон как тело решения (то, что хранится черновиком): JSON схемы или текст программы. */
export function solutionText(task: LabTask): string {
  const spec = task.spec as unknown as Record<string, unknown>;
  if (spec["kind"] === "circuit") return JSON.stringify(spec["solution"]);
  if (spec["kind"] === "asm") return String(spec["solution"]);
  return String(spec["reference"]);
}

/** Пустая схема нужной сборки. */
export function emptyDrawing(build: "gates" | "blocks"): string {
  return build === "gates" ? JSON.stringify({ gates: [], wires: [] }) : JSON.stringify({ instances: [], bus_wires: [] });
}

export const EMPTY_GATES = emptyDrawing("gates");

export async function putDraft(request: APIRequestContext, token: string, chapter: number, id: string, code: string): Promise<void> {
  const res = await request.put(`/api/exercises/${BOOK}/${chapter}/${id}/draft`, { headers: bearer(token), data: { code } });
  expect(res.status(), `черновик ${chapter}/${id}`).toBe(204);
}

/** Отправка решения на сервер как это делает интерфейс (ответ — как есть: 204 или 422 с причиной). */
export function putSolved(request: APIRequestContext, token: string, chapter: number, id: string, solution: string): Promise<APIResponse> {
  return request.put(`/api/exercises/${BOOK}/${chapter}/${id}/solved`, { headers: bearer(token), data: { solution } });
}

/** Причина отказа сервера (поле `detail` или `error` ответа 422). */
export async function rejectionOf(res: APIResponse): Promise<string> {
  const body = (await res.json()) as { detail?: string; error?: string };
  return String(body.detail ?? body.error ?? "");
}

export async function solveViaApi(request: APIRequestContext, token: string, chapter: number, id: string): Promise<void> {
  const res = await putSolved(request, token, chapter, id, solutionText(taskOf(chapter, id)));
  expect(res.status(), `решение ${chapter}/${id}: ${res.status()} ${res.status() === 204 ? "" : await res.text()}`).toBe(204);
}

/** Решает через API все упражнения до указанного (порядок курса: из решённых собираются составные блоки). */
export async function solveBefore(request: APIRequestContext, token: string, chapter: number, id: string): Promise<void> {
  for (const ch of ARCH_CHAPTERS) {
    if (ch > chapter) return;
    for (const t of tasksOf(ch)) {
      if (ch === chapter && t.id === id) return;
      await solveViaApi(request, token, ch, t.id);
    }
  }
}

export interface ChapterState {
  status: Record<string, string>;
  drafts: Record<string, string>;
}

export async function chapterState(request: APIRequestContext, token: string, chapter: number): Promise<ChapterState> {
  const res = await request.get(`/api/exercises/${BOOK}/${chapter}/state`, { headers: bearer(token) });
  expect(res.ok()).toBeTruthy();
  return (await res.json()) as ChapterState;
}

/** Статус упражнения на сервере (`ok`, `fail`, …) или `undefined`, если попыток не было. */
export async function statusOf(request: APIRequestContext, token: string, chapter: number, id: string): Promise<string | undefined> {
  return (await chapterState(request, token, chapter)).status[id];
}

/** Открывает упражнение главы в практике и ждёт, пока лаборатория загрузится. */
export async function openTask(page: Page, request: APIRequestContext, chapter: number, id: string): Promise<void> {
  const ch = await chapterId(request, BOOK, chapter);
  await page.goto(`/book/${BOOK}/chapter/${ch}/exercises?task=${id}`);
  await expect(page.locator(".pr-head h3")).toContainText(taskOf(chapter, id).title);
  await expect(page.locator(".lab").first()).toBeVisible();
}

/** Пункт списка упражнений слева. */
export const listItem = (page: Page, title: string) => page.locator(`.pr-item[title="${title}"]`);

/* ——— Действия на странице ——— */

/** Клик мышью в центр элемента (SVG-элементы доски принимают указатель, а не `click()` с проверками видимости). */
export async function clickCenter(page: Page, loc: Locator): Promise<void> {
  const b = await loc.boundingBox();
  if (!b) throw new Error("у элемента нет рамки");
  await page.mouse.click(b.x + b.width / 2, b.y + b.height / 2);
}

export async function centerOf(loc: Locator): Promise<{ x: number; y: number }> {
  const b = await loc.boundingBox();
  if (!b) throw new Error("у элемента нет рамки");
  return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
}

/** Тумблер входа на доске: для вентилей — узел входа, для блоков — «чип» в рамке «Входы». */
function inputToggle(page: Page, spec: CircuitSpec, id: string): Locator {
  const index = spec.inputs.indexOf(id);
  if (spec.build === "gates") return page.locator(".input-node").nth(index).locator(".node-click");
  return page.locator(".bbox.top").first().locator(".bchip").nth(index);
}

/**
 * Проходит сценарий упражнения «по шагам» руками и ждёт отметки шага «выполнен».
 * Если упражнение тактовое (`ticks`), такт — импульсы: поднятый CLK сначала опускают (новый фронт), выставляют данные, затем
 * подают нужное число фронтов (`pulses`). Иначе такт — обычный уровень: при спаде его опускают первым, при подъёме — последним.
 */
export async function playSteps(page: Page, spec: CircuitSpec): Promise<void> {
  const level: Record<string, number> = Object.fromEntries(spec.inputs.map((i) => [i, 0]));
  const clock = spec.clock;
  const toggle = async (id: string) => {
    await clickCenter(page, inputToggle(page, spec, id));
    level[id] = 1 - (level[id] ?? 0);
  };
  for (const [n, step] of spec.steps.entries()) {
    const target = clock === null ? 0 : (step.inputs[clock] ?? 0);
    if (clock !== null && level[clock] === 1 && (spec.ticks || target === 0)) await toggle(clock);
    for (const [id, v] of Object.entries(step.inputs)) {
      if (id !== clock && level[id] !== v) await toggle(id);
    }
    if (clock !== null && target === 1) {
      // «тактов: N» — столько фронтов нужно подать; между ними такт опускается
      for (let pulse = 0; pulse < (spec.ticks ? (step.pulses ?? 1) : 1); pulse++) {
        if (level[clock] === 1) await toggle(clock);
        await toggle(clock);
      }
    }
    await expect.poll(() => page.locator(".lab-step.done").count(), { message: `шаг ${n + 1}: ${step.text}` }).toBeGreaterThan(n);
  }
}

/** Упражнение со схемой решено в интерфейсе и принято сервером. */
export async function expectCircuitSolved(page: Page, request: APIRequestContext, token: string, chapter: number, task: LabTask<CircuitSpec>): Promise<void> {
  const spec = task.spec;
  await expect(page.locator(".lab-alert.ok, .lab-alert").first()).toContainText("Схема работает");
  await expect(page.locator(".lab-board-card ~ .lab-card .lab-badge.ok, .lab-card-head .lab-badge.ok").first()).toBeVisible();
  const item = listItem(page, task.title);
  await expect(item).toHaveClass(/\bok\b/);
  await expect(item.locator(".pr-mark")).toHaveText("✓");
  await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
  await expect(page.locator("p.error")).toHaveCount(0);
  await expect.poll(() => statusOf(request, token, chapter, task.id), { message: `статус ${chapter}/${task.id} на сервере` }).toBe("ok");
  if (spec.mode === "table") await expect(page.locator(".lab-tt .bad-mark")).toHaveCount(0);
}
