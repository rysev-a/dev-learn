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

// Удалить решения, статусы и черновики кода упражнений.
export function clearPractice() {
  try {
    const drop = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (/^say-(cex|cfail|code)-/.test(k)) drop.push(k);
    }
    drop.forEach((k) => localStorage.removeItem(k));
    return drop.length;
  } catch {
    return 0;
  }
}
