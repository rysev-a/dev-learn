// Слайды для «Базы данных», глава 11 — «Встроенные функции: строки, числа и даты».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db11.tsx).

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
} from "../anim/Db11.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ВЫРАЖЕНИЯ И ГРУППИРОВКА / ГЛАВА 11", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Функции по строке"}
      sub={"Глава 11 · Скалярные функции"}
      main={"Скалярная функция вычисляется для каждой строки; агрегатная — для набора."}
    >
      <V01 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Числа"}
      sub={"ABS, ROUND, остаток"}
      main={"ABS, ROUND и % — основа числовой обработки."}
    >
      <V02 cues={[12.6, 25.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Округление"}
      sub={"Что такое ROUND"}
      main={"ROUND округляет «от нуля»: 2.5 → 3, −2.5 → −3."}
    >
      <V03 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Формат вывода"}
      sub={"PRINTF"}
      main={"PRINTF('%.2f', x) форматирует число и склеивает текст."}
    >
      <V04 cues={[11.5, 23]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Дата и время"}
      sub={"DATE, TIME, DATETIME"}
      main={"DATE('now') возвращает сегодняшнюю дату в формате ISO."}
    >
      <V05 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Сдвиг даты"}
      sub={"Модификаторы"}
      main={"Модификаторы сдвигают дату: '+7 days', 'start of month'."}
    >
      <V06 cues={[11.8, 23.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"STRFTIME"}
      sub={"Части даты"}
      main={"STRFTIME('%Y-%m', d) вырезает год и месяц — удобно для группировки."}
    >
      <V07 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Разница дат"}
      sub={"JULIANDAY"}
      main={"JULIANDAY(a) − JULIANDAY(b) — число дней между датами."}
    >
      <V08 cues={[11.6, 23.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Давность"}
      sub={"Последние N дней"}
      main={"Условие по давности: date >= DATE('now', '-30 days')."}
    >
      <V09 cues={[12, 24]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Подводные камни дат"}
      sub={"Форматы и пояса"}
      main={"Неверный формат даты даёт NULL; часовые пояса храните явно."}
    >
      <V10 cues={[12, 24]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Типы и приведение"}
      sub={"typeof и CAST"}
      main={"typeof показывает тип значения, CAST меняет его явно."}
    >
      <V11 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Собираем функции"}
      sub={"Композиция"}
      main={"Функции можно вкладывать друг в друга: результат одной — аргумент другой."}
    >
      <V12 cues={[12.3, 24.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Функции"}
      main={"Числа, текст, даты: функции считаются для каждой строки."}
    >
      <V13 cues={[11.4, 22.7]} />
    </Slide>
  );
}

export const SLIDES_D11 = {
  "9:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D11).
export const SLIDE_TITLES_D11 = {
  "9:11": [
    "Введение",
    "Числа",
    "ROUND",
    "PRINTF",
    "Дата",
    "Модификаторы",
    "STRFTIME",
    "JULIANDAY",
    "Давность",
    "Камни",
    "Типы",
    "Композиция",
    "Итоги",
  ],
};
