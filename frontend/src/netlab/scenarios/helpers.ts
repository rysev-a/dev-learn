// Общие помощники сценариев лаборатории сети.
import type { Route } from "../types.ts";

/** маршрут по умолчанию через шлюз */
export const gw = (via: string): Route[] => [{ dst: "0.0.0.0/0", via, dev: null }];

export const route = (dst: string, via: string | null, dev: string | null = null): Route => ({ dst, via, dev });
