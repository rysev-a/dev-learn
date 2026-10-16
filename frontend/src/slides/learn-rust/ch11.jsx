// Слайды для «Изучаем Rust», глава 11 — «Строки: str в Python и String в Rust».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs11.jsx).

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
} from "../anim/Rs11.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / RUST ПОСЛЕ PYTHON / ГЛАВА 11</span>
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
      title={"Таблица соответствий"}
      sub={"Глава 11 · str ↔ String"}
      main={"Каждой строковой операции Python — запись в Rust."}
    >
      <V01 cues={[12.7, 26.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Два типа"}
      sub={"&str и String"}
      main={"&str читает, String владеет; принимаем &str, возвращаем String."}
    >
      <V02 cues={[11.4, 23.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Длина и индексы"}
      sub={"Байты и символы"}
      main={"len в байтах, нет s[0], срезы по границам символов."}
    >
      <V03 cues={[13.7, 26.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Методы"}
      sub={"trim, find, contains"}
      main={"strip → trim; find → Option."}
    >
      <V04 cues={[11.1, 28.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"split и join"}
      sub={"Разбор и склейка"}
      main={"split → итератор + collect; split_once; join на срезе."}
    >
      <V05 cues={[9.9, 28.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Форматирование"}
      sub={"f-строки и format!"}
      main={"Те же спецификаторы; проверка при сборке."}
    >
      <V06 cues={[14.4, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Построение строк"}
      sub={"push_str и with_capacity"}
      main={"String растёт амортизированно; with_capacity; retain."}
    >
      <V07 cues={[11.4, 27.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Сравнение и сортировка"}
      sub={"По байтам UTF-8"}
      main={"Заглавные раньше строчных; sort_by_key с to_lowercase."}
    >
      <V08 cues={[17.4, 22.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Символы"}
      sub={"char"}
      main={"ord, chr, проверки; to_uppercase возвращает итератор."}
    >
      <V09 cues={[14.2, 32.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Юникод"}
      sub={"Точки и графемы"}
      main={"Кодовые точки, графемы, нормализация — внешние пакеты."}
    >
      <V10 cues={[15.9, 30.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Байты"}
      sub={"encode и decode"}
      main={"as_bytes, from_utf8, from_utf8_lossy; encoding_rs."}
    >
      <V11 cues={[12.8, 31.7]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Безопасность"}
      sub={"Граница UTF-8"}
      main={"Любая String — корректный UTF-8; OsString и Path."}
    >
      <V12 cues={[15.1, 20.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — списки, массивы, векторы."}
    >
      <V13 cues={[12.1, 24.1]} />
    </Slide>
  );
}

export const SLIDES_R11 = {
  "10:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R11).
export const SLIDE_TITLES_R11 = {
  "10:11": [
    "Введение",
    "Типы",
    "Индексы",
    "Методы",
    "split, join",
    "format!",
    "Построение",
    "Сортировка",
    "char",
    "Юникод",
    "Байты",
    "Безопасность",
    "Итоги",
  ],
};
