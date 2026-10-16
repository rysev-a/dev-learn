// Слайды для «Погружаемся в Unix», глава 14 — «Модули, драйверы и наблюдаемость».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Os14.jsx).

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
} from "../anim/Os14.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗОЛЯЦИЯ И ЯДРО / ГЛАВА 14", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Ядро растёт и наблюдается"}
      sub={"Глава 14 · Модули и наблюдаемость"}
      main={
        "Ядро подключает драйверы на лету и даёт десяток способов заглянуть внутрь."
      }
    >
      <V01 cues={[5.7, 16.4, 26.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Устройства"}
      sub={"/dev, major и minor, udev"}
      main={"Файлы устройств создаёт udev по событиям ядра."}
    >
      <V02 cues={[11.6, 20.1, 24.7]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Модель устройств"}
      sub={"Шина, устройство, драйвер"}
      main={
        "Идентификатор устройства находит драйвер; нужный модуль загружается сам."
      }
    >
      <V03 cues={[10.5, 17.1, 27.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Модули"}
      sub={"lsmod, modprobe, подписи"}
      main={
        "modprobe учитывает зависимости, rmmod — пользователей, подписи защищают."
      }
    >
      <V04 cues={[6.3, 17.5, 24.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Rust в ядре"}
      sub={"С 6.1 до штатного статуса в 7.0"}
      main={
        "Драйверы на Rust уже в ядре, а экспериментальный статус снят в 7.0."
      }
    >
      <V05 cues={[15.8, 16.8, 29.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"sysctl"}
      sub={"Параметры без перезагрузки"}
      main={"Менять — echo или sysctl, закреплять — файл в /etc/sysctl.d."}
    >
      <V06 cues={[4.6, 15.3, 27.5]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Журнал ядра"}
      sub={"dmesg, oops, panic, kdump"}
      main={"Начинайте разбор с dmesg; kdump сохраняет память при панике."}
    >
      <V07 cues={[11.9, 20.4, 25.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Нагрузка и давление"}
      sub={"load average, vmstat, PSI"}
      main={"Load average — симптом, vmstat и PSI показывают причину."}
    >
      <V08 cues={[7.7, 18.8, 30.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"perf и трассировка"}
      sub={"Образцы, tracepoints, kprobe"}
      main={"perf отвечает, где тратится время; трассировка — что происходило."}
    >
      <V09 cues={[5.1, 21.6, 31.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"eBPF и итог"}
      sub={"Мощный инструмент наблюдения"}
      main={"eBPF — безопасный способ задавать ядру вопросы на лету."}
    >
      <V10 cues={[3.5, 20.1, 31.0]} />
    </Slide>
  );
}

export const SLIDES_LX14 = {
  "8:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_LX14).
export const SLIDE_TITLES_LX14 = {
  "8:14": [
    "Введение",
    "/dev",
    "Драйверы",
    "Модули",
    "Rust",
    "sysctl",
    "dmesg и паника",
    "Нагрузка",
    "perf",
    "eBPF и итог",
  ],
};
