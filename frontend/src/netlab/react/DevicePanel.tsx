import { useState } from "react";
import {
  addRoute,
  clearAddr,
  delRoute,
  getGateway,
  setAddr,
  setGateway,
  setUp,
} from "../term.ts";
import { routeTable } from "../sim.ts";
import { fqdn } from "../dns.ts";
import { ipStr, netStr, parseIp } from "../ip.ts";
import Terminal from "./Terminal.tsx";

/* Карточка устройства: вкладка «Настройки» (формы) и «Терминал». Формы и терминал меняют
   сеть через одни и те же функции, так что результат одинаковый. */

function Field({ label, children, error }) {
  return (
    <label className="nl-field">
      <span>{label}</span>
      {children}
      {error && <em>{error}</em>}
    </label>
  );
}

function IfaceRow({ d, i, apply, readOnly, tools }) {
  const [ip, setIp] = useState(i.ip ?? "");
  const [prefix, setPrefix] = useState(String(i.prefix));
  const [err, setErr] = useState("");
  const commit = () => {
    if (readOnly) return;
    setErr("");
    if (!ip.trim()) {
      if (i.ip !== null) apply((n) => clearAddr(n.devices[d.id], i.name));
      return;
    }
    const e = apply((n) => {
      const dev = n.devices[d.id];
      const cur = dev.ifaces.find((x) => x.name === i.name);
      const old = { ip: cur.ip, prefix: cur.prefix };
      clearAddr(dev, i.name);
      const er = setAddr(dev, i.name, `${ip.trim()}/${prefix}`);
      if (er && old.ip) setAddr(dev, i.name, `${old.ip}/${old.prefix}`);
      return er;
    });
    if (e) setErr(e);
  };
  return (
    <div className="nl-iface">
      <div className="nl-iface-name">
        <b>{i.name}</b>
        <small>{i.mac}</small>
      </div>
      <input
        value={ip}
        onChange={(e) => setIp(e.target.value)}
        onBlur={commit}
        onKeyDown={(e) => e.key === "Enter" && commit()}
        placeholder="IP-адрес"
        disabled={readOnly}
        aria-label={`IP ${i.name}`}
        spellCheck={false}
      />
      <span className="nl-slash">/</span>
      <input
        className="nl-prefix"
        value={prefix}
        onChange={(e) => setPrefix(e.target.value.replace(/\D/g, "").slice(0, 2))}
        onBlur={commit}
        onKeyDown={(e) => e.key === "Enter" && commit()}
        disabled={readOnly}
        aria-label={`Маска ${i.name}`}
      />
      <label className="nl-up">
        <input
          type="checkbox"
          checked={i.up}
          disabled={readOnly}
          onChange={(e) => apply((n) => setUp(n.devices[d.id], i.name, e.target.checked))}
        />
        вкл
      </label>
      {tools?.queue && (
        <label className="nl-up">
          очередь
          <input
            className="nl-prefix wide"
            defaultValue={String(i.txqueuelen ?? 1000)}
            disabled={readOnly}
            aria-label={`Очередь ${i.name}`}
            onBlur={(e) => {
              const v = Number(e.target.value);
              if (v >= 1 && v <= 10000) apply((n) => void (n.devices[d.id].ifaces.find((x) => x.name === i.name).txqueuelen = v));
            }}
          />
          пакетов
        </label>
      )}
      {err && <em className="nl-err">{err}</em>}
    </div>
  );
}

