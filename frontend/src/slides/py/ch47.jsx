// Слайды для «Python как первый язык», глава 47 — «Память, сборщик мусора и слабые ссылки».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py47.jsx).

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
} from "../anim/Py47.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / ПИТОН ИЗНУТРИ / ГЛАВА 47</span>
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
      title={"Память автоматическая"}
      sub={"Но понимать её нужно"}
      main={"Утечки и задержки — следствия устройства памяти."}
    >
      <V01 cues={[13.7, 28.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Имена и объекты"}
      sub={"Ссылки, id, is"}
      main={"Присваивание копирует ссылку, а не объект."}
    >
      <V02 cues={[13.1, 31.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Счётчик ссылок"}
      sub={"Первый механизм"}
      main={"Ноль ссылок — немедленное освобождение."}
    >
      <V03 cues={[12.3, 25.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"__del__"}
      sub={"Финализатор"}
      main={"Ресурсы закрывайте явно."}
    >
      <V04 cues={[15.6, 25.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Циклы"}
      sub={"Когда счётчика мало"}
      main={"Недостижимые циклы убирает сборщик gc."}
    >
      <V05 cues={[11.9, 25.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Поколения"}
      sub={"Как работает сборщик"}
      main={"Не опирайтесь на детали алгоритма."}
    >
      <V06 cues={[19.7, 24.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сколько занимает"}
      sub={"getsizeof и tracemalloc"}
      main={"Для плотных данных — array или NumPy."}
    >
      <V07 cues={[10.2, 23.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Слабые ссылки"}
      sub={"weakref.ref"}
      main={"Слабая ссылка не удерживает объект."}
    >
      <V08 cues={[16.7, 21.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Слабые коллекции"}
      sub={"И weakref.finalize"}
      main={"finalize надёжнее __del__."}
    >
      <V09 cues={[13.1, 23.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Утечки"}
      sub={"Причины и поиск"}
      main={"Чаще всего — кэши и подписки."}
    >
      <V10 cues={[22.9, 28.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Копирование"}
      sub={"copy и deepcopy"}
      main={"memo спасает от циклов, __deepcopy__ управляет копией."}
    >
      <V11 cues={[11.6, 29.2]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Распределитель"}
      sub={"pymalloc"}
      main={"Память не всегда возвращается ОС."}
    >
      <V12 cues={[15.4, 27.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Память в Питоне"}
      main={"Ссылки, сборщик, слабые ссылки, измерения."}
    >
      <V13 cues={[8.4, 19.6, 27.6]} />
    </Slide>
  );
}

export const SLIDES_P47 = {
  "13:47": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P47).
export const SLIDE_TITLES_P47 = {
  "13:47": [
    "Зачем знать",
    "Имена и объекты",
    "refcount",
    "__del__",
    "Циклы",
    "Поколения",
    "Измерения",
    "weakref",
    "Слабые коллекции",
    "Утечки",
    "Копирование",
    "pymalloc",
    "Итоги",
  ],
};
