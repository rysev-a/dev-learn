/* Реестр упражнений книги «Компьютерные сети»: номер главы → сценарии лаборатории. */
import { CH01 } from "./scenarios/ch01.ts";
import { CH02 } from "./scenarios/ch02.ts";
import { CH03 } from "./scenarios/ch03.ts";
import { CH04 } from "./scenarios/ch04.ts";
import { CH05 } from "./scenarios/ch05.ts";
import { CH06 } from "./scenarios/ch06.ts";
import { CH07 } from "./scenarios/ch07.ts";
import { CH08 } from "./scenarios/ch08.ts";
import { CH10 } from "./scenarios/ch10.ts";
import { CH11 } from "./scenarios/ch11.ts";
import { CH12 } from "./scenarios/ch12.ts";
import { CH13 } from "./scenarios/ch13.ts";
import { CH15 } from "./scenarios/ch15.ts";
import { CH16 } from "./scenarios/ch16.ts";
import { CH17 } from "./scenarios/ch17.ts";
import { CH18 } from "./scenarios/ch18.ts";
import { CH19 } from "./scenarios/ch19.ts";
import { CH20 } from "./scenarios/ch20.ts";
import type { Scenario } from "./types.ts";

export const NET_BOOK = 15;

export const NET_CHAPTERS: Record<number, Scenario[]> = {
  1: CH01,
  2: CH02,
  3: CH03,
  4: CH04,
  5: CH05,
  6: CH06,
  7: CH07,
  8: CH08,
  10: CH10,
  11: CH11,
  12: CH12,
  13: CH13,
  15: CH15,
  16: CH16,
  17: CH17,
  18: CH18,
  19: CH19,
  20: CH20,
};

export const netTasks = (chapter: string | number) =>
  (NET_CHAPTERS[Number(chapter)] ?? []).map((s) => ({
    id: s.id,
    title: s.title,
    text: s.statement,
    hint: s.hint,
  }));

export const NET_BY_ID: Record<string, Scenario> = Object.fromEntries(
  Object.values(NET_CHAPTERS).flat().map((s) => [s.id, s]),
);
