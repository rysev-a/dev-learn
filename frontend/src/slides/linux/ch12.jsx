// Слайды для «Погружаемся в Unix», глава 12 — «Загрузка, systemd и пакеты».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Os12.jsx).

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
} from "../anim/Os12.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СЕТЬ И СЛУЖБЫ / ГЛАВА 12</span>
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
      title={"От кнопки до служб"}
      sub={"Глава 12 · Загрузка и systemd"}
      main={
        "Прошивка, загрузчик, ядро, systemd — каждая ступень запускает следующую."
      }
    >
      <V01 cues={[5.3, 16.9, 25.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"UEFI и загрузчик"}
      sub={"Ядро и параметры"}
      main={"Загрузчик кладёт в память ядро и initramfs и передаёт параметры."}
    >
      <V02 cues={[10.5, 22.1, 30.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"initramfs"}
      sub={"Поиск настоящего корня"}
      main={"Начальный образ открывает диск и переключает корень на настоящий."}
    >
      <V03 cues={[8.8, 20.6, 26.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Юниты"}
      sub={"Service, socket, timer, mount, target"}
      main={"Юнит описывается тремя секциями: что, как и куда подключить."}
    >
      <V04 cues={[6.9, 19.6, 23.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Зависимости"}
      sub={"Requires, Wants, After"}
      main={"Граф зависимостей позволяет стартовать независимое параллельно."}
    >
      <V05 cues={[9.9, 18.9, 25.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Сокетная активация"}
      sub={"Служба по первому соединению"}
      main={"systemd слушает порт за службу; таймеры заменяют cron."}
    >
      <V06 cues={[13.1, 16.9, 26.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Перезапуски и лимиты"}
      sub={"Restart и StartLimit"}
      main={"Лимит запусков останавливает цикл падений."}
    >
      <V07 cues={[11.0, 19.4, 29.0]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"cgroup и песочница"}
      sub={"Ресурсы и защита службы"}
      main={
        "Своя cgroup даёт лимиты и чистую остановку; песочница отнимает лишнее."
      }
    >
      <V08 cues={[6.7, 18.8, 28.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Журнал"}
      sub={"journald и journalctl"}
      main={"Структурированный журнал фильтруют по юниту, уровню и времени."}
    >
      <V09 cues={[3.9, 14.9, 23.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Пакеты"}
      sub={"Зависимости, версии, уборка"}
      main={"Менеджер сам выбирает версии и порядок установки."}
    >
      <V10 cues={[9.9, 16.7, 25.7]} />
    </Slide>
  );
}

export const SLIDES_LX12 = {
  "8:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_LX12).
export const SLIDE_TITLES_LX12 = {
  "8:12": [
    "Введение",
    "Загрузчик",
    "initramfs",
    "Юниты",
    "Зависимости",
    "Сокеты и таймеры",
    "Перезапуски",
    "cgroup и защита",
    "Журнал",
    "Пакеты",
  ],
};
