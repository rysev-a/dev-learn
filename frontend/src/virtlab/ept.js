/* Модель трансляции адресов гостя для симулятора главы 4 («Память гостя»).
   Стоимость измеряется в обращениях к памяти. Теневые таблицы: промах TLB стоит обход одной таблицы
   (уровней столько, сколько у наименьшей страницы), но каждое изменение отображения — выход (EXIT).
   Вложенные EPT/NPT: промах стоит (g+1)*(h+1)-1 обращений, изменений гостя гипервизор не видит.
   Запись TLB описывает страницу наименьшего из двух размеров: крупная страница гостя на мелкой
   страничке хозяина «дробится». */

export const PAGES = { "4K": 4096, "2M": 2 * 1024 * 1024, "1G": 1024 * 1024 * 1024 };
export const LEVELS = { "4K": 4, "2M": 3, "1G": 2 };
export const TLB_ENTRIES = 64;
export const EXIT_COST = 1000;

const smaller = (a, b) => (PAGES[a] <= PAGES[b] ? a : b);

export function walkCost(mode, guest, host) {
  if (mode === "shadow") return LEVELS[smaller(guest, host)];
  return (LEVELS[guest] + 1) * (LEVELS[host] + 1) - 1;
}

function lcg(seed) {
  let x = seed >>> 0;
  return () => {
    x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
    return x;
  };
}

const MIB = 1024 * 1024;
const randomAddrs = (n, span, seed) => {
  const r = lcg(seed);
  return Array.from({ length: n }, () => (r() % (span / 8)) * 8);
};

export const WORKLOADS = [
  {
    id: "one",
    title: "Один промах TLB",
    note: "один доступ к памяти: смотрим цену обхода",
    make: () => ({ addrs: [0], maps: 0 }),
  },
  {
    id: "scan",
    title: "Сканирование 8 МиБ",
    note: "2048 обращений подряд с шагом 4 КиБ",
    make: () => ({ addrs: Array.from({ length: 2048 }, (_, i) => i * 4096), maps: 0 }),
  },
  {
    id: "random",
    title: "Случайные доступы по 64 МиБ",
    note: "4000 случайных обращений; TLB на 64 записи",
    make: () => ({ addrs: randomAddrs(4000, 64 * MIB, 7), maps: 0 }),
  },
  {
    id: "fork",
    title: "Частые изменения таблиц",
    note: "500 изменений отображения гостем и 2000 случайных обращений по 1 ГиБ",
    make: () => ({ addrs: randomAddrs(2000, 1024 * MIB, 11), maps: 500 }),
  },
];

export function simulate({ mode, guest, host, workload }) {
  const w = WORKLOADS.find((x) => x.id === workload).make();
  const eff = PAGES[smaller(guest, host)];
  const walk = walkCost(mode, guest, host);
  const tlb = [];
  let misses = 0;
  let cost = 0;
  for (const a of w.addrs) {
    const p = Math.floor(a / eff);
    const i = tlb.indexOf(p);
    if (i >= 0) {
      tlb.splice(i, 1);
      cost += 1;
    } else {
      misses += 1;
      cost += walk + 1;
      if (tlb.length >= TLB_ENTRIES) tlb.shift();
    }
    tlb.push(p);
  }
  const exits = mode === "shadow" ? w.maps : 0;
  cost += exits * EXIT_COST;
  return {
    walk,
    accesses: w.addrs.length,
    misses,
    hits: w.addrs.length - misses,
    exits,
    cost,
    effPage: smaller(guest, host),
  };
}

/* Цели: каждая привязана к нагрузке; check получает результат запуска и настройки. */
export const GOALS = [
  {
    id: "walk",
    workload: "one",
    text: "Один промах стоит не больше 15 обращений (вложенные таблицы)",
    check: (r, c) => c.mode === "ept" && r.walk <= 15,
  },
  {
    id: "scan",
    workload: "scan",
    text: "Сканирование 8 МиБ в 4 КиБ-страницах дешевле, чем в EPT: не больше 15 000",
    check: (r, c) => c.mode === "shadow" && c.guest === "4K" && c.host === "4K" && r.cost <= 15000,
  },
  {
    id: "random",
    workload: "random",
    text: "Случайные доступы по 64 МиБ укладываются в 10 000 обращений",
    check: (r) => r.cost <= 10000,
  },
  {
    id: "fork",
    workload: "fork",
    text: "Частые изменения таблиц: не больше 35 000 обращений",
    check: (r) => r.cost <= 35000,
  },
];
