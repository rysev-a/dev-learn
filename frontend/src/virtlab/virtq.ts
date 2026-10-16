/* Модель виртуальной очереди virtio для симулятора главы 6. В очереди SIZE дескрипторов; буфер
   занимает дескриптор от «положил гость» до «забрал гость готовым». Устройство — «спит» (ждёт
   оповещения) или «занято» (само просматривает доступное кольцо). Оповещение — выход в гипервизор.
   Без подавления драйвер звонит после каждой отправки; с подавлением — только если устройство спит. */

export const SIZE = 8;

export interface QueueState {
  avail: number;
  used: number;
  busy: boolean;
  notifies: number;
  posted: number;
  processed: number;
  overflow: boolean;
}

export const initial = (): QueueState => ({
  avail: 0, // буферы, ожидающие устройство
  used: 0, // обработанные, ещё не забранные гостем
  busy: false,
  notifies: 0,
  posted: 0,
  processed: 0,
  overflow: false,
});

export const free = (s: QueueState): number => SIZE - s.avail - s.used;

// Гость кладёт n буферов (пачкой — один раз оповещая). Всё или ничего.
export function post(s: QueueState, n: number, suppress: boolean): QueueState {
  if (n > free(s)) return { ...s, overflow: true };
  const t = { ...s, avail: s.avail + n, posted: s.posted + n, overflow: false };
  if (!suppress || !s.busy) t.notifies += 1;
  t.busy = true;
  return t;
}

// Устройство обрабатывает один буфер; когда доступное кольцо опустело, засыпает.
export function device(s: QueueState): QueueState {
  if (!s.busy || s.avail === 0) return s;
  const t = { ...s, avail: s.avail - 1, used: s.used + 1, processed: s.processed + 1 };
  if (t.avail === 0) t.busy = false;
  return t;
}

export function reap(s: QueueState): QueueState {
  return { ...s, used: 0 };
}

export const GOALS = [
  {
    id: "batch",
    text: "Отправьте 6 буферов и более не больше чем двумя оповещениями (без подавления)",
    check: (s: QueueState, c: { suppress: boolean }) => !c.suppress && s.posted >= 6 && s.notifies <= 2,
  },
  {
    id: "overflow",
    text: "Доведите очередь до переполнения: попробуйте положить буфер, когда свободных дескрипторов нет",
    check: (s: QueueState) => s.overflow,
  },
  {
    id: "suppress",
    text: "Включите подавление оповещений и отправьте 10 буферов и более не больше чем двумя оповещениями",
    check: (s: QueueState, c: { suppress: boolean }) => c.suppress && s.posted >= 10 && s.notifies <= 2,
  },
];
