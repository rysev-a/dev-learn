// Слайды для «Изучаем Rust», глава 13 — «Классы, трейты и перегрузка операторов».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs13.jsx).

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
} from "../anim/Rs13.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 13</span>
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
      title={"Классы Python и Rust"}
      sub={"Глава 13 · struct, impl, trait"}
      main={
        "struct — данные, impl — методы, trait — поведение; операторы — тоже трейты."
      }
    >
      <V01 cues={[19.6, 33.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Класс"}
      sub={"new, self, pub"}
      main={"Нет конструкторов; self в трёх видах; pub открывает доступ."}
    >
      <V02 cues={[13.6, 28.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Свойства и методы класса"}
      sub={"Геттеры и ассоциированные функции"}
      main={
        "Геттеры и сеттеры — методы; classmethod — ассоциированная функция."
      }
    >
      <V03 cues={[16.0, 30.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Наследование"}
      sub={"Композиция"}
      main={"Нет наследования: композиция и трейты."}
    >
      <V04 cues={[11.3, 30.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Трейт"}
      sub={"trait и impl for"}
      main={"Описание поведения; реализация отдельно."}
    >
      <V05 cues={[17.6, 24.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Полиморфизм"}
      sub={"impl Trait и dyn Trait"}
      main={"Методы по умолчанию, статическая и динамическая диспетчеризация."}
    >
      <V06 cues={[12.3, 25.0]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Display и Debug"}
      sub={"__str__ и __repr__"}
      main={"Display — для людей, Debug — для программистов."}
    >
      <V07 cues={[14.8, 28.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Сравнение"}
      sub={"PartialEq, PartialOrd, Hash"}
      main={
        "derive сравнивает поля по порядку; Eq и Ord — для полных порядков."
      }
    >
      <V08 cues={[15.2, 25.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Операторы"}
      sub={"Add и компания"}
      main={"impl Add, Output, AddAssign, Index."}
    >
      <V09 cues={[9.6, 27.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Детали операторов"}
      sub={"Ссылки и newtype"}
      main={"Операторы для ссылок; согласованность; newtype."}
    >
      <V10 cues={[13.1, 31.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Iterator и Drop"}
      sub={"__iter__ и __exit__"}
      main={"next() даёт for и методы; Drop заменяет with."}
    >
      <V11 cues={[13.6, 33.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"dataclass"}
      sub={"derive"}
      main={"Debug, Clone, PartialEq, Default; Clone против Copy."}
    >
      <V12 cues={[13.9, 28.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — словари и множества."}
    >
      <V13 cues={[13.1, 28.7]} />
    </Slide>
  );
}

export const SLIDES_R13 = {
  "10:13": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R13).
export const SLIDE_TITLES_R13 = {
  "10:13": [
    "Введение",
    "Класс",
    "Свойства",
    "Наследование",
    "Трейт",
    "Полиморфизм",
    "Display",
    "Сравнение",
    "Операторы",
    "Детали",
    "Iterator",
    "derive",
    "Итоги",
  ],
};
