// Слайды для «Современный Frontend», глава 18 — «Сеть: fetch, CORS, WebSocket и Server-Sent Events».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js18.jsx).

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
} from "../anim/Js18.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В БРАУЗЕРЕ / ГЛАВА 18</span>
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
      title={"Сеть как основа"}
      sub={"Глава 18 · Браузер и сервер"}
      main={"Сеть — основа фронтенда."}
    >
      <V01 cues={[14.4, 30.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"fetch"}
      sub={"Request, Response, Headers"}
      main={"404 — не ошибка fetch."}
    >
      <V02 cues={[11.8, 24.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Запрос и ответ"}
      sub={"Тело, json(), clone()"}
      main={"Тело читается один раз."}
    >
      <V03 cues={[13.4, 18.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Потоки"}
      sub={"ReadableStream, буфер"}
      main={"Куски копят в буфере."}
    >
      <V04 cues={[7.7, 21.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Отмена и повторы"}
      sub={"AbortController, backoff"}
      main={"Повторяют только идемпотентное."}
    >
      <V05 cues={[13.1, 23.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"CORS"}
      sub={"Источник и preflight"}
      main={"CORS настраивает сервер."}
    >
      <V06 cues={[18.5, 34.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Кеширование"}
      sub={"Cache-Control и ETag"}
      main={"304 экономит трафик."}
    >
      <V07 cues={[11.8, 26.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Авторизация"}
      sub={"Куки и токены"}
      main={"Одно обновление токена на всех."}
    >
      <V08 cues={[13.6, 19.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"HTTP/2 и HTTP/3"}
      sub={"Мультиплексирование и QUIC"}
      main={"Включается на сервере и в CDN."}
    >
      <V09 cues={[7.6, 25.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"WebSocket"}
      sub={"Двусторонний канал"}
      main={"Переподключение — дело клиента."}
    >
      <V10 cues={[14.1, 20.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Server-Sent Events"}
      sub={"EventSource"}
      main={"Односторонний поток с реконнектом."}
    >
      <V11 cues={[14.4, 20.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Сетевой слой"}
      sub={"Очередь, откат, дедупликация"}
      main={"Ошибки — по-человечески."}
    >
      <V12 cues={[10.0, 29.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — сервис-воркеры."}
    >
      <V13 cues={[13.0, 21.1]} />
    </Slide>
  );
}

export const SLIDES_J18 = {
  "11:18": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J18).
export const SLIDE_TITLES_J18 = {
  "11:18": [
    "Введение",
    "fetch",
    "Тело",
    "Потоки",
    "Отмена",
    "CORS",
    "Кеш",
    "Авторизация",
    "HTTP",
    "WebSocket",
    "SSE",
    "Слой",
    "Итоги",
  ],
};
