/* Модель мини-гипервизора для симулятора главы 2: ученик играет монитор виртуальных машин.
   Гость исполняет программу в непривилегированном режиме. Обычные команды идут напрямую, а на
   привилегированных процессор вызывает ловушку, и монитор должен правильно сымитировать действие
   над виртуальным состоянием гостя. Команда POPF в кольце 1 не вызывает ловушки (дыра x86), пока
   не включена двоичная трансляция. */

export interface GuestState {
  pc: number;
  acc: number;
  vif: number;
  vcr3: number;
  queue: number[];
  delivered: number[];
  log: string[];
  mistakes: number;
  silent: boolean;
  halted: boolean;
}

export interface TrapOption {
  label: string;
  ok: boolean;
  why?: string | undefined;
}

export type Inspection =
  | { kind: "direct" }
  | { kind: "silent"; why: string }
  | { kind: "trap"; title: string; options: TrapOption[] };

export const PROGRAMS = [
  {
    id: "base",
    title: "Привилегированные команды",
    code: ["ADD 3", "CLI", "WRCR3 4096", "ADD 2", "RDCR3", "STI", "HLT"],
    goal: "Пройдите программу: на каждой ловушке выберите верную имитацию",
  },
  {
    id: "irq",
    title: "Прерывания",
    code: ["CLI", "IRQ 1", "IRQ 2", "STI", "HLT"],
    goal: "Не потеряйте прерывания: они ждут в очереди, пока гость не разрешит",
  },
  {
    id: "popf",
    title: "Проблема POPF",
    code: ["CLI", "POPF 1", "ADD 2", "HLT"],
    goal: "Выполните программу так, чтобы POPF изменила виртуальный флаг IF",
  },
];

export const initial = (): GuestState => ({
  pc: 0,
  acc: 0,
  vif: 1,
  vcr3: 0,
  queue: [],
  delivered: [],
  log: [],
  mistakes: 0,
  silent: false,
  halted: false,
});

const opt = (label: string, ok: boolean, why?: string): TrapOption => ({ label, ok, why });

/* Что происходит на команде: {kind: "direct"} | {kind: "silent", why} | {kind: "trap", options} */
export function inspect(ins: string, s: GuestState, translate: boolean): Inspection {
  const [op, arg] = ins.split(" ");
  const n = Number(arg);
  switch (op) {
    case "ADD":
      return { kind: "direct" };
    case "CLI":
      return {
        kind: "trap",
        title: "CLI — запретить прерывания",
        options: [
          opt("виртуальный флаг vif ← 0", true),
          opt("выполнить CLI на настоящем процессоре", false, "монитор перестал бы получать прерывания таймера и потерял управление"),
          opt("vif ← 1", false, "это противоположное действие"),
        ],
      };
    case "STI":
      return {
        kind: "trap",
        title: "STI — разрешить прерывания",
        options: [
          opt("vif ← 1 и доставить очередь", true),
          opt("vif ← 1, очередь оставить", false, "прерывания, пришедшие раньше, так и не дойдут до гостя"),
          opt("выполнить STI на настоящем процессоре", false, "настоящий флаг и так включён: гость не получил бы своё состояние"),
        ],
      };
    case "WRCR3":
      return {
        kind: "trap",
        title: `MOV CR3, ${n} — сменить таблицы страниц`,
        options: [
          opt(`виртуальный vcr3 ← ${n}`, true),
          opt(`записать ${n} в настоящий CR3`, false, "гость получил бы доступ к чужой памяти: настоящим CR3 владеет монитор"),
          opt(`acc ← ${n}`, false, "команда пишет в CR3, а не в аккумулятор"),
        ],
      };
    case "RDCR3":
      return {
        kind: "trap",
        title: "MOV acc, CR3 — прочитать таблицы страниц",
        options: [
          opt("acc ← виртуальный vcr3", true),
          opt("acc ← настоящий CR3", false, "гость увидел бы настоящее состояние хозяина, а не своё"),
          opt("vcr3 ← 0", false, "чтение ничего не должно менять"),
        ],
      };
    case "HLT":
      return {
        kind: "trap",
        title: "HLT — остановить процессор",
        options: [
          opt("остановить виртуальный процессор гостя", true),
          opt("остановить настоящий процессор", false, "остановились бы все остальные гости и сам монитор"),
          opt("ничего не делать", false, "гость ждёт прерывания, а процессор хозяина молотил бы впустую"),
        ],
      };
    case "IRQ":
      return {
        kind: "trap",
        title: `внешнее прерывание ${n} для гостя`,
        options: [
          opt("доставить гостю сейчас", s.vif === 1, "гость запретил прерывания: доставлять нельзя"),
          opt("поставить в очередь", s.vif === 0, "гость прерывания разрешил: ждать незачем"),
        ],
      };
    case "POPF":
      if (!translate)
        return {
          kind: "silent",
          why: "В кольце 1 команда POPF не может изменить флаг IF, но и не вызывает ловушку: ничего не произошло, монитор не узнал.",
        };
      return {
        kind: "trap",
        title: `POPF ${n} — загрузить флаги (после трансляции — вызов монитора)`,
        options: [
          opt(`vif ← ${n}`, true),
          opt("игнорировать, как делает процессор", false, "ради этого и включили трансляцию"),
          opt("выполнить POPF на настоящем процессоре", false, "настоящий IF не должен зависеть от гостя"),
        ],
      };
    default:
      return { kind: "direct" };
  }
}

/* Применить верную имитацию (или прямое исполнение) команды к состоянию. */
export function apply(ins: string, s: GuestState): GuestState {
  const [op, arg] = ins.split(" ");
  const n = Number(arg);
  const t = { ...s, pc: s.pc + 1, queue: [...s.queue], delivered: [...s.delivered] };
  switch (op) {
    case "ADD":
      t.acc += n;
      break;
    case "CLI":
      t.vif = 0;
      break;
    case "STI":
      t.vif = 1;
      t.delivered.push(...t.queue);
      t.queue = [];
      break;
    case "WRCR3":
      t.vcr3 = n;
      break;
    case "RDCR3":
      t.acc = t.vcr3;
      break;
    case "HLT":
      t.halted = true;
      break;
    case "IRQ":
      if (t.vif) t.delivered.push(n);
      else t.queue.push(n);
      break;
    case "POPF":
      t.vif = n;
      break;
    default:
  }
  return t;
}

/* Ожидаемое виртуальное состояние при верной имитации всей программы. */
export function expected(code: string[]): GuestState {
  let s = initial();
  for (const ins of code) s = apply(ins, s);
  return s;
}
