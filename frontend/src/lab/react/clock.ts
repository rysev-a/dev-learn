/* Такт для упражнений с защёлками и регистрами: один импульс по кнопке и автогенератор.
   Порт ClockController: вместо сигналов — поле state и подписка onChange. */

const TICK_MS = 600;
export const CLOCK_RATES = [0.5, 1, 2, 4];

export class Clock {
  constructor(host: { clockId: () => any; level: (id: string|number) => any; setLevel: (id: string|number,level: number) => void; }, onChange: () => void) {
    this.host = host; // { clockId(), level(id), setLevel(id, v) }
    this.onChange = onChange;
    this.ticking = false;
    this.auto = false;
    this.rate = 1;
    this.edges = 0;
    this.pulseTimer = undefined;
    this.autoTimer = undefined;
  }

  set(patch: { ticking?: boolean; auto?: boolean; rate?: any; edges?: any; }) {
    Object.assign(this, patch);
    this.onChange();
  }

  tick(done: () => void) {
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

  setRate(hz: any) {
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
