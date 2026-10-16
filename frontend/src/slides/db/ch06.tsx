// Слайды для «Базы данных», глава 6 — «Объединение таблиц: JOIN».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db06.tsx).

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
} from "../anim/Db06.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / АГРЕГАТЫ, СОЕДИНЕНИЯ И ПОДЗАПРОСЫ / ГЛАВА 6", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Данные в разных таблицах"}
      sub={"Глава 6 · Соединения"}
      main={"JOIN склеивает строки двух таблиц по условию."}
    >
      <V01 cues={[12.5, 25]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Каждая с каждой"}
      sub={"Декартово произведение"}
      main={"Без условия JOIN даёт все пары строк: n × m."}
    >
      <V02 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"INNER JOIN"}
      sub={"Условие ON"}
      main={"INNER JOIN … ON оставляет только пары, для которых условие истинно."}
    >
      <V03 cues={[12, 24]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Имена и псевдонимы"}
      sub={"Неоднозначность"}
      main={"Если столбец есть в обеих таблицах, пишите таблица.столбец."}
    >
      <V04 cues={[12.1, 24.3]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"ON и WHERE"}
      sub={"Для INNER — одно и то же"}
      main={"Для INNER JOIN условие в ON и в WHERE равносильно."}
    >
      <V05 cues={[11.5, 23]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"LEFT JOIN"}
      sub={"Сохраняем левую таблицу"}
      main={"LEFT JOIN сохраняет все строки левой таблицы; недостающее заполняет NULL."}
    >
      <V06 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Кто без пары"}
      sub={"Анти-соединение"}
      main={"LEFT JOIN … WHERE правый.ключ IS NULL находит строки без пары."}
    >
      <V07 cues={[11.8, 23.7]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Ловушка LEFT JOIN"}
      sub={"Условие справа в WHERE"}
      main={"Условие по правой таблице в WHERE превращает LEFT JOIN в INNER."}
    >
      <V08 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"RIGHT и FULL"}
      sub={"Другие виды"}
      main={"RIGHT — зеркало LEFT, FULL сохраняет строки обеих таблиц."}
    >
      <V09 cues={[12.1, 24.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Цепочка таблиц"}
      sub={"Несколько JOIN"}
      main={"Таблицы подключают по одной: каждый JOIN — своя связь."}
    >
      <V10 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Размножение строк"}
      sub={"Один ко многим"}
      main={"После JOIN одна строка может размножиться: агрегаты завышаются."}
    >
      <V11 cues={[12.4, 24.7]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Самосоединение"}
      sub={"Таблица с самой собой"}
      main={"Таблицу можно соединить с собой — нужны разные псевдонимы."}
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
      sub={"Соединения"}
      main={"INNER теряет без пары, LEFT сохраняет; условие связи — в ON."}
    >
      <V13 cues={[13.9, 27.8]} />
    </Slide>
  );
}

export const SLIDES_D06 = {
  "9:6": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D06).
export const SLIDE_TITLES_D06 = {
  "9:6": [
    "Введение",
    "CROSS",
    "INNER JOIN",
    "Имена",
    "ON и WHERE",
    "LEFT JOIN",
    "Без пары",
    "Ловушка",
    "RIGHT и FULL",
    "Цепочка",
    "Размножение",
    "Самосоединение",
    "Итоги",
  ],
};
