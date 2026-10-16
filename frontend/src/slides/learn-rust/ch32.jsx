// Слайды для «Изучаем Rust», глава 32 — «async и await: конечные автоматы и Pin».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs32.jsx).

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
} from "../anim/Rs32.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 32</span>
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
      title={"Что делает компилятор"}
      sub={"Глава 32 · Автоматы и Pin"}
      main={"Во что превращается async и зачем Pin."}
    >
      <V01 cues={[16.1, 28.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Десахаринг"}
      sub={"async fn и async-блок"}
      main={"Анонимный тип; аргументы попадают в фьючер."}
    >
      <V02 cues={[17.0, 27.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Состояния"}
      sub={"Точки .await"}
      main={"Живые переменные определяют размер."}
    >
      <V03 cues={[16.1, 30.1]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Самоссылка"}
      sub={"Зачем Pin"}
      main={"Ссылка внутрь себя ломается при перемещении."}
    >
      <V04 cues={[17.4, 28.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Pin и Unpin"}
      sub={"Закрепление"}
      main={"Обещание не двигать; Box::pin, pin!, Pin::new."}
    >
      <V05 cues={[15.7, 28.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Pin на практике"}
      sub={"BoxFuture, select!"}
      main={"Где встречается Pin; pin-project."}
    >
      <V06 cues={[11.5, 26.2]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Async-замыкания"}
      sub={"async |x|"}
      main={"Замыкание с async-блоком, настоящие async-замыкания, AsyncFn."}
    >
      <V07 cues={[16.1, 26.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Заимствования"}
      sub={"'static и владение"}
      main={"spawn требует владения: move и Arc."}
    >
      <V08 cues={[8.4, 35.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Send"}
      sub={"Через .await"}
      main={"Rc и MutexGuard делают фьючер !Send."}
    >
      <V09 cues={[9.8, 31.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"async в трейтах"}
      sub={"Стабильно с 1.75"}
      main={"Статическая диспетчеризация; dyn и async-trait."}
    >
      <V10 cues={[16.1, 29.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Рекурсия и размер"}
      sub={"Box::pin"}
      main={"Упаковка рекурсии; большие фьючеры."}
    >
      <V11 cues={[18.5, 31.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Отмена"}
      sub={"Cancel safety"}
      main={"Любой .await может быть последним."}
    >
      <V12 cues={[13.5, 30.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — tokio."}>
      <V13 cues={[16.9, 29.2]} />
    </Slide>
  );
}

export const SLIDES_R32 = {
  "10:32": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R32).
export const SLIDE_TITLES_R32 = {
  "10:32": [
    "Введение",
    "Десахаринг",
    "Состояния",
    "Самоссылка",
    "Pin",
    "На практике",
    "Замыкания",
    "Заимствования",
    "Send",
    "Трейты",
    "Рекурсия",
    "Отмена",
    "Итоги",
  ],
};
