/* Реестр упражнений книги «Системный дизайн»: номер главы → сценарии лаборатории. */
import { CH01 } from "./scenarios/ch01.ts";
import { CH02 } from "./scenarios/ch02.ts";
import { CH03 } from "./scenarios/ch03.ts";
import { CH04 } from "./scenarios/ch04.ts";
import { CH05 } from "./scenarios/ch05.ts";
import { CH06 } from "./scenarios/ch06.ts";
import { CH07 } from "./scenarios/ch07.ts";
import { CH08 } from "./scenarios/ch08.ts";
import { CH09 } from "./scenarios/ch09.ts";
import { CH10 } from "./scenarios/ch10.ts";
import { CH11 } from "./scenarios/ch11.ts";
import { CH12 } from "./scenarios/ch12.ts";
import { CH13 } from "./scenarios/ch13.ts";
import { CH14 } from "./scenarios/ch14.ts";
import { CH15 } from "./scenarios/ch15.ts";
import { CH16 } from "./scenarios/ch16.ts";
import { CH17 } from "./scenarios/ch17.ts";
import { CH18 } from "./scenarios/ch18.ts";
import type { SdScenario } from "./types.ts";

export const SD_BOOK = 18;

export const SD_CHAPTERS: Record<number, SdScenario[]> = {
  1: CH01,
  2: CH02,
  3: CH03,
  4: CH04,
  5: CH05,
  6: CH06,
  7: CH07,
  8: CH08,
  9: CH09,
  10: CH10,
  11: CH11,
  12: CH12,
  13: CH13,
  14: CH14,
  15: CH15,
  16: CH16,
  17: CH17,
  18: CH18,
};

export const sdTasks = (chapter: string | number) =>
  (SD_CHAPTERS[Number(chapter)] ?? []).map((s) => ({
    id: s.id,
    title: s.title,
    text: s.statement,
    hint: s.hint,
  }));

export const SD_BY_ID: Record<string, SdScenario> = Object.fromEntries(
  Object.values(SD_CHAPTERS).flat().map((s) => [s.id, s]),
);
