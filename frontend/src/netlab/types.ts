// Доменные типы симулятора сети. Состояние сети — простые JSON-объекты (сохраняются строкой в кабинете).

export type DeviceKind = "host" | "server" | "router" | "switch" | "hub" | "internet";

export interface Tunnel {
  peer: string;
  port: number;
  key: string;
}

export interface Iface {
  name: string;
  mac: string;
  ip: string | null;
  prefix: number;
  up: boolean;
  mtu?: number;
  vlan?: number;
  trunk?: boolean;
  tun?: Tunnel;
  txqueuelen?: number;
}

/** маршрут: dst — «10.0.0.0/24», via — шлюз или null (напрямую), dev — интерфейс */
export interface Route {
  dst: string;
  via: string | null;
  dev?: string | null;
}

export interface NatRule {
  chain: "PREROUTING" | "POSTROUTING" | string;
  action: "DNAT" | "MASQUERADE" | string;
  in?: string;
  out?: string;
  src?: string | null;
  dst?: string | null;
  proto?: string;
  dport?: number;
  to?: string;
}

export interface FwRule {
  action: string;
  src?: string | null;
  dst?: string | null;
  proto?: string;
  sport?: number;
  dport?: number;
  in?: string;
  out?: string;
  state?: string | undefined;
}

export interface Firewall {
  policy: string;
  rules: FwRule[];
}

export interface Service {
  proto: string;
  port: number;
  bind?: string;
  name?: string;
}

/* ---- прикладные службы ---- */

export interface DnsRecord {
  name: string;
  type: string;
  value: string;
  ttl?: number;
}

export interface DnsDelegation {
  zone: string;
  ns: string;
}

export interface DnsConfig {
  records: DnsRecord[];
  delegations: DnsDelegation[];
  zones: string[];
  recursive: boolean;
  roots: string[];
}

export interface HttpRoute {
  path: string;
  status?: number;
  body?: string | undefined;
  type?: string;
  headers?: Record<string, string>;
  location?: string;
  etag?: string;
}

export interface HttpConfig {
  routes: HttpRoute[];
  protocol?: "h1" | "h2" | "h3";
  page?: { count: number; kb: number };
}

export interface RProxyRule {
  host?: string | undefined;
  path?: string;
  backend: string;
  cache?: boolean;
}

export interface RProxyConfig {
  rules: RProxyRule[];
}

export interface ProxyConfig {
  deny: string[];
  port?: number;
}

export interface TlsCert {
  cn: string;
  san: string[];
  issuer: string;
  notAfter: string;
}

export interface TlsConfig {
  cert: TlsCert;
  chain: string[];
  versions: string[];
}

export interface Pki {
  cas: Record<string, { issuer: string | null }>;
}

export interface SshUser {
  keys: string[];
  password?: string | undefined;
}

export interface SshConfig {
  hostKey: string;
  rot?: number;
  passwordAuth: boolean;
  users: Record<string, SshUser>;
}

export interface LbBackend {
  ip: string;
  port: number;
}

export interface LbConfig {
  vip: string;
  port: number;
  algo?: string;
  health?: boolean;
  backends: LbBackend[];
}

export interface AttackConfig {
  type: "arpspoof" | "synflood" | "scan" | string;
  victim?: string;
  gatewayIp?: string;
  target?: string;
  port?: number;
  ports?: number[];
}

/** устройство: расширения (dns, http, tls, …) есть только у тех, кто их запускает */
export interface Device {
  id: string;
  kind: DeviceKind;
  name: string;
  x: number;
  y: number;
  ifaces: Iface[];
  routes: Route[];
  forward: boolean;
  nat: NatRule[];
  fw: Firewall;
  services: Service[];
  locked: boolean;
  dropPrivate: boolean;
  icmpBlock?: boolean;
  syncookies?: boolean;
  arpStatic?: Record<string, string>;
  hosts?: Record<string, string>;
  resolver?: string | null | undefined;
  trust?: string[];
  tlsMin?: string;
  sshKey?: string | null;
  knownHosts?: Record<string, string>;
  rwnd?: number;
  cc?: string;
  dns?: DnsConfig;
  http?: HttpConfig;
  rproxy?: RProxyConfig;
  proxy?: ProxyConfig;
  tls?: TlsConfig;
  ssh?: SshConfig;
  lb?: LbConfig;
  attack?: AttackConfig;
}

