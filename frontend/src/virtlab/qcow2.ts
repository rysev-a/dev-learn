/* Модель цепочки слоёв qcow2 для симулятора главы 9. Цепочка — массив слоёв от верхнего (текущего,
   в него идут все записи) к базовому. Чтение идёт вниз до первого слоя, где кластер есть; каждая
   проверка слоя — обращение к таблицам. Снимок — новый пустой верхний слой. Слияние (commit)
   переносит кластеры верхнего слоя в нижний. Откат отбрасывает верхний слой. */

export const CLUSTERS = 8;

let uid = 0;
const layer = (name: string, data = {}) => ({ id: ++uid, name, data });

export function initialChain() {
  return [layer("база", { 0: "A", 1: "B", 2: "C", 3: "D" })];
}

export function snapshot(chain: { id: number; name: string; data: {}; }[], n: number) {
  return [layer(`слой ${n}`), ...chain];
}

export function write(chain: any[], c: string|number, d: string) {
  const below = chain.slice(1).some((l) => c in l.data) || (c in chain[0].data);
  const top = { ...chain[0], data: { ...chain[0].data, [c]: d } };
  return { chain: [top, ...chain.slice(1)], copyUp: below };
}

export function read(chain: string|any[], c: string|number) {
  for (let i = 0; i < chain.length; i++)
    if (c in chain[i].data)
      return { value: chain[i].data[c], depth: i, lookups: i + 1, layer: chain[i].name };
  return { value: null, depth: null, lookups: chain.length, layer: null };
}

export function commit(chain: string|any[]) {
  if (chain.length < 2) return null;
  const [top, next, ...rest] = chain;
  return [{ ...next, data: { ...next.data, ...top.data } }, ...rest];
}

export function revert(chain: string|any[]) {
  if (chain.length < 2) return null;
  return chain.slice(1);
}

export const GOALS = [
  { id: "deep", text: "Прочитайте кластер из базы при цепочке в 4 слоя и больше: чтение стоит 4 обращения и больше" },
  { id: "squash", text: "Слейте слои (commit), чтобы цепочка из 4 слоёв сократилась до двух" },
  { id: "rollback", text: "Запишите кластер в верхний слой, откатите слой — и убедитесь, что старые данные вернулись" },
];
