import { expect, type APIRequestContext, type Page } from "@playwright/test";
import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bearer, chapterId } from "./fixtures";

/* Helpers for the learning-module tests: reading course content from SQL files (correct quiz and task answers),
   tab URLs, direct API calls, the code-check worker (fake and real). */

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "..", "..");
const SQL = path.join(ROOT, "backend", "data", "sql");
export const PORT = Number(process.env.E2E_PORT ?? 8099);
export const WORKER_TOKEN = "e2e";

// --- reading course SQL files --------------------------------------------------------------------

type Cell = string | number | null;

/** Rows of all `INSERT INTO <table> (…) VALUES (…)` statements of a file: SQL strings ('' is a quote), numbers, NULL. */
export function parseInserts(file: string, table: string): Cell[][] {
  const text = fs.readFileSync(file, "utf8");
  const head = `INSERT INTO ${table} (`;
  const rows: Cell[][] = [];
  let i = 0;
  for (;;) {
    i = text.indexOf(head, i);
    if (i < 0) return rows;
    i = text.indexOf("VALUES (", i) + "VALUES (".length;
    const row: Cell[] = [];
    for (;;) {
      while (/\s/.test(text[i] ?? "")) i++;
      if (text[i] === "'") {
        let s = "";
        i++;
        for (;;) {
          const c = text[i++];
          if (c === undefined) throw new Error(`unterminated string in ${file}`);
          if (c === "'") {
            if (text[i] === "'") {
              s += "'";
              i++;
              continue;
            }
            break;
          }
          s += c;
        }
        row.push(s);
      } else {
        let t = "";
        while (text[i] !== "," && text[i] !== ")") t += text[i++];
        t = t.trim();
        row.push(t === "NULL" ? null : Number(t));
      }
      while (/\s/.test(text[i] ?? "")) i++;
      if (text[i] === ",") {
        i++;
        continue;
      }
      i++; // «)»
      break;
    }
    rows.push(row);
  }
}

function bookFile(dir: string, book: number): string {
  const prefix = `${String(book).padStart(2, "0")}-`;
  const name = fs.readdirSync(path.join(SQL, dir)).find((f) => f.startsWith(prefix));
  if (!name) throw new Error(`no SQL file for book ${book} in ${dir}`);
  return path.join(SQL, dir, name);
}

export interface QuizQuestion {
  q: string;
  options: string[];
  /** index of the correct option */
  answer: number;
  expl: string;
}

export function quizQuestions(book: number, chapter: number): QuizQuestion[] {
  return parseInserts(bookFile("quizzes", book), "quiz_questions")
    .filter((r) => r[0] === book && r[1] === chapter)
    .sort((a, b) => Number(a[2]) - Number(b[2]))
    .map((r) => ({ q: String(r[3]), options: JSON.parse(String(r[4])) as string[], answer: Number(r[5]), expl: String(r[6]) }));
}

export interface AnswerTask {
  q: string;
  /** accepted answers */
  answers: string[];
  hint: string;
}

export function answerTasks(book: number, chapter: number): AnswerTask[] {
  return parseInserts(bookFile("answers", book), "answer_tasks")
    .filter((r) => r[0] === book && r[1] === chapter)
    .sort((a, b) => Number(a[2]) - Number(b[2]))
    .map((r) => ({ q: String(r[3]), answers: JSON.parse(String(r[4])) as string[], hint: String(r[5] ?? "") }));
}

export function answerTitle(book: number, chapter: number): string {
  const row = parseInserts(bookFile("answers", book), "answer_sets").find((r) => r[0] === book && r[1] === chapter);
  if (!row) throw new Error(`no answer set ${book}:${chapter}`);
  return String(row[2]);
}

export interface CodeTask {
  id: string;
  mode: string;
  title: string;
  statement: string;
  starter: string;
  hint: string;
}

