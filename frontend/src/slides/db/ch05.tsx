// Слайды для «Базы данных», глава 5 — «Агрегатные функции».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db05.tsx).

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
} from "../anim/Db05.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / АГРЕГАТЫ, СОЕДИНЕНИЯ И ПОДЗАПРОСЫ / ГЛАВА 5", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Много строк — одно число"}
      sub={"Глава 5 · Агрегаты"}
      main={"Агрегатная функция сворачивает много строк в одно значение."}
    >
      <V01 cues={[12.4, 24.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"COUNT(*)"}
      sub={"Сколько строк"}
      main={"COUNT(*) считает строки после фильтрации."}
    >
      <V02 cues={[11.2, 22.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"SUM и AVG"}
      sub={"Сумма и среднее"}
      main={"SUM складывает, AVG делит сумму на число значений."}
    >
      <V03 cues={[12.3, 24.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"MIN и MAX"}
      sub={"Крайние значения"}
      main={"MIN и MAX работают с числами, строками и датами."}
    >
      <V04 cues={[11.6, 23.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"COUNT(столбец)"}
      sub={"Пропуски не считаются"}
      main={"COUNT(col) считает только непустые значения столбца."}
    >
      <V05 cues={[11.4, 22.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"NULL и агрегаты"}
      sub={"Пропуски игнорируются"}
      main={"SUM, AVG, MIN и MAX пропускают NULL; на пустом наборе SUM даёт NULL."}
    >
      <V06 cues={[11.2, 22.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"COUNT(DISTINCT)"}
      sub={"Сколько разных"}
      main={"COUNT(DISTINCT x) считает различные значения."}
    >
      <V07 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"WHERE и агрегаты"}
      sub={"Фильтр до свёртки"}
      main={"Сначала WHERE отбирает строки, потом агрегат считает по ним."}
    >
      <V08 cues={[10.8, 21.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Столбец рядом с агрегатом"}
      sub={"Что нельзя смешивать"}
      main={"Обычный столбец рядом с агрегатом без GROUP BY — ошибка логики."}
    >
      <V09 cues={[11.3, 22.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Несколько агрегатов"}
      sub={"В одном запросе"}
      main={"В одном SELECT можно считать любое число агрегатов."}
    >
      <V10 cues={[11.1, 22.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Выражения внутри"}
      sub={"SUM(qty * price)"}
      main={"Внутри агрегата — любое выражение; AVG не равен SUM / COUNT при NULL."}
    >
      <V11 cues={[10.5, 21.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"GROUP_CONCAT"}
      sub={"Склеить значения"}
      main={"GROUP_CONCAT склеивает значения группы в одну строку."}
    >
      <V12 cues={[12.8, 25.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Свёртка"}
      main={"Агрегаты сворачивают таблицу; помните про пять ловушек."}
    >
      <V13 cues={[12.7, 25.5]} />
    </Slide>
  );
}

export const SLIDES_D05 = {
  "9:5": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D05).
export const SLIDE_TITLES_D05 = {
  "9:5": [
    "Введение",
    "COUNT(*)",
    "SUM и AVG",
    "MIN и MAX",
    "COUNT(col)",
    "NULL",
    "DISTINCT",
    "WHERE",
    "Смешивание",
    "Несколько",
    "Выражения",
    "GROUP_CONCAT",
    "Итоги",
  ],
};
