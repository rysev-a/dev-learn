/* Арифметика IPv4: адреса как беззнаковые 32-битные числа, подсети в виде «a.b.c.d/p». */

export function parseIp(s: string | null | undefined): number | null {
  if (typeof s !== "string") return null;
  const m = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.exec(s.trim());
  if (!m) return null;
  let n = 0;
  for (let i = 1; i <= 4; i++) {
    const o = Number(m[i]);
    if (o > 255 || (m[i]!.length > 1 && m[i]![0] === "0")) return null;
    n = n * 256 + o;
  }
  return n;
}

export const ipStr = (n: number | null | undefined): string => {
  const v = n ?? 0;
  return [v >>> 24, (v >>> 16) & 255, (v >>> 8) & 255, v & 255].join(".");
};

export const maskOf = (p: number) => (p === 0 ? 0 : (0xffffffff << (32 - p)) >>> 0);

/** «192.168.1.10/24» → {ip, prefix} или null */
export function parseCidr(s: unknown): { ip: number; prefix: number } | null {
  const m = /^([\d.]+)\/(\d{1,2})$/.exec(String(s).trim());
  if (!m) return null;
  const ip = parseIp(m[1]);
  const prefix = Number(m[2]);
  if (ip === null || prefix > 32) return null;
  return { ip, prefix };
}

/** маска в виде 255.255.255.0 → длина префикса или null (если маска «дырявая») */
export function prefixOfMask(s: string): number | null {
  const n = parseIp(s);
  if (n === null) return null;
  for (let p = 0; p <= 32; p++) if (maskOf(p) === n) return p;
  return null;
}

export const networkOf = (ip: number | null, prefix: number): number => ((ip ?? 0) & maskOf(prefix)) >>> 0;
export const broadcastOf = (ip: number | null, prefix: number): number =>
  (networkOf(ip, prefix) | (~maskOf(prefix) >>> 0)) >>> 0;
export const inNet = (ip: number | null | undefined, net: number | null | undefined, prefix: number): boolean =>
  networkOf(ip ?? null, prefix) === networkOf(net ?? null, prefix);

export const cidrStr = (ip: number | null | undefined, prefix: number | string): string => `${ipStr(ip)}/${prefix}`;
export const netStr = (ip: number | null, prefix: number): string => cidrStr(networkOf(ip, prefix), prefix);

export function isPrivate(ip: number | null | undefined): boolean {
  return (
    inNet(ip, parseIp("10.0.0.0"), 8) ||
    inNet(ip, parseIp("172.16.0.0"), 12) ||
    inNet(ip, parseIp("192.168.0.0"), 16)
  );
}

/** Подсеть «a.b.c.d/p» или одиночный адрес/«any» → {net, prefix} */
export function parseNet(s: string | null | undefined): { net: number; prefix: number } | null {
  if (s == null || s === "any" || s === "0.0.0.0/0") return { net: 0, prefix: 0 };
  const c = parseCidr(s);
  if (c) return { net: networkOf(c.ip, c.prefix), prefix: c.prefix };
  const ip = parseIp(s);
  return ip === null ? null : { net: ip, prefix: 32 };
}

export function inNetStr(ip: number | null | undefined, spec: string | null | undefined): boolean {
  const n = parseNet(spec);
  return n ? inNet(ip, n.net, n.prefix) : false;
}

export function macStr(n: number): string {
  return [40, 40, (n >> 24) & 255, (n >> 16) & 255, (n >> 8) & 255, n & 255]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join(":");
}

export const BCAST_MAC = "ff:ff:ff:ff:ff:ff";