export interface Link {
  a: string;
  b: string;
  km: number;
  mbps: number;
  mtu?: number;
  loss?: number;
}

/* ---- кадры и пакеты ---- */

export interface IcmpInfo {
  type: string;
  id: number;
  orig?: Tuple;
  code?: string | null;
  mtu?: number | null;
}

export interface Tuple {
  proto: string;
  src: number | null;
  dst: number;
  sport?: number | undefined;
  dport?: number | undefined;
}

export interface DnsQuestion {
  name: string;
  type: string;
}

export interface DnsMessage {
  id: number;
  q: DnsQuestion;
  response: boolean;
  rd?: boolean;
  ra?: boolean;
  rcode?: string;
  answers?: DnsRecord[];
  referral?: { zone: string; ns: string } | null;
}

export interface Packet {
  src: number | null;
  dst: number;
  ttl: number;
  proto: string;
  sport?: number | undefined;
  dport?: number | undefined;
  size?: number;
  noTun?: boolean;
  tunnel?: { inner: Packet; key: string; name: string };
  icmp?: IcmpInfo | undefined;
  df?: boolean;
  flags?: string;
  seq?: number;
  ack?: number;
  len?: number;
  dns?: DnsMessage;
  fwd?: boolean;
}

export interface ArpInfo {
  op: "req" | "rep";
  sip: number;
  smac: string;
  tip: number;
  tmac: string | null;
}

interface FrameBase {
  size: number;
  src: string;
  dst: string;
  vlan?: number | undefined;
  uid?: number;
}

export interface ArpFrame extends FrameBase {
  type: "arp";
  arp: ArpInfo;
}

export interface IpFrame extends FrameBase {
  type: "ip";
  ip: Packet;
}

export type Frame = ArpFrame | IpFrame;

export interface NetEvent {
  t: number;
  dev: string;
  kind: string;
  text: string;
}

export interface Hop {
  from: string;
  fromPort: string;
  to: string;
  toPort: string;
  t0: number;
  t1: number;
  kind: string;
  label: string;
  frame: Frame;
}

export interface Delivered {
  dev: string;
  src: number | null;
  dst: number | null;
  proto: string;
  dport: number | null;
  sport: number | null;
}

/** итог пробы (ping, TCP, UDP, DNS) */
export interface ProbeRun {
  status: string;
  from: number | null;
  code: string | null;
  mtu: number | null;
  dns: DnsMessage | null;
  rttUs: number | null;
  events: NetEvent[];
  hops: Hop[];
  delivered: Delivered[];
}

export interface ConnEntry {
  orig: Tuple;
  tr: Tuple;
  replied: boolean;
}

/** служебные кэши симулятора; в кабинет не сохраняются */
export interface Runtime {
  arp: Record<string, Record<string, { mac: string; at: number; sim: number }>>;
  mac: Record<string, Record<string, string>>;
  ct: Record<string, ConnEntry[]>;
  dnsCache: Record<string, Record<string, DnsRecord[]>>;
  tunPeer?: Record<string, { ip: number | null; port: number | undefined; }>;
  lb?: Record<string, { n: number }>;
  fx?: { synflood: Record<string, boolean> };
  cap?: Record<string, { t: number; dir: string; frame: Frame }[]>;
  clock?: number;
  rpcache?: Record<string, Record<string, HttpResponse>>;
}

