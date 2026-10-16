// Слайды для «Базы данных», глава 3 — «Сортировка и ограничение строк».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db03.tsx).

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
} from "../anim/Db03.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ПЕРВЫЕ ЗАПРОСЫ / ГЛАВА 3", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Порядок не обещан"}
      sub={"Глава 3 · ORDER BY"}
      main={"Без ORDER BY порядок строк в результате не гарантирован."}
    >
      <V01 cues={[12.5, 25]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"ASC и DESC"}
      sub={"Направление"}
      main={"ASC — по возрастанию (по умолчанию), DESC — по убыванию."}
    >
      <V02 cues={[11.6, 23.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Сортировка текста"}
      sub={"Алфавит и регистр"}
      main={"Строки сортируются побайтово: заглавные идут перед строчными."}
    >
      <V03 cues={[12.4, 24.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Несколько ключей"}
      sub={"Тай-брейк"}
      main={"Второй ключ разрешает ничьи по первому."}
    >
      <V04 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Что можно сортировать"}
      sub={"Выражения и номера"}
      main={"Сортировать можно по выражению, по псевдониму и по номеру столбца."}
    >
      <V05 cues={[10.8, 21.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Пропуски при сортировке"}
      sub={"NULL"}
      main={"В SQLite NULL считается самым маленьким: он идёт первым."}
    >
      <V06 cues={[11.5, 23.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"LIMIT"}
      sub={"Первые N строк"}
      main={"LIMIT n оставляет первые n строк результата."}
    >
      <V07 cues={[11.3, 22.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Топ-N"}
      sub={"ORDER BY + LIMIT"}
      main={"ORDER BY сначала, LIMIT потом: сортируем, затем обрезаем."}
    >
      <V08 cues={[12.8, 25.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"OFFSET"}
      sub={"Пропустить строки"}
      main={"OFFSET пропускает начало: LIMIT 10 OFFSET 20 — третья страница."}
    >
      <V09 cues={[12.4, 24.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Ловушки пагинации"}
      sub={"Дорого и нестабильно"}
      main={"Большой OFFSET дорог; на больших таблицах листают по ключу."}
    >
      <V10 cues={[11.9, 23.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"DISTINCT и сортировка"}
      sub={"Порядок выполнения"}
      main={"Порядок: WHERE, DISTINCT, ORDER BY, затем LIMIT."}
    >
      <V11 cues={[11.4, 22.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Второй по цене"}
      sub={"Типичная задача"}
      main={"Второй по цене — ORDER BY price DESC LIMIT 1 OFFSET 1."}
    >
      <V12 cues={[11.5, 22.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Порядок и страницы"}
      main={"ORDER BY задаёт порядок, LIMIT и OFFSET — окно в результате."}
    >
      <V13 cues={[10.8, 21.6]} />
    </Slide>
  );
}

export const SLIDES_D03 = {
  "9:3": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D03).
export const SLIDE_TITLES_D03 = {
  "9:3": [
    "Введение",
    "Направление",
    "Текст",
    "Ключи",
    "Выражения",
    "NULL",
    "LIMIT",
    "Топ-N",
    "OFFSET",
    "Пагинация",
    "DISTINCT",
    "Второй",
    "Итоги",
  ],
};
