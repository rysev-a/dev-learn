/* Модель передачи файла по TCP: окно приёма, окно перегрузки, медленный старт, потери и очередь.
   Это не пакетная симуляция, а пораундовая модель (один шаг — один круговой обход): достаточно,
   чтобы видеть «пилу», влияние окна и алгоритма, потерь и размера буфера. Детерминирована. */
import { getIface, peerOf } from "./model.js";
import { ipStr } from "./ip.js";
import { ping1 } from "./sim.js";

const MSS = 1460;
const INIT = 10 * MSS;

/** путь «туда» по хопам эхо-запроса: список {link, from, fromPort} */
function forwardPath(state, run) {
  const hops = run.hops
    .filter((h) => h.frame.type === "ip" && h.frame.ip.proto === "icmp" && h.frame.ip.icmp.type === "echo-req")
    .sort((a, b) => a.t0 - b.t0);
  return hops.map((h) => ({ link: peerOf(state, h.from, h.fromPort).link, from: h.from, fromPort: h.fromPort, to: h.to }));
}

/** свойства пути до адреса: RTT (мкс), узкое место (Мбит/с), вероятность потери пакета, получатель */
export function pathInfo(state, srcId, dstIp) {
  ping1(state, srcId, dstIp, { id: 900 }); // прогрев ARP и таблиц
  const probe = ping1(state, srcId, dstIp, { id: 901 });
  if (probe.status !== "reply") return { ok: false, status: probe.status };
  const dstId = probe.delivered.find((x) => x.dst === dstIp)?.dev;
  const path = forwardPath(state, probe);
  const rate = Math.min(...path.map((h) => h.link.mbps || 1000));
  const lossP = 1 - path.reduce((a, h) => a * (1 - (h.link.loss || 0) / 100), 1);
  return { ok: true, probe, dstId, path, rtt0: probe.rttUs, rate, lossP, bott: path.find((h) => (h.link.mbps || 1000) === rate) };
}

export function transfer(state, srcId, dstIp, { bytes = 50_000_000 } = {}) {
  const info = pathInfo(state, srcId, dstIp);
  if (!info.ok) return { ok: false, status: info.status, chart: null, text: "нет связи: передавать некуда" };
  const { dstId, path, rtt0, rate, lossP, bott } = info;
  const qlen = getIface(state.devices[bott.from], bott.fromPort).txqueuelen ?? 1000; // пакетов
  const src = state.devices[srcId];
  const dst = state.devices[dstId];
  const rwnd = (dst.rwnd ?? 64) * 1024; // байт
  const cc = src.cc ?? "cubic";

  const rateBps = (rate * 1e6) / 8; // байт/с
  const bdp = (rateBps * rtt0) / 1e6;
  const qcap = qlen * 1500;

  let cwnd = INIT;
  let ssthresh = Infinity;
  let sent = 0;
  let t = 0;
  let lossAcc = 0;
  let losses = 0;
  let maxRtt = rtt0;
  const trace = [{ t: 0, cwnd: cwnd / 1024, rtt: rtt0 / 1000 }];
  let rounds = 0;

  while (sent < bytes && rounds < 4000) {
    rounds++;
    let win;
    let rtt;
    let delivered;
    if (cc === "bbr") {
      // BBR держит скорость у канала и почти игнорирует потери
      win = Math.min(rwnd, rounds < 4 ? cwnd : bdp * 1.25 + 4 * MSS);
      rtt = rtt0 + (Math.max(0, win - bdp) * 8) / (rate * 1e6) * 1e6;
      delivered = Math.min(win, (rateBps * rtt) / 1e6) * (1 - lossP * 0.6);
      cwnd = rounds < 4 ? cwnd * 2 : win;
    } else {
      win = Math.min(cwnd, rwnd);
      const queued = Math.max(0, Math.min(win - bdp, qcap));
      rtt = rtt0 + ((queued * 8) / (rate * 1e6)) * 1e6;
      delivered = Math.min(win, (rateBps * rtt) / 1e6);
      let loss = false;
      if (win > bdp + qcap) loss = true; // очередь переполнена
      lossAcc += (delivered / MSS) * lossP;
      if (lossAcc >= 1) {
        lossAcc -= 1;
        loss = true;
      }
      if (loss) {
        losses++;
        const beta = cc === "cubic" ? 0.7 : 0.5;
        ssthresh = Math.max(2 * MSS, win * beta);
        cwnd = ssthresh;
      } else if (cwnd < ssthresh) cwnd = Math.min(cwnd * 2, ssthresh === Infinity ? Infinity : ssthresh);
      else cwnd += (cc === "cubic" ? 3 : 1) * MSS;
    }
    sent += delivered;
    t += rtt;
    maxRtt = Math.max(maxRtt, rtt);
    trace.push({ t: t / 1000, cwnd: (cc === "bbr" ? win : cwnd) / 1024, rtt: rtt / 1000 });
  }

  const seconds = t / 1e6;
  const mbps = (Math.min(sent, bytes) * 8) / 1e6 / seconds;
  const limit =
    cc === "bbr"
      ? "канал"
      : rwnd < bdp * 0.9
        ? "окно приёма"
        : lossP > 0.001
          ? "потери (алгоритм сбрасывает окно)"
          : "канал";
  const text = [
    `передано ${(bytes / 1e6).toFixed(0)} МБ за ${seconds.toFixed(2)} с — ${mbps.toFixed(1)} Мбит/с`,
    `канал ${rate} Мбит/с · RTT ${(rtt0 / 1000).toFixed(1)} мс · BDP ${(bdp / 1024).toFixed(0)} КБ`,
    `окно приёма ${(rwnd / 1024).toFixed(0)} КБ · алгоритм ${cc} · потерь: ${losses}`,
    `RTT под нагрузкой до ${(maxRtt / 1000).toFixed(0)} мс (очередь ${qlen} пакетов)`,
    `ограничивает: ${limit}`,
  ].join("\n");
  return {
    ok: true,
    status: "done",
    mbps,
    seconds,
    loadedRttMs: maxRtt / 1000,
    losses,
    limit,
    bdpKb: bdp / 1024,
    rwndKb: rwnd / 1024,
    chart: { trace, bdpKb: bdp / 1024, rwndKb: rwnd / 1024, qcapKb: qcap / 1024, cc, from: srcId, to: ipStr(dstIp) },
    text,
  };
}
