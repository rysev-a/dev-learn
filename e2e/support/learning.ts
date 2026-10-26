import { expect, type APIRequestContext, type Page } from "@playwright/test";
import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bearer, chapterId } from "./fixtures";

/* Приспособления для тестов модулей обучения: чтение содержимого курса из SQL-файлов (верные ответы квизов и задач),
   адреса вкладок, прямые вызовы API, воркер проверки кода (подставной и настоящий). */

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, "..", "..");
const SQL = path.join(ROOT, "backend", "data", "sql");
export const PORT = Number(process.env.E2E_PORT ?? 8099);
export const WORKER_TOKEN = "e2e";

// --- чтение SQL-файлов курса --------------------------------------------------------------------

type Cell = string | number | null;

/** Строки всех `INSERT INTO <table> (…) VALUES (…)` файла: строки SQL ('' — кавычка), числа, NULL. */
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
          if (c === undefined) throw new Error(`обрыв строки в ${file}`);
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
  if (!name) throw new Error(`нет SQL-файла книги ${book} в ${dir}`);
  return path.join(SQL, dir, name);
}

export interface QuizQuestion {
  q: string;
  options: string[];
  /** индекс верного варианта */
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
  /** принимаемые ответы */
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
  if (!row) throw new Error(`нет набора ответов ${book}:${chapter}`);
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

// --- адреса и API -------------------------------------------------------------------------------

export type Tab = "" | "questions" | "exercises";

/** Адрес вкладки главы (в пути — внутренний id главы, не номер). */
export async function chapterPath(request: APIRequestContext, book: number, num: number, tab: Tab = ""): Promise<string> {
  const id = await chapterId(request, book, num);
  return `/book/${book}/chapter/${id}${tab ? `/${tab}` : ""}`;
}

/** Прогресс пользователя прямо с сервера. */
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

/** Ответить на вопрос квиза прямо через API (подготовка состояния). */
export async function answerQuiz(request: APIRequestContext, token: string, book: number, num: number, question: number, pick: number) {
  const res = await request.post(`/api/quizzes/${book}/${num}/answer`, { headers: bearer(token), data: { question, pick } });
  expect(res.ok(), `ответ на вопрос ${question}: ${res.status()}`).toBeTruthy();
  return (await res.json()) as { pick: number; answer: number; expl: string; right: number };
}

/** Поле ввода и значение для `fill`, не зависящие от регистра пробелов: ввод ответа — как набрал бы ученик. */
export const firstAnswer = (t: AnswerTask): string => t.answers[0] ?? "";

// --- охрана консоли ----------------------------------------------------------------------------

/**
 * Как `guard` из fixtures, но 404 на `GET /api/exercises/<книга>/<глава>` не считается ошибкой: так приложение узнаёт, что у главы нет
 * код-задач (например, у упражнений с вводом ответа), а браузер пишет такой ответ в консоль; а также ожидаемые отказы `POST /api/exercises/run`.
 */
export function learningGuard(page: Page) {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(`pageerror: ${e.message}`));
  page.on("console", (m) => {
    if (m.type() !== "error" || /Blocked script execution in 'about:srcdoc'/.test(m.text())) return;
    if (/Failed to load resource.*404/.test(m.text()) && /\/api\/exercises\/\d+\/\d+$/.test(m.location().url)) return;
    // ожидаемые отказы постановки проверки (нет воркера, пустой код, уже идёт проверка): интерфейс показывает их текстом
    if (/Failed to load resource.*(422|429|503)/.test(m.text()) && m.location().url.endsWith("/api/exercises/run")) return;
    if (/ResizeObserver loop/.test(m.text())) return;
    errors.push(`console.error: ${m.text().slice(0, 300)}`);
  });
  return { errors, assertClean: () => expect(errors, "ошибки в консоли браузера").toEqual([]) };
}

// --- настройки в localStorage -------------------------------------------------------------------

/** Записать настройку в localStorage до загрузки приложения. */
export async function presetSetting(page: Page, key: string, value: string) {
  await page.addInitScript(([k, v]) => { if (window === window.top) window.localStorage.setItem(k as string, v as string); }, [key, value]);
}

