// Слайды для «Изучаем Rust», глава 14 — «Словари Python, HashMap и множества Rust».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs14.jsx).

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
} from "../anim/Rs14.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 14</span>
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
      title={"dict и HashMap"}
      sub={"Глава 14 · Python → Rust"}
      main={"Хеш-карта, упорядоченная карта, множества."}
    >
      <V01 cues={[13.6, 32.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Создание"}
      sub={"new, from, collect"}
      main={"Нет литерала; Hash + Eq для ключей; f64 нельзя."}
    >
      <V02 cues={[13.2, 26.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Чтение"}
      sub={"get и remove"}
      main={"get возвращает Option; [] паникует."}
    >
      <V03 cues={[15.8, 26.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"entry"}
      sub={"Подсчёт слов"}
      main={"insert и entry().or_insert; идиома счётчика."}
    >
      <V04 cues={[12.4, 27.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"entry глубже"}
      sub={"or_default, and_modify"}
      main={"Группировка за один поиск."}
    >
      <V05 cues={[16.8, 24.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Перебор"}
      sub={"Порядок"}
      main={"iter, keys, values; порядок произволен."}
    >
      <V06 cues={[10.4, 25.5]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Хеширование"}
      sub={"Hash, Eq, SipHash"}
      main={"Ключи нельзя менять; SipHash; derive(Hash)."}
    >
      <V07 cues={[8.7, 27.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Владение"}
      sub={"Ключи и значения"}
      main={"insert забирает; get по &str; clone."}
    >
      <V08 cues={[6.4, 26.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"BTreeMap"}
      sub={"Отсортированная карта"}
      main={"Порядок и диапазоны; когда что брать."}
    >
      <V09 cues={[16.1, 24.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Множества"}
      sub={"HashSet, BTreeSet"}
      main={"Операции над множествами."}
    >
      <V10 cues={[10.3, 29.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Включения и слияние"}
      sub={"collect и extend"}
      main={"collect в HashMap; extend; сортировка по значению."}
    >
      <V11 cues={[18.1, 22.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Производительность"}
      sub={"O(1) и ёмкость"}
      main={"with_capacity; малые наборы; профилируйте."}
    >
      <V12 cues={[13.4, 31.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — владение и заимствование."}
    >
      <V13 cues={[10.2, 24.9]} />
    </Slide>
  );
}

export const SLIDES_R14 = {
  "10:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R14).
export const SLIDE_TITLES_R14 = {
  "10:14": [
    "Введение",
    "Создание",
    "Чтение",
    "entry",
    "entry глубже",
    "Перебор",
    "Хеширование",
    "Владение",
    "BTreeMap",
    "Множества",
    "Включения",
    "Скорость",
    "Итоги",
  ],
};
