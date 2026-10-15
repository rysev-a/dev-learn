// Настройки интерфейса: хранятся в localStorage этого браузера.

export const KEYS = {
  theme: "say-theme",
  aside: "say-aside-collapsed",
  anim: "say-anim-auto",
};

export function readSetting(key, fallback = null) {
  try {
    const v = localStorage.getItem(key);
    return v == null ? fallback : v;
  } catch {
    return fallback;
  }
}

export function writeSetting(key, value) {
  try {
    if (value == null) localStorage.removeItem(key);
    else localStorage.setItem(key, value);
  } catch {
    /* хранилище недоступно — настройка не сохранится */
  }
}

// Движение сцен выключено: системная настройка «уменьшить движение»
// или переключатель в настройках приложения.
export function motionOff() {
  const system =
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  return system || readSetting(KEYS.anim) === "0";
}
