// Озвучка без звука: пока аудио нет, абзац «читается» по виртуальным часам с
// той же скоростью, что и расчёт `cues` в слайдах (~14 символов в секунду).
export const CHARS_PER_SECOND = 14;

export function estimateSeconds(text) {
  return Math.max(3, (text || "").length / CHARS_PER_SECOND);
}

// Часы с интерфейсом, достаточным для плеера (как у HTMLAudioElement).
export class VirtualClock {
  constructor(duration) {
    this.duration = duration;
    this.currentTime = 0;
    this.paused = true;
    this.ontimeupdate = null;
    this.onended = null;
    this._timer = null;
    this._last = 0;
  }

  play() {
    if (!this.paused) return;
    this.paused = false;
    this._last = performance.now();
    this._timer = setInterval(() => {
      const now = performance.now();
      this.currentTime += (now - this._last) / 1000;
      this._last = now;
      if (this.currentTime >= this.duration) {
        this.currentTime = this.duration;
        this.pause();
        this.ontimeupdate?.();
        this.onended?.();
        return;
      }
      this.ontimeupdate?.();
    }, 100);
  }

  pause() {
    this.paused = true;
    clearInterval(this._timer);
    this._timer = null;
  }
}
