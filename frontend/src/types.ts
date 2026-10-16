// Типы данных, которыми клиент обменивается с бэкендом (backend/app/**/router.py).

export interface User {
  id: number;
  email: string;
  login: string;
}

export interface Book {
  id: number;
  title: string;
  /** короткое имя, каталог слайдов в src/slides и имя иконки — из backend/app/data/sql/books.sql */
  slug?: string | null;
  slides_dir?: string | null;
  icon?: string | null;
  ord?: number;
  sections_count?: number;
  lessons_count?: number;
  parts_count?: number;
}

export interface ChapterSummary {
  id: number;
  num: number;
  title: string;
  parts_count: number;
}

export interface Section {
  id: number;
  title: string;
  chapters: ChapterSummary[];
}

// Одна «часть» главы: абзац урока, свой слайд и свой файл озвучки.
export interface Lesson {
  id: string;
  ord: number;
  text: string;
  audio: string;
  dur: number;
}

export interface Chapter {
  id: number;
  num: number;
  title: string;
  section: string;
  lessons: Lesson[];
}

export type TaskMode = "func" | "stdout" | "sql" | "rust" | "c" | "js" | "lab";

// Задача, как её видит клиент: условие, заготовка и подсказка (тесты остаются на сервере).
export interface Task {
  id: string;
  mode: TaskMode;
  title: string;
  statement: string;
  starter: string;
  hint: string;
  dataset?: string;
  schema?: SqlDataset;
}

export interface SqlColumn {
  name: string;
  type: string;
  pk: boolean;
  notnull: boolean;
  fk?: { table: string; column: string } | null;
}

export interface SqlTable {
  name: string;
  kind: string;
  columns: SqlColumn[];
  rows: SqlValue[][];
  total: number;
}

// Связь «внешний ключ → родитель»
export interface SqlRelation {
  from: string;
  from_col: string;
  to: string;
  to_col: string;
}

export interface SqlDataset {
  tables: SqlTable[];
  relations: SqlRelation[];
}

export type SqlValue = string | number | null;

export interface ChapterTasks {
  tasks: Task[];
  datasets: Record<string, SqlDataset>;
}

export type TaskStatus = "ok" | "bad";

export interface Attempt {
  id: number;
  code: string;
  status: string;
  passed: number;
  total: number;
  created_at: string;
}

// Результат проверки SQL-задачи (поля got_*, exp_*) в том виде, как его отдаёт сервер
export interface SqlResultView {
  got_rows?: SqlValue[][];
  exp_rows?: SqlValue[][];
  got_cols?: string[];
  exp_cols?: string[];
  got_total?: number;
  exp_total?: number;
  ordered?: boolean;
}

// Результат одного теста: для функций — вызов (args), для SQL — таблицы (kind: "rows")
export interface TestResult extends SqlResultView {
  ok: boolean;
  got?: unknown;
  expected?: unknown;
  error?: string | null;
  args?: string;
  kind?: string;
}

export interface RunResult {
  status: string;
  results: TestResult[];
  stdout?: string;
  stderr?: string;
  passed?: number;
  total?: number;
  solved?: boolean;
  okAll?: boolean | undefined;
  attempt?: { id: number; status: string; created_at: string };
}

// Прогресс пользователя; ключ — «книга:номер_главы».
export interface ProgressData {
  slides: Record<string, number[]>;
  quiz: Record<string, (number | null)[]>;
  /** сколько ответов верны: {«книга:глава»: число}; считает сервер, ответов клиент не знает */
  quizRight: Record<string, number>;
  answers: Record<string, Record<string, string>>;
  code: Record<string, Record<string, TaskStatus>>;
}

export interface QuizQuestion {
  q: string;
  options: string[];
}

/** Верный ответ и пояснение: сервер отдаёт их только после того, как пользователь выбрал вариант */
export interface QuizReveal {
  answer: number;
  expl: string;
}

export interface Quiz {
  kind: "theory";
  title: string;
  questions: QuizQuestion[];
  /** по вопросам: раскрытый ответ или null, если на вопрос ещё не отвечали */
  reveal: (QuizReveal | null)[];
}

/** Ответ сервера на выбор варианта */
export interface QuizAnswerResult extends QuizReveal {
  pick: number;
  right: number;
}

export interface PracticeTask {
  q: string;
  hint?: string;
}

/** Задачи с вводом ответа: верные ответы знает только сервер, он же проверяет введённое */
export interface PracticeSet {
  kind: "practice";
  title: string;
  tasks: PracticeTask[];
  /** решённые пользователем задачи: {номер: принятый ответ} */
  solved: Record<string, string>;
}
