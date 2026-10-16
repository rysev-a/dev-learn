// Форматирование чисел и времени

// Доля a от b в процентах (0, если b = 0)
export const pct = (a: number, b: number): number => (b ? Math.round((a / b) * 100) : 0);

// Секунды → «м:сс»
export function fmtTime(s: number | null | undefined): string {
  if (!s || !isFinite(s) || s < 0) return "0:00";
  const m = Math.floor(s / 60);
  const ss = Math.floor(s % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${ss}`;
}
