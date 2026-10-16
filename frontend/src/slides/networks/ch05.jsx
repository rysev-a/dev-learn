// Слайды для «Компьютерные сети», глава 5 — «Маршрутизация: таблицы, ARP, ICMP и traceroute».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt05.jsx).

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
} from "../anim/Nt05.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОСНОВЫ СЕТЕЙ / ГЛАВА 5</span>
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
      title={"Кто выбирает дорогу"}
      sub={"Маршрутизатор и его таблица"}
      main={
        "Пакет не знает дороги: на каждом шаге маршрутизатор выбирает следующий по своей таблице."
      }
    >
      <V01 cues={[9.0, 14.1, 15.1]} />
      <div className="s-note">
        План: таблица, самый длинный префикс, ARP, TTL, ICMP, traceroute.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Таблица маршрутов"}
      sub={"Откуда берутся записи"}
      main={
        "Записи бывают подключённые, статические, динамические и маршрут по умолчанию 0.0.0.0/0."
      }
    >
      <V02 cues={[12.9, 19.0, 27.3]} />
      <div className="s-note">
        Нет следующего шага — получатель в той же сети.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Самый длинный префикс"}
      sub={"Если подходит несколько записей"}
      main={
        "Побеждает запись с самым длинным префиксом; 0.0.0.0/0 выбирается последней."
      }
    >
      <V03 cues={[7.8, 15.3, 25.8]} />
      <div className="s-note">
        Общий маршрут плюс исключения — так устроена вся маршрутизация.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Один шаг пересылки"}
      sub={"Что делает маршрутизатор с кадром"}
      main={
        "Приём, TTL−1, поиск по таблице, ARP следующего шага и новый кадр; IP-адреса прежние."
      }
    >
      <V04 cues={[8.4, 18.6, 29.1]} />
      <div className="s-note">
        Меняются кадр, TTL и контрольная сумма пакета.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"ARP"}
      sub={"Как узнать MAC следующего шага"}
      main={
        "ARP спрашивает всех «у кого этот IP?», хозяин отвечает, ответ живёт в кэше пару минут."
      }
    >
      <V05 cues={[6.7, 17.9, 28.3]} />
      <div className="s-note">
        Первый пакет к новому соседу чуть медленнее остальных.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"TTL и петли"}
      sub={"Защита от вечного хождения"}
      main={
        "Каждый маршрутизатор уменьшает TTL; на нуле пакет выбрасывается и приходит ICMP time exceeded."
      }
    >
      <V06 cues={[10.1, 17.1, 26.8]} />
      <div className="s-note">Стартовое TTL обычно 64 или 128.</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"ICMP"}
      sub={"Служебные сообщения сети"}
      main={
        "ICMP: эхо (ping), недоступно, time exceeded, перенаправление — без него сеть слепа."
      }
    >
      <V07 cues={[8.6, 16.4, 25.6]} />
      <div className="s-note">
        Файрвол не стоит закрывать от ICMP полностью.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Traceroute"}
      sub={"TTL как фонарик"}
      main={
        "Traceroute шлёт пакеты с TTL 1, 2, 3… и по ответам time exceeded собирает список шагов."
      }
    >
      <V08 cues={[3.3, 14.4, 22.9]} />
      <div className="s-note">
        Звёздочки — ICMP заблокирован или пакет потерян.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Протоколы маршрутизации"}
      sub={"OSPF и BGP"}
      main={
        "Внутри организации карту строит OSPF, между провайдерами BGP передаёт достижимость префиксов."
      }
    >
      <V09 cues={[8.6, 17.5, 27.3]} />
      <div className="s-note">
        Сходимость — время, за которое сеть успокаивается после обрыва.
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
        "Самый длинный префикс, шаг пересылки, ARP, TTL и ICMP — основа маршрутизации; дальше транспорт."
      }
    >
      <V10 cues={[10.6, 13.6, 20.6]} />
      <div className="s-note">Дальше — UDP и сокеты.</div>
    </Slide>
  );
}

export const SLIDES_NT5 = {
  "15:5": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT5).
export const SLIDE_TITLES_NT5 = {
  "15:5": [
    "Кто выбирает дорогу",
    "Таблица маршрутов",
    "Самый длинный префикс",
    "Шаг пересылки",
    "ARP",
    "TTL и петли",
    "ICMP",
    "Traceroute",
    "OSPF и BGP",
    "Итоги",
  ],
};
