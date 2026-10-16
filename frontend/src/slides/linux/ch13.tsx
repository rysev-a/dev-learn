// Слайды для «Погружаемся в Unix», глава 13 — «Контейнеры: пространства имён и cgroup».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Os13.jsx).

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
} from "../anim/Os13.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗОЛЯЦИЯ И ЯДРО / ГЛАВА 13", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Контейнер — это процесс"}
      sub={"Глава 13 · Контейнеры"}
      main={
        "Контейнер — обычные процессы на общем ядре; в ядре нет такой сущности."
      }
    >
      <V01 cues={[11.1, 12.6, 27.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Пространства имён"}
      sub={"Восемь видов"}
      main={"Каждое пространство подменяет один тип ресурса."}
    >
      <V02 cues={[9.1, 15.6, 25.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"PID namespace"}
      sub={"Один процесс — два номера"}
      main={"Внутри нумерация с единицы, а PID 1 отвечает за сирот."}
    >
      <V03 cues={[8.5, 17.3, 27.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Корень и монтирование"}
      sub={"mount namespace и pivot_root"}
      main={"pivot_root подменяет корень, хозяйская файловая система исчезает."}
    >
      <V04 cues={[10.1, 21.4, 25.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Сеть"}
      sub={"veth, мост, NAT, порты"}
      main={"Опубликованный порт — это правило пересылки внутрь."}
    >
      <V05 cues={[5.8, 19.2, 26.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Пользователи"}
      sub={"Отображение uid"}
      main={
        "root внутри — обычный uid снаружи: так работают rootless-контейнеры."
      }
    >
      <V06 cues={[6.5, 21.4, 29.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"cgroup v2"}
      sub={"Лимиты ресурсов"}
      main={"memory.max и cpu.max ограничивают потребление группы."}
    >
      <V07 cues={[7.6, 15.2, 28.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Образы и overlayfs"}
      sub={"Слои и copy-up"}
      main={"Слои общие, у каждого контейнера — тонкая записываемая добавка."}
    >
      <V08 cues={[7.7, 15.5, 32.4]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Защита"}
      sub={"Capabilities, seccomp, LSM"}
      main={"Контейнер — не виртуальная машина: ядро общее."}
    >
      <V09 cues={[7.8, 15.8, 26.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Запуск и здоровье"}
      sub={"runtime, OCI, проверки, теги"}
      main={"Закрепляйте теги и описывайте проверки здоровья."}
    >
      <V10 cues={[12.4, 15.1, 30.2]} />
    </Slide>
  );
}

export const SLIDES_LX13 = {
  "8:13": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_LX13).
export const SLIDE_TITLES_LX13 = {
  "8:13": [
    "Введение",
    "Namespaces",
    "PID",
    "Корень",
    "Сеть",
    "User namespace",
    "cgroup v2",
    "Образы",
    "Защита",
    "Запуск",
  ],
};