export interface NetState {
  devices: Record<string, Device>;
  links: Link[];
  rt?: Runtime | undefined;
  pki?: Pki;
  __busy?: boolean;
  [meta: string]: unknown;
}

export interface ProbeResult {
  status: string;
  from: number | null;
  at: number;
  ttl?: number;
  code?: string | null | undefined;
  mtu?: number | null | undefined;
  dns?: DnsMessage | undefined;
}

/** текущая проба симулятора: кто её послал и чем она закончилась */
export interface Probe {
  origin: string;
  id: number;
  sport?: number;
  result: ProbeResult | null;
  dst?: number | null;
  session?: boolean;
}

/* ---- HTTP ---- */

export interface HttpRequest {
  method: string;
  path: string;
  host?: string;
  headers: Record<string, string>;
}

export interface HttpResponse {
  status: number;
  reason: string;
  headers: Record<string, string>;
  body: string;
  rttUs?: number;
  ip?: number | null | undefined;
  via?: string | undefined;
  url?: string;
}

export interface ParsedUrl {
  scheme: string;
  host: string;
  port: number;
  path: string;
}

/** разрешение имени для curl: ip или ошибка (и проба DNS, если она была) */
export type ToIp = (
  state: NetState,
  d: Device,
  host: string,
) => { ip: number; from?: string | undefined; err?: undefined; run?: ProbeRun | undefined } | { err: string; ip?: undefined; run?: ProbeRun };

/* ---- сценарии и цели упражнений ---- */

export interface ProbeGoal {
  from: string;
  to: string;
  port?: number;
  expect?: "ok" | "fail";
  size?: number;
  df?: boolean;
  sizeFromMtu?: boolean;
  warm?: boolean;
  maxRttMs?: number;
  via?: string;
  avoid?: string;
  noLoop?: boolean;
  notSeenBy?: string;
  seenSrc?: string;
}

/** цель упражнения: ровно одно из полей-проверок */
export interface Goal {
  id: string;
  text: string;
  ping?: ProbeGoal;
  tcp?: ProbeGoal;
  udp?: ProbeGoal;
  dns?: { from: string; name: string; expect: string };
  mtu?: { dev: string; iface?: string; min?: number; max?: number };
  lbspread?: { from: string; to: string; port: number; n: number; distinct?: number; avoid?: string[]; sticky?: boolean };
  ssh?: { from: string; to: string; user: string; via?: string; pass?: string; auth?: string; expect?: string };
  page?: { from: string; to: string; https?: boolean; maxS: number };
  http?: {
    from: string;
    url: string;
    method?: string;
    follow?: boolean;
    headers?: Record<string, string>;
    proxy?: string;
    repeat?: number;
    fail?: boolean;
    nth?: number;
    status?: number;
    header?: Record<string, string | true>;
    noHeader?: string[];
    bodyIncludes?: string;
    maxRttMs?: number;
    hops?: number;
    finalUrl?: string;
  };
  xfer?: { from: string; to: string; mb?: number; minMbps?: number; maxLoadedRttMs?: number };
}

/** то, что показывает панель результата: хопы, события и (для передачи файла) график */
export interface GoalRun {
  hops: Hop[];
  events: NetEvent[];
  delivered: Delivered[];
  chart?: unknown;
  status?: string;
  err?: string;
}

export interface GoalResult {
  id: string;
  text: string;
  ok: boolean;
  detail: string;
  run: GoalRun;
}

/** шаг эталонного решения */
export type Op =
  | { unlink: [string, string] }
  | { drop: string }
  | { cable: [string, string]; extra?: Partial<Link> }
  | { cmd: [string, string] };

export interface Scenario {
  id: string;
  title: string;
  statement: string;
  hint: string;
  tools: Record<string, boolean | undefined>;
  build: () => NetState;
  goals: Goal[];
  /** шаги эталонного решения; функция — когда шаги зависят от состояния (MAC-адреса и т. п.) */
  solution: Op[] | ((state: NetState) => Op[]);
}
