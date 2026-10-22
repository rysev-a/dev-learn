// Настройки интерфейса: хранятся в localStorage этого браузера.

export const KEYS = {
  theme: "say-theme",
  aside: "say-aside-collapsed",
  anim: "say-anim-auto",
  autoWireLab: "say-autowire-lab",
  autoWireSd: "say-autowire-sd",
  sdBoardH: "say-sd-board-h",
  autoNext: "say-auto-next",
  voiceH: "say-voice-h",
} as const;

export type Theme = "dark" | "light";

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

/** автосвязывание на досках: по умолчанию включено, выключенное хранится как «0» */
export const autoWireOn = (key: typeof KEYS.autoWireLab | typeof KEYS.autoWireSd): boolean => readSetting(key) !== "0";

export const readTheme = (): Theme => (readSetting(KEYS.theme) === "light" ? "light" : "dark");

// Движение сцен выключено: системная настройка «уменьшить движение»
// или переключатель в настройках приложения.
export function motionOff(): boolean {
  const system =
    typeof window !== "undefined" &&
    !!window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  return system || readSetting(KEYS.anim) === "0";
}
