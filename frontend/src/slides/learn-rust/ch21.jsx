// Слайды для «Изучаем Rust», глава 21 — «Время жизни и умные указатели: кто и сколько живёт».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs21.jsx).

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
} from "../anim/Rs21.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 21</span>
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
      title={"Кто и сколько живёт"}
      sub={"Глава 21 · Без сборщика мусора"}
      main={
        "Один владелец и проверенные ссылки; для особых случаев — умные указатели."
      }
    >
      <V01 cues={[13.6, 24.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Время жизни"}
      sub={"Метки и правила пропуска"}
      main={"Метка 'a связывает ссылки; чаще всего компилятор выводит её сам."}
    >
      <V02 cues={[13.8, 29.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Типичные ошибки"}
      sub={"Локальное, структуры, два &mut"}
      main={
        "Чаще всего помогает не метка, а смена решения: владение, индекс, split_at_mut."
      }
    >
      <V03 cues={[7.9, 27.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Box"}
      sub={"Значение в куче"}
      main={
        "Box<T> — 8 байт на стеке; куча освобождается при выходе из области."
      }
    >
      <V04 cues={[11.0, 24.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Deref и Drop"}
      sub={"Что делает указатель умным"}
      main={
        "Deref даёт разыменование и приведение; Drop — действие при уничтожении."
      }
    >
      <V05 cues={[20.5, 27.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Rc"}
      sub={"Счётчик ссылок"}
      main={
        "Rc::clone увеличивает счётчик, данные не копируются; при нуле — освобождение."
      }
    >
      <V06 cues={[14.6, 25.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"RefCell"}
      sub={"Внутренняя изменяемость"}
      main={
        "Правила заимствования проверяются при запуске; Rc<RefCell<T>> — общий изменяемый узел."
      }
    >
      <V07 cues={[7.8, 25.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Weak"}
      sub={"Разрыв циклов"}
      main={
        "Цикл из Rc течёт; Weak не мешает освобождению, upgrade даёт Option."
      }
    >
      <V08 cues={[12.5, 25.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Arc"}
      sub={"Rc для потоков"}
      main={
        "Счётчик атомарный, поэтому медленнее; безопасность обеспечивают Send и Sync."
      }
    >
      <V09 cues={[13.5, 23.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Cow"}
      sub={"Копия при записи"}
      main={"Заимствованное или владеющее: копия только когда нужна запись."}
    >
      <V10 cues={[9.8, 28.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Размеры и mem::replace"}
      sub={"Что лежит на стеке"}
      main={
        "8 байт у обычных указателей, 16 у толстых; replace и take выручают без копий."
      }
    >
      <V11 cues={[8.1, 19.2]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Как выбирать"}
      sub={"Арена с индексами"}
      main={"Берите самое простое; часто индексы в Vec лучше Rc и RefCell."}
    >
      <V12 cues={[13.1, 27.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — модули, тесты и cargo."}
    >
      <V13 cues={[6.4, 20.9]} />
    </Slide>
  );
}

export const SLIDES_R21 = {
  "10:21": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R21).
export const SLIDE_TITLES_R21 = {
  "10:21": [
    "Введение",
    "'a",
    "Ошибки",
    "Box",
    "Deref и Drop",
    "Rc",
    "RefCell",
    "Weak",
    "Arc",
    "Cow",
    "Размеры",
    "Выбор",
    "Итоги",
  ],
};
