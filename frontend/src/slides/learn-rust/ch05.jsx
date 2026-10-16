// Слайды для «Изучаем Rust», глава 5 — «Условия и циклы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs05.jsx).

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
} from "../anim/Rs05.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 5</span>
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
      title={"Решения и повторения"}
      sub={"Глава 5 · if, циклы, match"}
      main={
        "if и match выбирают, loop, while, for повторяют; скобки блоков обязательны."
      }
    >
      <V01 cues={[14.0, 25.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"if и else if"}
      sub={"Условие — только bool"}
      main={"Без скобок вокруг условия; проверка сверху вниз."}
    >
      <V02 cues={[10.2, 25.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"if — выражение"}
      sub={"Значение ветки"}
      main={"Ветки одного типа; без else значение — ()."}
    >
      <V03 cues={[7.6, 22.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"loop"}
      sub={"Бесконечный цикл"}
      main={"Выход через break; break может вернуть значение."}
    >
      <V04 cues={[9.2, 27.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"while"}
      sub={"Пока истинно"}
      main={
        "Условие проверяется перед каждым шагом; не забывайте менять счётчик."
      }
    >
      <V05 cues={[11.9, 27.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"for и диапазоны"}
      sub={"a..b и a..=b"}
      main={"0..n без правой границы, 0..=n с ней; rev и step_by."}
    >
      <V06 cues={[10.6, 27.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"for по коллекциям"}
      sub={"chars, &v, enumerate"}
      main={"Перебор символов, элементов и пар «индекс — значение»."}
    >
      <V07 cues={[13.1, 28.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"break, continue, метки"}
      sub={"Управление циклом"}
      main={"break выходит, continue пропускает; метки выходят из вложенных."}
    >
      <V08 cues={[9.9, 20.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Четыре шаблона"}
      sub={"Сумма, счёт, максимум, поиск"}
      main={"Накопитель, счётчик, максимум и поиск с break."}
    >
      <V09 cues={[12.7, 27.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"match"}
      sub={"Выбор по образцу"}
      main={"Образцы, | и диапазоны, _ ; все случаи обязательны."}
    >
      <V10 cues={[17.6, 32.0]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ловушки"}
      sub={"Типичные ошибки"}
      main={"Ошибка на единицу, usize − 1, = вместо ==."}
    >
      <V11 cues={[16.6, 26.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={"range → .., elif → else if, while True → loop; нет truthy."}
    >
      <V12 cues={[9.7, 23.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — строки."}>
      <V13 cues={[12.8, 22.8]} />
    </Slide>
  );
}

export const SLIDES_R5 = {
  "10:5": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R5).
export const SLIDE_TITLES_R5 = {
  "10:5": [
    "Введение",
    "if",
    "if как выражение",
    "loop",
    "while",
    "for",
    "Коллекции",
    "Управление",
    "Шаблоны",
    "match",
    "Ловушки",
    "После Python",
    "Итоги",
  ],
};