export function codeTasks(book: number, chapter: number): CodeTask[] {
  return parseInserts(bookFile("tasks", book), "tasks")
    .filter((r) => r[0] === book && r[1] === chapter)
    .sort((a, b) => Number(a[3]) - Number(b[3]))
    .map((r) => ({ id: String(r[2]), mode: String(r[4]), title: String(r[5]), statement: String(r[6]), starter: String(r[7] ?? ""), hint: String(r[8] ?? "") }));
}

// --- URLs and API -------------------------------------------------------------------------------

export type Tab = "" | "questions" | "exercises";

/** Chapter tab URL (the path carries the internal chapter id, not the number). */
export async function chapterPath(request: APIRequestContext, book: number, num: number, tab: Tab = ""): Promise<string> {
  const id = await chapterId(request, book, num);
  return `/book/${book}/chapter/${id}${tab ? `/${tab}` : ""}`;
}

/** User progress straight from the server. */
export async function progressOf(request: APIRequestContext, token: string): Promise<{
  quiz: Record<string, (number | null)[]>;
  quizRight: Record<string, number>;
  answers: Record<string, Record<string, string>>;
  code: Record<string, Record<string, string>>;
}> {
  const res = await request.get("/api/progress", { headers: bearer(token) });
  expect(res.ok(), `GET /api/progress: ${res.status()}`).toBeTruthy();
  return res.json();
}

/** Answer a quiz question directly through the API (state setup). */
export async function answerQuiz(request: APIRequestContext, token: string, book: number, num: number, question: number, pick: number) {
  const res = await request.post(`/api/quizzes/${book}/${num}/answer`, { headers: bearer(token), data: { question, pick } });
  expect(res.ok(), `answer to question ${question}: ${res.status()}`).toBeTruthy();
  return (await res.json()) as { pick: number; answer: number; expl: string; right: number };
}

/** Input field and value for `fill`, independent of whitespace case: answer entry as a student would type it. */
export const firstAnswer = (t: AnswerTask): string => t.answers[0] ?? "";

// --- console guard ----------------------------------------------------------------------------

/**
 * Like `guard` from fixtures, but a 404 on `GET /api/exercises/<book>/<chapter>` is not an error: this is how the app learns that a chapter has no
 * code tasks (e.g. answer-entry exercises), and the browser logs such a response to the console; expected `POST /api/exercises/run` rejections are ignored too.
 */
export function learningGuard(page: Page) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() !== "error" || /Blocked script execution in 'about:srcdoc'/.test(m.text())) return;
    if (/Failed to load resource.*404/.test(m.text()) && /\/api\/exercises\/\d+\/\d+$/.test(m.location().url)) return;
    // expected rejections when queuing a check (no worker, empty code, a check already running): the UI shows them as text
    if (/Failed to load resource.*(422|429|503)/.test(m.text()) && m.location().url.endsWith("/api/exercises/run")) return;
    if (/ResizeObserver loop/.test(m.text())) return;
    errors.push(`console.error: ${m.text().slice(0, 300)}`);
  });
  return { errors, assertClean: () => expect(errors, "browser console errors").toEqual([]) };
}

// --- localStorage settings -------------------------------------------------------------------

/** Write a setting to localStorage before the app loads. */
export async function presetSetting(page: Page, key: string, value: string) {
  await page.addInitScript(([k, v]) => { if (window === window.top) window.localStorage.setItem(k as string, v as string); }, [key, value]);
}

// --- code-check worker -----------------------------------------------------------------------

export interface Job {
  id: string;
  lane: string;
  task: { id: string; mode: string } & Record<string, unknown>;
  code: string;
}

export interface WorkerResult {
  status: string;
  results?: Record<string, unknown>[];
  stdout?: string;
  stderr?: string;
}

/**
 * Fake worker: talks to `/internal/worker/*` with the e2e token but does not execute tasks — the test sets the result.
 * This way the queue, the "queued"/"running" states and result display are checked without Docker and deterministically.
 */
export class FakeWorker {
  constructor(
    private readonly request: APIRequestContext,
    readonly name = `fake-${Date.now().toString(36)}`,
  ) {}

