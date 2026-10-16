/* Реестр упражнений книги «Компьютерные сети»: номер главы → сценарии лаборатории. */
import { CH01 } from "./scenarios/ch01.js";
import { CH02 } from "./scenarios/ch02.js";
import { CH03 } from "./scenarios/ch03.js";
import { CH04 } from "./scenarios/ch04.js";
import { CH05 } from "./scenarios/ch05.js";
import { CH06 } from "./scenarios/ch06.js";
import { CH07 } from "./scenarios/ch07.js";
import { CH08 } from "./scenarios/ch08.js";
import { CH10 } from "./scenarios/ch10.js";
import { CH11 } from "./scenarios/ch11.js";
import { CH12 } from "./scenarios/ch12.js";
import { CH13 } from "./scenarios/ch13.js";
import { CH15 } from "./scenarios/ch15.js";
import { CH16 } from "./scenarios/ch16.js";
import { CH17 } from "./scenarios/ch17.js";
import { CH18 } from "./scenarios/ch18.js";
import { CH19 } from "./scenarios/ch19.js";
import { CH20 } from "./scenarios/ch20.js";

export const NET_BOOK = 15;

export const NET_CHAPTERS = {
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

export const netTasks = (chapter) =>
  (NET_CHAPTERS[chapter] ?? []).map((s) => ({
    id: s.id,
    title: s.title,
    text: s.statement,
    hint: s.hint,
  }));

export const NET_BY_ID = Object.fromEntries(
  Object.values(NET_CHAPTERS).flat().map((s) => [s.id, s]),
);
