// Выгрузка лаборатории «Компьютерные сети» в JSON для Rust-крейта shared-rs/netlab: для каждого упражнения — условие,
// исходная сеть (результат build()), цели, шаги решения (функции развёрнуты), а также «золотые» результаты TypeScript-движка
// (проверка целей на исходной и решённой сети, вывод команд терминала) — для дифференциальных тестов.
//
// Запуск: cd frontend && node scripts/net-export.mjs <каталог вывода>
//   → <каталог>/scenarios.json (для shared-rs/netlab: cargo run --release --bin import -- <каталог> <каталог данных>)
//   → <каталог>/golden.json   (копируется в shared-rs/netlab/tests/golden.json)
// Показать вывод команд движка TS для одного упражнения: node scripts/net-export.mjs --show <id> [start|solved]
// То же для «краевых» команд: node scripts/net-export.mjs --edge <id>
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const showIdx = args.indexOf("--show");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "net-export-"));
const nl = path.join(root, "src/netlab");

const entry = `
export { NET_CHAPTERS } from ${JSON.stringify(path.join(nl, "registry.ts"))};
export { applyOps, checkGoals } from ${JSON.stringify(path.join(nl, "check.ts"))};
export { exec } from ${JSON.stringify(path.join(nl, "term.ts"))};
export { clone, strip } from ${JSON.stringify(path.join(nl, "model.ts"))};
`;
fs.writeFileSync(path.join(tmp, "entry.ts"), entry);
await build({
  entryPoints: [path.join(tmp, "entry.ts")], bundle: true, platform: "node", format: "cjs", outfile: path.join(tmp, "bundle.cjs"),
  nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
const T = await import(pathToFileURL(path.join(tmp, "bundle.cjs")).href);
const { NET_CHAPTERS, applyOps, checkGoals, exec, clone, strip } = T.default ?? T;

/* ---- хеш строки: две FNV-1a по 32 бита с разными начальными значениями → 16 символов hex ---- */
function fnv(str, basis) {
  let h = basis >>> 0;
  for (const b of Buffer.from(str, "utf8")) {
    h ^= b;
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h.toString(16).padStart(8, "0");
}
const hash = (s) => fnv(s, 0x811c9dc5) + fnv(s, 0x01000193);
const num = (x) => String(x);

/* ---- сводка проверки целей: то, что должно совпасть у Rust-движка ---- */
function summarize(results) {
  return results.map((r) => ({
    id: r.id,
    ok: r.ok,
    detail: r.detail,
    events: r.run.events.length,
    ev_hash: hash(r.run.events.map((e) => `${num(e.t)}|${e.dev}|${e.kind}|${e.text}`).join("\n")),
    hops: r.run.hops.length,
    hop_hash: hash(r.run.hops.map((h) => `${num(h.t0)}|${num(h.t1)}|${h.from}|${h.fromPort}|${h.to}|${h.toPort}|${h.kind}|${h.label}`).join("\n")),
    delivered: r.run.delivered.length,
    chart: r.run.chart ? { n: r.run.chart.trace.length, last: r.run.chart.trace[r.run.chart.trace.length - 1] } : null,
  }));
}

/* ---- набор команд терминала для сценария: по целям, по устройствам и по службам ---- */
const firstIp = (d) => d.ifaces.find((i) => i.ip)?.ip ?? null;
function target(state, spec) {
  if (typeof spec === "string" && spec.startsWith("@")) {
    const d = state.devices[spec.slice(1).split(".")[0]];
    return d ? firstIp(d) : null;
  }
  return spec;
}
function battery(state, goals) {
  const cmds = [];
  const add = (dev, line) => cmds.push([dev, line]);
  const froms = new Set();
  for (const g of goals) {
    const x = g.ping ?? g.tcp ?? g.udp ?? g.dns ?? g.mtu ?? g.lbspread ?? g.ssh ?? g.page ?? g.http ?? g.xfer;
    const from = x.from ?? x.dev;
    froms.add(from);
    if (g.ping) {
      const t = target(state, g.ping.to);
      if (t) {
        add(from, `ping -c 2 ${t}`);
        add(from, `traceroute ${t}`);
        if (g.ping.size !== undefined) add(from, `ping -c 1 -s ${g.ping.size} -M do ${t}`);
      }
    } else if (g.tcp) {
      const t = target(state, g.tcp.to);
      if (t) add(from, `nc -zv ${t} ${g.tcp.port}`);
    } else if (g.udp) {
      const t = target(state, g.udp.to);
      if (t) add(from, `nc -u ${t} ${g.udp.port}`);
    } else if (g.dns) {
      add(from, `dig ${g.dns.name}`);
    } else if (g.http) {
      const h = g.http;
      add(from, `curl -v${h.follow ? "L" : ""}${h.method === "HEAD" ? "I" : ""} ${h.proxy ? `-x ${h.proxy} ` : ""}${h.method && h.method !== "HEAD" ? `-X ${h.method} ` : ""}${h.url}`);
    } else if (g.ssh) {
      const s = g.ssh;
      const t = target(state, s.to);
      const j = s.via ? target(state, s.via) : null;
      if (t) add(from, `ssh ${j ? `-J ${j} ` : ""}${s.pass ? `-P ${s.pass} ` : ""}${s.user}@${t}`);
    } else if (g.page) {
      const t = target(state, g.page.to);
      if (t) add(from, `pageload ${g.page.https === false ? "http" : "https"}://${t}/`);
    } else if (g.xfer) {
      const t = target(state, g.xfer.to);
      if (t) add(from, `iperf3 ${t} -n 20`);
    } else if (g.lbspread) {
      const t = target(state, g.lbspread.to);
      if (t) add(from, `nc -zv ${t} ${g.lbspread.port}`);
    }
  }
  for (const d of Object.values(state.devices)) {
    add(d.id, "hostname");
    add(d.id, "ip addr");
    add(d.id, "ip route");
    add(d.id, "ip neigh");
    add(d.id, "ss -ltn");
    if (d.kind === "switch") {
      add(d.id, "show mac");
      add(d.id, "show ports");
    }
    if (d.forward || d.fw.rules.length || d.nat.length) {
      add(d.id, "iptables -L");
      add(d.id, "iptables -t nat -L");
      add(d.id, "sysctl net.ipv4.ip_forward");
    }
    if (d.dns) add(d.id, "dns show");
    if (d.http) add(d.id, "web show");
    if (d.tls) add(d.id, "tls show");
    if (d.trust || d.kind === "host") add(d.id, "trust show");
    if (d.ssh) add(d.id, "sshd show");
    if (d.ifaces.some((i) => i.tun)) add(d.id, "vpn show");
    if (d.lb) add(d.id, "lb show");
    if (d.rproxy) add(d.id, "rproxy show");
    if (d.proxy) add(d.id, "proxy show");
    if (d.kind === "host" || d.kind === "server") add(d.id, "cat /etc/hosts");
  }
  for (const f of froms) {
    if (state.devices[f]) {
      add(f, "tcpdump -i any -c 12");
      add(f, "arp -n");
    }
  }
  return cmds;
}

function runBattery(state, cmds) {
  const s = clone(state);
  return cmds.map(([dev, line]) => {
    const r = exec(s, dev, line);
    const tag = r.changed === undefined ? "u" : r.changed ? "t" : "f";
    return [dev, line, hash(`${tag}|${r.out}`), r.out];
  });
}


/* ---- «краевые» команды: общий шаблон, подставляются интерфейс и адреса устройства; ошибки, разборы, изменения ---- */
const EDGE = [
  "help", "?", "clear", "hostname", "ip", "ip addr show", "ip a", "ip addr add 10.99.0.1/24 dev {if}", "ip addr add bad dev {if}", "ip addr add 10.99.0.1/24 dev nope",
  "ip addr add 10.99.0.9/24 dev {if}", "ip addr", "ip link", "ip link set {if} down", "ip link set {if} up", "ip link set {if} mtu 1400", "ip link set {if} mtu 10", "ip link set {if} txqueuelen 50",
  "ip link set {if} txqueuelen 0", "ip link", "ip route", "ip route add 10.77.0.0/24 dev {if}", "ip route add 10.77.0.0/24 via 1.1.1.1", "ip route add 10.88.0.0/24 via {gw}", "ip route add default via {gw}",
  "ip route add bad via x", "ip route add 10.55.0.0/24", "ip route add 10.55.0.0/24 via", "ip route del 10.77.0.0/24", "ip route del 10.1.1.0/24", "ip route get 8.8.8.8", "ip route get {ip}", "ip route get x", "ip route", "ip neigh",
  "ping", "ping -c 1 999.1.1.1", "ping -c 2 -t 1 {ip}", "ping -c 1 -s 2000 -M do {ip}", "ping -c 1 {own}", "ping -c 3 -s 100 {ip}", "ping nohost.test", "ping -c 0 {ip}", "traceroute", "traceroute {ip}", "traceroute nohost.test", "tracepath {ip}",
  "curl", "curl x", "curl http://{ip}/", "curl -I http://{ip}/nope", "curl -v http://{ip}:8080/", "curl -X POST http://{ip}/", "curl https://{ip}/", "curl -L http://{ip}/", "curl -v -x {ip}:3128 http://{ip}/", "curl http://nohost.test/",
  "nc -zv {ip} 80", "nc -zv {ip} 22", "nc -u {ip} 53", "nc -u {ip} 9999", "nc -u x 1", "nc -l 8080", "nc -u -l 5000", "nc -l", "nc", "ss -ltn", "ss", "close tcp 8080", "close udp 5000", "close tcp 1", "close", "listen tcp 8080 127.0.0.1", "listen tcp 99 1.2.3.4", "listen tcp 80 0.0.0.0", "ss",
  "sysctl net.ipv4.ip_forward", "sysctl -w net.ipv4.ip_forward=1", "sysctl -w net.ipv4.ip_forward=0", "echo 1 > /proc/sys/net/ipv4/ip_forward", "sysctl net.ipv4.tcp_rmem", "sysctl -w net.ipv4.tcp_rmem=\"4096 87380 6291456\"", "sysctl -w net.ipv4.tcp_rmem=1000",
  "sysctl -w net.ipv4.tcp_rmem=4096,131072,262144", "sysctl net.ipv4.tcp_rmem = 4096", "sysctl net.ipv4.tcp_congestion_control", "sysctl -w net.ipv4.tcp_congestion_control=bbr", "sysctl -w net.ipv4.tcp_congestion_control=foo", "sysctl net.ipv4.tcp_syncookies",
  "sysctl -w net.ipv4.tcp_syncookies=1", "sysctl -w net.ipv4.tcp_syncookies=0", "sysctl foo", "sysctl", "echo hello world", "echo",
  "iptables -L", "iptables -S", "iptables -t nat -L", "iptables -t foo -L", "iptables -L FOO", "iptables -A FORWARD -p tcp --dport 80 -j DROP", "iptables -A FORWARD -s 10.0.0.0/8 -d any -j ACCEPT", "iptables -I FORWARD 1 -p udp -j REJECT",
  "iptables -I FORWARD -p icmp -j DROP", "iptables -A FORWARD --ctstate ESTABLISHED,RELATED -j ACCEPT", "iptables -A FORWARD -m conntrack --ctstate NEW -j ACCEPT", "iptables -A FORWARD -i {if} -o {if} --sport 5 -j ACCEPT", "iptables -L", "iptables -D FORWARD -p tcp --dport 80 -j DROP",
  "iptables -D FORWARD -p tcp --dport 81 -j DROP", "iptables -P FORWARD DROP", "iptables -P FORWARD ACCEPT", "iptables -P INPUT DROP", "iptables -P FORWARD REJECT", "iptables -A FORWARD -j FOO", "iptables -A FORWARD --bogus", "iptables -A INPUT -j DROP", "iptables -A FORWARD", "iptables",
  "iptables -t nat -A POSTROUTING -o {if} -j MASQUERADE", "iptables -t nat -A POSTROUTING -j DROP", "iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.99.0.5:80", "iptables -t nat -A PREROUTING -j DNAT",
  "iptables -t nat -A PREROUTING -j DNAT --to-destination bad", "iptables -t nat -I PREROUTING 1 -p tcp --dport 81 -j DNAT --to-destination 1.1.1.1", "iptables -t nat -I POSTROUTING 0 -s 10.0.0.0/8 -j MASQUERADE", "iptables -t nat -L", "iptables -t nat -D PREROUTING -p tcp --dport 81 -j DNAT --to-destination 1.1.1.1",
  "iptables -t nat -D PREROUTING -p tcp --dport 83 -j DNAT --to-destination 1.1.1.1", "iptables -t nat -A OUTPUT -j DROP", "iptables -t nat -P PREROUTING DROP", "iptables -t nat -F", "iptables -F", "sudo iptables -L", "sudo ip route", "sudo",
  "dns show", "dns enable", "dns recursive on", "dns recursive off", "dns root 1.2.3.4", "dns root bad", "dns zone example.test", "dns zone", "dns add a.example.test A 1.2.3.4", "dns add b.example.test CNAME a.example.test", "dns add c TXT hello", "dns add d A bad", "dns add", "dns add x MX 10",
  "dns del a.example.test A", "dns del zzz", "dns delegate sub.example.test 1.2.3.5", "dns delegate", "dns undelegate sub.example.test", "dns show", "dns foo",
  "dig", "dig www.example.org", "dig a.example.test A @{ip}", "dig foo.test @bad", "nslookup foo.test", "nslookup foo.test {ip}", "host foo.test",
  "web show", "web enable", "web route /a 200 hello world", "web route /b 404", "web route bad", "web route /c 99", "web redirect /r 301 /a", "web redirect /r2 200 /a", "web header /a X-Test yes", "web header /zz X y", "web header /a",
  "web protocol h2", "web protocol h9", "web etag /a abc", "web etag", "web show", "web del /a", "web show", "web foo",
  "tls show", "tls enable", "tls cert new a.test b.test --issuer PublicIntCA --days 30", "tls cert new --issuer Nope --days 5", "tls cert new a.test --issuer PublicIntCA", "tls cert new a.test --issuer PublicIntCA --days 0", "tls chain add PublicIntCA", "tls chain add Nope", "tls chain clear",
  "tls versions 1.2", "tls versions 9.9", "tls versions", "tls show", "tls foo", "trust show", "trust add CorpRootCA", "trust add Nope", "trust del PublicRootCA", "trust show", "trust foo",
  "proxy show", "proxy enable", "proxy deny a.test", "proxy allow a.test", "proxy deny", "proxy show", "lb show", "lb add 1.2.3.4:80", "lb add bad", "lb add 1.2.3.4", "lb algo hash", "lb algo foo", "lb health off", "lb del 1.2.3.4", "lb del 9.9.9.9", "lb show",
  "rproxy show", "rproxy enable", "rproxy add * /api 10.99.0.7:80", "rproxy add a.test /x 10.99.0.8", "rproxy add bad", "rproxy cache /api on", "rproxy cache /zz on", "rproxy show", "rproxy del /api",
  "ssh-keygen", "ssh-keygen -l", "ssh-keygen -R 10.0.0.1", "ssh", "ssh alice@1.2.3.4", "ssh alice@{ip}", "ssh -P pw alice@{ip}", "ssh-copy-id alice@{ip}", "sshd show", "sshd enable", "sshd user alice pw", "sshd user", "sshd authorize alice SHA256:x", "sshd authorize zed SHA256:x", "sshd password off", "sshd password maybe",
  "sshd hostkey", "sshd show", "sshd foo", "vpn show", "vpn add wg9 --peer 1.2.3.4 --address 10.9.0.1/30 --key k", "vpn add wg9 --peer 1.2.3.4 --address 10.9.0.1/30 --key k", "vpn add", "vpn add wg8 --peer 1.2.3.4 --address 10.9.0.1/30", "vpn show", "vpn del wg9",
  "arp -n", "arp -s 10.1.1.1 aa:bb:cc:dd:ee:ff", "arp -s bad x", "arp -d 10.1.1.1", "arp", "cat /etc/resolv.conf", "cat /etc/hosts", "cat /x", "cat", "echo \"nameserver 10.99.0.53\" > /etc/resolv.conf", "echo nameserver x > /etc/resolv.conf", "echo \"10.1.1.1 foo.test\" >> /etc/hosts",
  "echo '10.1.1.2 bar.test' > /etc/hosts", "echo bad > /etc/hosts", "cat /etc/hosts", "cat /etc/resolv.conf", "pageload", "pageload http://foo.test", "pageload https://{ip}/", "iperf3", "iperf3 {ip} -n 5", "iperf3 {ip}", "tcpdump", "tcpdump -i nope", "tcpdump -i any icmp", "tcpdump -i any host {ip} and port 80",
  "tcpdump -c 3", "tcpdump -i {if} -c 2 tcp", "show mac", "show ports", "show", "port {if} vlan 10", "port {if} trunk", "port {if} access", "port {if} down", "port {if} up", "port {if} vlan 5000", "port xx vlan 5", "port {if} vlan abc", "show ports",
  "openssl", "openssl s_client -connect {ip}:443", "openssl s_client -connect {ip}:80 -servername a.test", "openssl s_client -connect nohost.test:443", "unknowncmd", "ping -c 2 {ip}", "arp", "ip neigh",
];
const fnv32 = (s) => fnv(s, 0x811c9dc5);
// цели после каждого шага решения, кроме последнего (промежуточные состояния: частичные решения ученика)
function partialSummaries(start, ops, goals) {
  const out = [];
  const s = clone(start);
  for (let k = 0; k < ops.length - 1; k++) {
    applyOps(s, [ops[k]]);
    out.push(summarize(checkGoals(s, goals)));
  }
  return out;
}
function edgeRuns(state, dump = false, keep = null) {
  const s = clone(state);
  if (keep) keep.state = s;
  const runs = [];
  const devs = Object.values(state.devices);
  const picks = [];
  for (const kind of ["host", "server", "router", "switch", "hub", "internet"]) {
    const d = devs.find((x) => x.kind === kind);
    if (d && (kind !== "server" || picks.length < 3)) picks.push(d);
  }
  for (const d of picks.slice(0, 4)) {
    const other = devs.find((x) => x.id !== d.id && x.kind !== "switch" && x.kind !== "hub" && firstIp(x));
    const vars = { if: d.ifaces[0]?.name ?? "eth0", ip: other ? firstIp(other) : "10.0.0.1", own: firstIp(d) ?? "10.0.0.2", gw: d.ifaces.find((i) => i.ip)?.ip?.replace(/\.\d+$/, ".254") ?? "10.0.0.254" };
    let hashes = "";
    for (const t of EDGE) {
      const line = t.replace(/\{(\w+)\}/g, (_, k) => vars[k]);
      const r = exec(s, d.id, line);
      const tag = r.changed === undefined ? "u" : r.changed ? "t" : "f";
      hashes += fnv32(`${tag}|${r.out}`);
      if (dump) console.log(`${d.id}$ ${line}\n[${tag}] ${r.out}\n`);
    }
    runs.push({ dev: d.id, vars, hashes });
  }
  return runs;
}


/* ---- синтетические цели: варианты имеющихся (иные ожидания, пороги, ограничения) — шире покрывают проверку целей ---- */
function synthGoals(goals, state) {
  const out = [];
  const devs = Object.values(state.devices);
  const others = devs.filter((d) => d.kind !== "switch" && d.kind !== "hub").map((d) => d.id);
  const seen = {};
  let n = 0;
  const add = (kind, body, tag) => out.push({ id: `s${n++}`, text: `${kind} ${tag}`, [kind]: body });
  for (const g of goals) {
    const kind = ["ping", "tcp", "udp", "dns", "mtu", "lbspread", "ssh", "page", "http", "xfer"].find((k) => g[k]);
    seen[kind] = (seen[kind] ?? 0) + 1;
    if (seen[kind] > 2) continue;
    const x = g[kind];
    const v = (extra, tag) => add(kind, { ...x, ...extra }, tag);
    if (kind === "ping") {
      v({ expect: "fail" }, "fail");
      v({ maxRttMs: 0.0001 }, "rtt-");
      v({ maxRttMs: 100000 }, "rtt+");
      v({ size: 1400, df: true }, "1400df");
      v({ size: 2000, df: true }, "2000df");
      v({ size: 2000 }, "2000");
      v({ sizeFromMtu: true }, "mtu");
      v({ warm: true, noLoop: true }, "warm");
      v({ seenSrc: `@${x.from}` }, "seen");
      for (const o of others.filter((o) => o !== x.from).slice(0, 2)) {
        v({ via: o }, `via-${o}`);
        v({ avoid: o }, `avoid-${o}`);
        v({ notSeenBy: o }, `notseen-${o}`);
      }
    } else if (kind === "tcp") {
      v({ expect: "fail" }, "fail");
      v({ port: 22 }, "22");
      v({ port: 443, warm: true }, "443");
      v({ port: 80, noLoop: true }, "80");
    } else if (kind === "udp") {
      v({ expect: "fail" }, "fail");
      v({ port: 53 }, "53");
      v({ port: 9, maxRttMs: 0.0001 }, "rtt-");
    } else if (kind === "dns") {
      v({ expect: "NXDOMAIN" }, "nx");
      v({ expect: "ошибка" }, "err");
      v({ expect: "1.2.3.4" }, "wrong");
      v({ name: "nohost.test" }, "nohost");
    } else if (kind === "mtu") {
      v({ min: 9000 }, "min");
      v({ max: 100 }, "max");
      v({ iface: "eth1" }, "eth1");
      v({ iface: "nope", min: 1 }, "nope");
    } else if (kind === "ssh") {
      v({ expect: "fail" }, "fail");
      v({ auth: "password", pass: "x" }, "pw");
      v({ auth: "key" }, "key");
      v({ pass: "x", via: undefined }, "pass");
    } else if (kind === "http") {
      v({ status: 200 }, "200");
      v({ status: 404 }, "404");
      v({ header: { server: "nginx" } }, "hdr");
      v({ header: { "x-none": true } }, "hdr-none");
      v({ noHeader: ["server"] }, "nohdr");
      v({ bodyIncludes: "zzz" }, "body");
      v({ maxRttMs: 0.01 }, "rtt");
      v({ hops: 1 }, "hops1");
      v({ hops: 3 }, "hops3");
      v({ finalUrl: "/x" }, "final");
      v({ nth: 0 }, "nth0");
      v({ repeat: 2 }, "rep2");
      v({ fail: true }, "fail");
      v({ follow: !x.follow }, "follow");
      v({ method: "HEAD" }, "head");
    } else if (kind === "xfer") {
      v({ minMbps: 1e9 }, "min");
      v({ maxLoadedRttMs: 0.001 }, "rtt");
      v({ mb: 5 }, "5mb");
    } else if (kind === "page") {
      v({ maxS: 0.001 }, "fast");
      v({ https: false }, "http");
    } else if (kind === "lbspread") {
      v({ distinct: 99 }, "distinct");
      v({ sticky: true }, "sticky");
      v({ n: 3 }, "n3");
    }
  }
  return out;
}

/* ---- разворачиваем решения ---- */
function expand(s) {
  const st = s.build();
  const start = clone(st);
  const ops = typeof s.solution === "function" ? s.solution(st) : s.solution;
  return { start, ops };
}

const scenarios = [];
const golden = {};
let n = 0;
for (const [ch, list] of Object.entries(NET_CHAPTERS)) {
  for (const s of list) {
    const { start, ops } = expand(s);
    if (Object.keys(start.devices).some((k) => /^\d+$/.test(k))) throw new Error(`${s.id}: числовой id устройства нарушит порядок ключей`);
    const startRes = checkGoals(clone(start), s.goals);
    const solved = applyOps(clone(start), ops);
    const solvedRes = checkGoals(solved, s.goals);
    const sb = battery(start, s.goals);
    const solvedStrip = strip(solved);
    const cb = battery(solvedStrip, s.goals);
    const outStart = runBattery(start, sb);
    const outSolved = runBattery(solvedStrip, cb);
    if (args.includes("--edge") && args[args.indexOf("--edge") + 1] === s.id) {
      edgeRuns(start, true);
      process.exit(0);
    }
    if (showIdx >= 0 && args[showIdx + 1] === s.id) {
      const which = args[showIdx + 2] === "solved" ? outSolved : outStart;
      for (const [dev, line, , out] of which) console.log(`# ${dev}$ ${line}\n${out}\n`);
      process.exit(0);
    }
    // решённая сеть: только изменившиеся устройства и все кабели
    const keepEdge = {};
    const changed = Object.values(solvedStrip.devices).filter((d) => JSON.stringify(d) !== JSON.stringify(start.devices[d.id]));
    scenarios.push({ chapter: Number(ch), id: s.id, title: s.title, statement: s.statement, hint: s.hint, tools: s.tools, start, goals: s.goals, solution: ops });
    golden[s.id] = {
      chapter: Number(ch),
      start: summarize(startRes),
      solved: summarize(solvedRes),
      solved_changed: changed,
      solved_links: solvedStrip.links,
      edge: edgeRuns(start, false, keepEdge),
      edge_goals: summarize(checkGoals(keepEdge.state, s.goals)),
      partial: partialSummaries(start, ops, s.goals),
      synth: (() => {
        const sg = synthGoals(s.goals, start);
        return { goals: sg, start: summarize(checkGoals(clone(start), sg)), solved: summarize(checkGoals(solvedStrip, sg)) };
      })(),
      cmds_start: outStart.map(([d, l, h]) => [d, l, h]),
      cmds_solved: outSolved.map(([d, l, h]) => [d, l, h]),
    };
    n++;
  }
}
if (showIdx >= 0 || args.includes("--edge")) {
  console.error("упражнение не найдено");
  process.exit(1);
}
const outDir = path.resolve(args[0] || "net-export");
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "scenarios.json"), JSON.stringify({ scenarios }));
fs.writeFileSync(path.join(outDir, "golden.json"), JSON.stringify({ version: 1, edge_template: EDGE, scenarios: golden }));
console.log(`упражнений ${n} → ${outDir}`);
fs.rmSync(tmp, { recursive: true, force: true });
