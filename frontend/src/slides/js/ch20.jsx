// Слайды для «Современный Frontend», глава 20 — «Производительность: что измерять и как ускорять».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js20.jsx).

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
} from "../anim/Js20.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 20</span>
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
      title={"Что значит быстро"}
      sub={"Глава 20 · Производительность"}
      main={"Сначала измеряем, потом ускоряем."}
    >
      <V01 cues={[15.0, 29.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Core Web Vitals"}
      sub={"LCP, INP, CLS"}
      main={"Оценка — по 75-му процентилю."}
    >
      <V02 cues={[13.9, 27.7]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Критический путь"}
      sub={"Блокировки и подсказки"}
      main={"Лишние подсказки вредят."}
    >
      <V03 cues={[12.3, 30.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Меньше байтов"}
      sub={"Сжатие, картинки, шрифты"}
      main={"Резервируйте место под картинки."}
    >
      <V04 cues={[8.4, 26.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Разделение кода"}
      sub={"import() и бюджет"}
      main={"Лишнее — не на первую загрузку."}
    >
      <V05 cues={[5.6, 24.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Главный поток"}
      sub={"Долгие задачи"}
      main={"Ввод важнее фона."}
    >
      <V06 cues={[8.9, 29.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Раскладка"}
      sub={"Reflow и композитор"}
      main={"Сначала читать, потом писать."}
    >
      <V07 cues={[14.9, 21.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Виртуализация"}
      sub={"Окно и наблюдатели"}
      main={"Рисуем только видимое."}
    >
      <V08 cues={[14.1, 19.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Память"}
      sub={"Утечки и снимки"}
      main={"Отписывайтесь при уничтожении."}
    >
      <V09 cues={[15.4, 24.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Профилирование"}
      sub={"Flame chart и User Timing"}
      main={"Реальные данные — пачками."}
    >
      <V10 cues={[8.9, 20.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Кеш и переходы"}
      sub={"immutable, bfcache, спекуляции"}
      main={"Хеш в имени — год в кеше."}
    >
      <V11 cues={[9.6, 19.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Острова и бюджеты"}
      sub={"Гидратация и CI"}
      main={"Сравнивайте медианы."}
    >
      <V12 cues={[14.8, 18.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — Node.js."}>
      <V13 cues={[8.6, 20.3]} />
    </Slide>
  );
}

export const SLIDES_J20 = {
  "11:20": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J20).
export const SLIDE_TITLES_J20 = {
  "11:20": [
    "Введение",
    "Метрики",
    "Загрузка",
    "Размер",
    "Код",
    "Поток",
    "Раскладка",
    "Списки",
    "Память",
    "Профиль",
    "Кеш",
    "Бюджеты",
    "Итоги",
  ],
};
