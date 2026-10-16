/* Модель размещения машин по узлам NUMA для симулятора главы 11. На хосте два узла: по 8 ядер
   и 32 ГиБ. У машины выбирают, где работают её vCPU и где лежит память: узел 0, узел 1 или
   «растянуть» (пополам). Доля удалённых обращений: свой узел — 0; процессоры и память на разных
   узлах — 1; что-то растянуто, а другое нет — 0,5; растянуто всё — 0,5, а с виртуальной
   топологией NUMA гость сам размещает данные ближе — 0,25. */

export const NODES = [
  { cores: 8, mem: 32 },
  { cores: 8, mem: 32 },
];

export const SCENARIOS = [
  {
    id: "small",
    title: "Четыре небольшие машины",
    vms: [
      { name: "A", vcpus: 4, mem: 16 },
      { name: "B", vcpus: 4, mem: 12 },
      { name: "C", vcpus: 4, mem: 16 },
      { name: "D", vcpus: 4, mem: 12 },
    ],
    goal: "Всё помещается, и удалённых обращений нет совсем (0%)",
    max: 0,
  },
  {
    id: "wide",
    title: "Большая машина",
    vms: [
      { name: "E", vcpus: 12, mem: 40 },
      { name: "F", vcpus: 2, mem: 8 },
      { name: "G", vcpus: 2, mem: 8 },
    ],
    goal: "Всё помещается, а средняя доля удалённых обращений (по vCPU) не больше 20%",
    max: 0.2,
  },
];

export const PLACES = [
  ["0", "узел 0"],
  ["1", "узел 1"],
  ["wide", "растянуть"],
];

// чему равна нагрузка на узел i от машины с таким размещением
const share = (place: string, i: number) => (place === "wide" ? 0.5 : Number(place) === i ? 1 : 0);

export function remote(cpu: string, mem: string, vnuma: any) {
  if (cpu === "wide" && mem === "wide") return vnuma ? 0.25 : 0.5;
  if (cpu === "wide" || mem === "wide") return 0.5;
  return cpu === mem ? 0 : 1;
}

/* plan: {имя: {cpu, mem, vnuma}} → загрузка узлов, переполнения и доля удалённых обращений. */
export function evaluate(vms: { name: string; vcpus: number; mem: number; }[], plan: { [x: string]: any; }) {
  const load = NODES.map(() => ({ cores: 0, mem: 0 }));
  let weighted = 0;
  let total = 0;
  const per = {};
  for (const vm of vms) {
    const p = plan[vm.name];
    NODES.forEach((_, i) => {
      load[i].cores += vm.vcpus * share(p.cpu, i);
      load[i].mem += vm.mem * share(p.mem, i);
    });
    const r = remote(p.cpu, p.mem, p.vnuma);
    per[vm.name] = r;
    weighted += r * vm.vcpus;
    total += vm.vcpus;
  }
  const over = load.some((l, i) => l.cores > NODES[i].cores || l.mem > NODES[i].mem);
  return { load, over, per, avg: total ? weighted / total : 0 };
}

export const defaultPlan = (vms: { name: string; vcpus: number; mem: number; }[]) =>
  Object.fromEntries(vms.map((v) => [v.name, { cpu: "0", mem: "0", vnuma: false }]));
