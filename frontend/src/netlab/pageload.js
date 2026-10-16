/* Загрузка веб-страницы по HTTP/1.1, HTTP/2 и HTTP/3: пораундовая модель. Страница — HTML и N ресурсов;
   считаем рукопожатия, число «кругов» запросов, передачу по узкому месту и цену потерь:
   h1 — шесть соединений, h2 — одно TCP (потеря тормозит все потоки), h3 — QUIC (потоки независимы). */
import { ipStr } from "./ip.js";
import { udp1 } from "./sim.js";
import { pathInfo } from "./transfer.js";

const PROTOS = { h1: "HTTP/1.1", h2: "HTTP/2", h3: "HTTP/3" };

export function pageModel({ rtt, rate, lossP, count, kb, https }, proto) {
  const bytes = (count + 1) * kb * 1024;
  const L = (bytes / 1460) * lossP; // ожидаемое число потерянных пакетов
  const tcpSetup = rtt; // SYN → SYN-ACK
  const tlsSetup = https ? rtt : 0; // TLS 1.3: ещё один круг
  const xfer = ((bytes * 8) / (rate * 1e6)) * 1e6; // мкс по узкому месту
  const slow = 3 * rtt; // разгон окна
  let setup, rounds, loss;
  if (proto === "h1") {
    setup = tcpSetup + tlsSetup;
    rounds = 1 + Math.ceil(count / 6); // HTML, затем ресурсы по 6 штук
    loss = (L * rtt) / 6;
  } else if (proto === "h2") {
    setup = tcpSetup + tlsSetup;
    rounds = 2; // HTML и все ресурсы разом
    loss = L * rtt; // потеря стопорит все потоки
  } else {
    setup = rtt; // QUIC: транспорт и шифрование за один круг
    rounds = 2;
    loss = L * rtt * 0.15;
  }
  const total = setup + rounds * rtt + xfer + (proto === "h1" ? slow * 1.5 : slow) + loss;
  return { proto, total, setup, rounds, xfer, loss, L };
}

/** проверка условий для HTTP/3: UDP/443 должен проходить; иначе браузер откатывается на HTTP/2 */
export function pageload(state, d, { dstIp, https = true }) {
  const info = pathInfo(state, d.id, dstIp);
  if (!info.ok) return { ok: false, error: "нет связи с сервером" };
  const srv = state.devices[info.dstId];
  const http = srv?.http;
  if (!http?.page) return { ok: false, error: "на сервере нет страницы для измерения" };
  const want = http.protocol ?? "h1";
  let used = want;
  let note = "";
  if (want === "h3") {
    const u = udp1(state, d.id, dstIp, 443);
    if (u.status !== "reply") {
      used = "h2";
      note = "UDP/443 до сервера не проходит или не слушается — браузер откатился на HTTP/2";
    }
  }
  const env = { rtt: info.rtt0, rate: info.rate, lossP: info.lossP, count: http.page.count, kb: http.page.kb, https };
  const all = ["h1", "h2", "h3"].map((p) => pageModel(env, p));
  const chosen = all.find((x) => x.proto === used);
  return { ok: true, want, used, note, chosen, all, env, ip: ipStr(dstIp) };
}

export function fmtPage(r) {
  if (!r.ok) return `pageload: ${r.error}`;
  const s = (us) => (us / 1e6).toFixed(2);
  const L = [
    `страница: ${r.env.count + 1} ресурсов по ~${r.env.kb} КБ · RTT ${(r.env.rtt / 1000).toFixed(0)} мс · канал ${r.env.rate} Мбит/с · потери ${(r.env.lossP * 100).toFixed(1)}%`,
    `сервер предлагает: ${PROTOS[r.want]}${r.note ? " → " + PROTOS[r.used] : ""}`,
    `загрузка: ${s(r.chosen.total)} с (рукопожатия ${s(r.chosen.setup)}, ${r.chosen.rounds} кругов запросов, передача ${s(r.chosen.xfer)}, потери ${s(r.chosen.loss)})`,
    "",
    "для сравнения:",
    ...r.all.map((x) => `  ${PROTOS[x.proto].padEnd(9)} ${s(x.total)} с${x.proto === r.used ? "   ← сейчас" : ""}`),
  ];
  if (r.note) L.push("", r.note);
  return L.join("\n");
}