  private headers() {
    return { Authorization: `Bearer ${WORKER_TOKEN}` };
  }

  /** Heartbeat: the server treats checking as available for the next 30 seconds. */
  async ping(lanes: string[] = ["light"]): Promise<void> {
    const res = await this.request.post("/internal/worker/ping", { headers: this.headers(), data: { name: this.name, lanes, slots: 1, jobs: [] } });
    expect(res.status(), "worker ping").toBe(204);
  }

  /** Claim a job (long poll up to `waitSec` seconds); `null` — there were no jobs. */
  async claim(waitSec = 15, lanes: string[] = ["light"]): Promise<Job | null> {
    const res = await this.request.post("/internal/worker/claim", {
      headers: this.headers(),
      data: { name: this.name, lanes, slots: 1, wait: waitSec },
      timeout: (waitSec + 15) * 1000,
    });
    if (res.status() === 204) return null;
    expect(res.status(), "worker claim").toBe(200);
    return (await res.json()) as Job;
  }

  /** Return a job result. */
  async complete(job: Job, result: WorkerResult): Promise<void> {
    const res = await this.request.post(`/internal/worker/jobs/${job.id}/result`, { headers: this.headers(), data: { name: this.name, result } });
    expect(res.status(), "worker result").toBe(204);
  }
}

/** All tests pass: the fake worker's result is "solved". */
export const passing = (stdout = ""): WorkerResult => ({ status: "ok", results: [{ ok: true, got: stdout, expected: stdout }], stdout });

/** One test fails: expected/got. */
export const failing = (expected: string, got: string): WorkerResult => ({ status: "ok", results: [{ ok: false, expected, got }], stdout: got });

/** Waits until the server stops counting workers as alive (heartbeat older than 30 s). */
export async function waitNoWorkers(request: APIRequestContext, timeoutMs = 45_000): Promise<void> {
  await expect
    .poll(async () => ((await (await request.get("/api/exercises/runner/status")).json()) as { available: boolean }).available, { timeout: timeoutMs, intervals: [500, 1000, 2000] })
    .toBe(false);
}

/** A unique comment: the solution will not hit the result cache (the key is a hash of the task and code). */
export const unique = () => `# e2e ${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;

// --- real checking in the sandbox -------------------------------------------------------------

/** The real worker is enabled explicitly (`E2E_WORKER=1`) and only with a live Docker that has the sandbox image. */
export const realWorkerRequested = process.env.E2E_WORKER === "1";

export function dockerReady(image = "python:3.13-slim"): boolean {
  if (spawnSync("docker", ["ps"], { stdio: "ignore" }).status !== 0) return false;
  return spawnSync("docker", ["image", "inspect", image], { stdio: "ignore" }).status === 0;
}

export interface RealWorker {
  stop: () => Promise<void>;
}

/** Starts `worker/worker.py` as a child process and waits until the server sees the worker. */
export async function startRealWorker(request: APIRequestContext): Promise<RealWorker> {
  const child: ChildProcess = spawn("uv", ["run", "worker.py", "--server", `http://127.0.0.1:${PORT}`, "--name", "e2e", "--light", "2", "--heavy", "1"], {
    cwd: path.join(ROOT, "worker"),
    env: { ...process.env, CS_CORE_WORKER_TOKEN: WORKER_TOKEN },
    stdio: "ignore",
    detached: true,
  });
  const exited = new Promise<void>((resolve) => child.once("exit", () => resolve()));
  await expect
    .poll(async () => ((await (await request.get("/api/exercises/runner/status")).json()) as { available: boolean }).available, { timeout: 60_000, intervals: [500, 1000] })
    .toBe(true);
  return {
    stop: async () => {
      if (child.pid && child.exitCode === null) {
        try {
          process.kill(-child.pid, "SIGTERM"); // the whole group: uv and python
        } catch {
          /* already finished */
        }
      }
      await Promise.race([exited, new Promise<void>((r) => setTimeout(r, 20_000))]);
    },
  };
}
