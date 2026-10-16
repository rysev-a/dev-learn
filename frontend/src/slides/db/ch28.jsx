// Слайды для «Базы данных», глава 28 — «Продвинутый SQL: окна, общие выражения, рекурсия и JSON».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db28.jsx).

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
} from "../anim/Db28.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ПРОЕКТИРОВАНИЕ И SQL / ГЛАВА 28", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"За пределами SELECT"}
      sub={"Глава 28 · Продвинутый SQL"}
      main={
        "Половину задач закрывают простые запросы, остальное — окна, CTE и рекурсия."
      }
    >
      <V01 cues={[9.7, 27.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Общие выражения"}
      sub={"WITH"}
      main={"Запрос читается сверху вниз и проверяется по шагам."}
    >
      <V02 cues={[11.3, 25.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Оконные функции"}
      sub={"OVER, PARTITION BY, ORDER BY"}
      main={"Окно считает значение для каждой строки, не схлопывая их."}
    >
      <V03 cues={[16.6, 23.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Рейтинг"}
      sub={"ROW_NUMBER, RANK, DENSE_RANK"}
      main={"Топ-N в группе: пронумеровать и отфильтровать."}
    >
      <V04 cues={[14.0, 26.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Соседние строки"}
      sub={"LAG, LEAD, FIRST_VALUE"}
      main={"Сравнение периодов без соединения таблицы с собой."}
    >
      <V05 cues={[14.4, 23.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Рамки окна"}
      sub={"ROWS и RANGE"}
      main={"Накопительные и скользящие значения задаёт рамка."}
    >
      <V06 cues={[16.3, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Условная агрегация"}
      sub={"CASE и FILTER"}
      main={"Строки превращаются в столбцы за один проход."}
    >
      <V07 cues={[15.4, 23.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Рекурсия"}
      sub={"WITH RECURSIVE"}
      main={"Якорь, шаг, остановка; цикл ограничивают глубиной."}
    >
      <V08 cues={[3.9, 22.2, 26.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Операции над множествами"}
      sub={"UNION, INTERSECT, EXCEPT, EXISTS"}
      main={"NOT EXISTS находит строки без пары и не боится NULL."}
    >
      <V09 cues={[14.7, 26.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"JSON в SQL"}
      sub={"Пути и индексы"}
      main={"Часто используемые пути индексируют или выносят в столбцы."}
    >
      <V10 cues={[13.6, 27.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Массовые изменения"}
      sub={"UPSERT, RETURNING, MERGE"}
      main={"Атомарные массовые операции без лишних запросов."}
    >
      <V11 cues={[19.1, 28.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"NULL, размножение, порядок"}
      main={"Проверяйте промежуточные результаты и задавайте порядок явно."}
    >
      <V12 cues={[12.6, 26.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — оптимизатор и планы."}
    >
      <V13 cues={[11.6, 27.5]} />
    </Slide>
  );
}

export const SLIDES_D28 = {
  "9:28": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D28).
export const SLIDE_TITLES_D28 = {
  "9:28": [
    "Введение",
    "CTE",
    "Окна",
    "Рейтинг",
    "LAG и LEAD",
    "Рамки",
    "Сводные",
    "Рекурсия",
    "Множества",
    "JSON",
    "UPSERT",
    "Ошибки",
    "Итоги",
  ],
};