// --- воркер проверки кода -----------------------------------------------------------------------

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
 * Подставной воркер: говорит с `/internal/worker/*` с токеном e2e, но задания не выполняет — результат задаёт тест.
 * Так очередь, состояния «в очереди»/«выполняется» и показ результатов проверяются без Docker и детерминированно.
 */
export class FakeWorker {
  constructor(
    private readonly request: APIRequestContext,
    readonly name = `fake-${Date.now().toString(36)}`,
  ) {}

  private headers() {
    return { Authorization: `Bearer ${WORKER_TOKEN}` };
  }

  /** Сердцебиение: сервер считает проверку доступной ближайшие 30 секунд. */
  async ping(lanes: string[] = ["light"]): Promise<void> {
    const res = await this.request.post("/internal/worker/ping", { headers: this.headers(), data: { name: this.name, lanes, slots: 1, jobs: [] } });
    expect(res.status(), "ping воркера").toBe(204);
  }

  /** Забрать задание (долгий опрос до `waitSec` секунд); `null` — заданий не было. */
  async claim(waitSec = 15, lanes: string[] = ["light"]): Promise<Job | null> {
    const res = await this.request.post("/internal/worker/claim", {
      headers: this.headers(),
      data: { name: this.name, lanes, slots: 1, wait: waitSec },
      timeout: (waitSec + 15) * 1000,
    });
    if (res.status() === 204) return null;
    expect(res.status(), "claim воркера").toBe(200);
    return (await res.json()) as Job;
  }

  /** Вернуть результат задания. */
  async complete(job: Job, result: WorkerResult): Promise<void> {
    const res = await this.request.post(`/internal/worker/jobs/${job.id}/result`, { headers: this.headers(), data: { name: this.name, result } });
    expect(res.status(), "результат воркера").toBe(204);
  }
}

/** Все тесты верны: результат подставного воркера «решено». */
export const passing = (stdout = ""): WorkerResult => ({ status: "ok", results: [{ ok: true, got: stdout, expected: stdout }], stdout });

/** Один тест не пройден: «ожидалось»/«получено». */
export const failing = (expected: string, got: string): WorkerResult => ({ status: "ok", results: [{ ok: false, expected, got }], stdout: got });

/** Ждёт, пока сервер перестанет считать воркеров живыми (сердцебиение старше 30 с). */
export async function waitNoWorkers(request: APIRequestContext, timeoutMs = 45_000): Promise<void> {
  await expect
    .poll(async () => ((await (await request.get("/api/exercises/runner/status")).json()) as { available: boolean }).available, { timeout: timeoutMs, intervals: [500, 1000, 2000] })
    .toBe(false);
}

/** Уникальный комментарий: решение не попадёт в кэш результатов (ключ — хеш задачи и кода). */
export const unique = () => `# e2e ${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;

// --- настоящая проверка в песочнице -------------------------------------------------------------

/** Настоящий воркер включается явно (`E2E_WORKER=1`) и только при живом Docker с образом песочницы. */
export const realWorkerRequested = process.env.E2E_WORKER === "1";

export function dockerReady(image = "python:3.13-slim"): boolean {
  if (spawnSync("docker", ["ps"], { stdio: "ignore" }).status !== 0) return false;
  return spawnSync("docker", ["image", "inspect", image], { stdio: "ignore" }).status === 0;
}

export interface RealWorker {
  stop: () => Promise<void>;
}

/** Запускает `worker/worker.py` как дочерний процесс и ждёт, пока сервер увидит воркера. */
export async function startRealWorker(request: APIRequestContext): Promise<RealWorker> {
  const child: ChildProcess = spawn("uv", ["run", "worker.py", "--server", `http://127.0.0.1:${PORT}`, "--name", "e2e", "--light", "2", "--heavy", "1"], {
    cwd: path.join(ROOT, "worker"),
    env: { ...process.env, SAY_WORKER_TOKEN: WORKER_TOKEN },
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
          process.kill(-child.pid, "SIGTERM"); // вся группа: uv и python
        } catch {
          /* уже завершён */
        }
      }
      await Promise.race([exited, new Promise<void>((r) => setTimeout(r, 20_000))]);
    },
  };
}
