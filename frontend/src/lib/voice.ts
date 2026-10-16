// Озвучка без звука: пока аудио нет, абзац «читается» по виртуальным часам с
// той же скоростью, что и расчёт `cues` в слайдах (~14 символов в секунду).
export const CHARS_PER_SECOND = 14;

export function estimateSeconds(text: string | null | undefined): number {
  return Math.max(3, (text || "").length / CHARS_PER_SECOND);
}

// Часы с интерфейсом, достаточным для плеера (как у HTMLAudioElement).
export class VirtualClock {
  duration: number;
  currentTime = 0;
  paused = true;
  ontimeupdate: (() => void) | null = null;
  onended: (() => void) | null = null;
  onerror: (() => void) | null = null;
  private timer: ReturnType<typeof setInterval> | null = null;
  private last = 0;

  constructor(duration: number) {
    this.duration = duration;
  }

  play(): Promise<void> {
    if (!this.paused) return Promise.resolve();
    this.paused = false;
    this.last = performance.now();
    this.timer = setInterval(() => {
      const now = performance.now();
      this.currentTime += (now - this.last) / 1000;
      this.last = now;
      if (this.currentTime >= this.duration) {
        this.currentTime = this.duration;
        this.pause();
        this.ontimeupdate?.();
        this.onended?.();
        return;
      }
      this.ontimeupdate?.();
    }, 100);
    return Promise.resolve();
  }

  pause(): void {
    this.paused = true;
    if (this.timer != null) clearInterval(this.timer);
    this.timer = null;
  }
}
