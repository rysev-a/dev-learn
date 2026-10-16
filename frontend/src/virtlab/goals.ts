import { useRef, useState } from "react";

export interface LabProps {
  solved: boolean;
  onSolved: (solution: string) => void;
}

/* Цели симулятора: ids — список целей; mark(id, info) отмечает цель достигнутой, а когда
   достигнуты все, один раз сообщает решение (JSON достигнутого) через onSolved. */
export function useGoals(ids: string[], solved: boolean, onSolved: (solution: string) => void) {
  const [done, setDone] = useState<Record<string, unknown>>({});
  const reported = useRef(false);
  const mark = (id: string, info?: unknown) =>
    setDone((d) => {
      if (d[id]) return d;
      const next = { ...d, [id]: info ?? true };
      if (ids.every((g) => next[g]) && !solved && !reported.current) {
        reported.current = true;
        onSolved(JSON.stringify(next));
      }
      return next;
    });
  const isDone = (id: string): boolean => !!done[id] || solved;
  return { isDone, mark, count: ids.filter((g) => done[g] || solved).length };
}
