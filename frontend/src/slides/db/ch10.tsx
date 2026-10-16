// Слайды для «Базы данных», глава 10 — «Условная логика: CASE WHEN».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db10.tsx).

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
} from "../anim/Db10.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ВЫРАЖЕНИЯ И ГРУППИРОВКА / ГЛАВА 10", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Если… то…"}
      sub={"Глава 10 · CASE"}
      main={"CASE — условное выражение: выбирает значение по условию."}
    >
      <V01 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Поисковый CASE"}
      sub={"WHEN условие THEN значение"}
      main={"CASE WHEN условие THEN значение … ELSE значение END."}
    >
      <V02 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Простой CASE"}
      sub={"CASE выражение WHEN значение"}
      main={"CASE x WHEN a THEN … — сравнение выражения с набором значений."}
    >
      <V03 cues={[11.7, 23.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"ELSE и NULL"}
      sub={"Что если ничего не подошло"}
      main={"Без ELSE неподошедшая строка получает NULL."}
    >
      <V04 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Порядок веток"}
      sub={"Побеждает первая"}
      main={"Ветки проверяются сверху вниз; побеждает первая подошедшая."}
    >
      <V05 cues={[12.1, 24.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Категоризация"}
      sub={"Метки из чисел"}
      main={"CASE превращает числа в понятные категории."}
    >
      <V06 cues={[12.3, 24.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"CASE в ORDER BY"}
      sub={"Свой порядок"}
      main={"CASE в ORDER BY задаёт произвольный порядок значений."}
    >
      <V07 cues={[12.3, 24.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Условный подсчёт"}
      sub={"Агрегат + CASE"}
      main={"SUM(CASE WHEN … THEN 1 ELSE 0 END) считает строки по условию."}
    >
      <V08 cues={[11.9, 23.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Сводная таблица"}
      sub={"Pivot вручную"}
      main={"Несколько условных агрегатов дают сводную таблицу."}
    >
      <V09 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"CASE в UPDATE"}
      sub={"Разные значения за один раз"}
      main={"CASE в UPDATE задаёт разные значения разным строкам одной командой."}
    >
      <V10 cues={[11.2, 22.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"IIF и родственники"}
      sub={"Короткие формы"}
      main={"IIF(условие, а, б) — сокращённый CASE; COALESCE и NULLIF — тоже его частные случаи."}
    >
      <V11 cues={[11.5, 23]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типы и ловушки"}
      sub={"Что проверять"}
      main={"Ветки возвращают значения одного типа; условие с NULL — не истина."}
    >
      <V12 cues={[12, 24]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Условия в запросах"}
      main={"CASE — главное средство условной логики в SQL."}
    >
      <V13 cues={[12.1, 24.1]} />
    </Slide>
  );
}

export const SLIDES_D10 = {
  "9:10": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D10).
export const SLIDE_TITLES_D10 = {
  "9:10": [
    "Введение",
    "Поисковый",
    "Простой",
    "ELSE",
    "Порядок",
    "Категории",
    "ORDER BY",
    "Условный счёт",
    "Сводная",
    "UPDATE",
    "IIF",
    "Ловушки",
    "Итоги",
  ],
};
