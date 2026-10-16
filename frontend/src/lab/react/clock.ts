/* Такт для упражнений с защёлками и регистрами: один импульс по кнопке и автогенератор.
   Порт ClockController: вместо сигналов — поле state и подписка onChange. */

const TICK_MS = 600;
export const CLOCK_RATES = [0.5, 1, 2, 4];

/** то, чем управляет такт: id тактового входа, чтение и запись его уровня */
export interface ClockHost {
  clockId: () => string | null | undefined;
  level: (id: string) => number;
  setLevel: (id: string, level: number) => void;
}

export class Clock {
  host: ClockHost;
  onChange: () => void;
  ticking = false;
  auto = false;
  rate = 1;
  edges = 0;
  pulseTimer: ReturnType<typeof setTimeout> | undefined = undefined;
  autoTimer: ReturnType<typeof setInterval> | undefined = undefined;

  constructor(host: ClockHost, onChange: () => void) {
    this.host = host;
    this.onChange = onChange;
  }

  set(patch: { ticking?: boolean; auto?: boolean; rate?: number; edges?: number }) {
    Object.assign(this, patch);
    this.onChange();
  }

  tick(done?: () => void): boolean {
    const id = this.host.clockId();
    if (!id || this.ticking || this.auto || this.host.level(id) === 1) return false;
    this.set({ ticking: true });
    this.host.setLevel(id, 1);
    this.pulseTimer = setTimeout(() => {
      this.host.setLevel(id, 0);
      this.set({ ticking: false });
      done?.();
    }, TICK_MS);
    return true;
  }

  toggleAuto() {
    if (this.auto) return this.stop();
    const id = this.host.clockId();
    if (!id || this.ticking) return;
    this.set({ auto: true });
    this.startAuto();
  }

  setRate(hz: number) {
    this.set({ rate: hz });
    if (this.auto) this.startAuto();
  }

  stop() {
    clearTimeout(this.pulseTimer);
    clearInterval(this.autoTimer);
    const was = this.auto || this.ticking;
    this.set({ auto: false, ticking: false });
    const id = this.host.clockId();
    if (was && id && this.host.level(id) === 1) this.host.setLevel(id, 0);
  }

  countEdge() {
    this.set({ edges: this.edges + 1 });
  }

  resetEdges() {
    this.set({ edges: 0 });
  }

  dispose() {
    clearTimeout(this.pulseTimer);
    clearInterval(this.autoTimer);
  }

  startAuto() {
    clearInterval(this.autoTimer);
    const id = this.host.clockId();
    if (!id) return;
    this.autoTimer = setInterval(() => this.host.setLevel(id, this.host.level(id) ^ 1), 500 / this.rate);
  }
}
