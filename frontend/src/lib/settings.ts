// Настройки интерфейса: хранятся в localStorage этого браузера.

export const KEYS = {
  theme: "say-theme",
  aside: "say-aside-collapsed",
  anim: "say-anim-auto",
} as const;

export function readSetting(key: string): string | null;
export function readSetting<F>(key: string, fallback: F): string | F;
export function readSetting(key: string, fallback: unknown = null): unknown {
  try {
    const v = localStorage.getItem(key);
    return v == null ? fallback : v;
  } catch {
    return fallback;
  }
}

export function writeSetting(key: string, value: string | null): void {
  try {
    if (value == null) localStorage.removeItem(key);
    else localStorage.setItem(key, value);
  } catch {
    /* хранилище недоступно — настройка не сохранится */
  }
}

// Движение сцен выключено: системная настройка «уменьшить движение»
// или переключатель в настройках приложения.
export function motionOff(): boolean {
  const system =
    typeof window !== "undefined" &&
    !!window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  return system || readSetting(KEYS.anim) === "0";
}
