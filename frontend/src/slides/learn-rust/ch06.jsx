// Слайды для «Изучаем Rust», глава 6 — «Строки: первое знакомство».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs06.jsx).

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
} from "../anim/Rs06.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 6</span>
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
      title={"Две строки"}
      sub={"Глава 6 · &str и String"}
      main={"&str — читаем, String — владеем и меняем."}
    >
      <V01 cues={[11.1, 27.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Литералы"}
      sub={"&'static str"}
      main={'Литерал зашит в программу и не меняется; сырые строки r"…".'}
    >
      <V02 cues={[12.0, 22.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"String"}
      sub={"Создание и рост"}
      main={"String::from, to_string, new; push и push_str; байты в куче."}
    >
      <V03 cues={[13.9, 25.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Склейка"}
      sub={"+, format!, join"}
      main={"+ забирает левую строку; format! и join ничего не забирают."}
    >
      <V04 cues={[9.5, 29.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"UTF-8"}
      sub={"Байты и символы"}
      main={"len — байты, chars().count() — символы."}
    >
      <V05 cues={[13.0, 24.7]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Индексы и срезы"}
      sub={"Границы символов"}
      main={"s[0] нельзя; срез по границам; get и nth."}
    >
      <V06 cues={[14.3, 32.5]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Перебор"}
      sub={"chars, split, lines"}
      main={"chars, bytes, char_indices, split_whitespace, lines, split."}
    >
      <V07 cues={[11.0, 21.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Методы"}
      sub={"contains, replace, trim"}
      main={"Поиск и преобразования возвращают новое значение."}
    >
      <V08 cues={[14.4, 26.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"split и parse"}
      sub={"Разбор текста в числа"}
      main={"split → trim → parse → collect; ошибки parse."}
    >
      <V09 cues={[15.4, 21.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Сравнение и типы"}
      sub={"== и преобразования"}
      main={"== между String и &str; &s, as_str, to_string; параметры — &str."}
    >
      <V10 cues={[15.1, 32.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Форматирование"}
      sub={"Ширина, точность"}
      main={"{:>10}, {:.2}, {:?}, {name}."}
    >
      <V11 cues={[17.3, 32.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={"Две строки; len в байтах; format! вместо f-строк."}
    >
      <V12 cues={[14.9, 26.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — кортежи, массивы, векторы."}
    >
      <V13 cues={[11.3, 24.3]} />
    </Slide>
  );
}

export const SLIDES_R6 = {
  "10:6": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R6).
export const SLIDE_TITLES_R6 = {
  "10:6": [
    "Введение",
    "Литералы",
    "String",
    "Склейка",
    "UTF-8",
    "Срезы",
    "Перебор",
    "Методы",
    "Разбор",
    "Сравнение",
    "Формат",
    "После Python",
    "Итоги",
  ],
};
