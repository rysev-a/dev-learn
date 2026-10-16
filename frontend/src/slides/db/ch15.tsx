// Слайды для «Базы данных», глава 15 — «Оконные функции».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db15.tsx).

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
} from "../anim/Db15.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ИНДЕКСЫ, CTE, ОКНА И ПРЕДСТАВЛЕНИЯ / ГЛАВА 15", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Агрегат без схлопывания"}
      sub={"Глава 15 · Окна"}
      main={"Оконная функция считает по набору строк, но не схлопывает их."}
    >
      <V01 cues={[13.3, 26.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"OVER"}
      sub={"Что делает окно"}
      main={"Функция OVER (…) — признак окна; пустое OVER () — все строки."}
    >
      <V02 cues={[10.6, 21.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"PARTITION BY"}
      sub={"Окно в группе"}
      main={"PARTITION BY делит строки на окна, как GROUP BY, но строки остаются."}
    >
      <V03 cues={[11.8, 23.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Накопительный итог"}
      sub={"ORDER BY в окне"}
      main={"SUM(x) OVER (ORDER BY …) — нарастающий итог."}
    >
      <V04 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"ROW_NUMBER"}
      sub={"Нумерация строк"}
      main={"ROW_NUMBER() нумерует строки окна: 1, 2, 3, …"}
    >
      <V05 cues={[11.6, 23.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"RANK и DENSE_RANK"}
      sub={"Места с ничьими"}
      main={"RANK оставляет «дырки» после ничьей, DENSE_RANK — нет."}
    >
      <V06 cues={[11.4, 22.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Топ-N в группе"}
      sub={"Лучшие в каждой категории"}
      main={"ROW_NUMBER в CTE + WHERE rn <= N — топ в каждой группе."}
    >
      <V07 cues={[11.7, 23.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"LAG и LEAD"}
      sub={"Соседние строки"}
      main={"LAG берёт значение предыдущей строки, LEAD — следующей."}
    >
      <V08 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"FIRST_VALUE и LAST_VALUE"}
      sub={"Опорные строки"}
      main={"FIRST_VALUE и LAST_VALUE берут значение первой и последней строки окна."}
    >
      <V09 cues={[11.6, 23.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Рамка окна"}
      sub={"ROWS BETWEEN"}
      main={"ROWS BETWEEN … AND … задаёт, какие строки видит каждая строка."}
    >
      <V10 cues={[11, 22]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"NTILE и доли"}
      sub={"Квантили"}
      main={"NTILE(n) делит строки на n равных групп; доля = значение / SUM() OVER ()."}
    >
      <V11 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Порядок выполнения"}
      sub={"Где живут окна"}
      main={"Окна считаются после WHERE, GROUP BY и HAVING, до ORDER BY."}
    >
      <V12 cues={[11.6, 23.3]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Окна"}
      main={"OVER (PARTITION BY … ORDER BY … ROWS …) — формула окна."}
    >
      <V13 cues={[12.3, 24.6]} />
    </Slide>
  );
}

export const SLIDES_D15 = {
  "9:15": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D15).
export const SLIDE_TITLES_D15 = {
  "9:15": [
    "Введение",
    "OVER",
    "PARTITION BY",
    "Накопительный",
    "ROW_NUMBER",
    "RANK",
    "Топ в группе",
    "LAG и LEAD",
    "FIRST_VALUE",
    "Рамка",
    "NTILE",
    "Порядок",
    "Итоги",
  ],
};
