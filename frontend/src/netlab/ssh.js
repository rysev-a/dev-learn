/* SSH в симуляторе: ключ хоста, known_hosts, вход по ключу или паролю, прыжок через бастион (-J).
   Сеть — настоящая (TCP-проба на порт 22), а проверки ключей и паролей — здесь. */
import { ipStr } from "./ip.js";
import { fmtMs, tcp1 } from "./sim.js";

export const newSsh = (extra = {}) => ({
  hostKey: "SHA256:hostKeyA1",
  passwordAuth: true,
  users: {}, // {alice: {keys: [fp], password: "..."}}
  ...extra,
});

export const keyOf = (d) => d.sshKey ?? null;
export const makeKey = (d) => `SHA256:${d.id}Key${(d.name.length * 7) % 97}`;

/** одно подключение client → server:22; auth: {pass?} → {ok, lines, error, run} */
export function sshHop(state, client, user, ip, { pass = null, noKey = false, label = "" } = {}) {
  const run = tcp1(state, client.id, ip, 22, { session: false });
  if (run.status === "refused") return { ok: false, error: `ssh: connect to host ${ipStr(ip)} port 22: Connection refused`, run };
  if (run.status !== "connected") return { ok: false, error: `ssh: connect to host ${ipStr(ip)} port 22: Connection timed out`, run };
  const srv = state.devices[run.delivered.find((x) => x.dst === ip)?.dev];
  if (!srv?.ssh) return { ok: false, error: "ssh_exchange_identification: на порту нет SSH-сервера", run };
  const lines = [];
  const known = (client.knownHosts ??= {});
  const k = ipStr(ip);
  if (!known[k]) {
    known[k] = srv.ssh.hostKey;
    lines.push(`Warning: Permanently added '${k}' (ключ хоста ${srv.ssh.hostKey}) to known_hosts.`);
  } else if (known[k] !== srv.ssh.hostKey) {
    return {
      ok: false,
      error: [
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        "@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @",
        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
        `Ключ хоста ${k} изменился: был ${known[k]}, сейчас ${srv.ssh.hostKey}. Это либо плановая смена ключа, либо подмена сервера (MITM).`,
        `Если смена законная: ssh-keygen -R ${k}`,
      ].join("\n"),
      run,
    };
  }
  const u = srv.ssh.users[user];
  if (!u) return { ok: false, error: `${user}@${k}: Permission denied (publickey${srv.ssh.passwordAuth ? ",password" : ""}) — пользователя нет`, run, srv };
  const key = noKey ? null : keyOf(client);
  if (key && u.keys.includes(key)) {
    lines.push(`Вход по ключу ${key} выполнен${label}`);
    return { ok: true, auth: "key", lines, run, srv };
  }
  if (srv.ssh.passwordAuth && pass !== null && pass === u.password) {
    lines.push(`Вход по паролю выполнен${label}`);
    return { ok: true, auth: "password", lines, run, srv };
  }
  const why = !srv.ssh.passwordAuth ? "парольный вход выключен, а ваш ключ на сервере не разрешён" : pass === null ? "нужен ключ или пароль" : "неверный пароль";
  return { ok: false, error: `${user}@${k}: Permission denied (publickey${srv.ssh.passwordAuth ? ",password" : ""}) — ${why}`, run, srv };
}

/** ssh [-J jump] user@host: через бастион клиент сначала входит на него, затем TCP до цели идёт с бастиона */
export function sshConnect(state, client, user, ip, { jump = null, pass = null, noKey = false } = {}) {
  if (!jump) return sshHop(state, client, user, ip, { pass, noKey });
  const a = sshHop(state, client, user, jump.ip, { pass, noKey, label: " (бастион)" });
  if (!a.ok) return { ...a, error: `бастион: ${a.error}` };
  const jd = a.srv;
  // дальше TCP идёт с бастиона: клиент проходит аутентификацию на цели своим ключом
  const probe = tcp1(state, jd.id, ip, 22, { session: false });
  if (probe.status !== "connected") return { ok: false, error: `ssh: бастион не достаёт до ${ipStr(ip)}:22 (${probe.status === "refused" ? "порт закрыт" : "нет ответа"})`, run: a.run };
  const srv = state.devices[probe.delivered.find((x) => x.dst === ip)?.dev];
  if (!srv?.ssh) return { ok: false, error: "на цели нет SSH-сервера", run: a.run };
  const known = (client.knownHosts ??= {});
  const k = ipStr(ip);
  if (known[k] && known[k] !== srv.ssh.hostKey) return { ok: false, error: `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! (${k}) — ssh-keygen -R ${k}`, run: a.run };
  known[k] ??= srv.ssh.hostKey;
  const u = srv.ssh.users[user];
  const key = noKey ? null : keyOf(client);
  const lines = [...(a.lines ?? []), `прыжок ${jd.name} → ${srv.name}: ${fmtMs(probe.rttUs)}`];
  if (u && key && u.keys.includes(key)) return { ok: true, auth: "key", lines: [...lines, `Вход по ключу ${key} выполнен на ${srv.name}`], run: a.run, srv };
  if (u && srv.ssh.passwordAuth && pass !== null && pass === u.password) return { ok: true, auth: "password", lines: [...lines, "Вход по паролю выполнен"], run: a.run, srv };
  return { ok: false, error: `${user}@${k}: Permission denied (publickey${srv.ssh.passwordAuth ? ",password" : ""})`, run: a.run, srv };
}
