// Слайды для «Изучаем Rust», глава 12 — «Списки Python, массивы и векторы Rust».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs12.jsx).

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
} from "../anim/Rs12.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 12", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"list и Vec"}
      sub={"Глава 12 · Python → Rust"}
      main={"Что соответствует списку; ловушки, которые исчезают."}
    >
      <V01 cues={[16.9, 29.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Однородность"}
      sub={"Типы элементов"}
      main={"Vec однороден; разные типы — enum."}
    >
      <V02 cues={[13.9, 25.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Основные методы"}
      sub={"push, pop, remove"}
      main={
        "append → push; pop возвращает Option; remove по значению — retain."
      }
    >
      <V03 cues={[12.1, 22.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Индексы и срезы"}
      sub={"Без отрицательных индексов"}
      main={"last(); срез — ссылка; step_by, chunks, windows."}
    >
      <V04 cues={[15.0, 25.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Копирование"}
      sub={"Алиасы и клоны"}
      main={"Перемещение, clone, to_vec."}
    >
      <V05 cues={[13.2, 22.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Изменение при обходе"}
      sub={"Ошибка сборки"}
      main={"retain, drain, filter + collect."}
    >
      <V06 cues={[13.6, 28.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сортировка"}
      sub={"sort, key, bisect"}
      main={"sort, sort_by_key, binary_search, max, min."}
    >
      <V07 cues={[12.5, 25.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Включения"}
      sub={"Итераторы"}
      main={"filter + map + collect; zip, enumerate, windows, fold."}
    >
      <V08 cues={[12.3, 24.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ёмкость"}
      sub={"capacity"}
      main={"len и capacity; рост вдвое; with_capacity."}
    >
      <V09 cues={[13.8, 26.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Разные типы"}
      sub={"enum и dyn Trait"}
      main={"Закрытый и открытый набор типов."}
    >
      <V10 cues={[14.6, 28.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Стек и очередь"}
      sub={"Vec, VecDeque, BinaryHeap"}
      main={"Vec — стек, VecDeque — очередь, BinaryHeap — куча."}
    >
      <V11 cues={[13.7, 28.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Двумерные списки"}
      sub={"Ловушка [[0]*n]*m"}
      main={"vec![vec![0; n]; m]; плоский вектор."}
    >
      <V12 cues={[13.1, 30.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — классы, трейты, операторы."}
    >
      <V13 cues={[11.4, 25.9]} />
    </Slide>
  );
}

export const SLIDES_R12 = {
  "10:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R12).
export const SLIDE_TITLES_R12 = {
  "10:12": [
    "Введение",
    "Однородность",
    "Методы",
    "Срезы",
    "Копирование",
    "Обход",
    "Сортировка",
    "Включения",
    "Ёмкость",
    "Разные типы",
    "Очереди",
    "Сетки",
    "Итоги",
  ],
};
