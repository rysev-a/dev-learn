/* Модель живой миграции для симулятора главы 10 книги «Виртуализация».
   Единицы: память — МиБ, время — секунды, простой — миллисекунды. Модель та же, что в главе:
   круг pre-copy передаёт остаток, за это время гость портит dirty * время МиБ (не больше всей памяти),
   это и есть следующий остаток. Миграция сходится, когда остаток помещается в допустимый простой. */

export const MEM_MIB = 16384;
export const STATE_MS = 20; // передача состояния процессоров и устройств при остановке
export const MAX_ROUNDS = 12;
export const COMPRESS_FACTOR = 1.5; // нулевые страницы и дельты: условный выигрыш канала

/* Параметры:
   dirty, bw — скорость записи гостя и пропускная способность сети (МиБ/с);
   downtimeMs — допустимый простой;
   autoConverge — притормаживать vCPU (старт 20%, +10% за круг, не больше 99%);
   compress — сжатие страниц;
   postcopyAfter — null (только pre-copy) или число кругов pre-copy до переключения на post-copy. */
export interface Simulation {
  outcome: MigrationOutcome;
  rounds: MigrationRound[];
  remaining: number;
  downtime: number;
  total: number;
  faults: number;
  limit: number;
}

export interface MigrationInput {
  dirty: number;
  bw: number;
  downtimeMs: number;
  autoConverge?: boolean;
  compress?: boolean;
  postcopyAfter?: number | null;
  mem?: number;
}

export type MigrationOutcome = "precopy" | "postcopy" | "failed";

export interface MigrationRound {
  k: number;
  sent: number;
  secs: number;
  throttle: number;
  next: number;
}

export function simulate({
  dirty,
  bw,
  downtimeMs,
  autoConverge = false,
  compress = false,
  postcopyAfter = null,
  mem = MEM_MIB,
}: MigrationInput): Simulation {
  const eff = bw * (compress ? COMPRESS_FACTOR : 1);
  const limit = (eff * downtimeMs) / 1000; // сколько МиБ можно передать за допустимый простой
  const rounds: MigrationRound[] = [];
  let remaining = mem;
  let elapsed = 0;
  let throttle = 0;
  let switched = false;

  for (let k = 1; k <= MAX_ROUNDS; k++) {
    if (remaining <= limit) break;
    if (postcopyAfter != null && k > postcopyAfter) {
      switched = true;
      break;
    }
    const secs = remaining / eff;
    if (autoConverge && k >= 2) throttle = Math.min(99, 20 + 10 * (k - 2));
    const rate = dirty * (1 - throttle / 100);
    const next = Math.min(mem, rate * secs);
    rounds.push({ k, sent: remaining, secs, throttle, next });
    elapsed += secs;
    remaining = next;
  }

  const fit = remaining <= limit;
  let outcome: MigrationOutcome;
  let downtime: number;
  let total: number;
  let faults = 0;
  if (fit) {
    outcome = "precopy";
    downtime = (remaining / eff) * 1000 + STATE_MS;
    total = elapsed + downtime / 1000;
  } else if (switched) {
    // гость уже на цели, страницы подтягиваются по требованию и фоном
    outcome = "postcopy";
    downtime = STATE_MS;
    const tail = remaining / eff;
    total = elapsed + tail;
    faults = Math.round(remaining / 64); // условно: одна ошибка на 64 МиБ остатка
  } else {
    // предел кругов исчерпан: машину всё равно приходится остановить с большим остатком
    outcome = "failed";
    downtime = (remaining / eff) * 1000 + STATE_MS;
    total = elapsed + downtime / 1000;
  }
  return {
    outcome,
    rounds,
    remaining,
    downtime: Math.round(downtime),
    total: Math.round(total * 10) / 10,
    faults,
    limit,
  };
}

/* Сценарии и цели. Скорости гостя и сети заданы сценарием, остальное подбирает ученик. */
export interface MigrationScenario {
  id: string;
  title: string;
  dirty: number;
  bw: number;
  goal: string;
  check: (r: Simulation) => boolean;
  hint: string;
}

export const SCENARIOS: MigrationScenario[] = [
  {
    id: "calm",
    title: "Спокойный гость",
    dirty: 300,
    bw: 1250,
    goal: "Pre-copy сошёлся, простой не больше 100 мс",
    check: (r) => r.outcome === "precopy" && r.downtime <= 100,
    hint: "Допустимый простой — это порог остановки: чем он меньше, тем больше кругов, но тем короче пауза.",
  },
  {
    id: "busy",
    title: "Активный гость",
    dirty: 2000,
    bw: 1250,
    goal: "Без post-copy: миграция сошлась, простой не больше 600 мс",
    check: (r) => r.outcome === "precopy" && r.downtime <= 600,
    hint: "Гость пишет быстрее, чем уходит по сети, — остаток не уменьшается. Нужно притормозить vCPU.",
  },
  {
    id: "wild",
    title: "Очень активный гость",
    dirty: 6000,
    bw: 1250,
    goal: "Гибрид: простой не больше 100 мс, общее время не больше 60 с",
    check: (r: { outcome: string; downtime: number; total: number; }) => r.outcome === "postcopy" && r.downtime <= 100 && r.total <= 60,
    hint: "Переключайтесь на post-copy раньше: каждый круг pre-copy здесь стоит около 13 секунд.",
  },
];
