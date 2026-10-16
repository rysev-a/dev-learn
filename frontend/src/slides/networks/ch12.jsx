// Слайды для «Компьютерные сети», глава 12 — «HTTP/2 и HTTP/3: мультиплексирование и QUIC».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt12.jsx).

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
} from "../anim/Nt12.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПРИКЛАДНОЙ УРОВЕНЬ / ГЛАВА 12</span>
      <span>{String(n).padStart(2, "0")} / 10</span>
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
      title={"Страница из сотен файлов"}
      sub={"Современный веб"}
      main={
        "Страница — это HTML и десятки ресурсов, и HTTP/1.1 вынуждает отдавать их по очереди."
      }
    >
      <V01 cues={[6.4, 14.6, 23.6]} />
      <div className="s-note">Ради скорости придумывали обходные пути.</div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Боль HTTP/1.1"}
      sub={"Очередь и повторы"}
      main={
        "Очередь ответов, шесть соединений и заголовки, повторяющиеся в каждом запросе."
      }
    >
      <V02 cues={[8.7, 19.6, 29.4]} />
      <div className="s-note">
        Спрайты, шардинг и склейка — всё ради очереди.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Мультиплексирование"}
      sub={"Основа HTTP/2"}
      main={
        "Одно соединение несёт много независимых потоков: кадры чередуются без очереди."
      }
    >
      <V03 cues={[7.4, 20.1, 26.9]} />
      <div className="s-note">Двоичные кадры и приоритеты потоков.</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"HPACK"}
      sub={"Сжатие заголовков"}
      main={"Общая таблица заголовков превращает 500 байт запроса в десятки."}
    >
      <V04 cues={[12.3, 16.3, 26.8]} />
      <div className="s-note">Server push на практике не прижился.</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Блокировка на TCP"}
      sub={"Слабость HTTP/2"}
      main={
        "Одна потеря стопорит все потоки на общем TCP — на мобильных сетях HTTP/2 может быть хуже HTTP/1.1."
      }
    >
      <V05 cues={[9.4, 21.4, 25.1]} />
      <div className="s-note">Порядок байтов гарантирует TCP, а не HTTP.</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"QUIC"}
      sub={"HTTP/3 меняет транспорт"}
      main={
        "QUIC поверх UDP: надёжность, потоки и TLS внутри, потеря задерживает только свой поток."
      }
    >
      <V06 cues={[9.4, 23.3, 26.0]} />
      <div className="s-note">Реализован в пространстве пользователя.</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Рукопожатие и миграция"}
      sub={"Быстрее и устойчивее"}
      main={
        "Транспорт и шифрование договариваются за один круг, 0-RTT и миграция соединения."
      }
    >
      <V07 cues={[14.4, 15.4, 25.1]} />
      <div className="s-note">0-RTT — с оговорками про повтор запросов.</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Как узнают про HTTP/3"}
      sub={"Alt-Svc"}
      main={
        "Заголовок Alt-Svc сообщает про QUIC, но без открытого UDP/443 браузер откатится на HTTP/2."
      }
    >
      <V08 cues={[4.2, 17.1, 26.6]} />
      <div className="s-note">Корпоративные файрволы часто режут UDP.</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Что меняется для разработчика"}
      sub={"Старые приёмы"}
      main={
        "Шардинг доменов вреден, склейка необязательна, важны приоритеты, сжатие и кэш."
      }
    >
      <V09 cues={[8.9, 16.9, 26.1]} />
      <div className="s-note">
        Оптимизации под HTTP/1.1 становятся антипаттернами.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итоги главы"}
      sub={"Что унести дальше"}
      main={
        "HTTP/2 — мультиплексирование и HPACK, HTTP/3 — QUIC; чем дальше сервер и хуже канал, тем заметнее выигрыш."
      }
    >
      <V10 cues={[10.5, 19.3, 26.2]} />
      <div className="s-note">Дальше — TLS.</div>
    </Slide>
  );
}

export const SLIDES_NT12 = {
  "15:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT12).
export const SLIDE_TITLES_NT12 = {
  "15:12": [
    "Много файлов",
    "Боль HTTP/1.1",
    "Мультиплексирование",
    "HPACK",
    "Блокировка на TCP",
    "QUIC",
    "0-RTT и миграция",
    "Alt-Svc",
    "Для разработчика",
    "Итоги",
  ],
};
