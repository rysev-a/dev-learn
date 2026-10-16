// Слайды для «Изучаем Rust», глава 25 — «Коллекции std: Vec, VecDeque, HashMap, BTreeMap, BinaryHeap».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs25.jsx).

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
} from "../anim/Rs25.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 25</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Восемь коллекций"}
      sub={"Глава 25 · Как выбирать"}
      main={"Начинайте с Vec; в большинстве программ хватает Vec и HashMap."}
    >
      <V01 cues={[13.0, 31.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Vec"}
      sub={"ptr, len, cap"}
      main={"Устройство, амортизированный push, swap_remove."}
    >
      <V02 cues={[11.9, 24.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Срезы"}
      sub={"Методы &[T]"}
      main={"windows, chunks, sort, binary_search и другие."}
    >
      <V03 cues={[20.6, 29.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"VecDeque"}
      sub={"Кольцевой буфер"}
      main={"Оба конца O(1); as_slices."}
    >
      <V04 cues={[13.2, 28.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"HashMap"}
      sub={"Swiss table"}
      main={"Метки хеша, рост, retain, drain."}
    >
      <V05 cues={[17.3, 27.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"HashSet"}
      sub={"Множество"}
      main={"Членство и операции над множествами."}
    >
      <V06 cues={[16.2, 30.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"BTreeMap"}
      sub={"B-дерево"}
      main={"Порядок, диапазоны, крайние элементы."}
    >
      <V07 cues={[14.9, 27.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"BinaryHeap"}
      sub={"Куча"}
      main={"push, pop, peek; Reverse для минимума."}
    >
      <V08 cues={[16.3, 30.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"LinkedList"}
      sub={"Почти не нужен"}
      main={"Плохая локальность кэша; Vec и VecDeque лучше."}
    >
      <V09 cues={[17.4, 28.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Общий интерфейс"}
      sub={"Итераторы и collect"}
      main={"iter, iter_mut, into_iter, collect, extend, drain."}
    >
      <V10 cues={[16.1, 28.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Сложности"}
      sub={"Таблица и кэш"}
      main={"O(1), O(log n), O(n) — но кэш решает."}
    >
      <V11 cues={[11.8, 28.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Внешние пакеты"}
      sub={"indexmap, smallvec, …"}
      main={"Что даёт экосистема."}
    >
      <V12 cues={[16.4, 27.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — текст и форматирование."}
    >
      <V13 cues={[12.9, 26.1]} />
    </Slide>
  );
}

export const SLIDES_R25 = {
  "10:25": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R25).
export const SLIDE_TITLES_R25 = {
  "10:25": [
    "Введение",
    "Vec",
    "Срезы",
    "VecDeque",
    "HashMap",
    "HashSet",
    "BTreeMap",
    "BinaryHeap",
    "LinkedList",
    "Итераторы",
    "Сложности",
    "Пакеты",
    "Итоги",
  ],
};
