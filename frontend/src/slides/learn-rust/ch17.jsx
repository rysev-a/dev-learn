// Слайды для «Изучаем Rust», глава 17 — «Структуры, перечисления и сопоставление с образцом».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs17.jsx).

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
} from "../anim/Rs17.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ДАННЫЕ И АБСТРАКЦИИ / ГЛАВА 17</span>
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
      title={"Произведение и сумма"}
      sub={"Глава 17 · struct, enum, match"}
      main={
        "struct — и то, и другое; enum — одно из; match — разбор с проверкой полноты."
      }
    >
      <V01 cues={[14.6, 26.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Структура и память"}
      sub={"Поля, выравнивание"}
      main={
        "Поля лежат подряд на стеке; раст сам переставляет их, repr(C) — нет."
      }
    >
      <V02 cues={[11.9, 30.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"impl и derive"}
      sub={"Методы и готовые реализации"}
      main={"Методы — в impl; derive даёт Debug, Clone, PartialEq, Default."}
    >
      <V03 cues={[10.9, 26.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Перечисления"}
      sub={"Варианты с данными"}
      main={"Значение — ровно один вариант со своими данными."}
    >
      <V04 cues={[10.1, 24.3]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Размер enum"}
      sub={"Тег и ниша"}
      main={"Размер = тег + наибольший вариант; Option<Box<T>> без тега."}
    >
      <V05 cues={[14.3, 22.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"match"}
      sub={"Исчерпывающий разбор"}
      main={"Все варианты должны быть учтены; под капотом — таблица переходов."}
    >
      <V06 cues={[13.0, 26.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Образцы"}
      sub={"Кортежи, диапазоны, охрана"}
      main={"Образцы вкладываются; охрана if и привязка @ уточняют ветвь."}
    >
      <V07 cues={[15.9, 27.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Option"}
      sub={"Вместо null"}
      main={"Нет значения — не null, а None: тип требует проверки."}
    >
      <V08 cues={[15.9, 26.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"if let и друзья"}
      sub={"Короткие формы match"}
      main={"if let, let else, while let и matches! — сокращения match."}
    >
      <V09 cues={[10.2, 22.4, 28.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"match и владение"}
      sub={"Переезд или заём"}
      main={"match по значению переносит данные, по ссылке заимствует."}
    >
      <V10 cues={[13.4, 28.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Автомат состояний"}
      sub={"Невозможное непредставимо"}
      main={"Состояния — варианты enum; переход принимает self по значению."}
    >
      <V11 cues={[10.6, 30.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Порядок, newtype, Default"}
      sub={"Полезные derive"}
      main={
        "Порядок полей — порядок сравнения; newtype бесплатен; Default собирается из полей."
      }
    >
      <V12 cues={[17.2, 23.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={
        "struct, enum, match — основа моделирования; дальше коллекции и Result."
      }
    >
      <V13 cues={[15.1, 25.4]} />
    </Slide>
  );
}

export const SLIDES_R17 = {
  "10:17": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R17).
export const SLIDE_TITLES_R17 = {
  "10:17": [
    "Введение",
    "struct",
    "impl",
    "enum",
    "Размер",
    "match",
    "Образцы",
    "Option",
    "if let",
    "Владение",
    "Состояния",
    "derive",
    "Итоги",
  ],
};
