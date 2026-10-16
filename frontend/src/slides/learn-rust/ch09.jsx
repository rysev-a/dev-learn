// Слайды для «Изучаем Rust», глава 9 — «Типы данных: объекты Python и значения Rust».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs09.jsx).

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
} from "../anim/Rs09.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 9</span>
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
      title={"Объект и значение"}
      sub={"Глава 9 · Python → Rust"}
      main={
        "В Python значение — объект, переменная — ссылка; в Rust значение лежит в переменной."
      }
    >
      <V01 cues={[11.2, 22.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Память"}
      sub={"28 байт против 4"}
      main={"Список указателей против вектора подряд."}
    >
      <V02 cues={[14.4, 21.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Целые"}
      sub={"Без границ против i32"}
      main={"int без границ против типов с размером; i128 и bigint."}
    >
      <V03 cues={[14.1, 26.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Деление"}
      sub={"// против /"}
      main={"Вниз против к нулю; div_euclid и rem_euclid."}
    >
      <V04 cues={[11.8, 23.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Дробные"}
      sub={"IEEE 754"}
      main={"Одинаковый стандарт; round и смешивание типов."}
    >
      <V05 cues={[13.1, 19.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"bool и None"}
      sub={"Логика и пустота"}
      main={"bool не число; только bool в условиях; Option вместо None."}
    >
      <V06 cues={[8.9, 22.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Строки"}
      sub={"Символы и байты"}
      main={"len в байтах; bytes ↔ &[u8]; char — отдельный тип."}
    >
      <V07 cues={[10.0, 28.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Присваивание"}
      sub={"Ссылка, копия, перемещение"}
      main={"b = a в Python — ссылка; в Rust — копия или перемещение."}
    >
      <V08 cues={[12.3, 20.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Типизация"}
      sub={"Динамическая и статическая"}
      main={
        "Тип у значения против типа у переменной; утиная типизация и трейты."
      }
    >
      <V09 cues={[9.9, 26.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Раскладка"}
      sub={"size_of и выравнивание"}
      main={"size_of, padding, repr(C)."}
    >
      <V10 cues={[9.8, 25.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Стек"}
      sub={"Кадры и лимиты"}
      main={"Кадр вызова; RecursionError против stack overflow."}
    >
      <V11 cues={[18.4, 26.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Байты чисел"}
      sub={"Дополнительный код и порядок байтов"}
      main={"to_le_bytes и to_be_bytes; to_bytes в Python."}
    >
      <V12 cues={[15.1, 22.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — функции и условные конструкции."}
    >
      <V13 cues={[13.7, 24.4]} />
    </Slide>
  );
}

export const SLIDES_R9 = {
  "10:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R9).
export const SLIDE_TITLES_R9 = {
  "10:9": [
    "Введение",
    "Память",
    "Целые",
    "Деление",
    "Дробные",
    "bool, None",
    "Строки",
    "Присваивание",
    "Типизация",
    "Раскладка",
    "Стек",
    "Байты",
    "Итоги",
  ],
};
