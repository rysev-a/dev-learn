// Слайды для «Современный Frontend», глава 17 — «Формы, валидация и хранилища: localStorage, cookie, IndexedDB, History API».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js17.jsx).

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
} from "../anim/Js17.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 17</span>
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
      title={"Путь данных"}
      sub={"Глава 17 · От формы до хранилища"}
      main={"Введённое нужно проверить, отправить и не потерять."}
    >
      <V01 cues={[16.6, 26.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Элементы форм"}
      sub={"Поля, label, autocomplete"}
      main={"Каждому полю — имя и подпись."}
    >
      <V02 cues={[15.6, 26.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Отправка"}
      sub={"FormData и кодирование"}
      main={"В набор попадают только поля с именем и не отключённые."}
    >
      <V03 cues={[14.5, 28.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Валидация"}
      sub={"Constraint Validation"}
      main={"validity читается программно."}
    >
      <V04 cues={[12.3, 34.3]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Клиент и сервер"}
      sub={"Сообщения и фокус"}
      main={"Клиентская проверка — не защита."}
    >
      <V05 cues={[11.1, 25.8]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Состояние формы"}
      sub={"Контролируемые поля, черновики"}
      main={"Предупреждайте о несохранённых изменениях."}
    >
      <V06 cues={[17.1, 26.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Cookie"}
      sub={"Set-Cookie и атрибуты"}
      main={"Сессию — в HttpOnly-куки."}
    >
      <V07 cues={[10.8, 30.0]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Web Storage"}
      sub={"localStorage и sessionStorage"}
      main={"Секретам там не место."}
    >
      <V08 cues={[12.2, 31.0]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"IndexedDB"}
      sub={"Транзакции и индексы"}
      main={"Схема меняется при увеличении версии."}
    >
      <V09 cues={[13.3, 31.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"URL и History"}
      sub={"pushState и popstate"}
      main={"Адрес — часть состояния приложения."}
    >
      <V10 cues={[12.4, 27.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Роутер"}
      sub={"Перехват кликов"}
      main={"Сервер отдаёт главную страницу на любой путь."}
    >
      <V11 cues={[14.8, 30.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Безопасность хранения"}
      sub={"XSS, CSRF, приватность"}
      main={"Скрипты страницы читают всё, что доступно им."}
    >
      <V12 cues={[12.1, 25.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide n={13} title={"Итоги"} sub={"Что дальше"} main={"Дальше — сеть."}>
      <V13 cues={[13.6, 23.4]} />
    </Slide>
  );
}

export const SLIDES_J17 = {
  "11:17": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J17).
export const SLIDE_TITLES_J17 = {
  "11:17": [
    "Введение",
    "Поля",
    "Отправка",
    "Валидация",
    "Клиент и сервер",
    "Состояние",
    "Cookie",
    "Web Storage",
    "IndexedDB",
    "History",
    "Роутер",
    "Безопасность",
    "Итоги",
  ],
};
