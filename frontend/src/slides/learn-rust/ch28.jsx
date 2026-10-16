// Слайды для «Изучаем Rust», глава 28 — «Время, числа и память: Duration, Instant, num, mem».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs28.jsx).

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
} from "../anim/Rs28.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 28</span>
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
      title={"Время, числа, память"}
      sub={"Глава 28 · Что в std"}
      main={"Время и числа в std; календарь и случайность — пакеты."}
    >
      <V01 cues={[5.5, 21.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Duration"}
      sub={"Длительность"}
      main={"Создание, чтение, арифметика, безопасные операции."}
    >
      <V02 cues={[14.4, 31.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Instant и SystemTime"}
      sub={"Два вида моментов"}
      main={"Замеры — Instant; метки — SystemTime; календарь — пакеты."}
    >
      <V03 cues={[17.1, 30.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Паузы и замеры"}
      sub={"sleep и black_box"}
      main={"sleep, таймауты, black_box, criterion."}
    >
      <V04 cues={[12.6, 29.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Целые"}
      sub={"Методы"}
      main={"checked, wrapping, биты, степени двойки."}
    >
      <V05 cues={[12.5, 29.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Дробные"}
      sub={"Методы"}
      main={"Округление, функции, проверки, total_cmp."}
    >
      <V06 cues={[12.7, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Чего нет в std"}
      sub={"num-*, rand"}
      main={"Нет трейта Number, больших чисел, случайных."}
    >
      <V07 cues={[13.6, 27.7]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Особые типы"}
      sub={"Wrapping, NonZero"}
      main={"Wrapping, Saturating, NonZero и ниши."}
    >
      <V08 cues={[13.2, 30.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Размеры"}
      sub={"size_of и раскладка"}
      main={"Размеры &T, &str, String, dyn; кэш."}
    >
      <V09 cues={[17.3, 26.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Низкоуровневое"}
      sub={"transmute и другие"}
      main={"transmute, ManuallyDrop, MaybeUninit, discriminant."}
    >
      <V10 cues={[13.6, 25.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Хеш и случайность"}
      sub={"Hasher и ГПСЧ"}
      main={"SipHash, стабильные хеши, свой генератор."}
    >
      <V11 cues={[13.2, 25.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Выделение памяти"}
      sub={"Куча и арены"}
      main={"global_allocator, арены."}
    >
      <V12 cues={[8.8, 28.0]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — каталог трейтов std."}
    >
      <V13 cues={[15.1, 24.3]} />
    </Slide>
  );
}

export const SLIDES_R28 = {
  "10:28": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R28).
export const SLIDE_TITLES_R28 = {
  "10:28": [
    "Введение",
    "Duration",
    "Instant",
    "Паузы",
    "Целые",
    "Дробные",
    "Нет в std",
    "Особые",
    "Размеры",
    "mem",
    "Хеш",
    "Аллокаторы",
    "Итоги",
  ],
};
