// Слайды для «Погружаемся в Unix», глава 11 — «Сеть: сокеты, стек и eBPF».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Os11.jsx).

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
} from "../anim/Os11.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СЕТЬ И СЛУЖБЫ / ГЛАВА 11</span>
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
      title={"Сетевой стек"}
      sub={"Глава 11 · Сеть"}
      main={"Для программы сеть — дескриптор; всё ниже сокета делает ядро."}
    >
      <V01 cues={[10.9, 23.4, 24.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Сокеты"}
      sub={"socket, bind, listen, accept"}
      main={"После accept сеть выглядит как обычный файл."}
    >
      <V02 cues={[9.6, 17.2, 24.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Адреса и маски"}
      sub={"IPv4, CIDR, шлюз"}
      main={"Маска делит адрес на сеть и машину; в чужую сеть — через шлюз."}
    >
      <V03 cues={[11.6, 22.6, 28.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Маршрутизация"}
      sub={"Longest prefix match"}
      main={"Побеждает самый длинный префикс, 0.0.0.0/0 — запасной вариант."}
    >
      <V04 cues={[9.4, 16.2, 25.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Путь пакета"}
      sub={"DMA, NAPI, sk_buff"}
      main={"Карта кладёт кадр в память сама; ядро забирает пакеты пачкой."}
    >
      <V05 cues={[10.2, 16.2, 25.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"TCP"}
      sub={"Рукопожатие и перегрузка"}
      main={
        "Три сегмента открывают соединение, алгоритм перегрузки управляет скоростью."
      }
    >
      <V06 cues={[12.8, 19.4, 28.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"netfilter и nftables"}
      sub={"Крючки и conntrack"}
      main={
        "Правила вешаются на пять точек пути пакета; nftables сменил iptables."
      }
    >
      <V07 cues={[11.3, 18.3, 24.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Имена и DNS"}
      sub={"nsswitch и resolved"}
      main={"Сначала hosts, потом DNS; systemd-resolved кэширует ответы."}
    >
      <V08 cues={[8.4, 13.9, 27.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"eBPF и XDP"}
      sub={"Программы внутри ядра"}
      main={
        "Верификатор делает загрузку безопасной, XDP — раннюю обработку пакетов."
      }
    >
      <V09 cues={[13.1, 23.4, 24.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Диагностика"}
      sub={"Идём снизу вверх"}
      main={"Канал, адрес, маршрут, имя, порт — так находят неисправность."}
    >
      <V10 cues={[8.5, 15.3, 25.4]} />
    </Slide>
  );
}

export const SLIDES_LX11 = {
  "8:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_LX11).
export const SLIDE_TITLES_LX11 = {
  "8:11": [
    "Введение",
    "Сокеты",
    "Адреса",
    "Маршруты",
    "Путь пакета",
    "TCP",
    "nftables",
    "DNS",
    "eBPF и XDP",
    "Диагностика",
  ],
};