function Routes({ d, apply, readOnly }) {
  const [dst, setDst] = useState("");
  const [via, setVia] = useState("");
  const [err, setErr] = useState("");
  const rows = routeTable(d);
  const add = () => {
    setErr("");
    const e = apply((n) => addRoute(n.devices[d.id], dst.trim() || "default", via.trim() || null, null));
    if (e) setErr(e);
    else (setDst(""), setVia(""));
  };
  return (
    <div className="nl-sec">
      <h4>Таблица маршрутов</h4>
      <table className="nl-table">
        <tbody>
          {rows.map((r, k) => (
            <tr key={k}>
              <td>{r.prefix === 0 ? "default" : netStr(r.net, r.prefix)}</td>
              <td>{r.via ? `via ${ipStr(r.via)}` : "напрямую"}</td>
              <td>{r.dev}</td>
              <td>
                {!r.connected && !readOnly && (
                  <button
                    type="button"
                    className="nl-x"
                    aria-label="Удалить маршрут"
                    onClick={() => apply((n) => delRoute(n.devices[d.id], r.prefix === 0 ? "default" : netStr(r.net, r.prefix)))}
                  >
                    ×
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {!readOnly && (
        <div className="nl-add">
          <input value={dst} onChange={(e) => setDst(e.target.value)} placeholder="сеть 10.0.0.0/24 или default" spellCheck={false} />
          <input value={via} onChange={(e) => setVia(e.target.value)} placeholder="через шлюз 10.0.1.1" spellCheck={false} />
          <button type="button" className="quiz-btn ghost" onClick={add}>
            + маршрут
          </button>
        </div>
      )}
      {err && <em className="nl-err">{err}</em>}
    </div>
  );
}

function Nat({ d, apply, readOnly, exec }) {
  const [out, setOut] = useState(d.ifaces[d.ifaces.length - 1]?.name ?? "");
  const [proto, setProto] = useState("tcp");
  const [port, setPort] = useState("");
  const [to, setTo] = useState("");
  const [inn, setInn] = useState(d.ifaces[d.ifaces.length - 1]?.name ?? "");
  const [msg, setMsg] = useState("");
  const masq = d.nat.find((n) => n.action === "MASQUERADE");
  return (
    <div className="nl-sec">
      <h4>NAT</h4>
      <div className="nl-add">
        <span className="nl-lbl">MASQUERADE на интерфейсе</span>
        <select value={out} onChange={(e) => setOut(e.target.value)} disabled={readOnly}>
          {d.ifaces.map((i) => (
            <option key={i.name}>{i.name}</option>
          ))}
        </select>
        <button
          type="button"
          className="quiz-btn ghost"
          disabled={readOnly}
          onClick={() => setMsg(exec(masq ? `iptables -t nat -D POSTROUTING -o ${masq.out} -j MASQUERADE` : `iptables -t nat -A POSTROUTING -o ${out} -j MASQUERADE`))}
        >
          {masq ? `выключить (сейчас ${masq.out})` : "включить"}
        </button>
      </div>
      <div className="nl-add">
        <span className="nl-lbl">Проброс порта: вход</span>
        <select value={inn} onChange={(e) => setInn(e.target.value)} disabled={readOnly}>
          {d.ifaces.map((i) => (
            <option key={i.name}>{i.name}</option>
          ))}
        </select>
        <select value={proto} onChange={(e) => setProto(e.target.value)} disabled={readOnly}>
          <option>tcp</option>
        </select>
        <input value={port} onChange={(e) => setPort(e.target.value.replace(/\D/g, ""))} placeholder="порт" className="nl-prefix wide" disabled={readOnly} />
        <input value={to} onChange={(e) => setTo(e.target.value)} placeholder="на 192.168.0.10:8080" disabled={readOnly} spellCheck={false} />
        <button
          type="button"
          className="quiz-btn ghost"
          disabled={readOnly}
          onClick={() => setMsg(exec(`iptables -t nat -A PREROUTING -i ${inn} -p ${proto} --dport ${port} -j DNAT --to-destination ${to}`))}
        >
          + проброс
        </button>
      </div>
      <ul className="nl-rules">
        {d.nat.map((n, k: Key|null|undefined) => (
          <li key={k}>
            <code>
              {n.chain}: {n.action} {n.out ? `-o ${n.out}` : ""} {n.in ? `-i ${n.in}` : ""} {n.dport ? `порт ${n.dport}` : ""} {n.to ? `→ ${n.to}` : ""}
            </code>
            {!readOnly && (
              <button type="button" className="nl-x" aria-label="Удалить правило" onClick={() => apply((s) => void s.devices[d.id].nat.splice(k, 1))}>
                ×
              </button>
            )}
          </li>
        ))}
        {d.nat.length === 0 && <li className="nl-none">правил NAT нет</li>}
      </ul>
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function Firewall({ d, apply, readOnly, exec }) {
  const [action, setAction] = useState("ACCEPT");
  const [src, setSrc] = useState("");
  const [dst, setDst] = useState("");
  const [proto, setProto] = useState("");
  const [port, setPort] = useState("");
  const [state, setState] = useState("");
  const [msg, setMsg] = useState("");
  const add = () => {
    const p = [];
    if (proto) p.push(`-p ${proto}`);
    if (src) p.push(`-s ${src}`);
    if (dst) p.push(`-d ${dst}`);
    if (port) p.push(`--dport ${port}`);
    if (state) p.push(`-m conntrack --ctstate ${state}`);
    setMsg(exec(`iptables -A FORWARD ${p.join(" ")} -j ${action}`));
  };
  return (
    <div className="nl-sec">
      <h4>Файрвол (цепочка FORWARD)</h4>
      <div className="nl-add">
        <span className="nl-lbl">Политика по умолчанию</span>
        <select value={d.fw.policy} disabled={readOnly} onChange={(e) => setMsg(exec(`iptables -P FORWARD ${e.target.value}`))}>
          <option>ACCEPT</option>
          <option>DROP</option>
        </select>
      </div>
      <div className="nl-add wrap">
        <select value={action} onChange={(e) => setAction(e.target.value)} disabled={readOnly}>
          <option>ACCEPT</option>
          <option>DROP</option>
          <option>REJECT</option>
        </select>
        <select value={proto} onChange={(e) => setProto(e.target.value)} disabled={readOnly}>
          <option value="">любой протокол</option>
          <option>tcp</option>
          <option>icmp</option>
        </select>
        <input value={src} onChange={(e) => setSrc(e.target.value)} placeholder="откуда 192.168.0.0/24" disabled={readOnly} spellCheck={false} />
        <input value={dst} onChange={(e) => setDst(e.target.value)} placeholder="куда" disabled={readOnly} spellCheck={false} />
        <input value={port} onChange={(e) => setPort(e.target.value.replace(/\D/g, ""))} placeholder="порт" className="nl-prefix wide" disabled={readOnly} />
        <select value={state} onChange={(e) => setState(e.target.value)} disabled={readOnly}>
          <option value="">любое состояние</option>
          <option value="NEW">новое соединение</option>
          <option value="ESTABLISHED,RELATED">уже установлено</option>
        </select>
        <button type="button" className="quiz-btn ghost" onClick={add} disabled={readOnly}>
          + правило
        </button>
      </div>
      <ol className="nl-rules">
        {d.fw.rules.map((r, k: Key|null|undefined) => (
          <li key={k}>
            <code>
              {r.action} {r.proto ?? ""} {r.src ? `от ${r.src}` : ""} {r.dst ? `к ${r.dst}` : ""} {r.dport ? `порт ${r.dport}` : ""} {r.state ? (r.state === "established" ? "(установленные)" : "(новые)") : ""}
            </code>
            {!readOnly && (
              <button type="button" className="nl-x" aria-label="Удалить правило" onClick={() => apply((s) => void s.devices[d.id].fw.rules.splice(k, 1))}>
                ×
              </button>
            )}
          </li>
        ))}
        {d.fw.rules.length === 0 && <li className="nl-none">правил нет — работает политика «{d.fw.policy}»</li>}
      </ol>
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function Services({ d, apply, readOnly }) {
  const [port, setPort] = useState("");
  const [proto, setProto] = useState("tcp");
  return (
    <div className="nl-sec">
      <h4>Слушающие порты</h4>
      <ul className="nl-rules">
        {d.services.map((s, k: Key|null|undefined) => (
          <li key={k}>
            <code>{s.proto}/{s.port}{s.bind && s.bind !== "0.0.0.0" ? ` (только ${s.bind})` : ""}</code>
            {!readOnly && s.bind && s.bind !== "0.0.0.0" && (
              <button type="button" className="quiz-btn ghost" onClick={() => apply((n) => void (n.devices[d.id].services[k].bind = "0.0.0.0"))}>
                слушать везде
              </button>
            )}
            {!readOnly && (
              <button type="button" className="nl-x" aria-label="Закрыть порт" onClick={() => apply((n) => void n.devices[d.id].services.splice(k, 1))}>
                ×
              </button>
            )}
          </li>
        ))}
        {d.services.length === 0 && <li className="nl-none">ни один порт не слушает</li>}
      </ul>
      {!readOnly && (
        <div className="nl-add">
          <select value={proto} onChange={(e) => setProto(e.target.value)} aria-label="Протокол">
            <option>tcp</option>
            <option>udp</option>
          </select>
          <input value={port} onChange={(e) => setPort(e.target.value.replace(/\D/g, ""))} placeholder="порт" className="nl-prefix wide" />
          <button
            type="button"
            className="quiz-btn ghost"
            onClick={() => {
              if (!port) return;
              apply((n) => void n.devices[d.id].services.push({ proto, port: Number(port) }));
              setPort("");
            }}
          >
            + слушать порт
          </button>
        </div>
      )}
    </div>
  );
}

export default function DevicePanel({ state, devId, tools, apply, exec, lines, onRun }) {
  const [tab, setTab] = useState("cfg");
  const d = state.devices[devId];
  if (!d) return null;
  const readOnly = d.locked;
  const isHost = d.kind === "host" || d.kind === "server";
  const isRouter = d.kind === "router" || d.kind === "internet";
  const macs = state.rt?.mac?.[d.id] ?? {};

  return (
    <div className="nl-panel">
      <div className="nl-panel-head">
        <h4>{d.name}</h4>
        <span className="nl-kind">
          {{ host: "компьютер", server: "сервер", router: "маршрутизатор", switch: "коммутатор", hub: "хаб (повторитель)", internet: "интернет (провайдер)" }[d.kind]}
        </span>
        {readOnly && <span className="nl-lock">только чтение</span>}
      </div>
      <div className="nl-tabs">
        <button type="button" className={tab === "cfg" ? "on" : ""} onClick={() => setTab("cfg")}>
          Настройки
        </button>
        <button type="button" className={tab === "term" ? "on" : ""} onClick={() => setTab("term")}>
          Терминал
        </button>
      </div>

      {tab === "cfg" ? (
        <div className="nl-cfg">
          {d.kind !== "switch" && (
            <div className="nl-sec">
              <h4>Интерфейсы</h4>
              {d.ifaces.map((i: unknown) => (
                <IfaceRow key={`${d.id}${i.name}${i.ip}${i.prefix}`} d={d} i={i} apply={apply} readOnly={readOnly} tools={tools} />
              ))}
            </div>
          )}
          {isHost && (
            <GatewayField d={d} apply={apply} readOnly={readOnly} />
          )}
          {isHost && tools.tcp && <TcpTune d={d} apply={apply} readOnly={readOnly} />}
          {isHost && tools.dns && <Resolver d={d} apply={apply} readOnly={readOnly} />}
          {d.tls && tools.tls && <TlsServer d={d} apply={apply} readOnly={readOnly} exec={exec} cas={Object.keys(state.pki?.cas ?? {})} />}
          {isHost && tools.tls && <TrustStore d={d} apply={apply} readOnly={readOnly} cas={Object.keys(state.pki?.cas ?? {})} />}
          {tools.ssh && d.kind !== "switch" && (d.ssh || isHost) && <SshBox d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {tools.vpn && (isRouter || isHost) && <VpnBox d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.lb && tools.lb && <LbBox d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.rproxy && tools.rproxy && <RproxyBox d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.proxy && tools.proxy && <ProxyBox d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.http && tools.http && <WebServer d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.dns && tools.dns && <DnsServer d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {isRouter && (
            <div className="nl-sec">
              <label className="nl-up">
                <input
                  type="checkbox"
                  checked={d.forward}
                  disabled={readOnly}
                  onChange={(e) => apply((n) => void (n.devices[d.id].forward = e.target.checked))}
                />
                пересылать пакеты между интерфейсами (ip_forward)
              </label>
            </div>
          )}
          {(isRouter || (isHost && tools.routes)) && <Routes d={d} apply={apply} readOnly={readOnly} />}
          {isRouter && tools.nat && <Nat d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {isRouter && tools.fw && <Firewall d={d} apply={apply} readOnly={readOnly} exec={exec} />}
          {d.kind === "server" && <Services d={d} apply={apply} readOnly={readOnly} />}
          {d.kind === "switch" && (
            <div className="nl-sec">
              <h4>Порты</h4>
              <table className="nl-table">
                <tbody>
                  {d.ifaces.map((i) => (
                    <tr key={i.name}>
                      <td>{i.name}</td>
                      <td>
                        <label className={`nl-up ${i.up ? "" : "off"}`}>
                          <input
                            type="checkbox"
                            checked={i.up}
                            disabled={readOnly}
                            onChange={(e) => apply((n) => setUp(n.devices[d.id], i.name, e.target.checked))}
                          />
                          вкл
                        </label>
                      </td>
                      <td>
                        <label className="nl-up">
                          VLAN
                          <input
                            className="nl-prefix"
                            value={i.trunk ? "" : String(i.vlan ?? 1)}
                            disabled={readOnly || i.trunk}
                            aria-label={`VLAN ${i.name}`}
                            onChange={(e) => {
                              const v = Number(e.target.value.replace(/\D/g, "").slice(0, 4));
                              if (v >= 1) apply((n) => void (n.devices[d.id].ifaces.find((x) => x.name === i.name).vlan = v));
                            }}
                          />
                        </label>
                      </td>
                      <td>
                        <label className="nl-up">
                          <input
                            type="checkbox"
                            checked={!!i.trunk}
                            disabled={readOnly}
                            onChange={(e) => apply((n) => void (n.devices[d.id].ifaces.find((x) => x.name === i.name).trunk = e.target.checked))}
                          />
                          trunk
                        </label>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {d.kind === "switch" && (
            <div className="nl-sec">
              <h4>Таблица MAC-адресов</h4>
              <table className="nl-table">
                <tbody>
                  {Object.entries(macs).map(([m, p]) => (
                    <tr key={m}>
                      <td>{m}</td>
                      <td>{p}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {Object.keys(macs).length === 0 && <p className="nl-none">Пока пусто: коммутатор учится на проходящих кадрах. Запустите ping между компьютерами.</p>}
            </div>
          )}
        </div>
      ) : (
        <Terminal device={d} lines={lines} onRun={onRun} />
      )}
    </div>
  );
}

function WebServer({ d, apply, readOnly, exec }) {
  const [path, setPath] = useState("");
  const [status, setStatus] = useState("200");
  const [extra, setExtra] = useState("");
  const [hp, setHp] = useState("");
  const [hn, setHn] = useState("");
  const [hv, setHv] = useState("");
  const [msg, setMsg] = useState("");
  return (
    <div className="nl-sec">
      <h4>Веб-сервер (HTTP, порт 80)</h4>
      {d.http.page && (
        <div className="nl-add">
          <span className="nl-lbl">протокол</span>
          <select value={d.http.protocol ?? "h1"} disabled={readOnly} onChange={(e) => apply((s) => void (s.devices[d.id].http.protocol = e.target.value))}>
            <option value="h1">HTTP/1.1</option>
            <option value="h2">HTTP/2</option>
            <option value="h3">HTTP/3</option>
          </select>
          <span className="nl-lbl">страница: {d.http.page.count + 1} ресурсов по ~{d.http.page.kb} КБ</span>
        </div>
      )}
      <table className="nl-table">
        <tbody>
          {d.http.routes.map((r, k: Key|null|undefined) => (
            <tr key={k}>
              <td>{r.path}</td>
              <td>{r.status ?? 200}</td>
              <td>
                {r.location ? `→ ${r.location}` : ""}
                {r.headers ? Object.entries(r.headers).map(([n, v]) => ` ${n}: ${v}`).join(";") : ""}
              </td>
              <td>{!readOnly && <button type="button" className="nl-x" aria-label="Удалить маршрут" onClick={() => apply((s) => void s.devices[d.id].http.routes.splice(k, 1))}>×</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {!readOnly && (
        <>
          <div className="nl-add">
            <input value={path} onChange={(e) => setPath(e.target.value)} placeholder="/путь" spellCheck={false} />
            <input className="nl-prefix wide" value={status} onChange={(e) => setStatus(e.target.value.replace(/\D/g, "").slice(0, 3))} aria-label="Код ответа" />
            <input value={extra} onChange={(e) => setExtra(e.target.value)} placeholder="текст или /куда (для 30x)" spellCheck={false} />
            <button
              type="button"
              className="quiz-btn ghost"
              onClick={() => {
                const st = Number(status);
                setMsg(exec([301, 302, 307, 308].includes(st) ? `web redirect ${path} ${st} ${extra}` : `web route ${path} ${st} ${extra}`));
              }}
            >
              + маршрут
            </button>
          </div>
          <div className="nl-add">
            <input value={hp} onChange={(e) => setHp(e.target.value)} placeholder="для пути /logo.png" spellCheck={false} />
            <input value={hn} onChange={(e) => setHn(e.target.value)} placeholder="заголовок Cache-Control" spellCheck={false} />
            <input value={hv} onChange={(e) => setHv(e.target.value)} placeholder="значение max-age=3600" spellCheck={false} />
            <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec(`web header ${hp} ${hn} ${hv}`))}>
              + заголовок
            </button>
          </div>
        </>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function TlsServer({ d, apply, readOnly, exec, cas }) {
  const [cn, setCn] = useState("");
  const [issuer, setIssuer] = useState("PublicIntCA");
  const [days, setDays] = useState("90");
  const [chain, setChain] = useState("PublicIntCA");
  const [msg, setMsg] = useState("");
  const t = d.tls;
  return (
    <div className="nl-sec">
      <h4>TLS-сертификат</h4>
      <p className="nl-none">
        CN={t.cert.cn} · SAN: {t.cert.san.join(", ")}
        <br />
        издатель {t.cert.issuer} · до {t.cert.notAfter}
        <br />
        цепочка: {t.chain.length ? t.chain.join(" → ") : "(только свой сертификат)"} · версии TLS {t.versions.join(", ")}
      </p>
      {!readOnly && (
        <>
          <div className="nl-add">
            <input value={cn} onChange={(e) => setCn(e.target.value)} placeholder="имена через пробел: example.org www.example.org" spellCheck={false} />
            <select value={issuer} onChange={(e) => setIssuer(e.target.value)}>
              {cas.map((c: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined) => <option key={c}>{c}</option>)}
            </select>
            <input className="nl-prefix wide" value={days} onChange={(e) => setDays(e.target.value.replace(/\D/g, ""))} aria-label="Дней" />
            <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec(`tls cert new ${cn} --issuer ${issuer} --days ${days}`))}>
              выпустить
            </button>
          </div>
          <div className="nl-add">
            <span className="nl-lbl">в цепочку:</span>
            <select value={chain} onChange={(e) => setChain(e.target.value)}>
              {cas.map((c: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined) => <option key={c}>{c}</option>)}
            </select>
            <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec(`tls chain add ${chain}`))}>+ добавить</button>
            <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec("tls chain clear"))}>очистить</button>
          </div>
          <div className="nl-add">
            <span className="nl-lbl">версии:</span>
            {["1.0", "1.1", "1.2", "1.3"].map((v) => (
              <label key={v} className="nl-up">
                <input
                  type="checkbox"
                  checked={t.versions.includes(v)}
                  onChange={(e) => apply((s) => void (s.devices[d.id].tls.versions = ["1.0", "1.1", "1.2", "1.3"].filter((x) => (x === v ? e.target.checked : s.devices[d.id].tls.versions.includes(x)))))}
                />
                {v}
              </label>
            ))}
          </div>
        </>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function TrustStore({ d, apply, readOnly, cas }) {
  const trust = d.trust ?? ["PublicRootCA"];
  const [pick, setPick] = useState(cas.find((c: any) => !trust.includes(c)) ?? cas[0]);
  return (
    <div className="nl-sec">
      <h4>Хранилище доверия (корневые CA)</h4>
      <ul className="nl-rules">
        {trust.map((c: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined) => (
          <li key={c}>
            <code>{c}</code>
            {!readOnly && <button type="button" className="nl-x" aria-label="Убрать" onClick={() => apply((s) => void (s.devices[d.id].trust = trust.filter((x: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined) => x !== c)))}>×</button>}
          </li>
        ))}
      </ul>
      {!readOnly && (
        <div className="nl-add">
          <select value={pick} onChange={(e) => setPick(e.target.value)}>
            {cas.map((c: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined) => <option key={c}>{c}</option>)}
          </select>
          <button type="button" className="quiz-btn ghost" onClick={() => apply((s) => void (s.devices[d.id].trust = [...new Set([...trust, pick])]))}>
            + доверять
          </button>
        </div>
      )}
    </div>
  );
}

function ProxyBox({ d, apply, readOnly, exec }) {
  const [host, setHost] = useState("");
  const [msg, setMsg] = useState("");
  return (
    <div className="nl-sec">
      <h4>HTTP-прокси (tcp/{d.proxy.port})</h4>
      <ul className="nl-rules">
        {d.proxy.deny.map((h: boolean|Key|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|Promise<string|number|bigint|boolean|ReactPortal|ReactElement<unknown,string|JSXElementConstructor<any>>|Iterable<ReactNode>|null|undefined>|null|undefined, k: any) => (
          <li key={h}>
            <code>запрещён: {h}</code>
            {!readOnly && <button type="button" className="nl-x" aria-label="Разрешить" onClick={() => apply((s) => void s.devices[d.id].proxy.deny.splice(k, 1))}>×</button>}
          </li>
        ))}
        {d.proxy.deny.length === 0 && <li className="nl-none">запретов нет</li>}
      </ul>
      {!readOnly && (
        <div className="nl-add">
          <input value={host} onChange={(e) => setHost(e.target.value)} placeholder="хост для запрета: social.example" spellCheck={false} />
          <button type="button" className="quiz-btn ghost" onClick={() => { setMsg(exec(`proxy deny ${host}`)); setHost(""); }}>
            + запретить
          </button>
        </div>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function LbBox({ d, apply, readOnly, exec }) {
  const [addr, setAddr] = useState("");
  const [msg, setMsg] = useState("");
  const lb = d.lb;
  return (
    <div className="nl-sec">
      <h4>Балансировщик {lb.vip}:{lb.port}</h4>
      <div className="nl-add">
        <span className="nl-lbl">алгоритм</span>
        <select value={lb.algo} disabled={readOnly} onChange={(e) => apply((s) => void (s.devices[d.id].lb.algo = e.target.value))}>
          <option value="rr">по кругу</option>
          <option value="hash">привязка по адресу клиента</option>
        </select>
        <label className="nl-up">
          <input type="checkbox" checked={!!lb.health} disabled={readOnly} onChange={(e) => apply((s) => void (s.devices[d.id].lb.health = e.target.checked))} />
          проверка здоровья
        </label>
      </div>
      <ul className="nl-rules">
        {lb.backends.map((b, k: any) => (
          <li key={b.ip + b.port}>
            <code>{b.ip}:{b.port}</code>
            {!readOnly && <button type="button" className="nl-x" aria-label="Убрать из пула" onClick={() => apply((s) => void s.devices[d.id].lb.backends.splice(k, 1))}>×</button>}
          </li>
        ))}
      </ul>
      {!readOnly && (
        <div className="nl-add">
          <input value={addr} onChange={(e) => setAddr(e.target.value)} placeholder="сервер для пула 10.0.1.12:80" spellCheck={false} />
          <button type="button" className="quiz-btn ghost" onClick={() => { setMsg(exec(`lb add ${addr}`)); setAddr(""); }}>+ в пул</button>
        </div>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function RproxyBox({ d, apply, readOnly, exec }) {
  const [host, setHost] = useState("*");
  const [path, setPath] = useState("");
  const [be, setBe] = useState("");
  const [msg, setMsg] = useState("");
  return (
    <div className="nl-sec">
      <h4>Обратный прокси / кэш</h4>
      <table className="nl-table">
        <tbody>
          {d.rproxy.rules.map((r, k: Key|null|undefined) => (
            <tr key={k}>
              <td>{r.host ?? "*"}{r.path}</td>
              <td>→ {r.backend}</td>
              <td>
                <label className="nl-up">
                  <input type="checkbox" checked={!!r.cache} disabled={readOnly} onChange={(e) => apply((s) => void (s.devices[d.id].rproxy.rules[k].cache = e.target.checked))} />
                  кэш
                </label>
              </td>
              <td>{!readOnly && <button type="button" className="nl-x" aria-label="Удалить правило" onClick={() => apply((s) => void s.devices[d.id].rproxy.rules.splice(k, 1))}>×</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {!readOnly && (
        <div className="nl-add">
          <input className="nl-prefix wide" value={host} onChange={(e) => setHost(e.target.value)} aria-label="Хост" />
          <input value={path} onChange={(e) => setPath(e.target.value)} placeholder="/путь" spellCheck={false} />
          <input value={be} onChange={(e) => setBe(e.target.value)} placeholder="сервер 10.0.2.10:8080" spellCheck={false} />
          <button type="button" className="quiz-btn ghost" onClick={() => { setMsg(exec(`rproxy add ${host || "*"} ${path} ${be}`)); setPath(""); setBe(""); }}>+ правило</button>
        </div>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function SshBox({ d, apply, readOnly, exec }) {
  const [msg, setMsg] = useState("");
  return (
    <div className="nl-sec">
      <h4>SSH {d.ssh ? "сервер" : "клиент"}</h4>
      {d.ssh && (
        <>
          <p className="nl-none">ключ хоста: {d.ssh.hostKey}</p>
          <label className="nl-up">
            <input type="checkbox" checked={d.ssh.passwordAuth} disabled={readOnly} onChange={(e) => apply((s) => void (s.devices[d.id].ssh.passwordAuth = e.target.checked))} />
            разрешить вход по паролю
          </label>
          <ul className="nl-rules">
            {Object.entries(d.ssh.users).map(([u, v]) => (
              <li key={u}>
                <code>{u}: {v.keys.length ? v.keys.join(", ") : "ключей нет"}</code>
              </li>
            ))}
          </ul>
        </>
      )}
      <div className="nl-add">
        <span className="nl-lbl">отпечаток вашего ключа: {d.sshKey ?? "ключа нет"}</span>
        {!d.ssh && !readOnly && (
          <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec("ssh-keygen"))}>создать ключ</button>
        )}
      </div>
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function VpnBox({ d, apply, readOnly, exec }) {
  const [name, setName] = useState("wg0");
  const [peer, setPeer] = useState("");
  const [addr, setAddr] = useState("");
  const [key, setKey] = useState("");
  const [msg, setMsg] = useState("");
  const tuns = d.ifaces.filter((i) => i.tun);
  return (
    <div className="nl-sec">
      <h4>VPN-туннели</h4>
      <ul className="nl-rules">
        {tuns.map((i) => (
          <li key={i.name}>
            <code>{i.name}: {i.ip}/{i.prefix} ↔ {i.tun.peer}</code>
            {!readOnly && <button type="button" className="nl-x" aria-label="Удалить туннель" onClick={() => setMsg(exec(`vpn del ${i.name}`))}>×</button>}
          </li>
        ))}
        {tuns.length === 0 && <li className="nl-none">туннелей нет</li>}
      </ul>
      {!readOnly && (
        <div className="nl-add wrap">
          <input className="nl-prefix wide" value={name} onChange={(e) => setName(e.target.value)} aria-label="Имя" />
          <input value={peer} onChange={(e) => setPeer(e.target.value)} placeholder="внешний IP пира" spellCheck={false} />
          <input value={addr} onChange={(e) => setAddr(e.target.value)} placeholder="адрес 10.9.0.1/30" spellCheck={false} />
          <input value={key} onChange={(e) => setKey(e.target.value)} placeholder="общий секрет" spellCheck={false} />
          <button type="button" className="quiz-btn ghost" onClick={() => setMsg(exec(`vpn add ${name} --peer ${peer} --address ${addr} --key ${key}`))}>+ туннель</button>
        </div>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function Resolver({ d, apply, readOnly }) {
  const [v, setV] = useState(d.resolver ?? "");
  const [err, setErr] = useState("");
  const commit = () => {
    if (readOnly) return;
    setErr("");
    if (v.trim() && parseIp(v.trim()) === null) return setErr("нужен IPv4-адрес DNS-сервера");
    apply((n) => void (n.devices[d.id].resolver = v.trim() || undefined));
  };
  return (
    <div className="nl-sec">
      <Field label="DNS-сервер (/etc/resolv.conf: nameserver)" error={err}>
        <input value={v} onChange={(e) => setV(e.target.value)} onBlur={commit} onKeyDown={(e) => e.key === "Enter" && commit()} placeholder="например 192.168.0.53" disabled={readOnly} spellCheck={false} />
      </Field>
    </div>
  );
}

function DnsServer({ d, apply, readOnly, exec }) {
  const [name, setName] = useState("");
  const [type, setType] = useState("A");
  const [val, setVal] = useState("");
  const [zone, setZone] = useState("");
  const [ns, setNs] = useState("");
  const [msg, setMsg] = useState("");
  const dns = d.dns;
  return (
    <div className="nl-sec">
      <h4>DNS-сервер {dns.recursive ? "(рекурсивный резолвер)" : "(авторитативный)"}</h4>
      {dns.zones.length > 0 && <p className="nl-none">зоны: {dns.zones.map((z: any) => z || "корень").join(", ")}</p>}
      {dns.recursive && (
        <div className="nl-add">
          <span className="nl-lbl">корневой сервер</span>
          <input defaultValue={dns.roots[0] ?? ""} disabled={readOnly} placeholder="198.41.0.4" spellCheck={false} onBlur={(e) => e.target.value && setMsg(exec(`dns root ${e.target.value.trim()}`))} />
        </div>
      )}
      <table className="nl-table">
        <tbody>
          {dns.records.map((r, k: Key|null|undefined) => (
            <tr key={k}>
              <td>{r.name}</td>
              <td>{r.type}</td>
              <td>{r.value}</td>
              <td>{!readOnly && <button type="button" className="nl-x" aria-label="Удалить запись" onClick={() => apply((s) => void s.devices[d.id].dns.records.splice(k, 1))}>×</button>}</td>
            </tr>
          ))}
          {dns.delegations.map((x, k: string) => (
            <tr key={"d" + k}>
              <td>{x.zone}</td>
              <td>NS →</td>
              <td>{x.ns}</td>
              <td>{!readOnly && <button type="button" className="nl-x" aria-label="Убрать делегирование" onClick={() => apply((s) => void s.devices[d.id].dns.delegations.splice(k, 1))}>×</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {!readOnly && !dns.recursive && (
        <>
          <div className="nl-add">
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="имя shop.example.org" spellCheck={false} />
            <select value={type} onChange={(e) => setType(e.target.value)}>
              <option>A</option>
              <option>CNAME</option>
              <option>MX</option>
              <option>TXT</option>
            </select>
            <input value={val} onChange={(e) => setVal(e.target.value)} placeholder="значение" spellCheck={false} />
            <button type="button" className="quiz-btn ghost" onClick={() => { setMsg(exec(`dns add ${name} ${type} ${val}`)); setName(""); setVal(""); }}>
              + запись
            </button>
          </div>
          <div className="nl-add">
            <input value={zone} onChange={(e) => setZone(e.target.value)} placeholder="делегировать зону example.org" spellCheck={false} />
            <input value={ns} onChange={(e) => setNs(e.target.value)} placeholder="на сервер 198.51.100.30" spellCheck={false} />
            <button type="button" className="quiz-btn ghost" onClick={() => { setMsg(exec(`dns delegate ${zone} ${ns}`)); setZone(""); setNs(""); }}>
              + делегирование
            </button>
          </div>
        </>
      )}
      {msg && <em className="nl-err">{msg}</em>}
    </div>
  );
}

function TcpTune({ d, apply, readOnly }) {
  const [w, setW] = useState(String(d.rwnd ?? 64));
  return (
    <div className="nl-sec">
      <h4>Настройки TCP</h4>
      <div className="nl-add">
        <span className="nl-lbl">Окно приёма, КБ</span>
        <input
          className="nl-prefix wide"
          value={w}
          disabled={readOnly}
          aria-label="Окно приёма"
          onChange={(e) => setW(e.target.value.replace(/\D/g, "").slice(0, 6))}
          onBlur={() => Number(w) >= 4 && apply((n) => void (n.devices[d.id].rwnd = Number(w)))}
          onKeyDown={(e) => e.key === "Enter" && Number(w) >= 4 && apply((n) => void (n.devices[d.id].rwnd = Number(w)))}
        />
        <span className="nl-lbl">алгоритм</span>
        <select value={d.cc ?? "cubic"} disabled={readOnly} onChange={(e) => apply((n) => void (n.devices[d.id].cc = e.target.value))}>
          <option>reno</option>
          <option>cubic</option>
          <option>bbr</option>
        </select>
      </div>
    </div>
  );
}

function GatewayField({ d, apply, readOnly }) {
  const [gw, setGw] = useState(getGateway(d));
  const [err, setErr] = useState("");
  const commit = () => {
    if (readOnly) return;
    setErr("");
    const e = apply((n) => setGateway(n.devices[d.id], gw.trim()));
    if (e) setErr(e);
  };
  return (
    <div className="nl-sec">
      <Field label="Шлюз по умолчанию" error={err}>
        <input
          value={gw}
          onChange={(e) => setGw(e.target.value)}
          onBlur={commit}
          onKeyDown={(e) => e.key === "Enter" && commit()}
          placeholder="например 192.168.0.1 (пусто — шлюза нет)"
          disabled={readOnly}
          spellCheck={false}
        />
      </Field>
    </div>
  );
}
