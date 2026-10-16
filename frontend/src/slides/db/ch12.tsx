// Слайды для «Базы данных», глава 12 — «Группировка данных: GROUP BY и HAVING».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db12.tsx).

import {
  V01,
  V02,
  V03,
  V04,
  V05,
  V06,
  V07,
  V08,
  V09,
  V10,
  V11,
  V12,
  V13,
} from "../anim/Db12.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ВЫРАЖЕНИЯ И ГРУППИРОВКА / ГЛАВА 12", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Итог по группе"}
      sub={"Глава 12 · GROUP BY"}
      main={"GROUP BY делит строки на группы и считает агрегаты для каждой."}
    >
      <V01 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"GROUP BY"}
      sub={"Один ключ"}
      main={"После GROUP BY — столбец-ключ; по строке на каждое значение ключа."}
    >
      <V02 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Что можно в SELECT"}
      sub={"Ключи и агрегаты"}
      main={"В SELECT — только ключи группы и агрегаты."}
    >
      <V03 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Несколько ключей"}
      sub={"Группа — комбинация"}
      main={"GROUP BY a, b — группы по каждой различной паре значений."}
    >
      <V04 cues={[12, 23.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Группировка по выражению"}
      sub={"Месяц, диапазон"}
      main={"Группировать можно по выражению: месяц, размер, остаток от деления."}
    >
      <V05 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"NULL — тоже группа"}
      sub={"Пропуски в ключе"}
      main={"Все NULL в ключе попадают в одну группу."}
    >
      <V06 cues={[11.6, 23.2]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"HAVING"}
      sub={"Условие на группу"}
      main={"HAVING фильтрует группы по значению агрегата."}
    >
      <V07 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"WHERE или HAVING"}
      sub={"Что куда"}
      main={"Условие по строке — в WHERE, по агрегату — в HAVING."}
    >
      <V08 cues={[11.3, 22.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Порядок выполнения"}
      sub={"Весь запрос"}
      main={"FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT."}
    >
      <V09 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Топ групп"}
      sub={"ORDER BY и LIMIT"}
      main={"ORDER BY агрегат + LIMIT — топ групп."}
    >
      <V10 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Группы и соединения"}
      sub={"Итоги по клиентам"}
      main={"JOIN + GROUP BY: итоги по сущности из другой таблицы."}
    >
      <V11 cues={[11.2, 22.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Что проверять"}
      main={"Лишний столбец, HAVING вместо WHERE, размножение после JOIN."}
    >
      <V12 cues={[11.4, 22.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Группировка"}
      main={"GROUP BY делит на группы, HAVING фильтрует группы, порядок выполнения решает."}
    >
      <V13 cues={[12.2, 24.4]} />
    </Slide>
  );
}

export const SLIDES_D12 = {
  "9:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D12).
export const SLIDE_TITLES_D12 = {
  "9:12": [
    "Введение",
    "GROUP BY",
    "Что в SELECT",
    "Несколько ключей",
    "По выражению",
    "NULL",
    "HAVING",
    "WHERE и HAVING",
    "Порядок",
    "Топ групп",
    "С JOIN",
    "Ошибки",
    "Итоги",
  ],
};
